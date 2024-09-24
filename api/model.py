import os

import gdown
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import CSVLoader
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from more_itertools import chunked

from settings import Settings


def get_chat_prompt(prompt: str) -> ChatPromptTemplate:
    return ChatPromptTemplate.from_messages(
        [
            ('system', prompt),
            MessagesPlaceholder('history'),
            ('human', '{input}'),
        ]
    )


global_store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in global_store:
        global_store[session_id] = ChatMessageHistory()
    return global_store[session_id]


def create_conversational_rag_chain() -> RunnableWithMessageHistory:
    settings = Settings()

    llm = ChatOllama(
        model=settings.chat_model_name,
        temperature=settings.temperature,
    )
    embeddings = HuggingFaceEmbeddings(
        model_name=settings.embed_model_name,
        model_kwargs={'device': settings.device},
    )

    if not (
        os.path.exists(settings.persist_directory)
        and os.listdir(settings.persist_directory)
    ):
        gdown.download(*settings.get_drive_settings(), quiet=False)
        vectorstore = Chroma(
            collection_name=settings.collection_name,
            embedding_function=embeddings,
            persist_directory=settings.persist_directory,
        )
        loader_train = CSVLoader(
            file_path=settings.csv_name,
            metadata_columns=['id', 'category'],
            content_columns=['question', 'content'],
            encoding='utf-8',
        )
        all_documents = list(chunked(loader_train.load(), 3000))

        for documents in all_documents:
            vectorstore.add_documents(documents=documents)
    else:
        vectorstore = Chroma(
            collection_name=settings.collection_name,
            embedding_function=embeddings,
            persist_directory=settings.persist_directory,
        )

    retriever = vectorstore.as_retriever(
        search_type=settings.search_type,
        search_kwargs={
            'num_answers': settings.num_answers,
            'lambda_mult': settings.lambda_mult,
        },
    )

    contextualize_q_prompt = get_chat_prompt(settings.contextualize_q_system_prompt)
    qa_prompt = get_chat_prompt(settings.system_prompt)

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key='input',
        history_messages_key='history',
        output_messages_key='answer',
    )


conversational_rag_chain = create_conversational_rag_chain()


def get_rag_answer(session_id: str, user_input: str) -> str:
    response = conversational_rag_chain.invoke(
        user_input,
        config={'configurable': {'session_id': session_id}},
    )
    return response['answer']

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import CSVLoader
from more_itertools import chunked

from api.settings import (
    CHAT_MODEL_NAME,
    CSV_FILE_NAME,
    EMBED_MODEL_NAME,
    CONTEXTUALIZE_Q_SYSTEM_PROMPT,
    SYSTEM_PROMPT,
)

global_store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in global_store:
        global_store[session_id] = ChatMessageHistory()
    return global_store[session_id]


def create_conversational_rag_chain(
    model_name: str,
    temperature: float,
    embed_name: str,
    file_path: str,
    contextualize_q_system_prompt: str,
    system_prompt: str,
    search_type: str = 'mmr',
    num_answers: int = 5,
    lambda_mult: float = 0.25,
) -> RunnableWithMessageHistory:
    loader_train = CSVLoader(
        file_path=file_path,
        metadata_columns=['id', 'category'],
        content_columns=['question', 'content'],
        encoding='utf-8',
    )
    embeddings = HuggingFaceEmbeddings(model_name=embed_name)
    llm = ChatOllama(model=model_name, temperature=temperature)

    chroma_collection = Chroma(
        collection_name='question_answer_collection',
        embedding_function=embeddings,
        persist_directory='./vectorestore/',
    )

    documents = loader_train.load()
    batch_size = 3000
    batches = list(chunked(documents, batch_size))

    for batch in batches:
        chroma_collection.add_documents(documents=batch)

    vectorstore = chroma_collection

    retriever = vectorstore.as_retriever(
        search_type=search_type,
        search_kwargs={'num_answers': num_answers, 'lambda_mult': lambda_mult},
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ('system', contextualize_q_system_prompt),
            MessagesPlaceholder('chat_history'),
            ('human', '{input}'),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ('system', system_prompt),
            MessagesPlaceholder('chat_history'),
            ('human', '{input}'),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    return RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key='input',
        history_messages_key='chat_history',
        output_messages_key='answer',
    )


conversational_rag_chain = create_conversational_rag_chain(
    model_name=CHAT_MODEL_NAME,
    temperature=0.1,
    embed_name=EMBED_MODEL_NAME,
    file_path=CSV_FILE_NAME,
    contextualize_q_system_prompt=CONTEXTUALIZE_Q_SYSTEM_PROMPT,
    system_prompt=SYSTEM_PROMPT,
)


def get_rag_answer(session_id: str, user_input: str) -> str:
    response = conversational_rag_chain.invoke(
        {'input': user_input},
        config={'configurable': {'session_id': session_id}},
    )
    return response['answer']

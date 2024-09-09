from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.document_loaders import CSVLoader

from settings import (
    CHAT_MODEL_NAME,
    CSV_FILE_NAME,
    EMBED_MODEL_NAME,
    CONTEXTUALIZE_Q_SYSTEM_PROMPT,
    SYSTEM_PROMPT,
)


loader = CSVLoader(
    file_path=CSV_FILE_NAME,
    metadata_columns=['id', 'category'],
    content_columns=['question', 'content'],
    encoding='utf-8',
)
documents = loader.load()

vectorstore = Chroma.from_documents(
    collection_name='question_answer_collection',
    documents=documents,
    embedding=OllamaEmbeddings(model=EMBED_MODEL_NAME),
)
retriever = vectorstore.as_retriever(
    search_type='mmr',
    search_kwargs={'k': 5, 'lambda_mult': 0.25},
)


llm = ChatOllama(model=CHAT_MODEL_NAME, temperature=0.1)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', CONTEXTUALIZE_Q_SYSTEM_PROMPT),
        MessagesPlaceholder('chat_history'),
        ('human', '{input}'),
    ]
)
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)


qa_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', SYSTEM_PROMPT),
        MessagesPlaceholder('chat_history'),
        ('human', '{input}'),
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key='input',
    history_messages_key='chat_history',
    output_messages_key='answer',
)


response = conversational_rag_chain.invoke(
    {'input': 'Как взять отпуск?'},
    config={'configurable': {'session_id': '1'}},
)
response['answer']

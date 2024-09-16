import gdown


CHAT_MODEL_NAME: str = 'gemma2:2b'
EMBED_MODEL_NAME: str = 'ai-forever/ru-en-RoSBERTa'

CSV_FILE_NAME: str = 'qa-chat-bot-data.csv'
CSV_FILE_URL: str = 'https://drive.google.com/uc?id=1KAXDtvO5gNpG5FWv7RYyG1uW3ybi64TJ'

gdown.download(CSV_FILE_URL, CSV_FILE_NAME, quiet=False)


CONTEXTUALIZE_Q_SYSTEM_PROMPT: str = """
    Given a chat history and the latest user question which might reference
    context in the chat history, formulate a standalone question which can be
    understood without the chat history. Do NOT answer the question, just
    reformulate it if needed and otherwise return it as is.
"""

SYSTEM_PROMPT: str = (
    """
    You are an internal technical support assistant for employees of a large company. 

    1. Use the entire conversation history with the user to understand the context of the inquiry.
    2. Incorporate the pieces of information retrieved from the knowledge base,
        which consists of pairs of questions (user inquiries) and fixed answers (responses).
    3. Based on the current conversation, choose the most relevant question from
        the retrieved pairs, and respond with the corresponding fixed answer from the knowledge base.
    4. You must provide responses exactly as they appear in the knowledge base,
        without any modifications. All responses must be in Russian.
    """
    '\n\n{context}'
)


config: dict[str, float] = {
    'chat_model_name': CHAT_MODEL_NAME,
    'temperature': 0.1,
    'embed_model_name': EMBED_MODEL_NAME,
    'persist_dir_path': './vectorestore/',
    'file_path': CSV_FILE_NAME,
    'search_type': 'mmr',
    'num_answers': 5,
    'lambda_mult': 0.25,
    'contextualize_q_system_prompt': CONTEXTUALIZE_Q_SYSTEM_PROMPT,
    'system_prompt': SYSTEM_PROMPT,
}

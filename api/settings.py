from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    chat_model_name: str = Field()
    embed_model_name: str = Field()

    device: str = Field()
    temperature: float = Field()

    persist_directory: str = Field()
    collection_name: str = Field()
    search_type: str = Field()
    num_answers: int = Field()
    lambda_mult: float = Field()

    csv_name: str = Field()
    csv_id: str = Field()

    contextualize_q_system_prompt: str = Field("""
        Given a chat history and the latest user question which might reference
        context in the chat history, formulate a standalone question which can be
        understood without the chat history. Do NOT answer the question, just
        reformulate it if needed and otherwise return it as is.
    """)

    system_prompt: str = Field(
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

    def get_drive_settings(self) -> tuple[HttpUrl, str]:
        return f'https://drive.google.com/uc?id={self.csv_id}', self.csv_name

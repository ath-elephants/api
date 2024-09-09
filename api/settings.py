CATEGORIES: list[str] = [
    'Категория не выбрана',
    'Личный кабинет',
    'Поддержка',
    'Табель',
    'Отпуск',
    'Удаленная работа',
    'Увольнение',
    'Моя карьера',
    'Беременность и роды',
    'Отгул',
    'Прием на работу',
    'Заявки',
    'Зарплата',
    'Электронная цифровая подпись',
    'График работы',
    'Больничный',
    'Документооборот',
    'Налоговый вычет',
    'Оператор',
    'Уход за больным',
    'Справка',
    'Материальная помощь',
    'Автомобиль',
    'Обучение',
    'Доверенность',
    'Командировка',
    'ДМС',
    'Перевод',
    'Выручай-карта',
    'Служба безопасности',
    'Машиночитаемая доверенность',
    'SED',
]


CHAT_MODEL_NAME: str = 'llama3.1:8b'
EMBED_MODEL_NAME: str = 'nomic-embed-text:v1.5'

CSV_FILE_NAME: str = 'LK_modified.xlsx - Вопрос ответ.csv'


CONTEXTUALIZE_Q_SYSTEM_PROMPT: str = """
    Given a chat history and the latest user question
    which might reference context in the chat history,
    formulate a standalone question which can be understood
    without the chat history. Do NOT answer the question,
    just reformulate it if needed and otherwise return it as is.
"""

SYSTEM_PROMPT: str = (
    """
    You are an internal technical support assistant for employees of a large company. 

    1. Use the entire conversation history with the user to understand the context of the inquiry.
    2. Incorporate the pieces of information retrieved from the knowledge base,
            which consists of pairs of questions (user inquiries) and fixed answers (responses).
    3. Based on the current conversation, choose the most relevant question
            from the retrieved pairs, and respond with the corresponding fixed answer from the knowledge base.
    4. You must provide responses exactly as they appear in the knowledge base,
            without any modifications. All responses must be in Russian.
    """
    '\n\n{context}'
)

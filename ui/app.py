import requests
import streamlit as st

from messages import CATEGORIES
from utils import (
    response_generator,
    startup_page_ui,
)


session_id = startup_page_ui()

category = st.selectbox(
    'Выберите категорию обращения',
    CATEGORIES,
)

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


if prompt := st.chat_input('Введите текст обращения'):
    with st.chat_message('user'):
        st.markdown(prompt)

    st.session_state.messages.append({'role': 'user', 'content': prompt})

    content = category + '/n' + prompt
    history_message = {
        'session_id': session_id,
        'history': [{'role': 'user', 'content': content}],
    }

    try:
        response = requests.post(
            'http://fastapi:80/api/v1/get_answer/',
            json=history_message,
        )
        response.raise_for_status()
        answer = response.json()

        with st.chat_message('assistant'):
            response = st.write_stream(response_generator(answer['answer']))

        st.session_state.messages.append({'role': 'assistant', 'content': response})

    except requests.exceptions.RequestException as e:
        st.error(f'Произошла ошибка: {e}')

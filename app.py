import time
import uuid

import requests
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

from api.settings import CATEGORIES


def response_generator(response: str):
    for word in response.split():
        yield word + ' '
        time.sleep(0.05)


cookies = EncryptedCookieManager(password='password')
if not cookies.ready:
    st.stop()


session_id = cookies.get('session_id')

if session_id is None:
    session_id = str(uuid.uuid4())
    cookies['session_id'] = session_id
    cookies.save()


st.logo(
    './images/x5_tech_logo.png',
    link='https://x5-tech.ru/',
)
st.html("""
    <style>
    [alt=Logo] {
        height: 3rem;
    }
    </style>
""")

st.title('Поддержка пользователей')

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
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    with st.chat_message('user'):
        st.markdown(prompt)

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

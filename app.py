import uuid

import requests
import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

from utils.settings import CATEGORIES


cookies = EncryptedCookieManager(password='password')
if not cookies.ready:
    st.stop()


session_id = cookies.get('session_id')

if session_id is None:
    session_id = str(uuid.uuid4())
    cookies['session_id'] = session_id
    cookies.save()


st.title('Поддержка пользователей')

category = st.selectbox(
    'Выберите категорию обращения',
    CATEGORIES,
)

text = st.text_area('Введите текст обращения')

if st.button('Отправить'):
    if text:
        content = category + '/n' + text
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

            st.write('Ответ:', answer['answer'])

        except requests.exceptions.RequestException as e:
            st.error(f'Произошла ошибка: {e}')
    else:
        st.error('Пожалуйста, введите текст обращения')

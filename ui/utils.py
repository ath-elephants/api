import time
import uuid

import streamlit as st
from extra_streamlit_components import CookieManager


def startup_page_ui() -> str:
    cookie_manager = CookieManager()
    session_id: str = cookie_manager.get(cookie='ajs_anonymous_id')

    if session_id is None:
        session_id = str(uuid.uuid4())
        cookie_manager.set('ajs_anonymous_id', session_id)

    st.logo(
        './ui/x5_tech_logo.png',
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

    return session_id


def response_generator(response: str):
    for word in response.split():
        yield word + ' '
        time.sleep(0.05)

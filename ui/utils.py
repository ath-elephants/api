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

    st_body = """
        <style>
        .st-emotion-cache-13k62yr > div {
            background: linear-gradient(#000000, #003200);
        }
        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }
        .st-emotion-cache-1p2n2i4 div {
            background: rgba(0,0,0,0);
            color: rgb(250, 250, 250);
        }
        .st-bu {
            background-color: rgb(38, 39, 48);
        }
        .st-b6 > div {
            color: rgb(250, 250, 250);
        }
        </style>
    """

    st.markdown(st_body, unsafe_allow_html=True)

    st.logo('x5_tech_logo.png', link='https://x5-tech.ru/')
    st.html("""
        <style>
        [alt=Logo] {
            height: 3rem;
        }
        </style>
    """)

    st.title('Поддержка пользователей')
    st.set_page_config(page_title='X5 Tech Chatbot', page_icon='🤖')

    return session_id


def response_generator(response: str):
    for word in response.split():
        yield word + ' '
        time.sleep(0.05)

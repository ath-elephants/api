import requests
import streamlit as st

from messages import CATEGORIES
from utils import response_generator, startup_page_ui


def main():
    session_id = startup_page_ui()

    category = st.selectbox('Выберите категорию обращения', CATEGORIES)

    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {'role': 'assistant', 'content': 'Чем я могу вам помочь?'}
        ]

    if prompt := st.chat_input('Введите текст обращения'):
        st.session_state.messages.append({'role': 'user', 'content': prompt})

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    if st.session_state.messages[-1]['role'] != 'assistant':
        with st.chat_message('assistant'):
            with st.spinner('Собираю информацию...'):
                history_message = {
                    'session_id': session_id,
                    'history': [{'role': 'user', 'content': category + '/n' + prompt}],
                }

                try:
                    response = requests.post(
                        'http://fastapi:80/api/v1/get_answer/',
                        json=history_message,
                    )
                    response.raise_for_status()
                    answer = response.json()

                    response = st.write_stream(response_generator(answer['answer']))
                    st.session_state.messages.append(
                        {'role': 'assistant', 'content': response}
                    )

                except requests.exceptions.RequestException as e:
                    st.error(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    main()

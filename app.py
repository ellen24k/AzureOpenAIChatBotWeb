import streamlit as st

from langchain.chat_models import AzureChatOpenAI
from streamlit_navigation_bar import st_navbar


def menu():
    st.set_page_config(initial_sidebar_state="collapsed")

    pages = ["Home", "Library", "Tutorials", "Development", "Download"]
    styles = {
        "nav": {
            "background-color": "rgb(123, 209, 146)",
        },
        "div": {
            "max-width": "32rem",
        },
        "span": {
            "border-radius": "0.5rem",
            "color": "rgb(49, 51, 63)",
            "margin": "0 0.125rem",
            "padding": "0.4375rem 0.625rem",
        },
        "active": {
            "background-color": "rgba(255, 255, 255, 0.25)",
        },
        "hover": {
            "background-color": "rgba(255, 255, 255, 0.35)",
        },
    }

    page = st_navbar(pages, styles=styles)
    st.write(page)

    with st.sidebar:
        st.write("Sidebar")

def app_page():
    menu()
    chat_model = AzureChatOpenAI()

    st.title('3행시 갤러리 using TTS, STT, Dall-E3, Chat-GPT4o with VTube')
    user_input = st.text_input('3행시를 만들 3글자를 입력하세요:')


    if st.button('시작'):
        with st.spinner('인공지능이 단어를 가지고 삼행시를 생성 중 입니다.'):
            if user_input:
                st.write(f"[사용자]\n")
                st.write(f"{user_input}\n\n")
                result = chat_model.predict(text=user_input + '의 3글자로 3행시 만들어. 형식은 "글자: 내용," 만 작성해')

                st.write(f"[챗봇]\n")
                st.write(f"{result}\n\n")

import streamlit as st

from pkg_utils.utils import padding_set


def load_view():

    padding_set()
    # st.title('삼행시 갤러리 using STT, TTS, Dall-e3, Chat-GPT4o with LangChain, GitHub, Streamlit, Supabase Storage, PostreSQL, Azure AI, Azure Speech.')
    st.title('삼행시 갤러리 using Dall-e, Chat-GPT4o')
    # st.image("https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/diagram.png", use_column_width=True)
    st.write('만든이 : 김태영')

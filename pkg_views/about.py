import streamlit as st

from pkg_utils.utils import padding_set, read_version


def load_view():
    padding_set()
    # st.title('삼행시 갤러리 using TTS, Dall-e3, Chat-GPT4o with LangChain, GitHub, Streamlit, Supabase Storage, PostreSQL, Azure AI, Azure Speech.')
    st.title('삼행시 갤러리 using Dall-e, Chat-GPT4o')
    st.write('만든이 : 김태영')
    if st.button(f'프로그램 버전: {read_version()}'):
        st.image("resources/diagram.png", use_column_width=True)

import streamlit as st
from streamlit import secrets


from pkg_utils.utils import padding_set
from pkg_views import admin


def load_view():
    padding_set()
    # st.title('삼행시 갤러리 using STT, TTS, Dall-e3, Chat-GPT4o with LangChain, GitHub, Streamlit, Supabase Storage, PostreSQL, Azure AI, Azure Speech.')
    st.title('삼행시 갤러리 using Dall-e, Chat-GPT4o')
    # st.image("https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/diagram.png", use_column_width=True)
    st.write('만든이 : 김태영')
    st.markdown("---")

    admin_pass=st.text_input('관리자 툴 비밀번호를 입력하세요.')
    if st.button('관리자 툴'):
        if admin_pass == secrets["passwords"]["admin_password"]:
            st.session_state['admin'] = True
            admin.load_view()
            #이동
        else:
            st.error('비밀번호가 틀렸습니다.')

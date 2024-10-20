import streamlit as st

from pkg_db.db import fetch_data, delete_data
from pkg_utils.utils import padding_set


def load_view():
    padding_set()
    # st.title('삼행시 갤러리 using STT, TTS, Dall-e3, Chat-GPT4o with LangChain, GitHub, Streamlit, Supabase Storage, PostreSQL, Azure AI, Azure Speech.')
    st.title('삼행시 갤러리 using Dall-e, Chat-GPT4o')
    # st.image("https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/diagram.png", use_column_width=True)
    st.write('만든이 : 김태영')
    st.markdown("---")

    st.text_input('관리자 툴 비밀번호를 입력하세요.')
    if st.button('관리자 툴'):
        data = fetch_data()

        if data.empty:
            st.write("No data available or table does not exist.")
        else:
            for index, row in data.iterrows():
                st.image(row['img_url'], use_column_width=False, caption=f"{row['content']}", width=200)
                if st.button('삭제'):
                    delete_data(row['date'])
                    st.rerun()

                st.markdown("---")

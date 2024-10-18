import os
import streamlit as st

from app import app_page
from login import login_page

# 페이지 구성 설정
st.set_page_config(page_title="My App", layout="wide")

# CSS를 사용하여 Share, Fork, Edit 버튼 숨기기
st.markdown(
    """
    <style>
    .stApp .header {display: none;}
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    print(st.session_state['logged_in'])
    if st.session_state['logged_in']:
        app_page()
    else:
        login_page()

if __name__ == '__main__':
    main()
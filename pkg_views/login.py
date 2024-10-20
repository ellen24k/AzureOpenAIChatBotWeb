import streamlit as st

from pkg_utils.utils import padding_set


def login_page():
    st.title('삼행시 갤러리')
    #password로 하면 비밀번호 저장 화면 계속 떠서 일반 text로 변경
    password = st.text_input('입장코드를 입력하세요.[개발자의 이름 세글자]')
    correct_password = st.secrets["passwords"]["login_password"]
    st.balloons()
    if st.button('입장'):
        if password == correct_password:
            st.success('성공')
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error('입장코드가 틀렸습니다.')
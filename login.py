import streamlit as st

def login_page():
    st.title('비밀번호를 입력하세요')
    password = st.text_input('비밀번호', type='password')
    correct_password = st.secrets["passwords"]["login_password"]
    if st.button('입장'):
        if password == correct_password:
            st.success('성공')
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error('비밀번호가 틀렸습니다.')
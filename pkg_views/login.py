import streamlit as st

from pkg_utils.utils import padding_set, shorten_url, url_to_qr_code


def login_page():
    padding_set()
    st.title('삼행시 갤러리')
    #password로 하면 비밀번호 저장 화면 계속 떠서 일반 text로 변경
    password = st.text_input('입장코드를 입력하세요.[개발자의 이름 세글자]')
    correct_password = st.secrets["passwords"]["login_password"]


    if st.button('입장'):
        if password == correct_password:
            st.success('성공')
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error('입장코드가 틀렸습니다.')


    if st.button('URL 생성'):
        url = st.text_input(
            '짧은 URL 및 QR코드를 생성하기 위해 URL을 입력하세요.',
            'https://azureopenaichatbotweb-eqbdxzpg3qqrctguzxaw2a.streamlit.app/')
        if st.button('짧은 URL 생성1'):
            s_url=shorten_url(url)
            st.image(url_to_qr_code(s_url))

        url2 = st.text_input(
            '짧은 URL 및 QR코드를 생성하기 위해 URL을 입력하세요.',
            ' https://5789-115-23-174-157.ngrok-free.app ')
        if st.button('짧은 URL 생성2'):
            s_url2=shorten_url(url2)
            st.image(url_to_qr_code(s_url2))


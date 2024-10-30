import streamlit as st

from pkg_utils.utils import padding_set, shorten_url, url_to_qr_code


def login_page():
    padding_set()
    st.title('삼행시 갤러리')
    password = st.text_input('입장코드를 입력하세요.')
    correct_password = st.secrets["passwords"]["login_password"]

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.button('입장'):
        if password == correct_password:
            st.success('성공')
            st.session_state['logged_in'] = True
            st.rerun()
        else:
            st.error('입장코드가 틀렸습니다.')

    st.markdown("---")

    if 'show_element' not in st.session_state:
        st.session_state['show_element'] = False

    if st.button('짧은 URL / QR CODE'):
        st.session_state['show_element'] = not st.session_state['show_element']
        st.rerun()

    if st.session_state['show_element']:
        st.image('resources/streamlit_qr.png')
        url = st.text_input(
            'streamlit URL',
            'https://azureopenaichatbotweb-eqbdxzpg3qqrctguzxaw2a.streamlit.app')
        if st.button('streamlit short URL 생성'):
            s_url = shorten_url(url)
            st.write(s_url)

        url2 = st.text_input(
            'ngrok URL',
            'https://1-1-1-1-1.ngrok-free.app')
        if st.button('ngrok short URL/QR 생성'):
            s_url2 = shorten_url(url2)
            st.write(s_url2)
            st.image(url_to_qr_code(s_url2))

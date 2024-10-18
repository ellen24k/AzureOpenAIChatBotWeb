import streamlit as st

from login import login_page
from menu import menu


def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    print(st.session_state['logged_in'])
    if st.session_state['logged_in']:
        menu()
        # app_page()
    else:
        login_page()


def menu_hide():
    hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stAppToolbar {visibility: hidden;}
</style>
"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if __name__ == '__main__':
    menu_hide()
    main()

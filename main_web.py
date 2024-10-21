import streamlit as st

from pkg_utils.utils import menu_hide
from pkg_views.login import login_page
from pkg_views.menu import menu_page


def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        menu_page()
    else:
        login_page()


if __name__ == '__main__':
    menu_hide()
    main()

# ngrok http 8501

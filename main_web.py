import os
import streamlit as st

from app import app_page
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


if __name__ == '__main__':
    main()

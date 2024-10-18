import os
import streamlit as st

from app import app_page
from login import login_page

from streamlit_navigation_bar import st_navbar


def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    print(st.session_state['logged_in'])
    if st.session_state['logged_in']:
        page = st_navbar(["Home", "Documentation", "Examples", "Community", "About"])
        app_page()
        st.write(page)
    else:
        login_page()

if __name__ == '__main__':
    main()
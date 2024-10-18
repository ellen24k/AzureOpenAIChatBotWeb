import os
import streamlit as st
from streamlit_navigation_bar import st_navbar

from app import app_page
from login import login_page



def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    print(st.session_state['logged_in'])
    if st.session_state['logged_in']:
        app_page()
    else:
        login_page()

if __name__ == '__main__':
    # menu()
    main()
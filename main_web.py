import streamlit as st

from app import app_page
from login import login_page

if st.session_state['page'] == 'login' or st.session_state['page'] == '':
    login_page()
elif st.session_state['page'] == 'app':
    app_page()

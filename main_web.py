# import streamlit as st
#
# from pkg_views.login import login_page
# from menu import menu
#
#
# def main():
#     if 'logged_in' not in st.session_state:
#         st.session_state['logged_in'] = False
#
#     if st.session_state['logged_in']:
#         menu()
#     else:
#         login_page()
#
#
# def menu_hide():
#     # .stAppToolbar {visibility: hidden;}
#     hide_streamlit_style = """
# <style>
# #MainMenu {visibility: hidden;}
# footer {visibility: hidden;}
# .stToolbarActionButton {visibility: hidden;}
# </style>
# """
#     st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#
# if __name__ == '__main__':
#     menu_hide()
#     main()

import streamlit as st

audio_value = st.experimental_audio_input("Record a voice message")

if audio_value:
    st.audio(audio_value)
    st.write(audio_value._file_urls)
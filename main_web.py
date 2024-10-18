import os
import streamlit as st

from app import app_page
from login import login_page

from streamlit_navigation_bar import st_navbar

def menu():
    st.set_page_config(initial_sidebar_state="collapsed")

    pages = ["Home", "Library", "Tutorials", "Development", "Download"]
    styles = {
        "nav": {
            "background-color": "rgb(123, 209, 146)",
        },
        "div": {
            "max-width": "32rem",
        },
        "span": {
            "border-radius": "0.5rem",
            "color": "rgb(49, 51, 63)",
            "margin": "0 0.125rem",
            "padding": "0.4375rem 0.625rem",
        },
        "active": {
            "background-color": "rgba(255, 255, 255, 0.25)",
        },
        "hover": {
            "background-color": "rgba(255, 255, 255, 0.35)",
        },
    }

    page = st_navbar(pages, styles=styles)
    st.write(page)

    with st.sidebar:
        st.write("Sidebar")


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
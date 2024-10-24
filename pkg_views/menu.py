import streamlit as st
from streamlit_option_menu import option_menu

from pkg_views import home, gallery, admin, about


def menu_page():
    options = ["ChatBot", "Gallery", "Admin", "About"]

    menu_style = {
        "container": {"width:": "100%", "display": "flex", "justify-content": "space-between",
                      "padding": "0!important"},
        "icon": {"color": "white", "font-size": "1.5em"},
        "nav-link": {"color": "white", "font-size": "1.0em", "padding": "0 0.5em", "text-decoration": "none",
                     "--hover-color": "grey"},
        "nav-link-selected": {"color": "white", "font-size": "1.0em", "padding": "0 0.5em", "text-decoration": "none"},
    }

    selected_option = option_menu(
        menu_title=None,
        options=options,
        icons=["robot", "image", "lock", "book"],
        orientation="horizontal",
        styles=menu_style,
        default_index=0
    )

    def navigation():
        if 'admin' not in st.session_state:
            st.session_state['admin'] = False

        if selected_option == "ChatBot":
            home.load_view()
        elif selected_option == "Gallery":
            gallery.load_view()
        elif selected_option == "Admin":
            admin.load_view()
        elif selected_option == "About":
            about.load_view()
        elif selected_option is None:
            home.load_view()

    navigation()

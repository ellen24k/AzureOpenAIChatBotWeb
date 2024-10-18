import streamlit as st
from streamlit_option_menu import option_menu
from views import home, about, search


options = ["Home", "Search", "About"]


menu_style = {
    "container": {"width:": "100%", "display": "flex", "justify-content": "space-between", "padding": "0!important"},
    "icon": {"color": "white", "font-size": "1.5em"},
    "nav-link": {"color": "white", "font-size": "1em", "padding": "0 1em", "text-decoration": "none", "--hover-color": "grey"},
    "nav-link-selected": {"color": "white", "font-size": "1em", "padding": "0 1em", "text-decoration": "none"},
}


selected_option = option_menu(
    menu_title=None,
    options=options,
    icons=["globe2", "search", "chat"],
    orientation="horizontal",
    styles=menu_style,
    default_index=0
)


def navigation():
    if selected_option == "Home":
        home.load_view()
    elif selected_option == "Search":
        search.load_view()
    elif selected_option == "About":
        about.load_view()
    elif selected_option == None:
        home.load_view()

navigation()
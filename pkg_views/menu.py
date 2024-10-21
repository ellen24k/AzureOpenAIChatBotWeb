import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

from pkg_views import home, about, gallery, admin

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

    # JavaScript 코드 삽입
    components.html("""
        <script>
        document.addEventListener('touchstart', handleTouchStart, false);        
        document.addEventListener('touchmove', handleTouchMove, false);

        var xDown = null;                                                        
        var yDown = null;

        function getTouches(evt) {
            return evt.touches ||             // browser API
                   evt.originalEvent.touches; // jQuery
        }                                                     

        function handleTouchStart(evt) {
            const firstTouch = getTouches(evt)[0];                                      
            xDown = firstTouch.clientX;                                      
            yDown = firstTouch.clientY;                                      
        };                                                

        function handleTouchMove(evt) {
            if ( ! xDown || ! yDown ) {
                return;
            }

            var xUp = evt.touches[0].clientX;                                    
            var yUp = evt.touches[0].clientY;

            var xDiff = xDown - xUp;
            var yDiff = yDown - yUp;

            if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {/* 가장 큰 차이를 확인합니다. */
                if ( xDiff > 0 ) {
                    /* 왼쪽으로 스와이프 */ 
                    Streamlit.setComponentValue('next');
                } else {
                    /* 오른쪽으로 스와이프 */
                    Streamlit.setComponentValue('prev');
                }                       
            } 
            /* 값 재설정 */
            xDown = null;
            yDown = null;                                             
        };
        </script>
    """, height=0)

    # 스와이프 이벤트 처리
    if st.session_state.get('swipe') == 'next':
        current_index = options.index(selected_option)
        next_index = (current_index + 1) % len(options)
        selected_option = options[next_index]
        st.session_state['swipe'] = None
        st.experimental_rerun()
    elif st.session_state.get('swipe') == 'prev':
        current_index = options.index(selected_option)
        prev_index = (current_index - 1) % len(options)
        selected_option = options[prev_index]
        st.session_state['swipe'] = None
        st.experimental_rerun()

menu_page()
import streamlit as st

from pkg_utils.utils import padding_set, read_version


def load_view():
    padding_set()

    st.title('삼행시 갤러리 using Dall-e-3, Chat-GPT4')
    st.write('만든이 : 김태영')
    # if st.button(f'프로그램 버전: {read_version()}'):
        # st.image(f"resources/diagram_sequence_streamlit.png", use_column_width=True)
        # st.image(f"resources/diagram_sequence_database.png", use_column_width=True)
        # st.image(f"resources/diagram_deployment.png", use_column_width=True)

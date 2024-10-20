import streamlit as st
from pkg_db.db import fetch_data, delete_data, delete_file


def load_view():
    if st.session_state['admin'] == True:
        data = fetch_data()

        if data.empty:
            st.write("No data available or table does not exist.")
        else:
            for index, row in data.iterrows():
                st.image(row['img_url'], use_column_width=False, caption=f"{row['content']}", width=200)
                if st.button(row['date'] + ' 삭제'):
                    delete_data(row['date'])
                    delete_file("ChatBotFiles", row['date'] + '.png')
                    delete_file("ChatBotFiles", row['date'] + '.wav')
                    st.rerun()

                st.markdown("---")
    else:
        st.write('관리자만 접근 가능합니다.')

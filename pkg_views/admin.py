from datetime import datetime

import streamlit as st
from pkg_db.db import fetch_data, delete_data, delete_file
from pkg_utils.utils import padding_set


def load_view():
    padding_set()

    if st.session_state['logged_in'] == False or st.session_state['admin'] == False:
        admin_pass = st.text_input('관리자 비밀번호를 입력하세요.')
        if st.button('관리자 로그인'):
            if admin_pass != st.secrets["passwords"]["admin_password"]:
                st.error('비밀번호가 틀렸습니다.')
                st.stop()
            else:
                st.session_state['admin'] = True
                st.write('관리자 로그인 성공')
                st.rerun()
    else:
        st.title('관리자')

        data = fetch_data()

        if data.empty:
            st.write("No data available or table does not exist.")
        else:
            for index, row in data.iterrows():
                st.image(row['img_url'], use_column_width=True, caption=f"{row['content']}")
                if st.button(row['date'] + ' 삭제'):
                    delete_data(row['date'])
                    file_name = datetime.strptime(row['date'], "%Y-%m-%dT%H:%M:%S.%f").strftime("%Y%m%d%H%M%S%f")
                    delete_file("ChatBotFiles", file_name + '.png')
                    delete_file("ChatBotFiles", file_name + '.wav')
                    st.rerun()

                st.markdown("---")

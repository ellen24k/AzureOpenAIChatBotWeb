# import streamlit as st
#
# from pkg_db.db import fetch_all_data
# from pkg_utils.utils import padding_set
#
#
# def load_view():
#     padding_set()
#     data = fetch_all_data()
#     if data.empty:
#         st.write("No data available or table does not exist.")
#     else:
#         for index, row in data.iterrows():
#             st.subheader(f"**{row['title']}**")
#             st.image(row['img_url'], use_column_width=True, caption=f"{row['content']}")
#             st.audio(row['wav_url'], format='audio/wav')
#             st.markdown("---")
#
#

import streamlit as st
from streamlit.runtime.media_file_storage import MediaFileStorageError

from pkg_db.db import fetch_all_data
from pkg_utils.utils import padding_set


def load_view():
    padding_set()
    data = fetch_all_data()
    if data.empty:
        st.write("No data available or table does not exist.")
    else:
        for index, row in data.iterrows():
            st.subheader(f"**{row['title']}**")
            try:
                st.image(row['img_url'], use_column_width=True, caption=f"{row['content']}")
            except MediaFileStorageError as e:
                st.error(f"이미지를 불러오는 중 오류가 발생했습니다: {e}")
            st.audio(row['wav_url'], format='audio/wav')
            st.markdown("---")


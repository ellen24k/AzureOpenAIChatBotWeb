import streamlit as st

from pkg_db.db import fetch_data
from pkg_utils.utils import extract_sv_value


def load_view():

    data = fetch_data()

    if data.empty:
        st.write("No data available or table does not exist.")
    else:
        for index, row in data.iterrows():
            st.subheader(row['title'])
            try:
                st.image(row['img_url'], use_column_width=True)
            except Exception as e:
                st.image("default_img.png", use_column_width=True)
            st.write("보관기간 :" + extract_sv_value(row['img_url']))
            st.write(f"**Date:** {row['date']}")
            st.write(f"**Content:** {row['content']}")
            st.markdown("---")

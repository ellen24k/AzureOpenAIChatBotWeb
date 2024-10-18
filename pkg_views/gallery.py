from supabase import create_client, Client
import pandas as pd
import streamlit as st
from postgrest import APIError

from pkg_db.db import fetch_data


def load_view():

    st.title('Supabase Data Gallery')

    data = fetch_data()
    st.write(data)

    if data.empty:
        st.write("No data available or table does not exist.")
    else:
        for index, row in data.iterrows():
            st.subheader(row['title'])
            try:
                st.image(row['img_url'], use_column_width=True)
            except Exception as e:
                st.image("default_img.png", use_column_width=True)
            st.write(f"**Date:** {row['date']}")
            st.write(f"**Content:** {row['content']}")
            st.markdown("---")


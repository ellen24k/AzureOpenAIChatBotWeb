import streamlit as st

from pkg_db.db import fetch_data
from pkg_utils.utils import padding_set


def load_view():
    padding_set()

    data = fetch_data()

    if data.empty:
        st.write("No data available or table does not exist.")
    else:
        for index, row in data.iterrows():
            st.subheader(f"**{row['title']}**")
            st.image(row['img_url'], use_column_width=True, caption=f"{row['content']}")
            # st.write(f"{row['date']}")
            st.audio(row['wav_url'], format='audio/wav')
            # st.image(row['img_url'], use_column_width=True)
            # st.write(f"**Expired** : {extract_ske_value(row['img_url'])}")
            # st.write(f"**Content:**\n\n{row['content']}")
            st.markdown("---")

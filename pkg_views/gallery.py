from datetime import datetime

import streamlit as st

from pkg_db.db import fetch_data
from pkg_utils.utils import extract_ske_value


def load_view():

    data = fetch_data()

    if data.empty:
        st.write("No data available or table does not exist.")
    else:
        for index, row in data.iterrows():
            st.subheader(row['title'])

            # if extract_sv_value(row['img_url']) >= datetime.today().strftime('%Y-%m-%d'):
            #     img_url ="resources/default_img.png"
            #     st.image(img_url, use_column_width=True)
            # else:
            #    st.image(row['img_url'], use_column_width=True)
            # st.write(extract_sv_value(row['img_url']) + "~" + datetime.today().strftime('%Y-%m-%d')))

            # st.image(row['img_url'], use_column_width=True, caption=row['img_url'])
            st.image(row['img_url'], use_column_width=True)
            st.write(f"**Date:** {row['date']}")
            # st.write(f"**Expired** : {extract_ske_value(row['img_url'])}")
            st.write(f"**Content:**\n\n{row['content']}")
            st.markdown("---")

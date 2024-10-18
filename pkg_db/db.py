from supabase import create_client, Client
import pandas as pd
import streamlit as st
from postgrest import APIError

supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(supabase_url, supabase_key)


def fetch_data():
    try:
        response = supabase.table('data').select('*').execute()
        data = response.data
        return pd.DataFrame(data)
    except APIError as e:
        st.error(f"Error fetching data: {e.message}")
        return pd.DataFrame()


def insert_data(img_url, title, content):
    try:
        response = supabase.table('data').insert({
            'img_url': img_url,
            'title': title,
            'content': content
        }).execute()
        return response
    except APIError as e:
        return None


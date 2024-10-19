from supabase import create_client, Client
import pandas as pd
import streamlit as st
from postgrest import APIError

supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(supabase_url, supabase_key)


def fetch_data():
    try:
        response = supabase.table('data').select('*').order('date', desc=True).execute()
        data = response.data
        return pd.DataFrame(data)
    except APIError as e:
        st.error(f"Error fetching data: {e.message}")
        return pd.DataFrame()


def insert_data(img_url, wav_url, title, content):
    try:
        response = supabase.table('data').insert({
            'img_url': img_url,
            'wav_url': wav_url,
            'title': title,
            'content': content
        }).execute()
        return response
    except APIError as e:
        return None


def upload_file(bucket_name: str, src_file_path: str, dest_file_name: str) -> str:
    try:
        with open(src_file_path, "rb") as file:
            file_content = file.read()
        response = supabase.storage.from_(bucket_name).upload(dest_file_name, file_content)
        public_url = supabase.storage.from_(bucket_name).get_public_url(dest_file_name)
        print(public_url)
        return public_url
    except APIError as e:
        return f"Error uploading file: {e.message}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"
import pandas as pd
import requests
import streamlit as st
from postgrest import APIError
from supabase import create_client, Client

supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
bucket_name = st.secrets["BUCKET_NAME"]

supabase: Client = create_client(supabase_url, supabase_key)


def fetch_all_data():
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


def delete_data(date):
    try:
        response = supabase.table('data').delete().eq('date', date).execute()
        return response
    except APIError as e:
        return None


def file_upload(bucket_name: str, src_file_path: str, dest_file_name: str) -> str:
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


def file_delete(bucket_name: str, file_name: str) -> str:
    try:
        response = supabase.storage.from_(bucket_name).remove(file_name)
        print(response)
        return response
    except APIError as e:
        return f"Error deleting file: {e.message}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def supabase_function_invoke(img_url, file_name):
    supabase_storage_base_url = 'https://uzefbkvgsuzmopxjxymz.supabase.co/storage/v1/object/public/ChatBotFiles/'
    default_img_url = 'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/default.png'

    try:
        response = supabase.functions.invoke(
            "download_file",
            invoke_options={
                "body": {
                    "bucket_name": bucket_name,
                    "name": "Functions",
                    "img_url": img_url,
                    "file_name": file_name
                },
                "headers": {
                    f'Authorization': f'Bearer {supabase_key}'
                },
            },
        )
        print("---------------------" + response)
        ret_url = supabase_storage_base_url + file_name
        return ret_url
    except APIError as e:
        print(f"Error invoking function: {e.message}")
        return default_img_url
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return default_img_url

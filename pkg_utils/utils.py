import shutil
from datetime import datetime
from urllib.parse import urlparse, parse_qs

import pyshorteners
import requests
import streamlit as st
import streamlit.components.v1 as components


def copy_file(source_file, destination_file):
    shutil.copy(source_file, destination_file)
    print(f"파일이 {source_file}에서 {destination_file}로 복사되었습니다.")


def download_file(url, destination_file):
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(destination_file, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    print(f"파일이 {url}에서 {destination_file}로 다운로드되었습니다.")


def get_current_time_no_spaces():
    return datetime.now().strftime('%Y%m%d%H%M%S%f')


def extract_ske_value(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    sv_value = query_params.get('ske', [None])[0]
    return sv_value


def autoplay_audio(file_path):
    audio_html = f"""
    <audio autoplay style="display:none;">
      <source src="{file_path}" type="audio/wav">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


def padding_set():
    css = """
    <style>
    .stMainBlockContainer.block-container.st-emotion-cache-13ln4jf.ea3mdgi5 {
        padding-top: 48px;
        padding-right: 4px;
        padding-bottom: 4px;
        padding-left: 4px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def shorten_url(url):
    s = pyshorteners.Shortener()
    ret_url = s.tinyurl.short(url)
    return ret_url


def url_to_qr_code(url):
    qr_code = f"https://api.qrserver.com/v1/create-qr-code/?size=400x400&data={url}"
    return qr_code


def extract_filename(url):
    start = url.rfind('/') + 1
    end = url.find('?', start)
    if start != -1 and end != -1:
        return url[start:end]
    return None


def scroll_here():
    html_code = """
                        <div id="scroll-target" style="margin-top: 1000px;"></div>
                        <script>
                          function scrollToTarget() {
                            document.getElementById('scroll-target').scrollIntoView({ behavior: 'smooth' });
                          }
                          window.onload = scrollToTarget;
                        </script>
                    """

    components.html(html_code, height=0)


def menu_hide():
    # .stAppToolbar {visibility: hidden;}
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stToolbarActionButton {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def read_version(file_path='version.txt'):
    with open(file_path, 'r') as file:
        version = file.read().strip()
    return version
import shutil
from datetime import datetime

import pyshorteners
import requests
import streamlit as st


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


# def autoSelectDevice():
#     p = pyaudio.PyAudio()
#     audioDeviceIndex1 = None
#     audioDeviceIndex2 = None
#     devices = p.get_device_count()
#     for i in range(devices):
#         device_info = p.get_device_info_by_index(i)
#         if device_info.get('maxInputChannels') <= 0:
#             if audioDeviceIndex1 == None and 'CABLE Input(VB-Audio Virtual Ca' in device_info.get('name'):
#                 audioDeviceIndex1 = device_info.get('index')
#             elif audioDeviceIndex2 == None and '스피커(Realtek(R) Audio)' in device_info.get('name'):
#                 # PHL 328M6FJR2
#                 # 스피커(Realtek(R) Audio)
#                 audioDeviceIndex2 = device_info.get('index')
#
#     print(f"audioDeviceIndex1: {audioDeviceIndex1}, audioDeviceIndex2: {audioDeviceIndex2}")
#     return audioDeviceIndex1, audioDeviceIndex2
from urllib.parse import urlparse, parse_qs


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
        padding-right: 2px;
        padding-bottom: 2px;
        padding-left: 2px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def live_2d():
    html_code = """
    <head>
        <meta charset="UTF-8">
        <title>live2d-demo</title>
        <script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
        <!-- Live2DCubismCore -->
        <script src="https://cdn.jsdelivr.net/gh/litstronger/live2d-moc3@master/js/frame/live2dcubismcore.min.js"></script>
        <!-- Include Pixi. -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pixi.js/4.6.1/pixi.min.js"></script>
        <!-- Include Cubism Components. -->
        <script src="https://cdn.jsdelivr.net/gh/litstronger/live2d-moc3@master/js/live2dcubismframework.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/litstronger/live2d-moc3@master/js/live2dcubismpixi.js"></script>
        <!-- User's Script -->
        <script src="https://cdn.jsdelivr.net/gh/litstronger/live2d-moc3@master/js/l2d.js"></script>
        <script src="https://cdn.jsdelivr.net/gh/litstronger/live2d-moc3@master/js/main.js"></script>
        <style>
        </style>
    </head>
    <body>
        <div id="layered-content" style="position: fixed; top: 300px; left: 200px; z-index: 1000;">
            <div class="Canvas"  id="L2dCanvas"></div>
                <script>
                    var config = {
                        width: 400,
                        height: 400,
                        left: '0px',
                        bottom: '0px',
                        basePath: 'https://cdn.jsdelivr.net/gh/alg-wiki/AzurLaneL2DViewer@gh-pages/assets',
                        role: 'bisimai_2',
                        background: 'transparent',
                        opacity: 1,
                        mobile: true
                    }
                    var v = new Viewer(config); 
            </script>
        </div>
    </body>
    """

    st.components.v1.html(html_code, height=400)



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
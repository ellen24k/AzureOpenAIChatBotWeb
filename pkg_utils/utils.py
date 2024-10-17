import os
import shutil
from datetime import datetime

import requests

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

def save_text_to_file(text, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"텍스트가 {file_path}에 저장되었습니다.")

def get_current_time_no_spaces():
    return datetime.now().strftime('%Y%m%d%H%M%S')

def make_history(generate_text, img_url, wav_file):

    try :
        now = get_current_time_no_spaces()
        if (img_url == 'default_img'):
            copy_file(f'resources/default_img.png', f'history/' + now + '.png')
        else:
            download_file(img_url, f'history/' + now + '.png')
        copy_file(wav_file, f'history/' + now + '.wav')
        save_text_to_file(generate_text, f'history/' + now + '.txt')
        return now
    except Exception as e:
        print(f"Error making history: {e}")
        return

def extract_title_from_txt(filename):
    with open(f'history/{filename}.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    temp = text.split(',')
    title = ''.join([line.split(':')[0].strip() for line in temp])
    return title

def delete_history(filename):
    try:
        os.remove(f'history/{filename}.png')
        os.remove(f'history/{filename}.wav')
        os.remove(f'history/{filename}.txt')
        print(f'history {filename} deleted.')
    except Exception as e:
        print(f"Error deleting history: {e}")

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


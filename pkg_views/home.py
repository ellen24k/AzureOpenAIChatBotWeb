import os
from time import sleep

import streamlit as st

from pkg_db.db import insert_data, file_upload
from pkg_utils.ProgressBar import ProgressBar
from pkg_utils.chat import make_poem
from pkg_utils.dalle import generate_image
from pkg_utils.tts import synthesize_speech
from pkg_utils.utils import autoplay_audio, get_current_time_no_spaces, download_file, padding_set, scroll_here


def load_view():
    padding_set()
    img_url = None
    content = None

    user_input = st.text_input('**삼행시를 만들 세글자를 입력하세요.**')

    if len(user_input) != 3:
        st.error('세글자를 입력해주세요.')
    else:
        if st.button('삼행시 만들기'):
            file_name = get_current_time_no_spaces()
            pbar = ProgressBar('작업을 시작합니다.')
            with pbar:
                autoplay_audio(
                    'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/msg_wait.wav')
                pbar.change_progress('인공지능이 단어를 가지고 삼행시를 생성 중 입니다. 잠시만 기다려주세요.', 0, 20)
                content = make_poem(user_input)
                sleep(3)

                autoplay_audio(
                    'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/snd_bg.wav')

                pbar.change_progress('이미지를 생성 중 입니다.', 20, 30)
                img_url = generate_image(content)  #

                if not img_url:
                    img_url = "https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/default_img.png"
                    pbar.change_progress('이미지 생성에 실패했습니다. 기본 이미지를 사용합니다.', 30, 50)
                else:
                    pbar.change_progress('이미지 생성이 완료되었습니다.', 30, 50)

                pbar.change_progress('오디오를 생성 중 입니다.', 50, 60)
                synthesize_speech(content, filename='temp/' + file_name + '.wav', ssml=True)
                pbar.change_progress('오디오 생성이 완료되었습니다.', 60, 70)

                pbar.change_progress('데이터를 저장 중 입니다.', 70, 80)
                download_file(img_url, 'temp/' + file_name + '.png')
                png_file_url = file_upload("ChatBotFiles", 'temp/' + file_name + '.png', file_name + '.png')
                wav_file_url = file_upload("ChatBotFiles", 'temp/' + file_name + '.wav', file_name + '.wav')
                insert_data(png_file_url, wav_file_url, user_input, content)

                st.title(user_input)
                st.image(png_file_url, use_column_width=True, caption=f'{content}')
                st.audio(wav_file_url, format='audio/wav', autoplay=True)
                pbar.change_progress('결과를 출력 하는 중 입니다.', 80, 90)

                pbar.change_progress('작업을 완료 하는 중 입니다.', 90, 100)
                pbar.empty()

                scroll_here()
                st.balloons()

                try:
                    os.remove('temp/' + file_name + '.png')
                    os.remove('temp/' + file_name + '.wav')
                except Exception as e:
                    print(e)

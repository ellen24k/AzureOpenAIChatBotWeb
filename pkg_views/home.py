import asyncio
import os
from time import sleep

import streamlit as st

from pkg_db.db import insert_data, file_upload
from pkg_utils.ProgressBar import ProgressBar
from pkg_utils.chat import make_poem
from pkg_utils.dalle import generate_image_async
from pkg_utils.tts import synthesize_speech
from pkg_utils.utils import autoplay_audio, get_current_time_no_spaces, download_file, padding_set, scroll_here


def on_image_generated(img_url, file_name, pbar, user_input, content):
    if not img_url:
        img_url = "https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/default_img.png"
        pbar.change_progress('이미지 생성에 실패했습니다. 기본 이미지를 사용합니다.', 10)
    else:
        pbar.change_progress('이미지 생성이 완료되었습니다.', 10)

    download_file(img_url, 'temp/' + file_name + '.png')
    png_file_url = file_upload("ChatBotFiles", 'temp/' + file_name + '.png', file_name + '.png')
    pbar.change_progress('이미지 파일이 저장되었습니다.', 10)

    st.title(user_input)
    st.image(img_url, use_column_width=True, caption=f'{content}')

    return png_file_url


def load_view():
    padding_set()
    img_url = None
    content = None
    png_file_url = None
    wav_file_url = None

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
                pbar.change_progress('인공지능이 단어를 가지고 삼행시를 생성 중 입니다. 잠시만 기다려주세요.', 5)
                content = make_poem(user_input)
                pbar.change_progress('삼행시가 생성되었습니다.', 10)

                autoplay_audio(
                    'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/snd_bg.wav')

                pbar.change_progress('이미지를 생성 중 입니다.', 5)

                async def async_gen_image():
                    img_url = await generate_image_async(content, test=True)
                    png_file_url = on_image_generated(img_url, file_name, pbar, user_input, content)
                    return img_url, png_file_url

                img_url, png_file_url = asyncio.run(async_gen_image())

                pbar.change_progress('오디오를 생성 중 입니다.', 5)
                synthesize_speech(content, filename='temp/' + file_name + '.wav', ssml=True)
                pbar.change_progress('오디오 생성이 완료되었습니다.', 10)
                wav_file_url = file_upload("ChatBotFiles", 'temp/' + file_name + '.wav', file_name + '.wav')
                pbar.change_progress('오디오 파일이 저장되었습니다.', 10)

                limit = 10
                while png_file_url is None or wav_file_url is None:
                    print("w", img_url, png_file_url, wav_file_url)
                    sleep(0.5)
                    limit -= 1
                    if limit == 0:
                        if png_file_url is None:
                            png_file_url = "https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/default_img.png"
                        if wav_file_url is None:
                            wav_file_url = "https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/default_wav.png"
                        break

                insert_data(png_file_url, wav_file_url, user_input, content)
                pbar.change_progress('데이타베이스에 자료가 저장되었습니다.', 10)

                pbar.empty()

                st.audio(wav_file_url, format='audio/wav', autoplay=True)

                try:
                    os.remove('temp/' + file_name + '.png')
                    os.remove('temp/' + file_name + '.wav')
                except Exception as e:
                    print(e)

                st.balloons()
                scroll_here()

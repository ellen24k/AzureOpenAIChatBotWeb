import os
import threading

import streamlit as st

from pkg_db.db import insert_data, file_upload
from pkg_utils.ProgressBar import ProgressBar
from pkg_utils.chat import make_poem
from pkg_utils.dalle import generate_image_sync
from pkg_utils.tts import synthesize_speech
from pkg_utils.utils import autoplay_audio, get_current_time_no_spaces
from pkg_utils.utils import download_file, padding_set, scroll_here, read_version

devmode = False
fastmode = True
dalletestmode = False


def gen_image_thread(content, file_name, pbar, user_input):
    img_url = generate_image_sync(content, dalletestmode)
    return img_url


def save_image_to_supabase(dalle_img_url, file_name, pbar):
    if not fastmode:
        pbar.change_progress('이미지 파일을 저장 중 입니다.', 10)
        download_file(dalle_img_url, 'temp/' + file_name + '.png')
        png_file_url = file_upload("ChatBotFiles", 'temp/' + file_name + '.png', file_name + '.png')
        return png_file_url
    else:
        return dalle_img_url


def remove_temp_files(file_name):
    try:
        if not fastmode:
            os.remove('temp/' + file_name + '.png')
        os.remove('temp/' + file_name + '.wav')
    except Exception as e:
        print(e)


def generate_poem():
    user_input = st.session_state['user_input']
    st.session_state['user_input'] = None

    dalle_img_url = None
    file_name = get_current_time_no_spaces()
    pbar = ProgressBar('')

    with pbar:
        autoplay_audio(
            'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/msg_wait.wav')
        pbar.change_progress('인공지능이 단어를 가지고 삼행시를 생성 중 입니다. 잠시만 기다려주세요.', 10)
        content = make_poem(user_input)

        def run_gen_image():
            nonlocal dalle_img_url
            dalle_img_url = gen_image_thread(content, file_name, pbar, user_input)

        thread_img = threading.Thread(target=run_gen_image)
        thread_img.start()
        # 쓰레드 뒤로 옮겨서 이미지 생성이 먼저 되도록 함.
        pbar.change_progress('이미지를 생성 중 입니다.', 30)

        autoplay_audio(
            'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/snd_bg.wav')

        pbar.change_progress('오디오를 생성 중 입니다.', 10)
        synthesize_speech(content, filename='temp/' + file_name + '.wav', ssml=True)

        pbar.change_progress('오디오 파일을 저장 중 입니다.', 10)
        wav_file_url = file_upload("ChatBotFiles", 'temp/' + file_name + '.wav', file_name + '.wav')

        pbar.change_progress('이미지 생성 작업을 마무리 중 입니다.', 10)
        thread_img.join()

        if not dalle_img_url:
            dalle_img_url = "https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/default_img.png"
            pbar.change_progress('이미지 생성에 실패했습니다. 기본 이미지를 사용합니다.', 10)
        else:
            pbar.change_progress('이미지 생성이 완료되었습니다.', 10)

        png_file_url = save_image_to_supabase(dalle_img_url, file_name, pbar)
        st.title(user_input)
        st.image(dalle_img_url, use_column_width=True, caption=f'{content}')
        st.audio(wav_file_url, format='audio/wav', autoplay=True)

        pbar.change_progress('작업한 내용을 데이타베이스에 저장 중 입니다.', 10)
        insert_data(png_file_url, wav_file_url, user_input, content)

        pbar.empty()

        st.balloons()
        scroll_here()

        remove_temp_files(file_name)


def load_view():
    padding_set()
    if devmode:
        st.write(f'[v{read_version()}] DEBUG MODE')
        if fastmode:
            st.write('fastmode on')
        if dalletestmode:
            st.write('dalletestmode on')

    if 'user_input' not in st.session_state:
        st.session_state['user_input'] = None

    if st.session_state['user_input'] is None:
        user_input = st.text_input('**삼행시를 만들 세글자를 입력하세요.**', max_chars=3)
        if len(user_input) != 3:
            st.error('세글자를 입력해주세요.')
        else:
            if st.button('삼행시 만들기'):
                st.session_state['user_input'] = user_input
                st.rerun()
    else:
        generate_poem()



import os
import time

import streamlit as st
from streamlit import spinner

from pkg_db.db import insert_data, upload_file
from pkg_utils.chat import make_poem
from pkg_utils.dalle import generate_image
from pkg_utils.sst import recognize_speech
from pkg_utils.tts import synthesize_speech
from pkg_utils.utils import autoplay_audio, get_current_time_no_spaces, download_file, padding_set, live_2d


def load_view():
    live_2d()
    padding_set()
    img_url = None
    content = None

    if 'mic_input' not in st.session_state:
        st.session_state['mic_input'] = ''

    if st.button('마이크로 입력하기'):
        with spinner('마이크가 작동중 입니다. 지금 말하세요.'):
            try:
                recognition_result = recognize_speech()
            except Exception as e:
                st.error(f'마이크 입력에 실패했습니다.')
                recognition_result = None

            if recognition_result:
                st.session_state['mic_input'] = recognition_result.replace('.', '')
            else:
                st.session_state['mic_input'] = ''
                st.info('마이크 입력 버튼을 다시 누르거나 직접 입력하세요.')

    user_input = st.text_input('**삼행시를 만들 세글자를 입력하세요.**', value=st.session_state['mic_input'])

    if len(user_input) != 3:
        st.error('세글자를 입력해주세요.')
    else:
        if st.button('삼행시 만들기'):
            file_name = get_current_time_no_spaces()

            with st.spinner('인공지능이 단어를 가지고 삼행시를 생성 중 입니다. 잠시만 기다려주세요.'):
                autoplay_audio(
                    'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/msg_wait.wav')
                # st.audio('https://uzefbkvgsuzmopxjxymz.supabase.co/storage/v1/object/public/ChatBotFiles/beep.wav', format='audio/wav', autoplay=True)
                content = make_poem(user_input)
                time.sleep(5)  #

            if content:
                st.success('삼행시 생성이 완료되었습니다.')

            with st.spinner('Dall-e3 가 이미지를 생성 중 입니다.'):
                autoplay_audio(
                    'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/snd_bg.wav')
                img_url = generate_image(content)  #

            if not img_url:
                img_url = "https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/default_img.png"
                st.warning('이미지 생성에 실패했습니다. 기본 이미지를 사용합니다.')
            else:
                st.success('이미지 생성이 완료되었습니다.')

            with st.spinner('오디오를 생성 중 입니다.'):
                synthesize_speech(content, filename='temp/' + file_name + '.wav', ssml=True)
                st.success('오디오 생성이 완료되었습니다.')

            # with st.spinner('이미지와 오디오를 출력 중 입니다.'):
            st.balloons()
            st.image(img_url, use_column_width=True, caption=f'{content}')
            st.audio('temp/' + file_name + '.wav', format='audio/wav', autoplay=True)


            with st.spinner('데이터를 저장 중 입니다.'):
                download_file(img_url, 'temp/' + file_name + '.png')
                png_file_url = upload_file("ChatBotFiles", 'temp/' + file_name + '.png', file_name + '.png')
                wav_file_url = upload_file("ChatBotFiles", 'temp/' + file_name + '.wav', file_name + '.wav')
                insert_data(png_file_url, wav_file_url, user_input, content)
                st.success('데이터 저장이 완료되었습니다.')

            with st.spinner('임시파일을 제거합니다.'):
                os.remove('temp/' + file_name + '.png')
                os.remove('temp/' + file_name + '.wav')
                st.info('임시파일을 제거했습니다.')

            st.success('모든 작업이 완료 되었습니다.')
            st.session_state['mic_input'] = ''

    # 뻐끔뻐끔
    # 이미지나 wav까지 스크롤
import time

import streamlit as st

from pkg_db.db import insert_data, upload_file
from pkg_utils.chat import make_poem
from pkg_utils.dalle import generate_image
from pkg_utils.stt import synthesize_speech
from pkg_utils.utils import autoplay_audio, get_current_time_no_spaces, download_file
import os

def load_view():

    img_url = None
    content = None

    user_input = st.text_input('**삼행시를 만들 3글자를 입력하세요:**')

    if st.button('3행시 만들기'):
        file_name = get_current_time_no_spaces()

        with st.spinner('인공지능이 단어를 가지고 삼행시를 생성 중 입니다. 잠시만 기다려주세요.'):
            autoplay_audio(
                'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/msg_wait.wav')
            # st.audio('https://uzefbkvgsuzmopxjxymz.supabase.co/storage/v1/object/public/ChatBotFiles/beep.wav', format='audio/wav', autoplay=True)
            content = make_poem(user_input)
            time.sleep(5)  #

        with st.spinner('Dall-e3 가 이미지를 생성 중 입니다.'):
            autoplay_audio(
                'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/snd_bg.wav')
            img_url = generate_image(content)  #

        if not img_url:
            img_url = "https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/default_img.png"
            st.write('부적절한 단어가 사용되어 기본 이미지를 사용합니다.')

        with st.spinner('오디오를 생성 중 입니다.'):
            synthesize_speech(content, filename='temp/' + file_name + '.wav', ssml=True)

        with st.spinner('이미지와 오디오를 출력 중 입니다.'):
            st.image(img_url, use_column_width=True, caption=f'{content}')
            st.audio('temp/' + file_name + '.wav', format='audio/wav', autoplay=True)

        with st.spinner('데이터를 저장 중 입니다.'):
            download_file(img_url, 'temp/' + file_name + '.png')
            png_file_url = upload_file("ChatBotFiles", 'temp/' + file_name + '.png', file_name + '.png')
            wav_file_url = upload_file("ChatBotFiles", 'temp/' + file_name + '.wav', file_name + '.wav')
            insert_data(png_file_url, wav_file_url, user_input, content)

        with st.spinner('임시파일을 제거합니다.'):
            os.remove('temp/' + file_name + '.png')
            os.remove('temp/' + file_name + '.wav')

        st.success('모든 작업이 완료 되었습니다.')


    #todo 화면 좀 위로 올릴 수 있나 보기
    #todo 마이크입력 STT 처리하기
    #todo 뻐끔뻐끔
    #todo requirement  생성처리 버전까지
    #todo 입장 번호 입력
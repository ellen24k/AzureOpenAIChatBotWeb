import time

import streamlit as st

from pkg_db.db import insert_data
from pkg_utils.chat import make_poem
from pkg_utils.dalle import generate_image
from pkg_utils.mic import speech_recognize_once_from_mic
from pkg_utils.stt import synthesize_and_play_speech
from pkg_utils.utils import autoplay_audio


def load_view():
    img_url = None
    content = None

    user_input = st.text_input('**3행시를 만들 3글자를 입력하세요:**')

    if st.button('3행시 만들기'):
        with st.spinner('인공지능이 단어를 가지고 삼행시를 생성 중 입니다. 잠시만 기다려주세요.'):
            autoplay_audio(
                'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/msg_wait.wav')
            content = make_poem(user_input)
            time.sleep(5) #

        with st.spinner('Dall-e3 가 이미지를 생성 중 입니다. 잠시만 기다려주세요.'):

            autoplay_audio(
                'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/snd_bg.wav')
            # img_url = generate_image(content) #


        if not img_url:
            img_url = "https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/default_img.png"
            st.write('부적절한 단어 사용으로 기본 이미지를 사용합니다.')

        st.image(img_url, use_column_width=False, caption=f'{content}', width=400)

        # with st.spinner('시를 낭송하는 중 입니다.'):
        # synthesize_and_play_speech(content, ssml=True)

        insert_data(img_url, user_input, content)

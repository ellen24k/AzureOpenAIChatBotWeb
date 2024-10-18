from datetime import datetime

import streamlit as st

from langchain_openai import AzureChatOpenAI

from pkg_db.db import insert_data
from pkg_utils.dalle import generate_image
from pkg_utils.stt import synthesize_and_play_speech
from pkg_utils.utils import extract_ske_value


def make_poem(user_input):
    chat_model = AzureChatOpenAI()
    st.write(f"[사용자]\n")
    st.write(f"{user_input}\n\n")
    result = chat_model.invoke(input=user_input + '의 3글자로 3행시 만들어. 형식은 세줄로 "글자: 내용" 만 작성해')
    st.write(f"[챗봇]\n")
    st.write(f"{result.content}\n\n")
    return result.content

def load_view():

    img_url = None
    content = None

    user_input = st.text_input('**3행시를 만들 3글자를 입력하세요:**')
    if st.button('3행시 만들기'):
        with st.spinner('인공지능이 단어를 가지고 삼행시를 생성 중 입니다.'):
            content = make_poem(user_input)
        with st.spinner('이미지를 생성하는 중 입니다. 잠시만 기다려주세요.'):
            img_url = generate_image(content)
            st.image(img_url, use_column_width=True, caption='Dall-E3 이미지 생성 결과')
        with st.spinner('시를 낭송하는 중 입니다.'):
            synthesize_and_play_speech(user_input, ssml=True)

        if not img_url:
            img_url ="resources/default_img.png"

        insert_data(img_url, user_input, content)

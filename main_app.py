import os

import streamlit as st
# import asyncio
# from pkg_azure_ai import chatbot
# from pkg_azure_ai.dalle import generate_image
from pkg_db.db import DatabaseManager
# from pkg_utils.utils import make_history


# 로그인 상태를 저장할 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# URL 매개변수 확인
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["login"])[0]

# 페이지 전환
if page == "main_app" and st.session_state['logged_in']:
    st.write("환영합니다! 메인 앱 페이지입니다.")
    if st.button("로그아웃"):
        st.session_state['logged_in'] = False
        st.experimental_set_query_params(page="login")
        st.success("로그아웃 되었습니다.")
else:
    st.experimental_set_query_params(page="login")
    st.error("로그인이 필요합니다.")

# Streamlit 애플리케이션 설정
st.title('3행시 갤러리 using TTS, STT, Dall-E3, Chat-GPT4o with VTube')

# 데이터베이스 초기화
db = DatabaseManager()

# 사용자 입력 받기
user_input = st.text_input('3행시를 만들 3글자를 입력하세요:')

if st.button('시작'):
    if user_input:
        st.write(f"[사용자]\n{user_input}\n")
        st.write('인공지능이 단어를 가지고 삼행시를 생성 중 입니다.')

        # 챗봇 응답 생성
        # generated_text = chatbot.chat(user_input)
        # st.write(f"[챗봇]\n{generated_text}\n\n")

        # 이미지 생성
        # img_url = asyncio.run(generate_image(generated_text))

        # if img_url is not None:
        # now = make_history(generated_text, img_url, f'temp/gen_text.wav')
        # else:
        #     st.write("부적절한 단어 사용등의 이유로 이미지 생성이 취소되었습니다. 기본이미지로 저장합니다.")
        # now = make_history(generated_text, 'default_img', f'temp/gen_text.wav')

        # 데이터베이스에 저장
        # db.add_data(now, user_input)

        # 생성된 이미지 표시
        # st.image(img_url if img_url else 'default_img', caption='Generated Image')

# 히스토리 표시
st.write('히스토리')
all_data = db.select_all_data()
for row in all_data:
    st.write(row[1])

for row in all_data:
    file_id = row[0]
    title = row[1]
    st.write(f"Title: {title}")

    # 이미지 표시
    img_path = f'history/{file_id}.png'
    if os.path.exists(img_path):
        st.image(img_path, caption=title)

    # 버튼을 클릭하면 wav 파일 재생
    if st.button(f"Play {title}"):
        wav_path = f'history/{file_id}.wav'
        if os.path.exists(wav_path):
            audio_file = open(wav_path, 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/wav')
        else:
            st.write("WAV 파일을 찾을 수 없습니다.")


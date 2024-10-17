import os
import streamlit as st
import streamlit_authenticator as stauth
from pkg_db.db import DatabaseManager

# 사용자 정보 설정
names = ["User"]
usernames = ["user"]
passwords = ["password"]

# 해시된 비밀번호 생성
hashed_passwords = stauth.Hasher(passwords).generate()

# 인증자 객체 생성
authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "some_cookie_name", "some_signature_key")

# 로그인 위젯
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.session_state['logged_in'] = True
    st.write(f"환영합니다, {name}님!")
    if st.button("로그아웃"):
        authenticator.logout("Logout", "main")
        st.session_state['logged_in'] = False
        st.experimental_set_query_params(page="login")
        st.success("로그아웃 되었습니다.")
elif authentication_status == False:
    st.error("사용자 이름 또는 비밀번호가 잘못되었습니다.")
elif authentication_status == None:
    st.warning("사용자 이름과 비밀번호를 입력하세요.")

# 페이지 전환
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["login"])[0]

if st.session_state.get('logged_in', False):
    if page == "main_app":
        st.write("환영합니다! 메인 앱 페이지입니다.")
    else:
        st.experimental_set_query_params(page="main_app")
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
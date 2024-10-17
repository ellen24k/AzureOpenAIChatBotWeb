import streamlit as st

# 사용자 데이터베이스 (예시)
USER_DATA = {
    "ellen": "rlaxodud",
    "user2": "password2"
}

# 로그인 상태를 저장할 세션 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 로그인 함수
def login(username, password):
    if username in USER_DATA and USER_DATA[username] == password:
        st.session_state['logged_in'] = True
        st.experimental_set_query_params(page="main_app")
        st.success("로그인 성공!")
    else:
        st.error("로그인 실패. 사용자 이름 또는 비밀번호를 확인하세요.")

# 로그아웃 함수
def logout():
    st.session_state['logged_in'] = False
    st.experimental_set_query_params(page="login")
    st.success("로그아웃 되었습니다.")

# URL 매개변수 확인
query_params = st.experimental_get_query_params()
page = query_params.get("page", ["login"])[0]

# 페이지 전환
if page == "main_app" and st.session_state['logged_in']:
    st.write("환영합니다! 메인 앱 페이지입니다.")
    if st.button("로그아웃"):
        logout()
else:
    st.title("로그인")
    username = st.text_input("사용자 이름")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        login(username, password)
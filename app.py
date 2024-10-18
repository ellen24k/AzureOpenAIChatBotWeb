import streamlit as st

from langchain.chat_models import AzureChatOpenAI


def app_page():
    chat_model = AzureChatOpenAI()

    st.title('3행시 갤러리 using TTS, STT, Dall-E3, Chat-GPT4o with VTube')
    user_input = st.text_input('3행시를 만들 3글자를 입력하세요:')


    if st.button('시작'):
        with st.spinner('인공지능이 단어를 가지고 삼행시를 생성 중 입니다.'):
            if user_input:
                st.write(f"[사용자]\n")
                st.write(f"{user_input}\n\n")
                result = chat_model.predict(text=user_input + '의 3글자로 3행시 만들어. 형식은 "글자: 내용," 만 작성해')

                st.write(f"[챗봇]\n")
                st.write(f"{result}\n\n")

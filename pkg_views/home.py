import streamlit as st

from langchain_openai import AzureChatOpenAI

from pkg_utils.mic import recognize_speech
from pkg_utils.stt import synthesize_speech, synthesize_and_play_speech


def make_poem(user_input):
    chat_model = AzureChatOpenAI()
    st.write(f"[사용자]\n")
    st.write(f"{user_input}\n\n")
    result = chat_model.invoke(input=user_input + '의 3글자로 3행시 만들어. 형식은 세줄로 "글자: 내용" 만 작성해')
    st.write(f"[챗봇]\n")
    st.write(f"{result.content}\n\n")
    return result.content

def load_view():
    st.title('3행시 갤러리 using TTS, STT, Dall-E3, Chat-GPT4o with VTube, Streamlit, Supabase, Azure.')
    user_input = None
    if st.button('마이크로 입력'):
        with st.spinner('마이크로 입력 중...'):
            user_input = recognize_speech()
        if not user_input:
            user_input = st.text_input('직접 3행시를 만들 3글자를 입력하세요:')
            if st.button('3행시 만들기'):
                with st.spinner('인공지능이 단어를 가지고 삼행시를 생성 중 입니다.'):
                    make_poem(user_input)
        else:
            st.write(user_input + ' 단어가 인식되었습니다.')
            with st.spinner('인공지능이 단어를 가지고 삼행시를 생성 중 입니다.'):
                synthesize_and_play_speech(make_poem(user_input), ssml=True)





# Add this import at the top of `views/home.py`
import streamlit as st
import speech_recognition as sr

def capture_audio():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.info("마이크를 통해 음성을 입력하세요...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ko-KR")
        st.success(f"인식된 텍스트: {text}")
        return text
    except sr.UnknownValueError:
        st.error("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        st.error(f"음성 인식 서비스에 접근할 수 없습니다: {e}")


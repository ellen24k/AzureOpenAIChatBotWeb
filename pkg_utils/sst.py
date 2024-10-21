import speech_recognition as sr
import streamlit as st


# speech_key = st.secrets["SPEECH_KEY"]
# service_region = st.secrets["SERVICE_REGION"]
#
# speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# audio_config = speechsdk.AudioConfig(use_default_microphone=True)
# speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config, language="ko-KR")
#
# def recognize_speech():
#     result = speech_recognizer.recognize_once()
#
#     if result.reason == speechsdk.ResultReason.RecognizedSpeech:
#         print("Recognized: {}".format(result.text))
#         return result.text
#     elif result.reason == speechsdk.ResultReason.NoMatch:
#         print("No speech could be recognized: {}".format(result.no_match_details))
#     elif result.reason == speechsdk.ResultReason.Canceled:
#         cancellation_details = result.cancellation_details
#         print("Speech Recognition canceled: {}".format(cancellation_details.reason))
#         if cancellation_details.reason == speechsdk.CancellationReason.Error:
#             print("Error details: {}".format(cancellation_details.error_details))
#     return None

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("마이크가 작동중 입니다. 지금 말하세요.")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="ko-KR")
        st.write(f"인식된 텍스트: {text}")
        return text
    except sr.UnknownValueError:
        st.write("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        st.write(f"음성 인식 서비스에 접근할 수 없습니다: {e}")
    return None


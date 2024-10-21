import streamlit as st
import azure.cognitiveservices.speech as speechsdk

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
    st.error('마이크 입력 기능은 현재 사용할 수 없습니다.')
    return None
    # 마이크로 입력받아 텍스트로 리턴해주는 웹브라우저에서 작동하는 함수





import streamlit as st
import azure.cognitiveservices.speech as speechsdk

try:
    speech_key = st.secrets["SPEECH_KEY"]
    service_region = st.secrets["SERVICE_REGION"]
except KeyError as e:
    raise RuntimeError(f"Missing Streamlit secret: {e}")

try:
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config, language="ko-KR")
except Exception as e:
    raise RuntimeError(f"Failed to initialize SpeechRecognizer: {e}")

def recognize_speech():
    result = speech_recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
    return None
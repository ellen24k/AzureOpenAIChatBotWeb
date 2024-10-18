import streamlit as st
import azure.cognitiveservices.speech as speechsdk

speech_key = st.secrets["SPEECH_KEY"]
service_region = st.secrets["SERVICE_REGION"]

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
audio_config = speechsdk.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config, language="ko-KR")

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

import azure.cognitiveservices.speech as speechsdk
import streamlit as st


def speech_recognize_once_from_mic():
    # Set up the speech config and audio config
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.AudioConfig(use_default_microphone=True)

    # Create a speech recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    st.write("Speak into your microphone.")
    result = speech_recognizer.recognize_once_async().get()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return f"Recognized: {result.text}"
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized"
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        return f"Speech Recognition canceled: {cancellation_details.reason}"
    else:
        return "Unknown error"

# Simple UI for processing the audio input

st.title("Azure Speech Service with Streamlit")

if st.button('Start speech recognition'):
    recognition_result = speech_recognize_once_from_mic()
    st.write(recognition_result)
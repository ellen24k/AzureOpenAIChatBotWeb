import asyncio

import streamlit as st
import azure.cognitiveservices.speech as speechsdk

speech_key = st.secrets["SPEECH_KEY"]
service_region = st.secrets["SERVICE_REGION"]

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
audio_config = speechsdk.AudioConfig(use_default_microphone=True)
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config, language="ko-KR")

async def recognize_speech():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, speech_recognizer.recognize_once)

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        # st.write("Recognized: {}".format(result.text))
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        st.write("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        st.write("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            st.write("Error details: {}".format(cancellation_details.error_details))
    return None


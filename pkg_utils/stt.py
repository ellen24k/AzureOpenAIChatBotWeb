import streamlit as st
import azure.cognitiveservices.speech as speechsdk

speech_key = st.secrets["SPEECH_KEY_S0"]
service_region = st.secrets["SERVICE_REGION_S0"]
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

def synthesize_and_play_speech(text, ssml=False, voice_name="ko-KR-JiMinNeural"):
    speech_config.speech_synthesis_voice_name = voice_name
    audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")  # 파일로 저장
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    if ssml:
        ssml_string = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='ko-KR'>
            <voice name='{voice_name}'>
                <prosody rate='-10%' pitch='+5%'>
                    <emphasis level="strong">
                        {text}
                    </emphasis>
                </prosody>
            </voice>
        </speak>
        """
        result = synthesizer.speak_ssml_async(ssml_string).get()
    else:
        result = synthesizer.speak_text_async(text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized for text \n[{text}]")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: \n{cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: \n{cancellation_details.error_details}")

    return "output.wav"

# Streamlit에서 파일 다운로드
st.title("Azure Speech Service with Streamlit")

if st.button('Generate and Download Speech'):
    text = st.text_input("Enter text to synthesize")
    if text:
        file_path = synthesize_and_play_speech(text)
        with open(file_path, "rb") as file:
            btn = st.download_button(
                label="Download synthesized speech",
                data=file,
                file_name="synthesized_speech.wav",
                mime="audio/wav"
            )
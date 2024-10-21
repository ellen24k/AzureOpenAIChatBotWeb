###마이크 입력
# if 'mic_input' not in st.session_state:
#     st.session_state['mic_input'] = ''
#
# if st.button('마이크로 입력하기'):
#     with spinner('마이크가 작동중 입니다. 지금 말하세요.'):
#         try:
#             recognition_result = recognize_speech()
#         except Exception as e:
#             st.error(f'마이크 입력에 실패했습니다.{e}')
#             recognition_result = None
#
#         if recognition_result:
#             st.session_state['mic_input'] = recognition_result.replace('.', '')
#         else:
#             st.session_state['mic_input'] = ''
#             st.info('마이크 입력 버튼을 다시 누르거나 직접 입력하세요.')
#
# user_input = st.text_input('**삼행시를 만들 세글자를 입력하세요.**', value=st.session_state['mic_input'])

# 모든 작업 끝난 후                 # st.session_state['mic_input'] = ''

# 각 페이지 시작에     # st.session_state['mic_input'] = '' 해주면 좋음.

###마이크입력

# def autoSelectDevice():
#     p = pyaudio.PyAudio()
#     audioDeviceIndex1 = None
#     audioDeviceIndex2 = None
#     devices = p.get_device_count()
#     for i in range(devices):
#         device_info = p.get_device_info_by_index(i)
#         if device_info.get('maxInputChannels') <= 0:
#             if audioDeviceIndex1 == None and 'CABLE Input(VB-Audio Virtual Ca' in device_info.get('name'):
#                 audioDeviceIndex1 = device_info.get('index')
#             elif audioDeviceIndex2 == None and '스피커(Realtek(R) Audio)' in device_info.get('name'):
#                 # PHL 328M6FJR2
#                 # 스피커(Realtek(R) Audio)
#                 audioDeviceIndex2 = device_info.get('index')
#
#     print(f"audioDeviceIndex1: {audioDeviceIndex1}, audioDeviceIndex2: {audioDeviceIndex2}")
#     return audioDeviceIndex1, audioDeviceIndex2


# def live_2d():
#     html_code = """
#     <head>
#         <meta charset="UTF-8">
#         <title>live2d-demo</title>
#         <script src="https://apps.bdimg.com/libs/jquery/2.1.4/jquery.min.js"></script>
#         <!-- Live2DCubismCore -->
#         <script src="https://cdn.jsdelivr.net/gh/litstronger/live2d-moc3@master/js/frame/live2dcubismcore.min.js"></script>
#         <!-- Include Pixi. -->
#         <script src="https://cdnjs.cloudflare.com/ajax/libs/pixi.js/4.6.1/pixi.min.js"></script>
#         <!-- Include Cubism Components. -->
#         <script src="https://cdn.jsdelivr.net/gh/litstronger/live2d-moc3@master/js/live2dcubismframework.js"></script>
#         <script src="https://cdn.jsdelivr.net/gh/litstronger/live2d-moc3@master/js/live2dcubismpixi.js"></script>
#         <!-- User's Script -->
#         <script src="https://cdn.jsdelivr.net/gh/litstronger/live2d-moc3@master/js/l2d.js"></script>
#         <script src="https://cdn.jsdelivr.net/gh/litstronger/live2d-moc3@master/js/main.js"></script>
#         <style>
#         </style>
#     </head>
#     <body>
#         <div id="layered-content" style="position: fixed; top: 300px; left: 200px; z-index: 1000;">
#             <div class="Canvas"  id="L2dCanvas"></div>
#                 <script>
#                     var config = {
#                         width: 400,
#                         height: 400,
#                         left: '0px',
#                         bottom: '0px',
#                         basePath: 'https://cdn.jsdelivr.net/gh/alg-wiki/AzurLaneL2DViewer@gh-pages/assets',
#                         role: 'bisimai_2',
#                         background: 'transparent',
#                         opacity: 1,
#                         mobile: true
#                     }
#                     var v = new Viewer(config);
#             </script>
#         </div>
#     </body>
#     """
#
#     st.components.v1.html(html_code, height=400)


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

# def recognize_speech():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.write("마이크가 작동중 입니다. 지금 말하세요.")
#         audio = recognizer.listen(source)
#     try:
#         text = recognizer.recognize_google(audio, language="ko-KR")
#         st.write(f"인식된 텍스트: {text}")
#         return text
#     except sr.UnknownValueError:
#         st.write("음성을 인식할 수 없습니다.")
#     except sr.RequestError as e:
#         st.write(f"음성 인식 서비스에 접근할 수 없습니다: {e}")
#     return None
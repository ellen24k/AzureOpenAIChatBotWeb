import os
import time
from time import sleep

import streamlit.components.v1 as components
import streamlit as st

from pkg_db.db import insert_data, upload_file
from pkg_utils.chat import make_poem
from pkg_utils.dalle import generate_image
from pkg_utils.tts import synthesize_speech
from pkg_utils.utils import autoplay_audio, get_current_time_no_spaces, download_file, padding_set


class ProgressBar:
    def __init__(self, text):
        self.text = text

    def __enter__(self):
        self.progress = st.progress(0, text=self.text)
        return self.progress

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.empty()

    def change_progress(self, text, from_percent, to_percent):
        self.text = text
        for percent_complete in range(from_percent, to_percent):
            time.sleep(0.05)
            self.progress.progress(percent_complete + 1, text='[' + str(percent_complete + 1) + '%] ' + self.text)
        sleep(0.5)

    def empty(self):
        self.progress.empty()


def load_view():
    # live_2d()
    padding_set()
    img_url = None
    content = None

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

    user_input = st.text_input('**삼행시를 만들 세글자를 입력하세요.**')

    if len(user_input) != 3:
        st.error('세글자를 입력해주세요.')
    else:
        if st.button('삼행시 만들기'):
            file_name = get_current_time_no_spaces()
            pbar = ProgressBar('작업을 시작합니다.')
            with pbar:
                autoplay_audio(
                    'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/msg_wait.wav')
                pbar.change_progress('인공지능이 단어를 가지고 삼행시를 생성 중 입니다. 잠시만 기다려주세요.', 0, 15)
                content = make_poem(user_input)
                sleep(3)

                autoplay_audio(
                    'https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/snd_bg.wav')

                pbar.change_progress('이미지를 생성 중 입니다.', 15, 30)
                img_url = generate_image(content)  #

                if not img_url:
                    img_url = "https://raw.githubusercontent.com/ellen24k/AzureOpenAIChatBotWeb/main/resources/default_img.png"
                    pbar.change_progress('이미지 생성에 실패했습니다. 기본 이미지를 사용합니다.', 30, 50)
                else:
                    pbar.change_progress('이미지 생성이 완료되었습니다.', 30, 50)

                pbar.change_progress('오디오를 생성 중 입니다.', 50, 60)
                synthesize_speech(content, filename='temp/' + file_name + '.wav', ssml=True)
                pbar.change_progress('오디오 생성이 완료되었습니다.', 60, 70)

                pbar.change_progress('데이터를 저장 중 입니다.', 70, 80)
                download_file(img_url, 'temp/' + file_name + '.png')
                png_file_url = upload_file("ChatBotFiles", 'temp/' + file_name + '.png', file_name + '.png')
                wav_file_url = upload_file("ChatBotFiles", 'temp/' + file_name + '.wav', file_name + '.wav')
                insert_data(png_file_url, wav_file_url, user_input, content)

                st.title(user_input)
                st.image(img_url, use_column_width=True, caption=f'{content}')
                pbar.change_progress('결과를 출력 하는 중 입니다.', 80, 95)
                st.audio('temp/' + file_name + '.wav', format='audio/wav', autoplay=True)

                pbar.change_progress('작업을 완료 하는 중 입니다.', 95, 100)
                pbar.empty()
                st.balloons()

                html_code = """
                        <div id="scroll-target" style="margin-top: 1000px;"></div>
                        <script>
                          function scrollToTarget() {
                            document.getElementById('scroll-target').scrollIntoView({ behavior: 'smooth' });
                          }
                          window.onload = scrollToTarget;
                        </script>
                    """

                components.html(html_code, height=0)

                try:
                    os.remove('temp/' + file_name + '.png')
                    os.remove('temp/' + file_name + '.wav')
                except Exception as e:
                    print(e)

                # st.session_state['mic_input'] = ''


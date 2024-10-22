from time import sleep
import streamlit as st

class ProgressBar:
    def __init__(self, text):
        self.text = text

    def __enter__(self):
        self.progress = st.progress(0, text=self.text)
        return self.progress

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.empty()

    def change_progress(self, text, plus_percent):
        self.text = text
        self.progress.progress(
            self.progress.progress + plus_percent,
            text='[' + str(self.progress.progress + plus_percent) + '%] ' + self.text
        )

    def empty(self):
        self.progress.progress(
            100,
            '[100%] 작업이 완료 되었습니다.',
        )
        sleep(0.5)
        self.progress.empty()

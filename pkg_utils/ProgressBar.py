import threading
from time import sleep

import streamlit as st


class ProgressBar:
    def __init__(self, text):
        self.text = text
        self.current_progress = 0
        self.lock = threading.Lock()

    def __enter__(self):
        self.progress = st.progress(self.current_progress, text=self.text)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.progress.empty()

    def change_progress(self, text, plus_percent):
        with self.lock:
            self.text = text
            to_percent = self.current_progress + plus_percent
            while self.current_progress < to_percent:
                self.current_progress += 1
                self.progress.progress(self.current_progress, text='[' + str(self.current_progress) + '%] ' + self.text)
                sleep(0.05)

    def empty(self):
        self.progress.progress(
            100,
            '[100%] 작업이 완료 되었습니다.',
        )
        sleep(0.5)
        self.progress.empty()

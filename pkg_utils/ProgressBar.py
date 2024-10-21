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

    def change_progress(self, text, from_percent, to_percent):
        self.text = text
        for percent_complete in range(from_percent, to_percent):
            sleep(0.05)
            self.progress.progress(percent_complete + 1, text='[' + str(percent_complete + 1) + '%] ' + self.text)
        sleep(0.5)

    def empty(self):
        self.progress.empty()

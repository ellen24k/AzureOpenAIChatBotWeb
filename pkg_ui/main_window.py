import asyncio
import threading
import time
import tkinter as tk
import tkinter.font as tkFont
from threading import Thread
from tkinter import ttk, messagebox

from pkg_azure_ai import tts, chatbot
from pkg_azure_ai.dalle import generate_image
from pkg_azure_ai.stt import recognize_speech
from pkg_db.db import DatabaseManager
from pkg_ui.input_dialog import InputDialog
from pkg_utils.sound_queue_manager import SoundQueueManager
from pkg_utils.utils import make_history, delete_history


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        # self.db.create_table()
        self.title('3행시 갤러리 using TTS, STT, Dall-E3, Chat-GPT4o with VTube')
        self.geometry('1024x454')
        self.hidden_values = {} # listbox에 표시되는 값과 실제 데이터베이스의 id를 매핑하기 위한 딕셔너리
        self.sound_manager = SoundQueueManager()
        self.sound_manager.start()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.stop_event = threading.Event()
        self.create_widgets()

    def create_widgets(self):
        font = tkFont.Font(family='맑은 고딕', size=24)
        font_size_middle = tkFont.Font(family='맑은 고딕', size=20)

        self.label = ttk.Label(self, text='[ 시 작 ] 버튼을 눌러 인공지능 삼행시를 시작하세요.', font=font)
        self.label.pack(pady=10)

        self.result_label = ttk.Label(self, text='', font=font_size_middle)
        self.result_label.pack(pady=10)

        self.frame = ttk.Frame(self)
        self.frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.button_image = tk.PhotoImage(file=f'resources/default_button.png')
        self.button_image = self.button_image.subsample(4)
        self.button = ttk.Button(self.frame, text='[ 시 작 ]', command=self.start_recognition, width=20,
                                 image=self.button_image,
                                 compound='top', style='TButton')
        self.button.pack(side=tk.LEFT, pady=10, padx=10)

        self.chatbot_response = tk.Text(self.frame, state='normal', height=5, width=35, font=font)
        self.chatbot_response.pack(side=tk.LEFT, pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.history_listbox = tk.Listbox(self.frame)
        self.history_listbox.pack(side=tk.LEFT, pady=10, padx=10, fill=tk.BOTH, expand=True)
        self.history_listbox.bind('<Double-1>', self.on_listbox_doubleclick)
        self.history_listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
        self.history_listbox.bind('<Button-3>', self.on_listbox_rightclick)

        self.populate_history_listbox()

    def on_listbox_rightclick(self, event):
        selected_index = self.history_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_id = self.hidden_values[selected_index]
            selected_title = self.db.select_data(selected_id)[1]
            response = messagebox.askyesno(f"{selected_title} 삭제하시겠습니까?", f"{selected_title} 삭제하시겠습니까?")
            if response:
                self.db.delete_data(selected_id)
                delete_history(selected_id)
                self.populate_history_listbox()
                self.chatbot_response.delete(1.0, tk.END)
                self.button_image = tk.PhotoImage(file=f'resources/default_button.png')
                self.button_image = self.button_image.subsample(4)
                self.button.config(image=self.button_image)
                self.set_result_label_text('')
                print("Item deleted")
            else:
                print("Deletion canceled")

    def on_listbox_select(self, event):
        selected_index = self.history_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_id = self.hidden_values[selected_index]
            print(selected_id)
            with open(f'history/{selected_id}.txt', 'r', encoding='utf-8') as file:
                text = file.read()
            self.chatbot_response.delete(1.0, tk.END)
            self.chatbot_response.insert(tk.END, f"{text}\n")
            new_image = tk.PhotoImage(file=f'history/{selected_id}.png')
            self.button_image = new_image.subsample(4)
            self.button.config(image=self.button_image)
            self.set_result_label_text(self.db.select_data(self.hidden_values[selected_index])[1])

    def open_input_dialog(self):
        dialog = InputDialog(self)
        result = dialog.show()
        if result:
            self.process_recognition(result)

    def on_listbox_doubleclick(self, event):
        selected_index = self.history_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_id = self.hidden_values[selected_index]
            self.sound_manager.put(f'history/{selected_id}.wav',True)
            self.wait_for_queue_empty()

    def populate_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        all_data = self.db.select_all_data()
        for row in all_data:
            self.history_listbox.insert(tk.END, row[1])
            self.hidden_values[self.history_listbox.size() - 1] = row[0]

    def set_result_label_text(self, text):
        self.result_label.config(text=text)

    def wait_for_queue_empty(self):
        while not self.sound_manager.sound_queue.empty():
            time.sleep(0.5)

    def start_recognition(self):
        def run():
            self.button.config(state='disabled')
            self.chatbot_response.delete(1.0, tk.END)
            self.set_result_label_text('삐 소리가 난 후 3행시를 만들 3글자를 말해주세요.')
            self.sound_manager.put(f'resources/msg_beep.wav', True)
            self.sound_manager.put(f'resources/snd_beep.wav')
            self.wait_for_queue_empty()

            self.stop_event.clear()
            Thread(target=lambda: self.on_recognized(recognize_speech())).start()
            # def run_recognition():
            #     recognized_text = recognize_speech()
            #     self.on_recognized(recognized_text)
            #
            # Thread(target=run_recognition).start()

            # def recognize_and_callback(callback):
            #     text = recognize_speech()
            #     callback(text)
            #
            # Thread(target=lambda: recognize_and_callback(self.on_recognized)).start()

            for i in range(5, -1, -1):
                if self.stop_event.is_set():
                    break
                self.set_result_label_text(f'인식 중...{i}초 남음.')
                self.after(0, self.update_idletasks)
                time.sleep(1)

        Thread(target=run).start()

    def on_recognized(self, text):
        self.stop_event.set()
        if not text:
            self.set_result_label_text('목소리가 인식되지 않았습니다. 다시 시도하세요.')
            self.sound_manager.put(f'resources/msg_retry.wav', True)
            self.button.config(state='normal')
            self.open_input_dialog()

            return
        self.set_result_label_text('인식 성공.')
        self.process_recognition(text[:3])

    def process_recognition(self, text):
        def run():
            self.chatbot_response.insert(tk.END, f"[사용자]\n{text}\n")
            self.after(0, self.update_idletasks)
            self.synthesize_and_play(text + ": 단어가 인식 되었습니다.", f'temp/gen_recog.wav')

            self.set_result_label_text('인공지능이 단어를 가지고 삼행시를 생성 중 입니다.')
            self.sound_manager.put(f'resources/msg_wait.wav', True)
            self.sound_manager.put(f'resources/snd_bg.wav')

            generated_text = chatbot.chat(text)

            self.synthesize_and_play(text + ": 단어를 가지고 삼행시를 만들었습니다.", f'temp/gen_info.wav')
            self.synthesize_and_play(generated_text, f'temp/gen_text.wav', True)
            self.sound_manager.put(f'resources/snd_bg.wav')

            img_url = asyncio.run(generate_image(generated_text))

            if img_url is not None:
                now = make_history(generated_text, img_url, f'temp/gen_text.wav')
            else:
                print("부적절한 단어 사용등의 이유로 이미지 생성이 취소되었습니다. 기본이미지로 저장합니다.")
                now = make_history(generated_text, 'default_img', f'temp/gen_text.wav')
            self.db.add_data(now, text)
            self.populate_history_listbox()
            new_image = tk.PhotoImage(file=f'history/' + now + '.png')
            self.button_image = new_image.subsample(4)
            self.button.config(image=self.button_image)
            self.chatbot_response.insert(tk.END, f"[챗봇]\n{generated_text}\n\n")
            self.wait_for_queue_empty()
            self.button.config(state='normal')
            self.set_result_label_text('')
            self.after(0, self.update_idletasks)

        Thread(target=run).start()

    def synthesize_and_play(self, text, file_path, ssml=False):
        tts.synthesize_speech(text, file_path, ssml)
        self.sound_manager.put(file_path, True)

    def on_closing(self):
        self.sound_manager.stop()
        self.db.close()
        self.destroy()

import queue
import threading
import time

from pkg_utils.sound_playback import SoundPlayback
from pkg_utils.utils import autoSelectDevice


class SoundQueueManager:

    def __init__(self):
        self.sound_queue = queue.Queue()
        self._stop_event = threading.Event()
        self.current_playback_thread = None
        self.thread = threading.Thread(target=self.run)
        self.deviceIndex = autoSelectDevice()

    def start(self):
        self.thread.start()

    def run(self):
        while not self._stop_event.is_set():
            if not self.sound_queue.empty() and (
                    self.current_playback_thread is None or not self.current_playback_thread.is_alive()):
                file_info = self.sound_queue.get()
                file_path = file_info[0]
                output_speaker_index1 = file_info[1]
                output_speaker_index2 = file_info[2] if len(file_info) > 2 else None
                self.current_playback_thread = SoundPlayback(file_path, output_speaker_index1,
                                                             output_speaker_index2, self)
                self.current_playback_thread.start()
            time.sleep(0.5)

    def stop(self):
        self._stop_event.set()
        self.thread.join()
        print('SoundQueueManager: Stopped')

    def put(self, file_name, two_channel=False):
        if two_channel == True:
            # checkVBCable.py를 실행시켜서 device_index를 확인해야함.
            # file_info = (file_name, 7, 6) # VB Audio Cable에 먼저 쏴줘야 vtube studio 딜레이가 적어짐.
            file_info = (file_name, self.deviceIndex[0], self.deviceIndex[1])
        else:
            # file_info = (file_name, 6)
            file_info = (file_name, self.deviceIndex[1])
        self.sound_queue.put(file_info)
        print('SoundQueueManager: Added file to queue:', file_info)

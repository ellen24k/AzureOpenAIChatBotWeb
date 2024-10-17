import threading
import wave

import pyaudio


class SoundPlayback(threading.Thread):
    def __init__(self, file_path, speaker_index1, speaker_index2, manager):
        super().__init__()
        self.file_path = file_path
        self.speaker_index1 = speaker_index1
        self.speaker_index2 = speaker_index2
        self.manager = manager

    def run(self):
        wf = wave.open(self.file_path, 'rb')
        p = pyaudio.PyAudio()

        stream1 = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                         channels=wf.getnchannels(),
                         rate=wf.getframerate(),
                         output=True,
                         output_device_index=self.speaker_index1)

        if self.speaker_index2 is not None:
            stream2 = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                             channels=wf.getnchannels(),
                             rate=wf.getframerate(),
                             output=True,
                             output_device_index=self.speaker_index2)

        data = wf.readframes(512)
        while data:
            stream1.write(data)
            if self.speaker_index2 is not None:
                stream2.write(data)
            data = wf.readframes(512)

        stream1.stop_stream()
        stream1.close()
        if self.speaker_index2 is not None:
            stream2.stop_stream()
            stream2.close()
        p.terminate()

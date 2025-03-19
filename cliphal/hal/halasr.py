import pyaudio
import time
import threading
from funasr import AutoModel
import webrtcvad
import queue
import numpy as np
import librosa
import wave

class ASRService:
    # setup model
    ASR_MODEL = "paraformer-zh"  # 語音識別模型
    VAD_MODEL = "fsmn-vad"       # 語音活動檢測（可選）
    PUNC_MODEL = "ct-punc"       # 標點符號模型（可選）

    VAD_MODE=3

    # setup audio args
    # CHUNK = 1024  # 每次讀取的音訊大小
    FORMAT = pyaudio.paInt16  # 16-bit PCM
    CHANNELS = 1  # 單聲道
    AUDIO_RATE = 48000  # FunASR 需要 16kHz
    TARGET_RATE = 16000  # FunASR 需要 16kHz
    DEVICE_INDEX = 5  # 手動設定裝置 ID（可用 list_audio_devices() 查詢）
    SILENCE_DURATION = 3  # 若無聲音超過 3 秒則結束錄音
    CHUNK = int(AUDIO_RATE * 20 / 1000)

    def __init__(self):
        # vars
        self.flag_run = False
        self.def_queue_limit = 100
        self.tmp_file = "/tmp/output.wav"
        self.flag_output = True

        self.text_queue = queue.Queue()

        # load modle
        self.model = AutoModel(model=self.ASR_MODEL, vad_model=self.VAD_MODEL, punc_model=self.PUNC_MODEL, disable_update=True, disable_log=True, disable_pbar=True)

        # Init mic
        self.audio = pyaudio.PyAudio()
    def get(self):
        if self.text_queue.empty() is False:
            return self.text_queue.get()
        else:
            return None

    def start(self):
        service_thread = threading.Thread(target=self.listen_continuous, daemon=True)
        service_thread.start()
    def stop(self):
        self.flag_run = False

    def save_wave(self, filename, audio_data, sample_rate):
        audio_np = np.frombuffer(audio_data, dtype=np.int16)
        if sample_rate != self.TARGET_RATE:
            audio_np = librosa.resample(audio_np.astype(np.float32), orig_sr=sample_rate, target_sr=self.TARGET_RATE)
            sample_rate = self.TARGET_RATE

        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_np.astype(np.int16).tobytes())

        # print(f"✅ 音檔已儲存: {filename} (取樣率: {sample_rate} Hz)")

    def command_handler(self, message):
        is_cmd = False
        # return true mean it's a command, and just ignore it.
        if message == "output enable":
            self.flag_output = True
            is_cmd = True
        elif message == "output disable":
            self.flag_output = False
            is_cmd = True
        elif message == "clear data":
            self.text_queue.queue.clear()
            is_cmd = True

        # check if we need to block recording
        if self.flag_output is False:
            is_cmd = True

        return is_cmd
    def recognize_audio(self, filename):
        result = self.model.generate(input=filename)
        return result[0]['text']

    def listen_continuous(self):
        # 初始化 VAD
        vad = webrtcvad.Vad()
        vad.set_mode(self.VAD_MODE)

        print("🎤 Continuous listen...")

        stream = self.audio.open(format=self.FORMAT,
                                 channels=self.CHANNELS,
                                 rate=self.AUDIO_RATE,
                                 input=True,
                                 frames_per_buffer=self.CHUNK,
                                 input_device_index=self.DEVICE_INDEX)
        self.flag_run = True
        while self.flag_run:
            audio_list = []
            is_recording = False
            start_time = time.time()
            silence_start_time = time.time()

            try:
                while self.flag_run:
                    data = stream.read(self.CHUNK, exception_on_overflow=False)
                    is_speech = vad.is_speech(data, self.AUDIO_RATE)

                    if is_speech is True and is_recording is False:
                        # Start recording
                        print("🎙️ Audio defected...")
                        is_recording = True
                        start_time = time.time()
                        silence_start_time = time.time()

                    # record data.
                    if is_recording is True:
                        audio_list.append(data)

                    # 偵測停止（若無聲音超過 SILENCE_DURATION 秒則結束錄音）
                    silence_duration = time.time() - silence_start_time
                    if is_recording and silence_duration > self.SILENCE_DURATION:
                        print("🛑 Recording ended, start recognition...")
                        break
            except KeyboardInterrupt:
                print("\n🛑 Stop listening.")
                break

            # 組合音訊數據
            audio_data = b''.join(audio_list)
            self.save_wave(self.tmp_file, audio_data, self.AUDIO_RATE)
            text_result = self.recognize_audio(self.tmp_file)
            if text_result != "" and self.command_handler(text_result) is False:
                if self.text_queue.qsize() > self.def_queue_limit:
                    print("Hit queue limit, just clear queue.")
                    self.text_queue.queue.clear()
                self.text_queue.put(text_result)

        stream.stop_stream()
        stream.close()
        self.audio.terminate()

if __name__ == "__main__":
    asr = ASRService()
    # asr.listen_continuous()
    asr.start()
    input("Enter to finish.")

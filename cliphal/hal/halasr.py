import traceback
import pyaudio
import time
import threading
from funasr import AutoModel
import webrtcvad
import queue
import numpy as np
import librosa
import wave
from opencc import OpenCC

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
    HOTWORDS = ["Hello."]
    CHUNK = int(AUDIO_RATE * 20 / 1000)
    SILENCE_DURATION = 1  # 若無聲音超過 3 秒則結束錄音
    SPEACH_TIMEOUT = 60  # switch output off if timeout hit.

    def __init__(self, device_index = 0, sample_rate = 48000, hot_words = None):
        # class variable
        self.DEVICE_INDEX = device_index
        self.AUDIO_RATE = sample_rate

        # flags
        self.flag_run = False
        self.flag_output = True
        self.flag_s2t = True
        self.flag_hotword_mode = False

        # vars
        self.def_queue_limit = 100
        self.tmp_file = "/tmp/output.wav"
        self.last_speech_time = time.time()  # 記錄最後一次辨識成功的時間
        self.text_queue = queue.Queue()

        # vars init
        # Init hotword
        if hot_words is not None:
            self.flag_hotword_mode = True
            for each_word in hot_words:
                if each_word not in self.HOTWORDS:
                    self.HOTWORDS.append(each_word)

        # load model
        self.model = AutoModel(model=self.ASR_MODEL, vad_model=self.VAD_MODEL, punc_model=self.PUNC_MODEL, disable_update=True, disable_log=True, disable_pbar=True)

        # Init mic
        self.audio = pyaudio.PyAudio()

        # init cc
        self.cc = OpenCC('s2t')
    def list_audio_devices(self, test_sample_rates=None):
        """
        列出 PyAudio 所有輸入裝置以及其支援的 sample rate 測試結果
        """
        if test_sample_rates is None:
            test_sample_rates = [
                8000,   # 電話品質
                11025,  # 老音訊格式
                16000,  # 常用語音辨識
                22050,  # 低品質音樂
                32000,  # 中品質音樂
                44100,  # CD 品質
                48000,  # 標準錄音
                88200,  # 高品質錄音
                96000,  # 高解析錄音
                176400, # 發燒級
                192000  # 專業錄音
            ]

        # self.audio = pyaudio.PyAudio()
        device_count = self.audio.get_device_count()

        print("🎧 Audio Input Device List:\n")

        for i in range(device_count):
            info = self.audio.get_device_info_by_index(i)

            if info.get("maxInputChannels") > 0:
                print(f"🔹 Device Index: {i}")
                print(f"    Name: {info['name']}")
                print(f"    Max Input Channels: {info['maxInputChannels']}")
                print(f"    Default Sample Rate: {int(info['defaultSampleRate'])}")

                print("    Supported Sample Rates:")
                for rate in test_sample_rates:
                    try:
                        self.audio.is_format_supported(rate,
                                               input_device=info["index"],
                                               input_channels=1,
                                               input_format=pyaudio.paInt16)
                        print(f"      ✅ {rate} Hz")
                    except ValueError:
                        pass
                        # print(f"      ❌ {rate} Hz")

                print("-" * 50)

        # self.audio.terminate()
    def get(self):
        if self.text_queue.empty() is False:
            message = self.text_queue.get()
            if self.flag_s2t:
                message = self.cc.convert(message)
            return message
        else:
            return None

    def wait(self):
        # just extend last_speech_time
        self.last_speech_time = time.time()
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

    def set_pause(self, is_enable):
        self.flag_output = not is_enable

    def command_event_handler(self, message):
        is_cmd = False
        cmd_message = message.strip().rstrip()
        # return true mean it's a command, and just ignore it.
        if cmd_message == "Output enable.":
            self.text_queue.queue.clear()
            self.flag_output = True
            is_cmd = True
            self.last_speech_time = time.time()
        elif cmd_message == "Output disable.":
            self.flag_output = False
            is_cmd = True
        elif cmd_message == "Clear data.":
            self.text_queue.queue.clear()
            is_cmd = True
        elif cmd_message == "Print information.":
            print(f"##  Flags")
            print(f"flag_output       : {self.flag_output}")
            print(f"flag_run          : {self.flag_run}")
            print(f"flag_output       : {self.flag_output}")
            print(f"flag_s2t          : {self.flag_s2t}")
            print(f"flag_hotword_mode : {self.flag_hotword_mode}")
            print(f"##  Vars")
            print(f"last_speech_time  : {self.last_speech_time}")
            print(f"current time      : {time.time()}")
            print(f"HOTWORDS          : {self.HOTWORDS}")
            is_cmd = True
        elif self.flag_output == False and cmd_message in self.HOTWORDS:
            self.text_queue.queue.clear()
            is_cmd = True
            self.flag_output = True
            self.last_speech_time = time.time()

        if is_cmd is True:
            print(f"Voice command:'{message}'")

        # check timeout.
        speach_silence_duration = time.time() - self.last_speech_time
        if self.flag_hotword_mode is True and speach_silence_duration > self. SPEACH_TIMEOUT:
            self.flag_output = False
        else:
            self.last_speech_time = time.time()

        # check if we need to block recording
        if self.flag_output is False:
            if is_cmd is False:
                print(f"Output has been blocked(Say 'hello' to enable it.): '{message}'")
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

        stream = None
        try:
            stream = self.audio.open(format=self.FORMAT,
                                    channels=self.CHANNELS,
                                    rate=self.AUDIO_RATE,
                                    input=True,
                                    frames_per_buffer=self.CHUNK,
                                    input_device_index=self.DEVICE_INDEX)
        except Exception as e:
            print(e)
            traceback_output = traceback.format_exc()
            print(traceback_output)
            self.list_audio_devices()
            raise

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

                    # Refresh silence_start_time
                    if is_speech is True:
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
            if text_result != "" and self.command_event_handler(text_result) is False:
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

"""
语音识别模块
使用 Whisper 实现实时语音转文字
"""

import whisper
import numpy as np
import threading
import time
from collections import deque
import pyaudio

class AudioRecognizer:
    """音频识别器 - 将语音实时转换为文字"""

    def __init__(self, model_size="base", language="en", silence_timeout=10):
        """
        初始化识别器

        Args:
            model_size: 模型大小 (tiny/base/small/medium/large)
            language: 源语言代码 (en/zh/ja等)
            silence_timeout: 静音超时时间（秒），超过此时间自动停止
        """
        print(f"正在加载 Whisper {model_size} 模型...")
        self.model = whisper.load_model(model_size)
        self.language = language
        self.is_listening = False
        self.silence_timeout = silence_timeout  # 静音超时时间
        self.last_audio_time = time.time()      # 最后有声音的时间
        self.silence_threshold = 0.01           # 静音阈值

        self.latest_text=""
        self.sample_rate = 16000  # Whisper 需要 16kHz
        self.chunk_size = 1024    # 每次读取的帧数
        self.channels = 1         # 单声道

        # 音频缓存（3秒）
        self.audio_buffer = deque(maxlen=int(self.sample_rate * 3))

        # PyAudio 对象
        self.p = None
        self.stream = None

        # 回调函数
        self.on_result_callback = None
        self.on_silence_callback = None  # 静音超时回调

        print(f"✅ 识别器初始化完成 (模型: {model_size}, 语言: {language}, 静音超时: {silence_timeout}秒)")

    def start_listening(self, callback):
        """
        开始监听麦克风

        不使用回调，改用轮询获取结果
        """
        self.on_result_callback = callback
        self.is_listening = True
        self.is_listening = True
        self.latest_text = ""
        # 初始化 PyAudio
        self.p = pyaudio.PyAudio()

        # 打开麦克风流
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._audio_callback
        )

        self.stream.start_stream()
        print("🎤 开始监听麦克风...")

        # 启动识别线程
        self.recognition_thread = threading.Thread(target=self._recognition_loop)
        self.recognition_thread.daemon = True
        self.recognition_thread.start()

    def _audio_callback(self, in_data, frame_count, time_info, status):
        """
        PyAudio 回调函数，实时接收麦克风音频

        Args:
            in_data: 音频数据 (bytes)
        """
        if self.is_listening:
            # 将 bytes 转换为 numpy 数组
            # PyAudio paInt16 格式需要转换为 float32 并归一化到 [-1.0, 1.0]
            audio_data = np.frombuffer(in_data, dtype=np.int16)
            audio_data = audio_data.astype(np.float32) / 32767.0  # 使用 32767 而不是 32768
            self.audio_buffer.extend(audio_data)
            
            # 检测是否有声音（通过计算音频能量）
            audio_energy = np.mean(np.abs(audio_data))
            if audio_energy > self.silence_threshold:
                self.last_audio_time = time.time()  # 更新最后有声音的时间
                #print(f"[DEBUG] 检测到声音，能量: {audio_energy}")

        return (None, pyaudio.paContinue)

    def start_listening_without_callback(self, silence_callback=None):
        """开始监听（不使用回调，改用轮询获取结果）
        
        Args:
            silence_callback: 静音超时回调函数
        """
        self.is_listening = True
        self.latest_text = ""
        self.last_audio_time = time.time()  # 重置最后有声音的时间
        self.on_silence_callback = silence_callback

        # 初始化 PyAudio
        self.p = pyaudio.PyAudio()

        # 打开麦克风流
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._audio_callback
        )

        self.stream.start_stream()
        print("🎤 开始监听麦克风...")
        
        # 启动识别线程
        self.recognition_thread = threading.Thread(target=self._recognition_loop_no_callback)
        self.recognition_thread.daemon = True
        self.recognition_thread.start()
        
        # 启动静音检测线程
        self.silence_thread = threading.Thread(target=self._silence_monitor)
        self.silence_thread.daemon = True
        self.silence_thread.start()

    def _recognition_loop_no_callback(self):
        """识别循环 - 存储结果到 latest_text"""
        last_text = ""

        while self.is_listening:
            if len(self.audio_buffer) > self.sample_rate:
                try:
                    audio_data = np.array(self.audio_buffer)
                    
                    result = self.model.transcribe(
                        audio_data,
                        language=self.language,
                        fp16=False
                    )
                    text = result["text"].strip()

                    if text and text != last_text:
                        last_text = text
                        self.latest_text = text  # 存储到变量，不直接回调
                        print(f"🎤 识别: {text}")

                except Exception as e:
                    print(f"识别错误: {e}")

            time.sleep(0.5)

    def _silence_monitor(self):
        """静音检测线程 - 检测长时间静音并自动停止"""
        while self.is_listening:
            time.sleep(1)  # 每秒检查一次
            if self.is_listening:
                elapsed = time.time() - self.last_audio_time
                if elapsed >= self.silence_timeout:
                    print(f"⏰ 检测到静音超过 {self.silence_timeout} 秒，自动停止监听")
                    self.stop_listening()
                    if self.on_silence_callback:
                        self.on_silence_callback()
                    break

    def get_latest_text(self):
        """获取最新的识别结果"""
        text = self.latest_text
        # 可选：获取后不清空，或者保留用于显示
        return text
    
    def check_silence(self):
        """检查是否超过静音超时时间"""
        elapsed = time.time() - self.last_audio_time
        return elapsed >= self.silence_timeout

    def stop_listening(self):
        """停止监听"""
        self.is_listening = False

        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.p:
            self.p.terminate()

        print("⏹️ 停止监听")

    def _recognition_loop(self):
        """识别循环 - 每隔一段时间识别一次音频"""
        last_text = ""
        last_recognition_time = 0

        while self.is_listening:
            # 每1秒识别一次（有足够音频时）
            if len(self.audio_buffer) > self.sample_rate:  # 至少有1秒音频

                try:
                    # 获取音频数据
                    audio_data = np.array(self.audio_buffer)

                    # 转写音频
                    result = self.model.transcribe(
                        audio_data,
                        language=self.language,
                        fp16=False  # CPU模式
                    )

                    text = result["text"].strip()

                    # 只有文本变化时才回调
                    if text and text != last_text:
                        last_text = text
                        if self.on_result_callback:
                            self.on_result_callback(text)
                            print(f"🎤 识别: {text}")

                except Exception as e:
                    print(f"识别错误: {e}")

            # 等待0.5秒再进行下一次识别
            time.sleep(0.5)

    @staticmethod
    def list_models():
        """列出可用的模型"""
        return ["tiny", "base", "small", "medium", "large"]


# 测试代码
if __name__ == "__main__":
    def on_text(text):
        print(f"识别结果: {text}")

    print("测试语音识别模块")
    recognizer = AudioRecognizer(model_size="tiny")

    input("按 Enter 开始录音测试...")
    recognizer.start_listening(on_text)

    input("按 Enter 停止...")
    recognizer.stop_listening()
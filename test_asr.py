"""测试语音识别模块"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.asr import AudioRecognizer
import time

def test_recognition():
    print("=== 测试语音识别 ===")
    
    # 创建识别器
    recognizer = AudioRecognizer(model_size="tiny", language="en")
    
    # 开始监听（不使用回调）
    recognizer.start_listening_without_callback()
    
    print("🎤 开始监听，请说话（5秒后停止）...")
    
    # 等待5秒
    for i in range(5):
        time.sleep(1)
        latest = recognizer.get_latest_text()
        print(f"第{i+1}秒 - 最新识别: '{latest}'")
    
    # 停止监听
    recognizer.stop_listening()
    print("⏹️ 测试结束")

if __name__ == "__main__":
    test_recognition()

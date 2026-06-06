"""
测试语音识别界面更新
"""
import streamlit as st
import sys
import os
import time

sys.path.append(os.path.dirname(__file__))
from src.asr import AudioRecognizer

# 初始化状态
if 'recognizer' not in st.session_state:
    st.session_state.recognizer = None
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False
if 'text' not in st.session_state:
    st.session_state.text = ""

st.title("🎤 测试语音识别")

# 显示识别结果
st.subheader("识别结果")
st.write(f"当前文本: '{st.session_state.text}'")

# 按钮
col1, col2 = st.columns(2)

with col1:
    def on_start():
        st.session_state.recognizer = AudioRecognizer(model_size="tiny", language="en")
        st.session_state.recognizer.start_listening_without_callback()
        st.session_state.is_listening = True
        print("开始监听")
        st.rerun()
    
    st.button("▶️ 开始", type="primary", on_click=on_start, disabled=st.session_state.is_listening)

with col2:
    def on_stop():
        if st.session_state.recognizer:
            st.session_state.recognizer.stop_listening()
            st.session_state.recognizer = None
        st.session_state.is_listening = False
        print("停止监听")
        st.rerun()
    
    st.button("⏹️ 停止", on_click=on_stop, disabled=not st.session_state.is_listening)

# 更新循环
if st.session_state.is_listening and st.session_state.recognizer:
    latest = st.session_state.recognizer.get_latest_text()
    print(f"获取最新文本: '{latest}'")
    
    if latest and latest != st.session_state.text:
        st.session_state.text = latest
        print(f"更新文本: '{latest}'")
    
    time.sleep(0.5)
    st.rerun()

st.info("测试：点击开始后说英语，看看界面是否更新")

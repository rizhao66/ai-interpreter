"""
AI同声传译助手 - 主程序
实时语音识别 + 翻译 + 自动纠错
"""

import streamlit as st
import sys
import os
import time

sys.path.append(os.path.dirname(__file__))
from src.asr import AudioRecognizer
from src.translator import LocalTranslator

# 页面配置
st.set_page_config(page_title="AI同声传译助手", page_icon="🎙️", layout="wide")

# 初始化session state
if 'recognizer' not in st.session_state:
    st.session_state.recognizer = None
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False
if 'original_text' not in st.session_state:
    st.session_state.original_text = ""
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""
if 'translator' not in st.session_state:
    st.session_state.translator = None

# 标题
st.title("🎙️ AI同声传译助手")

# 侧边栏设置
with st.sidebar:
    st.subheader("⚙️ 设置")
    model_size = st.selectbox("识别模型", ["tiny", "base", "small"], index=1)
    source_lang = st.selectbox("源语言", ["英语 (en)", "日语 (ja)", "中文 (zh)"], index=0)
    silence_timeout = st.slider("静音超时时间(秒)", min_value=5, max_value=30, value=10, step=1)
    
    st.divider()
    st.subheader("📊 状态")
    if st.session_state.is_listening:
        st.success("🟢 同传运行中")
    else:
        st.info("⚪ 待机状态")

# 主区域
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 原文识别")
    st.write(f"当前识别: '{st.session_state.original_text}'")

with col2:
    st.subheader("🇨🇳 中文翻译")
    st.write(f"翻译结果: '{st.session_state.translated_text}'")

# 控制按钮回调
def on_silence_timeout():
    """静音超时回调"""
    print("[APP] 静音超时，自动停止同传")
    on_stop()

def on_start():
    """开始同传"""
    lang_code = source_lang.split("(")[-1].replace(")", "").strip()
    
    # 创建识别器
    st.session_state.recognizer = AudioRecognizer(
        model_size=model_size, 
        language=lang_code,
        silence_timeout=silence_timeout
    )
    
    # 创建翻译器（使用本地词典）
    st.session_state.translator = LocalTranslator(
        source_lang=lang_code,
        target_lang='zh'
    )
    
    st.session_state.recognizer.start_listening_without_callback(
        silence_callback=on_silence_timeout
    )
    st.session_state.is_listening = True
    print(f"[APP] 开始监听")
    st.rerun()

def on_stop():
    """停止同传"""
    if st.session_state.recognizer:
        st.session_state.recognizer.stop_listening()
        st.session_state.recognizer = None
    st.session_state.is_listening = False
    print("[APP] 停止监听")
    st.rerun()

def on_clear():
    """清空文本"""
    st.session_state.original_text = ""
    st.session_state.translated_text = ""
    if st.session_state.translator:
        st.session_state.translator.clear_cache()
    st.rerun()

col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    st.button("▶️ 开始同传", type="primary", use_container_width=True, 
              on_click=on_start, disabled=st.session_state.is_listening)

with col_btn2:
    st.button("⏹️ 停止", use_container_width=True, 
              on_click=on_stop, disabled=not st.session_state.is_listening)

with col_btn3:
    st.button("🗑️ 清空", use_container_width=True, on_click=on_clear)

# 实时更新
if st.session_state.is_listening and st.session_state.recognizer:
    latest_text = st.session_state.recognizer.get_latest_text()
    print(f"[APP] 获取最新文本: '{latest_text}'")
    
    if latest_text and latest_text != st.session_state.original_text:
        st.session_state.original_text = latest_text
        if st.session_state.translator:
            translated = st.session_state.translator.translate(latest_text, use_context=True)
            st.session_state.translated_text = translated
            print(f"[APP] 翻译: '{latest_text}' → '{translated}'")
        else:
            st.session_state.translated_text = f"[待翻译] {latest_text}"
    
    time.sleep(0.5)
    st.rerun()

st.info(f"💡 提示：点击「开始同传」后，请允许浏览器访问麦克风权限。静音超过{silence_timeout}秒将自动停止同传。")

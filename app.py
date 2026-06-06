"""
AI同声传译助手 - 主程序
实时语音识别 + 翻译 + 自动纠错
"""

import streamlit as st
import sys
import os

# 添加src目录到路径
sys.path.append(os.path.dirname(__file__))

from src.asr import AudioRecognizer

# 页面配置
st.set_page_config(
    page_title="AI同声传译助手",
    page_icon="🎙️",
    layout="wide"
)

# 初始化session state
if 'is_listening' not in st.session_state:
    st.session_state.is_listening = False
if 'recognizer' not in st.session_state:
    st.session_state.recognizer = None
if 'original_text' not in st.session_state:
    st.session_state.original_text = ""
if 'translated_text' not in st.session_state:
    st.session_state.translated_text = ""

# 标题
st.title("🎙️ AI同声传译助手")
st.caption("实时语音识别 | 智能翻译 | 自动纠错")

# 侧边栏配置
with st.sidebar:
    st.subheader("⚙️ 设置")

    model_size = st.selectbox(
        "识别模型",
        ["tiny", "base", "small"],
        index=1,
        help="tiny: 最快但准确率较低 | base: 平衡 | small: 较慢但准确率高"
    )

    source_lang = st.selectbox(
        "源语言",
        ["英语 (en)", "日语 (ja)", "中文 (zh)"],
        index=0
    )

    target_lang = st.selectbox(
        "目标语言",
        ["中文 (zh)", "英语 (en)"],
        index=0
    )

    auto_correct = st.checkbox("🔧 启用自动纠错", value=True)

    st.divider()

    # 状态显示
    st.subheader("📊 状态")
    status_placeholder = st.empty()

    if st.session_state.is_listening:
        status_placeholder.success("🟢 同传运行中")
    else:
        status_placeholder.info("⚪ 待机状态")

# 主区域 - 两列布局
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 原文识别")
    original_display = st.empty()
    original_display.text_area("", st.session_state.original_text, height=200, key="original")

with col2:
    st.subheader("🇨🇳 中文翻译")
    translation_display = st.empty()
    translation_display.text_area("", st.session_state.translated_text, height=200, key="translated")

# 控制按钮
col_btn1, col_btn2, col_btn3 = st.columns(3)

def on_recognize(text):
    """识别回调函数"""
    st.session_state.original_text = text
    # TODO: 后续添加翻译功能
    st.session_state.translated_text = f"[翻译] {text}"

def start_listening():
    """开始同传"""
    if st.session_state.recognizer is None:
        # 解析语言代码
        lang_code = source_lang.split("(")[-1].replace(")", "").strip()

        # 创建识别器
        st.session_state.recognizer = AudioRecognizer(
            model_size=model_size,
            language=lang_code
        )

        # 开始监听
        st.session_state.recognizer.start_listening(on_recognize)
        st.session_state.is_listening = True
        st.rerun()

def stop_listening():
    """停止同传"""
    if st.session_state.recognizer:
        st.session_state.recognizer.stop_listening()
        st.session_state.recognizer = None
    st.session_state.is_listening = False
    st.rerun()

def clear_text():
    """清空文本"""
    st.session_state.original_text = ""
    st.session_state.translated_text = ""

with col_btn1:
    start_btn = st.button("▶️ 开始同传", type="primary", use_container_width=True, on_click=start_listening, disabled=st.session_state.is_listening)

with col_btn2:
    stop_btn = st.button("⏹️ 停止", use_container_width=True, on_click=stop_listening, disabled=not st.session_state.is_listening)

with col_btn3:
    clear_btn = st.button("🗑️ 清空", use_container_width=True, on_click=clear_text)

# 提示信息
st.info("💡 提示：点击「开始同传」后，程序会开始识别麦克风音频（演示模式：目前使用模拟音频）")

# 显示当前配置
with st.expander("⚙️ 当前配置"):
    st.write(f"- 识别模型: {model_size}")
    st.write(f"- 源语言: {source_lang}")
    st.write(f"- 目标语言: {target_lang}")
    st.write(f"- 自动纠错: {'启用' if auto_correct else '禁用'}")
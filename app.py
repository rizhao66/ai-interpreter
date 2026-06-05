"""
AI同声传译助手 - 主程序
实时语音识别 + 翻译 + 自动纠错
"""

import streamlit as st

# 页面配置
st.set_page_config(
    page_title="AI同声传译助手",
    page_icon="🎙️",
    layout="wide"
)

# 标题
st.title("🎙️ AI同声传译助手")
st.caption("实时语音识别 | 智能翻译 | 自动纠错")

# 侧边栏配置
with st.sidebar:
    st.subheader("⚙️ 设置")

    source_lang = st.selectbox(
        "源语言",
        ["英语 (en)", "日语 (ja)", "韩语 (ko)", "法语 (fr)"],
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
    status_placeholder.info("⚪ 等待启动")

    # 性能指标
    col1, col2 = st.columns(2)
    with col1:
        st.metric("延迟", "0ms")
    with col2:
        st.metric("纠错次数", "0")

# 主区域 - 两列布局
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 原文识别")
    original_display = st.empty()
    original_display.info("等待语音输入...")

with col2:
    st.subheader("🇨🇳 中文翻译")
    translation_display = st.empty()
    translation_display.info("等待翻译...")

# 控制按钮
col_btn1, col_btn2, col_btn3 = st.columns(3)
with col_btn1:
    start_btn = st.button("▶️ 开始同传", type="primary", use_container_width=True)
with col_btn2:
    stop_btn = st.button("⏹️ 停止", use_container_width=True)
with col_btn3:
    clear_btn = st.button("🗑️ 清空", use_container_width=True)

# 纠错日志
with st.expander("📋 纠错日志"):
    log_display = st.empty()
    log_display.info("暂无纠错记录")

# 提示信息
st.info("💡 提示：点击「开始同传」后，请允许浏览器访问麦克风权限")
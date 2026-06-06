"""
简单测试应用 - 验证 Streamlit 界面更新
"""
import streamlit as st
import time

# 初始化状态
if 'count' not in st.session_state:
    st.session_state.count = 0
if 'is_running' not in st.session_state:
    st.session_state.is_running = False

st.title("🔄 测试界面更新")

# 显示当前计数
st.subheader(f"当前计数: {st.session_state.count}")

# 按钮
col1, col2 = st.columns(2)

with col1:
    def on_start():
        st.session_state.is_running = True
        print("开始运行")
        st.rerun()
    
    st.button("▶️ 开始", type="primary", on_click=on_start, disabled=st.session_state.is_running)

with col2:
    def on_stop():
        st.session_state.is_running = False
        print("停止运行")
        st.rerun()
    
    st.button("⏹️ 停止", on_click=on_stop, disabled=not st.session_state.is_running)

# 更新循环
if st.session_state.is_running:
    st.session_state.count += 1
    print(f"更新计数: {st.session_state.count}")
    time.sleep(1)
    st.rerun()

st.info("测试：点击开始后计数应该每秒增加")

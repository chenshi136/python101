"""
主程序入口
Streamlit Web 应用
"""

import streamlit as st
from .chat import initialize_chat, render_chat_interface, render_sidebar, handle_user_input
from .memory import MEMORY_FOLDER

# 配置常量
DEFAULT_ROLE = "王晨阳"

def main():
    """主函数"""
    # 页面配置
    st.set_page_config(
        page_title="AI角色扮演聊天",
        page_icon=None,
        layout="wide"
    )
    
    # 渲染侧边栏并获取选择的角色
    selected_role = render_sidebar()
    
    # 初始化聊天
    initialize_chat(selected_role, MEMORY_FOLDER)
    
    # 渲染聊天界面
    render_chat_interface(st.session_state.selected_role)
    
    # 处理用户输入
    handle_user_input()

if __name__ == "__main__":
    main()

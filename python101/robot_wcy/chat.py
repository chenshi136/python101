"""
聊天界面逻辑模块
包含 Streamlit UI 的核心逻辑
"""

import streamlit as st
from .api import call_zhipu_api
from .roles import get_role_system
from .logoc import get_portrait
from .memory import MEMORY_FOLDER

# 结束对话规则
BREAK_MESSAGE = """【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演角色。"""

def initialize_chat(role_name, memory_folder=None):
    """
    初始化聊天对话
    
    参数:
        role_name: 角色名称
        memory_folder: 记忆文件夹路径（如果为None，使用默认路径）
    """
    if memory_folder is None:
        memory_folder = MEMORY_FOLDER
    
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "selected_role" not in st.session_state:
        st.session_state.selected_role = role_name
    if "initialized" not in st.session_state:
        st.session_state.initialized = False
    
    # 初始化对话历史（首次加载或角色切换时）
    if not st.session_state.initialized:
        role_system = get_role_system(role_name, memory_folder)
        system_message = role_system + "\n\n" + BREAK_MESSAGE
        st.session_state.conversation_history = [{"role": "system", "content": system_message}]
        st.session_state.initialized = True

def render_chat_interface(role_name):
    """渲染聊天界面"""
    # 页面标题
    st.title("wcy角色扮演聊天")
    st.markdown("---")
    
    # 显示对话历史
    st.subheader(f"💬 与 {role_name} 的对话")
    
    # 显示角色头像（在聊天窗口上方）
    st.code(get_portrait(), language=None)
    st.markdown("---")  # 分隔线
    
    # 显示历史消息（跳过 system 消息）
    for msg in st.session_state.conversation_history[1:]:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        elif msg["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write(msg["content"])

def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.header("设置")
        
        # 角色选择
        selected_role = st.selectbox(
            "选择角色",
            ["王晨阳"],
            index=0
        )
        
        # 如果角色改变，重新初始化对话
        if selected_role != st.session_state.selected_role:
            st.session_state.selected_role = selected_role
            st.session_state.initialized = False
            st.session_state.conversation_history = []
            st.rerun()
        
        # 清空对话按钮
        if st.button("清空对话"):
            st.session_state.conversation_history = []
            st.session_state.initialized = False
            st.rerun()
        
        st.markdown("---")
        st.markdown("###  说明")
        st.info(
            "- 选择角色后开始对话\n"
            "- 对话记录不会保存\n"
            "- AI的记忆基于初始记忆文件"
        )
    
    return selected_role

def handle_user_input():
    """处理用户输入"""
    user_input = st.chat_input("输入你的消息...")
    
    if user_input:
        # 检查是否结束对话
        if user_input.strip() == "再见":
            st.info("对话已结束")
            st.stop()
        
        # 添加用户消息到历史
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        
        # 显示用户消息
        with st.chat_message("user"):
            st.write(user_input)
        
        # 调用API获取AI回复
        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                try:
                    result = call_zhipu_api(st.session_state.conversation_history)
                    assistant_reply = result['choices'][0]['message']['content']
                    
                    # 添加AI回复到历史
                    st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
                    
                    # 显示AI回复
                    st.write(assistant_reply)
                    
                    # 检查是否结束
                    reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
                    if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
                        st.info("对话已结束")
                        st.stop()
                        
                except Exception as e:
                    st.error(f"发生错误: {e}")
                    st.session_state.conversation_history.pop()  # 移除失败的用户消息

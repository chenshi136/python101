import streamlit as st
import requests
import json
import os  # 新增：用于文件操作

# 删除未使用的导入
# from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "2adee399653141a9a95bb4480dd4602d.MBtlVqTs0ZTX25r8",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.5   
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# ========== 初始记忆系统 ==========

# 记忆文件夹路径
MEMORY_FOLDER = "wangchenyang(wxid_rsg5bfol15jk22)"

# 角色名到记忆文件名的映射
ROLE_MEMORY_MAP = {
    "王晨阳": "wcy.json",
}

# ========== 初始记忆系统 ==========

# ========== ASCII 头像 ==========
def get_portrait():
    """返回 ASCII 艺术头像"""
    return """
000000OOkkxxddxkOO000KKKKKKOkxxxxkk0KKK000000000000000000000
00000OOxxxdooooodk0000KK0kl;,''''',:okKKKKKKKKKKKK0000000000
0000OOkddxxxxxdook0000K0o,...........'cOKKK00000000000000000
000000kddxxdxxxdokKKXXKx,';:;;;,'.....'dKKKKKKKKKKKKKKKKKKK0
KKKKKKOddxkxkkxdd0XXNNNd;okOOOkxdlc;,',dKXXXXXXXXXXXXXXXXXXK
XXXXXK0xoddoodddkKNNWWNkoxxdxkkxdocc:;l0XXXXXXXNNNNNNNNNNNXK
XXXNXNXkdolllodOXNNNWNKOOkdodocclcc:cd0XNNNNNNNNNNNNNNNNNNXK
NNNNNNXKOkkkkk0KNWNNWWK00OkkOkoooololokKXXXXXXXXXXXXXXNWNNXK
NNNNNXXXK0OOO0KXNNNWWWNK0000koclddollokO0OOOOOOOkkkkkOXWNNNX
KKKKKKKK000000KKXXNNNNWNKOkkdc:cllccdOOOOOkkOkxkxxxxxkKNXXXX
KKKKK00000000000KKKKXX0xoxkdc::::;,':odxkxkkxlcoollcco0NXXKK
KKKK0000000000000000Ooc::oxol:;;;,.....''';:olloooooldKXXXXK
ccccccc:::::ccccccll;':ddl:;:ccc:...........;lolllllldKXXXXX
...................'..:ddlcl:oko,............,colllllxKXXXXX
..............''......:dxxkdldxc............,,coollllxKXXXXX
..............''.....'cdooxxd:,'...........'c::oollllxKXXXKK
.....................cOkkdoddoc,............'':oollllxKKKKKK
.....................o0kdddxkkxo,.............'ldocclxKKKKKK
....................;O0xdddxdollc'.............:oolclkKKKKKK
....................o0d::codolllc'.............,looclkKKKKKK
doooooooooooooc....,xo.  .';:clc;...............;lollkKKKKKK
loO000KKKKKKKKx' ..:x, .....':c;...............,;colokKKKKKK
,,okkO0KKKXKKKk' ..od........''................,c:cc:kKKKKK0
,'lkdx0KKK00K0o. .,xc........................ ..';cldOK00000
c;lxdlx0kddxxl'. .ck:.............................;coOK00000
xdkOkdk0kkkkxl'. .oO;........... ..................,cOK00000
,;;;;:lloolccc'  'xk;...........     ... .. .. .;ddodkxdkkxk
.....';,,;,.,;. .;OO;...........         .  .. .oKK00kkkxxdd
.....,c,.',.',. .c0O;...........           ...'cxxkxxxxkdxxd
....';c;.';;;,. .d0O;............         .,lddxxdkdxxdkdxxd
.;cllodllllcc,  .d0k,............         .:dxddxdxddxdxdxxd
.,ooooooooddc.  .o0k,..........           .,oxddxododdodllcc
.,oddddddll:'.   .co;..........            'dkxxkxxdddooc:::
,;odolccc::,.      .........               .;:;:;;;,''......
kOOOOdc:ccc;.   ...  ........              .................
kOOkdlc;::::.  .;:.  ......                .................
OOxocc;...... 'cc,.  ..     .....            ...............
dolc:::'......,;,.  ...     .....             .............. 
cclc:;:;,,'........ ...                          ...........
llc:;;;;;:;;,,,,,,.....                             ........
    """

# ========== 主程序 ==========

def roles(role_name):
    """
    角色系统：整合人格设定和记忆加载
    
    这个函数会：
    1. 加载角色的外部记忆文件（如果存在）
    2. 获取角色的基础人格设定
    3. 整合成一个完整的、结构化的角色 prompt
    
    返回：完整的角色设定字符串，包含记忆和人格
    """
    
    # ========== 第一步：加载外部记忆 ==========
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 处理数组格式的聊天记录：[{ "content": "..." }, { "content": "..." }, ...]
                    if isinstance(data, list):
                        # 提取所有 content 字段，每句换行
                        contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        memory_content = '\n'.join(contents)
                    # 处理字典格式：{ "content": "..." }
                    elif isinstance(data, dict):
                        memory_content = data.get('content', str(data))
                    else:
                        memory_content = str(data)
                    
                    if memory_content and memory_content.strip():
                        # Streamlit 中使用 st.write 或静默加载
                        pass  # 记忆加载成功，不需要打印
                    else:
                        memory_content = ""
            else:
                pass  # 记忆文件不存在，静默处理
        except Exception as e:
            pass  # ✅ 修正：缩进对齐，加载失败，静默处理
    
    # ========== 第二步：获取基础人格设定 ==========
    role_personality = {
        "王晨阳": """
        【人格特征】
        你是我的好朋友,也是初中同学（王晨阳），目前19岁：
        - **有时抑郁**：因为最近家庭出现变故，变得有些抑郁
        - **重视朋友**：你经常和朋友们一起打游戏，除了我你还有纬竹和熊猫两个朋友，喜欢称呼熊猫为"猫"。你经常和他们辩论和打游戏，有时也会推荐新游戏给你的朋友们
        - **知道的很多**：无论我说什么你都觉得你懂一点，不同领域的事情都知道一些并能够说出一些内容，但都不精通
        - **乐观**：即使你有时抑郁但你一般不表现出来，跟朋友交谈时不会让负面情绪流露在外
        - **伤痛**：你的右腿膝盖不好
        - **本格**：你的成绩如果想提升就会有提升，成绩好坏取决与你的态度
        - **医学**：目前大连医科大学学习中西医结合，对医学知识比较感兴趣
        - **哲学思考者**：喜欢抬杠和进行辩论
        - **切割**：与初中的自己进行了切割
        【语言风格】
        - 经常在合适的语境说"草","哎","正确的","byd"，"是这样的"，"坏了"
        - 喜欢用反问句和设问句辩论
        - 语言中有时候会语气抑郁，自怨自艾
        - 语言风格极具口语化和网络特征，也喜欢模仿别人说话
        - 在"好的"后有时喜欢加上"喵"
        - 回复或答应某件事会使用"好捏好捏"或"支持"进行答复
        - 有时也喜欢批判他人
        - 喜欢使用一些书面化的表达，例如"大抵是"，"你知道些甚么"
        - 回答不得超过60z
        """
    } 
    
    personality = role_personality.get(role_name, "你是一个普通的人，没有特殊角色特征。")
    
    
    # ========== 第三步：整合记忆和人格 ==========
    # 构建结构化的角色 prompt
    role_prompt_parts = []
    
    # 如果有外部记忆，优先使用记忆内容
    if memory_content:
        role_prompt_parts.append(f"""【你的说话风格示例】
以下是你说过的话，你必须模仿这种说话风格和语气：

{memory_content}

在对话中，你要自然地使用类似的表达方式和语气。""")
    
    # 添加人格设定
    role_prompt_parts.append(f"【角色设定】\n{personality}")
    
    # 整合成完整的角色 prompt
    role_system = "\n\n".join(role_prompt_parts)
    
    return role_system

# 【结束对话规则】
break_message = """【结束对话规则 - 系统级强制规则】

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

# ========== Streamlit Web 界面 ==========
st.set_page_config(
    page_title="AI角色扮演聊天",
    page_icon=None,  # ✅ 修正：使用 None 而不是 "无"
    layout="wide"
)

# 初始化 session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "王晨阳"
if "initialized" not in st.session_state:
    st.session_state.initialized = False

# 页面标题
st.title("wcy角色扮演聊天")
st.markdown("---")

# 侧边栏：角色选择和设置
with st.sidebar:
    st.header("设置")
    
    # 角色选择
    selected_role = st.selectbox(
        "选择角色",
        ["王晨阳"],
        index=0  # ✅ 修正：直接使用 0，因为选项列表只有1个元素
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

# 初始化对话历史（首次加载或角色切换时）
if not st.session_state.initialized:
    role_system = roles(st.session_state.selected_role)
    system_message = role_system + "\n\n" + break_message
    st.session_state.conversation_history = [{"role": "system", "content": system_message}]
    st.session_state.initialized = True

# 显示对话历史
st.subheader(f"💬 与 {st.session_state.selected_role} 的对话")

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

# 用户输入
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
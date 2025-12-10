import requests
import json
import os 

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "2adee399653141a9a95bb4480dd4602d.MBtlVqTs0ZTX25r8",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.6   
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
                        print(f"✓ 已加载角色 '{role_name}' 的记忆: {memory_file} ({len(data) if isinstance(data, list) else 1} 条记录)")
                    else:
                        memory_content = ""
            else:
                print(f"⚠ 记忆文件不存在: {memory_path}")
        except Exception as e:
            print(f"⚠ 加载记忆失败: {e}")
    
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

# 【角色选择】
role_system = roles("王晨阳")

# 【结束对话规则】
# 告诉AI如何识别用户想要结束对话的意图
# Few-Shot Examples：提供具体示例，让模型学习正确的行为
break_message = """【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"
用户："晚安" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演角色。"""

# 【系统消息】
# 将角色设定和结束规则整合到 system role 的 content 中
# role_system 已经包含了记忆和人格设定，直接使用即可
system_message = role_system + "\n\n" + break_message

# ========== 对话循环 ==========
# 
# 【重要说明】
# 1. 每次对话都是独立的，不保存任何对话历史
# 2. 只在当前程序运行期间，在内存中维护对话历史
# 3. 程序关闭后，所有对话记录都会丢失
# 4. AI的记忆完全基于初始记忆文件（life_memory.json）

try:
    # 初始化对话历史（只在内存中，不保存到文件）
    # 第一个消息是系统提示，包含初始记忆和角色设定
    conversation_history = [{"role": "system", "content": system_message}]
    
    print("✓ 已加载初始记忆，开始对话（对话记录不会保存）")
    
    while True:
        # 【步骤1：获取用户输入】
        user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")
        
        # 【步骤2：检查是否结束对话】
        if user_input in ['再见']:
            print("对话结束")
            break
        
        # 【步骤3：将用户输入添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "user", "content": user_input})
        
        # 【步骤4：调用API获取AI回复】
        # 传入完整的对话历史，让AI在当前对话中保持上下文
        # 注意：这些历史只在本次程序运行中有效，不会保存
        result = call_zhipu_api(conversation_history)
        assistant_reply = result['choices'][0]['message']['content']
        
        # 【步骤5：将AI回复添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        # 【步骤6：显示AI回复】
        # 生成Ascii头像：https://www.ascii-art-generator.org/
        portrait = """
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
        print(portrait + "\n" + assistant_reply)
        
        # 【步骤7：检查AI回复是否表示结束】
        reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
        if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
            print("\n对话结束")
            break

except KeyboardInterrupt:
    # 用户按 Ctrl+C 中断程序
    print("\n\n程序被用户中断")
except Exception as e:
    # 其他异常（API调用失败、网络错误等）
    print(f"\n\n发生错误: {e}")
    

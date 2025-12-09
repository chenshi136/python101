"""
角色系统模块
负责角色人格设定和记忆整合
"""

from .memory import load_memory, MEMORY_FOLDER

def get_role_personality(role_name):
    """获取角色的人格设定"""
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
- 回答不得超过60字
"""
    }
    
    return role_personality.get(role_name, "你是一个普通的人，没有特殊角色特征。")

def get_role_system(role_name, memory_folder=None):
    """
    获取完整的角色系统设定
    
    参数:
        role_name: 角色名称
        memory_folder: 记忆文件夹路径（如果为None，使用默认路径）
        
    返回:
        完整的角色设定字符串，包含记忆和人格
    """
    if memory_folder is None:
        memory_folder = MEMORY_FOLDER
    
    # 加载外部记忆
    memory_content = load_memory(role_name, memory_folder)
    
    # 获取基础人格设定
    personality = get_role_personality(role_name)
    
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

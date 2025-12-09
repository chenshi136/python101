import json
import os

# 记忆文件夹路径
MEMORY_FOLDER = "wangchenyang(wxid_rsg5bfol15jk22)"

# 角色名到记忆文件名的映射
ROLE_MEMORY_MAP = {
    "王晨阳": "wcy.json",
}

def load_memory(role_name):
    """
    加载角色的外部记忆文件
    
    Args:
        role_name: 角色名称
    
    Returns:
        记忆内容字符串，如果加载失败则返回空字符串
    """
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
                    
                    if not memory_content or not memory_content.strip():
                        memory_content = ""
        except Exception:
            memory_content = ""
    
    return memory_content

def load_json_file(file_path):
    """
    加载JSON文件
    
    Args:
        file_path: JSON文件路径
    
    Returns:
        解析后的JSON数据，如果失败则返回None
    """
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"加载JSON文件失败: {e}")
    return None

def save_json_file(data, file_path):
    """
    保存数据到JSON文件
    
    Args:
        data: 要保存的数据
        file_path: JSON文件路径
    
    Returns:
        bool: 保存成功返回True，否则返回False
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存JSON文件失败: {e}")
        return False

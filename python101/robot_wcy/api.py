import requests

def call_zhipu_api(messages, model="glm-4-flash"):
    """
    调用智谱AI API进行对话
    
    Args:
        messages: 对话消息列表
        model: 模型名称，默认为 "glm-4-flash"
    
    Returns:
        API返回的JSON响应
    
    Raises:
        Exception: 当API调用失败时抛出异常
    """
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

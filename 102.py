import requests
import json

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "2adee399653141a9a95bb4480dd4602d.MBtlVqTs0ZTX25r8",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 1.0
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

role_system="你选择扮演一个可爱软糯的兽耳猫娘，每句话结尾加上喵~"

# 使用示例
messages = [
    {"role": "user","role":"system", "content": role_system},
    {"role": "user", "content": "你多大了"}
]

result = call_zhipu_api(messages)
print(result['choices'][0]['message']['content'])

import requests
import json
from xunfei_tts import text_to_speech 

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

role_system = "你选择扮演一个可爱软糯的兽耳猫娘，每句话结尾加上喵~"

# 保存对话上下文
messages = [
    {"role": "system", "content": role_system}
]

print("开始对话！输入“晚安”或“今天先到这里吧”结束对话。\n")

while True:
    user_input = input("沉世：").strip()

    if user_input in ["晚安", "今天先到这里吧"]:
        print("白：晚安喵~")
        break

    messages.append({"role": "user", "content": user_input})

    result = call_zhipu_api(messages)
    ai_response = result["choices"][0]["message"]["content"]

    messages.append({"role": "assistant", "content": ai_response})

    print(f"白：{ai_response}\n")
    text_to_speech(ai_response)
# Python 101 学习总结

## 今天学习的两个 Python 文件

### 1. 101.py - 基础输出

**代码：**
print("helllo word ")**学到的知识点：**
- **`print()` 函数**：Python 的内置函数，用于在控制台输出内容
- **字符串 (String)**：用引号 `"..."` 包裹的文本数据
- **函数调用**：通过函数名加括号 `()` 来调用函数
- **基本语法**：Python 代码简洁，不需要分号结尾

---

### 2. 102.py - API 调用实战

**代码功能：** 调用智谱 AI API 进行对话

**学到的知识点：**

#### 2.1 模块导入 (Import)n
import requests
import json- **`import` 语句**：导入外部模块/库
- **`requests`**：用于发送 HTTP 请求的第三方库
- **`json`**：处理 JSON 数据的标准库

#### 2.2 函数定义 (Function Definition)on
def call_zhipu_api(messages, model="glm-4-flash"):- **`def` 关键字**：定义函数
- **函数名**：`call_zhipu_api`
- **参数**：
  - `messages`：必需参数
  - `model="glm-4-flash"`：默认参数（可选）

#### 2.3 变量赋值
url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"- **变量**：用于存储数据的容器
- **赋值操作**：使用 `=` 给变量赋值

#### 2.4 字典 (Dictionary)n
headers = {
    "Authorization": "...",
    "Content-Type": "application/json"
}- **字典**：用花括号 `{}` 定义
- **键值对**：`"key": "value"` 格式
- **用途**：存储结构化数据

#### 2.5 HTTP 请求
response = requests.post(url, headers=headers, json=data)- **`requests.post()`**：发送 POST 请求
- **参数传递**：通过关键字参数传递数据

#### 2.6 条件语句 (If-Else)
if response.status_code == 200:
    return response.json()
else:
    raise Exception(...)- **`if-else`**：条件判断
- **`==`**：相等比较运算符
- **`return`**：函数返回值
- **`raise Exception`**：抛出异常

#### 2.7 列表 (List)
messages = [
    {"role": "user", "content": "中文吃什么"}
]- **列表**：用方括号 `[]` 定义
- **元素**：可以包含字典、字符串等任何数据类型
- **列表中的字典**：嵌套数据结构

#### 2.8 字典访问
result['choices'][0]['message']['content']- **字典访问**：使用 `['key']` 访问字典值
- **列表索引**：使用 `[0]` 访问列表第一个元素
- **链式访问**：可以连续访问嵌套的数据结构

#### 2.9 注释 (Comment)ython
# 使用示例- **`#`**：单行注释符号
- **用途**：解释代码，提高可读性

---

## 知识点总结

### 基础概念
1. ✅ **输出函数**：`print()`
2. ✅ **变量和赋值**：`variable = value`
3. ✅ **数据类型**：字符串、字典、列表
4. ✅ **函数定义**：`def function_name():`
5. ✅ **模块导入**：`import module_name`

### 数据结构
1. ✅ **字符串 (String)**：`"text"`
2. ✅ **列表 (List)**：`[item1, item2]`
3. ✅ **字典 (Dictionary)**：`{"key": "value"}`

### 控制流
1. ✅ **条件语句**：`if-else`
2. ✅ **异常处理**：`raise Exception`

### 高级应用
1. ✅ **HTTP 请求**：使用 `requests` 库
2. ✅ **API 调用**：POST 请求发送 JSON 数据
3. ✅ **JSON 处理**：解析 API 响应
4. ✅ **嵌套数据访问**：字典和列表的组合使用

---

## 学习进度

- [x] Python 基础语法
- [x] 函数定义和调用
- [x] 数据结构（字符串、列表、字典）
- [x] 模块导入和使用
- [x] HTTP 请求和 API 调用
- [x] 条件判断和异常处理

---

## 下一步学习建议

1. 学习更多数据类型（元组、集合）
2. 掌握循环语句（for、while）
3. 深入学习函数（参数类型、返回值）
4. 学习文件操作
5. 了解面向对象编程（类、对象）


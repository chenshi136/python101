def check_end_conversation(reply):
    """
    检查AI回复是否表示结束对话
    
    Args:
        reply: AI的回复内容
    
    Returns:
        bool: 如果表示结束则返回True，否则返回False
    """
    reply_cleaned = reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
    return reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned)

def process_user_input(user_input):
    """
    处理用户输入，检查是否要结束对话
    
    Args:
        user_input: 用户输入的内容
    
    Returns:
        bool: 如果用户要结束对话则返回True，否则返回False
    """
    return user_input.strip() == "再见"
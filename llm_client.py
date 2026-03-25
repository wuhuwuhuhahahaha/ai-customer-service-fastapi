from openai import OpenAI
import json
from tools import FUNCTIONS_SCHEMA, FUNCTION_MAP

# 创建客户端
client = OpenAI(
    api_key='sk-b121cc392fe64cb3a01b85bc1ea92c55',
    base_url='https://api.deepseek.com/v1'
)

# 4. 对话历史（包含短期记忆）
conversation_history = [
    {'role': 'system', 'content': '你是一个智能助手，必须使用提供的工具函数来回答用户问题。\n\n【重要指令】\n当用户提到以下关键词时，你**必须**调用相应的函数：\n\n1. **订单号**（如 1001、1002、1003）→ 必须调用 get_order_status 函数\n2. **退款/退货 + 金额 + 天数** → 必须调用 calculate_refund 函数\n3. **加法/计算** → 必须调用 add_numbers 函数\n\n【函数说明】\n- get_order_status(order_id): 查询订单状态，需要订单号参数\n- calculate_refund(amount, days): 计算退款，需要金额和天数参数\n- add_numbers(a, b): 加法计算，需要两个数字参数\n\n【回答规则】\n1. 首先判断用户问题是否需要调用函数\n2. 如果需要，立即调用相应函数获取真实数据\n3. 基于函数返回的真实数据回答用户\n4. 绝对不要编造数据！必须使用函数返回的真实数据！\n\n【示例】\n用户：“订单 1001 发货了吗？”→ 你应该调用 get_order_status(order_id="1001")\n用户：“5000 元过了 10 天能退多少？”→ 你应该调用 calculate_refund(amount=5000, days=10)\n用户：“5 加 3 等于几？”→ 你应该调用 add_numbers(a=5, b=3)'}
]


def chat_with_function_calling(user_input):
    # 添加用户消息
    conversation_history.append({'role': 'user', 'content': user_input})

    # 发送请求（带上函数定义）
    response = client.chat.completions.create(
        model='deepseek-chat',
        messages=conversation_history,
        functions=FUNCTIONS_SCHEMA,
        function_call="auto"  # auto 表示让 AI 自动决定是否调用函数
    )

    message = response.choices[0].message

    # 检查 AI 是否想调用函数
    if message.function_call:
        function_name = message.function_call.name
        function_args = json.loads(message.function_call.arguments)

        print(f"🤖 AI 决定调用函数：{function_name}")
        print(f"📋 参数：{function_args}")

        # 调用实际函数
        if function_name in FUNCTION_MAP:
            result = FUNCTION_MAP[function_name](**function_args)
        else:
            result = f"错误：未找到函数 {function_name}"

        # 把函数结果返回给 AI
        conversation_history.append({
            'role': 'assistant',
            'content': None,
            'function_call': {
                'name': function_name,
                'arguments': json.dumps(function_args)
            }
        })

        conversation_history.append({
            'role': 'function',
            'name': function_name,
            'content': str(result) if not isinstance(result, dict) else json.dumps(result, ensure_ascii=False)
        })

        # 再次请求 AI，让它基于函数结果生成回复
        second_response = client.chat.completions.create(
            model='deepseek-chat',
            messages=conversation_history,
            functions=FUNCTIONS_SCHEMA,
            function_call="auto"
        )

        ai_response = second_response.choices[0].message.content
        
        # 返回包含函数调用信息的字典
        return {
            'response': ai_response,
            'function_called': function_name,
            'function_result': result if isinstance(result, dict) else {'result': result}
        }
    else:
        # 没有调用函数，直接回复
        ai_response = message.content
        conversation_history.append({'role': 'assistant', 'content': ai_response})
        
        # 返回没有函数调用的字典
        return {
            'response': ai_response,
            'function_called': None,
            'function_result': None
        }


# 测试
if __name__ == '__main__':
    print("="*50)
    print("🤖 多功能智能助手")
    print("="*50)
    print("\n💡 我可以帮您：")
    print("  • 加法计算（如：5 加 3 等于多少？）")
    print("  • 订单查询（如：查询订单 1001）")
    print("  • 退款计算（如：5000 元过了 10 天能退多少？）")
    print("\n输入 '退出' 结束对话\n")
    
    while True:
        user_input = input("你：")
        if user_input.lower() in ['退出', 'quit', 'exit']:
            print("\n👋 感谢使用，再见！")
            break

        response = chat_with_function_calling(user_input)
        print(f"AI：{response}\n")

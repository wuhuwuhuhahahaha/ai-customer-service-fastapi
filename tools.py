"""
工具函数模块
存放所有可被 AI 调用的工具函数
"""

import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def add_numbers(a, b):
    """计算两个数的和"""
    logger.info(f"调用加法函数：add_numbers(a={a}, b={b})")
    result = a + b
    logger.info(f"加法计算结果：{a} + {b} = {result}")
    return result


def calculate_refund(amount, days):
    """
    计算退款金额

    Args:
        amount: 订单金额
        days: 购买天数

    Returns:
        退款信息字典
    """
    logger.info(f"调用退款计算函数：calculate_refund(amount={amount}, days={days})")

    if days <= 7:
        refund_rate = 1.0
    elif days <= 15:
        refund_rate = 0.8
    else:
        refund_rate = 0.5

    refund_amount = amount * refund_rate
    result = {
        "original_amount": amount,
        "refund_amount": refund_amount,
        "refund_rate": f"{refund_rate * 100}%",
        "reason": f"购买{days}天，适用退款政策：{refund_rate * 100}%"
    }

    logger.info(f"退款计算完成：订单金额={amount}, 退款金额={refund_amount}, 退款率={refund_rate * 100}%")
    return result


def get_order_status(order_id):
    """
    查询订单状态

    Args:
        order_id: 订单号

    Returns:
        订单状态信息
    """
    logger.info(f"调用订单查询函数：get_order_status(order_id={order_id})")

    orders = {
        "1001": {
            "status": "已发货",
            "location": "北京",
            "time": "2024-03-05 14:30",
            "product": "无线蓝牙耳机",
            "quantity": 1,
            "price": 299,
            "tracking_number": "SF123456789",
            "estimated_delivery": "2023 年 10 月 15 日"
        },
        "1002": {
            "status": "配送中",
            "location": "上海",
            "time": "2024-03-06 09:15",
            "product": "智能手表",
            "quantity": 2,
            "price": 599,
            "tracking_number": "SF987654321",
            "estimated_delivery": "2023 年 10 月 18 日"
        },
        "1003": {
            "status": "已签收",
            "location": "广州",
            "time": "2024-03-04 16:20",
            "product": "机械键盘",
            "quantity": 1,
            "price": 459,
            "tracking_number": "SF112233445",
            "estimated_delivery": "2023 年 10 月 10 日"
        },
    }

    result = orders.get(order_id, {"status": "未找到订单", "location": None, "time": None})
        
    if result["status"] == "未找到订单":
        logger.warning(f"未找到订单：order_id={order_id}")
    else:
        logger.info(f"订单查询结果：order_id={order_id}, status={result['status']}, location={result['location']}")
        
    return result


# ... existing code ...


# ... existing code ...


# 函数描述（告诉 AI 这些函数的作用）
FUNCTIONS_SCHEMA = [
    {
        "name": "add_numbers",
        "description": "计算两个数字的和，当用户需要做加法运算时使用",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "第一个加数"
                },
                "b": {
                    "type": "number",
                    "description": "第二个加数"
                }
            },
            "required": ["a", "b"]
        }
    },
    {
        "name": "calculate_refund",
        "description": "计算退款金额，当用户咨询退款、退货时使用",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "订单金额"
                },
                "days": {
                 "type": "number",
                    "description": "购买天数"
                }
            },
            "required": ["amount", "days"]
        }
    },
    {
        "name": "get_order_status",
        "description": "查询订单状态和物流信息。系统存储了订单号、状态、地点、时间、商品名称、数量、价格、物流单号和预计送达时间。当用户询问订单、物流、发货等问题时使用此函数获取真实数据。",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "订单编号，例如：1001"
                }
            },
            "required": ["order_id"]
        }
    }
]

# 函数映射（函数名 -> 实际函数）
FUNCTION_MAP = {
    "add_numbers": add_numbers,
    "calculate_refund": calculate_refund,
    "get_order_status": get_order_status
}

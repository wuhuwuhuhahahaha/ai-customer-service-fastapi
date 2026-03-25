"""
工具函数模块
存放所有可被 AI 调用的工具函数
"""

import logging
import pymysql
from typing import List, Dict, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


# MySQL 数据库配置（请根据实际情况修改）
DB_CONFIG = {
    'host': 'localhost',        # 数据库地址
    'port': 3306,               # 数据库端口
    'user': 'root',             # 数据库用户名
    'password': '20040729aA', # 数据库密码
    'database': 'sky', # 数据库名称
    'charset': 'utf8mb4'
}


def execute_sql_query(sql: str) -> Dict[str, Any]:
    """
    执行 SQL 查询语句
    
    Args:
        sql: SQL 查询语句
        
    Returns:
        查询结果字典，包含 success(是否成功)、data(数据列表)、error(错误信息)
    """
    logger.info(f"调用数据库查询函数：execute_sql_query(sql={sql})")
    
    try:
        # 建立数据库连接
        connection = pymysql.connect(**DB_CONFIG)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            
            # 将结果转换为普通字典（处理 Decimal、datetime 等特殊类型）
            data = []
            for row in results:
                clean_row = {}
                for key, value in row.items():
                    # 处理 Decimal 类型
                    if hasattr(value, '__float__'):
                        clean_row[key] = float(value)
                    # 处理 datetime 类型
                    elif hasattr(value, 'strftime'):
                        clean_row[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        clean_row[key] = value
                data.append(clean_row)
            
            logger.info(f"数据库查询成功，返回{len(data)}条记录")
            return {
                'success': True,
                'data': data,
                'row_count': len(data)
            }
            
    except Exception as e:
        error_msg = f"数据库查询失败：{str(e)}"
        logger.error(error_msg)
        return {
            'success': False,
            'error': error_msg,
            'data': []
        }
    finally:
        if 'connection' in locals() and connection:
            connection.close()


def get_table_info(table_name: str) -> Dict[str, Any]:
    """
    获取表结构信息
    
    Args:
        table_name: 表名
        
    Returns:
        表结构信息
    """
    logger.info(f"调用表结构查询函数：get_table_info(table_name={table_name})")
    
    try:
        connection = pymysql.connect(**DB_CONFIG)
        
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 查询列信息
            cursor.execute("""
                SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_COMMENT
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s
                ORDER BY ORDINAL_POSITION
            """, (DB_CONFIG['database'], table_name))
            
            columns = cursor.fetchall()
            
            # 处理列信息中的特殊类型
            clean_columns = []
            for col in columns:
                clean_col = {}
                for key, value in col.items():
                    if hasattr(value, '__float__'):
                        clean_col[key] = float(value)
                    elif hasattr(value, 'strftime'):
                        clean_col[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        clean_col[key] = value
                clean_columns.append(clean_col)
            
            # 查询前 5 条数据示例
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
            sample_data = cursor.fetchall()
            
            # 处理示例数据中的特殊类型
            clean_sample_data = []
            for row in sample_data:
                clean_row = {}
                for key, value in row.items():
                    if hasattr(value, '__float__'):
                        clean_row[key] = float(value)
                    elif hasattr(value, 'strftime'):
                        clean_row[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        clean_row[key] = value
                clean_sample_data.append(clean_row)
            
            logger.info(f"表结构查询成功：{table_name} 表共有{len(columns)}个字段")
            return {
                'success': True,
                'table_name': table_name,
                'columns': clean_columns,
                'sample_data': clean_sample_data
            }
            
    except Exception as e:
        error_msg = f"查询表结构失败：{str(e)}"
        logger.error(error_msg)
        return {
            'success': False,
            'error': error_msg
        }
    finally:
        if 'connection' in locals() and connection:
            connection.close()


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
        "name": "execute_sql_query",
        "description": "执行 SQL 查询语句来获取数据库中的数据。当用户需要了解数据库内容、查询数据时使用此函数。可以执行 SELECT 语句查询任何表的数据。",
        "parameters": {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "SQL 查询语句，例如：SELECT * FROM users LIMIT 10"
                }
            },
            "required": ["sql"]
        }
    },
    {
        "name": "get_table_info",
        "description": "获取指定表的结构信息和示例数据。当用户想了解某个表有哪些字段、数据类型时使用此函数。",
        "parameters": {
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "表名，例如：users、orders"
                }
            },
            "required": ["table_name"]
        }
    },
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
    "execute_sql_query": execute_sql_query,
    "get_table_info": get_table_info,
    "add_numbers": add_numbers,
    "calculate_refund": calculate_refund,
    "get_order_status": get_order_status
}

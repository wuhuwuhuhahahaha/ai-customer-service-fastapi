"""
AI 服务接口 - 使用 FastAPI 暴露 AI 功能
可以通过 HTTP 请求调用大模型和工具函数
"""

import logging
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# 导入 AI 功能
from tools import FUNCTIONS_SCHEMA, FUNCTION_MAP
from llm_client import chat_with_function_calling, conversation_history

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 创建 FastAPI 应用
app = FastAPI(
    title="AI 智能助手服务",
    description="提供大模型对话和工具函数调用功能",
    version="1.0.0"
)

# 配置 CORS（允许跨域请求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源访问
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

# ========== 数据模型 ==========

class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str  # 用户消息

class ChatResponse(BaseModel):
    """聊天响应模型"""
    success: bool  # 是否成功
    message: str  # AI 回复内容
    data: dict = None  # 附加数据
    function_called: Optional[str] = None  # 调用的函数名
    function_result: Optional[dict] = None  # 函数返回结果

class ClearRequest(BaseModel):
    """清空记忆请求模型"""
    pass

class ToolCallRequest(BaseModel):
    """直接调用工具请求模型"""
    tool_name: str = None  # 工具名称（可选，如果不填则 AI 自动识别）
    arguments: dict = None  # 工具参数（可选，如果不填则 AI 自动提取）
    message: str = None  # 自然语言描述（可选，如果提供则 AI 自动解析）

# ========== API 接口 ==========

@app.get("/")
async def root():
    """根路径 - 服务信息"""
    return {
        "service": "AI 智能助手服务",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"  # API 文档地址
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    聊天接口 - 与大模型对话
    
    示例：
    - 5 加 3 等于多少？
    - 查询订单 1001
    - 5000 元过了 10 天能退多少？
    """
    try:
        logger.info(f"📥 收到用户消息：{request.message}")
        
        # 调用 AI 对话（返回函数调用信息）
        result = chat_with_function_calling(request.message)
        
        # 解析结果
        if isinstance(result, dict):
            response_text = result.get('response', '')
            function_called = result.get('function_called')
            function_result = result.get('function_result')
            
            if function_called:
                logger.info(f"✅ AI 调用了函数：{function_called}")
                logger.info(f"📊 函数返回：{function_result}")
            else:
                logger.info("ℹ️ AI 未调用函数，直接生成回复")
        else:
            response_text = result
            function_called = None
            function_result = None
        
        logger.info(f"📤 返回给用户：{response_text[:100]}...")
        
        return ChatResponse(
            success=True,
            message=response_text,
            data={
                "reply": response_text,
                "user_message": request.message
            },
            function_called=function_called,
            function_result=function_result
        )
    
    except Exception as e:
        logger.error(f"❌ 处理失败：{e}")
        raise HTTPException(
            status_code=500,
            detail=f"AI 处理失败：{str(e)}"
        )

@app.post("/api/clear")
async def clear_memory():
    """清空对话历史"""
    try:
        # 清空对话历史（保留 system 消息）
        conversation_history.clear()
        conversation_history.append({
            'role': 'system',
            'content': '你是一个多功能智能助手，可以帮助用户进行数学计算、查询订单、计算退款等'
        })
        
        return {
            "success": True,
            "message": "对话历史已清空"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"清空失败：{str(e)}"
        )

@app.post("/api/tool")
async def call_tool(request: ToolCallRequest):
    """
    调用工具函数（支持两种模式）
    
    模式 1：直接调用 - 指定 tool_name 和 arguments
    模式 2：智能调用 - 只提供 message，自动识别函数和参数
    
    可用工具：
    - add_numbers: 加法计算
    - calculate_refund: 退款计算
    - get_order_status: 订单查询
    """
    try:
        # 如果提供了自然语言 message，智能识别
        if request.message and not request.tool_name:
            logger.info(f"📥 收到自然语言请求：{request.message}")
            
            import re
            message = request.message
            
            # 智能识别订单号
            order_match = re.search(r'订单 (\d+)', message)
            if order_match:
                order_id = order_match.group(1)
                logger.info(f"🔍 识别到订单号：{order_id}")
                
                # 直接调用订单查询函数
                tool_func = FUNCTION_MAP['get_order_status']
                result = tool_func(order_id=order_id)
                
                return {
                    "success": True,
                    "tool_name": "get_order_status",
                    "result": result,
                    "ai_reply": f"订单 {order_id} 查询成功：{result.get('status', '未知状态')}，商品：{result.get('product', '未知')}，物流：{result.get('location', '未知')}"
                }
            
            # 智能识别退款计算
            refund_match = re.search(r'(\d+).*元.*?(\d+).*天', message)
            if refund_match:
                amount = float(refund_match.group(1))
                days = int(refund_match.group(2))
                logger.info(f"💰 识别到退款计算：金额={amount}, 天数={days}")
                
                tool_func = FUNCTION_MAP['calculate_refund']
                result = tool_func(amount=amount, days=days)
                
                return {
                    "success": True,
                    "tool_name": "calculate_refund",
                    "result": result,
                    "ai_reply": f"根据退款政策，{amount}元过了{days}天可以退还{result.get('refund_amount', 0)}元（退款比例：{result.get('refund_rate', '0%')}）"
                }
            
            # 智能识别加法计算
            add_match = re.search(r'(\d+)\s*[加+加]\s*(\d+)', message)
            if add_match:
                a = float(add_match.group(1))
                b = float(add_match.group(2))
                logger.info(f"🔢 识别到加法计算：{a} + {b}")
                
                tool_func = FUNCTION_MAP['add_numbers']
                result = tool_func(a=a, b=b)
                
                return {
                    "success": True,
                    "tool_name": "add_numbers",
                    "result": result,
                    "ai_reply": f"{a} 加 {b} 等于 {result}"
                }
            
            # 如果都没匹配到，返回错误
            return {
                "success": False,
                "tool_name": None,
                "result": None,
                "ai_reply": "抱歉，我没有理解您的请求。请明确说明您要查询的订单号、退款金额和天数，或者需要计算的数字。"
            }
        
        # 否则使用直接调用模式
        # 检查工具是否存在
        if not request.tool_name:
            raise HTTPException(
                status_code=400,
                detail="请提供 tool_name 或者 message 参数"
            )
        
        if request.tool_name not in FUNCTION_MAP:
            raise HTTPException(
                status_code=404,
                detail=f"工具不存在：{request.tool_name}"
            )
        
        # 调用工具函数
        tool_func = FUNCTION_MAP[request.tool_name]
        result = tool_func(**request.arguments)
        
        return {
            "success": True,
            "tool_name": request.tool_name,
            "result": result
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ 工具调用失败：{e}")
        raise HTTPException(
            status_code=500,
            detail=f"工具调用失败：{str(e)}"
        )

@app.get("/api/tools")
async def list_tools():
    """获取所有可用工具列表"""
    return {
        "success": True,
        "tools": FUNCTIONS_SCHEMA
    }

# ========== 主函数 ==========

if __name__ == "__main__":
    print("="*50)
    print("🚀 AI 服务启动")
    print("="*50)
    print("📡 访问地址：http://127.0.0.1:8000")
    print("📚 API 文档：http://127.0.0.1:8000/docs")
    print("💬 聊天接口：POST /api/chat")
    print(" 工具接口：POST /api/tool")
    print("🧹 清空接口：POST /api/clear")
    print("="*50)
    
    # 启动服务器
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

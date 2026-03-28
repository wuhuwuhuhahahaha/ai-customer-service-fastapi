# AI Customer Service FastAPI

基于 FastAPI 的 AI 客服系统，支持多 LLM 模型调用和工具函数集成。

## 项目结构

```
├── main.py              # 主入口
── ai_server.py         # AI 服务核心逻辑
├── llm_client.py        # LLM 客户端封装
├── tools.py             # 工具函数模块
├── start_server.py      # 服务启动脚本
├── requirements.txt     # 依赖包
└── .env.example         # 环境变量示例
```

## 核心功能

- ✅ FastAPI REST 服务
- ✅ 多 LLM 模型支持（千问等）
- ✅ 工具函数调用（文件读写、搜索替换等）
- ✅ AI 客服对话

## 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 配置 API Key
在代码中配置你的阿里云千问 API Key

### 3. 启动服务
```bash
python start_server.py
```

## 使用示例

```python
from llm_client import LLMClient

client = LLMClient()
response = client.chat("你好，有什么可以帮助你的？")
```

## 技术栈

- Python 3.x
- FastAPI
- 阿里云千问 API

## 许可证

MIT

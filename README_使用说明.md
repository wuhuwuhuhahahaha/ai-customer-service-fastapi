# Python AI 服务启动说明

## 📁 项目结构

```
PythonProject/
├── tools.py              # 工具函数模块（加法、订单、退款等）
├── llm_client.py         # AI 对话客户端
├── ai_server.py          # FastAPI 服务（对外暴露接口）
├── start_server.py       # 启动脚本（自动安装依赖）
├── test_api.py           # 测试脚本
├── requirements.txt      # 依赖列表
└── README_使用说明.md    # 本文档
```

## 🚀 快速启动

### 方法 1：使用启动脚本（推荐）

```bash
python start_server.py
```

这个脚本会：
1. 自动检查依赖是否安装
2. 如果缺少依赖，自动安装
3. 启动 AI 服务

### 方法 2：手动启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动服务
python ai_server.py
```

## ✅ 启动成功标志

看到以下输出表示服务启动成功：

```
==================================================
🚀 启动 AI 服务
==================================================
📡 访问地址：http://127.0.0.1:8000
📚 API 文档：http://127.0.0.1:8000/docs
💬 聊天接口：POST /api/chat
 工具接口：POST /api/tool
🧹 清空接口：POST /api/clear
==================================================
INFO:     Application startup complete.
```

## 🧪 测试服务

### 方法 1：使用测试脚本

打开**另一个终端**，运行：

```bash
python test_api.py
```

会自动测试所有功能。

### 方法 2：浏览器访问 API 文档

打开浏览器访问：http://127.0.0.1:8000/docs

可以看到交互式 API 文档，直接在网页上测试。

### 方法 3：使用 curl 命令

```bash
# 健康检查
curl http://127.0.0.1:8000/health

# 聊天测试
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好"}'

# 加法测试
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "5 加 3 等于多少？"}'

# 直接调用工具
curl -X POST http://127.0.0.1:8000/api/tool \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "add_numbers", "arguments": {"a": 10, "b": 20}}'
```

## 📡 API 接口列表

### 1. 聊天接口
- **URL**: `/api/chat`
- **方法**: POST
- **参数**: 
  ```json
  {
    "message": "用户消息"
  }
  ```
- **响应**:
  ```json
  {
    "success": true,
    "message": "AI 回复内容",
    "data": {
      "reply": "AI 回复",
      "user_message": "用户消息"
    }
  }
  ```

### 2. 工具调用接口
- **URL**: `/api/tool`
- **方法**: POST
- **参数**:
  ```json
  {
    "tool_name": "add_numbers",
    "arguments": {"a": 10, "b": 20}
  }
  ```

### 3. 清空记忆接口
- **URL**: `/api/clear`
- **方法**: POST

### 4. 工具列表接口
- **URL**: `/api/tools`
- **方法**: GET

## 🔧 可用工具

系统内置以下工具函数：

1. **add_numbers** - 加法计算
   - 参数：`a` (数字), `b` (数字)
   
2. **calculate_refund** - 退款计算
   - 参数：`amount` (金额), `days` (天数)
   
3. **get_order_status** - 订单查询
   - 参数：`order_id` (订单号)

## 💻 Java 调用示例

```java
OkHttpClient client = new OkHttpClient();
MediaType JSON = MediaType.get("application/json; charset=utf-8");

// 构建请求
JSONObject json = new JSONObject();
json.put("message", "5 加 3 等于多少？");
RequestBody body = RequestBody.create(json.toString(), JSON);

// 发送请求
Request request = new Request.Builder()
    .url("http://127.0.0.1:8000/api/chat")
    .post(body)
    .build();

try (Response response = client.newCall(request).execute()) {
    String responseBody = response.body().string();
    JSONObject jsonResponse = new JSONObject(responseBody);
    String aiReply = jsonResponse.getString("message");
    System.out.println("AI 回复：" + aiReply);
}
```

## ⚠️ 常见问题

### 1. 端口被占用
错误：`Address already in use`

解决：修改 `ai_server.py` 中的端口号（8000 改为其他）

### 2. 依赖未安装
错误：`ModuleNotFoundError`

解决：运行 `pip install -r requirements.txt`

### 3. 无法访问服务
检查：
- 服务是否已启动
- 防火墙是否阻止
- 访问地址是否正确（http://127.0.0.1:8000）

## 🛑 停止服务

在运行服务的终端按 `Ctrl + C`

## 📝 下一步

服务启动后，你可以：

1. ✅ 在浏览器访问 http://127.0.0.1:8000/docs 查看 API 文档
2. ✅ 使用测试脚本验证功能
3. ✅ 在 Java 项目中调用这些 API
4. ✅ 添加更多工具函数到 `tools.py`

## 🎯 完整调用流程

```
Java 项目 → HTTP 请求 → Python FastAPI → AI 大模型 → 返回结果
```

Java 代码只需要发送 HTTP 请求即可调用 AI 功能！

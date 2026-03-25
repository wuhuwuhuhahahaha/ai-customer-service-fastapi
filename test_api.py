"""
测试脚本 - 验证 AI 服务是否正常
在另一个终端运行此脚本
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """测试健康检查"""
    print("\n📋 测试 1: 健康检查")
    print("-" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"✅ 服务正常：{response.json()}")
            return True
        else:
            print(f"❌ 健康检查失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到服务：{e}")
        print("💡 请先运行 start_server.py 启动服务")
        return False

def test_chat():
    """测试聊天功能"""
    print("\n📋 测试 2: 聊天功能")
    print("-" * 50)
    
    try:
        data = {"message": "你好"}
        response = requests.post(f"{BASE_URL}/api/chat", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 聊天成功")
            print(f"   用户：你好")
            print(f"   AI: {result['message'][:50]}...")
            return True
        else:
            print(f"❌ 聊天失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False

def test_add():
    """测试加法功能"""
    print("\n📋 测试 3: 加法计算")
    print("-" * 50)
    
    try:
        data = {"message": "5 加 3 等于多少？"}
        response = requests.post(f"{BASE_URL}/api/chat", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 加法计算成功")
            print(f"   用户：5 加 3 等于多少？")
            print(f"   AI: {result['message']}")
            return True
        else:
            print(f"❌ 测试失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False

def test_order_query():
    """测试订单查询"""
    print("\n📋 测试 4: 订单查询")
    print("-" * 50)
    
    try:
        data = {"message": "查询订单 1001"}
        response = requests.post(f"{BASE_URL}/api/chat", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 订单查询成功")
            print(f"   用户：查询订单 1001")
            print(f"   AI: {result['message']}")
            return True
        else:
            print(f"❌ 测试失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False

def test_direct_tool():
    """测试直接调用工具"""
    print("\n📋 测试 5: 直接调用工具")
    print("-" * 50)
    
    try:
        data = {
            "tool_name": "add_numbers",
            "arguments": {"a": 10, "b": 20}
        }
        response = requests.post(f"{BASE_URL}/api/tool", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 工具调用成功")
            print(f"   工具：add_numbers")
            print(f"   参数：a=10, b=20")
            print(f"   结果：{result['result']}")
            return True
        else:
            print(f"❌ 测试失败：{response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        return False

def main():
    """主函数"""
    print("="*50)
    print("🧪 AI 服务测试")
    print("="*50)
    
    # 先测试健康检查
    if not test_health():
        print("\n" + "="*50)
        print("❌ 服务未启动，测试终止")
        print("="*50)
        return
    
    # 运行其他测试
    tests = [test_chat, test_add, test_order_query, test_direct_tool]
    passed = 0
    failed = 0
    
    for test in tests:
        if test():
            passed += 1
        else:
            failed += 1
    
    # 输出结果
    print("\n" + "="*50)
    print(f"📊 测试结果：{passed} 通过，{failed} 失败")
    print("="*50)
    
    if failed == 0:
        print("\n✅ 所有测试通过！服务运行正常")
    else:
        print(f"\n⚠️  有 {failed} 个测试失败，请检查日志")

if __name__ == "__main__":
    main()

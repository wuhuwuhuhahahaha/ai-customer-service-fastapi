"""
项目启动脚本
运行此脚本启动 AI 服务
"""

import sys
import subprocess

def check_and_install_dependencies():
    """检查并安装依赖"""
    print("="*50)
    print("📦 检查依赖...")
    print("="*50)
    
    required_packages = {
        'openai': 'openai',
        'fastapi': 'fastapi',
        'uvicorn': 'uvicorn',
        'pydantic': 'pydantic'
    }
    
    missing = []
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            missing.append(pip_name)
    
    if missing:
        print("\n⚠️  发现缺失的依赖，正在安装...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
        print("✅ 依赖安装完成！\n")
    else:
        print("\n✅ 所有依赖已就绪！\n")

def start_server():
    """启动服务器"""
    print("="*50)
    print("🚀 启动 AI 服务")
    print("="*50)
    
    try:
        import uvicorn
        uvicorn.run(
            "ai_server:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except Exception as e:
        print(f"\n❌ 启动失败：{e}")
        print("\n请确保已安装所有依赖：")
        print("pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    check_and_install_dependencies()
    start_server()

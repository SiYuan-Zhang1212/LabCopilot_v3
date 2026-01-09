#!/usr/bin/env python3
"""
Lab Diary AI 部署脚本
支持本地运行、Docker部署、云端部署
"""

import os
import sys
import subprocess
import webbrowser
import time
import platform

def check_requirements():
    """检查必要的依赖是否安装"""
    print("🔍 检查依赖...")
    
    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ Python版本过低，需要3.8或更高版本")
        return False
    
    # 检查pip
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print("✅ pip 已安装")
    except subprocess.CalledProcessError:
        print("❌ 未找到pip")
        return False
    
    return True

def install_dependencies():
    """安装依赖包"""
    print("📦 安装依赖包...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖包安装失败: {e}")
        return False

def run_local():
    """本地运行应用"""
    print("🚀 启动本地应用...")
    print("📱 应用将在浏览器中打开 http://localhost:8501")
    print("🛑 按 Ctrl+C 停止服务")
    
    try:
        # 启动Streamlit应用
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app.py",
            "--server.port=8501",
            "--server.address=localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 服务已停止")
    except Exception as e:
        print(f"❌ 启动失败: {e}")

def run_docker():
    """使用Docker运行应用"""
    print("🐳 使用Docker启动应用...")
    
    # 检查Docker是否安装
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        print("✅ Docker 已安装")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 未找到Docker，请先安装Docker")
        return
    
    # 检查docker-compose是否安装
    try:
        subprocess.run(["docker-compose", "--version"], capture_output=True, check=True)
        print("✅ Docker Compose 已安装")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ 未找到Docker Compose")
        return
    
    print("📦 构建Docker镜像...")
    try:
        subprocess.run(["docker-compose", "build"], check=True)
        print("✅ Docker镜像构建完成")
        
        print("🚀 启动Docker容器...")
        subprocess.run(["docker-compose", "up", "-d"], check=True)
        print("✅ Docker容器已启动")
        
        print("📱 应用地址: http://localhost:8501")
        print("🛑 使用 'docker-compose down' 停止服务")
        
        # 自动打开浏览器
        time.sleep(3)
        webbrowser.open("http://localhost:8501")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker启动失败: {e}")

def deploy_to_cloud():
    """部署到云端"""
    print("☁️ 云端部署选项:")
    print("1. Streamlit Cloud (推荐 - 免费)")
    print("2. Render.com")
    print("3. Railway.app")
    print("4. Heroku")
    
    choice = input("请选择 (1-4): ").strip()
    
    if choice == "1":
        deploy_to_streamlit_cloud()
    elif choice == "2":
        deploy_to_render()
    elif choice == "3":
        deploy_to_railway()
    elif choice == "4":
        deploy_to_heroku()
    else:
        print("❌ 无效选择")

def deploy_to_streamlit_cloud():
    """部署到Streamlit Cloud"""
    print("📋 Streamlit Cloud 部署步骤:")
    print("1. 访问 https://share.streamlit.io")
    print("2. 点击 'New app'")
    print("3. 选择您的GitHub仓库")
    print("4. 设置主文件为: app.py")
    print("5. 点击 'Deploy'")
    print("\n📦 需要上传的文件:")
    print("- app.py")
    print("- lab_diary_optimized.py")
    print("- requirements.txt")
    print("\n🌐 部署完成后，您将获得一个公开的URL")
    
    # 检查是否有Git仓库
    if os.path.exists(".git"):
        print("\n✅ 检测到Git仓库")
        # 检查是否有requirements.txt
        if os.path.exists("requirements.txt"):
            print("✅ requirements.txt 已存在")
        else:
            print("⚠️  请确保 requirements.txt 已提交")
    else:
        print("\n⚠️  建议初始化Git仓库并上传到GitHub")
        print("   git init")
        print("   git add .")
        print("   git commit -m 'Initial commit'")
        print("   git remote add origin <your-github-repo>")
        print("   git push -u origin main")
    
    # 打开Streamlit Cloud
    open_browser = input("🌐 是否打开Streamlit Cloud? (y/n): ").strip().lower()
    if open_browser == 'y':
        webbrowser.open("https://share.streamlit.io")

def deploy_to_render():
    """部署到Render.com"""
    print("📋 Render.com 部署步骤:")
    print("1. 访问 https://render.com")
    print("2. 创建新的Web Service")
    print("3. 连接到您的GitHub仓库")
    print("4. 设置环境:")
    print("   - Environment: Python")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: streamlit run app.py --server.port=10000 --server.address=0.0.0.0")
    print("5. 点击 'Create Web Service'")
    
    open_browser = input("🌐 是否打开Render.com? (y/n): ").strip().lower()
    if open_browser == 'y':
        webbrowser.open("https://render.com")

def deploy_to_railway():
    """部署到Railway.app"""
    print("📋 Railway.app 部署步骤:")
    print("1. 访问 https://railway.app")
    print("2. 创建新项目")
    print("3. 从GitHub部署")
    print("4. 添加Streamlit服务")
    print("5. 部署应用")
    
    open_browser = input("🌐 是否打开Railway.app? (y/n): ").strip().lower()
    if open_browser == 'y':
        webbrowser.open("https://railway.app")

def deploy_to_heroku():
    """部署到Heroku"""
    print("📋 Heroku 部署步骤:")
    print("1. 安装Heroku CLI")
    print("2. heroku login")
    print("3. heroku create your-app-name")
    print("4. git push heroku main")
    print("5. heroku ps:scale web=1")
    
    print("\n📦 需要创建的Heroku配置文件:")
    
    # 创建Heroku需要的文件
    with open("Procfile", "w") as f:
        f.write("web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0\n")
    
    with open("runtime.txt", "w") as f:
        f.write("python-3.9.18\n")
    
    with open("setup.sh", "w") as f:
        f.write("""#!/bin/bash
mkdir -p ~/.streamlit/
echo "\n[server]\nheadless = true\nenableCORS=false\nport = $PORT\n" > ~/.streamlit/config.toml
""")
    
    print("✅ 已创建 Heroku 配置文件")
    print("   - Procfile")
    print("   - runtime.txt") 
    print("   - setup.sh")
    
    open_browser = input("🌐 是否打开Heroku? (y/n): ").strip().lower()
    if open_browser == 'y':
        webbrowser.open("https://heroku.com")

def show_help():
    """显示帮助信息"""
    print("""
Lab Diary AI 部署脚本

使用方法:
    python deploy.py [选项]

选项:
    local       - 本地运行应用
    docker      - 使用Docker运行应用
    cloud       - 部署到云端
    install     - 安装依赖
    help        - 显示帮助信息

示例:
    python deploy.py local      # 本地运行
    python deploy.py docker     # Docker运行
    python deploy.py cloud      # 云端部署
""")

def main():
    """主函数"""
    print("🔬 Lab Diary AI 部署工具")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "local":
        if check_requirements():
            if not os.path.exists("requirements.txt"):
                print("❌ 未找到requirements.txt")
                return
            run_local()
    
    elif command == "docker":
        run_docker()
    
    elif command == "cloud":
        deploy_to_cloud()
    
    elif command == "install":
        if check_requirements():
            install_dependencies()
    
    elif command == "help":
        show_help()
    
    else:
        print(f"❌ 未知命令: {command}")
        show_help()

if __name__ == "__main__":
    main()

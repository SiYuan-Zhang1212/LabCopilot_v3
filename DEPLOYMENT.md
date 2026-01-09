# Lab Diary AI 部署指南

本文档详细介绍了Lab Diary AI工具的各种部署方式，包括本地部署、Docker部署和云端部署。

## 📋 目录

- [本地部署](#本地部署)
- [Docker部署](#docker部署)
- [云端部署](#云端部署)
- [部署脚本使用](#部署脚本使用)
- [常见问题](#常见问题)

## 💻 本地部署

### 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 18.04+)
- **内存**: 至少 2GB RAM
- **存储**: 至少 500MB 可用空间

### 步骤1: 安装Python

#### Windows
1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载Python 3.8或更高版本
3. 运行安装程序，确保勾选"Add Python to PATH"
4. 完成安装

#### macOS
```bash
# 使用Homebrew安装
brew install python3

# 或从官网下载安装
```

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 步骤2: 克隆或下载项目

```bash
# 如果是从Git仓库
git clone https://github.com/yourusername/lab-diary-ai.git
cd lab-diary-ai

# 如果是下载的压缩包，解压后进入目录
```

### 步骤3: 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 步骤4: 安装依赖

```bash
pip install -r requirements.txt
```

### 步骤5: 配置API密钥

推荐使用环境变量或 Streamlit secrets（避免把密钥写进代码）。

#### 方式A：使用 `.env`（本地推荐）
复制示例文件并填写：

```bash
copy .env.example .env
```

#### 方式B：使用 Streamlit secrets
复制 `.streamlit/secrets.toml.example` 为 `.streamlit/secrets.toml` 并填写：

```python
# DeepSeek API配置
DEEPSEEK_API_KEY = "your-api-key-here"

# 火山引擎ASR配置（可选）
VOLC_ASR_APP_KEY = "your-app-key"
VOLC_ASR_ACCESS_KEY = "your-access-key"
```

### 步骤6: 运行应用

```bash
streamlit run app.py
```

应用将在 http://localhost:8501 启动。

### 步骤7: 自动打开浏览器

应用启动后，会自动在默认浏览器中打开。如果没有自动打开，可以手动访问上述地址。

## 🐳 Docker部署

### 环境要求

- **Docker**: 20.10 或更高版本
- **Docker Compose**: 1.27 或更高版本

### 方法1: 使用Docker Compose（推荐）

#### 步骤1: 安装Docker和Docker Compose

**Windows/macOS**
1. 访问 [Docker官网](https://www.docker.com/products/docker-desktop)
2. 下载并安装Docker Desktop
3. Docker Compose会自动安装

**Ubuntu/Debian**
```bash
# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 步骤2: 配置环境变量

创建 `.env` 文件：

```bash
# DeepSeek API配置
DEEPSEEK_API_KEY=your-api-key-here

# 火山引擎ASR配置（可选）
VOLC_ASR_APP_KEY=your-app-key
VOLC_ASR_ACCESS_KEY=your-access-key

# Streamlit配置
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

#### 步骤3: 启动容器

```bash
docker-compose up -d
```

#### 步骤4: 查看日志

```bash
docker-compose logs -f
```

#### 步骤5: 停止容器

```bash
docker-compose down
```

### 方法2: 手动构建和运行

#### 步骤1: 构建Docker镜像

```bash
docker build -t lab-diary-ai .
```

#### 步骤2: 运行容器

```bash
docker run -d \
  --name lab-diary-ai \
  -p 8501:8501 \
  -v $(pwd)/uploads:/app/uploads \
  -v $(pwd)/backups:/app/backups \
  -e DEEPSEEK_API_KEY=your-api-key \
  lab-diary-ai
```

#### 步骤3: 查看容器状态

```bash
docker ps
docker logs lab-diary-ai
```

#### 步骤4: 停止容器

```bash
docker stop lab-diary-ai
docker rm lab-diary-ai
```

## ☁️ 云端部署

### 部署选项对比

| 平台 | 免费额度 | 部署难度 | 推荐指数 |
|------|---------|---------|---------|
| Streamlit Cloud | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐⭐ |
| Render.com | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Railway.app | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Heroku | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |

### Streamlit Cloud（推荐）

#### 优点
- ✅ 完全免费
- ✅ 部署简单
- ✅ 与GitHub集成
- ✅ 自动HTTPS
- ✅ 持续部署

#### 步骤1: 准备GitHub仓库

1. 创建新的GitHub仓库
2. 上传以下文件：
   - `app.py`
   - `lab_diary_optimized.py`
   - `requirements.txt`
   - `README.md`（可选）
   - `.streamlit/config.toml`（推荐）

#### 步骤2: 访问Streamlit Cloud

1. 访问 https://share.streamlit.io
2. 使用GitHub账号登录

#### 步骤3: 创建新应用

1. 点击 "New app"
2. 选择您的GitHub仓库
3. 设置：
   - Repository: 您的仓库
   - Branch: main（或master）
   - Main file path: `app.py`
   - App URL: （自动生成）

#### 步骤4: 配置Secrets/环境变量

1. 点击 "Advanced settings"
2. 在 Secrets（或环境变量）里添加：
   - `DEEPSEEK_API_KEY`: your-api-key
   - `VOLC_ASR_APP_KEY`: your-app-key（可选）
   - `VOLC_ASR_ACCESS_KEY`: your-access-key（可选）
   - `LAB_DIARY_AUTH_MODE`: email_otp（推荐：启用应用内邮箱验证码登录）
   - `LAB_DIARY_ALLOWED_EMAIL_DOMAINS`: yourorg.com（推荐：域名白名单，避免任何人都可请求验证码）
   - `SMTP_HOST`/`SMTP_PORT`/`SMTP_USER`/`SMTP_PASSWORD`/`SMTP_FROM`: 用于发送验证码邮件
   - （可选）`LAB_DIARY_REQUIRE_SIGNIN`: 1（如果你的 Cloud 账号提供平台级登录）

#### 步骤5: 部署

1. 点击 "Deploy"
2. 等待部署完成（约2-3分钟）
3. 获得公开访问URL

#### 步骤6: 邮箱登录与访问控制（可选）
如果你需要“用户用邮箱登录后才能访问”，优先使用平台自带的访问控制：
1. 进入 App 管理页（Manage app / Settings）
2. 打开 “Require sign-in / Private app / Manage access”（不同版本文案略有差异）
3. 在允许访问列表中添加用户邮箱

如果你的界面里没有这些选项（Community Cloud 常见），请使用应用内登录：
- 在 Secrets 中设置 `LAB_DIARY_AUTH_MODE=email_otp` 并配置 SMTP
- 可选设置 `LAB_DIARY_ALLOWED_EMAIL_DOMAINS`，实现“无需手动逐个添加邮箱”的访问控制

#### 数据持久化提醒
Streamlit Cloud 上的本地文件（包含 `my_lab_data.db`、`uploads/`、`backups/`）通常不保证长期持久化；如果你希望“多用户长期使用且数据不丢”，建议：
- 自托管（Docker + 挂载数据卷）继续使用 SQLite；或
- 改为外部数据库（如 Postgres/Supabase）存储任务与记录。

#### 步骤6: 配置自定义域名（可选）

1. 在应用设置中
2. 添加自定义域名
3. 配置DNS解析

### Render.com

#### 优点
- ✅ 免费额度充足
- ✅ 支持Docker
- ✅ 自动HTTPS
- ✅ 持续部署

#### 步骤1: 准备代码

确保您的代码在GitHub/GitLab上。

#### 步骤2: 创建Render账户

1. 访问 https://render.com
2. 注册账户
3. 连接GitHub/GitLab

#### 步骤3: 创建Web Service

1. 点击 "New" → "Web Service"
2. 选择您的仓库
3. 配置：
   - Name: lab-diary-ai
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=10000 --server.address=0.0.0.0`

#### 步骤4: 设置环境变量

在 "Environment" 标签页添加：
- `DEEPSEEK_API_KEY`: your-api-key
- `PYTHON_VERSION`: 3.9.18

#### 步骤5: 选择套餐

选择 "Free" 套餐进行测试，或选择付费套餐获得更好性能。

#### 步骤6: 部署

点击 "Create Web Service"，等待部署完成。

### Railway.app

#### 优点
- ✅ 部署快速
- ✅ 界面友好
- ✅ 支持多种语言
- ✅ 数据库集成

#### 步骤1: 准备代码

代码需要在GitHub上。

#### 步骤2: 创建Railway账户

1. 访问 https://railway.app
2. 注册账户
3. 连接GitHub

#### 步骤3: 创建新项目

1. 点击 "New Project"
2. 选择 "Deploy from GitHub repo"
3. 选择您的仓库

#### 步骤4: 添加Python服务

1. 点击 "Add Service"
2. 选择 "Python"
3. Railway会自动检测并配置

#### 步骤5: 配置环境变量

在 "Variables" 标签页添加环境变量。

#### 步骤6: 部署

Railway会自动部署，等待完成即可。

### Heroku

#### 注意
Heroku的免费套餐已停止，需要付费使用。

#### 步骤1: 安装Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# 下载安装程序：https://devcenter.heroku.com/articles/heroku-cli
```

#### 步骤2: 创建必要文件

创建 `Procfile`：
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

创建 `runtime.txt`：
```
python-3.9.18
```

创建 `setup.sh`：
```bash
#!/bin/bash
mkdir -p ~/.streamlit/
echo "\n[server]\nheadless = true\nenableCORS=false\nport = $PORT\n" > ~/.streamlit/config.toml
```

#### 步骤3: 登录Heroku

```bash
heroku login
```

#### 步骤4: 创建应用

```bash
heroku create your-app-name
```

#### 步骤5: 设置环境变量

```bash
heroku config:set DEEPSEEK_API_KEY=your-api-key
```

#### 步骤6: 部署

```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

#### 步骤7: 启动应用

```bash
heroku ps:scale web=1
```

## 🚀 部署脚本使用

我们提供了一个便捷的部署脚本 `deploy.py`。

### 使用方法

```bash
python deploy.py [命令]
```

### 可用命令

#### 本地运行
```bash
python deploy.py local
```

#### Docker部署
```bash
python deploy.py docker
```

#### 云端部署
```bash
python deploy.py cloud
```

#### 安装依赖
```bash
python deploy.py install
```

#### 显示帮助
```bash
python deploy.py help
```

### 脚本功能

- ✅ 检查环境要求
- ✅ 自动安装依赖
- ✅ 启动本地服务
- ✅ Docker容器管理
- ✅ 云端部署向导
- ✅ 自动打开浏览器

## 🔧 配置优化

### 性能优化

#### 1. Streamlit配置

在 `.streamlit/config.toml` 中添加：

```toml
[server]
maxUploadSize = 200
maxMessageSize = 200
enableCORS = false
headless = true

[browser]
gatherUsageStats = false

[runner]
fastReruns = true
```

#### 2. 数据库优化

定期清理和优化数据库：

```python
# 清理已完成任务的旧版本
# 压缩数据库文件
# 重建索引
```

#### 3. 缓存配置

使用Streamlit的缓存功能：

```python
@st.cache_data
def load_data():
    return df

@st.cache_resource
def get_database_connection():
    return conn
```

### 安全优化

#### 1. 环境变量管理

使用 `.env` 文件管理敏感信息：

```bash
# 安装python-dotenv
pip install python-dotenv

# 在代码中使用
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
```

#### 2. HTTPS配置

在Nginx中配置HTTPS：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 3. 访问控制

推荐（无需平台白名单）：启用项目内置“邮箱验证码登录”（适合 Community Cloud）。

1. 在 Secrets 中设置：
   - `LAB_DIARY_AUTH_MODE=email_otp`
   - `LAB_DIARY_ALLOWED_EMAIL_DOMAINS=yourorg.com`（建议）
   - 配置 `SMTP_HOST/SMTP_PORT/SMTP_USER/SMTP_PASSWORD/SMTP_FROM`
2. 部署后访问应用会先进入登录页，登录成功后按邮箱自动隔离数据（`data/users/<hash>/`）。

添加基本认证：

```python
import streamlit as st

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("密码", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("密码", type="password", on_change=password_entered, key="password")
        st.error("😕 密码错误")
        return False
    else:
        return True

if check_password():
    # 主应用代码
```

## 📝 监控和维护

### 日志监控

查看应用日志：

```bash
# Docker
docker logs lab-diary-ai

# Docker Compose
docker-compose logs -f

# 本地
streamlit run app.py --logger.level=debug
```

### 性能监控

使用Streamlit的metrics：

```python
import streamlit as st

@st.cache_resource
def get_performance_metrics():
    return {}
```

### 备份策略

#### 数据库备份

```bash
# 手动备份
sqlite3 my_lab_data.db ".backup backup.db"

# 自动备份（在应用中实现）
```

#### 文件备份

```bash
# 备份上传文件
tar -czf uploads_backup.tar.gz uploads/

# 备份整个应用
tar -czf lab_diary_backup.tar.gz \
    lab_diary_optimized.py \
    requirements.txt \
    my_lab_data.db \
    uploads/ \
    backups/
```

### 更新部署

#### Streamlit Cloud
- 自动更新：每次push到GitHub自动部署

#### Docker
```bash
# 拉取最新代码
git pull origin main

# 重新构建和启动
docker-compose down
docker-compose up --build -d
```

#### 云端平台
- 各平台提供自动或手动更新选项

## 🚨 常见问题

### Q1: 应用启动失败

**问题**: `streamlit: command not found`

**解决**: 
```bash
pip install streamlit
```

### Q2: 数据库连接错误

**问题**: `sqlite3.OperationalError: database is locked`

**解决**: 
- 等待其他进程释放数据库
- 重启应用
- 检查是否有多个实例运行

### Q3: AI功能不可用

**问题**: AI功能无响应

**解决**: 
- 检查API密钥是否正确
- 检查网络连接
- 查看API配额是否用完

### Q4: 语音识别失败

**问题**: 语音识别无结果

**解决**: 
- 检查麦克风权限
- 检查火山引擎配置
- 尝试重新录音

### Q5: 文件上传失败

**问题**: 文件无法上传

**解决**: 
- 检查文件大小限制
- 检查文件格式
- 检查存储空间

### Q6: 页面加载缓慢

**问题**: 页面响应慢

**解决**: 
- 优化数据库查询
- 启用缓存
- 增加服务器资源
- 使用CDN加速

### Q7: 部署后样式丢失

**问题**: CSS样式不生效

**解决**: 
- 检查静态文件路径
- 清除浏览器缓存
- 检查Streamlit配置

### Q8: 数据库迁移失败

**问题**: 历史记录导入失败

**解决**: 
- 检查文件格式
- 检查文件大小
- 查看错误日志
- 分批导入大文件

## 📞 技术支持

### 自助资源
- 📖 [README.md](README.md)
- 🐛 [GitHub Issues](https://github.com/yourusername/lab-diary-ai/issues)
- 💬 [GitHub Discussions](https://github.com/yourusername/lab-diary-ai/discussions)

### 联系方式
- 📧 Email: your-email@example.com
- 🐦 Twitter: @yourusername
- 💼 LinkedIn: Your Name

## 📄 许可证

本项目采用 MIT 许可证。查看 [LICENSE](LICENSE) 文件了解详情。

---

<div align="center">
  <p>
    <b>部署指南</b> - 让Lab Diary AI运行在任何地方
  </p>
</div>

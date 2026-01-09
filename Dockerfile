FROM python:3.9-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY lab_diary_optimized.py .
COPY uploads/ uploads/
COPY backups/ backups/

# 创建必要的目录
RUN mkdir -p uploads backups

# 暴露端口
EXPOSE 8501

# 运行应用
CMD ["streamlit", "run", "lab_diary_optimized.py", "--server.port=8501", "--server.address=0.0.0.0"]
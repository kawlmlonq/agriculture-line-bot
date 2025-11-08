# 使用 Python 3.12 基礎映像
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 複製需求檔案
COPY requirements.txt .

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用程式代碼
COPY . .

# 建立向量資料庫目錄
RUN mkdir -p /app/vector_db

# 暴露端口
EXPOSE 5000

# 設定環境變數
ENV PYTHONUNBUFFERED=1

# 啟動應用程式
CMD ["python", "app.py"]

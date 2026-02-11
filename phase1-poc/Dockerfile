# RockClaw Phase 1 POC - Docker 镜像
# 使用 python:3.11-slim 最小化基础
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码
COPY src/ ./src/
COPY .env.example .env

# 创建数据目录
RUN mkdir -p data/memory

# 暴露端口 (用于未来 WebSocket gateway)
EXPOSE 8080

# 运行交互式 Agent
CMD ["python", "-m", "src.agent"]
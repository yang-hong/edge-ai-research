#!/bin/bash
# RockClaw Phase 1 POC - 快速启动脚本

set -e

echo "🚀 RockClaw Phase 1 POC 快速启动"
echo ""

# 1. 检查 .env 配置
if [ ! -f .env ]; then
    echo "⚠️  .env 不存在，从模板创建..."
    cp .env.example .env
    echo "请编辑 .env 文件，填入你的 API 密钥:"
    echo "  - ANTHROPIC_API_KEY"
    echo "  - TELEGRAM_BOT_TOKEN (可选)"
    echo ""
    read -p "现在编辑 .env? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ${EDITOR:-vi} .env
    fi
fi

# 2. 构建 Docker 镜像
echo "🔨 构建 Docker 镜像..."
docker-compose build

# 3. 创建数据目录
mkdir -p data/memory

# 4. 启动服务
echo "✅ 启动受限容器 (1.5核, 1GB RAM)..."
echo "输入 'quit' 退出交互"
echo "---"
docker-compose up

# 5. 完成后清理
echo "---"
echo "容器已停止。查看日志: docker-compose logs -f"
echo "数据保存在: $(pwd)/data/"
#!/bin/bash
# Phase 1 POC 压力测试脚本
# 测试内存泄漏、稳定性、工具调用

set -e

CONTAINER_NAME="rockclaw-poc"
TEST_MESSAGE="这是一个压力测试消息，时间戳: $(date +%s)"
ITERATIONS=100
DELAY=5

echo "=== RockClaw Phase 1 POC 压力测试 ==="
echo "目标容器: $CONTAINER_NAME"
echo "测试迭代: $ITERATIONS 次"
echo "延迟: ${DELAY}秒"
echo ""

# 检查容器是否运行
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "错误: 容器未运行。请先执行: docker-compose up"
    exit 1
fi

echo "开始测试... (按 Ctrl+C 停止)"
echo ""

# 记录初始内存
INIT_MEM=$(docker stats --no-stream --format "{{.MemUsage}}" $CONTAINER_NAME | awk '{print $1}')
echo "初始内存: $INIT_MEM"

for i in $(seq 1 $ITERATIONS); do
    echo "[$i/$ITERATIONS] 发送测试消息..."

    # 发送消息到容器 (这里简化为执行 agent.py 的 stdin)
    # 实际需要通过 docker exec 传入
    echo "$TEST_MESSAGE" | docker exec -i $CONTAINER_NAME python -m src.agent > /dev/null 2>&1 || true

    # 每 10 次记录一次内存
    if (( i % 10 == 0 )); then
        CURRENT_MEM=$(docker stats --no-stream --format "{{.MemUsage}}" $CONTAINER_NAME | awk '{print $1}')
        echo "  当前内存: $CURRENT_MEM"
    fi

    sleep $DELAY
done

# 最终内存
FINAL_MEM=$(docker stats --no-stream --format "{{.MemUsage}}" $CONTAINER_NAME | awk '{print $1}')
echo ""
echo "=== 测试完成 ==="
echo "最终内存: $FINAL_MEM"
echo "请检查内存增长趋势，确认是否发生泄漏。"
#!/usr/bin/env python3
"""
自动化对话测试脚本
用于验证 Agent 基本功能和记忆持久化
"""

import asyncio
import subprocess
import time
import sys
from pathlib import Path

# 测试用例
TEST_CASES = [
    {
        "input": "你好",
        "expected_contains": ["你好", "帮助"],
        "description": "基础问候"
    },
    {
        "input": "现在几点了?",
        "expected_contains": ["20", "21", "22", "23", "00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19"],
        "description": "时间工具调用"
    },
    {
        "input": "搜索 Python asyncio",
        "expected_contains": ["Search", "搜索", "结果"],
        "description": "搜索工具调用"
    },
    {
        "input": "记住我的名字是张三",
        "expected_contains": ["记住", "张三"],
        "description": "记忆写入"
    },
    {
        "input": "我叫什么名字?",
        "expected_contains": ["张三"],
        "description": "记忆读取验证"
    }
]

async def run_test_async(agent_process, test_case):
    """向 agent 发送消息并检查响应"""
    input_text = test_case["input"]
    print(f"\n🧪 测试: {test_case['description']}")
    print(f"   输入: {input_text}")

    # 发送到 agent stdin
    agent_process.stdin.write(input_text + "\n")
    await agent_process.stdin.drain()

    # 读取响应 (简单实现，实际需要更严谨的协议)
    await asyncio.sleep(2)  # 等待响应

    # 这里需要根据实际情况解析输出
    print(f"   ⏳ 请手动检查响应是否符合预期")
    print(f"   应包含: {test_case['expected_contains']}")

async def main():
    print("🧪 RockClaw Phase 1 自动化测试")
    print("此脚本需要 agent 已经在受限容器中运行")
    print("")

    # 检查 Docker 容器
    result = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    if "rockclaw-poc" not in result.stdout:
        print("❌ 容器未运行！先执行: docker-compose up")
        sys.exit(1)

    # 连接容器 stdin 比较复杂，这里简化为指导用户手动测试
    print("✅ 检测到容器运行中")
    print("")
    print("📋 请手动执行以下测试用例:")
    for i, tc in enumerate(TEST_CASES, 1):
        print(f"{i}. {tc['description']}")
        print(f"   输入: {tc['input']}")
        print(f"   预期响应包含: {', '.join(tc['expected_contains'])}")
        print("")

    print("完成测试后，请检查:")
    print("  - 是否有工具调用输出")
    print("  - 记忆是否持久化 (data/memory 目录)")
    print("  - 内存是否持续增长 (docker stats)")
    print("")
    print("或者运行压力测试: tests/stress_test.sh")

if __name__ == "__main__":
    asyncio.run(main())
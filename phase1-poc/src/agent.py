"""
RockClaw POC - 核心 Agent 架构
最小化实现 OpenClaw 核心逻辑：Agent Loop + Tool Use + Memory
"""

import os
import json
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 内存目录
MEMORY_DIR = Path(os.getenv("MEMORY_DIR", "./data/memory"))
MEMORY_DIR.mkdir(parents=True, exist_ok=True)


class MemoryManager:
    """Manage OpenClaw-compatible file-based memory"""

    def __init__(self, memory_dir: Path):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    def read_file(self, filename: str) -> str:
        """Read a memory file, return empty string if not exists"""
        path = self.memory_dir / filename
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def write_file(self, filename: str, content: str):
        """Write to a memory file"""
        path = self.memory_dir / filename
        path.write_text(content, encoding="utf-8")

    def append_daily_note(self, text: str):
        """Append to today's daily note"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"{today}.md"
        existing = self.read_file(filename)
        timestamp = datetime.now().strftime("%H:%M")
        new_entry = f"\n## {timestamp}\n\n{text}\n"
        self.write_file(filename, existing + new_entry)

    def get_context(self) -> Dict[str, str]:
        """Get all memory files for context"""
        return {
            "SOUL": self.read_file("SOUL.md"),
            "USER": self.read_file("USER.md"),
            "MEMORY": self.read_file("MEMORY.md"),
        }


class ToolRegistry:
    """Registry of available tools (Anthropic Tool Use format)"""

    def __init__(self):
        self.tools = [
            {
                "name": "web_search",
                "description": "Search the web for current information",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "get_current_time",
                "description": "Get current date and time",
                "input_schema": {
                    "type": "object",
                    "properties": {},
                }
            },
            {
                "name": "memory_write",
                "description": "Write important information to long-term memory",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "Content to remember"}
                    },
                    "required": ["content"]
                }
            }
        ]

    def get_tools(self) -> List[Dict]:
        return self.tools

    async def execute(self, name: str, arguments: Dict[str, Any]) -> str:
        """Execute a tool by name"""
        if name == "web_search":
            return await self._web_search(arguments["query"])
        elif name == "get_current_time":
            return datetime.now().isoformat()
        elif name == "memory_write":
            # 实际写入在 agent 中处理，这里只返回确认
            return f"Remembered: {arguments['content']}"
        else:
            return f"Error: Unknown tool '{name}'"

    async def _web_search(self, query: str) -> str:
        """Placeholder: actual search via Brave API"""
        # TODO: Implement Brave Search API call
        return f"[Search results for: {query}] (Brave API not configured)"


class Agent:
    """Core Agent Loop (ReAct pattern with Anthropic Tool Use)"""

    def __init__(self, memory: MemoryManager, tools: ToolRegistry, api_key: str, model: str = "claude-sonnet-4-5"):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model
        self.memory = memory
        self.tools = tools
        self.max_iterations = 10

    async def chat(self, user_message: str) -> str:
        """Main chat loop: user message → (tool use loop) → final response"""
        # 构建上下文
        context = self.memory.get_context()
        system_prompt = f"""You are an AI assistant with tool use capabilities.

SOUL (your personality):
{context.get('SOUL', 'You are a helpful assistant.')}

USER (who you're talking to):
{context.get('USER', 'A user.')}

Important long-term memories:
{context.get('MEMORY', 'No long-term memories yet.')}

Use tools when needed. Think step by step. Respond in the same language as the user.
"""

        messages = [
            {"role": "user", "content": user_message}
        ]

        for iteration in range(self.max_iterations):
            response = await self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=messages,
                tools=self.tools.get_tools(),
                max_tokens=4000
            )

            # 添加 Claude 响应到消息历史
            messages.append({
                "role": "assistant",
                "content": response.content
            })

            # 检查是否结束
            stop_reason = response.stop_reason
            if stop_reason == "end_turn":
                # 提取最终文本
                final_text = ""
                for block in response.content:
                    if block.type == "text":
                        final_text += block.text
                # 持久化对话到每日笔记
                self.memory.append_daily_note(f"**User**: {user_message}\n\n**Assistant**: {final_text}")
                return final_text

            # 处理 tool_use
            tool_use_blocks = [b for b in response.content if b.type == "tool_use"]
            if tool_use_blocks:
                for block in tool_use_blocks:
                    tool_name = block.name
                    tool_input = block.input
                    print(f"[Tool] {tool_name}({tool_input})")

                    result = await self.tools.execute(tool_name, tool_input)

                    # 添加工具结果到消息历史
                    messages.append({
                        "role": "user",
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result
                            }
                        ]
                    })
                continue  # 继续下一轮迭代

            # 没有工具调用但也没有结束？保守返回
            return "Unexpected response format."

        return "Max iterations reached."


async def main():
    """Entry point for Phase 1 POC"""
    # 配置
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set")
        return

    memory = MemoryManager(MEMORY_DIR)
    tools = ToolRegistry()
    agent = Agent(memory, tools, api_key)

    print("RockClaw POC Agent Started")
    print("Type 'quit' to exit\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if user_input.lower() in ["quit", "exit"]:
                break

            if not user_input:
                continue

            print("Agent: ", end="", flush=True)
            response = await agent.chat(user_input)
            print(response)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n[Error] {e}")


if __name__ == "__main__":
    asyncio.run(main())
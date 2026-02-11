# RockClaw Phase 1 POC

**目标**: 在 Mac 上模拟 RK3576 受限环境，验证 OpenClaw 核心架构可行性

**硬件参考**: Radxa Rock 4D RK3576 8GB (8核, 6 TOPS NPU)

---

## 🚀 快速开始

### 1. 配置环境

```bash
cp .env.example .env
# 编辑 .env，填入:
# - ANTHROPIC_API_KEY
# - TELEGRAM_BOT_TOKEN (可选，当前用命令行交互)
```

### 2. 构建并运行 (受限 Docker 容器)

```bash
# 构建镜像
docker-compose build

# 运行 POC (限制 1.5核 / 1GB RAM)
docker-compose up

# 或直接使用 docker run
docker run -it --rm \
  --cpus="1.5" \
  --memory="1g" \
  --memory-swap="0" \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/.env:/app/.env \
  rockclaw-poc:latest
```

### 3. 交互测试

进入容器后，你会看到:

```
RockClaw POC Agent Started
Type 'quit' to exit

You: 你好，请介绍一下你自己。
Agent: 你好！我是 RockClaw，一个运行在资源受限环境的 AI 助理...
```

---

## 📊 性能基准测试

### 手动测量

```bash
# 启动时间
time docker-compose up

# 内存峰值 (Mac)
# 在 Docker Desktop 中查看容器的内存使用

# 连续对话测试
# 发送 10 条消息，观察内存增长
```

### 自动化压力测试

```bash
# 运行压力测试脚本 (需要先启动容器)
bash tests/stress_test.sh
```

---

## 📁 项目结构

```
phase1-poc/
├── src/
│   └── agent.py          # 核心 Agent Loop + Tool Use + Memory
├── data/
│   └── memory/           # 持久化记忆 (运行后生成)
│       ├── SOUL.md
│       ├── USER.md
│       ├── MEMORY.md
│       └── 2026-02-11.md
├── tests/
│   └── stress_test.sh   # 自动化压力测试
├── docs/
│   └── benchmark.md     # 性能报告模板
├── .env.example         # 环境变量模板
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🧪 测试场景

### 场景 1: 基础对话
```
You: 你是谁？
Agent: 我是 RockClaw...
```

### 场景 2: 工具调用
```
You: 现在几点了？
Agent: [调用 get_current_time] → 返回当前时间

You: 搜索 Python asyncio 教程
Agent: [调用 web_search] → 返回搜索结果
```

### 场景 3: 记忆持久化
```
You: 我的名字是张三。
Agent: 你好，张三！

# 重启容器后
You: 我叫什么名字？
Agent: 你是张三 (从 MEMORY.md 读取)
```

---

## 📈 性能目标 (Mac 模拟 RK3576 限制)

| 指标 | 目标 | 实测 |
|------|------|------|
| 启动时间 | < 30s | `time docker-compose up` |
| 内存占用 (空闲) | < 300MB | Docker Desktop 监控 |
| 内存占用 (对话中) | < 800MB | 连续 10 轮后测量 |
| 单次请求延迟 | < 3s | 秒表计时 |
| 24h 内存泄漏 | < 50MB | 长时间监控 |

---

## 🔧 调试技巧

### 查看容器日志
```bash
docker-compose logs -f
```

### 进入容器调试
```bash
docker-compose exec rockclaw-poc bash
# 查看内存文件
cat /app/data/memory/MEMORY.md
```

### 重置数据
```bash
rm -rf data/
docker-compose restart
```

---

## 🎯 成功标准

- [ ] 在 1.5核/1GB 限制下正常运行
- [ ] 工具调用循环正确 (Tool Use)
- [ ] 记忆持久化 (重启后保留)
- [ ] 24 小时连续运行无崩溃
- [ ] 内存增长 < 50MB/24h

---

## 📚 参考资源

- OpenClaw 官方文档: https://docs.openclaw.ai
- Anthropic Tool Use: https://docs.anthropic.com/claude/docs/tool-use
- MimiClaw 参考: https://github.com/memovai/mimiclaw
- RK3576 模型生态: 见 `~/edge-ai-research/resources/RK3576-open-models-survey.md`

---

## 🚀 下一步

完成 Phase 1 POC 后，进入 Phase 2:
- Telegram Bot 集成
- 配置管理系统 (无需重编译)
- WebSocket gateway
- OTA 更新
- Systemd 服务化

---

**开发者**: OpenClaw Agent
**日期**: 2026-02-11
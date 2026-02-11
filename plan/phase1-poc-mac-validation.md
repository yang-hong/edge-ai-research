# Phase 1 POC: Mac 环境模拟验证计划

**目标**: 在 Mac 上模拟 RK3576 的资源限制（CPU、内存、网络），验证 OpenClaw 核心架构的可行性

**工具**: 本地 Mac + Gemini CLI 辅助开发 + Docker 限制资源

---

## 🎯 验证要点

### 1. 核心架构跑通
- [ ] Agent Loop (思考 → 调用工具 → 观察结果)
- [ ] Tool Use 协议 (Anthropic format)
- [ ] Memory 持久化 (SOUL.md, USER.md, MEMORY.md)
- [ ] Telegram Bot 集成
- [ ] Claude API 调用

### 2. 资源限制模拟
- [ ] CPU 限制: 1-2 核心 (模拟 A55 单核性能)
- [ ] 内存限制: 512MB - 2GB (模拟嵌入式环境)
- [ ] 网络限速: 1Mbps (模拟弱网)
- [ ] 磁盘 I/O 延迟: 增加 10-100ms (模拟 eMMC)

### 3. 生产环境考虑
- [ ] 启动时间 (< 30s)
- [ ] 内存占用峰值 (< 1GB)
- [ ] 稳定性 (24h 运行无泄漏)
- [ ] OTA 更新可行性
- [ ] 功耗估算 (基于 CPU 占用)

---

## 🛠️ Mac 验证环境搭建

### 方案 A: Docker 限制 (推荐)

```bash
# 1. 创建受限容器
docker run -it --rm \
  --cpus="1.5" \              # 限制 1.5 个 CPU 核心
  --memory="1g" \             # 限制 1GB RAM
  --memory-swap="0" \         # 禁用 swap (模拟嵌入式)
  --pids-limit=100 \          # 限制进程数
  -v $(pwd):/app \            # 挂载代码
  python:3.11-slim

# 2. 在容器内安装依赖
pip install openai anthropic
# 复制 OpenClaw 核心代码
# 运行测试
```

### 方案 B: 系统级限制 (macOS)

```bash
# 使用 `cpulimit` 限制 CPU (需要 brew install)
brew install cpulimit

# 限制进程 CPU 占用 50%
cpulimit -l 50 -- python -m openclaw

# 使用 `memory_pressure` 模拟内存压力
# （需要自定义脚本）
```

### 方案 C: 组合方案

- 主程序: Docker 限制资源
- 网络模拟: `tc` (需要 root) 或 `netem` Docker 网络
- 磁盘 I/O: 使用 `dd` 创建慢速存储卷挂载

---

## 📋 Phase 1 验证清单

### ✅ Day 1-2: 基础架构

1. **创建测试项目** `rockclaw-poc`
   ```bash
   mkdir rockclaw-poc && cd rockclaw-poc
   # 复制 OpenClaw 核心: agent.py, tools.py, memory.py
   # 最小化裁剪: 只保留必要功能
   ```

2. **实现最小 Agent Loop**
   ```python
   # Minimal agent loop (ReAct pattern)
   while True:
       user_msg = input()
       response = claude.chat(user_msg, tools=available_tools)
       # 处理工具调用循环
       # 保存到 memory/
   ```

3. **Telegram Bot 集成测试**
   - 使用 BotFather 创建测试 bot
   - 用 `python-telegram-bot` 库接收/发送消息
   - 验证长轮询 (webhook 需要公网 IP)

4. **本地 Memory 验证**
   - 确认重启后记忆不丢失
   - 检查文件格式兼容性 (SOUL.md, USER.md, MEMORY.md)
   - 每日日志轮转 (`memory/YYYY-MM-DD.md`)

---

### ✅ Day 3-4: 工具系统

5. **实现核心工具**
   ```python
   tools = [
       web_search(query: str) -> str,    # Brave API
       get_current_time() -> datetime,   # NTP/HTTP
       # 可选: GPIO 控制 (在 Mac 上 mock)
   ]
   ```

6. **Tool Use 协议验证**
   - Claude API `tool_choice` 参数
   - 解析 `tool_use` 块
   - 执行工具并返回结果
   - 循环直到 `stop_reason: "end_turn"`

7. **错误处理与重试**
   - API 限流重试 (exponential backoff)
   - 网络中断缓存
   - 磁盘满保护

---

### ✅ Day 5-7: 资源限制压力测试

8. **基准测试脚本**
   ```bash
   # 1. 启动时间测量
   time python -m rockclaw

   # 2. 内存峰值
   /usr/bin/time -l python -m rockclaw

   # 3. 连续运行 24h 监控
   # - 用 `top` 记录内存增长
   # - 用 `dmesg` 检查 OOM
   ```

9. **模拟弱网测试**
   ```bash
   # 用 tc (需要 sudo) 限制带宽
   sudo tc qdisc add dev lo root netem rate 1mbit
   # 测试 Claude API 超时情况
   ```

10. **极端场景**
    - 同时 5 个用户并发对话
    - 长上下文 (10K tokens)
    - 工具疯狂调用 (100 次/分钟)

---

### ✅ Day 8-10: 部署与 OTA

11. **Systemd 服务化**
    ```ini
    [Unit]
    Description=RockClaw AI Assistant
    After=network-online.target

    [Service]
    Type=simple
    User=rockclaw
    WorkingDirectory=/opt/rockclaw
    ExecStart=/usr/bin/python3 -m rockclaw
    Restart=on-failure
    RestartSec=10

    [Install]
    WantedBy=multi-user.target
    ```

12. **OTA 更新机制原型**
    - 用 GitHub Release + `git pull` 实现
    - 版本号管理 (`VERSION` 文件)
    - 回滚方案 (保留上一个版本)

13. **监控与日志**
    - journald 日志查看: `journalctl -u rockclaw -f`
    - 内存/CPU 监控: `systemd-cgtop`
    - 自定义状态端点 (可选)

---

## 📊 性能基准目标 (Mac 模拟 RK3576)

| 指标 | 目标 | 测试方法 |
|------|------|----------|
| 启动时间 | < 30s | `time systemctl start rockclaw` |
| 内存占用 (空闲) | < 300MB | `ps -o rss= -p <pid>` |
| 内存占用 (对话中) | < 800MB | 同上，连续对话 |
| 单次请求延迟 | < 2s (网络 + Claude) | 计时查询 |
| 24h 内存泄漏 | < 50MB 增长 | 长时间监控 |
| 磁盘写入 | < 10MB/天 | `iostat` 监控 |

**注意**: Mac 性能远强于 RK3576，这些指标是"软上限"，实际目标是在 1GB 内存限制下满足。

---

## 🧪 代码模板 (Gemini CLI 辅助)

**需求**: 用 Gemini CLI 帮助生成测试脚本、Dockerfile、systemd unit

```bash
# 生成 Dockerfile 模板
gemini prompt: "Write a Dockerfile for Python 3.11 minimal, with openclaw dependencies (anthropic, telegram, python-dotenv). Expose port 8080."

# 生成系统服务文件
gemini prompt: "Generate a systemd service file for a Python AI agent that starts on boot, restarts on failure, logs to journald."

# 生成资源限制测试脚本
gemini prompt: "Write a Python script that spawns 10 concurrent requests to an HTTP endpoint and measures memory usage over time."
```

---

## 🔧 调试技巧 (Mac)

1. **查看内存占用**
   ```bash
   # 实时
   top -o rss

   # 峰值记录
   /usr/bin/time -l python -m rockclaw 2>&1 | grep "maximum resident set size"
   ```

2. **模拟 OOM**
   ```bash
   # 限制内存到 512MB
   docker run --memory="512m" ...
   ```

3. **网络抓包**
   ```bash
   # 查看 Claude API 请求
   tcpdump -i any -w claude.pcap port 443
   ```

4. **文件系统监控**
   ```bash
   # 查看 memory/ 目录写入
   sudo fs_usage -f pathname | grep MEMORY.md
   ```

---

## 📤 交付物清单

- [ ] 最小化可运行 `rockclaw-poc` 代码库
- [ ] Docker 镜像 (`rockclaw-poc:latest`) 可复现环境
- [ ] 自动化测试脚本 (`tests/stress_test.sh`)
- [ ] 性能报告 (`docs/benchmark-mac.md`)
- [ ] 部署脚本 (`deploy.sh` + systemd unit)
- [ ] OTA 原型 (GitHub Actions workflow)
- [ ] Phase 2 设计文档 (针对真实 RK3576)

---

## ⏱️ 时间估算 (单人)

- 环境搭建 + 原型: **2 天**
- 功能实现 + 调试: **5 天**
- 压力测试 + 优化: **3 天**
- 文档 + 代码评审: **2 天**

**总计: 12 个工作日 (约 2-3 周)**

---

## 🚀 立即开始

```bash
# 1. 创建项目仓库
cd ~/edge-ai-research
git checkout -b phase1-poc
mkdir -p phase1-poc/{src,tests,docs}

# 2. 用 Gemini CLI 生成初始代码
gemini prompt: "Create minimal OpenClaw agent loop in Python with tool support and memory persistence."

# 3. 开始迭代
cd phase1-poc
python -m src.agent  # 运行测试
```

---

**下一步**: 我可以直接用你的 Mac 上的 Gemini CLI 来生成初始代码框架，或者在你的电脑上直接执行这些步骤。要我马上开始吗？

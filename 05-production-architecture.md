# RK3576 边缘 AI 生产架构

## 1. 高层架构 (ASCII)

```mermaid
graph TD
    User[客户端 / 用户] -->|HTTP/REST| Gateway[API 网关 (FastAPI)]
    Gateway -->|健康检查| Monitor[系统监控]
    Gateway -->|路由逻辑| Router{任务路由器}
    
    subgraph "Rock 4D (边缘)"
        Router -->|简单/快速| LocalLLM[RKLLM 运行时 (NPU)]
        Router -->|视觉| YOLO[RKNN 运行时 (NPU)]
        LocalLLM -->|上下文| VectorDB[(SQLite + Faiss)]
    end
    
    subgraph "云端回退 (可选)"
        Router -->|复杂/慢速| CloudLLM[OpenAI / DeepSeek API]
    end
```

## 2. 组件设计

### API 网关 (FastAPI)
- **角色**: 所有 AI 请求的入口点。
- **协议**: 兼容 OpenAI 的 API (`/v1/chat/completions`)。
- **中间件**: 速率限制、认证、日志。
- **队列**: 请求队列以防止 NPU 过载（通常最大并发 = 1）。

### NPU 资源管理器
- **约束**: NPU 无法处理无限并发请求。
- **策略**: 
  - **单例模式**: 如果显存 < 8GB 且模型 > 4GB，一次只能在显存中加载一个模型。
  - **上下文切换**: 需要时卸载 LLM 加载 CV 模型（昂贵，耗时 ~2-5s）。
  - **理想**: 保持一个小型高效 LLM（例如 Qwen2.5-1.5B-W4A16）常驻。

### 本地 RAG
- **存储**: SQLite 用于元数据，Faiss 用于向量搜索。
- **嵌入**: 使用在 CPU 或 NPU 上运行的小型 BERT 模型（例如 `m3e-small`）。
- **流程**: 用户查询 -> 嵌入 -> 搜索向量库 -> 构建提示词 -> RKLLM 推理。

## 3. 代码脚手架

### `main.py` (FastAPI 骨架)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI(title="Edge AI Gateway")

class ChatRequest(BaseModel):
    model: str
    messages: list
    stream: bool = False

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatRequest):
    # 1. 检查 NPU 可用性
    if is_npu_busy():
        raise HTTPException(status_code=503, detail="NPU Busy")
    
    # 2. 获取锁
    try:
        # 3. 推理
        response = run_rkllm_inference(req.messages)
        return {"choices": [{"message": {"content": response}}]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "npu_temp": get_npu_temp()}

def is_npu_busy():
    # 实现信号量或锁检查
    return False

def get_npu_temp():
    # 读取 /sys/class/thermal/thermal_zoneX/temp
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return float(f.read()) / 1000.0
    except:
        return 0.0
```

### Systemd 服务 (`edge-ai.service`)

```ini
[Unit]
Description=Edge AI API Gateway
After=network.target

[Service]
User=rock
WorkingDirectory=/home/rock/edge-ai
ExecStart=/home/rock/edge-ai/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## 4. 资源管理策略

| 资源 | 约束 | 策略 |
| :--- | :--- | :--- |
| **VRAM (8GB)** | 与 CPU/GPU 共享 | 使用 **W4A16** 量化。限制最大上下文长度（例如 2048 或 4096）。 |
| **NPU 核心 (2)** | 共享 | 尽可能并行，但单个 LLM 请求通常占用全部以保证速度。 |
| **散热** | 被动散热限制性能 | 持续 LLM 推理**必须**使用主动散热（风扇）。 |
| **存储** | eMMC/SD 较慢 | 如果可能，使用 PCIe NVMe SSD 以快速加载模型。 |

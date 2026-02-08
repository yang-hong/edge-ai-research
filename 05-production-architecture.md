# RK3576 Edge AI Production Architecture

## 1. High-Level Architecture (ASCII)

```mermaid
graph TD
    User[Client / User] -->|HTTP/REST| Gateway[API Gateway (FastAPI)]
    Gateway -->|Health Check| Monitor[System Monitor]
    Gateway -->|Routing Logic| Router{Task Router}
    
    subgraph "Rock 4D (Edge)"
        Router -->|Simple/Fast| LocalLLM[RKLLM Runtime (NPU)]
        Router -->|Vision| YOLO[RKNN Runtime (NPU)]
        LocalLLM -->|Context| VectorDB[(SQLite + Faiss)]
    end
    
    subgraph "Cloud Fallback (Optional)"
        Router -->|Complex/Slow| CloudLLM[OpenAI / DeepSeek API]
    end
```

## 2. Component Design

### API Gateway (FastAPI)
- **Role**: Entry point for all AI requests.
- **Protocol**: OpenAI-compatible API (`/v1/chat/completions`).
- **Middleware**: Rate limiting, auth, logging.
- **Queue**: Request queue to prevent NPU overload (max concurrency = 1 usually).

### NPU Resource Manager
- **Constraint**: The NPU cannot handle unlimited concurrent requests.
- **Strategy**: 
  - **Singleton Pattern**: Only one model loaded in VRAM at a time if VRAM < 8GB and models > 4GB.
  - **Context Switching**: Unload LLM to load CV model if needed (expensive, takes ~2-5s).
  - **Ideal**: Keep one small efficient LLM (e.g., Qwen2.5-1.5B-W4A16) permanently loaded.

### Local RAG
- **Storage**: SQLite for metadata, Faiss for vector search.
- **Embeddings**: Use a small BERT model running on CPU or NPU (e.g., `m3e-small`).
- **Flow**: User Query -> Embed -> Search VectorDB -> Construct Prompt -> RKLLM Inference.

## 3. Code Scaffolding

### `main.py` (FastAPI Skeleton)

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
    # 1. Check NPU availability
    if is_npu_busy():
        raise HTTPException(status_code=503, detail="NPU Busy")
    
    # 2. Acquire Lock
    try:
        # 3. Inference
        response = run_rkllm_inference(req.messages)
        return {"choices": [{"message": {"content": response}}]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "npu_temp": get_npu_temp()}

def is_npu_busy():
    # Implement semaphore or lock check
    return False

def get_npu_temp():
    # Read from /sys/class/thermal/thermal_zoneX/temp
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return float(f.read()) / 1000.0
    except:
        return 0.0
```

### Systemd Service (`edge-ai.service`)

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

## 4. Resource Management Strategy

| Resource | Constraint | Strategy |
| :--- | :--- | :--- |
| **VRAM (8GB)** | Shared with CPU/GPU | Use **W4A16** quantization. Limit max context length (e.g., 2048 or 4096). |
| **NPU Cores (2)** | Shared | Parallelize if possible, but single LLM request usually consumes both for speed. |
| **Thermal** | Passive cooling limits perf | Active cooling (Fan) is **mandatory** for sustained LLM inference. |
| **Storage** | eMMC/SD slow | Use NVMe SSD via PCIe if possible for fast model loading. |

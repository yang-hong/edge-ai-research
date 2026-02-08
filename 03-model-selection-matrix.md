# RK3576 Model Selection Matrix (Based on Research)

*Note: Local benchmarks skipped due to environment issues. Recommendations based on RK3576 specs (6 TOPS, 8GB RAM) and community data.*

## 1. Top Recommendation: General Purpose Chat / Assistant
- **Model**: **Qwen2.5-1.5B-Instruct** (Quantized W4A16 or W8A8)
- **Why**: Best balance of speed, quality, and instruction following for small parameter count.
- **Est. Speed**: ~15-20 tok/s.
- **RAM**: ~1.5GB (leaves plenty for OS/apps).

## 2. Best for Reasoning / Code
- **Model**: **DeepSeek-R1-Distill-Qwen-1.5B**
- **Why**: Distilled reasoning capabilities in a small package.
- **Est. Speed**: ~12-18 tok/s.
- **Caveat**: Newer model, ensure RKLLM v1.2.3+ is used.

## 3. Best for English / Creative Writing
- **Model**: **Phi-3-Mini-3.8B** (Quantized W4A16)
- **Why**: High quality text generation, trained on synthetic data.
- **Est. Speed**: ~5-8 tok/s (Slower due to size).
- **RAM**: ~3.5GB.

## 4. Best for Ultra-Low Latency / IoT Control
- **Model**: **TinyLlama-1.1B** or **Qwen2.5-0.5B**
- **Why**: Extremely fast, low memory footprint. Good for simple JSON extraction or classification.
- **Est. Speed**: 30+ tok/s.
- **RAM**: < 1GB.

## 5. Vision-Language (VLM) Options
- **Model**: **Qwen2-VL-2B** or **MiniCPM-V-2.6**
- **Why**: Only viable VLMs for this hardware class.
- **Status**: Supported in RKLLM. Requires C++ demo usually for best performance.

## 6. Deployment Strategy
| Use Case | Recommended Model | Quantization | Notes |
| :--- | :--- | :--- | :--- |
| **Personal Assistant** | Qwen2.5-1.5B | W4A16 / W8A8 | Fast, good chat. |
| **Coding Helper** | DeepSeek-R1-Distill | W4A16 | Good logic, fits in RAM. |
| **Home Automation** | Qwen2.5-0.5B | W8A8 | Instant response. |
| **Reading Long Text** | Phi-3-Mini | W4A16 | Better coherence (3.8B). |

# RK3576 Ecosystem Report

## 1. RKNN SDK Status

### Toolkits & Versions
- **RKNN-Toolkit2**: v2.3.2 (Latest)
  - Supports RK3576, RK3588, RK356x.
  - Python Support: 3.6 - 3.12.
  - [GitHub Repo](https://github.com/airockchip/rknn-toolkit2)
- **RKLLM-Toolkit**: v1.2.3 (Latest)
  - Specifically for LLMs on Rockchip NPUs.
  - Supports RK3576.
  - Python Support: 3.9 - 3.12.
  - [GitHub Repo](https://github.com/airockchip/rknn-llm)

### RK3576 Hardware Specifics
- **NPU**: 6 TOPS total (INT8).
- **Cores**: 2 NPU Cores (vs 3 cores in RK3588).
  - *Crucial for scripts*: Set `rknn_core_num=2` when initializing runtime.
- **CPU**: 4x Cortex-A72 + 4x Cortex-A53.
- **RAM**: 8GB LPDDR5 (System takes ~1-2GB, leaving ~6GB for models).
- **Supported Quantization**:
  - W8A8 (Weight 8-bit, Activation 8-bit) — Standard for efficiency.
  - W4A16 (Weight 4-bit, Activation 16-bit) — For larger LLMs to fit in RAM.
  - Recommend **W4A16** for 1.5B+ models on 8GB RAM to ensure headroom.

### Model Support
Official support via RKLLM:
- **Qwen2.5** (0.5B, 1.5B, 3B, 7B - 7B might be tight on 8GB)
- **DeepSeek-R1-Distill** (Support confirmed in v1.2.3)
- **Phi-3 Mini**
- **Gemma 2 / Gemma 3 / 3n**
- **TinyLlama**
- **MiniCPM**

## 2. Community Tools Assessment

| Project | Status for RK3576 | Notes |
| :--- | :--- | :--- |
| **RKLLM-Toolkit** | ✅ Official & Active | Best path. v1.2.3 supports latest models like DeepSeek-R1. |
| **RKLLama** | ❓ Uncertain | Primarily RK3588 focused. Check `rknn-llm` repo for official C++ demo instead. |
| **EzRKNN-LLM** | ⚠️ Likely RK3588 | Most community repos default to RK3588. Verify before use. |
| **Radxa Docs** | ✅ Good | Official hardware documentation available. |

## 3. Performance Expectations

*Estimated based on NPU TOPS (6 vs 6 on RK3588, but fewer cores) and bandwidth.*

- **DeepSeek-R1-Distill-Qwen-1.5B (W4A16)**:
  - Est. Speed: **15 - 20 tokens/s**
  - RAM Usage: ~1.5 - 2.0 GB
  - Usability: Very fast for chat.

- **Phi-3 Mini (3.8B) (W4A16)**:
  - Est. Speed: **6 - 10 tokens/s**
  - RAM Usage: ~3.5 - 4.0 GB
  - Usability: Acceptable for reasoning tasks.

- **Qwen2.5-7B (W4A16)**:
  - Est. Speed: **2 - 4 tokens/s**
  - RAM Usage: ~5.5 - 6.0 GB (Risky on 8GB board with desktop GUI)
  - Usability: Slow, batch processing only.

- **YOLOv8n (Object Detection)**:
  - Latency: < 10ms
  - FPS: 60+ FPS
  - Very efficient on 6 TOPS NPU.

## 4. Competitor Comparison

| Feature | **Radxa Rock 4D (RK3576)** | **Raspberry Pi 5 + Hailo-8L** | **Jetson Orin Nano** |
| :--- | :--- | :--- | :--- |
| **Price** | ~$58 (Board) | ~$60 (Pi) + ~$70 (Hailo) = ~$130 | ~$250 |
| **NPU** | **6 TOPS** (Integrated) | 13 TOPS (Add-on) | 20-40 TOPS (Integrated) |
| **RAM** | 8GB LPDDR5 | 8GB LPDDR4X | 4GB / 8GB |
| **LLM Support**| **Good (RKLLM)** | Limited (Hailo focuses on CV) | Excellent (TensorRT-LLM) |
| **Verdict** | **Best Value for Edge LLM** | Better for CV, worse for LLM | Premium choice |

## 5. Ecosystem Links
- [RKLLM Model Zoo (Download Pre-converted Models)](https://console.box.lenovo.com/l/l0tXb8) (Pass: rkllm)
- [RKNN Toolkit2 Repo](https://github.com/airockchip/rknn-toolkit2)
- [Radxa Rock 4D Hardware Docs](https://docs.radxa.com/en/rock4/rock4d)

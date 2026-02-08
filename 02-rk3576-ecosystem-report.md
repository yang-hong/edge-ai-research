# RK3576 生态系统报告

## 1. RKNN SDK 状态

### 工具包与版本
- **RKNN-Toolkit2**: v2.3.2 (最新)
  - 支持 RK3576, RK3588, RK356x。
  - Python 支持: 3.6 - 3.12。
  - [GitHub 仓库](https://github.com/airockchip/rknn-toolkit2)
- **RKLLM-Toolkit**: v1.2.3 (最新)
  - 专为 Rockchip NPU 上的 LLM 设计。
  - 支持 RK3576。
  - Python 支持: 3.9 - 3.12。
  - [GitHub 仓库](https://github.com/airockchip/rknn-llm)

### RK3576 硬件特性
- **NPU**: 总算力 6 TOPS (INT8)。
- **核心**: 2 个 NPU 核心 (对比 RK3588 的 3 个核心)。
  - *脚本关键点*: 初始化运行时，设置 `rknn_core_num=2`。
- **CPU**: 4x Cortex-A72 + 4x Cortex-A53。
- **内存**: 8GB LPDDR5 (系统占用 ~1-2GB，剩余 ~6GB 给模型)。
- **支持的量化**:
  - W8A8 (权重 8-bit, 激活 8-bit) — 标准高效。
  - W4A16 (权重 4-bit, 激活 16-bit) — 适合较大的 LLM 以适应内存。
  - 推荐对 1.5B+ 模型在 8GB 内存上使用 **W4A16** 以确保余量。

### 模型支持
通过 RKLLM 官方支持：
- **Qwen2.5** (0.5B, 1.5B, 3B, 7B - 7B 在 8GB 上可能很紧凑)
- **DeepSeek-R1-Distill** (v1.2.3 确认支持)
- **Phi-3 Mini**
- **Gemma 2 / Gemma 3 / 3n**
- **TinyLlama**
- **MiniCPM**

## 2. 社区工具评估

| 项目 | RK3576 状态 | 备注 |
| :--- | :--- | :--- |
| **RKLLM-Toolkit** | ✅ 官方且活跃 | 最佳路径。v1.2.3 支持 DeepSeek-R1 等最新模型。 |
| **RKLLama** | ❓ 不确定 | 主要针对 RK3588。请检查 `rknn-llm` 仓库获取官方 C++ 演示。 |
| **EzRKNN-LLM** | ⚠️ 可能仅 RK3588 | 大多数社区仓库默认针对 RK3588。使用前请验证。 |
| **Radxa 文档** | ✅ 良好 | 提供官方硬件文档。 |

## 3. 性能预期

*基于 NPU TOPS（6 vs RK3588 的 6，但核心较少）和带宽估算。*

- **DeepSeek-R1-Distill-Qwen-1.5B (W4A16)**:
  - 预估速度: **15 - 20 tokens/s**
  - 内存占用: ~1.5 - 2.0 GB
  - 可用性: 聊天响应非常快。

- **Phi-3 Mini (3.8B) (W4A16)**:
  - 预估速度: **6 - 10 tokens/s**
  - 内存占用: ~3.5 - 4.0 GB
  - 可用性: 推理任务可接受。

- **Qwen2.5-7B (W4A16)**:
  - 预估速度: **2 - 4 tokens/s**
  - 内存占用: ~5.5 - 6.0 GB (在带有桌面 GUI 的 8GB 板上有风险)
  - 可用性: 慢，仅适合批处理。

- **YOLOv8n (目标检测)**:
  - 延迟: < 10ms
  - FPS: 60+ FPS
  - 在 6 TOPS NPU 上非常高效。

## 4. 竞品对比

| 特性 | **Radxa Rock 4D (RK3576)** | **Raspberry Pi 5 + Hailo-8L** | **Jetson Orin Nano** |
| :--- | :--- | :--- | :--- |
| **价格** | ~$58 (板卡) | ~$60 (Pi) + ~$70 (Hailo) = ~$130 | ~$250 |
| **NPU** | **6 TOPS** (集成) | 13 TOPS (外接) | 20-40 TOPS (集成) |
| **内存** | 8GB LPDDR5 | 8GB LPDDR4X | 4GB / 8GB |
| **LLM 支持**| **良好 (RKLLM)** | 有限 (Hailo 侧重于 CV) | 优秀 (TensorRT-LLM) |
| **结论** | **边缘 LLM 性价比之王** | 适合 CV，LLM 较差 | 高端选择 |

## 5. 生态系统链接
- [RKLLM 模型库 (下载预转换模型)](https://console.box.lenovo.com/l/l0tXb8) (密码: rkllm)
- [RKNN Toolkit2 仓库](https://github.com/airockchip/rknn-toolkit2)
- [Radxa Rock 4D 硬件文档](https://docs.radxa.com/en/rock4/rock4d)

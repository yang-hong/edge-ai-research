# 🦞 边缘 AI 研究 — 隔夜总结

## 1. 执行摘要
Radxa Rock 4D (RK3576, 8GB) 是一个**极具潜力**的边缘 AI 平台，在约 $60 美元的价格点上表现出色。虽然它的算力略低于 RK3588（同为 6 TOPS，但核心数/带宽较少），但其现代化的架构（Cortex-A72/A53）和 LPDDR5 内存使其非常适合运行量化 LLM（1.5B - 3B 范围）。

**状态**: 
- 研究完成: ✅
- 脚本生成: ✅
- 架构设计: ✅
- 本地基准测试: ⚠️ **跳过** (Ollama 构建受限于旧款 Intel Mac)。
- 建议: 基于已验证的 RK3576 规格和社区数据。

## 2. 三大意外发现
1. **NPU 核心数陷阱**: RK3576 只有 **2 个 NPU 核心**，而不像流行的 RK3588 有 3 个。如果不修改 `core_mask` 参数，许多复制粘贴的脚本将会失败。
2. **模型转换严格性**: 你**不能**在开发板本身上转换模型。你需要一台 x86 Linux 机器（虚拟机/Docker）来进行 rknn-toolkit2 转换步骤。
3. **DeepSeek 支持**: 最新的 RKLLM v1.2.3 官方支持 **DeepSeek-R1-Distill**，使该板成为可行的本地推理引擎。

## 3. 立即行动计划（第一天）
1. **刷入系统**: 从 Radxa 下载并安装 Debian 12 (Bookworm)。
2. **运行设置脚本**: 执行 `~/edge-ai-research/04-quickstart-scripts/setup-board.sh`。
3. **安装 NPU/LLM 运行时**: 执行 `~/edge-ai-research/04-quickstart-scripts/install-rknn.sh`。
4. **首次推理**: 下载 `DeepSeek-R1-Distill-Qwen-1.5B-W4A16.rkllm` 并运行 `run-first-llm.sh`。

## 4. 推荐首选模型
- **模型**: **Qwen2.5-1.5B-Instruct** (W4A16 量化)
- **理由**: 速度（~15-20 tok/s）、指令遵循能力和内存占用（~1.5GB）的最佳平衡。
- **备选**: **DeepSeek-R1-Distill-Qwen-1.5B** 用于推理任务。

## 5. 风险评估
| 风险 | 严重程度 | 缓解措施 |
| :--- | :--- | :--- |
| **发热 / 降频** | 高 | 持续 LLM 负载必须使用主动散热（风扇）。 |
| **模型转换** | 中 | 在 Mac/PC 上使用 Docker/虚拟机进行转换。不要尝试在板上转换。 |
| **软件成熟度** | 中 | RKLLM 发展迅速。请坚持使用最新版本 (v1.2.3+)。 |
| **Ollama 支持** | 低 | Ollama 目前尚未原生支持 NPU 加速（使用 CPU）。请使用 RKLLM 运行时以获得速度。 |

## 6. 下一步行动
- [ ] 查看 `02-rk3576-ecosystem-report.md` 了解完整的软件生态。
- [ ] 在 Mac 上设置 x86 Linux 虚拟机（或 Docker）以进行模型转换。
- [ ] 从 RKLLM 模型库（报告中有链接）下载推荐模型。
- [ ] 开发板到货后，执行 `04-quickstart-scripts/` 中生成的脚本。

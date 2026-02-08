# 🦞 Edge AI Research — Overnight Summary

## 1. Executive Summary
The Radxa Rock 4D (RK3576, 8GB) is a **highly capable** edge AI platform, punching above its weight class for its ~$60 price point. While slightly less powerful than the RK3588 (6 TOPS vs 6 TOPS but fewer cores/bandwidth), its modern architecture (Cortex-A72/A53) and LPDDR5 RAM make it excellent for running quantized LLMs (1.5B - 3B range).

**Status**: 
- Research Completed: ✅
- Scripts Generated: ✅
- Architecture Designed: ✅
- Local Benchmarks: ⚠️ **Skipped** (Ollama build stuck on legacy Intel Mac).
- Recommendations: Based on verified RK3576 specs and community data.

## 2. Top 3 Surprises
1. **NPU Core Count Trap**: RK3576 has **2 NPU cores**, not 3 like the popular RK3588. Many copy-paste scripts will fail without modification (`core_mask` parameter).
2. **Model Conversion Strictness**: You **cannot** convert models on the board itself. You need an x86 Linux machine (VM/Docker) for the rknn-toolkit2 conversion step.
3. **DeepSeek Support**: The latest RKLLM v1.2.3 officially supports **DeepSeek-R1-Distill**, making this board a viable local reasoning engine.

## 3. Immediate Action Plan (Day 1)
1. **Flash OS**: Install Debian 12 (Bookworm) from Radxa downloads.
2. **Run Setup Script**: execute `~/edge-ai-research/04-quickstart-scripts/setup-board.sh`.
3. **Install NPU/LLM Runtime**: execute `~/edge-ai-research/04-quickstart-scripts/install-rknn.sh`.
4. **First Inference**: Download `DeepSeek-R1-Distill-Qwen-1.5B-W4A16.rkllm` and run `run-first-llm.sh`.

## 4. Recommended First Model
- **Model**: **Qwen2.5-1.5B-Instruct** (W4A16 Quantized)
- **Why**: Best balance of speed (~15-20 tok/s), instruction following, and RAM usage (~1.5GB).
- **Runner Up**: **DeepSeek-R1-Distill-Qwen-1.5B** for reasoning tasks.

## 5. Risk Assessment
| Risk | Severity | Mitigation |
| :--- | :--- | :--- |
| **Heat / Throttling** | High | Active cooling (fan) is mandatory for sustained LLM loads. |
| **Model Conversion** | Medium | Use Docker/VM on Mac/PC for conversion. Don't try on-board. |
| **Software Maturity** | Medium | RKLLM is evolving fast. Stick to latest releases (v1.2.3+). |
| **Ollama Support** | Low | Ollama doesn't natively support NPU acceleration yet (uses CPU). Use RKLLM runtime for speed. |

## 6. Next Steps for You
- [ ] Review `02-rk3576-ecosystem-report.md` for full software landscape.
- [ ] Setup x86 Linux VM (or Docker) on your Mac for model conversion.
- [ ] Download recommended models from RKLLM Model Zoo (link in report).
- [ ] Execute the generated scripts in `04-quickstart-scripts/` when board arrives.

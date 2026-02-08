# RK3576 学习资源

## 1. 官方文档
- **Radxa Rock 4D Wiki**: [https://docs.radxa.com/en/rock4/rock4d](https://docs.radxa.com/en/rock4/rock4d)
  - 硬件规格、引脚图、系统安装。
- **Rockchip RKNN Toolkit2**: [https://github.com/airockchip/rknn-toolkit2](https://github.com/airockchip/rknn-toolkit2)
  - 官方 NPU 推理工具包仓库 (视觉)。
- **Rockchip RKLLM Toolkit**: [https://github.com/airockchip/rknn-llm](https://github.com/airockchip/rknn-llm)
  - 官方 LLM 部署仓库。
- **RKNN Model Zoo**: [https://github.com/airockchip/rknn_model_zoo](https://github.com/airockchip/rknn_model_zoo)
  - 预转换的视觉模型和示例。

## 2. 社区与教程
- **CNX Software - Rockchip RK3576 深度解析**: 在 [CNX Software](https://www.cnx-software.com/) 上搜索。
- **Firefly / Banana Pi Wiki**: 通常包含适用于 Radxa 的优质 RK3576 指南。
- **YouTube 频道**:
  - **ExplainingComputers**: 通用 SBC 评论/教程。
  - **Jeff Geerling**: 高质量的 Pi/SBC 内容 (寻找 Rockchip 相关视频)。
  - **Leepoly**: 专门的边缘 AI 内容。

## 3. 高级主题 (深入研究)
- **模型量化理论**: 
  - [Hugging Face 量化指南](https://huggingface.co/docs/transformers/main_classes/quantization)
  - 了解 INT8 vs FP16 的权衡。
- **NPU 架构**:
  - Rockchip NPU 用户指南 (SDK 文档中有 PDF)。
  - 理解 "权重共享"、"通道剪枝" 和 "稀疏性"。
- **RK3576 Linux 内核**:
  - [Rockchip Linux Kernel 仓库](https://github.com/rockchip-linux/kernel)
  - 寻找与 NPU 内存分配相关的设备树覆盖 (`.dts`)。

## 4. 故障排除
- **Radxa 论坛**: [https://forum.radxa.com/](https://forum.radxa.com/)
- **Armbian 论坛**: [https://forum.armbian.com/](https://forum.armbian.com/) (极好的内核/系统问题资源)。
- **GitHub Issues**: 遇到问题请先检查 `rknn-toolkit2` 和 `rknn-llm` 的 issue 跟踪器！

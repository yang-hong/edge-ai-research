# RK3576 Learning Resources

## 1. Official Documentation
- **Radxa Rock 4D Wiki**: [https://docs.radxa.com/en/rock4/rock4d](https://docs.radxa.com/en/rock4/rock4d)
  - Hardware specs, pinout, OS installation.
- **Rockchip RKNN Toolkit2**: [https://github.com/airockchip/rknn-toolkit2](https://github.com/airockchip/rknn-toolkit2)
  - Official repo for NPU inference toolkit (Vision).
- **Rockchip RKLLM Toolkit**: [https://github.com/airockchip/rknn-llm](https://github.com/airockchip/rknn-llm)
  - Official repo for LLM deployment.
- **RKNN Model Zoo**: [https://github.com/airockchip/rknn_model_zoo](https://github.com/airockchip/rknn_model_zoo)
  - Pre-converted vision models and examples.

## 2. Community & Tutorials
- **CNX Software - Rockchip RK3576 Deep Dive**: Search on [CNX Software](https://www.cnx-software.com/).
- **Firefly / Banana Pi Wiki**: Often contain good RK3576 guides that apply to Radxa too.
- **YouTube Channels**:
  - **ExplainingComputers**: General SBC reviews/tutorials.
  - **Jeff Geerling**: High-quality Pi/SBC content (look for Rockchip videos).
  - **Leepoly**: Specific AI on edge content.

## 3. Advanced Topics (Deep Dive)
- **Model Quantization Theory**: 
  - [Hugging Face Quantization Guide](https://huggingface.co/docs/transformers/main_classes/quantization)
  - Learn about INT8 vs FP16 trade-offs.
- **NPU Architecture**:
  - Rockchip NPU User Guide (PDF available in SDK docs).
  - Understand "weight sharing", "channel pruning", and "sparsity".
- **Linux Kernel for RK3576**:
  - [Rockchip Linux Kernel Repo](https://github.com/rockchip-linux/kernel)
  - Look for Device Tree overlays (`.dts`) related to NPU memory allocation.

## 4. Troubleshooting
- **Radxa Forum**: [https://forum.radxa.com/](https://forum.radxa.com/)
- **Armbian Forum**: [https://forum.armbian.com/](https://forum.armbian.com/) (Great for kernel/OS issues).
- **GitHub Issues**: Check the `rknn-toolkit2` and `rknn-llm` issue trackers first!

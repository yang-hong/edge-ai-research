# RK3576 学习资源 (深度版)

## 1. 核心工具链：RKLLM-Toolkit (必读)

RKLLM 是 Rockchip 专为 LLM (大语言模型) 设计的 NPU 推理工具链。**它是你在 RK3576 上跑通 LLM 的唯一官方路径。**

### 1.1 核心工作流 (Workflow)
要在 RK3576 上运行模型，你必须经历 "PC端转换" -> "板端推理" 两个步骤：

1.  **模型导出 (PC/x86 Linux)**:
    -   下载原始模型 (HuggingFace, e.g., Qwen2.5-1.5B)。
    -   使用 `rkllm-toolkit` (Python) 将模型量化并导出为 `.rkllm` 格式。
    -   **关键配置**:
        -   `target_platform="rk3576"` (必须指定，否则默认 RK3588 会导致 NPU 核心数不匹配)。
        -   `quantized_dtype="w4a16"` (推荐 W4A16 以平衡 8GB 内存)。
        -   `optimization_level=1` (开启图优化)。

2.  **板端部署 (Rock 4D)**:
    -   将 `.rkllm` 文件拷贝到开发板。
    -   使用 C++ API (`librkllmrt.so`) 或 Python API (`rkllm-runtime`) 加载模型。
    -   **注意**: Python API 适合快速验证，但 C++ API 性能更稳，占用内存更少。

### 1.2 常用命令速查 (Cheat Sheet)
```python
# PC端转换脚本片段 (export_rkllm.py)
from rkllm.api import RKLLM

model = RKLLM()
ret = model.load_huggingface(model_path="./Qwen2.5-1.5B-Instruct")
# 针对 RK3576 的关键参数
ret = model.build(
    do_quantization=True,
    optimization_level=1,
    quantized_dtype='w4a16',
    target_platform='rk3576'  # 核心！
)
ret = model.export_rkllm("./qwen-1.5b.rkllm")
```

### 1.3 资源链接
-   **GitHub**: [airockchip/rknn-llm](https://github.com/airockchip/rknn-llm) (包含 Toolkit 和 Runtime)
-   **文档路径**: 仓库内的 `doc/` 目录是金矿，尤其是 `RKLLM_User_Guide_EN.pdf`。

---

## 2. 社区项目：RKLLama (进阶)

**RKLLama** 是一个基于 `librkllmrt` 的社区/非官方封装，旨在简化 Llama 类模型的部署。

### 2.1 它是什么？
-   它本质上是对 Rockchip 官方 C++ 运行时的一个**高级封装**。
-   提供了更像 `llama.cpp` 的体验，通常包含现成的 HTTP Server 示例。
-   **注意**: 它的更新速度通常落后于官方 SDK。如果官方支持了新模型 (如 DeepSeek)，RKLLama 可能需要几天到几周才能跟进。

### 2.2 适用场景
-   如果你想快速搭建一个 **OpenAI 兼容的 API Server**，RKLLama 的示例代码通常比官方的更完整。
-   如果你主要是跑 Llama 3 / Qwen 等标准架构，它很好用。
-   **不适用**: 如果你要跑刚出的新架构 (如 DeepSeek-R1-Distill)，建议直接用官方 RKLLM Runtime。

---

## 3. 硬件文档：Radxa Rock 4D (基础)

Radxa 的文档主要解决"怎么让板子跑起来"的问题，而不是"怎么跑 AI"。

### 3.1 关键页面
-   **入门指南**: [Rock 4D Getting Started](https://docs.radxa.com/en/rock4/rock4d/getting-started)
    -   *必看*: 镜像下载 (推荐 Debian CLI 版本，不要带桌面环境以节省 1GB 内存)。
    -   *必看*: 供电要求 (PD 20W+ 是必须的，NPU 全速运行时峰值功耗较高)。
-   **硬件接口**: [GPIO Pinout](https://docs.radxa.com/en/rock4/rock4d/hardware/gpio)
    -   如果你需要接风扇 (PWM 控制)，看这里。

### 3.2 避坑指南 (Radxa 特有)
-   **NPU 驱动**: Radxa 的官方镜像通常已经内置了 NPU 驱动 (`rknpu` 内核模块)。**不要**自己去编译内核安装驱动，除非你知道自己在做什么。
-   **Overlay**: 如果你要用 NVMe SSD，可能需要在 `/boot/uEnv.txt` 或 `armbianEnv.txt` 中开启 PCIe overlay。

---

## 4. 学习路线图 (2小时速成)

1.  **第 0-30 分钟 (环境准备)**:
    -   在 PC (Linux/Docker) 上拉取 `rknn-llm` 仓库。
    -   在 Rock 4D 上刷好系统，连接网络，安装 `htop` 监控。
2.  **第 30-60 分钟 (跑通 Hello World)**:
    -   不要自己转换！直接去 **RKNN Model Zoo** (HuggingFace/网盘) 下载一个现成的 `Qwen2.5-1.5B-w4a16.rkllm`。
    -   传到板子上，运行官方仓库里的 `example/python/main.py`。
3.  **第 60-90 分钟 (进阶交互)**:
    -   修改 Python 脚本，实现连续对话 (Chat Loop)。
    -   观察 `top` 中的内存占用，感受 W4A16 和 W8A8 的区别。
4.  **第 90-120 分钟 (应用集成)**:
    -   尝试写一个简单的 FastAPI 接口包裹这个 Python 脚本。
    -   恭喜，你已经有了一个边缘 AI API Server。

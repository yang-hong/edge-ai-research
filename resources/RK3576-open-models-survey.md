# RK3576 端侧开源模型生态调研报告

**调研日期**: 2026-02-11
**目标芯片**: Rockchip RK3576 (NPU 端侧推理)
**调研范围**: GitHub + 官方模型动物园 + 中国开发者社区

---

## 📋 执行摘要

RK3576 作为 Rockchip 新一代中端端侧芯片，已获得**极其丰富**的开源模型支持。通过官方 `rknn_model_zoo` 和社区项目（如 `rkllama`），开发者可轻松部署**数十类模型**，涵盖：

- ✅ 大语言模型 (LLM)
- ✅ 目标检测 (YOLO 全系列 + 更多)
- ✅ 图像分割 / 姿态估计
- ✅ 语音识别 / 合成
- ✅ OCR / 人脸识别
- ✅ 多模态视觉语言模型

**性能亮点**：在 RK3576 单核 NPU 上，YOLOv5n 可达 **82+ FPS**，ResNet50 可达 **110+ FPS**，完全满足实时应用需求。

---

## 🏗️ 核心项目生态

### 1. Official: rknn_model_zoo (Rockchip 官方)

- **仓库**: https://github.com/airockchip/rknn_model_zoo
- **支持平台**: RK3562/66/68, **RK3576**, RK3588, RV1126B 等
- **SDK 版本**: RKNN-Toolkit2 2.3.2+
- **特点**: 提供预转换好的 `.rknn` 模型文件，开箱即用

### 2. Community: rkllama (NotPunchnox)

- **仓库**: https://github.com/NotPunchnox/rkllama
- **Stars**: 415 ⭐ (活跃更新)
- **定位**: Ollama 替代方案，专为 Rockchip NPU 优化
- **API**: 兼容 Ollama + OpenAI API
- **特点**: 支持 LLM + 多模态 + Tool Calling + 图像生成 + TTS/STT

### 3. Commercial: Seeed reComputer-RK-LLM

- **仓库**: https://github.com/Seeed-Projects/reComputer-RK-LLM
- **形式**: Docker 容器化部署
- **适合**: 快速原型验证

---

## 🤖 大语言模型 (LLM) 支持

| 模型 | 格式 | 来源 | 备注 |
|------|------|------|------|
| **Qwen2.5** 系列 | `.rkllm` | rkllama / HF | 阿里通义千问，推荐 3B/7B |
| **Qwen2VL / Qwen2.5VL** | `.rkllm` + `.rknn` | rkllama | 视觉语言模型，支持图像问答 |
| **Qwen3VL** (最新) | `.rkllm` + `.rknn` | rkllama | 多模态能力更强 |
| **MiniCPMV4 / 4.5** | `.rkllm` + `.rknn` | rkllama | 性价比高的多模态模型 |
| **Llama 3.2+** | `.rkllm` | rkllama | Meta 开源模型 |
| **TinyLlama** | `.rkllm` | rkllama | 1.1B 小模型，快速推理 |

**推荐场景**:
- **轻量对话/本地知识库**: Qwen2.5-3B
- **视觉问答**: Qwen2.5VL-2B 或 MiniCPMV4.5
- **成本敏感**: TinyLlama (1.1B)

---

## 🎯 目标检测 (Object Detection) - YOLO 全家桶

RKNN Model Zoo 提供了**全系列 YOLO** 的 INT8 优化版本，全部支持 RK3576：

| 模型系列 | 变体 | 输入尺寸 | 精度 (INT8) | 性能 (FPS) RK3576 单核 |
|---------|------|----------|-------------|-----------------------|
| **YOLOv5** | yolov5n | 640×640 | FP16/INT8 | **82.5** |
| | yolov5s | 640×640 | FP16/INT8 | 48.4 |
| | yolov5m | 640×640 | FP16/INT8 | 20.9 |
| | yolov5n_relu | 640×640 | FP16/INT8 | 66.1 |
| **YOLOv6** | yolov6n | 640×640 | FP16/INT8 | **106.4** |
| | yolov6s | 640×640 | FP16/INT8 | 36.4 |
| | yolov6m | 640×640 | FP16/INT8 | 17.8 |
| **YOLOv7** | yolov7-tiny | 640×640 | FP16/INT8 | **72.7** |
| | yolov7 | 640×640 | FP16/INT8 | 11.4 |
| **YOLOv8** | yolov8n | 640×640 | FP16/INT8 | **73.5** |
| | yolov8s | 640×640 | FP16/INT8 | 38.0 |
| | yolov8m | 640×640 | FP16/INT8 | 16.2 |
| **YOLOv8 OBB** | yolov8n-obb | 640×640 | INT8 | 74.0 |
| **YOLOv10** | yolov10n | 640×640 | FP16/INT8 | **61.2** |
| | yolov10s | 640×640 | FP16/INT8 | 33.8 |
| **YOLO11** (最新) | yolo11n | 640×640 | FP16/INT8 | **60.0** |
| | yolo11s | 640×640 | FP16/INT8 | 33.0 |
| | yolo11m | 640×640 | FP16/INT8 | 12.7 |
| **YOLOX** | yolox_s | 640×640 | FP16/INT8 | 37.1 |
| | yolox_m | 640×640 | FP16/INT8 | 16.0 |
| **PPYOLOE** | ppyoloe_s | 640×640 | FP16/INT8 | 32.5 |
| | ppyoloe_m | 640×640 | FP16/INT8 | 15.8 |
| **YOLO-World v2** | yolo_world_v2s | 640×640 | FP16/INT8 | 22.1 |

**💡 关键发现**:
- **最快速度**: YOLOv6n 达到 **106+ FPS**，适合超实时场景
- **平衡选择**: YOLOv8n (73 FPS) / YOLOv5n (82 FPS)
- **最新架构**: YOLO11 系列 (2024年底发布) 已支持
- **开放词汇**: YOLO-World v2s 支持文本引导检测

---

## 🔍 图像分割 (Segmentation)

| 模型 | 类型 | 输入尺寸 | 性能 (FPS) |
|------|------|----------|------------|
| **YOLOv5-seg** | yolov5n-seg | 640×640 | 69.3 |
| | yolov5s-seg | 640×640 | 36.8 |
| | yolov5m-seg | 640×640 | 16.4 |
| **YOLOv8-seg** | yolov8n-seg | 640×640 | **60.8** |
| | yolov8s-seg | 640×640 | 28.9 |
| | yolov8m-seg | 640×640 | 12.6 |
| **DeepLabV3+** | deeplab-v3-plus-mobilenet-v2 | 513×513 | 34.0 |
| **PPSeg** | pp_liteseg_cityscapes | 512×512 | 35.7 |
| **MobileSAM** | mobilesam_encoder_tiny + decoder | 448×448 | Enc: 10.0 / Dec: 116.4 |

---

## 🦴 人体姿态估计 (Pose)

| 模型 | 说明 | 性能 (FPS) |
|------|------|------------|
| **YOLOv8-Pose** | yolov8n-pose | 640×640 | **55.9** |

---

## 👤 人脸与关键点

| 模型 | 任务 | 性能 (FPS) |
|------|------|------------|
| **RetinaFace** | 人脸检测 (mobile320) | 320×320 | **227.2** |
| | 人脸检测 (resnet50) | 320×320 | 49.2 |

---

## 🚗 垂直领域模型

### OCR (文字识别)
- **PPOCRv4** (PaddlePaddle): 检测 + 识别，Chinese supported
- **LPRNet**: 车牌识别

### 图像分类
- **MobileNetV2**: 224×224, **450.7 FPS** (极快)
- **ResNet50**: 224×224, **110.1 FPS**

### 图像-文本匹配
- **CLIP**: ViT-B/32, 支持图像检索

---

## 🗣️ 语音模型

### 语音识别 (ASR/STT)

| 模型 | 类型 | 性能 | 备注 |
|------|------|------|------|
| **Whisper** | OpenAI | base (20s) RTF 0.215 | 多语言 |
| **Wav2Vec2** | Facebook | base (20s) RTF 0.133 | 英语 |
| **Zipformer** | NVIDIA | bilingual zh-en (streaming) RTF **0.065** | 最快，中英双语 |

**RTF** = Real-Time Factor, 越小越快 (<1 表示实时)

### 语音合成 (TTS)

| 模型 | 语言 | 性能 | 备注 |
|------|------|------|------|
| **MMS-TTS** | 英语 | RTF 0.069 | Meta 多语言 |
| **Piper** | 多语言 | 可自定义 | 需要转换 .onnx → .rknn |

---

## 🖼️ 图像生成

| 模型 | 分辨率 | 格式 | 备注 |
|------|--------|------|------|
| **LCM Stable Diffusion 1.5** | 512×512 | RKNN | 加速采样，~5步生成 |
| **LCM SSD 1B** | 1024×1024 | RKNN | 更小更快 |

需转换为 RKNN 格式，预转换模型可从 HuggingFace 获取。

---

## 🧩 多模态与视觉语言

| 模型 | 能力 | 架构 |
|------|------|------|
| **Qwen2VL / Qwen2.5VL** | 图像问答、多轮对话 | LLM + Vision Encoder (.rknn) |
| **MiniCPMV4 / 4.5** | 轻量级多模态 | LLM + Vision Encoder |
| **CLIP** | 图像-文本匹配 | ViT + Text Encoder |

---

## 📊 RK3576 性能基准 (NPU Single Core)

数据来源: rknn_model_zoo 官方 benchmark (最大 NPU 频率)

| 模型 | 输入 | FPS | Latency (ms) |
|------|------|-----|--------------|
| **MobileNetV2** | 1×3×224×224 | **450.7** | 2.2 |
| **ResNet50** | 1×3×224×224 | **110.1** | 9.1 |
| **YOLOv6n** | 1×3×640×640 | **106.4** | 9.4 |
| **yolov5n** | 1×3×640×640 | **82.5** | 12.1 |
| **yolov5n_relu** | 1×3×640×640 | **66.1** | 15.1 |
| **yolov8n** | 1×3×640×640 | **73.5** | 13.6 |
| **LPRNet** | 1×3×24×94 | **647.8** | 1.5 |
| **RetinaFace (mobile320)** | 1×3×320×320 | **470.5** | 2.1 |
| **PPOCR-Det** | 1×3×480×480 | **50.7** | 19.7 |
| **PPOCR-Rec** | 1×3×48×320 | **73.9** | 13.5 |
| **Zipformer** | 20s audio | RTF 0.065 | 实时快于1倍 |
| **Whisper** | 20s audio | RTF 0.215 | 实时 |

**结论**: RK3576 NPU 算力足以支撑大多数端侧 AI 场景，YOLO 系列模型轻松达到 60-100+ FPS 实时性能。

---

## 🇨🇳 中国开发者实践特点 (基于 GitHub 生态)

### 活跃项目趋势

1. **rkllama** (NotPunchnox): 社区最活跃的 Ollama 替代方案，持续更新，支持最新模型 (Qwen3VL, MiniCPMV4.5)
2. **RKLLM-Toolkit** (官方): 用于将 HuggingFace 模型转换为 `.rkllm` 格式
3. **YOLO 系列适配**: airockchip 官方维护 yolov5/v6/v7/v8/v10/yolo11 的 RKNN 转换

### 常见使用模式

- **快速原型**: 使用 `rkllama` + 预转换模型，一条命令启动 API 服务
- **生产部署**: 使用 `rknn-toolkit2` 自行转换和优化模型，集成到 C++/Python 应用
- **多模态**: Qwen2.5VL + MiniCPMV4 是热门选择
- **边缘摄像头**: YOLOv8n + PPOCR 组合用于智能监控

### Docker 部署

- `ghcr.io/notpunchnox/rkllama:main` 官方镜像
- `rknn-llm:v1.2.3` （之前项目中使用）
- 适合快速验证，生产建议构建精简镜像

---

## 🔧 快速入门建议

### 方案一：LLM 推理 (推荐 rkllama)

```bash
# 1. 安装
git clone https://github.com/NotPunchnox/rkllama
cd rkllama && pip install -e .

# 2. 创建模型目录
mkdir -p ~/models

# 3. 拉取预转换模型 (例如 Qwen2.5-3B)
rkllama_client pull c01zaut/Qwen2.5-3B-Instruct-RK3588-1.1.4

# 4. 启动服务
rkllama_server --models ~/models

# 5. 对话
rkllama_client run qwen2.5:3b
```

### 方案二：目标检测 (推荐 rknn_model_zoo)

```bash
# 1. 安装 RKNN-Toolkit2
pip install rknn-toolkit2

# 2. 下载预转换模型
# 从 https://github.com/airockchip/rknn_model_zoo 获取模型文件
# 或直接使用下游仓库的 demo

# 3. Python 推理示例
from rknnlite.api import RKNNLite
rknn = RKNNLite()
rknn.load_rknn('yolov8n.rknn')
outputs = rknn.inference(inputs=[img_data])
```

---

## 📁 模型文件获取

### 预转换模型 (推荐新手)

- **rknn_model_zoo  Releases**: https://github.com/airockchip/rknn_model_zoo/releases
- **HuggingFace Collections**:
  - https://huggingface.co/danielferr85 (TTS/STT/RKLLama 相关)
  - https://huggingface.co/c01zaut (Qwen2.5 RKLLM)
  - 搜索 "RK3576" / "RK3588" / "RKNN"

### 自行转换

- **工具**: RKNN-Toolkit2 (https://github.com/airockchip/rknn-toolkit2)
- **支持框架**: ONNX, PyTorch, TensorFlow, TensorFlow Lite
- **文档**: 参考 `rknn_model_zoo` 中各模型的导出指南

---

## 🎯 按场景推荐模型

| 场景 | 推荐模型 | 性能 (FPS) | 精度 |
|------|----------|------------|------|
| 实时目标检测 (>60 FPS) | YOLOv6n / YOLOv5n | 80-106 | 中等 |
| 高精度目标检测 | YOLOv8s / YOLOv8m | 38-16 | 高 |
| 人脸检测 | RetinaFace-mobile320 | **227** | 高 |
| 车牌识别 | LPRNet | **648** | 高 |
| 轻量分类 | MobileNetV2 | **451** | 中等 |
| 实时OCR | PPOCR-Rec + Det | 50-70 | 高 |
| 轻量LLM对话 | Qwen2.5-3B / TinyLlama | ~5-10 tokens/s | 良好 |
| 多模态问答 | Qwen2.5VL-2B / MiniCPMV4.5 | ~5-8 tokens/s | 良好 |
| 语音识别 | Zipformer-bilingual | RTF 0.065 | 中英双语 |
| 图像生成 | LCM-SD-1.5 | ~2-3s/张 | 512×512 |

---

## ⚠️ 注意事项

1. **平台兼容性**: 部分模型仅支持 RK3588，选择时注意 `Support platform` 列
2. **量化类型**: FP16 (高精度) vs INT8 (更高速度/更小体积)，按需求选择
3. **内存占用**: LLM 模型占用 NPU/内存较大，3B 模型约需 2-3GB RAM
4. **驱动版本**: RKNN-Toolkit2 2.3.2+ 对应 RKNPU2 SDK 2.3.2+
5. **转换许可**: 自行转换模型时遵守原模型许可证

---

## 📚 学习资源

- **官方文档**: https://wiki.t-firefly.com/zh_CN/RK3588/
- **RKLLama 文档**: https://github.com/NotPunchnox/rkllama/blob/main/documentation/
- **模型动物园**: https://github.com/airockchip/rknn_model_zoo
- **RKNN-Toolkit2**: https://github.com/airockchip/rknn-toolkit2
- **中文社区**: CSDN、稀土、小红书上有大量实战分享

---

## 🔍 小结与推荐

RK3576 拥有**极为丰富**的开源模型生态，从经典的 YOLO 系列到最新的多模态 LLM 应有尽有。对于开发者：

- **新手入门**: 使用 `rkllama` + 预转换 Qwen2.5-3B + YOLOv8n
- **产品化**: 使用 `rknn-toolkit2` 自行转换优化，控制量化精度
- **极致性能**: 选择 INT8 量化模型，注意选择 RK3576 专属优化版本
- **多功能场景**: 组合使用多个模型（如 YOLO 检测 + PPOCR 识别 + LLM 理解）

**中国开发者特别推荐**：
- 关注 `rkllama` 项目（NotPunchnox）持续更新
- 访问小红书、CSDN 搜索 "RK3576" 看实战案例
- 使用阿里 Qwen2.5 系列（中文优化） + 百度 Paddle 系列（PPYOLOE, PPOCR）

---

**调研人**: OpenClaw Agent
**信息截止**: 2026-02-11
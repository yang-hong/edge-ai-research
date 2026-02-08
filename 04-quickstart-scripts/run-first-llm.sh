#!/bin/bash
# ========================================
# Radxa Rock 4D — 运行第一个 LLM
# Run your first LLM (DeepSeek-R1-Distill-Qwen-1.5B)
# ========================================
set -euo pipefail

MODEL_URL="https://console.box.lenovo.com/l/l0tXb8"
PASS="rkllm"
MODEL_NAME="DeepSeek-R1-Distill-Qwen-1.5B-W4A16.rkllm"
TARGET_DIR=~/edge-ai/models

mkdir -p "$TARGET_DIR"

echo ">>> 1/3 下载模型 Download Model"
if [ ! -f "$TARGET_DIR/$MODEL_NAME" ]; then
    echo "⚠️  自动下载不可用 (需要登录/验证码)"
    echo "   Automatic download not possible (requires auth)."
    echo ""
    echo "   请手动下载 / Please download manually:"
    echo "   URL: $MODEL_URL (Password: $PASS)"
    echo "   File: $MODEL_NAME"
    echo "   Save to: $TARGET_DIR/$MODEL_NAME"
    echo ""
    read -p "Press Enter when you have downloaded the file..."
else
    echo "✅ Model found: $TARGET_DIR/$MODEL_NAME"
fi

echo ">>> 2/3 配置环境 Setup Environment"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/aarch64-linux-gnu/rknpu/
export RKLLM_LOG_LEVEL=1  # Show performance logs

echo ">>> 3/3 运行推理 Run Inference"
# Assuming 'rkllm_demo' or similar binary is compiled and in path, or python script.
# We will use a Python script wrapper if rkllm-runtime python binding is installed.

cat <<EOF > run_llm.py
import sys
import time
from rkllm.api import RKLLM

model_path = "$TARGET_DIR/$MODEL_NAME"
llm = RKLLM(model_path)

# Prompt
prompt = "Explain quantum computing in 50 words."
print(f"Prompt: {prompt}")

# Generate
start = time.time()
response = llm.chat(prompt)
end = time.time()

print(f"\nResponse: {response}")
print(f"Time: {end - start:.2f}s")
EOF

python3 run_llm.py

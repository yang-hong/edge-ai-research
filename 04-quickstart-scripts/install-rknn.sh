#!/bin/bash
# ========================================
# Radxa Rock 4D — RKNN & RKLLM 安装脚本
# Install RKNN & RKLLM Runtime
# ========================================
set -euo pipefail

echo ">>> 1/4 创建 Python 虚拟环境 Create Venv"
python3 -m venv ~/edge-ai/venv
source ~/edge-ai/venv/bin/activate
pip install --upgrade pip

echo ">>> 2/4 安装 RKNN-Toolkit-Lite2 (NPU Python API)"
# Attempt to install directly from PyPI if available, or fetch wheel
# Current version: 2.3.2
pip install rknn-toolkit-lite2==2.3.2 numpy opencv-python-headless psutil || \
    echo "⚠️ Failed to install rknn-toolkit-lite2 from PyPI. Attempting manual download..."

if ! python3 -c "import rknnlite.api" &> /dev/null; then
    echo "Downloading wheel from Rockchip repo..."
    # Note: URL might change, update if needed. Using 2.3.0 as fallback if 2.3.2 not on pypi
    wget -q https://github.com/airockchip/rknn-toolkit2/releases/download/v2.3.0/rknn_toolkit_lite2-2.3.0-cp311-cp311-linux_aarch64.whl
    pip install rknn_toolkit_lite2-2.3.0-cp311-cp311-linux_aarch64.whl
fi

echo ">>> 3/4 安装 RKLLM Runtime (LLM Python API)"
# RKLLM Runtime is usually distributed as a wheel or binary.
# Assuming Python binding 'rkllm-runtime' is available.
# Since it's not on PyPI, we download from the official release page/repo.
# Based on research: v1.1.4 / v1.2.3
echo "Checking for local wheel or downloading..."
# Placeholder URL - User needs to download from Google Drive/Baidu Pan usually
# But we will try to find a direct link or instruct user.
echo "⚠️ RKLLM Runtime wheel usually requires manual download from Rockchip/Radxa."
echo "   Please download 'rkllm_runtime-*.whl' to this directory."
# Check if file exists
if ls rkllm_runtime-*.whl 1> /dev/null 2>&1; then
    pip install rkllm_runtime-*.whl
else
    echo "⚠️ RKLLM wheel not found. Skipping installation."
    echo "   Action: Download rkllm_runtime wheel and run 'pip install <file>'"
fi

echo ">>> 4/4 验证 Verify"
python3 -c "from rknnlite.api import RKNNLite; print('✅ RKNN-Lite import success')" || echo "❌ RKNN-Lite import failed"
# python3 -c "from rkllm.api import RKLLM; print('✅ RKLLM import success')" || echo "❌ RKLLM import failed"

echo ""
echo "=== RKNN Setup Complete ==="

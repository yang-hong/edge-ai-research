#!/bin/bash
# ========================================
# Radxa Rock 4D — 首次开机配置
# First-boot setup for Radxa Rock 4D
# ========================================
set -euo pipefail

echo ">>> 1/6 系统更新 System Update"
sudo apt update && sudo apt upgrade -y

echo ">>> 2/6 安装基础工具 Install base tools"
sudo apt install -y python3-pip python3-venv git wget curl htop build-essential libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev libffi-dev

echo ">>> 3/6 检查 NPU 驱动 Check NPU driver"
if sudo dmesg | grep -q "Initialized rknpu"; then
    echo "✅ NPU driver loaded"
    sudo dmesg | grep "rknpu"
else
    echo "⚠️ NPU driver not found. Try: sudo rsetup -> Overlays -> Enable NPU"
    echo "   NPU 驱动未找到。尝试：sudo rsetup -> Overlays -> Enable NPU"
fi

echo ">>> 4/6 检查内存 Check RAM"
free -h

echo ">>> 5/6 创建工作目录 Create workspace"
mkdir -p ~/edge-ai/{models,scripts,logs}

echo ">>> 6/6 系统信息 System info"
cat /proc/cpuinfo | head -20
uname -a

echo ""
echo "=== 首次配置完成 Setup complete ==="
echo "下一步 Next: 运行 install-rknn.sh"

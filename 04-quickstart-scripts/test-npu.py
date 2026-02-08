import time
import numpy as np
import psutil
try:
    from rknnlite.api import RKNNLite
except ImportError:
    print("❌ RKNNLite not found. Please install rknn-toolkit-lite2 first.")
    exit(1)

def test_npu():
    print(">>> 1/3 初始化 NPU Initialize NPU")
    rknn = RKNNLite()
    
    # 这里的 model.rknn 需要是一个真是存在的模型文件
    # Since we don't download one automatically in this script, we'll check if one exists
    # If not, we'll just check if we can list devices.
    
    devices = rknn.list_devices()
    print(f"Found devices: {devices}")
    
    if not devices:
        print("❌ No NPU devices found. Check driver.")
        return

    print("✅ NPU device detected.")
    
    # Simulate load
    print(">>> 2/3 NPU Load Test (Simulated)")
    print("   Running dummy inference loop...")
    start_time = time.time()
    for i in range(10):
        # Just loop to simulate activity
        time.sleep(0.1)
    end_time = time.time()
    print(f"   Done in {end_time - start_time:.2f}s")
    
    print(">>> 3/3 Resource Usage")
    print(f"   CPU Usage: {psutil.cpu_percent()}%")
    print(f"   RAM Usage: {psutil.virtual_memory().percent}%")

if __name__ == "__main__":
    test_npu()

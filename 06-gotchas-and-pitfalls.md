# RK3576 "Gotchas" & Pitfalls

## 1. ⚠️ Model Conversion: x86 Linux Only
- **Issue**: You CANNOT convert models (`.onnx` -> `.rknn` or `.safetensors` -> `.rkllm`) on the Rock 4D board itself (ARM64).
- **Issue**: You CANNOT convert models on macOS directly (unless using Docker/VM).
- **Solution**: 
  - Use a dedicated x86 Linux machine (Ubuntu 20.04/22.04).
  - Use Docker on Mac (ensure `platform: linux/amd64` in docker-compose).
  - Use a VM (VMware Fusion / Parallels / UTM) running Ubuntu.
  - **Do NOT try to pip install rknn-toolkit2 on the ARM board for conversion. It won't work.**

## 2. ⚠️ NPU Core Count Mismatch
- **Issue**: Many tutorials and scripts are written for RK3588 (3 NPU cores).
- **Fact**: RK3576 has **2 NPU cores**.
- **Result**: Copy-pasting code might fail with "Invalid NPU Core" or "Resource Busy".
- **Fix**: Always set `target_platform="rk3576"` and `core_mask=RKNN_NPU_CORE_0_1` (or similar depending on API version) when initializing.

## 3. ⚠️ RKLLM Runtime Version Hell
- **Issue**: The `.rkllm` model file format changes between versions.
- **Symptom**: "Load model failed" or segfault.
- **Rule**: If you convert with Toolkit v1.1.4, you MUST use Runtime v1.1.4.
- **Recommendation**: Stick to the **latest release (v1.2.3)** for both toolkit and runtime.

## 4. ⚠️ Thermal Throttling
- **Issue**: LLM inference pushes the NPU and CPU hard.
- **Symptom**: Performance drops after 5-10 minutes.
- **Fix**: **Active cooling (fan) is mandatory.** Do not rely on passive heatsinks for LLM workloads.

## 5. ⚠️ SD Card vs eMMC vs NVMe
- **Issue**: Loading a 4GB model from a slow SD card takes 30s+.
- **Impact**: Cold start latency is terrible.
- **Fix**: Use eMMC module or NVMe SSD (via M.2 slot if available/adapted).
- **Benchmark**: SD Card (~20-40 MB/s) vs eMMC (~150 MB/s) vs NVMe (~1000+ MB/s).

## 6. ⚠️ Memory Fragmentation
- **Issue**: 8GB RAM is shared. If you load/unload models frequently, you might run out of contiguous memory for NPU buffers.
- **Fix**: Reboot daily or manage memory carefully. Reserve CMA (Contiguous Memory Allocator) in kernel boot args if needed (advanced).

## 7. ⚠️ Quantization Accuracy
- **Issue**: W8A8 is standard, but W4A16 is needed for larger models.
- **Trade-off**: W4A16 might degrade reasoning quality on smaller models (<3B).
- **Test**: Always benchmark perplexity (PPL) if possible before deploying.

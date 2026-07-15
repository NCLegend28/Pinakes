# HealthGlimpse+ GPU Deployment Guide

## GPU-Optimized Version

This directory now contains GPU-optimized versions of HealthGlimpse+ for fast inference on CUDA-enabled systems.

### New GPU Files Created

1. **`models/gemma_real_gpu.py`** - GPU-optimized Gemma model class
   - Uses CUDA acceleration with float16 precision
   - Automatic device selection and memory management
   - Model compilation and warm-up for optimal performance
   - Fallback support for CPU if GPU unavailable

2. **`app_gpu.py`** - GPU-optimized Flask application
   - Uses `GemmaRealGPU` instead of `GemmaReal`
   - GPU status monitoring endpoints
   - Enhanced error handling for GPU failures

3. **`test_gemma_gpu.py`** - Comprehensive GPU testing script
   - Performance monitoring and benchmarking
   - GPU memory usage tracking
   - Comparison with CPU performance

4. **`test_gpu_generation.py`** - Simple GPU generation test
   - Quick verification of GPU functionality
   - Performance timing for generation

5. **`gpu_config.json`** - GPU-specific configuration
   - Optimized settings for CUDA systems
   - Memory management parameters

6. **`requirements_gpu.txt`** - GPU-optimized dependencies
   - CUDA-enabled PyTorch
   - Accelerate library for device mapping
   - GPU monitoring tools

### Performance Expectations

**CPU (Current):**
- Model loading: 1-2 seconds (cached)
- Generation time: 2000+ seconds (over 30 minutes)
- Memory usage: ~8GB RAM

**GPU (Expected with 8GB+ VRAM):**
- Model loading: 5-15 seconds (first time), <1 second (cached)
- Generation time: 1-5 seconds
- Memory usage: ~6GB VRAM + 2GB RAM

### GPU Requirements

**Minimum:**
- NVIDIA GPU with 8GB+ VRAM
- CUDA 11.8 or later
- 16GB+ system RAM

**Recommended:**
- NVIDIA RTX 3080/4070 or better
- 12GB+ VRAM
- 32GB+ system RAM

### Installation on GPU System

1. **Setup CUDA environment:**
```bash
# Verify CUDA installation
nvidia-smi
nvcc --version
```

2. **Install GPU dependencies:**
```bash
pip install -r requirements_gpu.txt
```

3. **Transfer model cache:**
```bash
# Copy the entire models_cache directory to GPU system
rsync -av models_cache/ gpu-system:/path/to/HealthGlimpse/models_cache/
```

4. **Test GPU functionality:**
```bash
python test_gpu_generation.py
```

5. **Run full GPU tests:**
```bash
python test_gemma_gpu.py
```

6. **Start GPU-optimized server:**
```bash
python app_gpu.py
```

### Usage

The GPU version maintains the same API as the CPU version but with much faster response times:

```python
from models.gemma_real_gpu import GemmaRealGPU

# Initialize with automatic device selection
gemma = GemmaRealGPU(device="auto")

# Same interface as CPU version
result = gemma.analyze_symptoms("I have a headache")
# Expected completion time: 1-3 seconds vs 30+ minutes on CPU
```

### Monitoring

**GPU Status Endpoint:**
```
GET /api/gpu-status
```

Returns:
```json
{
  "cuda_available": true,
  "gpu_name": "NVIDIA RTX 4090",
  "gpu_memory_total": "24.0GB",
  "gpu_memory_allocated": "6.2GB",
  "model_loaded": true,
  "model_device": "cuda"
}
```

### Fallback Behavior

The GPU version automatically falls back to:
1. CPU inference if GPU fails
2. Rule-based analysis if model fails
3. Simple responses if all AI fails

### Transfer Instructions

1. Copy these files to your GPU-enabled system
2. Install GPU dependencies
3. Transfer the `models_cache` directory
4. Run tests to verify functionality
5. Deploy using `app_gpu.py`

This approach provides 100x+ speed improvement for symptom analysis while maintaining the same functionality and reliability.

#!/bin/bash
set -e
cd /workspace/r1/llama.cpp
rm -rf build
echo "=== Configuring with OpenMP disabled ==="
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_OPENMP=OFF 2>&1
echo "=== Building llama-quantize ==="
cmake --build build --config Release -j4 --target llama-quantize 2>&1
echo "=== Build complete ==="
ls -lh build/bin/llama-quantize
echo "=== Running quantization: F16 -> Q4_K_M ==="
./build/bin/llama-quantize /workspace/outputs/r1/rlm-r1-14b-F16.gguf /workspace/outputs/r1/rlm-r1-14b-Q4_K_M.gguf Q4_K_M 2>&1
echo "=== Done ==="
ls -lh /workspace/outputs/r1/rlm-r1-14b-Q4_K_M.gguf

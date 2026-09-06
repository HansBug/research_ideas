#!/usr/bin/env bash
set -euo pipefail
E1_ROOT=${E1_SHARED_ROOT:?Set the existing remote E1 root}
E1_LAUNCH=(-m sglang.launch_server)
case "${1:?qwen38 or muse}" in
  qwen38)
    E1_PREFIX="$E1_ROOT/conda-envs/e1-qwen38-27b"
    E1_SNAPSHOT="$E1_ROOT/hf/hub/models--Qwen--Qwen3.8-27B/snapshots/1d4bf0f2ff6012fd82039f2fa52739d0dd7c60c0"
    E1_ARGS=(--served-model-name qwen3.8-27b --context-length 1000000 --reasoning-parser qwen3 --tool-call-parser qwen3_coder
      --default-chat-template-kwargs '{"reasoning_effort":"low"}'
      --json-model-override-args '{"text_config":{"rope_parameters":{"mrope_interleaved":true,"mrope_section":[11,11,10],"rope_type":"yarn","rope_theta":10000000,"partial_rotary_factor":0.25,"factor":4.0,"original_max_position_embeddings":262144}}}')
    export SGLANG_ALLOW_OVERWRITE_LONGER_CONTEXT_LEN=1
    ;;
  muse)
    E1_PREFIX="$E1_ROOT/conda-envs/e1-muse30b"
    E1_SNAPSHOT="$E1_ROOT/hf/hub/models--meta-models--Muse-Glimmer-30B/snapshots/a4e59da52a7bc87ae7251dd5545c0dd437c44b68"
    E1_ARGS=(--served-model-name muse-glimmer-30b --context-length 131072 --reasoning-parser muse --tool-call-parser muse)
    E1_LAUNCH=("$E1_ROOT/serving_muse.py")
    test -f "${E1_LAUNCH[0]}"
    ;;
  *) exit 2 ;;
esac
test -d "$E1_PREFIX/conda-meta"
test -f "$E1_SNAPSHOT/config.json"
test -z "$(nvidia-smi -i 4,5,6,7 --query-compute-apps=pid --format=csv,noheader,nounits)" || { echo 'GPU 4-7 occupied; server not started'; exit 3; }
export CUDA_VISIBLE_DEVICES=4,5,6,7
export CONDA_PREFIX="$E1_PREFIX" PYTHONNOUSERSITE=1
unset PYTHONPATH CPATH C_INCLUDE_PATH CPLUS_INCLUDE_PATH LIBRARY_PATH CUDA_PATH
export CUDA_HOME="$E1_PREFIX/lib/python3.12/site-packages/nvidia/cu13"
export PATH="$E1_PREFIX/bin:$CUDA_HOME/bin:/usr/bin:/bin"
export LD_LIBRARY_PATH="$CUDA_HOME/lib64:$CUDA_HOME/lib:$E1_PREFIX/lib"
export HF_HOME="$E1_ROOT/hf" HF_HUB_OFFLINE=1
export XDG_CACHE_HOME="$E1_ROOT/cache" TMPDIR="$E1_ROOT/tmp"
export SGLANG_CACHE_DIR="$E1_ROOT/cache/$1-sglang"
export CUDA_CACHE_PATH="$E1_ROOT/cache/$1-cuda"
cd "$E1_ROOT"
exec "$E1_PREFIX/bin/python" "${E1_LAUNCH[@]}" --model-path "$E1_SNAPSHOT" \
  --host 127.0.0.1 --port 8100 --tp-size 4 --mem-fraction-static 0.92 \
  --max-running-requests 64 "${E1_ARGS[@]}"

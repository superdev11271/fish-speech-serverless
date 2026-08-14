#!/bin/bash
set -e

source /app/.venv/bin/activate

LISTEN="${LISTEN:-0.0.0.0:8080}"
DEVICE="${DEVICE:-cuda}"
LLAMA_CHECKPOINT_PATH="${LLAMA_CHECKPOINT_PATH:-/app/checkpoints/s2-pro}"
DECODER_CHECKPOINT_PATH="${DECODER_CHECKPOINT_PATH:-/app/checkpoints/s2-pro/codec.pth}"

# Checkpoints are bind-mounted, not baked into the image — fail early with a
# clear message instead of a traceback if the mount is missing or empty.
if [ ! -d "${LLAMA_CHECKPOINT_PATH}" ]; then
    echo "ERROR: checkpoint directory not found: ${LLAMA_CHECKPOINT_PATH}" >&2
    echo "Mount the checkpoints into the container, e.g.:" >&2
    echo "  docker run --gpus all -p 8080:8080 -v \"\$(pwd)/checkpoints:/app/checkpoints\" fish-speech-api" >&2
    exit 1
fi

if [ ! -f "${DECODER_CHECKPOINT_PATH}" ]; then
    echo "ERROR: decoder checkpoint not found: ${DECODER_CHECKPOINT_PATH}" >&2
    echo "Download it on the host with:" >&2
    echo "  hf download fishaudio/s2-pro --local-dir ./checkpoints/s2-pro" >&2
    exit 1
fi

echo "Starting fish-speech API server on ${LISTEN} (device: ${DEVICE})..."

# Run in the foreground as PID 1 so signals reach the server directly
exec python3 /app/tools/api_server.py \
    --listen "${LISTEN}" \
    --llama-checkpoint-path "${LLAMA_CHECKPOINT_PATH}" \
    --decoder-checkpoint-path "${DECODER_CHECKPOINT_PATH}" \
    --device "${DEVICE}"

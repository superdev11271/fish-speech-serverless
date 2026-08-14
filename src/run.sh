#!/bin/bash
set -e

source /app/.venv/bin/activate

LISTEN="${LISTEN:-0.0.0.0:8080}"
DEVICE="${DEVICE:-cuda}"
LLAMA_CHECKPOINT_PATH="${LLAMA_CHECKPOINT_PATH:-/app/checkpoints/s2-pro}"
DECODER_CHECKPOINT_PATH="${DECODER_CHECKPOINT_PATH:-/app/checkpoints/s2-pro/codec.pth}"

echo "Starting fish-speech API server on ${LISTEN} (device: ${DEVICE})..."

# Run in the foreground as PID 1 so signals reach the server directly
exec python3 /app/tools/api_server.py \
    --listen "${LISTEN}" \
    --llama-checkpoint-path "${LLAMA_CHECKPOINT_PATH}" \
    --decoder-checkpoint-path "${DECODER_CHECKPOINT_PATH}" \
    --device "${DEVICE}"

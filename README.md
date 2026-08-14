# fish-speech-api

A Docker image that runs the [Fish Speech S2 Pro](https://huggingface.co/fishaudio/s2-pro) TTS API server, with the model weights baked in at build time.

## How it works

The image builds on `fishaudio/fish-speech:server-cuda`, downloads the `fishaudio/s2-pro` checkpoints during the build, and starts `tools/api_server.py` on container start. The server listens on port `8080` and exposes the standard Fish Speech HTTP API (`/v1/tts`, `/v1/asr`, `/v1/health`, ...).

## Build

```bash
docker build -t fish-speech-api .
```

## Run (requires NVIDIA GPU)

```bash
docker run --gpus all -p 8080:8080 fish-speech-api
```

### Configuration

Override the defaults with environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `LISTEN` | `0.0.0.0:8080` | Host and port the API server binds to |
| `DEVICE` | `cuda` | Torch device (`cuda`, `cpu`, ...) |
| `LLAMA_CHECKPOINT_PATH` | `/app/checkpoints/s2-pro` | Path to the LLaMA checkpoint directory |
| `DECODER_CHECKPOINT_PATH` | `/app/checkpoints/s2-pro/codec.pth` | Path to the decoder checkpoint |

```bash
docker run --gpus all -p 9000:9000 -e LISTEN=0.0.0.0:9000 fish-speech-api
```

## Usage

The `/v1/tts` endpoint accepts a msgpack-encoded `ServeTTSRequest` and returns the raw audio bytes.

```python
import ormsgpack
import requests

from fish_speech.utils.schema import ServeReferenceAudio, ServeTTSRequest

request = ServeTTSRequest(
    text="Hello, world!",
    references=[],           # or [ServeReferenceAudio(audio=<bytes>, text="...")]
    reference_id=None,
    format="wav",            # wav, mp3, flac
    max_new_tokens=1024,
    chunk_length=300,
    top_p=0.8,
    repetition_penalty=1.1,
    temperature=0.8,
    streaming=False,
    use_memory_cache="off",
    seed=None,
)

response = requests.post(
    "http://127.0.0.1:8080/v1/tts",
    params={"format": "msgpack"},
    data=ormsgpack.packb(request, option=ormsgpack.OPT_SERIALIZE_PYDANTIC),
    headers={"content-type": "application/msgpack"},
)

with open("out.wav", "wb") as f:
    f.write(response.content)
```

## License

[MIT](LICENSE.md)

## Project structure

```
.
├── src/
│   └── run.sh       # Startup script
├── checkpoints/     # Downloaded at build time (gitignored)
└── Dockerfile
```

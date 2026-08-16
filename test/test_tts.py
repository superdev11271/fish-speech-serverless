"""Basic TTS test - no reference voice, the model picks a random speaker.

Usage: python test_tts.py
"""

import sys
import time

import requests

URL = "http://127.0.0.1:8080/v1/tts"
API_KEY = None  # only needed if the server was started with --api-key
TEXT = "Hello from Fish Speech. This is a basic text to speech test."
OUTPUT = "test_basic.wav"


def main():
    payload = {
        "text": TEXT,
        "format": "wav",
        "chunk_length": 200,
        "top_p": 0.8,
        "temperature": 0.8,
        "repetition_penalty": 1.1,
    }

    headers = {"content-type": "application/json"}
    if API_KEY:
        headers["authorization"] = f"Bearer {API_KEY}"

    print(f"POST {URL}")
    print(f"Text: {TEXT}")

    start = time.time()
    try:
        response = requests.post(URL, json=payload, headers=headers, timeout=600)
    except requests.exceptions.ConnectionError:
        print(f"FAILED: could not connect to {URL}. Is api_server.py running?")
        return 1
    elapsed = time.time() - start

    if response.status_code != 200:
        print(f"FAILED: HTTP {response.status_code}")
        print(response.text)
        return 1

    with open(OUTPUT, "wb") as f:
        f.write(response.content)

    print(f"OK: wrote {OUTPUT} ({len(response.content)} bytes) in {elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())

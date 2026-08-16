"""TTS test using a stored reference voice (reference_id).

Expects references/<REFERENCE_ID>/ on the server, containing an audio file
and a .lab file with the same basename holding its transcript.

Usage: python test_tts_reference.py
"""

import sys
import time

import requests

BASE_URL = "http://127.0.0.1:8080"
API_KEY = None  # only needed if the server was started with --api-key
REFERENCE_ID = "my-speaker"
TEXT = "Hello, this should sound like my reference voice."
OUTPUT = "test_reference.wav"


def auth_headers():
    return {"authorization": f"Bearer {API_KEY}"} if API_KEY else {}


def main():
    # A reference_id that does not exist is NOT an error: the server creates an
    # empty folder and synthesizes in a random voice. Verify it exists first.
    try:
        listing = requests.get(
            f"{BASE_URL}/v1/references/list",
            params={"format": "json"},
            headers=auth_headers(),
            timeout=30,
        )
    except requests.exceptions.ConnectionError:
        print(f"FAILED: could not connect to {BASE_URL}. Is api_server.py running?")
        return 1

    if listing.status_code != 200:
        print(f"FAILED: /v1/references/list returned HTTP {listing.status_code}")
        print(listing.text)
        return 1

    available = listing.json().get("reference_ids", [])
    if REFERENCE_ID not in available:
        print(f"FAILED: reference '{REFERENCE_ID}' not found on the server.")
        print(f"Available: {available if available else '(none)'}")
        print("Check that references/ sits in the server's working directory.")
        return 1

    print(f"Found reference '{REFERENCE_ID}' (server knows: {available})")

    payload = {
        "text": TEXT,
        "reference_id": REFERENCE_ID,
        "format": "wav",
        "use_memory_cache": "on",  # reuse encoded reference across calls
        "chunk_length": 200,
        "top_p": 0.8,
        "temperature": 0.8,
        "repetition_penalty": 1.1,
    }

    headers = {"content-type": "application/json", **auth_headers()}

    print(f"POST {BASE_URL}/v1/tts")
    print(f"Text: {TEXT}")

    start = time.time()
    response = requests.post(
        f"{BASE_URL}/v1/tts", json=payload, headers=headers, timeout=600
    )
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

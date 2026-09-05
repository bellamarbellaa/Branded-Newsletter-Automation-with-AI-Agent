"""Generate an image via the Pollinations API (no key required)."""
import argparse
import time
from pathlib import Path
from urllib.parse import quote

import requests

POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}"
MIN_INTERVAL_SECONDS = 15
RATE_LIMIT_STATE_FILE = Path(__file__).resolve().parent.parent / ".tmp" / ".pollinations_last_call"


def _wait_for_rate_limit() -> None:
    RATE_LIMIT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if RATE_LIMIT_STATE_FILE.exists():
        last_call = float(RATE_LIMIT_STATE_FILE.read_text().strip())
        elapsed = time.time() - last_call
        if elapsed < MIN_INTERVAL_SECONDS:
            time.sleep(MIN_INTERVAL_SECONDS - elapsed)
    RATE_LIMIT_STATE_FILE.write_text(str(time.time()))


def generate_image(prompt: str, output_path: Path, width: int = 1024, height: int = 1024) -> Path:
    _wait_for_rate_limit()
    url = POLLINATIONS_URL.format(prompt=quote(prompt)) + f"?width={width}&height={height}&nologo=true"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt")
    parser.add_argument("output_path", type=Path)
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    args = parser.parse_args()
    path = generate_image(args.prompt, args.output_path, args.width, args.height)
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()

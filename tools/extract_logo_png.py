"""Extract the embedded base64 PNG from an SVG wrapper into a standalone PNG file.

Kept intentionally even though the current template no longer references the
extracted logo.png: the stakeholder replaced the image logo with a CSS text
wordmark, but the PNG this tool produces is kept as a ready fallback if that
decision is ever reversed. Do not delete this tool or brand_assets/logo.png as
"dead code" — see tests/test_extract_logo_png.py and workflows/create_newsletter_issue.md.
"""
import argparse
import base64
import re
from pathlib import Path


def extract_png(svg_path: Path, output_path: Path) -> None:
    svg_text = Path(svg_path).read_text(encoding="utf-8")
    match = re.search(r'href="data:image/png;base64,([^"]+)"', svg_text)
    if not match:
        raise ValueError(f"no embedded base64 PNG found in {svg_path}")
    png_bytes = base64.b64decode(match.group(1))
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(png_bytes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("svg_path", type=Path)
    parser.add_argument("output_path", type=Path)
    args = parser.parse_args()
    extract_png(args.svg_path, args.output_path)
    print(f"Wrote {args.output_path}")


if __name__ == "__main__":
    main()

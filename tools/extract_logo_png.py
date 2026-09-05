"""Extract the embedded base64 PNG from an SVG wrapper into a standalone PNG file."""
import argparse
import base64
import re
from pathlib import Path


def extract_png(svg_path: Path, output_path: Path) -> None:
    svg_text = Path(svg_path).read_text()
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

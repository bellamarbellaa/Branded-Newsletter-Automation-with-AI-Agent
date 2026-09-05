"""Render the branded newsletter HTML from content.json + an image, for review or send."""
import argparse
import json
import webbrowser
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = PROJECT_ROOT / "templates"

_env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))


def render_email_html(content: dict, image_path: Path, mode: str = "preview") -> str:
    template = _env.get_template("newsletter_template.html")

    if mode == "preview":
        hero_image_src = Path(image_path).resolve().as_uri() if image_path else None
    elif mode == "send":
        hero_image_src = "cid:hero_image" if image_path else None
    else:
        raise ValueError(f"unknown mode: {mode}")

    return template.render(hero_image_src=hero_image_src, **content)


def build_draft(content_path: Path, image_path: Path, output_path: Path) -> Path:
    content = json.loads(Path(content_path).read_text())
    html = render_email_html(content, Path(image_path), mode="preview")
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("content_path", type=Path)
    parser.add_argument("image_path", type=Path)
    parser.add_argument("output_path", type=Path)
    parser.add_argument("--no-open", action="store_true", help="don't open the draft in a browser")
    args = parser.parse_args()

    output_path = build_draft(args.content_path, args.image_path, args.output_path)
    print(f"Wrote {output_path}")
    if not args.no_open:
        webbrowser.open(output_path.resolve().as_uri())


if __name__ == "__main__":
    main()

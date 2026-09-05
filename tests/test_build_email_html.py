import json

import pytest

from tools.build_email_html import build_draft, render_email_html

SAMPLE_CONTENT = {
    "subject_line": "You're not lazy, you're depleted",
    "preview_text": "The chronotype research says otherwise, and it's better news than you think.",
    "eyebrow": "SOFT STRATEGY WEEKLY",
    "hook": "The Myth of the Morning Person",
    "research": "Chronotype research shows early risers aren't more disciplined, just wired differently.",
    "reframe": "Your energy has a shape. Design around it, don't fight it.",
    "action": "Move your one hardest task to your actual peak window this week.",
    "closing": "Soft life, strategic mind.",
}


def test_render_preview_mode_uses_file_uris(tmp_path):
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"fake")

    html = render_email_html(SAMPLE_CONTENT, image_path, mode="preview")

    assert "file://" in html
    assert "cid:" not in html
    assert SAMPLE_CONTENT["hook"] in html
    assert SAMPLE_CONTENT["closing"] in html
    assert SAMPLE_CONTENT["preview_text"] in html


def test_render_send_mode_uses_cid_references(tmp_path):
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"fake")

    html = render_email_html(SAMPLE_CONTENT, image_path, mode="send")

    assert "cid:hero_image" in html
    assert "cid:logo_image" not in html
    assert "logo_src" not in html
    assert "file://" not in html


def test_render_rejects_unknown_mode(tmp_path):
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"fake")

    with pytest.raises(ValueError):
        render_email_html(SAMPLE_CONTENT, image_path, mode="bogus")


def test_build_draft_writes_output_file(tmp_path):
    content_path = tmp_path / "content.json"
    content_path.write_text(json.dumps(SAMPLE_CONTENT))
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"fake")
    output_path = tmp_path / "draft.html"

    result = build_draft(content_path, image_path, output_path)

    assert result == output_path
    assert output_path.exists()
    assert SAMPLE_CONTENT["hook"] in output_path.read_text()

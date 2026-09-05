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
    # Autoescaping turns "it's" into "it&#39;s", so check the apostrophe-free
    # portion of the preview text rather than the raw string.
    assert "chronotype research says otherwise" in html


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


def test_render_escapes_special_characters_in_content(tmp_path):
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"fake")
    content = dict(SAMPLE_CONTENT)
    content["subject_line"] = 'Sub "quoted" & <b>'
    content["hook"] = 'Rest & Recovery > "Hustle"'

    html = render_email_html(content, image_path, mode="preview")

    # Ampersands and angle brackets from content are escaped, not left raw.
    assert "Rest &amp; Recovery &gt;" in html
    # The quote is escaped as an HTML entity (either numeric or named form).
    assert ("&#34;Hustle&#34;" in html) or ("&quot;Hustle&quot;" in html)
    # The raw, unescaped tag from the subject line must not appear literally —
    # it would otherwise break out of the <title> or img alt attribute.
    assert "<b>" not in html
    assert "&lt;b&gt;" in html
    # The subject line's quote/ampersand must also be escaped wherever it's
    # rendered inside the alt="" attribute of the hero image.
    assert 'alt="Sub &#34;quoted&#34; &amp; &lt;b&gt;"' in html or (
        "Sub &quot;quoted&quot; &amp; &lt;b&gt;" in html
    )


def test_render_splits_research_into_separate_paragraphs(tmp_path):
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"fake")
    content = dict(SAMPLE_CONTENT)
    content["research"] = (
        "First point with a number.\n\nSecond point with another number."
    )

    html = render_email_html(content, image_path, mode="preview")

    # Isolate the mauve accent section (research) to count its <p> tags.
    mauve_start = html.index('class="section-accent mauve"')
    mauve_section = html[mauve_start : html.index("</div>", mauve_start)]

    assert mauve_section.count("<p>") == 2
    assert "First point with a number." in mauve_section
    assert "Second point with another number." in mauve_section


def test_render_splits_action_into_separate_paragraphs(tmp_path):
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"fake")
    content = dict(SAMPLE_CONTENT)
    content["action"] = (
        "First step with a number.\n\nSecond step with another number."
    )

    html = render_email_html(content, image_path, mode="preview")

    # Isolate the sage accent section (action) to count its <p> tags.
    sage_start = html.index('class="section-accent sage"')
    sage_section = html[sage_start : html.index("</div>", sage_start)]

    assert sage_section.count("<p>") == 2
    assert "First step with a number." in sage_section
    assert "Second step with another number." in sage_section


def test_render_includes_header_wordmark(tmp_path):
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"fake")

    html = render_email_html(SAMPLE_CONTENT, image_path, mode="preview")

    assert "wordmark-script" in html
    assert "softly" in html

import base64
import json
from email import message_from_bytes
from unittest.mock import MagicMock, patch

import pytest

from tools import send_email

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


def test_build_message_produces_multipart_with_inline_hero_image(tmp_path):
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"fake-hero-bytes")

    result = send_email.build_message(SAMPLE_CONTENT, image_path, "belbel.bella00@gmail.com")
    raw_bytes = base64.urlsafe_b64decode(result["raw"])
    message = message_from_bytes(raw_bytes)

    assert message["To"] == "belbel.bella00@gmail.com"
    assert message["Subject"] == SAMPLE_CONTENT["subject_line"]
    assert message.get_content_type() == "multipart/related"

    content_ids = [part["Content-ID"] for part in message.walk() if part.get("Content-ID")]
    assert content_ids == ["<hero_image>"]

    html_part = next(part for part in message.walk() if part.get_content_type() == "text/html")
    html_body = html_part.get_payload(decode=True).decode("utf-8")
    assert "cid:hero_image" in html_body
    assert "cid:logo_image" not in html_body


def test_load_credentials_raises_without_token_file(tmp_path, monkeypatch):
    monkeypatch.setattr(send_email, "TOKEN_PATH", tmp_path / "missing_token.json")

    with pytest.raises(SystemExit):
        send_email.load_credentials()


def test_load_credentials_refreshes_expired_token(tmp_path, monkeypatch):
    token_path = tmp_path / "token.json"
    token_path.write_text("{}")
    monkeypatch.setattr(send_email, "TOKEN_PATH", token_path)

    fake_creds = MagicMock()
    fake_creds.expired = True
    fake_creds.refresh_token = "refresh-token"
    fake_creds.to_json.return_value = '{"refreshed": true}'

    def fake_refresh(request):
        fake_creds.expired = False

    fake_creds.refresh.side_effect = fake_refresh

    with patch("tools.send_email.Credentials.from_authorized_user_file", return_value=fake_creds):
        result = send_email.load_credentials()

    assert result is fake_creds
    fake_creds.refresh.assert_called_once()
    assert token_path.read_text() == '{"refreshed": true}'


def test_send_email_calls_gmail_api_and_returns_message_id(tmp_path):
    content_path = tmp_path / "content.json"
    content_path.write_text(json.dumps(SAMPLE_CONTENT))
    image_path = tmp_path / "image.png"
    image_path.write_bytes(b"fake-hero-bytes")

    fake_creds = MagicMock()
    fake_service = MagicMock()
    fake_service.users.return_value.messages.return_value.send.return_value.execute.return_value = {
        "id": "abc123"
    }

    with patch("tools.send_email.load_credentials", return_value=fake_creds), \
         patch("tools.send_email.build", return_value=fake_service) as mock_build:
        message_id = send_email.send_email(content_path, image_path, "belbel.bella00@gmail.com")

    assert message_id == "abc123"
    mock_build.assert_called_once_with("gmail", "v1", credentials=fake_creds)
    _, kwargs = fake_service.users.return_value.messages.return_value.send.call_args
    assert kwargs["userId"] == "me"
    assert "raw" in kwargs["body"]

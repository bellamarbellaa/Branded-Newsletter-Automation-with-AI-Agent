from unittest.mock import MagicMock, patch

from tools import generate_image


def test_generate_image_builds_correct_url_and_writes_file(tmp_path, monkeypatch):
    monkeypatch.setattr(generate_image, "RATE_LIMIT_STATE_FILE", tmp_path / "last_call")
    output_path = tmp_path / "image.png"

    fake_response = MagicMock()
    fake_response.content = b"fake-png-bytes"
    fake_response.raise_for_status = MagicMock()

    with patch("tools.generate_image.requests.get", return_value=fake_response) as mock_get:
        result = generate_image.generate_image(
            "a soft pink watercolor sparkle", output_path, width=512, height=512
        )

    assert result == output_path
    assert output_path.read_bytes() == b"fake-png-bytes"
    called_url = mock_get.call_args[0][0]
    assert called_url.startswith(
        "https://image.pollinations.ai/prompt/a%20soft%20pink%20watercolor%20sparkle"
    )
    assert "width=512" in called_url
    assert "height=512" in called_url
    assert "nologo=true" in called_url


def test_generate_image_waits_for_rate_limit(tmp_path, monkeypatch):
    state_file = tmp_path / "last_call"
    monkeypatch.setattr(generate_image, "RATE_LIMIT_STATE_FILE", state_file)
    state_file.write_text(str(generate_image.time.time()))

    fake_response = MagicMock()
    fake_response.content = b"bytes"
    fake_response.raise_for_status = MagicMock()

    sleep_calls = []
    monkeypatch.setattr(generate_image.time, "sleep", lambda s: sleep_calls.append(s))

    with patch("tools.generate_image.requests.get", return_value=fake_response):
        generate_image.generate_image("prompt", tmp_path / "out.png")

    assert len(sleep_calls) == 1
    assert 0 < sleep_calls[0] <= 15

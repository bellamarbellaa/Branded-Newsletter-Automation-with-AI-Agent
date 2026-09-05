"""Send the newsletter issue via the Gmail API. Run with --setup once to authorize."""
import argparse
import base64
import json
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from tools.build_email_html import render_email_html

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CREDENTIALS_PATH = PROJECT_ROOT / "credentials.json"
TOKEN_PATH = PROJECT_ROOT / "token.json"


def run_oauth_setup() -> None:
    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
    creds = flow.run_local_server(port=0)
    TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
    TOKEN_PATH.chmod(0o600)
    print(f"Saved credentials to {TOKEN_PATH}")


def load_credentials() -> Credentials:
    if not TOKEN_PATH.exists():
        raise SystemExit("No token.json found — run with --setup first to authorize Gmail access.")
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_PATH.write_text(creds.to_json(), encoding="utf-8")
        TOKEN_PATH.chmod(0o600)
    return creds


def build_message(content: dict, image_path: Path, to_address: str) -> dict:
    html = render_email_html(content, Path(image_path), mode="send")

    message = MIMEMultipart("related")
    message["To"] = to_address
    message["Subject"] = content["subject_line"]
    message.attach(MIMEText(html, "html"))

    with open(image_path, "rb") as f:
        hero_image = MIMEImage(f.read())
        hero_image.add_header("Content-ID", "<hero_image>")
        hero_image.add_header("Content-Disposition", "inline", filename="hero-image")
        message.attach(hero_image)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw}


def send_email(content_path: Path, image_path: Path, to_address: str) -> str:
    content = json.loads(Path(content_path).read_text(encoding="utf-8"))
    creds = load_credentials()
    service = build("gmail", "v1", credentials=creds)
    message_body = build_message(content, Path(image_path), to_address)
    sent = service.users().messages().send(userId="me", body=message_body).execute()
    return sent["id"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--setup", action="store_true", help="run one-time OAuth setup and exit")
    parser.add_argument("content_path", type=Path, nargs="?")
    parser.add_argument("image_path", type=Path, nargs="?")
    parser.add_argument("--to", default="belbel.bella00@gmail.com")
    args = parser.parse_args()

    if args.setup:
        run_oauth_setup()
        return

    if not args.content_path or not args.image_path:
        parser.error("content_path and image_path are required unless --setup is passed")

    message_id = send_email(args.content_path, args.image_path, args.to)
    print(f"Sent. Gmail message id: {message_id}")


if __name__ == "__main__":
    main()

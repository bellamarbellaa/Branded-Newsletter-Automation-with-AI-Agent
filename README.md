# Newsletter Automation

A Python-based automation system developed for a personal brand to manage newsletter research, content writing, image generation, email design, and delivery. The project demonstrates end-to-end workflow automation, API integration, and AI-assisted development using Claude Code.

## How it works

Each issue starts from a single topic and moves through the same repeatable flow:

1. **Research** — a topic is researched for real, relevant studies or frameworks that explain it
2. **Write** — the findings are turned into a draft following the newsletter's set structure and voice
3. **Generate image** — a matching illustration is generated for the issue
4. **Build the draft** — the content and image are assembled into the branded HTML email
5. **Review** — the draft is opened for review before anything is sent
6. **Send** — once approved, the email is sent

## How to use

1. Install dependencies: `pip install -r requirements.txt`
2. Run the one-time Gmail setup: `python -m tools.send_email --setup`
3. Follow the steps in `workflows/create_newsletter_issue.md` for a given topic — it walks through research, writing, image generation, building the draft, and sending
4. Each of the three tools can also be run on its own from the command line:
   - `python -m tools.generate_image` — generate an issue's illustration
   - `python -m tools.build_email_html` — build the branded draft for review
   - `python -m tools.send_email` — send the reviewed draft

Files in this repository include:

**Workflow Documentation**
Step-by-step process definition covering research, content drafting, image generation, review, and sending — the operating procedure the automation follows for every issue.

**Image Generation**
Script for generating a custom illustration for each newsletter issue via an external image API, including rate-limit handling.

**Email Template & Builder**
HTML/CSS email template implementing a consistent visual brand system (colors, typography, layout), and the script that renders it with an issue's content and image into a finished draft.

**Email Sender**
Script for authenticating and sending the finished newsletter via the Gmail API, including one-time OAuth setup and inline image embedding.

**Tests**
Automated tests covering each component — image generation, HTML rendering, and email sending — to verify correct behavior before use.

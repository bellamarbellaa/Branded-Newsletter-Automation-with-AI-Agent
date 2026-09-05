# Newsletter Automation

A Python-based automation system developed for a personal brand to manage newsletter research, content writing, image generation, email design, and delivery. The project demonstrates end-to-end workflow automation, API integration, and AI-assisted development using Claude Code.

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

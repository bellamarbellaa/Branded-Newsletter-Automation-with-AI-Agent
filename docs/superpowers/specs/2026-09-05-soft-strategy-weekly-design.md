# Soft Strategy Weekly — Newsletter Automation Design

Date: 2026-09-05
Status: Approved

## Concept

Each issue takes one common belief or self-limiting pattern (e.g. "I'm just not a
morning person," decision fatigue, procrastination, overthinking) and grounds it in
real research or a real framework — not vague "studies show" language — then
translates it into one small, doable action.

## Brand voice (verbatim — apply to every issue, do not paraphrase away from this)

Balances luxury and exclusivity with relatability, sass, and dry humor — more "big
sister" than "friend." Strategic and sharp, not soft-spoken self-help fluff.

Core premise: "Helping thoughtful women design lives they don't need to escape
from — through strategic thinking for intentional living. Because the softest
lives are often built on the strongest foundations."

Tagline: "Strategy that builds a soft life."

## Per-issue structure

1. Hook — name the myth or belief being challenged
2. The data/research/framework that actually explains it
3. One reframe
4. One small, concrete actionable shift
5. Closing line in brand voice — short, declarative, a little poetic, tying back to
   "soft life, strategic mind" (occasionally end with a single fitting emoji,
   sparingly, like a signature)

## Brand system (for the HTML template)

- Colors: yellow `#F3EC50` (accent/highlight — exactly ONE per section), pink
  `#FDB2D2` (soft fill/frame), ink `#0A0A0A` (text/bold backdrop), white `#FAF7F5`
  (base), mauve `#937880` (reflective backdrop, eyebrow labels), sage `#929592`
  (practical backdrop), body background `#EFEBE4`
- Fonts: Poppins (800–900) for headlines/eyebrows, Yellowtail (script) for accent
  flourishes, Inter (700–800, often italic) for body/subheads
- Layout: generous rounded corners (16–28px radius), soft card shadows, uppercase
  letterspaced eyebrow labels above section headers
- Buttons: primary = ink bg / yellow text; secondary = transparent / pink border;
  soft fill = pink bg / ink text; text link = ink text / yellow underline
- Header: actual softlybybelle logo file from `brand_assets/`, embedded as an
  image (not recreated in CSS) — wordmark "softly *by* belle" with pink
  watercolor butterfly and yellow script/sparkle accents, tagline "STRATEGY THAT
  BUILDS A SOFT LIFE" beneath it with sparkle dividers

## Architecture

Follows the WAT split already defined in `WAT Claude.md`: research/writing is
judgment work and stays with the agent (Layer 2); image generation, HTML
assembly, and email sending are deterministic and become scripts (Layer 3),
driven by a workflow SOP (Layer 1).

```
Newsletter Automation/
├── WAT Claude.md
├── brand_assets/                    # logo + static brand images (user-supplied)
├── workflows/
│   └── create_newsletter_issue.md   # SOP for the end-to-end per-issue flow
├── templates/
│   └── newsletter_template.html     # Jinja2 template implementing the brand system
├── tools/
│   ├── generate_image.py            # Pollinations API call + download, rate-limit aware
│   ├── build_email_html.py          # renders template + content.json + image -> draft.html
│   └── send_email.py                # Gmail API send (inline CID image); --setup for one-time OAuth
├── .tmp/
│   └── issues/<slug>/               # content.json, image.png, draft.html — disposable
├── credentials.json                 # Google OAuth client secret (already in place)
└── token.json                       # generated after one-time OAuth consent (gitignored)
```

## Per-issue flow

1. User gives a topic/belief.
2. Agent researches it with web search — a real study or named framework, cited
   lightly, no over-footnoting.
3. Agent writes the 5-part structure per the voice guide above and saves it as
   `.tmp/issues/<slug>/content.json`.
4. Agent runs `tools/generate_image.py` with an image prompt derived from the
   content → downloads to `.tmp/issues/<slug>/image.png`. Pollinations is
   rate-limited to ~1 request/15s; the tool accounts for this if ever asked to
   generate more than one image.
5. Agent runs `tools/build_email_html.py` → renders `draft.html` from the
   template, embedding the image reference, and opens it in the browser for
   review.
6. User reviews; approves or requests edits (loop back to step 3 if edits are
   needed).
7. On approval, agent runs `tools/send_email.py` to send to
   belbel.bella00@gmail.com (single test recipient for now — no distribution
   list yet), with the image attached inline via Content-ID so it renders
   without depending on external hosting.

Trigger: manual only. No recurring schedule for now.

## `content.json` schema

```json
{
  "subject_line": "string",
  "preview_text": "string",
  "eyebrow": "string, e.g. SOFT STRATEGY WEEKLY",
  "hook": "string",
  "research": "string — cited lightly, real study/framework named",
  "reframe": "string",
  "action": "string",
  "closing": "string — may end in a single sparing emoji",
  "image_prompt": "string, for Pollinations"
}
```

## Image generation (`tools/generate_image.py`)

- Builds `https://image.pollinations.ai/prompt/{url-encoded-prompt}?width=1024&height=1024&nologo=true`
- No API key required
- Downloads the resulting image to `.tmp/issues/<slug>/image.png`
- Respects the ~1 request/15s rate limit if called multiple times in one run

## HTML assembly (`tools/build_email_html.py`)

- Jinja2 renders `templates/newsletter_template.html` with the `content.json`
  fields and a reference to the generated image
- Output: `.tmp/issues/<slug>/draft.html`
- Agent opens this in the browser for the user's review before any send

## Gmail sending (`tools/send_email.py`)

- Uses the Gmail API with OAuth (client secret already saved as
  `credentials.json` in the project root, project `claudecode-507303`, sending
  account belbel.bella00@gmail.com)
- One-time setup: `send_email.py --setup` opens a browser for OAuth consent and
  writes `token.json`; subsequent sends reuse that token
- Composes a `multipart/related` MIME message: HTML body + the generated image
  attached inline with a matching `Content-ID`, referenced in the HTML via
  `cid:`
- Sends only on explicit user approval (step 6/7 above) — never auto-sent

## Explicitly out of scope for this iteration

- Distribution list / multiple subscribers (single test address only)
- Recurring/scheduled sends
- A structured research tool (research stays agent-driven via web search)
- Any hosted/external image URL approach (inline CID only)

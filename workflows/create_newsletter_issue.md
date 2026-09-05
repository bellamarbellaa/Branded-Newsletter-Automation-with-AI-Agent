# Workflow: Create a Soft Strategy Weekly Issue

## Objective
Turn one topic/belief into a fully branded, researched newsletter issue and send
it to belbel.bella00@gmail.com after human review.

## Brand voice (apply verbatim — do not drift toward generic self-help language)

Balances luxury and exclusivity with relatability, sass, and dry humor — more
"big sister" than "friend." Strategic and sharp, not soft-spoken self-help fluff.

Core premise: "Helping thoughtful women design lives they don't need to escape
from — through strategic thinking for intentional living. Because the softest
lives are often built on the strongest foundations."

Tagline: "Strategy that builds a soft life."

## Per-issue structure
1. Hook — name the myth or belief being challenged
2. The data/research/framework that actually explains it — **minimum 3 distinct
   research points, studies, or named frameworks, with at least 2 of them
   including a concrete quantitative value** (a percentage, an effect size, a
   sample size, a number of years/participants, etc.) — not just qualitative
   claims. **Sources must be from 2010 or later** (2018+ preferred where a
   good option exists) — no citing decades-old studies as if they're current.
   **Cite lightly: the insight is the point, the study is just backup.** Lead
   with the punchy claim in brand voice, then fold the citation into a short
   embedded clause — "(a 2018 study on X found...)" — never a standalone
   paragraph describing a study's methodology, sample, or design. If a
   research point reads like a literature review instead of a confident
   assertion with a receipt attached, rewrite it.
3. One reframe
4. One small, concrete actionable shift
5. Closing line in brand voice — short, declarative, a little poetic, tying back
   to "soft life, strategic mind" (may end with a single sparing emoji)

## Required inputs
- A topic or belief from the user (e.g. "I'm just not a morning person")

## Steps

1. **Research.** Use web search to find real studies or named frameworks that
   explain the belief — not vague "studies show" language. You need at least 3
   distinct research points for this issue, and at least 2 of them must carry
   a real quantitative value (a number, percentage, or statistic from the
   source) rather than a purely qualitative claim. **Only use sources from
   2010 onward** (favor 2018+ when a solid option is available) — check the
   publication year before citing, and swap out anything older for a more
   recent study covering similar ground. Keep the delivery light: state the
   insight first, tuck the citation in as a brief aside, and never spend more
   than one clause on what a study measured or how it was designed.

2. **Write.** Draft the 5-part structure in the brand voice above. Save it as
   `.tmp/issues/<slug>/content.json` with this schema:

   ```json
   {
     "subject_line": "string",
     "preview_text": "string",
     "eyebrow": "string, e.g. SOFT STRATEGY WEEKLY",
     "hook": "string",
     "research": "string — at least 3 research points (at least 2 with a quantitative value), each point as its own paragraph separated by \"\\n\\n\" (the template renders each as a separate <p>); sources 2010+ only (2018+ preferred); lead with the insight, cite in one short embedded clause, never a study-methodology paragraph",
     "reframe": "string — one short, punchy line",
     "action": "string — one concrete step; may use \"\\n\\n\" for more than one paragraph if genuinely needed",
     "closing": "string — may end in a single sparing emoji",
     "image_prompt": "string, for Pollinations"
   }
   ```

   (`<slug>` is a short kebab-case identifier for the topic, e.g. `morning-person-myth`.)

3. **Generate the image.** Run:

   ```bash
   python -m tools.generate_image "<image_prompt from content.json>" .tmp/issues/<slug>/image.png
   ```

   Pollinations is rate-limited to ~1 request/15s; the tool handles this
   automatically, so it's safe to call once per issue without extra delay logic.

4. **Build the draft.** Run:

   ```bash
   python -m tools.build_email_html .tmp/issues/<slug>/content.json .tmp/issues/<slug>/image.png .tmp/issues/<slug>/draft.html
   ```

   This opens the draft in the browser automatically.

5. **Review gate.** Show the user the draft and wait for explicit approval.
   Never proceed to sending without it. If they request changes, go back to
   step 2 and re-run steps 3–4 as needed (skip step 3 if the image itself
   doesn't need to change).

6. **Send.** Only after approval, run:

   ```bash
   python -m tools.send_email .tmp/issues/<slug>/content.json .tmp/issues/<slug>/image.png
   ```

   This sends to belbel.bella00@gmail.com by default (the `--to` flag exists
   but there is no distribution list yet — every issue currently goes to this
   single test address).

## One-time setup (before the first issue ever sent)
- `pip install -r requirements.txt`
- `python -m tools.send_email --setup` (opens a browser for Gmail OAuth consent,
  writes `token.json`)

## Notes / learnings
(Add anything discovered here as the system is used — rate-limit quirks, Gmail
API errors, template rendering issues, etc.)

- The header uses a CSS text wordmark, not an image logo (see the header
  comment in `templates/newsletter_template.html`). The original logo SVG,
  the extracted PNG, and the one-time extraction tool were removed once it
  was confirmed nothing needed them — if an image logo is ever wanted again,
  it'll need to be re-added from scratch.

- First real issue ("Bend the method, not the mission") drew stakeholder
  feedback that the first research draft read too academic — full paragraphs
  describing each study's methodology, with sources going back to 1999. The
  research-section rules above (2010+ sources, cite in a light embedded
  clause, insight leads) were added directly in response and now apply to
  every issue going forward, not just that one.

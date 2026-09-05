---
name: creating-newsletter-issue
description: Use when creating a new Soft Strategy Weekly newsletter issue from a topic or belief, before researching, writing content.json, generating the hero image, building the draft, or sending.
---

# Creating a Newsletter Issue

## Overview

This project's full newsletter creation process lives in
`workflows/create_newsletter_issue.md` — read it and follow it exactly. This
skill exists so that process is found automatically, and so two rules that
aren't written down anywhere else get applied every time.

## Follow the workflow doc

**REQUIRED:** Read `workflows/create_newsletter_issue.md` before doing
anything else. It has the full 5-part structure, the brand voice guide, the
`content.json` schema, and the exact CLI commands. Don't improvise a
different process — this repo follows a Workflows/Agents/Tools split (see
`WAT Claude.md`) specifically so the process stays consistent across runs.

## Two rules worth restating here

**Verify every citation is real before using it.** Web-search summaries
sometimes surface specific-sounding but unverifiable citations — a lab that
doesn't exist, a meta-analysis with a suspiciously round participant count.
Cross-check each study (author, year, actual finding) with an independent
search before citing it. If you can't confirm it's real, drop it and find a
different one. Never invent or embellish a citation to hit the "3 points, 2
quantitative" minimum from the workflow doc.

**Never send without explicit approval.** Build the draft, show the user the
file path (or open it), and wait for them to say it's good — every time, no
exceptions, even if a topic or draft looks obviously fine.

## Environment note

Use `python3`, not `python` — this machine doesn't have a bare `python` on
PATH. The workflow doc's example commands say `python`; substitute `python3`
when actually running them.

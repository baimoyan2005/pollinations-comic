# Pollinations Comic

[![Made with pollinations.ai](https://raw.githubusercontent.com/pollinations/pollinations/main/packages/ui/src/brand/badge-made-with.svg)](https://pollinations.ai/?ref=badge)

An [Agent Skill](https://agentskills.io) that turns any story, joke or idea into a **one-page printable comic**, using Pollinations models paid from the user's own Pollen balance.

Built for Pollinations quest [#20020 - An agent skill that makes something creative with Pollinations](https://github.com/pollinations/pollinations/issues/20020). The App URL is intentionally empty, as the quest requires: the deliverable is the skill in this repository.

## What it does

Give it a story. It writes a short panel plan, generates one illustration per panel with a Pollinations image model, adds dialogue and captions, and assembles everything into a single self-contained `comic.html`. The file base64-embeds the images, so it opens and prints offline with no server and no network.

The sign-in uses the official `polli` CLI device flow (`polli auth login`). The user approves a key for their own Pollen; this skill never asks for a pasted `sk_` key and never writes a key to a file.

## Files

| Path | Purpose |
| --- | --- |
| `SKILL.md` | The Agent Skill itself - instructions the agent follows |
| `scripts/build_comic.py` | Builds one offline, printable HTML comic from panel images + text |
| `examples/story.json` | Sample 4-panel story with inline placeholder art |
| `examples/sandwich-heist.html` | Fully assembled, offline comic - opens with no key and no network |
| `examples/screenshot.png` | Screenshot of that rendered comic (real output, not a mockup) |

## Zero-cost verification

Open `examples/sandwich-heist.html` directly in a browser. It uses tiny embedded placeholder images, so **review costs no Pollen and needs no API key**. It demonstrates the full layout: panel grid, speech bubbles, captions, panel numbers, title, print CSS and the Pollinations badge.

## Models

Every default used by the skill is `paid_only: false` in the live catalog at https://gen.pollinations.ai/models (checked 2026-11-20):

| Model | Endpoint | Use |
| --- | --- | --- |
| `openai/gpt-5.4-nano` | `/v1/chat/completions` | panel plan / script |
| `black-forest-labs/flux.1-schnell` | `/image` | panel art (fast, free) |
| `openai/tts-1` | audio | optional read-aloud button |

The skill re-checks the live catalog before spending and confirms the panel count with the user first.

## Install the skill

Copy `SKILL.md` (and the `scripts/`, `examples/` folders) into your agent's skills directory, e.g.:

```bash
# Claude Code
cp -r pollinations-comic ~/.claude/skills/

# WorkBuddy
cp -r pollinations-comic ~/.workbuddy/skills/
```

Then ask your agent: "make a comic about ..."

## Credit

Made with [pollinations.ai](https://pollinations.ai/?ref=badge). Text, image and speech all through one API, paid from your own balance.

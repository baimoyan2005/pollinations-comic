---
name: pollinations-comic
description: Turn any story, joke, idea or memory into a one-page printable comic. Use when a user wants a comic strip, sequential art, a visual story, or a shareable illustrated scene. Generates panel art and character speech with Pollinations image, text and speech models, then assembles a self-contained offline HTML comic the user can open and print. Runs on the user's own Pollinations balance via the official polli CLI.
---

# Pollinations Comic

Turn a story into a single, printable comic page — panel by panel — using Pollinations models, paid from the user's own Pollen balance.

The output is one self-contained `comic.html` with embedded images and text. It opens offline, prints on one page, and needs no server.

## When to use

- "Make a comic about my cat stealing a sandwich"
- "Turn this joke into a comic strip"
- "Draw a 4-panel story about a robot's first day"
- Any request for sequential art, a comic, a manga-style page, or a visual story.

## Principles

1. **Sign in with Pollinations, never ask for a pasted key.** Use the official `polli` CLI device flow. If the user is not signed in, run `polli auth login` and follow the printed instructions. Never ask the user to paste an `sk_` key into chat or a file.
2. **Check models before spending.** Read the live catalog at `https://gen.pollinations.ai/models` and confirm every model you use exists and has `paid_only: false`. Prefer free models so a review costs nothing. Tell the user which models and roughly how many images you will generate **before** you start.
3. **Ask before spending real Pollen.** Image generation spends the user's balance. Confirm the panel count and style with a short message first. The offline fixture (below) is free.
4. **Make it work offline.** After generating, base64-embed every image into the HTML so the comic opens with no network.
5. **Credit Pollinations.** Include the "Made with pollinations.ai" badge and link in the finished page.

## Free models (verify against the live catalog before use)

These were `paid_only: false` at time of writing — re-check `https://gen.pollinations.ai/models`:

- Text / script: `openai/gpt-5.4-nano`, `openai/gpt-6-luna`
- Image: `black-forest-labs/flux.1-schnell` (fast), `tongyi-mai/z-image-turbo`, `microsoft/mai-image-2.7-flash`
- Speech (optional sound button): `openai/tts-1`

## Workflow

### 1. Plan the page

Ask or infer: the story, the number of panels (3–6 works well on one page), the art style (e.g. "bold comic ink", "manga", "soft storybook"), and whether dialogue should be English.

Write a short panel plan: for each panel, one scene description and the exact dialogue/caption. Keep dialogue short — it must fit in a speech bubble.

### 2. Sign in

```bash
polli auth login
```

The CLI prints a verification URL and code. Ask the user to open it and approve. Do not handle or store the key yourself beyond what the CLI manages.

### 3. Generate each panel image

Use the CLI's image generation, or a direct call with the key the CLI provides. Example with the HTTP API:

```bash
curl -s -X GET "https://gen.pollinations.ai/image/$(python -c 'import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))' 'A cat in a superhero cape on a kitchen counter, bold comic ink, high contrast')" \
  -H "Authorization: Bearer $POLLINATIONS_API_KEY" \
  -o panel1.jpg
```

Or render a URL in a browser:
`https://gen.pollinations.ai/image/<encoded-prompt>?model=black-forest-labs/flux.1-schnell&width=1024&height=640`

Keep the **same style suffix** on every panel prompt so the art looks consistent. Describe composition, not dialogue (text is added in HTML).

### 4. Assemble the comic

Use `scripts/build_comic.py` to turn the panel images and panel text into one offline HTML file. It base64-embeds the images, lays out a responsive grid, and draws speech bubbles as HTML overlays.

```bash
python scripts/build_comic.py --story story.json --out comic.html
```

`story.json` format:

```json
{
  "title": "The Great Sandwich Heist",
  "style": "bold comic ink",
  "panels": [
    {
      "image": "panel1.jpg",
      "speech": "I have a plan.",
      "caption": "Elsewhere, a cat had a plan."
    }
  ]
}
```

### 5. Verify offline

Open `comic.html` with no network and confirm:
- every panel image renders,
- speech bubbles are readable,
- it fits a 375px viewport and prints on one page,
- the Pollinations badge is visible.

### 6. Zero-cost fixture for review

`examples/sandwich-heist.html` is a fully assembled comic using tiny embedded placeholder images. It needs no API key and no network. Reviewers can open it to check layout and credit without spending Pollen.

## Notes

- If image generation fails, fall back to `examples/` placeholders and tell the user which panels need regenerating.
- Never place a raw API key inside the generated HTML or any committed file.
- Keep dialogue text short; long text overflows speech bubbles.

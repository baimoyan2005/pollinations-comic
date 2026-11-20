#!/usr/bin/env python3
"""Build a single, self-contained, printable comic HTML from panel images + text.

Usage:
    python build_comic.py --story story.json --out comic.html

The story JSON:
{
  "title": "The Great Sandwich Heist",
  "style": "bold comic ink",
  "panels": [
    {"image": "panel1.jpg", "speech": "I have a plan.", "caption": "Elsewhere..."}
  ]
}
Images are base64-embedded, so the output opens and prints with no network.
No API keys are read or written by this script.
"""
import argparse
import base64
import html
import json
import mimetypes
import os
import sys


def embed(path):
    """Return a data: URL for a local image file or an inline data:/http URL."""
    if not path:
        return ""
    if path.startswith("data:") or path.startswith("http://") or path.startswith("https://"):
        return path
    if not os.path.isfile(path):
        return ""
    with open(path, "rb") as f:
        data = f.read()
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    return "data:{};base64,{}".format(mime, base64.b64encode(data).decode("ascii"))


def panel_html(panel, index):
    src = embed(panel.get("image", ""))
    speech = html.escape(str(panel.get("speech", "")))
    caption = html.escape(str(panel.get("caption", "")))
    img = ('<img src="{}" alt="panel {}">'.format(src, index + 1)
           if src else '<div class="placeholder">Panel {}<small>image missing</small></div>'.format(index + 1))
    bubble = '<div class="bubble">{}</div>'.format(speech) if speech else ""
    cap = '<div class="caption">{}</div>'.format(caption) if caption else ""
    return """
    <figure class="panel">
      <div class="frame">{img}{bubble}</div>
      {cap}
      <span class="num">{n}</span>
    </figure>""".format(img=img, bubble=bubble, cap=cap, n=index + 1)


CSS = """
:root{--ink:#161b22;--paper:#fffdf7;--accent:#e4572e;--line:#161b22}
*{box-sizing:border-box}
body{margin:0;background:#e9edf2;color:var(--ink);
  font-family:Comic Sans MS,"Segoe UI",system-ui,sans-serif;padding:24px}
.page{max-width:900px;margin:0 auto;background:var(--paper);
  box-shadow:0 20px 60px rgba(0,0,0,.18);padding:26px 26px 34px;border-radius:4px}
header{display:flex;align-items:baseline;justify-content:space-between;
  gap:12px;border-bottom:4px solid var(--line);padding-bottom:10px;margin-bottom:18px;flex-wrap:wrap}
h1{font-size:clamp(22px,4vw,38px);margin:0;letter-spacing:-.5px}
.style-tag{font-size:12px;color:#6b7280;font-weight:bold;text-transform:uppercase;letter-spacing:1px}
.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.panel{margin:0;position:relative}
.frame{position:relative;border:3px solid var(--line);border-radius:6px;overflow:hidden;
  aspect-ratio:16/10;background:#f2f2ee}
.frame img{width:100%;height:100%;object-fit:cover;display:block}
.placeholder{width:100%;height:100%;display:flex;flex-direction:column;align-items:center;
  justify-content:center;color:#9aa0aa;font-weight:bold;gap:4px}
.placeholder small{font-weight:normal}
.bubble{position:absolute;left:8%;top:8%;max-width:80%;background:#fff;border:3px solid var(--line);
  border-radius:50%;padding:12px 16px;font-size:clamp(12px,2vw,17px);line-height:1.25;
  text-align:center;box-shadow:2px 3px 0 rgba(0,0,0,.12)}
.caption{margin-top:6px;font-size:13px;color:#4b5563;font-style:italic;line-height:1.4}
.num{position:absolute;right:-6px;top:-6px;width:26px;height:26px;border-radius:50%;
  background:var(--accent);color:#fff;font-weight:bold;font-size:14px;display:grid;place-items:center;
  border:2px solid #fff}
footer{margin-top:20px;padding-top:12px;border-top:2px dashed #d1d5db;text-align:center;
  font-size:12px;color:#6b7280}
footer a{color:var(--accent);text-decoration:none;font-weight:bold}
@media(max-width:560px){.grid{grid-template-columns:1fr}}
@media print{body{background:#fff;padding:0}.page{box-shadow:none;max-width:none}
  .grid{grid-template-columns:repeat(2,1fr)}.panel{break-inside:avoid}}
"""


def build(story):
    title = html.escape(str(story.get("title", "Untitled Comic")))
    style = html.escape(str(story.get("style", "comic")))
    panels = story.get("panels", [])
    if not panels:
        print("story.json has no panels", file=sys.stderr)
        sys.exit(2)
    body = "".join(panel_html(p, i) for i, p in enumerate(panels))
    return """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{css}</style></head><body>
<main class="page">
<header><h1>{title}</h1><span class="style-tag">{style}</span></header>
<section class="grid">{body}</section>
<footer>Made with <a href="https://pollinations.ai/?ref=badge">pollinations.ai</a> &middot; a Pollinations Comic</footer>
</main></body></html>""".format(title=title, style=style, css=CSS, body=body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--story", required=True, help="path to story.json")
    ap.add_argument("--out", required=True, help="output HTML path")
    args = ap.parse_args()
    with open(args.story, encoding="utf-8") as f:
        story = json.load(f)
    result = build(story)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(result)
    print("Wrote {} ({} bytes, {} panels)".format(args.out, len(result), len(story.get("panels", []))))


if __name__ == "__main__":
    main()

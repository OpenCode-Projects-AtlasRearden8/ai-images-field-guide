#!/usr/bin/env python3
"""Build the Field Guide to Making Images with AI static site.

Converts docs/*.md into a small, polished static website (site/).
Standard library only: no keys, no network, no dependencies.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent
DEFAULT_DOCS_DIR = REPO_ROOT / "docs"
DEFAULT_OUT_DIR = REPO_ROOT / "site"

SITE_TITLE = "The Field Guide to Making Images with AI"
SITE_TAGLINE = "Written like a friend would explain it: plain English, step by step, never condescending."
FOOTER_CREDIT = "Part of The Massive AI Manual \u00b7 by Asdale Dynamics, LLC \u00b7 MIT License"

# Hand-written one-line blurbs for the index; falls back to the first
# paragraph of the chapter when a file has no entry here.
BLURBS = {
    "00-start-here.md": "Who this guide is for, how to read it, and the five habits that make everything else click.",
    "01-image-tools-vs-chat.md": "Why image tools are a camera in a box, not a chat buddy \u2014 and what that changes for you.",
    "02-prompt-patterns-styles.md": "Fill-in-the-blanks patterns and before/after cards that turn vague wishes into plans.",
    "03-prompt-patterns-edits.md": "img2img, inpainting, outpainting: change one thing at a time and keep what works.",
    "04-upscale-and-cleanup.md": "Fix content first, upscale last, crop with intent, and name your files like an adult.",
    "05-honest-limits.md": "Hands, text, mirrors, crowds: where image tools break, and the workarounds that help.",
    "06-copyright-and-watermarks.md": "Who owns what you generate, and the watermark rules that keep you out of trouble.",
    "07-never-fake-real-people.md": "The zero-tolerance zone, the share test, and why labels protect your credibility.",
    "08-family-photo-respect.md": "Consent first, know where photos travel, label the art, protect the kids.",
    "09-printing-habits.md": "The 300-DPI math, margins and bleed, and a test-print ritual that saves money.",
    "10-tool-safety-checklist.md": "The whole guide compressed into checkboxes you can tape near your desk.",
    "11-glossary.md": "Plain-English definitions for every term this guide throws around.",
}

CALLOUT_CLASSES = {
    "card": "prompt-card",
    "caution": "callout callout-caution",
    "tip": "callout callout-tip",
}


# ---------------------------------------------------------------------------
# Inline rendering
# ---------------------------------------------------------------------------

def escape_html(text: str) -> str:
    return html.escape(text, quote=True)


def render_inline(text: str) -> str:
    """Render inline markdown (code, links, bold, italic) to safe HTML."""
    # Split on inline code first so its content is rendered verbatim.
    parts = re.split(r"(`[^`]+`)", text)
    out: List[str] = []
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) > 1:
            out.append("<code>" + escape_html(part[1:-1]) + "</code>")
        else:
            out.append(_render_inline_plain(part))
    return "".join(out)


def _render_inline_plain(text: str) -> str:
    text = escape_html(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", _link_repl, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", text)
    return text


def _link_repl(match: re.Match) -> str:
    label = match.group(1)
    url = match.group(2)
    if url.startswith("http://") or url.startswith("https://"):
        return f'<a href="{url}" rel="noopener">{label}</a>'
    return f'<a href="{url}">{label}</a>'


# ---------------------------------------------------------------------------
# Block rendering
# ---------------------------------------------------------------------------

_RE_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_RE_UL_ITEM = re.compile(r"^[-*]\s+(.*)$")
_RE_CHECKBOX = re.compile(r"^-\s+\[([ xX])\]\s+(.*)$")
_RE_OL_ITEM = re.compile(r"^\d+\.\s+(.*)$")
_RE_QUOTE = re.compile(r"^>\s?(.*)$")
_RE_CONTAINER_OPEN = re.compile(r"^:::([a-zA-Z-]+)\s*$")
_RE_TABLE_SEP = re.compile(r"^\|?[\s:|-]+\|?\s*$")


def render_blocks(markdown: str) -> str:
    """Render a markdown string (the supported subset) to HTML blocks."""
    lines = markdown.split("\n")
    out: List[str] = []
    i = 0
    n = len(lines)

    def collect_until(stop_pred, start: int) -> Tuple[List[str], int]:
        collected: List[str] = []
        j = start
        while j < n and not stop_pred(lines[j]):
            collected.append(lines[j])
            j += 1
        return collected, j

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # Fenced containers: :::card / :::caution / :::tip ... :::
        container = _RE_CONTAINER_OPEN.match(stripped)
        if container:
            name = container.group(1).lower()
            body, i = collect_until(lambda l: l.strip() == ":::", i + 1)
            if i >= n:
                raise ValueError(f"Unclosed ::: container '{name}'")
            i += 1  # consume closing :::
            css = CALLOUT_CLASSES.get(name, "callout")
            inner = render_blocks("\n".join(body))
            label = _callout_label(name)
            content = f"<p class=\"callout-label\">{escape_html(label)}</p>{inner}" if label else inner
            out.append(f'<div class="{css}">{content}</div>')
            continue

        # Fenced code blocks
        if stripped.startswith("```"):
            code_lines, i = collect_until(lambda l: l.strip().startswith("```"), i + 1)
            if i >= n:
                raise ValueError("Unclosed ``` code fence")
            i += 1
            out.append("<pre><code>" + escape_html("\n".join(code_lines)) + "</code></pre>")
            continue

        heading = _RE_HEADING.match(stripped)
        if heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{render_inline(heading.group(2).strip())}</h{level}>")
            i += 1
            continue

        if stripped in ("---", "***", "___"):
            out.append("<hr>")
            i += 1
            continue

        # Tables: consecutive lines starting with '|'
        if stripped.startswith("|"):
            table_lines, i = collect_until(lambda l: not l.strip().startswith("|"), i)
            out.append(_render_table(table_lines))
            continue

        # Blockquotes (may span multiple lines, may contain bare '>' lines)
        if stripped.startswith(">"):
            quote_lines = []
            j = i
            while j < n and lines[j].strip().startswith(">"):
                quote_lines.append(_RE_QUOTE.match(lines[j].strip()).group(1))
                j += 1
            i = j
            inner = render_blocks("\n".join(quote_lines))
            out.append(f"<blockquote>{inner}</blockquote>")
            continue

        # Lists (unordered incl. checkboxes, ordered)
        if stripped.startswith("- ") or stripped.startswith("* ") or re.match(r"^\d+\.\s", stripped):
            items: List[str] = []
            ordered = bool(re.match(r"^\d+\.\s", stripped))
            checkboxes = False
            j = i
            while j < n:
                item_line = lines[j].strip()
                cb = _RE_CHECKBOX.match(item_line)
                if cb:
                    checkboxes = True
                    checked = " checked" if cb.group(1).lower() == "x" else ""
                    items.append(
                        f'<li><input type="checkbox" disabled{checked}> '
                        f"<span>{render_inline(cb.group(2))}</span></li>"
                    )
                elif ordered and _RE_OL_ITEM.match(item_line):
                    items.append("<li>" + render_inline(_RE_OL_ITEM.match(item_line).group(1)) + "</li>")
                elif not ordered and _RE_UL_ITEM.match(item_line):
                    items.append("<li>" + render_inline(_RE_UL_ITEM.match(item_line).group(1)) + "</li>")
                else:
                    break
                j += 1
            i = j
            tag = "ol" if ordered else "ul"
            cls = ' class="checklist"' if checkboxes and not ordered else ""
            out.append(f"<{tag}{cls}>{''.join(items)}</{tag}>")
            continue

        # Paragraph: gather until a blank line or a new block start.
        para_lines = [stripped]
        j = i + 1
        while j < n:
            nxt = lines[j].strip()
            if (not nxt or nxt.startswith("|") or nxt.startswith(">") or nxt.startswith("```")
                    or nxt.startswith(":::") or nxt.startswith("#") or _RE_UL_ITEM.match(nxt)
                    or _RE_OL_ITEM.match(nxt) or nxt in ("---", "***", "___")):
                break
            para_lines.append(nxt)
            j += 1
        i = j
        out.append("<p>" + render_inline(" ".join(para_lines)) + "</p>")

    return "\n".join(out)


def _callout_label(name: str) -> str:
    return {"caution": "Caution", "tip": "Tip"}.get(name, "")


def _render_table(table_lines: List[str]) -> str:
    rows = []
    for raw in table_lines:
        line = raw.strip().strip("|")
        cells = [c.strip() for c in line.split("|")]
        rows.append(cells)
    if len(rows) < 2:
        # Not a real table; treat as a paragraph-ish fallback.
        return "<p>" + render_inline(" ".join(table_lines)) + "</p>"
    header = rows[0]
    # Second line is the |---|---| separator; drop it from the body.
    body_rows = rows[2:] if len(table_lines) > 1 and _RE_TABLE_SEP.match(table_lines[1].strip()) else rows[1:]
    thead = "<tr>" + "".join(f"<th>{render_inline(c)}</th>" for c in header) + "</tr>"
    tbody = "".join(
        "<tr>" + "".join(f"<td>{render_inline(c)}</td>" for c in row) + "</tr>"
        for row in body_rows
    )
    return f"<table><thead>{thead}</thead><tbody>{tbody}</tbody></table>"


# ---------------------------------------------------------------------------
# Document handling
# ---------------------------------------------------------------------------

def doc_title(markdown: str, fallback: str) -> str:
    for line in markdown.split("\n"):
        m = _RE_HEADING.match(line.strip())
        if m:
            return re.sub(r"\*+", "", m.group(2)).strip()
    return fallback


def first_paragraph(markdown: str, limit: int = 200) -> str:
    for para in markdown.split("\n\n")[1:]:
        text = para.strip().replace("\n", " ")
        if text and not text.startswith(("#", ">", "|", ":::", "```", "- ", "1.")):
            plain = re.sub(r"\*+", "", re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text))
            return (plain[: limit - 3] + "\u2026") if len(plain) > limit else plain
    return ""


def slug_for(path: Path) -> str:
    return path.stem


def load_documents(docs_dir: Path) -> List[dict]:
    docs = []
    for path in sorted(docs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            raise ValueError(f"Empty document: {path.name}")
        title = doc_title(text, fallback=path.stem)
        if not _RE_HEADING.match(text.strip().split("\n")[0]):
            raise ValueError(f"{path.name} must start with an H1 title")
        docs.append({
            "slug": slug_for(path),
            "file": path.name,
            "title": title,
            "blurb": BLURBS.get(path.name) or first_paragraph(text),
            "markdown": text,
        })
    if not docs:
        raise ValueError(f"No markdown files found in {docs_dir}")
    return docs


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{meta_description}">
<title>{page_title} \u00b7 {site_title}</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="site-title" href="index.html">{site_title}</a>
    <p class="site-tagline">{site_tagline}</p>
  </div>
</header>
<nav class="chapter-nav" aria-label="Chapter navigation">
  <div class="wrap">
    <span class="chapter-count">Chapter {chapter_number} of {total_chapters}</span>
    <div class="nav-links">
      <a href="index.html">\u2190 Contents</a>
      {prev_link}
      {next_link}
    </div>
  </div>
</nav>
<main class="wrap">
<article>
{body}
</article>
<nav class="pager">
  {prev_page}
  {next_page}
</nav>
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>{footer_credit}</p>
    <p><a href="index.html">All chapters</a> \u00b7 Generated locally by <code>build.py</code> \u2014 no keys, no network.</p>
  </div>
</footer>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{meta_description}">
<title>{site_title}</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="site-header hero">
  <div class="wrap">
    <h1 class="site-title">{site_title}</h1>
    <p class="site-tagline">{site_tagline}</p>
    <p class="hero-note">{hero_note}</p>
  </div>
</header>
<main class="wrap">
<h2 class="contents-title">Contents</h2>
<ol class="chapter-grid">
{chapter_cards}
</ol>
<section class="home-note">
{home_note}
</section>
</main>
<footer class="site-footer">
  <div class="wrap">
    <p>{footer_credit}</p>
    <p>Generated locally by <code>build.py</code> \u2014 no keys, no network. Licensed MIT.</p>
  </div>
</footer>
</body>
</html>
"""


def pager_html(docs: List[dict], index: int) -> Tuple[str, str, str, str]:
    prev_link = ""
    next_link = ""
    prev_page = ""
    next_page = ""
    if index > 0:
        prev = docs[index - 1]
        prev_link = f'<a href="{prev["slug"]}.html">\u2190 Prev</a>'
        prev_page = (
            f'<a class="pager-link prev" href="{prev["slug"]}.html">'
            f'<span class="pager-dir">\u2190 Previous</span>'
            f'<span class="pager-title">{escape_html(prev["title"])}</span></a>'
        )
    if index < len(docs) - 1:
        nxt = docs[index + 1]
        next_link = f'<a href="{nxt["slug"]}.html">Next \u2192</a>'
        next_page = (
            f'<a class="pager-link next" href="{nxt["slug"]}.html">'
            f'<span class="pager-dir">Next \u2192</span>'
            f'<span class="pager-title">{escape_html(nxt["title"])}</span></a>'
        )
    return prev_link, next_link, prev_page, next_page


# ---------------------------------------------------------------------------
# Site build
# ---------------------------------------------------------------------------

def validate_internal_links(docs: List[dict], built_html_by_slug: dict) -> List[str]:
    """Return a list of broken relative .html links across all built pages."""
    problems: List[str] = []
    known = {d["slug"] + ".html" for d in docs} | {"index.html", "styles.css"}
    href_re = re.compile(r'href="([^"]+)"')
    for slug, page_html in built_html_by_slug.items():
        for href in href_re.findall(page_html):
            if href.startswith(("http://", "https://", "#")):
                continue
            target = href.split("#")[0]
            if target and target not in known:
                problems.append(f"{slug}.html links to missing target: {href}")
    return problems


def build_site(docs_dir: Path, out_dir: Path, write: bool = True) -> dict:
    docs = load_documents(docs_dir)
    built: dict = {}
    total = len(docs)

    # Chapter pages
    for idx, doc in enumerate(docs):
        body_html = render_blocks(doc["markdown"])
        prev_link, next_link, prev_page, next_page = pager_html(docs, idx)
        page = PAGE_TEMPLATE.format(
            meta_description=escape_html(doc["blurb"]),
            page_title=escape_html(doc["title"]),
            site_title=escape_html(SITE_TITLE),
            site_tagline=escape_html(SITE_TAGLINE),
            chapter_number=idx + 1,
            total_chapters=total,
            prev_link=prev_link,
            next_link=next_link,
            prev_page=prev_page,
            next_page=next_page,
            body=body_html,
            footer_credit=escape_html(FOOTER_CREDIT),
        )
        built[doc["slug"]] = page

    # Index page
    cards = []
    for idx, doc in enumerate(docs):
        cards.append(
            f'<li><a class="chapter-card" href="{doc["slug"]}.html">'
            f'<span class="chapter-number">{idx + 1:02d}</span>'
            f'<span class="chapter-name">{escape_html(doc["title"])}</span>'
            f'<span class="chapter-blurb">{escape_html(doc["blurb"])}</span>'
            f"</a></li>"
        )
    home_note = render_blocks(
        "Everything here runs locally: no accounts, no API keys, no network. "
        "Start with [Start Here](00-start-here.html), or jump straight to the "
        "[tool-safety checklist](10-tool-safety-checklist.html) if you already have a tool you like."
    )
    index_html = INDEX_TEMPLATE.format(
        meta_description=escape_html(SITE_TAGLINE),
        site_title=escape_html(SITE_TITLE),
        site_tagline=escape_html(SITE_TAGLINE),
        hero_note="A beginner's manual on making images with AI \u00b7 12 short chapters",
        chapter_cards="\n".join(cards),
        home_note=home_note,
        footer_credit=escape_html(FOOTER_CREDIT),
    )
    built_index_key = "index"
    built[built_index_key] = index_html

    # Validation
    problems: List[str] = []
    chapter_built = {k: v for k, v in built.items() if k != built_index_key}
    problems += validate_internal_links(docs, chapter_built)
    problems += validate_internal_links(
        docs, {"index": index_html}  # index links use same known set
    )
    for doc in docs:
        page_html = chapter_built[doc["slug"]]
        if "<script" in page_html.lower():
            problems.append(f"{doc['slug']}.html contains unescaped script tag")
        if doc["title"] not in page_html:
            problems.append(f"{doc['slug']}.html missing its title")

    if write:
        out_dir.mkdir(parents=True, exist_ok=True)
        for slug, page_html in built.items():
            (out_dir / f"{slug}.html").write_text(page_html, encoding="utf-8")
        (out_dir / "styles.css").write_text(STYLES_CSS, encoding="utf-8")

    return {
        "docs": docs,
        "pages": sorted(built.keys()),
        "problems": problems,
        "out_dir": out_dir,
        "written": write,
    }


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

STYLES_CSS = """/* The Field Guide to Making Images with AI - generated by build.py */
:root {
  --bg: #faf6f0;
  --ink: #2c2a26;
  --muted: #6f6a60;
  --accent: #b3541e;
  --accent-soft: #f4e3d3;
  --card-bg: #fffdf9;
  --line: #e5ddcf;
  --caution-bg: #fdf0e5;
  --caution-line: #c96a2e;
  --tip-bg: #eef4ec;
  --tip-line: #5d7d54;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Georgia, "Times New Roman", serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.65;
}
.wrap { max-width: 46rem; margin: 0 auto; padding: 0 1.25rem; }
a { color: var(--accent); }
a:hover { text-decoration-thickness: 2px; }

.site-header { border-bottom: 3px double var(--line); background: var(--card-bg); }
.site-header.hero { text-align: center; padding: 2.5rem 0 2rem; }
.site-title {
  font-size: 1.05rem; font-weight: bold; text-decoration: none;
  color: var(--ink); letter-spacing: 0.02em;
}
.site-header.hero .site-title {
  display: block; font-size: 2rem; text-decoration: none; margin-bottom: 0.25rem;
}
.site-tagline { color: var(--muted); font-style: italic; margin: 0.2rem 0 0; }
.hero-note { color: var(--muted); font-size: 0.95rem; margin-top: 0.4rem; }

.chapter-nav { background: var(--accent-soft); border-bottom: 1px solid var(--line); }
.chapter-nav .wrap {
  display: flex; flex-wrap: wrap; gap: 0.75rem; align-items: center;
  justify-content: space-between; padding-top: 0.5rem; padding-bottom: 0.5rem;
}
.chapter-count { font-size: 0.8rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; }
.nav-links { display: flex; gap: 1rem; font-size: 0.92rem; }
.nav-links a { text-decoration: none; }

main { padding: 2rem 1.25rem 3rem; }
article h1 { font-size: 2rem; line-height: 1.25; margin: 0 0 1.25rem; }
article h2 { font-size: 1.35rem; margin: 2.2rem 0 0.7rem; border-bottom: 1px solid var(--line); padding-bottom: 0.25rem; }
article h3 { font-size: 1.1rem; margin: 1.6rem 0 0.5rem; }
article p { margin: 0.8rem 0; }
article ol, article ul { padding-left: 1.4rem; }
article li { margin: 0.35rem 0; }

blockquote {
  margin: 1rem 0; padding: 0.6rem 1rem;
  border-left: 4px solid var(--line); background: var(--card-bg);
  color: var(--muted); font-style: italic;
}
blockquote p { margin: 0.3rem 0; }

code {
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
  font-size: 0.88em; background: #f1ebe1; padding: 0.1em 0.35em; border-radius: 4px;
}
pre { background: #f1ebe1; padding: 0.9rem 1rem; border-radius: 8px; overflow-x: auto; }
pre code { background: none; padding: 0; }

table { border-collapse: collapse; width: 100%; margin: 1.1rem 0; font-size: 0.95rem; }
th, td { border: 1px solid var(--line); padding: 0.45rem 0.7rem; text-align: left; }
th { background: var(--accent-soft); }
tbody tr:nth-child(even) { background: var(--card-bg); }

.callout-label {
  font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em;
  margin: 0 0 0.35rem; font-weight: bold; font-style: normal;
}
.callout, .prompt-card {
  margin: 1.3rem 0; padding: 0.9rem 1.1rem; border-radius: 10px;
  border: 1px solid var(--line); background: var(--card-bg);
}
.prompt-card { border-left: 5px solid var(--accent); }
.prompt-card blockquote { background: #f6efe3; color: var(--ink); }
.callout-caution { border-left: 5px solid var(--caution-line); background: var(--caution-bg); }
.callout-caution .callout-label { color: var(--caution-line); }
.callout-tip { border-left: 5px solid var(--tip-line); background: var(--tip-bg); }
.callout-tip .callout-label { color: var(--tip-line); }

.checklist { list-style: none; padding-left: 0; }
.checklist li {
  padding: 0.45rem 0.6rem 0.45rem 2.2rem; position: relative;
  background: var(--card-bg); border: 1px solid var(--line); border-radius: 8px; margin: 0.45rem 0;
}
.checklist input[type="checkbox"] { position: absolute; left: 0.6rem; top: 0.75rem; accent-color: var(--accent); }

.pager { display: flex; gap: 1rem; margin-top: 2.5rem; flex-wrap: wrap; }
.pager-link {
  flex: 1 1 14rem; text-decoration: none; border: 1px solid var(--line);
  background: var(--card-bg); border-radius: 10px; padding: 0.7rem 1rem;
  display: flex; flex-direction: column; gap: 0.15rem;
}
.pager-link.next { text-align: right; margin-left: auto; }
.pager-dir { font-size: 0.78rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }
.pager-title { color: var(--ink); font-weight: bold; }

.contents-title { margin-bottom: 1rem; }
.chapter-grid { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.8rem; counter-reset: none; }
.chapter-card {
  display: flex; flex-direction: column; gap: 0.2rem; text-decoration: none;
  background: var(--card-bg); border: 1px solid var(--line); border-left: 5px solid var(--accent);
  border-radius: 10px; padding: 0.85rem 1.1rem;
}
.chapter-card:hover { background: var(--accent-soft); }
.chapter-number { font-size: 0.8rem; color: var(--muted); letter-spacing: 0.08em; }
.chapter-name { font-weight: bold; color: var(--ink); font-size: 1.05rem; }
.chapter-blurb { color: var(--muted); font-size: 0.92rem; }
.home-note { margin-top: 2rem; color: var(--muted); font-size: 0.95rem; border-top: 1px solid var(--line); padding-top: 1rem; }

.site-footer { border-top: 3px double var(--line); background: var(--card-bg); padding: 1.2rem 0 1.6rem; font-size: 0.9rem; color: var(--muted); }
.site-footer p { margin: 0.2rem 0; }

@media print {
  body { background: #fff; }
  .chapter-nav, .pager, .site-footer { display: none; }
  main { padding: 0; }
}
@media (max-width: 600px) {
  article h1 { font-size: 1.6rem; }
  .nav-links { font-size: 0.85rem; }
}
"""


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Build the Field Guide static site.")
    parser.add_argument("--docs", type=Path, default=DEFAULT_DOCS_DIR, help="Directory of markdown chapters")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR, help="Output directory for the site")
    parser.add_argument("--check", action="store_true", help="Validate only; do not write files")
    args = parser.parse_args(argv)

    try:
        result = build_site(args.docs, args.out, write=not args.check)
    except ValueError as exc:
        print(f"build failed: {exc}", file=sys.stderr)
        return 1

    label = "validated" if args.check else "built"
    for slug in result["pages"]:
        print(f"  {label}: {slug}.html")
    if result["problems"]:
        for problem in result["problems"]:
            print(f"  PROBLEM: {problem}", file=sys.stderr)
        print(f"build failed with {len(result['problems'])} problem(s)", file=sys.stderr)
        return 1
    chapters = len(result["docs"])
    print(f"OK: {chapters} chapters, {len(result['pages'])} pages generated locally from {args.docs}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

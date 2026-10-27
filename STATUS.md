# STATUS.md — The Field Guide to Making Images with AI

**Project:** Beginner manual on making images with AI (Markdown source + static HTML site)
**Owner:** Asdale Dynamics, LLC
**Date completed:** October 27, 2026

## What was built

A complete, tested, zero-dependency beginner manual on making images with AI, written in the
plain, warm, never-condescending style of *The Massive AI Manual*.

**Content — 12 chapters in `docs/` (Markdown):**

1. **Start Here** — who it's for, the five core habits, quick chapter map
2. **How Image Tools Differ From Chat** — chat vs. image AI comparison table, five surprises, local vs. browser tools
3. **Prompt Patterns for Styles** — fill-in-the-blanks base pattern, 5 patterns, style bank table, before/after prompt cards
4. **Prompt Patterns for Edits** — img2img strength table, inpainting, outpainting, zoom-and-regenerate, before/after edit cards
5. **Upscaling and Cleanup** — source-first discipline, 5-step cleanup routine, upscale-strength table, face-change caution
6. **Honest Limits** — hands, text in images, crowds/mirrors, re-roll math (3–10 attempts is normal)
7. **Copyright and Watermark Cautions** — who owns what (check the terms), training-data honesty, watermark rules both ways, styles vs. living artists
8. **Never Fake Real People** — zero-tolerance zone, the share test, fictional-people labeling
9. **Family-Photo Respect** — consent every time, upload privacy, kids' extra protection, grief/memorial care, originals-vs-AI folder habit
10. **Good Printing Habits** — 300 DPI math table, margins/bleed, RGB-vs-CMYK honesty, test-print ritual, paper choices
11. **Tool-Safety Checklist** — 21 checkboxes across before-using/before-generating/before-editing/before-sharing/before-printing
12. **Glossary** — 19 plain-English terms

**Featured elements requested by the brief:** before/after prompt cards (7 across chapters 3–4, plus a rights decision card), a tool-safety checklist with real checkboxes, and a glossary. All present and verified in the built HTML.

**Code:**

- `build.py` — stdlib-only Python builder (no pip installs, no API keys, no network). Converts the Markdown subset used by the manual (headings, paragraphs, lists, real checkboxes, tables, blockquotes, code fences, `:::card`/`:::caution`/`:::tip` callouts) into a polished static site: `index.html` with chapter cards, one page per chapter with prev/next pager, `styles.css` (warm serif design, print stylesheet). Validates every page: escaped HTML, resolved internal links, present titles, balanced callouts. CLI flags: `--docs`, `--out`, `--check` (validate without writing).
- `tests/test_build.py` — 15 `unittest` tests covering page generation, index links, cards/callouts/checkboxes/tables rendering, HTML escaping (XSS), internal-link resolution, balanced containers, glossary terms, footer credit, exact LICENSE line, and CLI end-to-end (build exits 0; `--check` writes nothing).

## How to run it

```bash
python3 build.py                    # builds site/ (index.html + 12 chapter pages + styles.css)
python3 build.py --check            # validate only, write nothing
python3 -m unittest discover -s tests -v   # run the test suite
```

Then open `site/index.html` in any browser. Requires only Python 3.9+. No keys, no accounts, no network.

## Verification results

- `python3 build.py` → **OK: 12 chapters, 13 pages generated locally** (exit 0)
- `python3 build.py --check` → **validated, wrote nothing, exit 0**
- `python3 -m unittest discover -s tests` → **Ran 15 tests … OK** (after fixing one over-strict test assertion that flagged the *word* "checked" in prose rather than the attribute)
- HTML structure check (`html.parser` tag-balance scan of all 13 pages) → **ALL BALANCED**
- Internal-link check → every `href` in every page resolves to a built file
- Escaping check → no raw `<script>` possible; test injects a script tag and asserts escaping
- Secrets scan → no API keys, tokens, passwords, emails, or personal data anywhere in the repo
- LICENSE contains the exact required line: `Copyright (c) 2026 Asdale Dynamics, LLC`; README credits Asdale Dynamics, LLC

## Known gaps / honest notes

- **Static and offline by design:** no search, no analytics, no images in the manual itself — readers supply their own tool and see the tool's own UI. Chapter examples are deliberately tool-neutral since tool pricing/rules change often.
- **Markdown subset:** `build.py` supports what the manual uses (it is not a full CommonMark renderer). Unsupported syntax fails loudly rather than silently.
- **Legal content is education, not legal advice** — chapters 7–9 point to primary sources (tool terms, copyright office) instead of pretending to be counsel.
- Tool names are deliberately not named/compared in detail; a tool-comparison chapter would go stale quickly and is better maintained on the hub site.
- The site is gitignored (generated output); rebuild with one command.

## Git

Single plain commit on `main` containing the manual, builder, tests, LICENSE, README, STATUS.md. No remote was created, nothing was pushed or published.

# The Field Guide to Making Images with AI

A beginner-friendly manual on creating images with AI — written like a friend would explain it. Plain English, step by step, never condescending.

Written and published by **Asdale Dynamics, LLC** (Dylan Asdale) as part of *The Massive AI Manual* family of guides.

## What's in here

- **docs/** — the whole manual in Markdown, one readable chapter per file:
  - How image tools are different from chat
  - Prompt patterns for styles and edits (with before/after prompt cards)
  - Upscaling and cleanup steps
  - Honest limits: hands and text
  - Copyright, watermarks, and never faking real people
  - Family-photo respect
  - Good printing habits
  - A tool-safety checklist and a plain-English glossary
- **build.py** — a zero-dependency Python script that turns the Markdown into a polished static HTML site in `site/`
- **tests/test_build.py** — a `unittest` suite that verifies the build actually works

## How to run it

This is fully local. No API keys, no accounts, no internet needed after download.

```bash
# Build the static site
python3 build.py

# Run the tests
python3 -m unittest discover -s tests -v

# Read the site
# open site/index.html in any browser
```

Requires Python 3.9+ and nothing else.

## Honest by design

This manual will never help you fake a real person, steal someone's art style to pass off as your own, or print things you don't have rights to. The safety chapters are part of the manual, not an appendix.

## License

MIT — see [LICENSE](LICENSE).

Copyright (c) 2026 Asdale Dynamics, LLC

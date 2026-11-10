---
inclusion: always
---

# Docs

Five tutorial pages (walk through the code → build → wire and validate → flash → configure and test) plus an overview. The pin map lives on the wire Validate page.

Write for someone new to ESPHome: plain sentences, explain each YAML block before moving on, no internal jargon or phase numbers. Don't mention future plans or versions.

Shell steps use a `.run` block (command, then real output in a `{.no-copy}` block). Only show output you actually captured. If you can't capture it, describe what to look for in prose instead of inventing log lines.

Avoid `---` separators between sections; headings are enough.

```bash
.venv/bin/python -m zensical serve
```

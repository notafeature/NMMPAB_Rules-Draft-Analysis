#!/usr/bin/env python3
"""Point every stylesheet link at the current style.css, by content hash.

GitHub Pages caches each file for ten minutes, so a page and its stylesheet
can arrive from different deploys. Versioning the link (style.css?v=<hash>)
makes fresh HTML fetch matching CSS instead of reusing a stale copy.

Run after any edit to docs/style.css. With --check, changes nothing and
exits non-zero if any page's link does not match; tools/check-site.py
performs the same check.
"""
import glob, hashlib, os, re, sys

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

with open(os.path.join(DOCS, "style.css"), "rb") as f:
    want = hashlib.sha256(f.read()).hexdigest()[:8]

check = "--check" in sys.argv
stale = []
for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
    src = open(path).read()
    new = re.sub(r'href="style\.css[^"]*"', f'href="style.css?v={want}"', src)
    if new != src:
        stale.append(os.path.basename(path))
        if not check:
            open(path, "w").write(new)

if check and stale:
    print(f"stylesheet links out of date (style.css is at ?v={want}): " + ", ".join(stale))
    sys.exit(1)
print(f"style.css?v={want}: " + (f"{len(stale)} page(s) updated" if stale else "all links current"))

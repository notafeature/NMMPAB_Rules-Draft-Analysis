#!/usr/bin/env python3
"""One entry point for the site checks. Non-zero exit on any failure.

Covers every page in docs/: HTML parses, no nested anchors, no em dashes,
and the visit counter is present. For every page that is not a redirect
stub: the shared menu (<header class="topbar">) and its script are
byte-identical except for the aria-current marker, the menu links every
non-stub page, the no-JavaScript fallback is present, internal links
resolve, every page is reachable from another page, and prose carries no
live-blog tense ("today", "this morning", "this afternoon") outside
quoted material.
"""
import glob, hashlib, html.parser, os, re, sys

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
failures = []

with open(os.path.join(DOCS, "style.css"), "rb") as f:
    CSSV = hashlib.sha256(f.read()).hexdigest()[:8]

def fail(msg):
    failures.append(msg)
    print("FAIL " + msg)

navs = {}
navjs = {}
srcs = {}
for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
    name = os.path.basename(path)
    src = open(path).read()
    srcs[name] = src

    class P(html.parser.HTMLParser):
        def __init__(self):
            super().__init__(); self.stack = []; self.bad = []
        def handle_starttag(self, tag, attrs):
            if tag not in ("meta", "link", "br", "hr", "img", "input",
                           "line", "rect", "circle", "path", "text"):
                self.stack.append(tag)
        def handle_endtag(self, tag):
            if self.stack and self.stack[-1] == tag: self.stack.pop()
            elif tag in self.stack: self.bad.append(tag)
    p = P(); p.feed(src)
    if p.bad or p.stack:
        fail(f"{name}: parse {p.bad or p.stack}")
    for m in re.finditer(r"<a\b[^>]*>", src):
        close = src.find("</a>", m.end())
        if close != -1 and "<a " in src[m.end():close]:
            fail(f"{name}: nested anchor")
            break
    if chr(8212) in src:
        fail(f"{name}: {src.count(chr(8212))} em dash(es)")
    if 'id="countjs"' not in src:
        fail(f"{name}: visit counter missing")
    for m in re.finditer(r'href="style\.css([^"]*)"', src):
        if m.group(1) != f"?v={CSSV}":
            fail(f"{name}: stylesheet link {m.group(0)} does not match style.css "
                 f"at ?v={CSSV}; run tools/sync-css-version.py")

    if 'http-equiv="refresh"' in src:
        continue

    # shared chrome and its script, normalized for the current-page marker
    m = re.search(r'<header class="topbar">.*?</header>', src, re.S)
    if m:
        navs[name] = re.sub(r' aria-current="page"', "", m.group(0))
    else:
        fail(f"{name}: shared menu missing")
    m = re.search(r'<script id="navjs">.*?</script>', src, re.S)
    if m:
        navjs[name] = m.group(0)
    else:
        fail(f"{name}: menu script missing")
    if '<noscript><style>.tnav{display:flex}</style></noscript>' not in src:
        fail(f"{name}: no-JavaScript menu fallback missing")
    # live-blog tense outside verbatim blocks
    prose = re.sub(r'<div class="verbatim">.*?</div>', "", src, flags=re.S)
    prose = re.sub(r"<script.*?</script>", "", prose, flags=re.S)
    for word in ("this morning", "this afternoon", "meets today", "later today"):
        if word in prose.lower():
            fail(f"{name}: live-blog tense: '{word}'")
    # internal links resolve
    for href in set(re.findall(r'href="([^"]+)"', src)):
        if href.startswith(("http", "#", "mailto:")) or "'" in href or "+" in href:
            continue
        target = href.split("#")[0].split("?")[0]
        if target and not os.path.exists(os.path.join(DOCS, target)):
            fail(f"{name}: broken link {href}")

for label, blocks in (("chrome", navs), ("menu script", navjs)):
    if len(set(blocks.values())) > 1:
        byname = {}
        for k, v in blocks.items(): byname.setdefault(v, []).append(k)
        groups = " | ".join(",".join(v) for v in byname.values())
        fail(f"{label} differs between pages: {groups}")

# the shared menu links every page that is not a redirect stub
if navs:
    nav = next(iter(navs.values()))
    nav_hrefs = {h.split("#")[0] for h in re.findall(r'href="([^"]+)"', nav)}
    for n, s in srcs.items():
        if 'http-equiv="refresh"' not in s and n not in nav_hrefs:
            fail(f"{n}: not linked from the shared menu")

    # the Documents dropdown holds the register and the current PDFs, in a new tab
    if 'record.html#documents' not in nav:
        fail("menu: the All documents entry is missing")
    for pdf in ("documents/rules-draft-2026-07-23-published.pdf",
                "documents/NMMPAB-2026-07-17-board-transcript.pdf",
                "documents/NMMPAB-2026-07-17-committee-transcript.pdf",
                "documents/metz-recommendations-2026-07-17.pdf"):
        if f'href="{pdf}" target="_blank" rel="noopener"' not in nav:
            fail(f"menu: {pdf} is missing or does not open in a new tab")

# every page is reachable: linked by href from at least one other page.
# Redirect stubs are exempt; they are retired addresses, not destinations.
stubs = {n for n, s in srcs.items() if 'http-equiv="refresh"' in s}
linked = set()
for n, s in srcs.items():
    if n in stubs:
        continue
    for href in re.findall(r'href="([^"#?]+\.html)', s):
        if os.path.basename(href) != n:
            linked.add(os.path.basename(href))
for n in srcs:
    if n not in stubs and n not in linked:
        fail(f"{n}: reachable from no other page")

# every redirect stub's target holds the anchor it promises
for n in stubs:
    m = re.search(r'url=([^">]+)', srcs[n])
    if not m:
        fail(f"{n}: stub with no url=")
        continue
    target, _, frag = m.group(1).partition("#")
    if target not in srcs:
        fail(f"{n}: stub target {target} missing")
    elif frag and f'id="{frag}"' not in srcs[target]:
        fail(f"{n}: stub target {target} lacks anchor #{frag}")

if failures:
    print(f"\n{len(failures)} failure(s).")
    sys.exit(1)
print(f"checked {len(glob.glob(os.path.join(DOCS, '*.html')))} pages: clean.")

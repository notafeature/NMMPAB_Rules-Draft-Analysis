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

Three checks read from tools/sync-nav.py rather than carrying their own
copy of the same facts, so the menu, the page names, and this file cannot
drift apart:

- Every page's <title>, its H1, and its label in the shared menu say the
  same words. Each disagreement costs a reader a re-orientation on every
  navigation, and all three surfaces disagreed on most pages before the
  naming pass.
- Every document in the Documents dropdown has a row in the register at
  record.html#documents. The dropdown's membership contract is stated in
  sync-nav.DOCUMENTS_CONTRACT.
- Every id cited from another page exists on the page that is supposed to
  hold it. This generalizes the redirect-stub anchor check to every
  internal fragment link on the site.

A fourth reads tools/sync-record.py the same way: the chain, the register,
and the gaps register on record.html are generated from the data in that
file, and this check fails if the page has drifted from it. Importing the
module also runs its own validation, so a document a chain event attaches
but the register does not hold, or an absence a gap claims that its event
does not carry back, fails here as well.

A fifth reads tools/sync-pathways.py: the starting-license picker and the
five panels on pathways.html are written into the page from the data in
that file, and this check fails if the page has drifted from it.
"""
import glob, hashlib, html.parser, importlib.util, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(ROOT, "tools", filename))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


syncnav = _load("syncnav", "sync-nav.py")
syncrecord = _load("syncrecord", "sync-record.py")
syncpathways = _load("syncpathways", "sync-pathways.py")

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

    # the Documents dropdown carries what sync-nav.MENU_DOCUMENTS says it carries,
    # and every document in it opens in a new tab and has a register row
    register = ""
    m = re.search(r'<section id="documents">.*?</section>', srcs.get("record.html", ""), re.S)
    if m:
        register = m.group(0)
    else:
        fail("record.html: the document register at #documents is missing")
    for d in syncnav.MENU_DOCUMENTS:
        href = d["href"]
        if href.endswith(".html") or "#" in href:
            if f'href="{href}"' not in nav:
                fail(f"menu: the {d['label']} entry is missing")
            continue
        if f'href="{href}" target="_blank" rel="noopener"' not in nav:
            fail(f"menu: {href} is missing or does not open in a new tab")
        if register and href not in register:
            fail(f"menu: {href} is in the Documents dropdown with no register row "
                 "at record.html#documents")

# the chain, the register, and the gaps register match tools/sync-record.py
if syncrecord.stale():
    fail("record.html: the chain, the register, or the gaps register no longer matches "
         "tools/sync-record.py; run it without --check")

# the picker and the five starting-license panels match tools/sync-pathways.py
if syncpathways.stale():
    fail("pathways.html: the starting-license picker or the panels no longer match "
         "tools/sync-pathways.py; run it without --check")

# titles, headings, and menu labels say the same words
for page, name in syncnav.NAMES.items():
    src = srcs.get(page + ".html")
    if src is None:
        fail(f"sync-nav.NAMES lists {page}, which is not a page in docs/")
        continue
    want = f"{name} &middot; {syncnav.TITLE_SUFFIX}"
    norm = lambda t: t.strip().replace("&middot;", chr(183)).replace("&amp;", "&")
    m = re.search(r"<title>(.*?)</title>", src, re.S)
    if not m:
        fail(f"{page}.html: no <title>")
    elif norm(m.group(1)) != norm(want):
        fail(f"{page}.html: title reads {m.group(1).strip()!r}, "
             f"and the name in tools/sync-nav.py is {want!r}")
    m = re.search(r"<h1[^>]*>(.*?)</h1>", src, re.S)
    if not m:
        fail(f"{page}.html: no <h1>")
    elif norm(m.group(1)) != norm(name):
        fail(f"{page}.html: H1 reads {m.group(1).strip()!r}, "
             f"and the name in tools/sync-nav.py is {name!r}")
    if navs:
        m = re.search(rf'<a href="[^"]*"[^>]*data-nav="{re.escape(page)}"[^>]*>(.*?)<span class="sub">',
                      next(iter(navs.values())), re.S)
        if not m:
            fail(f"{page}.html: no entry in the shared menu")
        elif norm(m.group(1)) != norm(name):
            fail(f"{page}.html: menu label reads {m.group(1).strip()!r}, "
                 f"and the name in tools/sync-nav.py is {name!r}")

# every id cited from anywhere on the site exists on the page that holds it
ids = {n: set(re.findall(r'id="([^"]+)"', s)) for n, s in srcs.items()}
for n, s in srcs.items():
    body = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    for href in sorted(set(re.findall(r'href="([^"]+)"', body))):
        if href.startswith(("http", "mailto:")) or "'" in href or "+" in href:
            continue
        target, _, frag = href.partition("#")
        if not frag:
            continue
        page = os.path.basename(target) or n
        if page not in ids:
            continue          # a missing file is already reported as a broken link
        if frag not in ids[page]:
            fail(f"{n}: links {href}, and {page} has no id=\"{frag}\"")

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

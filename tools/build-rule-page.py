#!/usr/bin/env python3
"""Builds docs/rule.html from the plain-text extraction of the published rule.

The extraction lives in source-text/ and is produced with pypdf, one
"===== PAGE n =====" marker per page. When a new version of the rule is
published: extract it the same way, point SOURCE at the new file, update
DOC, DOCDATE, and the hero constants, review ANNOTATIONS, and run this
script. Every section and page anchor regenerates.

Line breaks inside the text are collapsed to single spaces and nothing
else is altered. Where the extraction is garbled, the linked PDF governs;
the page says so.

The chrome is not written here. The shared menu comes from tools/sync-nav.py,
imported below, so the menu on this page can never drift from the other
thirteen. After writing the page this script runs tools/sync-css-version.py,
tools/sync-count.py, and tools/sync-provenance.py, which stamp the versioned
stylesheet link, the visit-counter beacon, and the provenance block into the
fresh page, the same way they maintain every other page. The August 2026
refusal-to-run, which existed because this script once emitted the retired
<header class="top"> chrome, is retired with the chrome that caused it.
"""

import html
import importlib.util
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import partlib
PART = partlib.current_part()
partlib.load_data(PART, "build-rule-page", globals())
OUT = os.path.join(partlib.docs_dir(PART), "rule.html")

_spec = importlib.util.spec_from_file_location(
    "syncnav", os.path.join(ROOT, "tools", "sync-nav.py"))
syncnav = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(syncnav)
# The site-wide method page lives with Part 3 until it moves to the root; a
# Part's data may point the footer at it with ABOUT_HREF.
FOOT = f"""<footer class="foot"><div class="wrap">
<span>An independent community record of the rulemaking. Not affiliated with the New Mexico Department of Health.</span>
<span>Nothing here is final rule text, legal advice, or medical advice.</span>
<a href="{globals().get("ABOUT_HREF", "/about/")}">Sources and method</a>
<a href="comment.html">Report an error</a>
</div></footer>"""

def read_sections():
    raw = open(SOURCE).read()
    # index of every page marker
    pages = [(m.start(), int(m.group(1))) for m in re.finditer(r"===== PAGE (\d+) =====", raw)]
    def page_of(i):
        p = 1
        for start, n in pages:
            if start <= i: p = n
            else: break
        return p
    # find each section heading in sequence
    marks = []
    pos = 0
    for n in range(1, NSECTIONS + 1):
        # earlier published texts misnumbered some headings 7.34.3; accept both and record it
        last = PART.split(".")[-1]
        m = re.compile(rf"7\.3([45])\.{last}\.{n}\s+([A-Z][^a-z]*?):").search(raw, pos)
        if not m:
            raise SystemExit(f"section {PART}.{n} not found after offset {pos}")
        misprint = m.group(1) == "4"
        marks.append((n, m.start(), m.end(), re.sub(r"\s+", " ", m.group(2)).strip(), misprint))
        pos = m.end()
    sections = []
    for i, (n, start, bodystart, title, misprint) in enumerate(marks):
        end = marks[i + 1][1] if i + 1 < len(marks) else len(raw)
        body = raw[bodystart:end]
        body = re.sub(r"===== PAGE \d+ =====", "", body)
        sections.append({"n": n, "title": title, "page": page_of(start), "body": body,
                         "misprint": misprint})
    return sections

def read_definitions():
    """The program-side definitions from the amendments extraction, verbatim,
    each with the PDF page it sits on."""
    raw = open(AMEND_SOURCE).read()
    pages = [(m.start(), int(m.group(1))) for m in re.finditer(r"===== PAGE (\d+) =====", raw)]
    def page_of(i):
        p = 1
        for start, n in pages:
            if start <= i: p = n
            else: break
        return p
    flat = re.sub(r"===== PAGE \d+ =====", "", raw)
    # every definition start: “Term” means, “Term” or “alias” means, and the
    # struck standalone guide entry, whose bracket opens before the quote
    starts = [(m.start(), m.group(1)) for m in re.finditer(
        r"[“\"]([A-Z][^”\"]{1,60})[”\"](?:\s+or\s+[“\"][^”\"]+[”\"])?\s*(?:means|includes|is any|an individual)", flat)]
    bounds = {}
    for i, (pos, term) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(flat)
        # stop at a lettered group heading between this entry and the next
        m = re.search(r"\n\s+[A-Z]\.\s+Definitions beginning", flat[pos:end])
        if m: end = pos + m.start()
        bounds.setdefault(term.strip().lower(), (pos, end))
    # offsets into `flat` do not match `raw`; map by text position of the term
    out = []
    for term in DEF_TERMS:
        key = term.lower()
        if key not in bounds:
            raise SystemExit(f"definition {term!r} not found in the amendments extraction")
        pos, end = bounds[key]
        text = re.sub(r"\s+", " ", flat[pos:end]).strip()
        # the span runs to the next definition's start, which can leave that
        # entry's leading enumeration token behind; trim it
        text = re.sub(r"(?:\s*\[?\(\d+\)\]?)+\s*\.?\s*$", "", text).rstrip()
        if not text.endswith((".", "]", ";")):
            text += "."
        text = "“" + text
        # the guide entry sits inside a struck bracket that opens before the
        # quote; carry the bracket in so the strike renders
        if term == "Guide" and not text.startswith("["):
            open_b = flat.rfind("[", 0, pos)
            if open_b != -1 and flat.find("]", pos) < end + 40:
                text = "[" + text
        rawpos = raw.find(flat[pos:pos + 40])
        out.append({"term": term, "text": text,
                    "page": page_of(rawpos if rawpos != -1 else 0)})
    return out


def render_definition(d):
    t = html.escape(d["text"])
    t = re.sub(r"\[([^\]]+)\]", r"<s>\1</s>", t)
    t = re.sub(r"^““", "“", t)
    if d["term"] == "Guide":
        # the whole entry is struck; the opening bracket precedes the quote
        t = t.replace("“<s>", "<s>", 1)
    chipword = {"open": "Open", "settled": "Settled", "defect": "Defect", "blue": "Note"}
    notes = "\n".join(
        f"<div class='note {kind}'><span class='mark {kind}'>{chipword[kind]}</span> "
        f"<b>{html.escape(title)}.</b> {txt}</div>"
        for kind, title, txt in DEF_NOTES.get(d["term"], []))
    return (f"<div class='defentry' id='def-{d['term'].lower().replace(' ', '-')}'>"
            f"<div class='defhead'><span class='dterm'>{html.escape(d['term'])}</span>"
            f"<a class='pdf' href='{AMEND_DOC}#page={d['page']}' target='_blank' rel='noopener' "
            f"data-cite='Proposed amendments to 7.35.2 NMAC, August 25, 2026, page {d['page']}'>"
            f"PDF p. {d['page']}</a></div>"
            f"<p class='deftext'>{t}</p>{notes}</div>")


def render_defs_section():
    entries = "\n".join(render_definition(d) for d in read_definitions())
    return f"""
<section class="rsec" id="defs">
  <div class="rhead"><span class="rnum">7.35.2.7</span><h2 class="rtitle">The Definitions The Rule Runs On</h2>
  <a class="pdf" href="{AMEND_DOC}#page=1" target="_blank" rel="noopener" data-cite="Proposed amendments to 7.35.2 NMAC, August 25, 2026">PDF pp. 1-4</a></div>
  <p class="defslede">{DEFS_LEDE}</p>
  {entries}
</section>"""


def render_body(body):
    """Split on subsection letters at line starts; collapse whitespace inside."""
    lines = body.split("\n")
    paras, cur = [], []
    for ln in lines:
        if re.match(r"\s{0,4}[A-Z]\.\s+\S", ln) and cur:
            paras.append(" ".join(cur)); cur = [ln]
        else:
            cur.append(ln)
    if cur: paras.append(" ".join(cur))
    out = []
    for p in paras:
        p = re.sub(r"\s+", " ", p).strip()
        if not p: continue
        p = html.escape(p)
        p = re.sub(r"^([A-Z]\.)\s", r"<b>\1</b> ", p)
        p = re.sub(r"\[(7\.35\.\d+\.\d+ NMAC[^\]]*)\]", r"<span class='hist'>[\1]</span>", p)
        out.append(f"<p>{p}</p>")
    return "\n".join(out)


def main():
    sections = read_sections()
    toc, body = [], []
    for s in sections:
        n, title, page = s["n"], html.escape(s["title"]), s["page"]
        notes = list(ANNOTATIONS.get(n, []))
        if s["misprint"]:
            notes.append(("blue", "Heading misprint in the published text",
                f"The published PDF numbers this section's heading 7.34.{PART.split('.')[-1]}.{n}. Its own history note and every "
                f"cross-reference in the rule read {PART}.{n}, which this page uses."))
        chips = ""
        kinds = []
        for kind, _, _ in notes:
            if kind not in kinds: kinds.append(kind)
        chipword = {"open": "Open", "settled": "Settled", "defect": "Defect", "blue": "Note"}
        chips = " ".join(f"<span class='mark {k}'>{chipword[k]}</span>" for k in kinds)
        toc.append(f"<a class='toc' href='#s{n}'><span class='sect'>.{n}</span> <span class='t'>{title.title()}</span> {chips}</a>")
        notehtml = "\n".join(
            f"<div class='note {kind}'><span class='mark {kind}'>{chipword[kind]}</span> <b>{html.escape(t)}.</b> {txt}</div>"
            for kind, t, txt in notes)
        body.append(f"""
<section class="rsec" id="s{n}">
  <div class="rhead"><span class="rnum">{PART}.{n}</span><h2 class="rtitle">{title.title()}</h2>
  <a class="pdf" href="{DOC}#page={page}" target="_blank" rel="noopener" data-cite="{CITE}, {DOCDATE}, page {page}">PDF p. {page}</a></div>
  <div class="verbatim">{render_body(s['body'])}</div>
  {notehtml}
</section>""")

    # The definitions the rule imports, placed directly after 7.35.3.7, which
    # is the section that imports them. Only a Part that imports its
    # definitions carries this section; the Part's data says so.
    if HAS_DEFS:
        body.insert(7, render_defs_section())
        toc.insert(7, "<a class='toc' href='#defs'><span class='sect'>2.7</span> "
                      "<span class='t'>The Definitions The Rule Runs On</span> "
                      "<span class='mark open'>Open</span> <span class='mark blue'>Note</span></a>")

    name = syncnav.NAMES["rule"]
    nav = syncnav.build_nav("rule")
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} &middot; {syncnav.TITLE_SUFFIX}</title>
<link rel="stylesheet" href="/style.css">
<style>
.toclist{{display:grid;grid-template-columns:1fr 1fr;gap:2px 28px;margin:18px 0 6px}}
a.toc{{display:flex;gap:10px;align-items:baseline;padding:6px 8px;border-radius:4px;text-decoration:none;color:var(--ink);font-size:13.5px}}
a.toc:hover{{background:var(--wash)}}
a.toc .t{{flex:1}}
.rsec{{margin:52px 0;scroll-margin-top:70px}}
.rhead{{display:flex;gap:14px;align-items:baseline;border-bottom:1.5px solid var(--ink);padding-bottom:6px;margin-bottom:12px}}
.rnum{{font:650 13px var(--mono);color:var(--blue)}}
.rtitle{{font:650 16.5px/1.3 var(--sans);margin:0;flex:1}}
a.pdf{{font:600 10.5px var(--mono);color:var(--faint);text-decoration:none;white-space:nowrap}}
a.pdf:hover{{color:var(--blue)}}
.hist{{color:var(--faint);font-size:12.5px}}
.defslede{{font-size:14px;color:var(--ink2);line-height:1.6;max-width:74ch;margin:0 0 18px}}
.defentry{{padding:12px 0;border-top:1px solid var(--hair);scroll-margin-top:70px}}
.defentry:first-of-type{{border-top:none}}
.defhead{{display:flex;gap:12px;align-items:baseline}}
.dterm{{font:650 14px var(--sans);color:var(--ink);flex:1}}
.deftext{{font-size:14px;color:var(--ink2);line-height:1.6;margin:5px 0 0;max-width:74ch}}
.deftext s,.defslede s{{color:var(--faint)}}
@media(max-width:760px){{.toclist{{grid-template-columns:1fr}}}}
</style>
<noscript><style>.tnav{{display:flex}}</style></noscript>
</head>
<body>
<header class="topbar">
  <div class="inner">
    <a class="brand" href="index.html"><span class="dot"></span>{partlib.brand(PART)}</a>
{nav}
    <button class="hamburger" id="hbtn" aria-label="Menu" aria-expanded="false" aria-controls="tnav">&#9776;</button>
  </div>
</header>
<main class="wrap">
  <div class="head">
    <p class="kicker">{KICKER}</p>
    <h1>{name}</h1>
    <p class="lede">{LEDE}</p>
    <p class="stamp">Text from the official PDF published {DOCDATE}. Regenerated by tools/build-rule-page.py.</p>
  </div>
  <div class="toclist">
  {"".join(toc)}
  </div>
  {"".join(body)}
</main>
{FOOT}
{syncnav.NAV_JS}
</body>
</html>
"""
    open(OUT, "w").write(doc)
    print(f"wrote {OUT}: {len(sections)} sections, {len(doc)} bytes")

    # The page-wide tools own the versioned stylesheet link, the visit counter,
    # and the provenance block; running them here means a regenerated page is
    # never live without them.
    for tool in ("sync-css-version.py", "sync-count.py", "sync-provenance.py"):
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", tool), "--part", PART],
                       check=True, stdout=subprocess.DEVNULL)
    print("stamped: stylesheet version, visit counter, provenance block")

if __name__ == "__main__":
    main()

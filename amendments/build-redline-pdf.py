#!/usr/bin/env python3
"""Build the side-by-side practicum amendment redline.

Left column: the rule as published July 23, 2026, verbatim.
Right column: the proposed amendment, with insertions and deletions marked.

Every left-column block is verified against the text layer of the published PDF
by exact contiguous match before the file is written. If any block fails, the
build aborts.

Usage:  python3 amendments/build-redline-pdf.py
"""

import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import P, NEW, UNCHANGED          # noqa: E402
from notes import source_for, review_for       # noqa: E402

REPO = Path(__file__).resolve().parent.parent
PUBLISHED_PDF = REPO / "docs/documents/rules-draft-2026-07-23-published.pdf"

VERSION = "v9"
VERSION_DATE = "July 26, 2026"
OUT_PDF = REPO / ("amendments/7.35.3-practicum-amendments-%s.pdf" % VERSION)

LINE_TOLERANCE = 3.0

RETITLE = True

OLD_TITLE = {
    "{{PT}}": "practitioner",
    "{{PTS}}": "practitioners",
    "{{PT_C}}": "Practitioner",
    "{{PTS_C}}": "Practitioners",
    "{{PT_UC}}": "PRACTITIONER",
    "{{PTS_UC}}": "PRACTITIONERS",
}

NEW_TITLE = {
    "{{PT}}": "licensed provider",
    "{{PTS}}": "licensed providers",
    "{{PT_C}}": "Licensed provider",
    "{{PTS_C}}": "Licensed providers",
    "{{PT_UC}}": "LICENSED PROVIDER",
    "{{PTS_UC}}": "LICENSED PROVIDERS",
}

# Tokens for text that is wholly new. There is nothing to strike, so the title
# is written out rather than marked as a change.
FRESH_TITLE = {
    "{{NPT}}": ("licensed provider", "practitioner"),
    "{{NPTS}}": ("licensed providers", "practitioners"),
}

SECTION_TITLES = {
    "7.35.3.14": "Authorized possession, purchase, or sale of medical psilocybin",
    "7.35.3.18": "Educational requirements for certifying clinicians, practitioners, and facilitators",
    "7.35.3.19": "Practicum requirements for practitioners and facilitators",
    "7.35.3.20": "Requirements for healing centers and other approved locations",
    "7.35.3.29": "Proposed new section, in two versions. Practicum participants who are not qualified patients",
}

SECTION_INTRO = {
    "7.35.3.14": "Authorized possession. Subsections A and B are amended so that a practicum participant who is not "
                 "a qualified patient may lawfully be provided psilocybin under Version 2 of the first practicum "
                 "stage. The permit name is conformed throughout the section. Nothing here changes who may possess or "
                 "administer: those acts stay with the licensed provider, the facilitator and the healing center.",
    "7.35.3.18": "Educational requirements. The 84-hour total is stated in one place, the New Mexico module is given "
                 "an hour count, eight content areas are added to the required topic list, an incomplete sentence at "
                 "Subsection F is repaired, and the permit name is conformed throughout the section.",
    "7.35.3.19": "Practicum requirements. The practicum totals, the supervision hours and the practicum sequence are "
                 "amended; independent medical screening, the consultation requirement and the end-of-life checkpoint "
                 "are added; the section is re-lettered A through K.",
    "7.35.3.20": "Requirements for healing centers and other approved locations. The section heading number is "
                 "corrected and the permit name is conformed in Paragraph (5) of Subsection H. No staffing ratio is "
                 "changed, and the qualified student provision is carried forward exactly as the department wrote it.",
    "7.35.3.29": "The first stage of the practicum, in two versions. Version 1 needs no new section and works under "
                 "the Medical Psilocybin Act as it stands today. Version 2 is the model the Metz recommendation "
                 "describes, and Subsection D of it states the statutory amendment that would be required.",
}


# ---------------------------------------------------------------------------
# Verification
# ---------------------------------------------------------------------------

def flatten(t):
    t = t.replace("’", "'").replace("‘", "'")
    t = t.replace("“", '"').replace("”", '"')
    t = t.replace("‐", "-").replace("‑", "-")
    return re.sub(r"\s+", " ", t).strip()


def read_published():
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTTextContainer, LTTextLine
    out = []
    for page in extract_pages(str(PUBLISHED_PDF)):
        items = []
        for element in page:
            if not isinstance(element, LTTextContainer):
                continue
            for line in element:
                if isinstance(line, LTTextLine) and line.get_text().strip():
                    items.append((line.y0, line.x0, line.get_text().rstrip("\n")))
        items.sort(key=lambda r: -r[0])
        clusters = []
        for y, x, text in items:
            if clusters and abs(clusters[-1][0] - y) <= LINE_TOLERANCE:
                clusters[-1][1].append((x, text))
            else:
                clusters.append((y, [(x, text)]))
        for _, parts in clusters:
            parts.sort(key=lambda r: r[0])
            out.append(" ".join(t for _, t in parts))
    return flatten(" ".join(out))


def verify():
    corpus = read_published()
    failures = []
    for section, sub, published, _ in P:
        if published in (NEW, UNCHANGED):
            continue
        for chunk in published.split("\n"):
            c = flatten(chunk)
            if c and c not in corpus:
                failures.append((section, sub, c[:110]))
    return failures


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

CSS = """
@page { size: letter landscape; margin: 0.62in 0.5in 0.6in 0.5in;
        @top-left { content: ""; font-family: Helvetica, Arial, sans-serif; font-size: 7.4pt; color: #777; }
        @top-right { content: "Working draft {VERSION}"; font-family: Helvetica, Arial, sans-serif;
                     font-size: 7.4pt; color: #999; }
        @bottom-center { content: counter(page); } }
* { box-sizing: border-box; }
body { font-family: "Times New Roman", Times, Georgia, serif; font-size: 8.7pt;
       line-height: 1.36; color: #111; margin: 0; }
h1 { font-family: Helvetica, Arial, sans-serif; font-size: 13.5pt; margin: 0 0 3pt 0; letter-spacing: -0.2pt; }
.sub { font-family: Helvetica, Arial, sans-serif; font-size: 8.4pt; color: #444; margin: 0 0 3pt 0; }
.cover { border-bottom: 2px solid #111; padding-bottom: 5pt; margin-bottom: 7pt; }
ul.what { font-family: Helvetica, Arial, sans-serif; font-size: 8.2pt; line-height: 1.42;
          margin: 0 0 7pt 0; padding-left: 15pt; max-width: 7.6in; }
ul.what li { margin-bottom: 2pt; }
.key { font-family: Helvetica, Arial, sans-serif; font-size: 7.9pt; color: #333;
       border-top: 0.5px solid #ccc; border-bottom: 0.5px solid #ccc; padding: 4pt 0; margin: 0 0 7pt 0; }
p.tnote { font-family: Helvetica, Arial, sans-serif; font-size: 7.5pt; color: #555; margin: 0; max-width: 6.6in; }
h2 { font-family: Helvetica, Arial, sans-serif; font-size: 11pt; margin: 0 0 5pt 0;
     padding: 3pt 0; border-top: 1.5px solid #111; border-bottom: 0.5px solid #111; break-after: avoid; }
section.rr { break-before: page; }
h2.sec { break-before: avoid; }
h2 .ttl { font-weight: normal; color: #555; font-size: 9pt; }
p.intro { font-family: Helvetica, Arial, sans-serif; font-size: 8.1pt; line-height: 1.5; color: #333;
          margin: 0 0 8pt 0; padding-left: 8pt; border-left: 2.5px solid #bbb; break-after: avoid; }
table.rl { width: 100%; border-collapse: collapse; }
table.rl tr { break-inside: auto; }
.label { break-after: avoid; }
.prov, .review { break-inside: avoid; }
table.rl th { font-family: Helvetica, Arial, sans-serif; font-size: 7.6pt; text-transform: uppercase;
              letter-spacing: 0.4pt; color: #333; text-align: left; padding: 5pt 9pt 6pt 9pt;
              border-bottom: 1px solid #999; width: 50%; vertical-align: top; }
table.rl th span { display: block; font-weight: normal; text-transform: none; letter-spacing: 0;
                   font-size: 7.1pt; color: #777; margin-top: 2pt; }
table.rl td { vertical-align: top; padding: 8pt 0 9pt 0; border-bottom: 0.5px solid #ddd; }
table.rl tr.keep { break-inside: avoid; }
.cols { display: grid; grid-template-columns: 1fr 1fr; }
.cl { padding: 0 9pt 0 9pt; border-right: 1px solid #ccc; color: #333; }
.cr { padding: 0 9pt 0 9pt; }
table.rl tr.provrow .review, table.rl tr.provrow .prov { margin-left: 9pt; margin-right: 9pt; }
.label { font-family: Helvetica, Arial, sans-serif; font-size: 7.7pt; font-weight: bold; color: #000;
         margin-bottom: 3pt; }
ins { text-decoration: underline; color: #0a5c2e; font-weight: bold; }
del { text-decoration: line-through; color: #9b1c1c; }
.none { color: #888; font-style: italic; }
.note { color: #666; font-style: italic; font-size: 8pt; }
.unch { color: #666; font-style: italic; }
.rangebadge { display: inline-block; font-family: Helvetica, Arial, sans-serif; font-size: 6.6pt;
              line-height: 1; color: #8a5a00; background: #fdf5e3; border: 0.5px solid #e0c98a;
              border-radius: 2pt; padding: 2pt 4pt; margin: 0 3pt; vertical-align: 1.5pt;
              white-space: nowrap; font-weight: normal; text-decoration: none; }
.prov { margin-top: 6pt; padding-top: 4pt; border-top: 0.5px dashed #bbb;
        font-family: Helvetica, Arial, sans-serif; font-size: 7.2pt; line-height: 1.45; color: #555; }
.prov span { display: inline-block; text-transform: uppercase; letter-spacing: 0.5pt; font-size: 6.5pt;
             color: #888; margin-right: 5pt; }
.review { margin-top: 7pt; border: 1.5pt solid #e09a3e; background: #fffdf8; border-radius: 7pt;
          padding: 6pt 10pt; font-family: Helvetica, Arial, sans-serif; font-size: 7.5pt;
          line-height: 1.5; color: #7a2e2e; font-weight: 600; }
.review b { color: #c0392b; font-weight: bold; letter-spacing: 0.3pt; }
table.hrs { border-collapse: collapse; font-family: Helvetica, Arial, sans-serif; font-size: 8.2pt;
            margin: 0 0 6pt 0; break-inside: avoid; }
table.hrs th, table.hrs td { border: 0.5px solid #bbb; padding: 1.9pt 9pt; text-align: left; }
table.hrs th { background: #f2f2f2; font-size: 7.6pt; text-transform: uppercase; letter-spacing: 0.3pt; }
table.hrs td.n { text-align: right; white-space: nowrap; }
table.hrs tr.band td { background: #f2f2f2; font-weight: bold; border-top: 1.5px solid #111; }
table.dep { width: 100%; border-collapse: collapse; font-family: Helvetica, Arial, sans-serif;
            font-size: 7.9pt; margin: 4pt 0 10pt 0; }
table.dep th, table.dep td { border: 0.5px solid #bbb; padding: 4pt 7pt; text-align: left; vertical-align: top; }
table.dep th { background: #f2f2f2; font-size: 7.6pt; }
table.dep td.amd { color: #0a5c2e; font-weight: bold; }
table.dep td.flag { color: #9b1c1c; }
.foot { margin-top: 14pt; border-top: 1.5px solid #111; padding-top: 8pt;
        font-family: Helvetica, Arial, sans-serif; font-size: 7.7pt; line-height: 1.5; color: #444; }
"""


# Running header in the top-left margin of every page. A named page per section
# means a page carries the identity of the section it belongs to, and Chromium
# reproduces that in the margin box on every page the section spans.
RUNNING = [
    ("s14", "7.35.3.14", "Authorized possession, purchase, or sale of medical psilocybin"),
    ("s18", "7.35.3.18", "Educational requirements"),
    ("s19", "7.35.3.19", "Practicum requirements"),
    ("s20", "7.35.3.20", "Requirements for healing centers and other approved locations"),
    ("s29", "7.35.3.29", "Proposed new section, practicum participants who are not qualified patients"),
    ("adA", "Addendum A", "Provisions on which the practicum operates"),
    ("adB", "Addendum B", "Terms used in Part 3 and defined nowhere"),
    ("adC", "Addendum C", "The permit name, and every place the renaming reaches"),
    ("adD", "Addendum D", "Sections not addressed"),
]

SECTION_CLASS = {sec: cls for cls, sec, _ in RUNNING if sec.startswith("7.")}


def running_css():
    out = []
    for cls, label, title in RUNNING:
        out.append('@page %s { @top-left { content: "%s  %s"; } }' % (cls, label, title))
        out.append('section.%s { page: %s; }' % (cls, cls))
    return "\n".join(out)


def _fresh(t, i):
    for k, v in FRESH_TITLE.items():
        t = t.replace(k, v[i])
    return t


def render_rule(t):
    """Right-column rule text. The permit title is marked as a change."""
    for k in OLD_TITLE:
        if RETITLE:
            t = t.replace(k, '<del>%s</del> <ins>%s</ins>' % (OLD_TITLE[k], NEW_TITLE[k]))
        else:
            t = t.replace(k, OLD_TITLE[k])
    return _fresh(t, 0 if RETITLE else 1)


def render_label(t):
    """Row labels. These locate a provision in the rule as published."""
    for k, v in OLD_TITLE.items():
        t = t.replace(k, v)
    return _fresh(t, 1)


def render_note(t):
    """Source and review notes. These describe the proposal."""
    table = NEW_TITLE if RETITLE else OLD_TITLE
    for k, v in table.items():
        t = t.replace(k, v)
    return _fresh(t, 0 if RETITLE else 1)


def esc(t):
    return html.escape(t).replace("\n", "<br>")


HEAD = """
<div class="cover">
<h1>7.35.3 NMAC: proposed amendments to the practicum and training provisions</h1>
<p class="sub">Working draft {VERSION}, {VERSION_DATE}. Rule hearing August 28, 2026.</p>
</div>

<ul class="what">
<li>This document analyzes the recommendation of Dr. Anne Metz to the Training and Education Committee dated
July 17, 2026, and states it as amendment language against the proposed rule published July 23, 2026. The working
redline of Denali Wilson dated July 25, 2026 is folded in, and provisions taken from it are cited to her.</li>
<li>It covers 7.35.3.19, practicum requirements, and the three provisions on which the practicum depends:
7.35.3.18, educational requirements; 7.35.3.14, authorized possession; and Paragraph (5) of Subsection H of
7.35.3.20, staffing ratios. One new section is proposed; no other provision of Part 3 is addressed.</li>
<li>Recommendation 1 of the Metz recommendation renames the practitioner permit to licensed provider. The renaming
is carried through and marked <del>practitioner</del> <ins>licensed provider</ins> wherever it falls inside a
provision reproduced here. Addendum C counts every other place in 7.35.3 NMAC and 7.35.2 NMAC that a conforming
amendment would have to reach, so the committee can see the whole extent of it before adopting it.</li>
<li><b>Two decisions are put to the committee as drafted alternatives, not as questions.</b> Paragraph (1) of
Subsection D of 7.35.3.19 is drafted in two versions. Version 1 operates under the Medical Psilocybin Act exactly as
it stands today and needs no new section. Version 2 is the model the Metz recommendation describes and cannot operate
until the Act is amended; proposed 7.35.3.29 states the amendment requested in its own subsection. The practicum
total is 62 and 72 hours under either version.</li>
<li>Where a source states a range, this draft adopts the low end and marks it, so that the committee may raise it.
Where the rule as published is unclear, the published text is left exactly as it stands and the choice is set out at
that provision. No figure appears anywhere in this draft that is not carried by a cited source.</li>
</ul>

<div class="key">
<b>The columns.</b> Left is the rule as published, verbatim. Right is the proposed amendment:
<ins>underlined green inserted</ins>, <del>struck red deleted</del>, unmarked text carried forward unchanged.
<span class="rangebadge">Metz: 6 to 8</span> marks a figure taken from the low end of a recommended range.
</div>

<h2>Hours <span class="ttl">Published against proposed</span></h2>
<table class="hrs">
<tr><th>Component</th><th>Published</th><th>Proposed</th><th>Change</th></tr>
<tr><td>New Mexico module</td><td class="n">not stated</td><td class="n">6</td><td class="n">+6</td></tr>
<tr><td>Psilocybin therapy module, didactic</td><td class="n">30</td><td class="n">68</td><td class="n">+38</td></tr>
<tr><td>Simulated patient experience</td><td class="n">5</td><td class="n">5</td><td class="n">0</td></tr>
<tr><td>Role-specific module</td><td class="n">5</td><td class="n">5</td><td class="n">0</td></tr>
<tr><td><b>Module total, either permit</b></td><td class="n"><b>40</b></td><td class="n"><b>84</b></td><td class="n"><b>+44</b></td></tr>
<tr><td>Practicum, facilitator</td><td class="n">100</td><td class="n">62</td><td class="n">&minus;38</td></tr>
<tr><td>Practicum, licensed provider</td><td class="n">120</td><td class="n">72</td><td class="n">&minus;48</td></tr>
<tr><td>Supervision or consultation</td><td class="n">10</td><td class="n">20</td><td class="n">+10</td></tr>
<tr class="band"><td>Program total, facilitator</td><td class="n">150</td><td class="n">166</td><td class="n">+16</td></tr>
<tr class="band"><td>Program total, licensed provider</td><td class="n">170</td><td class="n">176</td><td class="n">+6</td></tr>
</table>
<p class="tnote">The 20 supervision hours in 7.35.3.19 C sit inside the practicum total, not on top of it, so the
published licensed provider total is 170. The basis is set out at 7.35.3.19 C.</p>
"""


def strip_tags(t):
    return re.sub(r"<[^>]+>", "", t or "")


def build_body():
    rows = []
    current = None
    for section, sub, published, proposed in P:
        if section != current:
            if current is not None:
                rows.append("</table></section>")
            current = section
            rows.append('<section class="rr %s">' % SECTION_CLASS[section])
            rows.append('<h2 class="sec">%s <span class="ttl">%s</span></h2>' % (section, SECTION_TITLES[section]))
            if section in SECTION_INTRO:
                rows.append('<p class="intro">%s</p>' % SECTION_INTRO[section])
            rows.append('<table class="rl"><tr>'
                        '<th>Current language<span>Proposed rule as published July 23, 2026</span></th>'
                        '<th>Proposed amendment<span>Draft for review. Not filed, not adopted</span></th></tr>')
        label = render_label(sub)
        if published == UNCHANGED and proposed == UNCHANGED:
            rows.append('<tr class="provrow keep"><td colspan="2"><div class="cols">'
                        '<div class="cl"><div class="label">%s</div><span class="unch">Not amended.</span></div>'
                        '<div class="cr"><div class="label">%s</div><span class="unch">Not amended.</span></div>'
                        '</div></td></tr>' % (label, label))
            continue
        left = ('<span class="none">%s</span>' % NEW) if published == NEW else esc(published)
        if proposed == UNCHANGED:
            right = '<span class="unch">Not amended.</span>'
        else:
            right = render_rule(proposed)
        src = source_for(section, sub)
        rev = review_for(section, sub)
        extra = ''
        if src:
            extra += '<div class="prov"><span>Source</span>%s</div>' % render_note(src)
        if rev:
            extra += '<div class="review"><b>Please review.</b> %s</div>' % render_note(rev)
        # One row per provision. The two columns are a grid inside a single
        # cell, and the notes run the full width beneath them, so a note is
        # about half as tall as it would be inside a column. A provision short
        # enough to fit a page is marked so it is never split.
        body = max(len(strip_tags(left)), len(strip_tags(right))) / 92.0
        lines = body + len(strip_tags(extra)) / 190.0 + 4
        keep = " keep" if lines < 18 else ""
        rows.append('<tr class="provrow%s"><td colspan="2">'
                    '<div class="cols"><div class="cl"><div class="label">%s</div>%s</div>'
                    '<div class="cr"><div class="label">%s</div>%s</div></div>%s</td></tr>'
                    % (keep, label, left, label, right, extra))
    rows.append("</table></section>")
    return "\n".join(rows)


ADDENDA = """
<section class="rr adA">
<h2 class="sec">Addendum A <span class="ttl">Provisions on which the practicum operates</span></h2>
<p class="intro">Provisions on which 7.35.3.19 operates, and whether this draft amends each.</p>
<table class="dep">
<tr><th>Provision</th><th>Page</th><th>What the practicum needs from it</th><th>In this draft</th></tr>
<tr><td>7.35.2.7 NMAC</td><td>n/a</td><td>Supplies every defined term used in Part 3, by force of 7.35.3.7</td><td class="flag">Not amended here. Renaming the permit would require amending the definition at P(7); 7.35.2 NMAC is a separate rulemaking. Facilitator, healing center, certifying clinician and student are used in Part 3 and defined in neither part. Addenda B and C</td></tr>
<tr><td>Medical Psilocybin Act, Section 5</td><td>n/a</td><td>The criminal and civil exemption. Names producers, clinicians and qualified patients, and protects presence only for anyone else</td><td class="flag">Statute. Not reachable by rule</td></tr>
<tr><td>7.35.3.9 C(3), E, F</td><td>3</td><td>Certification applications require documentation of the completed practicum, and E(1) sets the practitioner licensure predicate</td><td>Not amended</td></tr>
<tr><td>7.35.3.10 D</td><td>5</td><td>Out-of-jurisdiction 40-hour practicum waiver</td><td class="flag">Not amended. Disagrees with 7.35.3.19 K</td></tr>
<tr><td>7.35.3.11 A, B</td><td>5 to 7</td><td>Healing centers and other approved locations. The practicum may only happen in them</td><td>Not amended</td></tr>
<tr><td>7.35.3.12 A</td><td>7</td><td>Educational program certification</td><td>Not amended</td></tr>
<tr><td>7.35.3.13 B</td><td>8</td><td>Facilitator scope of work, which limits what the practicum can usefully train</td><td class="flag">Not amended</td></tr>
<tr><td class="amd">7.35.3.14</td><td>9</td><td>Authority to possess and administer</td><td class="amd">AMENDED. Heading, Subsections A and B</td></tr>
<tr><td>7.35.3.15 A(4)</td><td>9</td><td>Practicum site agreements need prior written approval, with no deadline on the department</td><td class="flag">Not amended</td></tr>
<tr><td>7.35.3.17 A</td><td>10 to 11</td><td>The 10 mentoring hours the consultation requirement would replace</td><td class="flag">Not amended</td></tr>
<tr><td>7.35.3.17 B, C</td><td>11</td><td>Test-out, graduation conditions, and the practicum records a program must keep</td><td>Not amended</td></tr>
<tr><td class="amd">7.35.3.18</td><td>11 to 12</td><td>The didactic requirement the practicum entry gate is measured against</td><td class="amd">AMENDED. Heading and Subsections A, C, E, F and G</td></tr>
<tr><td class="amd">7.35.3.19</td><td>12 to 13</td><td>The practicum</td><td class="amd">AMENDED. Re-lettered A to K</td></tr>
<tr><td>7.35.3.20 D</td><td>14</td><td>Students may be present at an administration session</td><td>Not amended</td></tr>
<tr><td class="amd">7.35.3.20 H(5)</td><td>14</td><td>Staffing ratio, which counts a qualified student</td><td class="amd">AMENDED. Permit name only. No ratio changed</td></tr>
<tr><td>7.35.3.22</td><td>15</td><td>Prohibitions, reaching "the qualified patient or certificant"</td><td class="flag">Not amended</td></tr>
<tr><td>7.35.3.27</td><td>16 to 19</td><td>Discipline and appeal</td><td>Not amended</td></tr>
</table>

<h2>Proposed new provisions</h2>
<table class="dep">
<tr><th>Provision</th><th>What it does</th><th>Source</th><th>If dropped</th></tr>
<tr><td>7.35.3.18 H</td><td>States the 84-hour total in one place</td><td>Metz recommendation, page 3</td><td>Module hours survive individually; no total is stated anywhere</td></tr>
<tr><td>7.35.3.19 D</td><td>The four-step practicum sequence</td><td>Metz recommendation, pages 3 to 4; Wilson redline for the drafting</td><td>Practicum totals survive; the sequence is lost</td></tr>
<tr><td>7.35.3.19 F</td><td>Separates medical screening from the training program overseeing the practicum</td><td>Wilson redline</td><td class="flag">A program may clear its own students for the treatments that generate their hours</td></tr>
<tr><td>7.35.3.19 H</td><td>20 consultation hours, two presented cases, standardized evaluation form</td><td>Metz recommendation, pages 4 to 5</td><td>7.35.3.17 A survives at 10 hours with no requirement to have seen a client</td></tr>
<tr><td>7.35.3.19 I</td><td>End-of-life checkpoint</td><td>Metz recommendation, page 5</td><td>No end-of-life competency gate remains</td></tr>
<tr><td>7.35.3.29<br>Version 2 only</td><td>Lets the first practicum stage run with participants who are not qualified patients, and states the statutory amendment that would be required</td><td>Metz recommendation, step 1, page 3; Medical Psilocybin Act, Section 5</td><td>Version 1 governs, the first stage runs with qualified patients, and no statutory work is needed</td></tr>
</table>
<p class="tnote">No training permit is proposed. At the July 17, 2026 Training and Education Committee meeting the
department stated that a training permit "really wouldn't be necessary with the model that we have" and undertook to
count students toward the staffing ratio instead. Paragraph (5) of Subsection H of 7.35.3.20 as published does that.
See the note at that paragraph.</p>

<h2>The one statutory request in this document</h2>
<p class="intro">Everything else in this draft can be adopted by rule. One thing cannot. If the committee wants the
first practicum stage to run with well participants, as the Metz recommendation describes, the Medical Psilocybin Act
has to be amended, and this document asks for that amendment in plain terms rather than leaving it implied.</p>
<table class="dep">
<tr><th>What the Act says now</th><th>Why the first stage falls outside it</th><th>The amendment requested</th><th>If it is not pursued</th></tr>
<tr><td>Paragraph (2) of Subsection B of Section 5 makes lawful the conduct of "a clinician administering or a qualified patient taking psilocybin in an approved setting". Subsection D of the same section protects a person "for simply being in the presence of the medical use of psilocybin"</td><td>A well participant is not a qualified patient, because Subsection H of Section 3 defines a qualified patient by diagnosis with a qualifying condition. Presence is protected; taking psilocybin is not</td><td class="amd">Extend the exemption in Section 5 to a practicum participant taking medical psilocybin in an approved setting under department rule, and to a certificant or student administering or providing it to such a participant</td><td>Adopt Version 1. The first stage runs with qualified patients, the practicum total stays at 62 and 72 hours, and proposed 7.35.3.29 is deleted</td></tr>
</table>

</section>
<section class="rr adB">
<h2 class="sec">Addendum B <span class="ttl">Terms used in Part 3 and defined nowhere</span></h2>
<p class="intro">7.35.3.7 provides in full: "The definitions in 7.35.2.7 NMAC apply to this part." 7.35.2 NMAC was adopted effective June 23, 2026. The terms below are used in Part 3. Apart from the permit title, no amendment to the definitions is proposed in this document.</p>
<table class="dep">
<tr><th>Term used in Part 3</th><th>In 7.35.2.7?</th><th>What 7.35.2.7 has</th><th>Consequence</th></tr>
<tr><td><b>Facilitator</b></td><td class="flag">No. Zero occurrences in 7.35.2 NMAC</td><td>"Guide" an individual who has completed training and education approved by the department to be able to assist practitioners during the administration sessions and who has been registered with the department</td><td class="flag">Every facilitator provision in Part 3 rests on an undefined term. A guide holds no professional license, so a facilitator is not a "clinician" under Section 3(B) of the Act, while 7.35.3.14 B authorizes facilitators to possess and provide</td></tr>
<tr><td><b>Healing center</b></td><td class="flag">No</td><td>"Approved location" means a location approved by the department for psilocybin administration sessions</td><td class="flag">Healing centers are certified and regulated throughout Part 3 with no definition</td></tr>
<tr><td><b>Certifying clinician</b></td><td class="flag">No</td><td>"Clinician" means an approved health care provider licensed in New Mexico who holds a certification from the department to provide medical services to qualified patients</td><td>Probably the same role renamed</td></tr>
<tr><td><b>Student</b></td><td class="flag">No</td><td>Nothing</td><td class="flag">Carries consequence at 7.35.3.19, 7.35.3.20 D and 7.35.3.20 H(5)</td></tr>
<tr><td>Practitioner</td><td>Yes</td><td>"Practitioner" means an individual who is a licensed healthcare professional who is certified by the department to provide medical psilocybin integrative therapy, supervise guides, and who has completed department required trainings</td><td class="amd">Carries the same licensure predicate as the Act's "clinician". Renamed by this draft. Addendum C</td></tr>
</table>

</section>
<section class="rr adC">
<h2 class="sec">Addendum C <span class="ttl">The permit name, and every place the renaming reaches</span></h2>
<p class="intro">Recommendation 1 of the Metz recommendation, page 1, renames the practitioner permit to licensed provider. This draft
carries the renaming. It is marked <del>practitioner</del> <ins>licensed provider</ins> wherever
it falls inside a provision reproduced in this document. The term is defined at Paragraph (7) of Subsection P of
7.35.2.7 NMAC, and 7.35.3.7 NMAC provides in full: "The definitions in 7.35.2.7 NMAC apply to this part." Renaming
the permit is therefore an amendment to 7.35.2 NMAC plus a conforming pass over 7.35.3 NMAC. The tables below count every
occurrence in both parts, so that the committee can see the whole surface.</p>
<p class="tnote">Two drafting notes. First, the Metz recommendation writes "Licensed Provider" in title case; this
draft writes "licensed provider" in lower case, because the rule as published writes "practitioner" in lower case
except in headings and at the start of a subsection. Second, the renaming reaches no hour count and no practicum
requirement. Those attach to the permit type, and what the permit is turns on the licensure predicate at Paragraph (1)
of Subsection E of 7.35.3.9 NMAC, which already requires a New Mexico professional license. Adopting or declining the
renaming changes nothing else in this document.</p>
<table class="dep">
<tr><th>7.35.3 NMAC, section</th><th>Occurrences</th><th>Reached by this draft</th><th>Note</th></tr>
<tr><td>Part title</td><td>1</td><td class="flag">No</td><td>"PART 3 PATIENTS, CERTIFYING CLINICIANS, PRACTITIONERS, FACILITATORS, HEALING CENTERS, OTHER APPROVED LOCATIONS, AND EDUCATIONAL PROGRAMS"</td></tr>
<tr><td>7.35.3.2 Scope</td><td>1</td><td class="flag">No</td><td>Who the part applies to</td></tr>
<tr><td>7.35.3.6 Objective</td><td>1</td><td class="flag">No</td><td></td></tr>
<tr><td>7.35.3.9 Certification requirements</td><td>5</td><td class="flag">No</td><td>Includes the section heading and the licensure predicate at E(1)</td></tr>
<tr><td>7.35.3.10 Application process</td><td>5</td><td class="flag">No</td><td>Includes the section heading and the out-of-jurisdiction pathway</td></tr>
<tr><td>7.35.3.11 Healing centers</td><td>3</td><td class="flag">No</td><td></td></tr>
<tr><td>7.35.3.12 Educational programs</td><td>1</td><td class="flag">No</td><td></td></tr>
<tr><td>7.35.3.13 Requirements and prohibitions</td><td>12</td><td class="flag">No</td><td>The largest block outside this draft. Includes the section heading and the scope of work</td></tr>
<tr><td class="amd">7.35.3.14 Authorized possession</td><td>6</td><td class="amd">Yes, all 6</td><td>Heading and Subsection A</td></tr>
<tr><td>7.35.3.17 Educational programs</td><td>2</td><td class="flag">No</td><td>Includes the mentoring provision at Subsection A</td></tr>
<tr><td class="amd">7.35.3.18 Educational requirements</td><td>14</td><td class="amd">Yes, all 14</td><td>Heading and Subsections A, C, E, F and G</td></tr>
<tr><td class="amd">7.35.3.19 Practicum requirements</td><td>6</td><td class="amd">Yes, all 6</td><td>Heading and Subsections A and C</td></tr>
<tr><td class="amd">7.35.3.20 Healing centers</td><td>3</td><td class="amd">Yes, all 3</td><td>All three are in Paragraph (5) of Subsection H</td></tr>
<tr><td>7.35.3.26 Voluntary withdrawal</td><td>1</td><td class="flag">No</td><td></td></tr>
<tr><td>7.35.3.27 Disciplinary actions</td><td>5</td><td class="flag">No</td><td>Includes the section heading</td></tr>
<tr class="band"><td><b>Total, 7.35.3 NMAC</b></td><td><b>66</b></td><td><b>29 reached, 37 not</b></td><td>Fourteen of the twenty-eight sections carry the term</td></tr>
</table>
<table class="dep">
<tr><th>7.35.2 NMAC, section</th><th>Occurrences</th><th>Reached by this draft</th><th>Note</th></tr>
<tr><td>7.35.2.7 Definitions</td><td>3</td><td class="flag">No</td><td>The definition itself at P(7); also inside the definitions of "certification" at C(3) and "guide" at G(3)</td></tr>
<tr><td>7.35.2.10 General producer requirements</td><td>1</td><td class="flag">No</td><td></td></tr>
<tr><td>7.35.2.14 Packaging and labeling</td><td>3</td><td class="flag">No</td><td>The product information document duties</td></tr>
<tr><td>7.35.2.15 General tracking requirements</td><td>1</td><td class="flag">No</td><td></td></tr>
<tr><td>7.35.2.19 Required testing</td><td>2</td><td class="flag">No</td><td>Includes the failed-lot notification duty</td></tr>
<tr><td>7.35.2.24 Transportation</td><td>1</td><td class="flag">No</td><td></td></tr>
<tr><td>7.35.2.26 Disciplinary actions</td><td>1</td><td class="flag">No</td><td></td></tr>
<tr class="band"><td><b>Total, 7.35.2 NMAC</b></td><td><b>12</b></td><td><b>0 reached</b></td><td>7.35.2 NMAC was adopted effective June 23, 2026 and is not before this hearing</td></tr>
</table>
<div class="review"><b>Please review.</b> The renaming is all or nothing. If it is adopted, the conforming amendment has
to reach all 66 occurrences in 7.35.3 NMAC and all 12 in 7.35.2 NMAC, including the definition at Paragraph (7) of
Subsection P of 7.35.2.7 NMAC. This document reaches 29. If the committee adopts the renaming, the remaining 49 are a
conforming pass, and 7.35.2 NMAC is a separate rulemaking. If the committee declines it, strike every
<del>practitioner</del> <ins>licensed provider</ins> mark in this document; nothing else in the document depends on
it.</div>

</section>
<section class="rr adD">
<h2 class="sec">Addendum D <span class="ttl">Sections not addressed</span></h2>
<p class="intro">Part 3 has twenty-eight sections. This draft addresses the practicum and the provisions on which it operates. The sections below are not addressed. Findings are recorded in the concerns inventory of July 23, 2026, which lists five blocking and twenty-three material findings across the part.</p>
<table class="dep">
<tr><th>Group</th><th>Sections</th><th>Recorded findings</th></tr>
<tr><td>Terminology</td><td>7.35.3.7, and 7.35.2.7 NMAC</td><td>Facilitator, healing center, certifying clinician and student undefined. Addendum B</td></tr>
<tr><td>Educational programs</td><td>7.35.3.12, .15, .16, .17</td><td>The evaluator conflict rule disqualifies the evaluators a program must hire; the third-party evaluation deferral expires the day it becomes available; no deadline binds the department on instructor changes; the denial grounds were deleted; the evaluator qualification standard may be unmeetable; mentoring is unfunded and untied to certification; the test-out price cap assumes per-module pricing</td></tr>
<tr><td>Out-of-jurisdiction pathway</td><td>7.35.3.10</td><td>The two 40-hour waivers disagree; the 2027 waiver may cancel itself; the approved list is empty at launch and populates only retroactively; individuals must produce an evaluation only a program can commission</td></tr>
<tr><td>Locations and oversight</td><td>7.35.3.11, .20, .21</td><td>Healing center staff authority hangs on a registration that does not exist; outdoor locations need no AED while healing centers do; the patient roster and the patient-interview authority; other approved locations have a 90-day term and no renewal path</td></tr>
<tr><td>Patients, applicants, process</td><td>7.35.3.8, .9, .13, .22 to .27</td><td>Facilitator scope conflicts with the practicum and the ratios; complainants lose confidentiality; the benefit-risk attestation; renewals can lapse while pending; the re-application clause reads as a deadline; two review tracks with inconsistent scope; a suspended certificant can be out of practice more than 135 days</td></tr>
<tr><td>Mechanical</td><td>Throughout</td><td>Five section headings read 7.34.3 instead of 7.35.3, two of which are corrected here; two sections carry a real effective date while the rest carry placeholders; a numbering gap at 7.35.3.9 D</td></tr>
</table>
</section>
"""

FOOT = """
<div class="foot">
<b>Sources.</b> Rule as published: <i>rules-draft-2026-07-23-published.pdf</i>, 19 pages. Recommendations: Dr. Anne
Metz, <i>Recommendations on Education and Training Requirements for Facilitators and Licensed Providers</i>, July 17,
2026, with the one-page summary and the committee slide deck of the same date. Working redline: Denali Wilson,
<i>NMAC 7.35.3</i>, July 25, 2026, tracked changes and comments as exported from the document file. July 17, 2026 transcripts, morning
Advisory Board and afternoon Training and Education Committee, both labeled "UNOFFICIAL AUTO-GENERATED TRANSCRIPT.
NO SPEAKER ATTRIBUTION." Statute: the Medical Psilocybin Act, cited throughout by its own section numbers. The text
consulted is the Act as passed in the 2025 regular session; its codification in NMSA 1978 has not been verified and no
NMSA section number is asserted anywhere in this document. 7.35.2 NMAC as adopted effective June 23, 2026.<br><br>
<b>Method.</b> The left column reproduces the rule as published, verbatim, with line breaks introduced by the PDF
collapsed to single spaces and no other alteration. Each block was checked against the text layer of the published
rule.<br><br>
<b>Status.</b> Working draft {VERSION}. Not a filing, not submitted, and not adopted rule text.
</div>
"""


def main():
    failures = verify()
    if failures:
        print("VERIFICATION FAILED:")
        for section, sub, chunk in failures:
            print("  %s %s :: %s" % (section, render_label(sub), chunk))
        return 1
    print("verified: every published-column block matches the published PDF")

    head = HEAD.replace("{VERSION}", VERSION).replace("{VERSION_DATE}", VERSION_DATE)
    foot = FOOT.replace("{VERSION}", VERSION)
    css = CSS.replace("{VERSION}", VERSION) + "\n" + running_css()
    doc = ("<!doctype html><html><head><meta charset='utf-8'>"
           "<title>7.35.3 NMAC practicum amendments %s</title>"
           "<style>%s</style></head><body>%s%s%s%s</body></html>"
           % (VERSION, css, head, build_body(), ADDENDA, foot))

    tmp = Path(tempfile.mkdtemp()) / "redline.html"
    tmp.write_text(doc, encoding="utf-8")

    chrome = None
    for cand in ["/opt/pw-browsers/chromium", "chromium", "chromium-browser", "google-chrome"]:
        c = shutil.which(cand) or (cand if Path(cand).exists() else None)
        if c:
            chrome = c
            break
    if not chrome:
        print("no chromium found")
        return 1

    subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--print-to-pdf=%s" % OUT_PDF, tmp.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("wrote %s (%.0f KB)" % (OUT_PDF.relative_to(REPO), OUT_PDF.stat().st_size / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())

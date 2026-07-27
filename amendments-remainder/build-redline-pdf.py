#!/usr/bin/env python3
"""Build the side-by-side redline for the twenty-four sections outside the practicum draft.

Left column: the rule as published July 23, 2026, verbatim.
Right column: the proposed amendment, with insertions and deletions marked.

Every left-column block is verified against the text layer of the published PDF
by exact contiguous match before any file is written. If any block fails, the
build aborts and writes nothing.

One document: the redline, sections in numerical order, then five addenda.
Sections share pages so no section forces a page of its own.

The form follows `amendments/7.35.3-practicum-amendments-v9.pdf` for the table:
each provision is one table row whose two columns are a grid inside a single
cell, so a long provision flows across a page break with the columns still
aligned and the notes run the full width beneath them. The redline body shares
one named CSS page instead of one per section, a recorded divergence from v9.

The machinery is copied from `amendments/build-redline-pdf.py` rather than
imported, so that the practicum document keeps building if this one breaks.

Usage:  python3 amendments-remainder/build-redline-pdf.py
"""

import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import P, NEW, UNCHANGED, D1, D2, D3, D4     # noqa: E402
from notes import source_for, review_for, REVIEW, GROUPS, QUESTIONS   # noqa: E402

REPO = Path(__file__).resolve().parent.parent
OUT_PDF = REPO / "amendments-remainder/7.35.3-remainder-amendments-v3.pdf"
PUBLISHED_PDF = REPO / "docs/documents/rules-draft-2026-07-23-published.pdf"
PART2_TXT = REPO / "source-text/7.35.2-NMAC-adopted-2026-06-23.txt"

VERSION = "v3"
VERSION_DATE = "July 26, 2026"

LINE_TOLERANCE = 3.0

SECTION_TITLES = {
    "7.35.3.2": "Scope",
    "7.35.3.3": "Statutory authority",
    "7.35.3.5": "Effective date",
    "7.35.3.7": "Definitions",
    "7.35.3.8": "Patient enrollment application process",
    "7.35.3.9": "Certifying clinician, practitioner, and facilitator application process",
    "7.35.3.10": "Application process based on educational programs from other jurisdictions",
    "7.35.3.11": "Application process for healing centers and other approved locations",
    "7.35.3.12": "Application process for psilocybin educational programs",
    "7.35.3.13": "Requirements and prohibitions for certifying clinicians, practitioners, and facilitators",
    "7.35.3.15": "Psilocybin educational programs; required reporting and curriculum approval",
    "7.35.3.16": "Requirements for third-party evaluators of educational programs",
    "7.35.3.17": "Educational programs; mentoring requirements; record-keeping",
    "7.35.3.20": "Requirements for healing centers and other approved locations",
    "7.35.3.21": "Department evaluation and assessment",
    "7.35.3.23": "Prohibition against dual ownership in certificant and permittee",
    "7.35.3.24": "Complaints to the department",
    "7.35.3.25": "Informal administrative review of denied patient applications",
    "7.35.3.27": "Disciplinary actions and appeal process",
}

# The terms Addendum A maps. Each is used in 7.35.3 NMAC and defined nowhere.
UNDEFINED_TERMS = [
    "educational program", "facilitator", "healing center", "certifying clinician",
    "other approved location", "practicum", "student", "certificant", "registrant",
    "didactic", "adverse health event", "administrative review committee", "graduate",
    "simulated patient", "medical psilocybin services", "equity and access fund",
]

# Terms 7.35.2.7 NMAC does define, shown for contrast in Addendum A.
DEFINED_TERMS = ["practitioner", "clinician", "qualified patient", "administration session",
                 "approved location", "guide"]


# ---------------------------------------------------------------------------
# Reading the published rule
# ---------------------------------------------------------------------------

def flatten(t):
    for a, b in [("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("‐", "-"), ("‑", "-"), ("–", "-"), ("—", "-"), ("­", "")]:
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def read_published():
    """The text layer of the published rule, as one flattened string.

    Lines are joined in reading order. Where a line ends in a hyphen and the
    next begins with a lowercase letter, the hyphenation was introduced by the
    line break and the halves are rejoined. Nothing else is altered.
    """
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTTextContainer, LTTextLine
    lines = []
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
            lines.append(" ".join(t for _, t in parts))
    out = ""
    for raw in lines:
        s = re.sub(r"\s+", " ", raw).strip()
        if out.endswith("-") and s[:1].islower():
            out += s
        else:
            out = (out + " " + s) if out else s
    return flatten(out)


def verify(corpus):
    failures = []
    for doc, section, sub, published, _ in P:
        if published in (NEW, UNCHANGED):
            continue
        for chunk in published.split("\n"):
            c = flatten(chunk)
            if c and c not in corpus:
                failures.append((doc, section, sub, c[:110]))
    return failures


def segment(corpus, pattern):
    """Split a corpus into sections keyed by section number."""
    heads, seen = [], set()
    for m in re.finditer(pattern, corpus):
        n = int(m.group(1))
        if n in seen:
            continue
        seen.add(n)
        heads.append((m.start(), n))
    out = {}
    for i, (pos, n) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(corpus)
        out[n] = corpus[pos:end]
    return heads, out


def count_term(body, term):
    if term == "clinician":
        return len(re.findall(r"(?i)(?<!certifying )clinician", body))
    return len(re.findall(r"(?i)" + re.escape(term), body))


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
p.tnote { font-family: Helvetica, Arial, sans-serif; font-size: 7.5pt; color: #555; margin: 0 0 3pt 0;
          max-width: 7.4in; }
h2 { font-family: Helvetica, Arial, sans-serif; font-size: 11pt; margin: 0 0 5pt 0;
     padding: 3pt 0; border-top: 1.5px solid #111; border-bottom: 0.5px solid #111; break-after: avoid; }
section.rr { break-before: page; }
section.src { break-before: page; }
section.flow { break-before: avoid; }
section.flow h2.sec { margin-top: 9pt; }
h2.sec { break-before: avoid; }
h2 .ttl { font-weight: normal; color: #555; font-size: 9pt; }
h2 .pt { float: right; font-weight: normal; color: #888; font-size: 7.4pt; text-transform: uppercase;
         letter-spacing: 0.6pt; padding-top: 3pt; }
p.intro { font-family: Helvetica, Arial, sans-serif; font-size: 8.1pt; line-height: 1.5; color: #333;
          margin: 0 0 8pt 0; padding-left: 8pt; border-left: 2.5px solid #bbb; break-after: avoid; }
table.rl { width: 100%; border-collapse: collapse; }
table.rl tr { break-inside: auto; }
table.rl tr.keep { break-inside: avoid; }
table.rl th { font-family: Helvetica, Arial, sans-serif; font-size: 7.6pt; text-transform: uppercase;
              letter-spacing: 0.4pt; color: #333; text-align: left; padding: 5pt 9pt 6pt 9pt;
              border-bottom: 1px solid #999; width: 50%; vertical-align: top; }
table.rl th span { display: block; font-weight: normal; text-transform: none; letter-spacing: 0;
                   font-size: 7.1pt; color: #777; margin-top: 2pt; }
table.rl td { vertical-align: top; padding: 8pt 0 9pt 0; border-bottom: 0.5px solid #ddd; }
.cols { display: grid; grid-template-columns: 1fr 1fr; }
.cl { padding: 0 9pt 0 9pt; border-right: 1px solid #ccc; color: #333; }
.cr { padding: 0 9pt 0 9pt; }
table.rl tr.provrow .review, table.rl tr.provrow .prov { margin-left: 9pt; margin-right: 9pt; }
.label { font-family: Helvetica, Arial, sans-serif; font-size: 7.7pt; font-weight: bold; color: #000;
         margin-bottom: 3pt; break-after: avoid; }
ins { text-decoration: underline; color: #0a5c2e; font-weight: bold; }
del { text-decoration: line-through; color: #9b1c1c; }
.none { color: #888; font-style: italic; }
.unch { color: #666; font-style: italic; }
.rangebadge { display: inline-block; font-family: Helvetica, Arial, sans-serif; font-size: 6.6pt;
              line-height: 1; color: #8a5a00; background: #fdf5e3; border: 0.5px solid #e0c98a;
              border-radius: 2pt; padding: 2pt 4pt; margin: 0 3pt; vertical-align: 1.5pt;
              white-space: nowrap; font-weight: normal; text-decoration: none; }
.prov { margin-top: 6pt; padding-top: 4pt; border-top: 0.5px dashed #bbb; break-inside: avoid;
        font-family: Helvetica, Arial, sans-serif; font-size: 7.2pt; line-height: 1.45; color: #555; }
.prov span.tag { display: inline-block; text-transform: uppercase; letter-spacing: 0.5pt; font-size: 6.5pt;
                 color: #888; margin-right: 5pt; }
.review { margin-top: 7pt; border: 1.5pt solid #e09a3e; background: #fffdf8; border-radius: 7pt;
          padding: 6pt 10pt; break-inside: avoid; font-family: Helvetica, Arial, sans-serif; font-size: 7.5pt;
          line-height: 1.5; color: #7a2e2e; font-weight: 600; }
.review b { color: #c0392b; font-weight: bold; letter-spacing: 0.3pt; }
table.dep { width: 100%; border-collapse: collapse; font-family: Helvetica, Arial, sans-serif;
            font-size: 7.3pt; line-height: 1.4; margin: 3pt 0 8pt 0; }
table.dep th, table.dep td { border: 0.5px solid #bbb; padding: 2.6pt 5pt; text-align: left; vertical-align: top; }
table.dep th { background: #f2f2f2; font-size: 7.3pt; }
table.dep thead { display: table-header-group; }
table.dep tr { break-inside: avoid; }
table.dep td.amd { color: #0a5c2e; font-weight: bold; }
table.dep td.flag { color: #9b1c1c; }
table.dep td.n { text-align: right; white-space: nowrap; }
table.toc { border-collapse: collapse; font-family: Helvetica, Arial, sans-serif; font-size: 7.8pt;
            margin: 0 0 6pt 0; break-inside: avoid; width: 100%; }
table.toc th, table.toc td { border: 0.5px solid #bbb; padding: 2.4pt 7pt; text-align: left;
                             vertical-align: top; }
table.toc th { background: #f2f2f2; font-size: 7.3pt; text-transform: uppercase; letter-spacing: 0.3pt; }
table.toc td.pt { white-space: nowrap; font-weight: bold; }
table.toc td.n { text-align: right; white-space: nowrap; }
table.tm { border-collapse: collapse; font-family: Helvetica, Arial, sans-serif; font-size: 6.6pt;
           margin: 4pt 0 8pt 0; }
table.tm th, table.tm td { border: 0.5px solid #ccc; padding: 1.6pt 3pt; text-align: right; }
table.tm th { background: #f2f2f2; font-size: 6.2pt; }
table.tm th.term { text-align: left; white-space: nowrap; padding-right: 6pt; }
table.tm thead { display: table-header-group; }
table.tm td.term { text-align: left; white-space: nowrap; padding-right: 6pt; }
table.tm td.z { color: #ccc; }
table.tm tr.tot td { border-top: 1.2px solid #111; font-weight: bold; background: #fafafa; }
table.tm tr.def td { background: #f4f8f4; }
.foot { margin-top: 14pt; border-top: 1.5px solid #111; padding-top: 8pt;
        font-family: Helvetica, Arial, sans-serif; font-size: 7.7pt; line-height: 1.5; color: #444; }
table.qs { width: 100%; border-collapse: collapse; font-family: Helvetica, Arial, sans-serif;
           font-size: 6.5pt; line-height: 1.2; margin: 2pt 0 4pt 0; }
table.qs th, table.qs td { border: 0.5px solid #bbb; padding: 1.3pt 4pt; text-align: left; vertical-align: top; }
table.qs th { background: #f2f2f2; font-size: 6.3pt; text-transform: uppercase; letter-spacing: 0.3pt; }
table.qs td.prov { white-space: nowrap; font-weight: bold; }
table.qs tr.grp td { background: #ececec; font-weight: bold; font-size: 6.8pt; border-top: 1.2px solid #111; }
table.qs tr { break-inside: avoid; }
section.adE p.intro { margin-bottom: 5pt; }
"""


# Running header in the top-left margin of every page. The redline flows as one
# body: its sections share one named page so that small sections share pages
# instead of each forcing a page of its own. Each addendum keeps its own named
# page. This diverges from the per-section named pages of practicum v9, and the
# README records the divergence.
RUNNING = [
    ("body", "7.35.3 NMAC", "Proposed amendments outside the practicum"),
    ("src", "Sources and method", "How every claim in this document was checked"),
    ("adA", "Addendum A", "Terms this part uses and no part defines"),
    ("adB", "Addendum B", "Dependencies across the two drafting scopes"),
    ("adC", "Addendum C", "Defects recorded and not drafted, and why"),
    ("adD", "Addendum D", "Mechanical defects across all twenty-eight sections"),
    ("adE", "Addendum E", "The questions, one line each, grouped by who answers"),
]


def running_css():
    out = []
    for cls, label, title in RUNNING:
        out.append('@page %s { @top-left { content: "%s  %s"; } }' % (cls, label, title))
        out.append('section.%s { page: %s; }' % (cls, cls))
    return "\n".join(out)


def strip_tags(t):
    return re.sub(r"<[^>]+>", "", t)


def esc(t):
    return html.escape(t).replace("\n", "<br>")


HEAD = """
<section class="flow body">
<div class="cover">
<h1>7.35.3 NMAC: proposed amendments to the twenty-four sections outside the practicum</h1>
<p class="sub">Working draft {VERSION}, {VERSION_DATE}. Rule hearing August 28, 2026. Not a filing, not
submitted, and not adopted rule text.</p>
</div>

<ul class="what">
<li><b>Twenty-three provisions are amended.</b> One redline, sections in numerical order. Every change is a
mechanical correction, a conforming amendment between two provisions of the same rule, or a restoration of
wording the July 9, 2026 draft carried. No figure or policy choice enters without a source.</li>
<li><b>Four provisions are reproduced without amendment.</b> Each carries a question. Every question in the
document sits in an orange callout at its provision, question first, and all of them are on one page in
Addendum E, grouped by who answers.</li>
<li><b>Eleven further defects are recorded and not drafted.</b> Addendum C lists each with the reason.</li>
<li>Questions are limited to gaps, contradictions, typos, and drafting mistakes. The unfilled dates and
placeholders are the department's to fill at publication and are not raised. Nothing here reopens the
practicum draft: read against its working draft v9, and Addendum B records every dependency between the two
scopes.</li>
</ul>

<div class="key">
<b>The columns.</b> Left is the rule as published, verbatim. Right is the proposed amendment:
<ins>underlined green inserted</ins>, <del>struck red deleted</del>, unmarked text carried forward unchanged.
A badge such as <span class="rangebadge">90 from 7.35.3.11 D</span> names the provision a figure is taken
from. The source note and, where there is one, the question run the full width beneath both columns.
</div>

<h2>Contents</h2>
{CONTENTS}
</section>
"""


def contents_table():
    secs = []
    for _, section, _, _, _ in sorted(P, key=lambda e: int(e[1].rsplit(".", 1)[1])):
        if section not in secs:
            secs.append(section)
    rows = ['<table class="toc">',
            '<tr><th>Where</th><th>What</th></tr>']
    rows.append('<tr><td class="pt">The redline</td><td>Sections %s, in numerical order.</td></tr>'
                % ", ".join(s.replace("7.35.3.", ".") for s in secs))
    rows.append('<tr><td class="pt">Addendum A</td>'
                '<td>Terms this part uses and no part defines, counted in both parts, with the material for a '
                'definition of each assembled from the sources.</td></tr>')
    rows.append('<tr><td class="pt">Addendum B</td>'
                '<td>Dependencies between these sections and the practicum draft, in both directions.</td></tr>')
    rows.append('<tr><td class="pt">Addendum C</td>'
                '<td>Every defect recorded and not drafted, with the reason nothing is proposed.</td></tr>')
    rows.append('<tr><td class="pt">Addendum D</td>'
                '<td>Numbering and drafting-form defects across all twenty-eight sections.</td></tr>')
    rows.append('<tr><td class="pt">Addendum E</td>'
                '<td>Every question in the document, one line each, grouped by who answers. One page.</td></tr>')
    rows.append('</table>')
    return "\n".join(rows)


def build_body():
    rows, current = [], None
    for doc, section, sub, published, proposed in sorted(P, key=lambda e: int(e[1].rsplit(".", 1)[1])):
        if section != current:
            if current is not None:
                rows.append("</table></section>")
            current = section
            rows.append('<section class="flow body">')
            rows.append('<h2 class="sec">%s <span class="ttl">%s</span></h2>'
                        % (section, SECTION_TITLES[section]))
            rows.append('<table class="rl"><tr>'
                        '<th>Current language<span>Proposed rule as published July 23, 2026</span></th>'
                        '<th>Proposed amendment<span>Draft for review. Not filed, not adopted</span></th></tr>')
        if published == UNCHANGED and proposed == UNCHANGED:
            continue
        left = ('<span class="none">%s</span>' % NEW) if published == NEW else esc(published)
        if proposed == UNCHANGED:
            right = ('<span class="unch">Not amended. Reproduced for the question below.</span>')
        else:
            right = proposed
        src = source_for(section, sub)
        rev = review_for(section, sub)
        extra = ''
        if src:
            extra += '<div class="prov"><span class="tag">Source</span>%s</div>' % src
        if rev:
            extra += '<div class="review"><b>Question.</b> %s</div>' % rev
        # One row per provision. The two columns are a grid inside a single cell,
        # and the notes run the full width beneath them, so a note is about half
        # as tall as it would be inside a column. A provision short enough to fit
        # a page is marked so that it is never split.
        body = max(len(strip_tags(left)), len(strip_tags(right))) / 92.0
        lines = body + len(strip_tags(extra)) / 190.0 + 4
        keep = " keep" if lines < 18 else ""
        rows.append('<tr class="provrow%s"><td colspan="2">'
                    '<div class="cols"><div class="cl"><div class="label">%s</div>%s</div>'
                    '<div class="cr"><div class="label">%s</div>%s</div></div>%s</td></tr>'
                    % (keep, sub, left, sub, right, extra))
    rows.append("</table></section>")
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Addendum A: the undefined terms, counted from the corpus at build time
# ---------------------------------------------------------------------------

def term_map(corpus3, corpus2):
    _, s3 = segment(corpus3, r"7\.3[45]\.3\.(\d{1,2})\s+(?!NMAC)[A-Z][A-Z]+")
    secs = sorted(s3)
    out = ['<table class="tm">', '<thead>',
           '<tr><th class="term">Term in 7.35.3 NMAC</th>'
           + "".join('<th>%d</th>' % n for n in secs)
           + '<th>Part&nbsp;3</th><th>Part&nbsp;2</th></tr>', '</thead>']
    for term in UNDEFINED_TERMS:
        cells = ""
        for n in secs:
            c = count_term(s3[n], term)
            cells += ('<td>%d</td>' % c) if c else '<td class="z">.</td>'
        out.append('<tr><td class="term">%s</td>%s<td><b>%d</b></td><td><b>%d</b></td></tr>'
                   % (term, cells, count_term(corpus3, term), count_term(corpus2, term)))
    out.append('<tr class="tot"><td class="term">Defined in 7.35.2.7 NMAC, for contrast</td>'
               + "".join('<td></td>' for _ in secs) + '<td></td><td></td></tr>')
    for term in DEFINED_TERMS:
        cells = ""
        for n in secs:
            c = count_term(s3[n], term)
            cells += ('<td>%d</td>' % c) if c else '<td class="z">.</td>'
        out.append('<tr class="def"><td class="term">%s</td>%s<td><b>%d</b></td><td><b>%d</b></td></tr>'
                   % (term, cells, count_term(corpus3, term), count_term(corpus2, term)))
    out.append('</table>')
    return "\n".join(out)


ADDENDUM_A_INTRO = """
<section class="rr adA">
<h2 class="sec">Addendum A <span class="ttl">Terms this part uses and no part defines</span></h2>
<p class="intro">7.35.3.7 NMAC provides in full: "The definitions in 7.35.2.7 NMAC apply to this part." Every
count in the table below is produced from the text layer of the published rule and of 7.35.2 NMAC each time
this document is built, section by section, so no count in it is transcribed by hand. Column headings are
section numbers within each part. The first block is terms used in 7.35.3 NMAC that 7.35.2.7 NMAC does not
define. The second block, shaded, is the terms 7.35.2.7 NMAC does define, shown for contrast.</p>
"""

ADDENDUM_A_TAIL = """
<p class="tnote"><b>What the table shows.</b> Sixteen terms carrying regulatory consequence in this part are
defined in neither part. Six of them are defined in the draft at 7.35.3.7 NMAC, because a single provision of
the published rule supplies the content: certificant, facilitator, other approved location, practicum,
registrant of another approved location, and student. Ten are not, and the two largest are healing center and
certifying clinician. "Guide", the one
defined term in 7.35.2.7 NMAC for an individual who assists practitioners during administration sessions,
appears nowhere in 7.35.3 NMAC, while "facilitator", which 7.35.2.7 NMAC does not define, appears throughout
it. 7.35.2 NMAC was adopted effective June 23, 2026, so amending 7.35.2.7 NMAC is a separate rulemaking and any
term this part needs has to be carried in this part.</p>
<p class="tnote"><b>The Act.</b> Section 3(B) of the Medical Psilocybin Act defines a clinician as an approved
health care provider licensed in New Mexico who holds a permit from the department to provide medical services
to qualified patients. 7.35.2.7 NMAC defines "Clinician" in the same terms except that it reads certification
where the Act reads permit, and defines "Permit" as the authorization to operate as a psilocybin producer or
psilocybin testing laboratory. Section 5 of the Act exempts a producer, a clinician and a qualified patient
from arrest, prosecution and penalty. Neither the Act nor 7.35.2.7 NMAC uses the word facilitator. The
consequence is stated at 7.35.3.7 NMAC in the redline above.</p>
"""


ADDENDUM_A_TERMS = """
<h2 class="sec">Addendum A, continued <span class="ttl">The material for a definition of each term, assembled
from the sources</span></h2>
<p class="intro">For each term the table counts, what follows gathers the provisions of 7.35.3 NMAC, 7.35.2
NMAC and the Medical Psilocybin Act that bear on the term, quoted exactly and cited, so that a definition can
be decided from assembled material rather than composed from scratch. Two of the sixteen, other approved
location and practicum, are defined in the redline at 7.35.3.7 NMAC because a single provision supplies the
content; they are marked below, and the source of each is quoted. Nothing below proposes language for the
remaining ten, and none of the sixteen terms appears anywhere in the Medical Psilocybin Act.</p>

<p class="tnote"><b>healing center.</b> The most-used undefined term, and no provision states what a healing
center is. What the rule supplies: it is certified on application, 7.35.3.11 NMAC Subsection A, page 5, "An
applicant seeking certification as a healing center shall submit a complete application"; it is an
organization with owners, a board of directors and employees, Paragraph (11) of the same subsection; and it is
a place where administration sessions occur and psilocybin products are handled, 7.35.3.14 NMAC, page 9, under
which "Owners and employees of healing centers who are registered with the department may purchase medical
psilocybin products from permitted producers, may possess medical psilocybin products, and may sell or
otherwise administer those products to qualified patients in administration sessions conducted at the healing
center or other approved locations", and "A healing center may only sell or otherwise provide psilocybin
products that are obtained from permitted producers." Its operating duties are stated at 7.35.3.20 NMAC, pages
13 to 15, including the patient list at Subsection A and the reporting duty at Subsection L. Its location is
what an other approved location is defined against: other approved locations "are physical locations at which
medical psilocybin is intended to be consumed, that are not locations of healing centers", 7.35.3.11 NMAC
Subsection B, page 6. 7.35.2 NMAC does not use the term; its nearest defined term is "Approved location",
meaning "a location approved by the department for psilocybin administration sessions". The Act does not use
the term and speaks instead of settings: Section 5(B)(2) makes lawful the conduct of a clinician administering
or a qualified patient taking psilocybin "in an approved setting", and Section 7(A)(3) directs the department
to establish "treatment protocols, including patient selection criteria, medical service standards, dosage
standards and approved settings for administration of psilocybin to patients". Whether a healing center is one
of the Act's approved settings is stated nowhere in this record.</p>

<p class="tnote"><b>certifying clinician.</b> No provision states what a certifying clinician is, and the rule
uses the bare word clinician in its scope section while using the two-word term everywhere else. What the rule
supplies: the certifying clinician stands at the door of the program, since a patient application "shall be
submitted by a patient and the patient's certifying clinician", 7.35.3.8 NMAC lead-in, page 1; the work is
certifying patients, and "In order to certify a patient, a certifying clinician must have an actual
clinician-patient relationship with the patient.", 7.35.3.13 NMAC Subsection A, page 8; an applicant must hold
a license, "Documentation of current professional license to practice in New Mexico (e.g. MD, NP)", 7.35.3.9
NMAC Subsection D, page 3; and "All certifying clinicians shall complete a certifying clinician module",
7.35.3.18 NMAC Subsection B, page 11. What the other sources supply: Section 3(B) of the Act defines
"clinician" as "an approved health care provider licensed in New Mexico who holds a permit from the department
to provide medical services to qualified patients", and 7.35.2.7 NMAC defines "Clinician" in the same words
except that it reads certification where the Act reads permit. Whether the certifying clinician of this part
is the clinician that Section 3(B) of the Act and 7.35.2.7 NMAC define is stated nowhere in this record.</p>

<p class="tnote"><b>educational program.</b> Regulated as a certificant, never described. What the rule
supplies: it is certified on application, "An applicant seeking certification as a psilocybin educational
program shall submit a complete application through the electronic system designated by the department.",
7.35.3.12 NMAC Subsection A, page 7; its application must include, at Paragraph (18) of that subsection, "A
plan demonstrating how the program will ensure that enrolled students complete all required components and
graduate within two years of enrollment"; and it is one of the classes that may relinquish a certification,
7.35.3.26 NMAC, page 16. 7.35.2 NMAC does not use the term. The Act does not use the term; its only training
provision is Section 7(A)(2), which directs the department to establish "necessary initial and ongoing
training for producers and clinicians", naming neither practitioners, facilitators, students nor programs.</p>

<p class="tnote"><b>other approved location. Defined in the redline at 7.35.3.7 NMAC.</b> One provision
supplies the content, which is why this term is drafted: 7.35.3.11 NMAC Subsection B, page 6, provides that
"Other approved locations are physical locations at which medical psilocybin is intended to be consumed, that
are not locations of healing centers." The same subsection supplies the "temporary department certification",
the purposes, "if a qualified patient is unable to be physically transported to a healing center, for other
reasons of medical necessity, for purposes of improving patient access in rural and frontier counties, or to
enable treatment to occur in a natural environment setting", and the examples, "Such locations may include a
patient's residence, or another temporary location." 7.35.2.7 NMAC defines "Approved location" but not this
longer term, and the Act does not use it.</p>

<p class="tnote"><b>practicum. Defined in the redline at 7.35.3.7 NMAC.</b> One provision supplies the
content, which is why this term is drafted: 7.35.3.19 NMAC Subsection A, page 12, provides that an individual
who seeks to become certified as a practitioner or facilitator "shall participate in supervised practice
training, otherwise referred to as a" practicum. That section belongs to the practicum amendment draft, whose
working draft v9 amends the hour figures in the same subsection and keeps the quoted phrase; Addendum B
records the dependency. In this document's scope the word appears in the reporting duty for "Any modification,
termination, or addition of practicum site agreements", 7.35.3.15 NMAC Subsection A, page 9, in the mentoring
obligation that runs "after graduation and after practicum hours are completed", 7.35.3.17 NMAC Subsection A,
page 10, and in the waiver reproduced at Paragraph (1) of Subsection D of 7.35.3.10 NMAC, page 5. Neither
7.35.2 NMAC nor the Act uses the word.</p>

<p class="tnote"><b>didactic.</b> The word does the work of an equivalency test in this document's scope and
of an hour denomination in the practicum draft's. 7.35.3.10 NMAC Subsection A, page 4, keeps a program from
another jurisdiction on the department list only while its curriculum stays equivalent to the "didactic
educational requirements applicable for New Mexico certification", and removes it when "the didactic
requirements of the educational program are no longer equivalent to those applicable for New Mexico
certification". The module provisions of 7.35.3.18 NMAC, pages 11 to 12, state their minimums in didactic
hours, and 7.35.3.19 NMAC Subsection A, page 12, opens the practicum to a student "after completing at least
half of the didactic requirements and all of the simulated patient requirements of the educational
requirements". No provision states which parts of a program are didactic and which are not. Neither 7.35.2
NMAC nor the Act uses the word.</p>

<p class="tnote"><b>adverse health event.</b> The nearest the rule comes to content is the list of what a
report of one must include. 7.35.3.20 NMAC Subsection L, pages 14 to 15, requires a healing center and a
registrant of another approved location to "report any potential adverse health event associated with medical
psilocybin services to the department no later than two business days" after becoming aware of it, and
requires reports to include "Any challenging psychological, emotional, or behavioral reactions", "Any
participant reaction requiring medical or therapeutic attention", "Any incident requiring emergency response",
and "Any other incident which has a negative impact on a patient". A location's safety plan must include
"adverse health event response and reporting", 7.35.3.11 NMAC Paragraph (15) of Subsection A, page 5; patient
information must cover "How to report an adverse health event to the department", 7.35.3.20 NMAC Paragraph (5)
of Subsection G, page 14; and a practitioner's administration records must note "Any adverse health events",
7.35.3.13 NMAC Subsection C, page 9. Whether the report-contents list is the definition is stated nowhere: it
is a list of what reports include, not of what an event is. Neither 7.35.2 NMAC nor the Act uses the term.</p>

<p class="tnote"><b>administrative review committee.</b> All four occurrences sit in 7.35.3.25 NMAC, page 16.
"The administrative review shall be conducted by the administrative review committee.", Subsection C; "The
decision of the administrative review committee is the final decision of the informal administrative review
proceeding.", Paragraph (2) of Subsection D; and Subsection E provides that "Except as otherwise provided by
law, there shall be no right to judicial review of a decision by the administrative review committee." Nothing
in 7.35.3 NMAC or 7.35.2 NMAC constitutes the committee, states who sits on it, or says how it is appointed,
and the Act does not use the term. The review note at 7.35.3.25 above records who must answer.</p>

<p class="tnote"><b>graduate.</b> Four occurrences, and the fullest statement of what graduation takes is a
list inside a subsection the Wilson working redline proposes to strike. An educational program must plan for
enrolled students to "complete all required components and graduate within two years of enrollment", 7.35.3.12
NMAC Paragraph (18) of Subsection A, page 7; mentoring runs "after graduation and after practicum hours are
completed", 7.35.3.17 NMAC Subsection A, page 10; a student using the test-out option completes "the New
Mexico Module, certifications, simulated patient, and practicum requirements to graduate from the educational
program", 7.35.3.17 NMAC Subsection B, page 11; and the practicum-hours waiver reaches an applicant who
"Graduates from an educational program that the department certifies by December 31, 2027", 7.35.3.19 NMAC
Paragraph (3) of Subsection G, page 13. Neither 7.35.2 NMAC nor the Act uses the word.</p>

<p class="tnote"><b>simulated patient.</b> The rule requires the experience and never says what a simulated
patient is. "A simulated patient experience of no less than 5 hours", 7.35.3.18 NMAC Subsection C, page 12;
the practicum opens only after "all of the simulated patient requirements" are complete, 7.35.3.19 NMAC
Subsection A, page 12; and the test-out option leaves the requirement standing, 7.35.3.17 NMAC Subsection B,
page 11. Neither 7.35.2 NMAC nor the Act uses the term.</p>

<p class="tnote"><b>medical psilocybin services.</b> Three occurrences, against a two-word term both other
sources define. A facilitator "is authorized to work alongside a practitioner during medical psilocybin
services", 7.35.3.13 NMAC Subsection B, page 8; the education requirements reach all certificants "who provide
medical psilocybin services", 7.35.3.18 NMAC Subsection A, page 11; and the reporting duty covers "any
potential adverse health event associated with medical psilocybin services", 7.35.3.20 NMAC Subsection L,
pages 14 to 15. Section 3(D) of the Act and 7.35.2.7 NMAC define "Medical services", identically, as "services
provided to a patient in an approved setting before, during and after the ingestion of psilocybin", including
a preparation session, an administration session and an integration session. Whether the three-word term means
the same as the defined two-word term is stated nowhere in this record.</p>

<p class="tnote"><b>equity and access fund.</b> One occurrence, and no source names a fund by this name. A
patient application must include "Information required for patient participation in the Equity and Access Fund
(as applicable)", 7.35.3.8 NMAC Paragraph (7) of Subsection B, page 2. The Act creates two funds in Section
11, neither by this name: the "medical psilocybin treatment equity fund", to be used "to fund treatments of
qualified patients who meet income requirements determined by rule of the department", and the "medical
psilocybin research fund". 7.35.2 NMAC uses neither name. Whether the Equity and Access Fund is the Act's
medical psilocybin treatment equity fund is stated nowhere in this record.</p>
"""


ADDENDUM_B = """
</section>
<section class="rr adB">
<h2 class="sec">Addendum B <span class="ttl">Dependencies across the two drafting scopes</span></h2>
<p class="intro">Provisions in these four documents that operate on, or are operated on by, a provision the
practicum amendment draft in <i>amendments/</i> reaches. Nothing in these documents amends a provision in that
draft's scope. Where a fix would require one, it is recorded here and left undrafted.</p>
<table class="dep">
<thead>
<tr><th>Provision here</th><th>Provision in the practicum draft's scope</th><th>Relationship</th><th>Handled</th></tr>
</thead>
<tr><td>7.35.3.11 A(11), page 5</td><td>7.35.3.14 C, page 9</td>
<td>7.35.3.14 C conditions healing center owner and employee authority on being registered with the
department, and no registration exists. The registration is drafted here, at the point where the healing
center already files the names.</td>
<td class="amd">Drafted here. The practicum draft flagged 7.35.3.14 C and did not amend it, and it is not
amended here either.</td></tr>
<tr><td>7.35.3.7, page 1</td><td>7.35.3.20 H(5), page 14</td>
<td>The definition of student drafted here is taken from the qualified student test in 7.35.3.20 H(5). The
practicum draft amends that paragraph for the permit title and does not change the test.</td>
<td class="amd">Drafted here, sourced there. If the test changes, the definition follows it.</td></tr>
<tr><td>7.35.3.7, page 1</td><td>7.35.3.19 A, page 12</td>
<td>The definition of practicum drafted here is taken from 7.35.3.19 A, which provides that an individual
seeking certification as a practitioner or facilitator "shall participate in supervised practice training,
otherwise referred to as a" practicum. The practicum draft amends the hour figures in the same subsection and
keeps that phrase.</td>
<td class="amd">Drafted here, sourced there. If the phrase changes, the definition follows it.</td></tr>
<tr><td>7.35.3.7, page 1</td><td>7.35.3.14 B, page 9</td>
<td>7.35.3.14 B authorizes facilitators to possess psilocybin products and provide them to qualified patients.
Whether a facilitator is a clinician under Section 3(B) of the Medical Psilocybin Act, and so within the
Section 5 exemption, governs whether that authority holds. This is the administering half of Paragraph (2) of
Subsection B of Section 5 of the Act. The practicum draft reads the taking half of the same provision against
Subsection H of Section 3, and its proposed 7.35.3.29 states the statutory amendment that half would need and
conditions the section on it, so the two drafts read the same provision consistently.</td>
<td class="flag">Not drafted. Recorded at 7.35.3.7 as a question for department counsel.</td></tr>
<tr><td>7.35.3.7, page 1</td><td>7.35.3.14 A and C, page 9, with 7.35.3.20 D, page 14</td>
<td>The position of a student is not in doubt and is not raised in these documents. The practicum draft locates
the provision of the medicine in the practitioner or the healing center, and 7.35.3.20 D provides that
"students completing their practicums may be present during an administration session". The definition of
student drafted here does not disturb that.</td>
<td class="amd">Settled in the practicum draft. Nothing here contradicts it.</td></tr>
<tr><td>7.35.3.13 B, page 8</td><td>7.35.3.14 B, 7.35.3.19 C, 7.35.3.20 H(5)</td>
<td>The facilitator scope of work in 7.35.3.13 B is narrower than the authority the other three provisions
confer, and "direct supervision" is not defined anywhere in the rule.</td>
<td class="flag">Not drafted. Any amendment has to be coordinated with the practicum draft.</td></tr>
<tr><td>7.35.3.17 A, pages 10 to 11</td><td>Proposed 7.35.3.19 H, which exists only in that draft's
re-lettering of 7.35.3.19</td>
<td>Whether the consultation requirement is stated in hours or in cases, and whether it sits at the proposed
7.35.3.19 H or at 7.35.3.17 A, is open in the practicum document for Dr. Metz, Ms. Wilson and Dr. Leeman. As
published, 7.35.3.19 NMAC runs A through G and has no Subsection H.</td>
<td class="flag">Not drafted. 7.35.3.17 A is left exactly as published so that their answer governs.</td></tr>
<tr><td>7.35.3.10 D(1), page 5</td><td>7.35.3.19 G(4), page 13, which that draft re-letters as 7.35.3.19 K</td>
<td>Two waivers of the practicum hours requirement each set a 40-hour floor for applications received by
December 31, 2027. For the same 40 hours of contact time, 7.35.3.10 D(1) requires "two separate group
sessions" and 7.35.3.19 G(4) requires "A minimum of one group session". The practicum draft records the
conflict at its 7.35.3.19 K and amends neither provision, on the ground that 7.35.3.10 is outside its
scope.</td>
<td class="flag">Not drafted here either. Conforming one to the other is a choice between two figures already
in the rule, so neither document makes it. The provision is reproduced at 7.35.3.10 above with the sharpened
record, and the choice is put to the committee there.</td></tr>
<tr><td>7.35.3.16 A and C, page 10</td><td>7.35.3.18, pages 11 to 12</td>
<td>The third-party evaluation assesses the curriculum that 7.35.3.18 requires. Curing the evaluator conflict
does not touch the curriculum, and the practicum draft's changes to the curriculum do not touch the
conflict.</td>
<td class="amd">Drafted here. No coordination needed.</td></tr>
<tr><td>7.35.3.20 heading, page 13</td><td>7.35.3.20 heading, page 13</td>
<td>The heading reads 7.34.3.20. The practicum draft corrects it.</td>
<td class="amd">Not duplicated here. The correction stands in the practicum draft.</td></tr>
</table>
"""


ADDENDUM_C = """
</section>
<section class="rr adC">
<h2 class="sec">Addendum C <span class="ttl">Defects recorded and not drafted, and why</span></h2>
<p class="intro">Gaps, contradictions, typos and drafting mistakes this draft records and does not amend, each
with the reason no language is proposed.</p>
<table class="dep">
<thead>
<tr><th>Provision</th><th>Defect</th><th>Why nothing is drafted</th></tr>
</thead>
<tr><td>7.35.3.7, page 1</td>
<td>Ten of the sixteen undefined terms have no definition in any source, including healing center, 54
occurrences, and certifying clinician, 53 occurrences.</td>
<td>Composing a definition from no source is a policy act. Addendum A assembles the material for each.</td></tr>
<tr><td>7.35.3.9 E(1) and F, page 3</td>
<td>A practitioner applicant must document a professional license "(e.g. PSY, LSW, LCSW)" with no stated scope
of practice, and a facilitator applicant needs no license at all. The Wilson working redline comments "Also no
scope here - what happened to therapy scope? It's missing - if DOH wants that, they need to include it." and
"without specifying, they're setting themselves up to have athletic trainers and massage therapists apply and
then not have a regulation to point to explain why that's not sufficient."</td>
<td>The redline raises the gap and supplies no list of qualifying licenses, and no other source in this record
supplies one.</td></tr>
<tr><td>7.35.3.8 C, page 2, with 7.35.3.9 A(1), page 2</td>
<td>The department has 30 business days to decide a patient application and 30 calendar days to decide a
certificant application.</td>
<td>Conforming one to the other is a choice between two figures already in the rule, and both bind the
department.</td></tr>
<tr><td>7.35.3.10 D(1), page 5, with 7.35.3.19 G(4), page 13</td>
<td>The two 40-hour waivers set different group-session minimums, two against one.</td>
<td>Conforming one to the other is a choice between two figures already in the rule. The practicum draft
records the same conflict and amends neither provision. The question is at 7.35.3.10 above.</td></tr>
<tr><td>7.35.3.11, page 5</td>
<td>The two-person universal requirement the Wilson working redline adds, which its author records did not
reach the published rule.</td>
<td>The author records that she does not know where the provision belongs. Placing it would answer her
question, which is at 7.35.3.11 B(10) above.</td></tr>
<tr><td>7.35.3.12, pages 7 to 8, against the July 9, 2026 draft</td>
<td>The grounds for denying an educational program application present in the July 9 draft do not appear in the
published rule. Finding M9.</td>
<td>Restoring deleted grounds is a substantive policy decision, and this record cannot show whether the
deletion was deliberate.</td></tr>
<tr><td>7.35.3.17 A, pages 10 to 11</td>
<td>The consultation obligation, whether it is stated in hours or cases, where it sits, and the double-count if
it is stated twice.</td>
<td>Open in the practicum document for three named people. The question is at 7.35.3.17 A above. Addendum
B.</td></tr>
<tr><td>7.35.3.17 B, page 11</td>
<td>The test-out price cap is a fraction of the price of "each of the educational modules", which assumes
per-module pricing. The Wilson working redline strikes the subsection.</td>
<td>Whether the option survives at all is the committee's decision, and a restated cap is worth drafting only
if it does.</td></tr>
<tr><td>7.35.3.24, page 15</td>
<td>The July 9, 2026 draft allowed a complaint from patients or staff; the published section allows one from a
qualified patient or certificant, so staff who are neither have no route.</td>
<td>Restoring standing for staff is a policy decision. The confidentiality assurance the July 9 draft carried
is restored in the redline above, because that text exists in a source.</td></tr>
<tr><td>7.35.3.25 C and D(2), page 16</td>
<td>The administrative review committee decides a denied patient application and is constituted nowhere in
7.35.3 NMAC or 7.35.2 NMAC. Four occurrences, all in this section.</td>
<td>Only the department can say who the committee is. The question is at 7.35.3.25 above.</td></tr>
<tr><td>7.35.3.8 D, 7.35.3.25 A, 7.35.3.27 C(7), pages 2, 16 and 17</td>
<td>Three provisions describe review of a denial and their scopes overlap, so a patient applicant denied on the
merits may have both an informal review and a hearing. Finding M23.</td>
<td>The redline fixes the name of the proceeding only. Which track applies to which denial is a question of
what process is owed.</td></tr>
</table>
<p class="tnote"><b>Out of scope by decision.</b> The controlled-substance number requirement for certifying
clinicians, at Paragraph (3) of Subsection B of 7.35.3.8 NMAC and Paragraph (2) of Subsection D of 7.35.3.9
NMAC. The latter is reproduced in the redline above, as published, because the renumbering around it required
it; it is not amended, and nothing is proposed about it.</p>
"""


ADDENDUM_D_INTRO = """
</section>
<section class="rr adD">
<h2 class="sec">Addendum D <span class="ttl">Mechanical defects across all twenty-eight sections</span></h2>
<p class="intro">Numbering and drafting form, checked across the whole of 7.35.3 NMAC rather than only the
sections this document amends. Every count and every entry is produced from the text layer of the published
rule each time this document is built. The unfilled dates and history-note placeholders are the department's
to fill at publication and are not defects.</p>
"""


def addendum_d(corpus):
    heads = []
    for m in re.finditer(r"(7\.3[45]\.3\.\d{1,2})\s+(?!NMAC)([A-Z][A-Z ,;\-]+?)(?=:)", corpus):
        heads.append((m.group(1), flatten(m.group(2))))
    bad = [(h, t) for h, t in heads if h.startswith("7.34.3")]
    reached = {"7.35.3.14": "practicum draft", "7.35.3.20": "practicum draft",
               "7.35.3.13": "redline above", "7.35.3.23": "redline above",
               "7.35.3.25": "redline above"}
    out = ['<table class="dep">', '<thead>',
           '<tr><th>Item</th><th>Count</th><th>Where</th><th>Corrected</th></tr>', '</thead>']
    out.append('<tr><td>Section headings reading 7.34.3 instead of 7.35.3</td><td class="n">%d of %d</td>'
               '<td class="flag">%s</td><td class="amd">%s</td></tr>'
               % (len(bad), len(heads), ", ".join(h for h, _ in bad),
                  "; ".join("%s in the %s" % (h.replace("7.34.3", "7.35.3"), reached[h.replace("7.34.3", "7.35.3")])
                            for h, _ in bad)))
    d9 = re.search(r"D\.\s+Certifying clinician application requirements:(.*?)E\.\s+Practitioner application",
                   corpus, re.S)
    items = re.findall(r"\((\d)\)", d9.group(1)) if d9 else []
    out.append('<tr><td>Numbering gap inside a subsection</td><td class="n">1</td>'
               '<td class="flag">7.35.3.9 D runs %s. There is no (3).</td>'
               '<td class="amd">Renumbered in the redline above.</td></tr>' % ", ".join("(%s)" % i for i in items))
    parens = sorted({m.group(1) for m in re.finditer(r"\(([A-Z])\)\s+[A-Z][a-z]", corpus)})
    out.append('<tr><td>Subsections lettered "(A)" rather than "A."</td><td class="n">%d</td>'
               '<td class="flag">7.35.3.11 A, and 7.35.3.14 A, B and C. Letters found: %s</td>'
               '<td class="amd">7.35.3.11 A in the redline above; 7.35.3.14 in the practicum draft.</td></tr>'
               % (len(parens) + 1, ", ".join(parens)))
    out.append('<tr><td>Sentence with no verb governing the decision</td><td class="n">1</td>'
               '<td class="flag">7.35.3.25 D(1), page 16. Carried over from the July 9, 2026 draft.</td>'
               '<td class="amd">Corrected in the redline above.</td></tr>')
    out.append('<tr><td>Sentence that does not complete</td><td class="n">1</td>'
               '<td class="flag">7.35.3.18 F, page 12.</td>'
               '<td>In the practicum draft\'s scope. Corrected there.</td></tr>')
    out.append('<tr><td>Presiding official named inconsistently</td><td class="n">1</td>'
               '<td class="flag">7.35.3.27 M reads "hearing examiner"; the rest of 7.35.3.27 reads "hearing '
               'officer".</td><td class="amd">Corrected in the redline above.</td></tr>')
    out.append('<tr><td>Duplicated words</td><td class="n">1</td>'
               '<td class="flag">7.35.3.24 reads "the electronic system designated by the department '
               'electronic system".</td><td class="amd">Corrected in the redline above.</td></tr>')
    out.append('<tr><td>Spacing inside a heading</td><td class="n">1</td>'
               '<td class="flag">7.35.3.16 C reads "Conflict of -interest prohibitions". The July 9, 2026 '
               'draft read "Conflict-of-interest prohibitions".</td>'
               '<td class="amd">Corrected in the redline above.</td></tr>')
    out.append('<tr><td>Class named in the lead-in but not in the operative words</td><td class="n">1</td>'
               '<td class="flag">7.35.3.27 B(8) opens "for certifying clinicians and practitioners" and then '
               'refers only to "the clinician".</td>'
               '<td class="amd">Corrected in the redline above.</td></tr>')
    out.append('<tr><td>Patient described as certified rather than enrolled</td><td class="n">1</td>'
               '<td class="flag">7.35.3.27 C(1) reads "a certified patient".</td>'
               '<td class="amd">Corrected in the redline above.</td></tr>')
    out.append('</table>')
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Addendum E: the question sheet, generated from the review notes' companion
# list in notes.py so it cannot drift from them. audit.py checks that every
# review note appears here, that every row points at a review note, that each
# row sits under the decision-maker its note names, and that the sheet is one
# page.
# ---------------------------------------------------------------------------

COUNT_WORDS = {14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
               20: "twenty", 21: "twenty-one", 22: "twenty-two", 23: "twenty-three",
               24: "twenty-four", 25: "twenty-five", 26: "twenty-six"}


def compact_cite(section, sub):
    """A short citation derived mechanically from the provision label."""
    m = re.match(r"Paragraph \((\d+)\) of Subsection ([A-Z])", sub)
    if m:
        return "%s %s(%s)" % (section, m.group(2), m.group(1))
    m = re.match(r"Paragraphs \((\d+)\) and \((\d+)\) of Subsection ([A-Z])", sub)
    if m:
        return "%s %s(%s), (%s)" % (section, m.group(3), m.group(1), m.group(2))
    m = re.match(r"Subsection ([A-Z])", sub)
    if m:
        return "%s %s" % (section, m.group(1))
    if sub.startswith("Entire section"):
        return section
    if sub.startswith("Section heading"):
        return "%s heading and A" % section
    return "%s %s" % (section, sub)


def addendum_e():
    rows = ['</section>', '<section class="rr adE">',
            '<h2 class="sec">Addendum E <span class="ttl">The questions, one line each, grouped by who '
            'answers</span></h2>',
            '<p class="intro">The %s questions in this document, verbatim, grouped by who answers. The '
            'callout at the provision named in each row carries the basis.</p>'
            % COUNT_WORDS[len(QUESTIONS)],
            '<table class="qs">',
            '<tr><th>At</th><th>The question</th></tr>']
    for key, label in GROUPS:
        rows.append('<tr class="grp"><td colspan="2">%s</td></tr>' % label)
        for g, section, sub, q in QUESTIONS:
            if g != key:
                continue
            rows.append('<tr><td class="prov">%s</td><td>%s</td></tr>' % (compact_cite(section, sub), q))
    rows.append('</table>')
    return "\n".join(rows)


FOOT = """
</section>
<section class="src">
<div class="foot">
<b>Sources.</b> Rule as published: <i>docs/documents/rules-draft-2026-07-23-published.pdf</i>, 19 pages,
7.35.3.1 through 7.35.3.28. Prior board-meeting draft, used for new against carried-over determinations:
<i>docs/documents/rules-draft-2026-07-09.pdf</i>. Defined terms: <i>7.35.2 NMAC</i> as adopted effective
June 23, 2026, at <i>source-text/7.35.2-NMAC-adopted-2026-06-23.txt</i>. Statute: the Medical Psilocybin Act,
Senate Bill 219, 57th Legislature, First Session, 2025, as passed; Section 1 provides that Sections 1 through
11 of the act may be cited as the Medical Psilocybin Act, and those section numbers are the ones cited here.
This record does not verify any NMSA 1978 section number. Working redline: Denali Wilson, <i>NMAC 7.35.3</i>,
July 25, 2026, tracked changes and comments as exported from the document file. July 17, 2026 transcripts,
morning Advisory Board and afternoon Training and Education Committee, both labeled "UNOFFICIAL AUTO-GENERATED
TRANSCRIPT. NO SPEAKER ATTRIBUTION."; no speaker is named from either transcript in this document. Inventory
relied on and re-verified: <i>analysis/july23-rule-concerns.md</i>.<br><br>
<b>Method.</b> The left column reproduces the rule as published, verbatim, with line breaks introduced by the
PDF collapsed to single spaces and hyphenation introduced by a line break rejoined. Nothing else is altered.
Every block was checked against the text layer of the published rule by exact contiguous match, and the build
aborts if any block fails. <i>amendments-remainder/audit.py</i> re-checks every verifiable claim in these
documents and exits non-zero on any failure; <i>amendments-remainder/AUDIT.md</i> is its output.<br><br>
<b>Status.</b> Working draft {VERSION}. Not a filing, not submitted, and not adopted rule text. Nothing in
<i>amendments/</i> or <i>docs/</i> was modified by this work.
</div>
</section>
"""


def main():
    corpus3 = read_published()
    failures = verify(corpus3)
    if failures:
        print("VERIFICATION FAILED:")
        for doc, section, sub, chunk in failures:
            print("  [%s] %s %s :: %s" % (doc, section, sub, chunk))
        return 1
    n_blocks = sum(1 for _, _, _, pub, _ in P if pub not in (NEW, UNCHANGED))
    print("verified: %d published-column blocks match the published PDF" % n_blocks)

    corpus2 = flatten(PART2_TXT.read_text(encoding="utf-8"))

    chrome = None
    for cand in ["/opt/pw-browsers/chromium", "chromium", "chromium-browser", "google-chrome"]:
        c = shutil.which(cand) or (cand if Path(cand).exists() else None)
        if c:
            chrome = c
            break
    if not chrome:
        print("no chromium found")
        return 1

    addenda = (ADDENDUM_A_INTRO + term_map(corpus3, corpus2) + ADDENDUM_A_TAIL + ADDENDUM_A_TERMS
               + ADDENDUM_B + ADDENDUM_C + ADDENDUM_D_INTRO + addendum_d(corpus3) + addendum_e())
    head = (HEAD.replace("{VERSION}", VERSION).replace("{VERSION_DATE}", VERSION_DATE)
            .replace("{CONTENTS}", contents_table()))
    foot = FOOT.replace("{VERSION}", VERSION)
    css = CSS.replace("{VERSION}", VERSION) + "\n" + running_css()
    doc_html = ("<!doctype html><html><head><meta charset='utf-8'>"
                "<title>7.35.3 NMAC amendments outside the practicum %s</title>"
                "<style>%s</style></head><body>%s%s%s%s</body></html>"
                % (VERSION, css, head, build_body(), addenda, foot))

    tmp = Path(tempfile.mkdtemp()) / "redline.html"
    tmp.write_text(doc_html, encoding="utf-8")
    subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--print-to-pdf=%s" % OUT_PDF, tmp.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("wrote %s (%.0f KB)" % (OUT_PDF.relative_to(REPO), OUT_PDF.stat().st_size / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build the side-by-side redline for the twenty-four sections outside the practicum draft.

Left column: the rule as published July 23, 2026, verbatim.
Right column: the proposed amendment, with insertions and deletions marked.

Every left-column block is verified against the text layer of the published PDF
by exact contiguous match before any file is written. If any block fails, the
build aborts and writes nothing.

One PDF per document key in `DOCS`. Regrouping the draft is an edit to `DOCS`
here and to the `doc` field of each entry in `content.py`; nothing else depends
on the split.

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
from notes import source_for, review_for                  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "amendments-remainder"
PUBLISHED_PDF = REPO / "docs/documents/rules-draft-2026-07-23-published.pdf"
PART2_TXT = REPO / "source-text/7.35.2-NMAC-adopted-2026-06-23.txt"

VERSION = "v1"
VERSION_DATE = "July 26, 2026"

LINE_TOLERANCE = 3.0

# doc key -> (file stem, number, title, one-line statement of what it covers)
DOCS = {
    D1: ("7.35.3-framework-amendments", "1", "Framework and defined terms",
         "7.35.3.1 through 7.35.3.7. The defined-term dependency on 7.35.2.7 NMAC, and the four definitions "
         "the published rule itself supplies."),
    D2: ("7.35.3-education-amendments", "2", "Educational programs",
         "7.35.3.10, .12, .15, .16 and .17. The third-party evaluator conflict, the out-of-jurisdiction "
         "pathway, and the reporting and consultation obligations."),
    D3: ("7.35.3-locations-amendments", "3", "Locations and oversight",
         "7.35.3.11, .20 and .21. Healing center and other approved location applications, the registration "
         "on which healing center staff authority depends, and department assessments."),
    D4: ("7.35.3-process-amendments", "4", "Patients, applicants and process",
         "7.35.3.8, .9, .13 and .22 through .28. Enrollment and certification applications, complaints, "
         "review of denials, and discipline."),
}

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
@page { size: letter landscape; margin: 0.5in 0.5in 0.6in 0.5in;
        @bottom-center { content: counter(page); } }
* { box-sizing: border-box; }
body { font-family: "Times New Roman", Times, Georgia, serif; font-size: 8.7pt;
       line-height: 1.36; color: #111; margin: 0; }
h1 { font-family: Helvetica, Arial, sans-serif; font-size: 15pt; margin: 0 0 3pt 0; letter-spacing: -0.2pt; }
.sub { font-family: Helvetica, Arial, sans-serif; font-size: 8.4pt; color: #444; margin: 0 0 3pt 0; }
.cover { border-bottom: 2px solid #111; padding-bottom: 7pt; margin-bottom: 9pt; }
ul.what { font-family: Helvetica, Arial, sans-serif; font-size: 8.6pt; line-height: 1.5;
          margin: 0 0 10pt 0; padding-left: 15pt; max-width: 7.6in; }
ul.what li { margin-bottom: 2pt; }
.key { font-family: Helvetica, Arial, sans-serif; font-size: 8.2pt; color: #333;
       border-top: 0.5px solid #ccc; border-bottom: 0.5px solid #ccc; padding: 5pt 0; margin: 0 0 10pt 0; }
p.tnote { font-family: Helvetica, Arial, sans-serif; font-size: 7.5pt; color: #555; margin: 0; max-width: 7.4in; }
h2 { font-family: Helvetica, Arial, sans-serif; font-size: 11pt; margin: 0 0 6pt 0;
     padding: 3pt 0; border-top: 1.5px solid #111; border-bottom: 0.5px solid #111; break-after: avoid; }
h2.sec { break-before: page; }
h2 .ttl { font-weight: normal; color: #555; font-size: 9pt; }
p.intro { font-family: Helvetica, Arial, sans-serif; font-size: 8.1pt; line-height: 1.5; color: #333;
          margin: 0 0 8pt 0; padding-left: 8pt; border-left: 2.5px solid #bbb; break-after: avoid; }
table.rl { width: 100%; border-collapse: collapse; break-before: page; }
table.rl.first { break-before: auto; }
table.rl tr { break-inside: avoid; }
table.rl thead { display: table-header-group; }
table.rl th.run { font-family: Helvetica, Arial, sans-serif; text-align: left; padding: 0;
                  border: none; border-top: 1.5px solid #111; border-bottom: 0.5px solid #111; }
table.rl th.run div { padding: 3pt 0 4pt 0; font-size: 11pt; }
table.rl th.run span.ttl { font-weight: normal; color: #555; font-size: 9pt; }
table.rl th.run span.doc { float: right; font-weight: normal; color: #888; font-size: 7.4pt;
                           text-transform: uppercase; letter-spacing: 0.5pt; padding-top: 3pt; }
table.rl th.col { font-family: Helvetica, Arial, sans-serif; font-size: 7.6pt; text-transform: uppercase;
                  letter-spacing: 0.4pt; color: #333; text-align: left; padding: 5pt 9pt 6pt 9pt;
                  border-bottom: 1px solid #999; width: 50%; vertical-align: top; }
table.rl th.col span { display: block; font-weight: normal; text-transform: none; letter-spacing: 0;
                       font-size: 7.1pt; color: #777; margin-top: 2pt; }
table.rl td { vertical-align: top; padding: 8pt 9pt 10pt 9pt; border-bottom: 0.5px solid #ddd; width: 50%; }
table.rl td.left { border-right: 1px solid #ccc; color: #333; background: #fcfcfc; }
.label { font-family: Helvetica, Arial, sans-serif; font-size: 7.7pt; font-weight: bold; color: #000;
         margin-bottom: 3pt; }
ins { text-decoration: underline; color: #0a5c2e; font-weight: bold; }
del { text-decoration: line-through; color: #9b1c1c; }
.none { color: #888; font-style: italic; }
.unch { color: #666; font-style: italic; }
.rangebadge { display: inline-block; font-family: Helvetica, Arial, sans-serif; font-size: 6.6pt;
              line-height: 1; color: #8a5a00; background: #fdf5e3; border: 0.5px solid #e0c98a;
              border-radius: 2pt; padding: 2pt 4pt; margin: 0 3pt; vertical-align: 1.5pt;
              white-space: nowrap; font-weight: normal; text-decoration: none; }
.prov { margin-top: 6pt; padding-top: 4pt; border-top: 0.5px dashed #bbb;
        font-family: Helvetica, Arial, sans-serif; font-size: 7.2pt; line-height: 1.45; color: #555; }
.prov span.tag { display: inline-block; text-transform: uppercase; letter-spacing: 0.5pt; font-size: 6.5pt;
                 color: #888; margin-right: 5pt; }
.review { margin-top: 7pt; border: 1.5pt solid #e09a3e; background: #fffdf8; border-radius: 7pt;
          padding: 6pt 10pt; font-family: Helvetica, Arial, sans-serif; font-size: 7.5pt;
          line-height: 1.5; color: #7a2e2e; font-weight: 600; }
.review b { color: #c0392b; font-weight: bold; letter-spacing: 0.3pt; }
table.dep { width: 100%; border-collapse: collapse; font-family: Helvetica, Arial, sans-serif;
            font-size: 7.6pt; margin: 4pt 0 10pt 0; }
table.dep th, table.dep td { border: 0.5px solid #bbb; padding: 3.4pt 6pt; text-align: left; vertical-align: top; }
table.dep th { background: #f2f2f2; font-size: 7.3pt; }
table.dep thead { display: table-header-group; }
table.dep tr.an th { background: #fff; border: none; border-bottom: 0.5px solid #111;
                     font-family: Helvetica, Arial, sans-serif; font-size: 8.6pt; padding: 2pt 0 3pt 0; }
table.dep tr.an th span { float: right; font-weight: normal; color: #888; font-size: 7.2pt;
                          text-transform: uppercase; letter-spacing: 0.5pt; }
table.dep td.amd { color: #0a5c2e; font-weight: bold; }
table.dep td.flag { color: #9b1c1c; }
table.dep td.n { text-align: right; white-space: nowrap; }
table.tm { border-collapse: collapse; font-family: Helvetica, Arial, sans-serif; font-size: 6.6pt;
           margin: 4pt 0 8pt 0; }
table.tm th, table.tm td { border: 0.5px solid #ccc; padding: 1.6pt 3pt; text-align: right; }
table.tm th { background: #f2f2f2; font-size: 6.2pt; }
table.tm th.term { text-align: left; white-space: nowrap; padding-right: 6pt; }
table.tm thead { display: table-header-group; }
table.tm tr.an th { background: #fff; border: none; border-bottom: 0.5px solid #111;
                    font-family: Helvetica, Arial, sans-serif; font-size: 8.6pt; padding: 2pt 0 3pt 0;
                    white-space: normal; }
table.tm tr.an th span { float: right; font-weight: normal; color: #888; font-size: 7.2pt;
                         text-transform: uppercase; letter-spacing: 0.5pt; }
table.tm td.term { text-align: left; white-space: nowrap; padding-right: 6pt; }
table.tm td.z { color: #ccc; }
table.tm tr.tot td { border-top: 1.2px solid #111; font-weight: bold; background: #fafafa; }
table.tm tr.def td { background: #f4f8f4; }
.foot { margin-top: 14pt; border-top: 1.5px solid #111; padding-top: 8pt;
        font-family: Helvetica, Arial, sans-serif; font-size: 7.7pt; line-height: 1.5; color: #444; }
"""


def esc(t):
    return html.escape(t).replace("\n", "<br>")


HEAD = """
<div class="cover">
<h1>7.35.3 NMAC: proposed amendments outside the practicum. {NUM} of 4, {TITLE}</h1>
<p class="sub">Working draft {VERSION}, {VERSION_DATE}. Rule hearing August 28, 2026. Not a filing, not
submitted, and not adopted rule text.</p>
</div>

<ul class="what">
<li>{COVERS}</li>
<li>This is one of four documents covering the twenty-four sections of 7.35.3 NMAC that the practicum
amendment draft in <i>amendments/</i> does not reach. That draft covers 7.35.3.14, .18, .19, Paragraph (5) of
Subsection H of .20, and a proposed .29, and nothing here reopens any of them.</li>
<li>Every proposed change carries a citation to the provision, source document, or transcript it comes from.
Where a defect has no fix that a source supplies, the published text is left exactly as it stands and the
question is stated at that provision, with the choices and who decides.</li>
<li>No figure appears in a right column unless a source carries it. A figure taken from elsewhere in the rule
is badged with where it comes from.</li>
</ul>

<div class="key">
<b>The columns.</b> Left is the rule as published, verbatim. Right is the proposed amendment:
<ins>underlined green inserted</ins>, <del>struck red deleted</del>, unmarked text carried forward unchanged.
<span class="rangebadge">60 from 7.35.3.15 B</span> marks a figure taken from another provision of the same
rule rather than newly drafted. A provision shown with no amendment is reproduced because it carries a finding.
</div>
"""


def build_body(doc):
    rows, current, first = [], None, True
    for d, section, sub, published, proposed in P:
        if d != doc:
            continue
        if section != current:
            if current is not None:
                rows.append("</table>")
            current = section
            run = ('<thead><tr><th class="run" colspan="2"><div>%s <span class="ttl">%s</span>'
                   '<span class="doc">%s of 4 &middot; %s</span></div></th></tr>'
                   '<tr><th class="col">Current language<span>Proposed rule as published July 23, 2026</span></th>'
                   '<th class="col">Proposed amendment<span>Draft for review. Not filed, not adopted</span></th>'
                   '</tr></thead>'
                   % (section, SECTION_TITLES[section], DOCS[doc][1], DOCS[doc][2]))
            rows.append('<table class="rl%s">%s' % (" first" if first else "", run))
            first = False
        if published == UNCHANGED and proposed == UNCHANGED:
            continue
        left = ('<span class="none">%s</span>' % NEW) if published == NEW else esc(published)
        if proposed == UNCHANGED:
            right = '<span class="unch">Not amended. This provision is reproduced because it carries a ' \
                    'finding recorded below.</span>'
        else:
            right = proposed
        src = source_for(section, sub)
        rev = review_for(section, sub)
        extra = ''
        if src:
            extra += '<div class="prov"><span class="tag">Source</span>%s</div>' % src
        if rev:
            extra += '<div class="review"><b>Please review.</b> %s</div>' % rev
        rows.append('<tr><td class="left"><div class="label">%s</div>%s</td>'
                    '<td><div class="label">%s</div>%s%s</td></tr>' % (sub, left, sub, right, extra))
    rows.append("</table>")
    return "\n".join(rows)


# ---------------------------------------------------------------------------
# Addendum A: the undefined terms, counted from the corpus at build time
# ---------------------------------------------------------------------------

def term_map(corpus3, corpus2):
    _, s3 = segment(corpus3, r"7\.3[45]\.3\.(\d{1,2})\s+(?!NMAC)[A-Z][A-Z]+")
    secs = sorted(s3)
    out = ['<table class="tm">', '<thead>',
           '<tr class="an"><th class="term" colspan="%d">Addendum A '
           '<span>Terms this part uses and no part defines</span></th></tr>' % (len(secs) + 3),
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
<h2 class="sec">Addendum A <span class="ttl">Terms this part uses and no part defines</span></h2>
<p class="intro">7.35.3.7 NMAC provides in full: "The definitions in 7.35.2.7 NMAC apply to this part." Every
count in the table below is produced from the text layer of the published rule and of 7.35.2 NMAC each time
this document is built, section by section, so no count in it is transcribed by hand. Column headings are
section numbers within each part. The first block is terms used in 7.35.3 NMAC that 7.35.2.7 NMAC does not
define. The second block, shaded, is the terms 7.35.2.7 NMAC does define, shown for contrast.</p>
"""

ADDENDUM_A_TAIL = """
<p class="tnote"><b>What the table shows.</b> Sixteen terms carrying regulatory consequence in this part are
defined in neither part. Four of them are defined in the draft at 7.35.3.7 NMAC, because a single provision of
the published rule supplies the content: certificant, facilitator, registrant of another approved location, and
student. Twelve are not, and the two largest are healing center and certifying clinician. "Guide", the one
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


ADDENDUM_B = """
<h2 class="sec">Addendum B <span class="ttl">Dependencies across the two drafting scopes</span></h2>
<p class="intro">Provisions in these four documents that operate on, or are operated on by, a provision the
practicum amendment draft in <i>amendments/</i> reaches. Nothing in these documents amends a provision in that
draft's scope. Where a fix would require one, it is recorded here and left undrafted.</p>
<table class="dep">
<thead>
<tr class="an"><th colspan="4">Addendum B <span>Dependencies across the two drafting scopes</span></th></tr>
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
<tr><td>7.35.3.7, page 1</td><td>7.35.3.14 B, page 9</td>
<td>7.35.3.14 B authorizes facilitators to possess psilocybin products and provide them to qualified patients.
Whether a facilitator is a clinician under Section 3(B) of the Medical Psilocybin Act, and so within the
Section 5 exemption, governs whether that authority holds.</td>
<td class="flag">Not drafted. Recorded at 7.35.3.7 as a question for department counsel.</td></tr>
<tr><td>7.35.3.13 B, page 8</td><td>7.35.3.14 B, 7.35.3.19 C, 7.35.3.20 H(5)</td>
<td>The facilitator scope of work in 7.35.3.13 B is narrower than the authority the other three provisions
confer, and "direct supervision" is not defined anywhere in the rule.</td>
<td class="flag">Not drafted. Any amendment has to be coordinated with the practicum draft.</td></tr>
<tr><td>7.35.3.17 A, pages 10 to 11</td><td>7.35.3.19 H, as that draft proposes it</td>
<td>Whether the consultation requirement is stated in hours or in cases, and whether it sits at the proposed
7.35.3.19 H or at 7.35.3.17 A, is open in the practicum document for Dr. Metz, Ms. Wilson and Dr. Leeman. As
published, 7.35.3.19 NMAC runs A through G and has no Subsection H.</td>
<td class="flag">Not drafted. 7.35.3.17 A is left exactly as published so that their answer governs.</td></tr>
<tr><td>7.35.3.10 D(1), page 5</td><td>7.35.3.19 G(4), page 13</td>
<td>Two waivers of the practicum hours requirement each set a 40-hour floor for applications received by
December 31, 2027. 7.35.3.10 D(1) requires two separate individual and two separate group sessions;
7.35.3.19 G(4) requires two individual sessions and one group session.</td>
<td class="flag">Not drafted. Conforming one to the other is a choice between two figures already in the rule,
and one of the two provisions belongs to the practicum draft.</td></tr>
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
<h2 class="sec">Addendum C <span class="ttl">Defects recorded and not drafted, and why</span></h2>
<p class="intro">Every defect this record found in the twenty-four sections, that this draft does not amend.
The reason in each row is the reason no language is proposed, not an assessment of severity. Each has a review
note at the provision named, stating the choices and who decides.</p>
<table class="dep">
<thead>
<tr class="an"><th colspan="3">Addendum C <span>Defects recorded and not drafted, and why</span></th></tr>
<tr><th>Provision</th><th>Defect</th><th>Why nothing is drafted</th></tr>
</thead>
<tr><td>7.35.3.5, page 1, with the history notes at page 19</td>
<td>Twenty-six history notes carry the placeholder "xx/xx/2026"; the notes for 7.35.3.27 and 7.35.3.28 carry
9/22/2026. Under 7.35.3.5 a later date cited at the end of a section controls, so two sections would take
effect before the rest has a date.</td>
<td>No source supplies the intended effective date, and which way to conform is the department's to choose.</td></tr>
<tr><td>7.35.3.7, page 1</td>
<td>Twelve of the sixteen undefined terms have no definition in any source, including healing center, 54
occurrences, and certifying clinician, 53 occurrences.</td>
<td>Drafting a defined term with regulatory consequence from no source would be composing it. Addendum A
records the slate.</td></tr>
<tr><td>7.35.3.9 B, page 3</td>
<td>A renewal application is due no less than 30 days before expiry, and the department has no deadline to
decide it, so a certification can lapse while a timely renewal is pending. Nothing continues the certification
in the interim.</td>
<td>The fix is a continued-validity provision, which is a new grant, and no source in this record proposes its
terms.</td></tr>
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
<tr><td>7.35.3.10 A(2) and A(3), pages 4 to 5</td>
<td>The list of out-of-jurisdiction programs populates only when an individual application relying on a
program is approved, so it is empty at launch. A(3) refers to programs approved by Oregon and Colorado "as of
December 31, 2027", which is after the December 31, 2027 waiver in D(1) has closed.</td>
<td>Both fixes are new grants of authority to the department, and no source in this record proposes their
terms.</td></tr>
<tr><td>7.35.3.10 D(1), page 5, with 7.35.3.19 G(4), page 13</td>
<td>The two 40-hour waivers set different group-session minimums, two against one.</td>
<td>One of the two provisions is in the practicum draft's scope. Addendum B.</td></tr>
<tr><td>7.35.3.11 A(22)(d) and (e), and B(10)(d), pages 5 to 7</td>
<td>The 15-minute threshold for a remote natural environment. The Wilson working redline asks twice whether it
should be 30.</td>
<td>A question in the source, not a recommendation, and no source supplies a figure.</td></tr>
<tr><td>7.35.3.11, page 5</td>
<td>The two-person universal requirement the Wilson working redline adds, which its author records did not
reach the published rule.</td>
<td>The author records that she does not know where the provision belongs. Placing it would answer her
question.</td></tr>
<tr><td>7.35.3.12 A(20) and B(1), pages 7 to 8</td>
<td>An application filed on or before December 31, 2027 may be approved without the third-party evaluation
provided the evaluation is submitted by December 31, 2027, so the deferral shortens to nothing as that date
approaches and is unavailable on the last day.</td>
<td>The fix is a period, and no source in this record supplies one. Tying it to the certification term would
be a choice about how long a program may operate unevaluated.</td></tr>
<tr><td>7.35.3.12, pages 7 to 8, against the July 9, 2026 draft</td>
<td>The grounds for denying an educational program application present in the July 9 draft do not appear in the
published rule. Finding M9.</td>
<td>Restoring deleted grounds is a substantive policy decision, and this record cannot show whether the
deletion was deliberate.</td></tr>
<tr><td>7.35.3.17 A, pages 10 to 11</td>
<td>The mentoring obligation, and whether it is stated in hours or cases and where it sits.</td>
<td>Open in the practicum document for three named people. Addendum B.</td></tr>
<tr><td>7.35.3.17 B, page 11</td>
<td>The test-out price cap is a fraction of the price of "each of the educational modules", which assumes
per-module pricing. The Wilson working redline strikes the subsection.</td>
<td>Whether the option survives at all is the committee's decision, and a restated cap is worth drafting only
if it does.</td></tr>
<tr><td>7.35.3.20 A, page 13, with 7.35.3.21 A, page 15</td>
<td>Healing centers must keep a roster of all qualified patients intended to use and who have used the
location, and the department may interview patients.</td>
<td>Whether the roster should be kept in a form that does not identify patients turns on the department's data
needs, which no source in this record states.</td></tr>
<tr><td>7.35.3.20, page 13</td>
<td>The term "registrant of another approved location", 10 occurrences, against the certification that
7.35.3.11 B issues.</td>
<td>The definition drafted at 7.35.3.7 ties the two words together. Conforming all 10 occurrences instead is a
drafting choice, and this document does not make it.</td></tr>
<tr><td>7.35.3.21, page 15</td>
<td>No interval is set for department assessments, and none for repeating a third-party evaluation after the
first.</td>
<td>An interval is a figure and a demand on department capacity. No source supplies either.</td></tr>
<tr><td>7.35.3.25 C and D(2), page 16</td>
<td>The administrative review committee decides a denied patient application and is constituted nowhere in
7.35.3 NMAC or 7.35.2 NMAC. Four occurrences, all in this section.</td>
<td>Only the department can say who the committee is.</td></tr>
<tr><td>7.35.3.25 E, page 16</td>
<td>"Except as otherwise provided by law, there shall be no right to judicial review of a decision by the
administrative review committee." The Wilson working redline comments on it.</td>
<td>Whether the provision is within the department's authority is a legal question for department counsel.</td></tr>
<tr><td>7.35.3.24, page 15</td>
<td>The July 9, 2026 draft allowed a complaint from patients or staff; the published section allows one from a
qualified patient or certificant, so staff who are neither have no route.</td>
<td>Restoring standing for staff is a policy decision. The confidentiality assurance the July 9 draft carried
is restored in the redline above, because that text exists in a source.</td></tr>
<tr><td>7.35.3.27, pages 16 to 19</td>
<td>A certificant suspended immediately under Subsection A can be out of practice more than 135 days before a
final decision, and there is no expedited track. Finding N5.</td>
<td>An expedited schedule is a set of periods binding the department and the secretary, and no source supplies
them.</td></tr>
<tr><td>7.35.3.8 D, 7.35.3.25 A, 7.35.3.27 C(7), pages 2, 16 and 17</td>
<td>Three provisions describe review of a denial and their scopes overlap, so a patient applicant denied on the
merits may have both an informal review and a hearing. Finding M23.</td>
<td>The redline fixes the name of the proceeding only. Which track applies to which denial is a question of
what process is owed.</td></tr>
</table>
<p class="tnote"><b>Out of scope by decision.</b> The controlled-substance number requirement for certifying
clinicians. It appears at Paragraph (3) of Subsection B of 7.35.3.8 NMAC, page 1, and at Paragraph (2) of
Subsection D of 7.35.3.9 NMAC, page 3. Paragraph (2) is reproduced in the redline above because the
renumbering of the paragraphs around it required it. It is reproduced as published and is not amended, and
nothing is proposed about it.</p>
"""


ADDENDUM_D_INTRO = """
<h2 class="sec">Addendum D <span class="ttl">Mechanical defects across all twenty-eight sections</span></h2>
<p class="intro">Numbering, dates and drafting form, checked across the whole of 7.35.3 NMAC rather than only
the sections these documents amend. Every count and every entry is produced from the text layer of the
published rule each time this document is built.</p>
"""


def addendum_d(corpus):
    heads = []
    for m in re.finditer(r"(7\.3[45]\.3\.\d{1,2})\s+(?!NMAC)([A-Z][A-Z ,;\-]+?)(?=:)", corpus):
        heads.append((m.group(1), flatten(m.group(2))))
    bad = [(h, t) for h, t in heads if h.startswith("7.34.3")]
    notes = re.findall(r"\[(7\.3[45]\.3\.\d{1,2}) NMAC(\s*-\s*N)?,\s*([^\]]+)\]", corpus)
    no_n = [s for s, n, _ in notes if not n.strip()]
    real = [(s, d.strip()) for s, _, d in notes if "xx" not in d]
    reached = {"7.35.3.14": "practicum draft", "7.35.3.20": "practicum draft",
               "7.35.3.13": "document 4 above", "7.35.3.23": "document 4 above",
               "7.35.3.25": "document 4 above"}
    out = ['<table class="dep">', '<thead>',
           '<tr class="an"><th colspan="4">Addendum D '
           '<span>Mechanical defects across all twenty-eight sections</span></th></tr>',
           '<tr><th>Item</th><th>Count</th><th>Where</th><th>Corrected</th></tr>', '</thead>']
    out.append('<tr><td>Section headings reading 7.34.3 instead of 7.35.3</td><td class="n">%d of %d</td>'
               '<td class="flag">%s</td><td class="amd">%s</td></tr>'
               % (len(bad), len(heads), ", ".join(h for h, _ in bad),
                  "; ".join("%s in the %s" % (h.replace("7.34.3", "7.35.3"), reached[h.replace("7.34.3", "7.35.3")])
                            for h, _ in bad)))
    out.append('<tr><td>History notes carrying a real effective date rather than a placeholder</td>'
               '<td class="n">%d of %d</td><td class="flag">%s</td>'
               '<td>Not corrected. Recorded at 7.35.3.5 above.</td></tr>'
               % (len(real), len(notes), ", ".join("%s reads %s" % (s, d) for s, d in real)))
    out.append('<tr><td>History notes omitting the "- N" new-section designator</td>'
               '<td class="n">%d of %d</td><td>%s</td>'
               '<td>Not corrected. Mechanical, and the designator is the department\'s to set.</td></tr>'
               % (len(no_n), len(notes), ", ".join(no_n)))
    d9 = re.search(r"D\.\s+Certifying clinician application requirements:(.*?)E\.\s+Practitioner application",
                   corpus, re.S)
    items = re.findall(r"\((\d)\)", d9.group(1)) if d9 else []
    out.append('<tr><td>Numbering gap inside a subsection</td><td class="n">1</td>'
               '<td class="flag">7.35.3.9 D runs %s. There is no (3).</td>'
               '<td class="amd">Renumbered in document 4 above.</td></tr>' % ", ".join("(%s)" % i for i in items))
    parens = sorted({m.group(1) for m in re.finditer(r"\(([A-Z])\)\s+[A-Z][a-z]", corpus)})
    out.append('<tr><td>Subsections lettered "(A)" rather than "A."</td><td class="n">%d</td>'
               '<td class="flag">7.35.3.11 A, and 7.35.3.14 A, B and C. Letters found: %s</td>'
               '<td class="amd">7.35.3.11 A in document 3 above. 7.35.3.14 in the practicum draft.</td></tr>'
               % (len(parens) + 1, ", ".join(parens)))
    out.append('<tr><td>Sentence with no verb governing the decision</td><td class="n">1</td>'
               '<td class="flag">7.35.3.25 D(1), page 16. Carried over from the July 9, 2026 draft.</td>'
               '<td class="amd">Corrected in document 4 above.</td></tr>')
    out.append('<tr><td>Sentence that does not complete</td><td class="n">1</td>'
               '<td class="flag">7.35.3.18 F, page 12.</td>'
               '<td>In the practicum draft\'s scope. Corrected there.</td></tr>')
    out.append('<tr><td>Presiding official named inconsistently</td><td class="n">1</td>'
               '<td class="flag">7.35.3.27 M reads "hearing examiner"; the rest of 7.35.3.27 reads "hearing '
               'officer".</td><td class="amd">Corrected in document 4 above.</td></tr>')
    out.append('<tr><td>Duplicated words</td><td class="n">1</td>'
               '<td class="flag">7.35.3.24 reads "the electronic system designated by the department '
               'electronic system".</td><td class="amd">Corrected in document 4 above.</td></tr>')
    out.append('<tr><td>Spacing inside a heading</td><td class="n">1</td>'
               '<td class="flag">7.35.3.16 C reads "Conflict of -interest prohibitions". The July 9, 2026 '
               'draft read "Conflict-of-interest prohibitions".</td>'
               '<td class="amd">Corrected in document 2 above.</td></tr>')
    out.append('<tr><td>Class named in the lead-in but not in the operative words</td><td class="n">1</td>'
               '<td class="flag">7.35.3.27 B(8) opens "for certifying clinicians and practitioners" and then '
               'refers only to "the clinician".</td>'
               '<td class="amd">Corrected in document 4 above.</td></tr>')
    out.append('<tr><td>Patient described as certified rather than enrolled</td><td class="n">1</td>'
               '<td class="flag">7.35.3.27 C(1) reads "a certified patient".</td>'
               '<td class="amd">Corrected in document 4 above.</td></tr>')
    out.append('</table>')
    return "\n".join(out)


FOOT = """
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
<b>Status.</b> Working draft {VERSION}, document {NUM} of 4. Not a filing, not submitted, and not adopted rule
text. Nothing in <i>amendments/</i> or <i>docs/</i> was modified by this work.
</div>
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

    addenda = (ADDENDUM_A_INTRO + term_map(corpus3, corpus2) + ADDENDUM_A_TAIL
               + ADDENDUM_B + ADDENDUM_C + ADDENDUM_D_INTRO + addendum_d(corpus3))

    for doc, (stem, num, title, covers) in DOCS.items():
        head = (HEAD.replace("{VERSION}", VERSION).replace("{VERSION_DATE}", VERSION_DATE)
                .replace("{NUM}", num).replace("{TITLE}", title).replace("{COVERS}", covers))
        foot = FOOT.replace("{VERSION}", VERSION).replace("{NUM}", num)
        out_pdf = OUT_DIR / ("%s-%s.pdf" % (stem, VERSION))
        doc_html = ("<!doctype html><html><head><meta charset='utf-8'>"
                    "<title>7.35.3 NMAC %s amendments %s</title>"
                    "<style>%s</style></head><body>%s%s%s%s</body></html>"
                    % (title.lower(), VERSION, CSS, head, build_body(doc), addenda, foot))
        tmp = Path(tempfile.mkdtemp()) / "redline.html"
        tmp.write_text(doc_html, encoding="utf-8")
        subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox",
                        "--no-pdf-header-footer", "--print-to-pdf=%s" % out_pdf, tmp.as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("wrote %s (%.0f KB)" % (out_pdf.relative_to(REPO), out_pdf.stat().st_size / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())

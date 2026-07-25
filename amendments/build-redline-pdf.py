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

VERSION = "v5"
VERSION_DATE = "July 25, 2026"
OUT_PDF = REPO / ("amendments/7.35.3-practicum-amendments-%s.pdf" % VERSION)

LINE_TOLERANCE = 3.0

PERMIT_TITLE = {
    "{{PT}}": "practitioner",
    "{{PTS}}": "practitioners",
    "{{PT_C}}": "Practitioner",
    "{{PTS_C}}": "Practitioners",
    "{{PT_UC}}": "PRACTITIONER",
    "{{PTS_UC}}": "PRACTITIONERS",
}

SECTION_TITLES = {
    "7.35.3.14": "Authorized possession, purchase, or sale of medical psilocybin",
    "7.35.3.18": "Educational requirements for certifying clinicians, practitioners, and facilitators",
    "7.35.3.19": "Practicum requirements for practitioners and facilitators",
    "7.35.3.20": "Requirements for healing centers and other approved locations",
    "7.35.3.29": "Proposed new section. Practicum participants who are not qualified patients",
}

SECTION_INTRO = {
    "7.35.3.14": "The provision that authorizes a person to hold and hand over the medicine. The practicum depends on "
                 "it. One new subsection is proposed, for training permittees.",
    "7.35.3.18": "The educational requirements. The recommendation's 84-hour total is stated in one place, the New "
                 "Mexico module gains the hour count the recommendation gives it, and the recommendation's content "
                 "areas are added to the required topic list.",
    "7.35.3.19": "The practicum. This is the section the work was asked for; the other three are here because this one "
                 "depends on them.",
    "7.35.3.20": "Healing centers and other approved locations. One paragraph is touched, the staffing ratio, because "
                 "it counts students toward mandatory staffing.",
    "7.35.3.29": "Proposed new section. Nothing in the rule as published corresponds to it. It carries the first stage "
                 "of the practicum in Recommendation 3.",
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
@page { size: letter landscape; margin: 0.5in 0.5in 0.6in 0.5in;
        @bottom-center { content: counter(page); } }
* { box-sizing: border-box; }
body { font-family: "Times New Roman", Times, Georgia, serif; font-size: 8.7pt;
       line-height: 1.36; color: #111; margin: 0; }
h1 { font-family: Helvetica, Arial, sans-serif; font-size: 15pt; margin: 0 0 3pt 0; letter-spacing: -0.2pt; }
.sub { font-family: Helvetica, Arial, sans-serif; font-size: 8.4pt; color: #444; margin: 0 0 3pt 0; }
.cover { border-bottom: 2px solid #111; padding-bottom: 9pt; margin-bottom: 12pt; }
ul.what { font-family: Helvetica, Arial, sans-serif; font-size: 8.6pt; line-height: 1.55;
          margin: 0 0 12pt 0; padding-left: 15pt; max-width: 7.6in; }
ul.what li { margin-bottom: 3pt; }
.key { font-family: Helvetica, Arial, sans-serif; font-size: 8.2pt; color: #333;
       border-top: 0.5px solid #ccc; border-bottom: 0.5px solid #ccc; padding: 6pt 0; margin: 0 0 14pt 0; }
h2 { font-family: Helvetica, Arial, sans-serif; font-size: 11pt; margin: 0 0 6pt 0;
     padding: 3pt 0; border-top: 1.5px solid #111; border-bottom: 0.5px solid #111; break-after: avoid; }
h2.sec { break-before: page; }
h2 .ttl { font-weight: normal; color: #555; font-size: 9pt; }
p.intro { font-family: Helvetica, Arial, sans-serif; font-size: 8.1pt; line-height: 1.5; color: #333;
          margin: 0 0 8pt 0; padding-left: 8pt; border-left: 2.5px solid #bbb; break-after: avoid; }
table.rl { width: 100%; border-collapse: collapse; }
table.rl tr { break-inside: avoid; }
table.rl th { font-family: Helvetica, Arial, sans-serif; font-size: 7.6pt; text-transform: uppercase;
              letter-spacing: 0.4pt; color: #333; text-align: left; padding: 5pt 9pt 6pt 9pt;
              border-bottom: 1px solid #999; width: 50%; vertical-align: top; }
table.rl th span { display: block; font-weight: normal; text-transform: none; letter-spacing: 0;
                   font-size: 7.1pt; color: #777; margin-top: 2pt; }
table.rl td { vertical-align: top; padding: 8pt 9pt 10pt 9pt; border-bottom: 0.5px solid #ddd; width: 50%; }
table.rl td.left { border-right: 1px solid #ccc; color: #333; background: #fcfcfc; }
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
.review { margin-top: 6pt; border: 1px solid #d9a441; background: #fdf6e7; border-radius: 3pt;
          padding: 5pt 7pt; font-family: Helvetica, Arial, sans-serif; font-size: 7.4pt;
          line-height: 1.5; color: #5c4200; }
.review b { color: #8a5a00; }
table.hrs { border-collapse: collapse; font-family: Helvetica, Arial, sans-serif; font-size: 8.2pt;
            margin: 0 0 6pt 0; }
table.hrs th, table.hrs td { border: 0.5px solid #bbb; padding: 4pt 9pt; text-align: left; }
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


def render(t):
    for k, v in PERMIT_TITLE.items():
        t = t.replace(k, v)
    return t


def esc(t):
    return html.escape(t).replace("\n", "<br>")


HEAD = """
<div class="cover">
<h1>7.35.3 NMAC: proposed amendments to the practicum and training provisions</h1>
<p class="sub">Working draft {VERSION}, {VERSION_DATE}. Against the proposed rule published July 23, 2026.
Rule hearing August 28, 2026.</p>
</div>

<ul class="what">
<li><b>What this is.</b> The Training and Education Committee's July 17, 2026 recommendations, written as amendment
language against the rule as published, provision by provision.</li>
<li><b>What is in it.</b> The practicum, 7.35.3.19, and the three provisions it cannot function without: 7.35.3.18
educational requirements, 7.35.3.14 authorized possession, and 7.35.3.20 H(5) staffing ratios. Plus one proposed new
section. Nothing else in Part 3.</li>
<li><b>How every number got here.</b> Each proposed change carries a Source line. Where the recommendation gives a
range, the low end is drafted and the range is shown in a small badge next to it. Where the rule as published is
unclear, it is left alone and a Please review note says what is unclear. Nothing is invented to close a gap.</li>
</ul>

<div class="key">
<b>Reading the columns.</b> Left is the rule as published, verbatim. Right is the proposal:
<ins>underlined green inserted</ins>, <del>struck red deleted</del>, unmarked text carried forward unchanged.
<span class="rangebadge">Recommendation: 6 to 8</span> marks a number taken from the low end of a recommended range.
</div>

<div class="key" style="border:0;padding:0;margin-bottom:14pt">
<b>Items marked Please review:</b> 7.35.3.14 C, the registration that does not exist &middot; 7.35.3.18 A, no date for
the New Mexico module &middot; 7.35.3.18 C, the 68-hour figure and the per-topic ranges &middot; 7.35.3.19 A, the entry
gate and the 80-hour figure &middot; 7.35.3.19 C, the supervision hours and whether the published total is 170 or 190
&middot; 7.35.3.19 G, the permit term &middot; 7.35.3.19 K, the two waivers disagreeing &middot; 7.35.3.29, the
statutory question.
</div>

<h2>Hours <span class="ttl">Where the hours sit, published against proposed</span></h2>
<table class="hrs">
<tr><th>Component</th><th>Published</th><th>Proposed</th><th>Change</th></tr>
<tr><td>New Mexico module</td><td class="n">not stated</td><td class="n">6</td><td class="n">+6</td></tr>
<tr><td>Psilocybin therapy module, didactic</td><td class="n">30</td><td class="n">68</td><td class="n">+38</td></tr>
<tr><td>Simulated patient experience</td><td class="n">5</td><td class="n">5</td><td class="n">0</td></tr>
<tr><td>Role-specific module</td><td class="n">5</td><td class="n">5</td><td class="n">0</td></tr>
<tr><td><b>Module total, either permit</b></td><td class="n"><b>40</b></td><td class="n"><b>84</b></td><td class="n"><b>+44</b></td></tr>
<tr><td>Practicum, facilitator</td><td class="n">100</td><td class="n">62</td><td class="n">&minus;38</td></tr>
<tr><td>Practicum, practitioner</td><td class="n">120</td><td class="n">72</td><td class="n">&minus;48</td></tr>
<tr><td>Supervision or consultation</td><td class="n">10</td><td class="n">20</td><td class="n">+10</td></tr>
<tr class="band"><td>Program total, facilitator</td><td class="n">150</td><td class="n">166</td><td class="n">+16</td></tr>
<tr class="band"><td>Program total, practitioner</td><td class="n">170</td><td class="n">176</td><td class="n">+6</td></tr>
</table>
<div class="review" style="max-width:7.6in">
<b>Please review.</b> The practitioner row assumes the 20 supervision hours in 7.35.3.19 C sit inside the published
120. On the other reading of that subsection the published practitioner total is 190, and the proposed 176 would be
below it. See the note at 7.35.3.19 C.
</div>
"""


def build_body():
    rows = []
    current = None
    for section, sub, published, proposed in P:
        if section != current:
            if current is not None:
                rows.append("</table>")
            current = section
            rows.append('<h2 class="sec">%s <span class="ttl">%s</span></h2>' % (section, SECTION_TITLES[section]))
            if section in SECTION_INTRO:
                rows.append('<p class="intro">%s</p>' % SECTION_INTRO[section])
            rows.append('<table class="rl"><tr>'
                        '<th>Current language<span>Proposed rule as published July 23, 2026</span></th>'
                        '<th>Proposed amendment<span>Draft for review. Not filed, not adopted</span></th></tr>')
        label = render(sub)
        if published == UNCHANGED and proposed == UNCHANGED:
            rows.append('<tr><td class="left"><div class="label">%s</div><span class="unch">Not amended.</span></td>'
                        '<td><div class="label">%s</div><span class="unch">Not amended.</span></td></tr>'
                        % (label, label))
            continue
        left = ('<span class="none">%s</span>' % NEW) if published == NEW else esc(published)
        if proposed == UNCHANGED:
            right = '<span class="unch">Not amended.</span>'
        else:
            right = render(proposed)
        src = source_for(section, sub)
        rev = review_for(section, sub)
        extra = ''
        if src:
            extra += '<div class="prov"><span>Source</span>%s</div>' % render(src)
        if rev:
            extra += '<div class="review"><b>Please review.</b> %s</div>' % render(rev).replace("Please review. ", "", 1)
        rows.append('<tr><td class="left"><div class="label">%s</div>%s</td>'
                    '<td><div class="label">%s</div>%s%s</td></tr>' % (label, left, label, right, extra))
    rows.append("</table>")
    return "\n".join(rows)


ADDENDA = """
<h2 class="sec">Addendum A <span class="ttl">What the practicum depends on</span></h2>
<p class="intro">The practicum is 7.35.3.19. It cannot function without each row below. The right column says whether
this draft touches it.</p>
<table class="dep">
<tr><th>Provision</th><th>Page</th><th>What the practicum needs from it</th><th>In this draft</th></tr>
<tr><td>7.35.2.7 NMAC</td><td>n/a</td><td>Supplies every defined term used in Part 3, by force of 7.35.3.7</td><td class="flag">Not amended. Facilitator, healing center, certifying clinician and student are used in Part 3 and defined in neither part. Addendum B</td></tr>
<tr><td>Medical Psilocybin Act, Section 5</td><td>n/a</td><td>The criminal and civil exemption. Names producers, clinicians and qualified patients, and protects presence only for anyone else</td><td class="flag">Statute. Not reachable by rule</td></tr>
<tr><td>7.35.3.9 C(3), E, F</td><td>3</td><td>Certification applications require documentation of the completed practicum, and E(1) sets the practitioner licensure predicate</td><td>Not amended</td></tr>
<tr><td>7.35.3.10 D</td><td>5</td><td>Out-of-jurisdiction 40-hour practicum waiver</td><td class="flag">Not amended. Disagrees with 7.35.3.19 K</td></tr>
<tr><td>7.35.3.11 A, B</td><td>5 to 7</td><td>Healing centers and other approved locations. The practicum may only happen in them</td><td>Not amended</td></tr>
<tr><td>7.35.3.12 A</td><td>7</td><td>Educational program certification</td><td>Not amended</td></tr>
<tr><td>7.35.3.13 B</td><td>8</td><td>Facilitator scope of work, which limits what the practicum can usefully train</td><td class="flag">Not amended</td></tr>
<tr><td class="amd">7.35.3.14</td><td>9</td><td>Authority to possess and administer</td><td class="amd">AMENDED. New Subsection D</td></tr>
<tr><td>7.35.3.15 A(4)</td><td>9</td><td>Practicum site agreements need prior written approval, with no deadline on the department</td><td class="flag">Not amended</td></tr>
<tr><td>7.35.3.17 A</td><td>10 to 11</td><td>The 10 mentoring hours the consultation requirement would replace</td><td class="flag">Not amended</td></tr>
<tr><td>7.35.3.17 B, C</td><td>11</td><td>Test-out, graduation conditions, and the practicum records a program must keep</td><td>Not amended</td></tr>
<tr><td class="amd">7.35.3.18</td><td>11 to 12</td><td>The didactic requirement the practicum entry gate is measured against</td><td class="amd">AMENDED</td></tr>
<tr><td class="amd">7.35.3.19</td><td>12 to 13</td><td>The practicum</td><td class="amd">AMENDED. Re-lettered A to K</td></tr>
<tr><td>7.35.3.20 D</td><td>14</td><td>Students may be present at an administration session</td><td>Not amended</td></tr>
<tr><td class="amd">7.35.3.20 H(5)</td><td>14</td><td>Staffing ratio, which counts a qualified student</td><td class="amd">AMENDED</td></tr>
<tr><td>7.35.3.22</td><td>15</td><td>Prohibitions, reaching "the qualified patient or certificant"</td><td class="flag">Not amended</td></tr>
<tr><td>7.35.3.27</td><td>16 to 19</td><td>Discipline and appeal</td><td>Not amended</td></tr>
</table>

<h2>Proposed new provisions</h2>
<table class="dep">
<tr><th>Provision</th><th>What it does</th><th>Source</th><th>If dropped</th></tr>
<tr><td>7.35.3.14 D</td><td>Authorizes a training permittee to possess and administer under supervision</td><td>Recommendation 3, page 4</td><td class="flag">The practicum stays unauthorized. Stands or falls with 7.35.3.19 G</td></tr>
<tr><td>7.35.3.18 H</td><td>States the 84-hour total in one place</td><td>Recommendation 2, page 3</td><td>Module hours survive individually; no total is stated anywhere</td></tr>
<tr><td>7.35.3.19 D</td><td>The four-step practicum sequence</td><td>Recommendation 3, pages 3 to 4</td><td>Practicum totals survive; the sequence is lost</td></tr>
<tr><td>7.35.3.19 G</td><td>Creates the training permit</td><td>Recommendation 3, page 4</td><td class="flag">The practicum stays unauthorized</td></tr>
<tr><td>7.35.3.19 H</td><td>20 consultation hours, two presented cases, standardized evaluation form</td><td>Recommendation 4, pages 4 to 5</td><td>7.35.3.17 A survives at 10 hours with no requirement to have seen a client</td></tr>
<tr><td>7.35.3.19 I</td><td>End-of-life checkpoint</td><td>Recommendation 4, page 5</td><td>No end-of-life competency gate remains</td></tr>
<tr><td>7.35.3.29</td><td>Practicum participants who are not qualified patients</td><td>Recommendation 3, step 1, page 3</td><td>The first stage of the practicum has no lawful setting</td></tr>
</table>

<h2 class="sec">Addendum B <span class="ttl">Terms and titles, not proposed here</span></h2>
<p class="intro">Recorded because it affects every provision in this draft and cannot be fixed inside Part 3.
7.35.3.7 provides in full: "The definitions in 7.35.2.7 NMAC apply to this part." 7.35.2 NMAC was adopted effective
June 23, 2026.</p>
<table class="dep">
<tr><th>Term used in Part 3</th><th>In 7.35.2.7?</th><th>What 7.35.2.7 has</th><th>Consequence</th></tr>
<tr><td><b>Facilitator</b></td><td class="flag">No. Zero occurrences in 7.35.2 NMAC</td><td>"Guide" an individual who has completed training and education approved by the department to be able to assist practitioners during the administration sessions and who has been registered with the department</td><td class="flag">Every facilitator provision in Part 3 rests on an undefined term. A guide holds no professional license, so a facilitator is not a "clinician" under Section 3(B) of the Act, while 7.35.3.14 B authorizes facilitators to possess and provide</td></tr>
<tr><td><b>Healing center</b></td><td class="flag">No</td><td>"Approved location" means a location approved by the department for psilocybin administration sessions</td><td class="flag">Healing centers are certified and regulated throughout Part 3 with no definition</td></tr>
<tr><td><b>Certifying clinician</b></td><td class="flag">No</td><td>"Clinician" means an approved health care provider licensed in New Mexico who holds a certification from the department to provide medical services to qualified patients</td><td>Probably the same role renamed</td></tr>
<tr><td><b>Student</b></td><td class="flag">No</td><td>Nothing</td><td class="flag">Carries consequence at 7.35.3.19, 7.35.3.20 D and 7.35.3.20 H(5)</td></tr>
<tr><td>Practitioner</td><td>Yes</td><td>"Practitioner" means an individual who is a licensed healthcare professional who is certified by the department to provide medical psilocybin integrative therapy, supervise guides, and who has completed department required trainings</td><td>Carries the same licensure predicate as the Act's "clinician"</td></tr>
</table>
<p class="intro" style="border:0;padding-left:0"><b>The permit title.</b> Recommendation 1 proposes retitling
"Practitioner" as "Licensed Provider". This draft keeps "practitioner" because the decision has not been made. The
title is held as a variable in the source, so changing it is one command. It reaches no hour count and no practicum
requirement: those attach to the permit type, and what the practicum is turns on the licensure predicate at
7.35.3.9 E(1), which already requires a New Mexico professional license. A retitle is an amendment to 7.35.2.7 NMAC
plus a conforming pass over Part 3.</p>

<h2 class="sec">Addendum C <span class="ttl">Outside this draft</span></h2>
<p class="intro">Part 3 has twenty-eight sections. This draft covers the practicum and what it depends on. The rest are
inventoried in <i>analysis/july23-rule-concerns.md</i>, which records five blocking and twenty-three material findings
across the whole part, and are listed here so the boundary is visible.</p>
<table class="dep">
<tr><th>Group</th><th>Sections</th><th>Recorded findings</th></tr>
<tr><td>Terminology</td><td>7.35.3.7, and 7.35.2.7 NMAC</td><td>Facilitator, healing center, certifying clinician and student undefined. Addendum B</td></tr>
<tr><td>Educational programs</td><td>7.35.3.12, .15, .16, .17</td><td>The evaluator conflict rule disqualifies the evaluators a program must hire; the third-party evaluation deferral expires the day it becomes available; no deadline binds the department on instructor changes; the denial grounds were deleted; the evaluator qualification standard may be unmeetable; mentoring is unfunded and untied to certification; the test-out price cap assumes per-module pricing</td></tr>
<tr><td>Out-of-jurisdiction pathway</td><td>7.35.3.10</td><td>The two 40-hour waivers disagree; the 2027 waiver may cancel itself; the approved list is empty at launch and populates only retroactively; individuals must produce an evaluation only a program can commission</td></tr>
<tr><td>Locations and oversight</td><td>7.35.3.11, .20, .21</td><td>Healing center staff authority hangs on a registration that does not exist; outdoor locations need no AED while healing centers do; the patient roster and the patient-interview authority; other approved locations have a 90-day term and no renewal path</td></tr>
<tr><td>Patients, applicants, process</td><td>7.35.3.8, .9, .13, .22 to .27</td><td>Facilitator scope conflicts with the practicum and the ratios; complainants lose confidentiality; the benefit-risk attestation; renewals can lapse while pending; the re-application clause reads as a deadline; two review tracks with inconsistent scope; a suspended certificant can be out of practice more than 135 days</td></tr>
<tr><td>Mechanical</td><td>Throughout</td><td>Five section headings read 7.34.3 instead of 7.35.3, two of which are corrected here; two sections carry a real effective date while the rest carry placeholders; a numbering gap at 7.35.3.9 D</td></tr>
</table>
"""

FOOT = """
<div class="foot">
<b>Sources.</b> Rule as published: <i>rules-draft-2026-07-23-published.pdf</i>, 19 pages. Recommendations: Dr. Anne
Metz, <i>Recommendations on Education and Training Requirements for Facilitators and Licensed Providers</i>, July 17,
2026, with the one-page summary and the committee slide deck of the same date. July 17, 2026 transcripts, morning
Advisory Board and afternoon Training and Education Committee, both labeled "UNOFFICIAL AUTO-GENERATED TRANSCRIPT.
NO SPEAKER ATTRIBUTION." Medical Psilocybin Act, Senate Bill 219, 2025, as introduced; the enacted text at Sections
26-2D-1 through -11 NMSA 1978 has not been checked against it. 7.35.2 NMAC as adopted effective June 23, 2026.<br><br>
<b>Status.</b> Working draft {VERSION}. Not a filing, not submitted, not adopted rule text. Every left-column block was
verified against the text layer of the published PDF before this file was generated.
</div>
"""


def main():
    failures = verify()
    if failures:
        print("VERIFICATION FAILED:")
        for section, sub, chunk in failures:
            print("  %s %s :: %s" % (section, render(sub), chunk))
        return 1
    print("verified: every published-column block matches the published PDF")

    head = HEAD.replace("{VERSION}", VERSION).replace("{VERSION_DATE}", VERSION_DATE)
    foot = FOOT.replace("{VERSION}", VERSION)
    doc = ("<!doctype html><html><head><meta charset='utf-8'>"
           "<title>7.35.3 NMAC practicum amendments %s</title>"
           "<style>%s</style></head><body>%s%s%s%s</body></html>"
           % (VERSION, CSS, head, build_body(), ADDENDA, foot))

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

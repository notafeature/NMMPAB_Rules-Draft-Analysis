#!/usr/bin/env python3
"""Builds docs/rule.html from the plain-text extraction of the published rule.

The extraction lives in source-text/ and is produced with pypdf, one
"===== PAGE n =====" marker per page. When a new version of the rule is
published: extract it the same way, point SOURCE at the new file, update
DOC and DOCDATE, review ANNOTATIONS, and run this script. Every section
and page anchor regenerates.

Line breaks inside the text are collapsed to single spaces and nothing
else is altered. Where the extraction is garbled, the linked PDF governs;
the page says so.
"""

import re, html

SOURCE = "source-text/rules-draft-2026-07-23-published.txt"
DOC = "documents/rules-draft-2026-07-23-published.pdf"
DOCDATE = "July 23, 2026"
OUT = "docs/rule.html"
NSECTIONS = 28

NAV = """<header class="top"><div class="wrap">
<a class="brand" href="index.html">7.35.3 <b>·</b> Training &amp; Education</a>
<nav>
<a href="index.html">Overview</a>
<a href="rule.html" aria-current="page">The rule</a>
<a href="pathways.html">Pathways</a>
<a href="recommendation.html">Recommendation</a>
<a href="hours.html">Hours</a>
<a href="record.html">Record</a>
<a href="comment.html">Comment</a>
<a href="about.html">About</a>
</nav>
</div></header>"""

FOOT = """<footer class="foot"><div class="wrap">
<span>An independent community record of the rulemaking. Not affiliated with the New Mexico Department of Health.</span>
<span>Nothing here is final rule text, legal advice, or medical advice.</span>
<a href="about.html">Sources and method</a>
<a href="comment.html">Report an error</a>
</div></footer>"""

# Notes placed under the section they describe. Every claim is sourced.
# type: open | settled | defect | blue
ANNOTATIONS = {
    7: [("open", "Deferred to committee",
         "Definitions were sent to the Training and Education Committee on July 17 along with the hours, "
         "with the department asking for language sooner rather than later. "
         "Source: July 17 committee meeting transcript, on the <a href='record.html'>record page</a>.")],
    9: [("settled", "Controlled-substance number, kept",
         "The requirement that a certifying clinician hold a New Mexico controlled-substance number was "
         "contested through June and July and kept by the department on July 17; it stands in this section. "
         "The full account is on the <a href='cs-number.html'>controlled-substance number page</a>.")],
    10: [("settled", "Reciprocity deadlines, settled July 9",
         "Both reciprocity waiver deadlines were extended to December 31, 2027 at the July 9 board meeting, "
         "resolved without objection. The board chair described December 31 as a legislative backstop. "
         "Source: July 9 meeting transcript.")],
    14: [("defect", "Students are not authorized here",
         "The practicum in 7.35.3.19 requires students to conduct administration sessions, and 7.35.3.20 lets "
         "students count toward staffing, but this section authorizes no student to possess or administer "
         "psilocybin. Stated in the July 25 concerns inventory, finding B1."),
        ("defect", "A registration this rule does not create",
         "Subsection C conditions healing-center owner and employee authorization on registration with the "
         "department, and the rule creates no such registration. Finding B5.")],
    16: [("defect", "Paid evaluators are disqualified by the conflict rule",
         "The program must engage and pay the third-party evaluation team, and the section's own conflict rule "
         "disqualifies paid evaluators. Finding B3.")],
    18: [("open", "Deferred to committee, then raised",
         "The didactic hours were deferred to the Training and Education Committee by a 7-0 board vote on "
         "July 17. The text published six days later raised the shared module from 25 hours to 30 and added "
         "three topics: trauma-informed care, dosing, and non-ordinary states of consciousness. The committee's "
         "recommendation, submitted July 27, proposes a single 80-hour didactic standard with minimums in "
         "nine content areas; it is on the <a href='recommendation.html'>recommendation page</a>."),
        ("defect", "A module with no date it must exist",
         "Every certification pathway requires a New Mexico module created or approved by the department, and "
         "the rule sets no date by which that module must exist. Finding B2.")],
    19: [("open", "Deferred to committee, published unchanged",
         "The board voted 7-0 on July 17 to send the practicum hours to committee. This text carries them "
         "unchanged: 100 hours for facilitators, 120 for practitioners. The committee's recommendation, "
         "submitted July 27, proposes a staged practicum of 60 hours for facilitators and 70 for licensed "
         "providers; the two positions can be compared on the "
         "<a href='hours.html'>working model of the hours</a>."),
        ("blue", "New in this draft",
         "The condition that the practicum cannot begin until half the didactic requirements and all simulated "
         "patient requirements are complete appears in no earlier version and was not raised at either "
         "July 17 meeting."),
        ("defect", "A practicum that requires patients it cannot lawfully use",
         "Subsection A requires a minimum of 14 qualified patients at approved locations, no provision "
         "authorizes practicum with non-patients, and the only relief is a discretionary waiver with no "
         "stated standard. Finding B4.")],
    20: [("blue", "Students in the staffing ratio",
         "Paragraph 5 of subsection H counts qualified students toward staffing ratios, which is how the "
         "department said students would participate instead of a training permit. It depends on the "
         "authorization missing from 7.35.3.14. Source: July 17 committee transcript; finding B1.")],
}

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
        # the published text misnumbers some headings 7.34.3; accept both and record it
        m = re.compile(rf"7\.3([45])\.3\.{n}\s+([A-Z][^a-z]*?):").search(raw, pos)
        if not m:
            raise SystemExit(f"section 7.35.3.{n} not found after offset {pos}")
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
        p = re.sub(r"\[(7\.35\.3\.\d+ NMAC[^\]]*)\]", r"<span class='hist'>[\1]</span>", p)
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
                f"The published PDF numbers this section's heading 7.34.3.{n}. Its own history note and every "
                f"cross-reference in the rule read 7.35.3.{n}, which this page uses."))
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
  <div class="rhead"><span class="rnum">7.35.3.{n}</span><h2 class="rtitle">{title.title()}</h2>
  <a class="pdf" href="{DOC}#page={page}" target="_blank" rel="noopener" data-cite="Published proposed rule 7.35.3 NMAC, {DOCDATE}, page {page}">PDF p. {page}</a></div>
  <div class="verbatim">{render_body(s['body'])}</div>
  {notehtml}
</section>""")
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The rule · 7.35.3 NMAC Training and Education</title>
<link rel="stylesheet" href="style.css">
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
@media(max-width:760px){{.toclist{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
{NAV}
<main class="wrap">
  <div class="head">
    <p class="kicker">Proposed rule · published {DOCDATE} · <b>rule hearing August 28</b></p>
    <h1>The rule</h1>
    <p class="lede">The full text of 7.35.3 NMAC as published for hearing, all twenty-eight sections, with the state of each contested provision noted where it lives. Line breaks are collapsed for reading; where the extraction stumbles, the linked PDF governs.</p>
    <p class="stamp">Text from the official PDF published {DOCDATE}. Regenerated by tools/build-rule-page.py.</p>
  </div>
  <div class="toclist">
  {"".join(toc)}
  </div>
  {"".join(body)}
</main>
{FOOT}
</body>
</html>
"""
    open(OUT, "w").write(doc)
    print(f"wrote {OUT}: {len(sections)} sections, {len(doc)} bytes")

if __name__ == "__main__":
    main()

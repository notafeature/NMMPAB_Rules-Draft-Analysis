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

SOURCE = os.path.join(ROOT, "source-text", "rules-draft-2026-08-25-published.txt")
DOC = "documents/rules-draft-2026-08-25-published.pdf"
DOCDATE = "August 25, 2026"
OUT = os.path.join(ROOT, "docs", "rule.html")
NSECTIONS = 28

KICKER = ('Published August 25, 2026 &middot; <b>the current proposed rule</b> &middot; '
          'rule hearing October 2, 2026')
LEDE = ("The full text of 7.35.3 NMAC as published August 25, 2026, all twenty-eight "
        "sections, with the state of each contested provision noted where it lives. This "
        "text supersedes the set-aside July 23 publication and goes to hearing on "
        "October 2, 2026; public comment continues through the hearing. The rule&rsquo;s "
        "definitions are in amendments to 7.35.2.7 NMAC published the same day. Line "
        "breaks are collapsed for reading; where the extraction stumbles, the linked PDF "
        "governs.")

_spec = importlib.util.spec_from_file_location(
    "syncnav", os.path.join(ROOT, "tools", "sync-nav.py"))
syncnav = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(syncnav)

FOOT = """<footer class="foot"><div class="wrap">
<span>An independent community record of the rulemaking. Not affiliated with the New Mexico Department of Health.</span>
<span>Nothing here is final rule text, legal advice, or medical advice.</span>
<a href="about.html">Sources and method</a>
<a href="comment.html">Report an error</a>
</div></footer>"""

# Notes placed under the section they describe. Every claim is sourced.
# type: open | settled | defect | blue
ANNOTATIONS = {
    7: [("blue", "The definitions live in the 7.35.2 amendments",
         "This rule defines nothing of its own. The definitions it runs on, certifying clinician, "
         "practitioner, facilitator, and the New Mexico module among them, are in the amendments to "
         "7.35.2.7 NMAC published August 25 alongside this text. The definitions were sent to the "
         "Training and Education Committee on July 17 with the hours; the amendments carry the "
         "department's language. The amendments PDF is in the register on the "
         "<a href='record.html#documents'>record page</a>.")],
    9: [("settled", "Controlled-substance number, kept",
         "The requirement that a certifying clinician hold a New Mexico controlled-substance number was "
         "contested through June and July and kept by the department on July 17. It stands in this "
         "section, and the amended definition of certifying clinician in 7.35.2.7 now carries the "
         "number inside it. The full account is on the "
         "<a href='cs-number.html'>controlled-substance number page</a>.")],
    10: [("settled", "Reciprocity deadlines, settled July 9",
         "Both reciprocity waiver deadlines were extended to December 31, 2027 at the July 9 board meeting, "
         "resolved without objection. The board chair described December 31 as a legislative backstop. "
         "Source: July 9 meeting transcript.")],
    13: [("blue", "New in this text",
         "Two provisions appear here for the first time in the August 25 text: a certifying clinician, "
         "practitioner, or facilitator shall not consume or be under the influence of psilocybin or any "
         "other intoxicant when providing services to a patient, Subsection F, and certifying "
         "clinicians, practitioners, and facilitators must provide the department access to records on "
         "request, Subsection G.")],
    14: [("defect", "Students are not authorized here",
         "The practicum in 7.35.3.19 requires students to conduct administration sessions, and 7.35.3.20 lets "
         "students count toward staffing, but this section authorizes no student to possess or administer "
         "psilocybin. Stated in the July 25 concerns inventory, finding B1, and analyzed at "
         "<a href='deferred.html#s14'>7.35.3.14 on What a practicum change touches</a>."),
        ("defect", "A registration this rule does not create",
         "Subsection C conditions healing-center owner and employee authorization on registration with the "
         "department, and the rule creates no such registration. Finding B5, analyzed at "
         "<a href='deferred.html#new2'>the missing healing-center registration on What a "
         "practicum change touches</a>."),
        ("blue", "New in this text: chain of custody",
         "Paragraph D, new in the August 25 text, requires a practitioner, facilitator, or healing "
         "center owner or employee who obtains or transfers medical psilocybin to generate or verify a "
         "chain of custody form, and to carry identification and the form when transporting. It pairs "
         "with the amended transportation rules in 7.35.2.24, published the same day.")],
    15: [("blue", "New in this text",
         "Subsection A, new in the August 25 text, puts every educational program curriculum through "
         "department review and approval, initial applications and later modifications alike, with five "
         "stated grounds for denial.")],
    16: [("defect", "Paid evaluators are disqualified by the conflict rule",
         "The program must engage and pay the third-party evaluation team, and the section's own conflict rule "
         "disqualifies paid evaluators. Finding B3.")],
    17: [("blue", "New in this text",
         "Educational programs must collect structured student feedback within 30 calendar days of each "
         "module's completion, Subsection F, new in the August 25 text.")],
    18: [("open", "The didactic hours, doubled and still contested",
         "The board sent the didactic hours to committee by a 7-0 vote on July 17. The July 23 text set "
         "the therapy module at 30 didactic hours with 5 simulated patient hours; this text sets 65 "
         "didactic hours, at least one third in person, with 10 simulated patient hours, matching the "
         "recommendation's 80-hour total while declining its per-area minimums. The committee's "
         "recommendation, at its August 21 position, sets minimums in nine content areas; it is on the "
         "<a href='recommendation.html'>recommendation page</a>, and public comment continues through "
         "the October 2 hearing."),
        ("blue", "New in this text",
         "Eleven topics enter the required list, legal considerations, cultural competencies, "
         "traditional and ceremonial practices, equity and access, informed consent, touch and somatic "
         "awareness, and continuity of care among them, none with an hour minimum. A new waiver at "
         "Subsection H lets the department reduce the didactic hourly and topic requirements."),
        ("blue", "Drafting slip in the published PDF",
         "Paragraph (2) of Subsection C states its competency-evaluation sentence twice and carries a "
         "stray punctuation mark after &ldquo;five hours&rdquo;. Quoted as published; the PDF governs."),
        ("defect", "A module with no date it must exist",
         "Every certification pathway requires a New Mexico module created or approved by the department, and "
         "the rule sets no date by which that module must exist. Finding B2.")],
    19: [("open", "The practicum totals, published unchanged a second time",
         "The board voted 7-0 on July 17 to send the practicum hours to committee. The July 23 text "
         "carried them unchanged, and this text carries them unchanged again: 100 hours for "
         "facilitators, 120 for practitioners. The committee's recommendation, at its August 21 "
         "position, proposes a staged practicum of 102 hours for facilitators and 114 for licensed "
         "providers, the recommendation's name for the role this text calls the practitioner; the two "
         "positions can be compared on the <a href='hours.html'>working model of the hours</a>."),
        ("blue", "New in this text",
         "Three additions inside the unchanged totals: the first 20 administration-day hours are with "
         "patients the supervising practitioner determines to be low-risk, Paragraph (3) of Subsection "
         "A; same-day sessions must include patients with a diversity of the qualifying conditions, "
         "Paragraph (4); and the student must pass case presentations on two of their last four "
         "patients to complete the practicum, Subsection C."),
        ("defect", "A practicum that requires patients it cannot lawfully use",
         "Subsection A requires a minimum of 14 qualified patients at approved locations, no provision "
         "authorizes practicum with non-patients, and the only relief is a discretionary waiver with no "
         "stated standard. Finding B4. The provision is quoted, with everything else a practicum "
         "change reaches, at <a href='deferred.html#s19a'>7.35.3.19 (A) on What a practicum "
         "change touches</a>.")],
    20: [("blue", "Students in the staffing ratio, now including billing",
         "Paragraph 5 of Subsection H counts qualified students toward staffing ratios once past 50 "
         "practicum hours, which is how the department said students would participate instead of a "
         "training permit, and the August 25 text adds that the substitution includes the purpose of "
         "billing. It depends on the authorization missing from 7.35.3.14. Source: July 17 committee "
         "transcript; finding B1."),
        ("blue", "Moved here from the application sections",
         "The natural-environment requirements, two wilderness-certified individuals present and a "
         "first aid kit and AED on site when the setting is 15 minutes or more from emergency medical "
         "services, were application items in 7.35.3.11 in the July 23 text. The August 25 text makes "
         "them an operational duty during administration sessions, Subsection K.")],
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
        # earlier published texts misnumbered some headings 7.34.3; accept both and record it
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
  <a class="pdf" href="{DOC}#page={page}" target="_blank" rel="noopener" data-cite="Revised proposed rule 7.35.3 NMAC, {DOCDATE}, page {page}">PDF p. {page}</a></div>
  <div class="verbatim">{render_body(s['body'])}</div>
  {notehtml}
</section>""")

    name = syncnav.NAMES["rule"]
    nav = syncnav.build_nav("rule")
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} &middot; {syncnav.TITLE_SUFFIX}</title>
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
<noscript><style>.tnav{{display:flex}}</style></noscript>
</head>
<body>
<header class="topbar">
  <div class="inner">
    <a class="brand" href="index.html"><span class="dot"></span>7.35.3 NMAC &middot; Training &amp; Education</a>
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
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", tool)],
                       check=True, stdout=subprocess.DEVNULL)
    print("stamped: stylesheet version, visit counter, provenance block")

if __name__ == "__main__":
    main()

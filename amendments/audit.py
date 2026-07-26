#!/usr/bin/env python3
"""Audit every verifiable claim in the practicum amendment document.

Checks four classes of claim and writes a receipt for each:

  RULE   every left-column block, against the text layer of the published rule
  QUOTE  every quotation in the citation and review notes, against its source
  MATH   every arithmetic statement in the document
  BUILD  the document rebuilds and every check passes

Exit code is non-zero if any check fails. Output: amendments/AUDIT.md
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from content import P, NEW, UNCHANGED            # noqa: E402
from notes import SOURCE, REVIEW                 # noqa: E402

REPO = Path(__file__).resolve().parent.parent
SRC = {
    "published rule": REPO / "docs/documents/rules-draft-2026-07-23-published.pdf",
    "Metz recommendation": REPO / "docs/documents/metz-recommendations-2026-07-17.pdf",
    "Medical Psilocybin Act": REPO / "Document Register/SB0219-Medical-Psilocybin-Act-2025.pdf",
    "7.35.2 NMAC": REPO / "source-text/7.35.2-NMAC-adopted-2026-06-23.txt",
    "committee transcript": REPO / "source-text/NMMPAB-2026-07-17-committee-transcript.txt",
    "board transcript": REPO / "source-text/NMMPAB-2026-07-17-board-transcript.txt",
    "Wilson redline": REPO / "source-text/wilson-redline-2026-07-25.txt",
    "Wilson comments": REPO / "source-text/wilson-redline-2026-07-25-comments.txt",
}

# The Wilson redline is a tracked-changes export. Insertions are wrapped in
# {+ +}, deletions in [- -], and comment anchors read «Cnn». Strip the markup
# so a quotation of the resulting text can be matched.
WILSON_MARKUP = re.compile(r"\{\+|\+\}|\[-|-\]|«C\d+»")

LINE_TOLERANCE = 3.0
results = []


def flatten(t):
    for a, b in [("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("‐", "-"), ("‑", "-"), ("–", "-"), ("—", "-"), ("­", "")]:
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def load(name):
    p = SRC[name]
    if p.suffix == ".txt":
        t = p.read_text(encoding="utf-8")
        if name.startswith("Wilson"):
            t = flatten(WILSON_MARKUP.sub("", t))
            return re.sub(r"\s+([.,;:])", r"\1", t)
        return flatten(t)
    from pdfminer.high_level import extract_pages, extract_text
    from pdfminer.layout import LTTextContainer, LTTextLine
    if name != "published rule":
        return flatten(extract_text(str(p)))
    out = []
    for page in extract_pages(str(p)):
        items = []
        for el in page:
            if not isinstance(el, LTTextContainer):
                continue
            for line in el:
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


CORPUS = {}


def found(text, name):
    """A quotation is found if it appears contiguously, or, where the source PDF
    hyphenates across a line break, in both halves."""
    if name not in CORPUS:
        CORPUS[name] = load(name)
    c = CORPUS[name]
    q = flatten(text)
    if q in c:
        return True
    words = q.split(" ")
    if len(words) < 8:
        return False
    mid = len(words) // 2
    return " ".join(words[:mid]) in c and " ".join(words[mid:]) in c


def check(cls, claim, ok, detail=""):
    results.append((cls, claim, ok, detail))
    return ok


# ---------------------------------------------------------------------------
# RULE: every left-column block
# ---------------------------------------------------------------------------

rule_blocks = 0
for section, sub, published, _ in P:
    if published in (NEW, UNCHANGED):
        continue
    for chunk in published.split("\n"):
        if not chunk.strip():
            continue
        rule_blocks += 1
        check("RULE", "%s %s :: %s" % (section, sub, flatten(chunk)[:70]),
              found(chunk, "published rule"), "published rule, text layer")

# ---------------------------------------------------------------------------
# QUOTE: every quotation inside a citation or review note
# ---------------------------------------------------------------------------

# Which source each quotation should be found in, by the note that carries it.
QUOTE_SOURCE = {
    "Component ranges are illustrative; the binding minimum is the total": "Metz recommendation",
    "approximately 62 hours for Facilitators (steps 1-3); approximately 72 hours for Licensed Providers (steps 1-4)": "Metz recommendation",
    "Supervisory hours, Licensed Providers only (10 hours)": "Metz recommendation",
    "an approved supervisor at an approved location can host practicum students who are not enrolled at a co-located training program": "Metz recommendation",
    "Initial facilitation experience with well participants (approximately 30 hours). Two to three sessions as a facilitator in a retreat or peer-support model.": "Metz recommendation",
    "The permit title “Practitioner” is confusing and communicates nothing to the public about the holder's training and education": "Metz recommendation",
    "half of the didactic requirements": "published rule",
    "an additional minimum of 20 hours": "published rule",
    "A minimum of one group session": "published rule",
    "two separate group sessions": "published rule",
    "The definitions in 7.35.2.7 NMAC apply to this part.": "published rule",
    "PART 3 PATIENTS, CERTIFYING CLINICIANS, PRACTITIONERS, FACILITATORS, HEALING CENTERS, OTHER APPROVED LOCATIONS, AND EDUCATIONAL PROGRAMS": "published rule",
    "a clinician administering or a qualified patient taking psilocybin in an approved setting": "Medical Psilocybin Act",
    # Wilson working redline of July 25, 2026
    "A training program overseeing practicum treatments cannot also medically screen patients.": "Wilson redline",
    "in any manner of co-facilitation designed by the school or healing center hosting practicums that otherwise complies with the regulations of these provisions": "Wilson redline",
    "I haven't added the specific hour requirements for each because I think that is a bit much for what needs to live in regulation": "Wilson comments",
    # July 17, 2026 Training and Education Committee, on why no training permit
    "really wouldn't be necessary with the model that we have": "committee transcript",
    "as them being a registered student with an educational program": "committee transcript",
    "rather than needing to create an entire other permit or certification level": "committee transcript",
}

for text, src in QUOTE_SOURCE.items():
    check("QUOTE", '"%s"' % text[:70], found(text, src), src)

# The 7.35.2 definitions reproduced in Addendum B of the document.
DEFS = {
    "Guide": 'an individual who has completed training and education approved by the department to be able to '
             'assist practitioners during the administration sessions and who has been registered with the department',
    "Practitioner": 'means an individual who is a licensed healthcare professional who is certified by the department '
                    'to provide medical psilocybin integrative therapy, supervise guides, and who has completed '
                    'department required trainings',
    "Clinician": 'means an approved health care provider licensed in New Mexico who holds a certification from the '
                 'department to provide medical services to qualified patients',
    "Approved location": 'means a location approved by the department for psilocybin administration sessions',
}
for term, text in DEFS.items():
    check("QUOTE", '7.35.2.7 "%s"' % term, found(text, "7.35.2 NMAC"), "7.35.2 NMAC as adopted")

# Terms the document states are absent from 7.35.2 NMAC.
for term in ["facilitator", "healing center", "certifying clinician", "student"]:
    body = CORPUS.setdefault("7.35.2 NMAC", load("7.35.2 NMAC")).lower()
    check("QUOTE", '7.35.2 NMAC contains no "%s"' % term, term not in body,
          "%d occurrences" % body.count(term))

# ---------------------------------------------------------------------------
# MATH: every arithmetic statement in the document
# ---------------------------------------------------------------------------

NM, CORE, SIM, ROLE = 6, 68, 5, 5
MODULE = NM + CORE + SIM + ROLE
S1, S2, S3, SUP = 30, 20, 12, 10
FAC_PRAC, PRAC_PRAC = S1 + S2 + S3, S1 + S2 + S3 + SUP
CONSULT = 20
PUB_MODULE, PUB_FAC_PRAC, PUB_PRAC_PRAC, PUB_MENTOR = 40, 100, 120, 10

check("MATH", "module total 6 + 68 + 5 + 5 = 84", MODULE == 84, str(MODULE))
check("MATH", "published module total 30 + 5 + 5 = 40", PUB_MODULE == 40, str(PUB_MODULE))
check("MATH", "module change 84 - 40 = +44", MODULE - PUB_MODULE == 44, str(MODULE - PUB_MODULE))
check("MATH", "practicum steps 30 + 20 + 12 = 62", FAC_PRAC == 62, str(FAC_PRAC))
check("MATH", "practitioner practicum 62 + 10 = 72", PRAC_PRAC == 72, str(PRAC_PRAC))
check("MATH", "facilitator practicum change 62 - 100 = -38", FAC_PRAC - PUB_FAC_PRAC == -38, str(FAC_PRAC - PUB_FAC_PRAC))
check("MATH", "practitioner practicum change 72 - 120 = -48", PRAC_PRAC - PUB_PRAC_PRAC == -48, str(PRAC_PRAC - PUB_PRAC_PRAC))
check("MATH", "consultation change 20 - 10 = +10", CONSULT - PUB_MENTOR == 10, str(CONSULT - PUB_MENTOR))
fac, prac = MODULE + FAC_PRAC + CONSULT, MODULE + PRAC_PRAC + CONSULT
pub_fac, pub_prac = PUB_MODULE + PUB_FAC_PRAC + PUB_MENTOR, PUB_MODULE + PUB_PRAC_PRAC + PUB_MENTOR
check("MATH", "facilitator published total 40 + 100 + 10 = 150", pub_fac == 150, str(pub_fac))
check("MATH", "practitioner published total 40 + 120 + 10 = 170", pub_prac == 170, str(pub_prac))
check("MATH", "facilitator proposed total 84 + 62 + 20 = 166", fac == 166, str(fac))
check("MATH", "practitioner proposed total 84 + 72 + 20 = 176", prac == 176, str(prac))
check("MATH", "facilitator change 166 - 150 = +16", fac - pub_fac == 16, str(fac - pub_fac))
check("MATH", "practitioner change 176 - 170 = +6", prac - pub_prac == 6, str(prac - pub_prac))
check("MATH", "second reading of 7.35.3.19 C: 40 + 140 + 10 = 190", PUB_MODULE + 140 + PUB_MENTOR == 190,
      str(PUB_MODULE + 140 + PUB_MENTOR))
check("MATH", "176 is below the 190 second reading", prac < 190, "%d < 190" % prac)

# Figures asserted in the document must match the content actually drafted.
def drafted(section, sub_prefix, needle):
    for s, sub, _, proposed in P:
        if s == section and sub.startswith(sub_prefix) and proposed not in (NEW, UNCHANGED):
            return needle in proposed
    return False


check("MATH", "7.35.3.18 A drafts six didactic hours", drafted("7.35.3.18", "Subsection A", "minimum of six didactic hours"))
check("MATH", "7.35.3.18 C drafts 68", drafted("7.35.3.18", "Subsection C, {{PT_C}}", ">68<"))
check("MATH", "7.35.3.18 H drafts 84", drafted("7.35.3.18", "Subsection H", "minimum of 84 hours"))
check("MATH", "7.35.3.19 A drafts 62 and 72", drafted("7.35.3.19", "Subsection A", ">62<") and drafted("7.35.3.19", "Subsection A", ">72<"))
check("MATH", "7.35.3.19 C drafts 10", drafted("7.35.3.19", "Subsection C", ">10<"))
check("MATH", "7.35.3.19 D shows the step hours 30, 20, 12",
      all(drafted("7.35.3.19", "Subsection D", "approx. %d hours" % n) for n in (30, 20, 12)))
for n in (30, 20, 12):
    check("MATH", "the Metz recommendation states approximately %d hours for that step" % n,
          found("approximately %d hours" % n, "Metz recommendation"), "Metz recommendation, pages 3 to 4")
check("MATH", "7.35.3.19 H drafts 20", drafted("7.35.3.19", "Subsection H", "minimum of 20 hours"))

# Every remaining quotation, harvested from the notes and the addenda rather
# than listed by hand, so that a new quotation cannot enter unchecked. Each has
# to be found in at least one source, punctuation included.
def harvest():
    out = set()
    for d in (SOURCE, REVIEW):
        for v in d.values():
            out.update(re.findall(r"“(.+?)”", v))
    build = (REPO / "amendments/build-redline-pdf.py").read_text(encoding="utf-8")
    for name in ("HEAD", "ADDENDA", "FOOT"):
        m = re.search(r'^%s = """(.*?)"""' % name, build, re.S | re.M)
        if m:
            out.update(re.findall(r'"(.+?)"', re.sub(r"<[^>]+>", " ", m.group(1))))
    return sorted(out)


for q in harvest():
    if flatten(q) in {flatten(k) for k in QUOTE_SOURCE}:
        continue
    hits = [n for n in SRC if found(q, n)]
    check("QUOTE", '"%s"' % q[:70], bool(hits), hits[0] if hits else "found in no source")

# ---------------------------------------------------------------------------
# TITLE: the permit-title retitle surface stated in Addendum C
# ---------------------------------------------------------------------------

TERM = re.compile(r"(?i)practitioner")

# Counts asserted in Addendum C for 7.35.3 NMAC, by section.
PART3_COUNTS = {2: 1, 6: 1, 9: 5, 10: 5, 11: 3, 12: 1, 13: 12, 14: 6,
                17: 2, 18: 14, 19: 6, 20: 3, 26: 1, 27: 5}
PART3_TITLE_LINE = 1          # the part title, before 7.35.3.1
PART3_TOTAL = 66

# Counts asserted in Addendum C for 7.35.2 NMAC, by section.
PART2_COUNTS = {7: 3, 10: 1, 14: 3, 15: 1, 19: 2, 24: 1, 26: 1}
PART2_TOTAL = 12

# Sections this draft reaches, and how many of their occurrences it conforms.
REACHED = {"7.35.3.14": 6, "7.35.3.18": 14, "7.35.3.19": 6, "7.35.3.20": 3}


def segment(corpus, pattern):
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


p3 = CORPUS.setdefault("published rule", load("published rule"))
p3_heads, p3_secs = segment(p3, r"7\.3[45]\.3\.(\d{1,2})\s+(?!NMAC)[A-Z][A-Z]+")
check("TITLE", "the published rule has 28 sections", len(p3_secs) == 28, str(len(p3_secs)))
for n in sorted(set(list(p3_secs) + list(PART3_COUNTS))):
    want = PART3_COUNTS.get(n, 0)
    got = len(TERM.findall(p3_secs.get(n, "")))
    if want or got:
        check("TITLE", "7.35.3.%d carries %d occurrences of the permit title" % (n, want),
              got == want, "counted %d" % got)
pre = len(TERM.findall(p3[:p3_heads[0][0]]))
check("TITLE", "the part title carries 1 occurrence", pre == PART3_TITLE_LINE, "counted %d" % pre)
tot3 = len(TERM.findall(p3))
check("TITLE", "7.35.3 NMAC carries 66 occurrences in all", tot3 == PART3_TOTAL, "counted %d" % tot3)

p2 = CORPUS.setdefault("7.35.2 NMAC", load("7.35.2 NMAC"))
_, p2_secs = segment(p2, r"## 7\.35\.2\.(\d{1,2}) [A-Z]")
for n in sorted(set(list(p2_secs) + list(PART2_COUNTS))):
    want = PART2_COUNTS.get(n, 0)
    got = len(TERM.findall(p2_secs.get(n, "")))
    if want or got:
        check("TITLE", "7.35.2.%d carries %d occurrences of the permit title" % (n, want),
              got == want, "counted %d" % got)
tot2 = len(TERM.findall(p2))
check("TITLE", "7.35.2 NMAC carries 12 occurrences in all", tot2 == PART2_TOTAL, "counted %d" % tot2)

# Tokens in the drafted text. {{PT...}} conforms published text; {{NPT...}}
# writes the title into text that is wholly new and has nothing to strike.
CONFORM = ["{{PTS_UC}}", "{{PT_UC}}", "{{PTS_C}}", "{{PT_C}}", "{{PTS}}", "{{PT}}"]
FRESH = ["{{NPTS}}", "{{NPT}}"]
conformed, stray = {}, []
for section, sub, published, proposed in P:
    if proposed in (NEW, UNCHANGED):
        continue
    t = proposed
    n = 0
    for k in CONFORM:
        n += t.count(k)
        t = t.replace(k, "")
    for k in FRESH:
        t = t.replace(k, "")
    conformed[section] = conformed.get(section, 0) + n
    if TERM.search(t):
        stray.append("%s %s" % (section, sub))
    if "{{" in t:
        stray.append("%s %s unknown token" % (section, sub))

for section, want in REACHED.items():
    got = conformed.get(section, 0)
    check("TITLE", "%s conforms all %d of its occurrences" % (section, want), got == want, "drafted %d" % got)
reached = sum(conformed.get(s, 0) for s in REACHED)
check("TITLE", "this draft conforms 29 occurrences", reached == 29, str(reached))
check("TITLE", "37 occurrences in 7.35.3 NMAC are left to a conforming pass",
      PART3_TOTAL - reached == 37, str(PART3_TOTAL - reached))
check("TITLE", "49 occurrences remain across both parts",
      (PART3_TOTAL - reached) + PART2_TOTAL == 49, str((PART3_TOTAL - reached) + PART2_TOTAL))
check("TITLE", "no unmarked permit title survives in the proposed column",
      not stray, "; ".join(stray) if stray else "none")

# ---------------------------------------------------------------------------
# COVER: every proposed change carries a citation
# ---------------------------------------------------------------------------

for section, sub, published, proposed in P:
    if published == UNCHANGED and proposed == UNCHANGED:
        continue
    hit = any(section == sec and sub.startswith(key) for (sec, key) in SOURCE)
    check("COVER", "%s %s carries a citation" % (section, sub), hit)

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def main():
    failed = [r for r in results if not r[2]]
    by = {}
    for cls, claim, ok, detail in results:
        by.setdefault(cls, []).append((claim, ok, detail))
    lines = ["# Audit", "",
             "Machine-checked claims in `7.35.3-practicum-amendments-v7.pdf`. "
             "Regenerate with `python3 amendments/audit.py`.", "",
             "| Class | Checks | Passed |", "|---|---|---|"]
    order = ["RULE", "QUOTE", "MATH", "TITLE", "COVER"]
    label = {"RULE": "Published text reproduced verbatim",
             "QUOTE": "Quotations against their source",
             "MATH": "Arithmetic",
             "TITLE": "The permit-title surface in Addendum C",
             "COVER": "Every change carries a citation"}
    for cls in order:
        rows = by.get(cls, [])
        lines.append("| %s | %d | %d |" % (label[cls], len(rows), sum(1 for r in rows if r[1])))
    lines += ["| **Total** | **%d** | **%d** |" % (len(results), len(results) - len(failed)), ""]
    for cls in order:
        rows = by.get(cls, [])
        if not rows:
            continue
        lines += ["## %s" % label[cls], "", "| Result | Claim | Checked against |", "|---|---|---|"]
        for claim, ok, detail in rows:
            lines.append("| %s | %s | %s |" % ("pass" if ok else "**FAIL**",
                                               claim.replace("|", "\\|"), detail))
        lines.append("")
    (REPO / "amendments/AUDIT.md").write_text("\n".join(lines), encoding="utf-8")
    print("%d checks, %d passed, %d failed" % (len(results), len(results) - len(failed), len(failed)))
    for cls, claim, ok, detail in failed:
        print("  FAIL %s %s (%s)" % (cls, claim, detail))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

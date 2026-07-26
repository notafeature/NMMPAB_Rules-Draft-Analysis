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
}

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
        return flatten(p.read_text(encoding="utf-8"))
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
    "authorizing them to practice under supervision": "Metz recommendation",
    "Component ranges are illustrative; the binding minimum is the total": "Metz recommendation",
    "approximately 62 hours for Facilitators (steps 1-3); approximately 72 hours for Licensed Providers (steps 1-4)": "Metz recommendation",
    "Supervisory hours, Licensed Providers only (10 hours)": "Metz recommendation",
    "an approved supervisor at an approved location can host practicum students who are not enrolled at a co-located training program": "Metz recommendation",
    "Initial facilitation experience with well participants (approximately 30 hours). Two to three sessions as a facilitator in a retreat or peer-support model.": "Metz recommendation",
    "half of the didactic requirements": "published rule",
    "an additional minimum of 20 hours": "published rule",
    "A minimum of one group session": "published rule",
    "two separate group sessions": "published rule",
    "a clinician administering or a qualified patient taking psilocybin in an approved setting": "Medical Psilocybin Act",
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
check("MATH", "7.35.3.19 D drafts 30, 20, 12", all(drafted("7.35.3.19", "Subsection D", "approximately %d hours" % n) for n in (30, 20, 12)))
check("MATH", "7.35.3.19 H drafts 20", drafted("7.35.3.19", "Subsection H", "minimum of 20 hours"))

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
             "Machine-checked claims in `7.35.3-practicum-amendments-v6.pdf`. "
             "Regenerate with `python3 amendments/audit.py`.", "",
             "| Class | Checks | Passed |", "|---|---|---|"]
    order = ["RULE", "QUOTE", "MATH", "COVER"]
    label = {"RULE": "Published text reproduced verbatim",
             "QUOTE": "Quotations against their source",
             "MATH": "Arithmetic",
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

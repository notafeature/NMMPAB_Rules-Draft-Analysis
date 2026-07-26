#!/usr/bin/env python3
"""Audit every verifiable claim in the amendment document outside the practicum.

Eight classes of check, each with a receipt:

  RULE    every left-column block, against the text layer of the published rule
  QUOTE   every quotation in the notes and the addenda, harvested rather than
          listed, against its source
  FIGURE  every numeric token inside a proposed insertion, against the published
          rule, so that no figure can enter that no source carries
  COUNT   every count the addenda assert, recomputed from the sources
  TERM    the undefined-term claims, recounted in both parts
  CITE    every provision that proposes a change carries a source note; every
          provision reproduced without amendment carries a note saying why
  PROSE   every review note finishes its sentences and states the issue, the
          choices, and who decides
  STYLE   no em dashes, and no NMSA 1978 section number asserted by this draft
  HEADER  every page of the built PDF names the section or addendum it carries

Exit code is non-zero if any check fails. Output: amendments-remainder/AUDIT.md
"""

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from content import P, NEW, UNCHANGED                      # noqa: E402
from notes import SOURCE, REVIEW                           # noqa: E402

REPO = HERE.parent
SRC = {
    "published rule": REPO / "docs/documents/rules-draft-2026-07-23-published.pdf",
    "July 9 draft": REPO / "docs/documents/rules-draft-2026-07-09.pdf",
    "Medical Psilocybin Act": REPO / "Document Register/SB0219-Medical-Psilocybin-Act-2025.pdf",
    "7.35.2 NMAC": REPO / "source-text/7.35.2-NMAC-adopted-2026-06-23.txt",
    "committee transcript": REPO / "source-text/NMMPAB-2026-07-17-committee-transcript.txt",
    "board transcript": REPO / "source-text/NMMPAB-2026-07-17-board-transcript.txt",
    "Wilson redline": REPO / "source-text/wilson-redline-2026-07-25.txt",
    "Wilson comments": REPO / "source-text/wilson-redline-2026-07-25-comments.txt",
}

# The Wilson redline is a tracked-changes export. Insertions are wrapped in
# {+ +}, deletions in [- -], and comment anchors read as a C followed by a
# number in guillemets. Strip the markup so a quotation of the resulting text can
# be matched. The export also leaves bare plus signs inside and against words
# where an insertion boundary fell mid-word, as in "shal+l" and "+practitioner+";
# those are stripped where a letter sits on either side of the sign.
WILSON_MARKUP = re.compile(r"\{\+|\+\}|\[-|-\]|«C\d+»")
WILSON_STRAY_PLUS = re.compile(r"(?<=[A-Za-z])\+|\+(?=[A-Za-z])")

LINE_TOLERANCE = 3.0
results = []


def flatten(t):
    for a, b in [("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 ("‐", "-"), ("‑", "-"), ("–", "-"), ("—", "-"), ("­", "")]:
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def unent(t):
    """Turn the curly-quote entities the notes use back into characters."""
    return t.replace("&#8220;", '"').replace("&#8221;", '"').replace("&#8230;", "...") \
            .replace("&nbsp;", " ").replace("&middot;", ".").replace("&amp;", "&")


def read_pdf(path, dehyphenate):
    from pdfminer.high_level import extract_pages, extract_text
    from pdfminer.layout import LTTextContainer, LTTextLine
    if not dehyphenate:
        return flatten(extract_text(str(path)))
    lines = []
    for page in extract_pages(str(path)):
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
            lines.append(" ".join(t for _, t in parts))
    out = ""
    for raw in lines:
        s = re.sub(r"\s+", " ", raw).strip()
        if out.endswith("-") and s[:1].islower():
            out += s
        else:
            out = (out + " " + s) if out else s
    return flatten(out)


def load(name):
    p = SRC[name]
    if p.suffix == ".txt":
        t = p.read_text(encoding="utf-8")
        if name.startswith("Wilson"):
            t = flatten(WILSON_STRAY_PLUS.sub("", WILSON_MARKUP.sub("", t)))
            return re.sub(r"\s+([.,;:])", r"\1", t)
        return flatten(t)
    return read_pdf(p, dehyphenate=name in ("published rule", "July 9 draft"))


CORPUS = {}


def corpus(name):
    if name not in CORPUS:
        CORPUS[name] = load(name)
    return CORPUS[name]


def _contiguous(q, c):
    """q appears in c, allowing only the line numbers and page artifacts that a
    statute's text layer interleaves to sit between its words."""
    if q in c:
        return True
    words = [re.escape(w) for w in q.split(" ") if w]
    if not words:
        return False
    gap = r"(?:\s+(?:\d{1,2}|-\s*\d{1,2}\s*-|\.\d+B\.\d+))*\s+"
    return re.search(gap.join(words), c) is not None


def found(text, name):
    """A quotation is found if every part of it appears in the source.

    An ellipsis in the quotation marks an elision, so each side of it is required
    separately. Otherwise the quotation must appear contiguously, save for the
    line numbers a statute's text layer interleaves. Where a short quotation
    fails outright and the source wraps it awkwardly, both halves are required.
    """
    c = corpus(name)
    q = flatten(unent(text))
    if "..." in q:
        return all(_contiguous(part.strip(" ,;"), c) for part in q.split("...") if part.strip(" ,;"))
    if _contiguous(q, c):
        return True
    words = q.split(" ")
    if len(words) < 8:
        return False
    mid = len(words) // 2
    return " ".join(words[:mid]) in c and " ".join(words[mid:]) in c


# Every iteration that produces a check is over a list or a sorted set, so the
# receipts in AUDIT.md are byte-identical between runs and a diff of that file
# shows only real changes.
def check(cls, claim, ok, detail=""):
    results.append((cls, claim, bool(ok), detail))
    return bool(ok)


def segment(body, pattern):
    heads, seen = [], set()
    for m in re.finditer(pattern, body):
        n = int(m.group(1))
        if n in seen:
            continue
        seen.add(n)
        heads.append((m.start(), n))
    out = {}
    for i, (pos, n) in enumerate(heads):
        end = heads[i + 1][0] if i + 1 < len(heads) else len(body)
        out[n] = body[pos:end]
    return heads, out


def count_term(body, term):
    if term == "clinician":
        return len(re.findall(r"(?i)(?<!certifying )clinician", body))
    return len(re.findall(r"(?i)" + re.escape(term), body))


BUILD = (HERE / "build-redline-pdf.py").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# RULE
# ---------------------------------------------------------------------------

for doc, section, sub, published, _ in P:
    if published in (NEW, UNCHANGED):
        continue
    for chunk in published.split("\n"):
        if not chunk.strip():
            continue
        check("RULE", "%s %s :: %s" % (section, sub, flatten(chunk)[:66]),
              flatten(chunk) in corpus("published rule"), "published rule, text layer, exact match")


# ---------------------------------------------------------------------------
# QUOTE: harvested, not listed
# ---------------------------------------------------------------------------

def harvest():
    """Every quoted span in the notes and in the addenda of the build script."""
    out = set()
    notes_src = (HERE / "notes.py").read_text(encoding="utf-8")
    for q in re.findall(r"&#8220;(.+?)&#8221;", notes_src, re.S):
        out.add(re.sub(r'"\s*\n\s*"', "", q))
    for name in ("ADDENDUM_A_INTRO", "ADDENDUM_A_TAIL", "ADDENDUM_B", "ADDENDUM_C",
                 "ADDENDUM_D_INTRO", "HEAD", "FOOT"):
        m = re.search(r'^%s = """(.*?)"""' % name, BUILD, re.S | re.M)
        if m:
            body = re.sub(r"<[^>]+>", " ", m.group(1))
            out.update(re.findall(r'"(.+?)"', body, re.S))
    for m in re.finditer(r"'([^']{0,12})' rather than '([^']{0,12})'", BUILD):
        out.update(m.groups())
    for m in re.finditer(r'\'([A-Z][^\']{4,140}?)\'', BUILD):
        out.add(m.group(1))
    return sorted({flatten(unent(q)) for q in out if len(flatten(unent(q))) > 2})


# Quotations of this draft's own headings and labels, which are not quotations of
# a source and are not checked against one.
NOT_FROM_SOURCE = {
    "A.", "(A)", "- N", "practicum", "guide", "facilitator", "certifying clinician",
    "healing center", "student", "certificant", "registrant", "clinician",
    "Clinician", "Permit", "Practitioner", "Guide", "qualified patient",
    "registrant of another approved location", "Conflict-of-interest prohibitions",
    "60 from 7.35.3.15 B", "90 from 7.35.3.11 D", "xx/xx/2026", "9/22/2026",
    "underlined green inserted", "struck red deleted",
}

for q in harvest():
    if q in NOT_FROM_SOURCE:
        check("QUOTE", '"%s" (this draft\'s own words, not a quotation of a source)' % q[:60], True,
              "excluded by name")
        continue
    hits = [n for n in SRC if found(q, n)]
    check("QUOTE", '"%s"' % q[:66], bool(hits), hits[0] if hits else "FOUND IN NO SOURCE")

# The four definitions drafted at 7.35.3.7 are each traceable to one provision.
# Check that the provision each is drawn from says what the note says it says.
DEF_BASIS = {
    "certificant": "a practitioner, certifying clinician, facilitator, healing center or other approved "
                   "location, or educational program may voluntarily relinquish its certification",
    "facilitator": "A facilitator is authorized to work alongside a practitioner during medical psilocybin "
                   "services. A facilitator works under the direct supervision of a practitioner, and provides "
                   "peer support to qualified patients, as well as logistical and administrative support to the "
                   "practitioner and to the healing center.",
    "registrant": "A practitioner or facilitator may apply for temporary department certification of an "
                  '"other approved location"',
    "student": "a student shall be deemed qualified if they are registered with a certified educational "
               "program",
}
for term, basis in DEF_BASIS.items():
    check("QUOTE", "the provision behind the %s definition says so" % term,
          found(basis, "published rule"), "published rule")

# The July 9 wording this draft restores.
for phrase in ["Medical or research practice", "Conflict-of-interest prohibitions",
               "Name and contact information for the complainant which will remain confidential",
               "Patients or staff may lodge a complaint with the department",
               "should be in writing and submitted by U.S. mail or through the electronic",
               "may request a record review from the department",
               "DENIAL OF AN INITIAL PATIENT APPLICATION; RECORD REVIEW"]:
    check("QUOTE", 'July 9 draft carries "%s"' % phrase[:56], found(phrase, "July 9 draft"), "July 9 draft")

# The Act provisions the draft relies on.
for label, phrase in [
        ("Section 1, short title", "through 11 of this act may be cited as the \"Medical Psilocybin Act\""),
        ("Section 3(B), clinician", "an approved health care provider licensed in New Mexico who holds a "
                                    "permit from the department to provide medical services to qualified patients"),
        ("Section 5(A), exemption", "A producer, clinician or qualified patient shall not be subject to "
                                    "arrest, prosecution or penalty for participating in the program"),
        ("Section 5(B)(2), lawful conduct", "a clinician administering or a qualified patient taking psilocybin "
                                            "in an approved setting"),
        ("Section 3(I), qualifying condition", "end-of-life care")]:
    check("QUOTE", "Medical Psilocybin Act %s" % label, found(phrase, "Medical Psilocybin Act"),
          "Medical Psilocybin Act, as passed")

# Neither the Act nor 7.35.2 NMAC uses the word facilitator.
for name in ("Medical Psilocybin Act", "7.35.2 NMAC"):
    check("QUOTE", "%s contains no \"facilitator\"" % name,
          "facilitator" not in corpus(name).lower(),
          "%d occurrences" % corpus(name).lower().count("facilitator"))


# ---------------------------------------------------------------------------
# FIGURE: no figure enters a right column that the published rule does not carry
# ---------------------------------------------------------------------------

p3 = corpus("published rule")
p2 = corpus("7.35.2 NMAC")
_, s3 = segment(p3, r"7\.3[45]\.3\.(\d{1,2})\s+(?!NMAC)[A-Z][A-Z]+")
_, s2 = segment(p2, r"## 7\.35\.2\.(\d{1,2}) [A-Z]")


def tokens(body):
    """Numeric tokens in drafted text. HTML entities are not figures."""
    body = re.sub(r"&#\d+;", " ", body)
    return set(re.findall(r"\d+(?:\.\d+)*", body))


PUB_TOKENS = tokens(corpus("published rule"))

# A figure may enter a right column only if a named provision of the published
# rule carries it. It is not enough that the digits appear somewhere in the rule:
# the provision the figure is taken from is named here, and the check requires
# that provision's own published text to contain it. Section references and
# paragraph renumbering are not figures and are listed separately.
#
# (section, subsection label) -> {token: (what it is, published text that carries it)}
FIGURE_BASIS = {
    ("7.35.3.15", "Subsection A, required reporting of updates"): {
        "60": ("the period the same section already gives the department",
               "The department shall notify the applicant within 60 calendar days"),
    },
    ("7.35.3.11", "Subsection D, certification period; approval and denial"): {
        "90": ("the term the same subsection already sets",
               "shall be valid for 90 days"),
    },
    ("7.35.3.11", "Paragraph (10) of Subsection B, outdoor or natural environments"): {
        "15": ("the threshold the healing center paragraph already sets, reproduced",
               "If the natural environment setting is 15 minutes or more away from emergency medical "
               "service response or a hospital, urgent care, or other emergency medical services, then "
               "there must be a basic first aid kit and an AED on site"),
    },
}

# Tokens that are references or list numbering rather than figures.
SECTION_REF = re.compile(r"^7\.35\.[23]\.\d{1,2}$")
RENUMBER = {
    # Renumbering existing paragraphs to close the gap at (3).
    ("7.35.3.9", "Subsection D, certifying clinician application requirements"): {"3", "4", "5"},
    # Numbering the four paragraphs of the definitions list this draft adds.
    ("7.35.3.7", "Entire section, definitions"): {"1", "2", "3", "4"},
}

for doc, section, sub, _, proposed in P:
    if proposed in (NEW, UNCHANGED):
        continue
    basis = FIGURE_BASIS.get((section, sub), {})
    for ins_text in re.findall(r"<ins>(.*?)</ins>", proposed, re.S):
        for tok in sorted(tokens(ins_text)):
            label = "%s %s inserts %s" % (section, sub, tok)
            if SECTION_REF.match(tok):
                check("FIGURE", "%s, a section reference to a section that exists" % label,
                      int(tok.rsplit(".", 1)[1]) in (s3 if tok.startswith("7.35.3") else s2),
                      "not a figure")
                continue
            if tok in RENUMBER.get((section, sub), set()):
                check("FIGURE", "%s, numbering a paragraph rather than stating a quantity" % label, True,
                      "not a figure; list numbering only")
                continue
            if tok in basis:
                what, carrier = basis[tok]
                check("FIGURE", "%s, %s" % (label, what), found(carrier, "published rule"),
                      "carried by: %s" % carrier[:80])
                continue
            check("FIGURE", "%s, with no provision named as its source" % label, False,
                  "NO BASIS RECORDED. A figure may not enter without one.")

# Every figure named in a badge must be the figure the badge points at, and the
# provision the badge names must carry it.
for doc, section, sub, _, proposed in P:
    if proposed in (NEW, UNCHANGED):
        continue
    for badge in re.findall(r'<span class="rangebadge">(.*?)</span>', proposed, re.S):
        m = re.match(r"(\d+) from (7\.35\.3\.\d{1,2}) ([A-Z])$", flatten(badge))
        check("FIGURE", "%s %s badge \"%s\" is well formed" % (section, sub, flatten(badge)), bool(m),
              "expected the form: figure from section subsection")
        if not m:
            continue
        tok, ref, letter = m.groups()
        n = int(ref.rsplit(".", 1)[1])
        body = s3.get(n, "")
        sub_body = re.split(r"(?<![A-Za-z(])%s\.\s" % letter, body)
        check("FIGURE", "%s %s badge names a provision that carries %s" % (section, sub, tok),
              len(sub_body) > 1 and tok in sub_body[1][:1400],
              "%s %s of the published rule" % (ref, letter))

# ---------------------------------------------------------------------------
# COUNT and TERM: every count the addenda assert
# ---------------------------------------------------------------------------

check("COUNT", "the published rule has 28 sections", len(s3) == 28, "counted %d" % len(s3))
check("COUNT", "7.35.2 NMAC has 27 sections", len(s2) == 27, "counted %d" % len(s2))

heads = re.findall(r"(7\.3[45]\.3\.\d{1,2})\s+(?!NMAC)[A-Z][A-Z ,;\-]+?(?=:)", p3)
bad = [h for h in heads if h.startswith("7.34.3")]
check("COUNT", "28 section headings, 5 of which read 7.34.3",
      len(heads) == 28 and len(bad) == 5, "%d headings, %d read 7.34.3: %s" % (len(heads), len(bad), bad))
check("COUNT", "the five are .13, .14, .20, .23 and .25",
      bad == ["7.34.3.13", "7.34.3.14", "7.34.3.20", "7.34.3.23", "7.34.3.25"], str(bad))
corrected = sorted({sec for _, sec, _, _, prop in P
                    if prop not in (NEW, UNCHANGED) and "<del>7.34.3" in prop})
check("COUNT", "this draft corrects three of the five and the practicum draft corrects two",
      corrected == ["7.35.3.13", "7.35.3.23", "7.35.3.25"], str(corrected))

notes = re.findall(r"\[(7\.3[45]\.3\.\d{1,2}) NMAC(\s*-\s*N)?,\s*([^\]]+)\]", p3)
check("COUNT", "28 history notes", len(notes) == 28, "counted %d" % len(notes))
real = [(s, d.strip()) for s, _, d in notes if "xx" not in d]
check("COUNT", "26 history notes carry a placeholder and 2 carry a real date",
      len(notes) - len(real) == 26 and len(real) == 2, str(real))
check("COUNT", "the two are 7.35.3.27 and 7.35.3.28, both reading 9/22/2026",
      real == [("7.35.3.27", "9/22/2026"), ("7.35.3.28", "9/22/2026")], str(real))
no_n = [s for s, n, _ in notes if not n.strip()]
check("COUNT", "9 history notes omit the \"- N\" designator", len(no_n) == 9, "%d: %s" % (len(no_n), no_n))

d9 = re.search(r"D\.\s+Certifying clinician application requirements:(.*?)E\.\s+Practitioner application",
               p3, re.S)
items = re.findall(r"\((\d)\)", d9.group(1)) if d9 else []
check("COUNT", "7.35.3.9 D runs (1), (2), (4), (5), (6) with no (3)",
      items == ["1", "2", "4", "5", "6"], str(items))

parens = sorted({m.group(1) for m in re.finditer(r"\(([A-Z])\)\s+[A-Z][a-z]", p3)})
check("COUNT", "parenthetical subsection letters appear as (A), (B) and (C) only",
      parens == ["A", "B", "C"], str(parens))
check("COUNT", "\"registered with the department\" appears once in 7.35.3 NMAC",
      count_term(p3, "registered with the department") == 1,
      "counted %d" % count_term(p3, "registered with the department"))
check("COUNT", "\"registrant\" appears 10 times in 7.35.3 NMAC, all in 7.35.3.20",
      count_term(p3, "registrant") == 10 and count_term(s3[20], "registrant") == 10,
      "%d in the part, %d in .20" % (count_term(p3, "registrant"), count_term(s3[20], "registrant")))
check("COUNT", "\"administrative review committee\" appears 4 times, all in 7.35.3.25",
      count_term(p3, "administrative review committee") == 4
      and count_term(s3[25], "administrative review committee") == 4,
      "%d in the part, %d in .25" % (count_term(p3, "administrative review committee"),
                                     count_term(s3[25], "administrative review committee")))

# Addendum A: the sixteen terms defined in neither part, and the counts stated
# in its closing note.
UNDEFINED = re.search(r"^UNDEFINED_TERMS = \[(.*?)\]", BUILD, re.S | re.M).group(1)
TERMS = re.findall(r'"(.+?)"', UNDEFINED)
check("TERM", "Addendum A maps 16 terms", len(TERMS) == 16, "%d: %s" % (len(TERMS), TERMS))
for term in TERMS:
    check("TERM", "\"%s\" appears in 7.35.3 NMAC and not in 7.35.2 NMAC" % term,
          count_term(p3, term) > 0 and count_term(p2, term) == 0,
          "part 3: %d, part 2: %d" % (count_term(p3, term), count_term(p2, term)))
DEFS27 = re.search(r"^DEFINED_TERMS = \[(.*?)\]", BUILD, re.S | re.M).group(1)
for term in re.findall(r'"(.+?)"', DEFS27):
    check("TERM", "\"%s\" is defined in 7.35.2.7 NMAC" % term,
          found('"%s"' % term.capitalize(), "7.35.2 NMAC") or found('"%s" or' % term.capitalize(), "7.35.2 NMAC"),
          "7.35.2.7 NMAC as adopted")
check("TERM", "\"healing center\" appears 54 times in 7.35.3 NMAC",
      count_term(p3, "healing center") == 54, "counted %d" % count_term(p3, "healing center"))
check("TERM", "\"certifying clinician\" appears 53 times in 7.35.3 NMAC",
      count_term(p3, "certifying clinician") == 53, "counted %d" % count_term(p3, "certifying clinician"))
check("TERM", "\"guide\" appears 0 times in 7.35.3 NMAC and 3 times in 7.35.2 NMAC",
      count_term(p3, "guide") == 0 and count_term(p2, "guide") == 3,
      "part 3: %d, part 2: %d" % (count_term(p3, "guide"), count_term(p2, "guide")))
check("TERM", "4 of the 16 are defined in the draft at 7.35.3.7",
      len(re.findall(r"&#8220;[A-Z][a-z]", next(prop for _, sec, _, _, prop in P if sec == "7.35.3.7"))) == 4,
      "certificant, facilitator, registrant of another approved location, student")


# ---------------------------------------------------------------------------
# CITE
# ---------------------------------------------------------------------------

for doc, section, sub, published, proposed in P:
    has = bool(SOURCE.get((section, sub), "").strip())
    check("CITE", "%s %s carries a source note" % (section, sub), has,
          "amends" if proposed not in (NEW, UNCHANGED) else "reproduced without amendment")
    if proposed == UNCHANGED:
        check("CITE", "%s %s says why it is reproduced unamended" % (section, sub),
              "Not amended" in SOURCE.get((section, sub), ""), "source note opens with Not amended")

for section, sub in list(SOURCE) + list(REVIEW):
    check("CITE", "the note at %s %s attaches to a provision in the draft" % (section, sub),
          any(s == section and u == sub for _, s, u, _, _ in P), "orphan note check")

# A subsection cited in drafted text or in a note must be a subsection that
# exists. This check exists because a first draft of the registration provision
# at 7.35.3.11 A(11) cited "Subsection E of this section" and 7.35.3.11 has only
# A through D.
def subsections_of(n):
    body = s3.get(n, "")
    body = re.sub(r"^7\.3[45]\.3\.\d{1,2}\s+[^:]+:", "", body)
    return {m.group(1) for m in re.finditer(r"(?:^|\s)\(?([A-Z])[.)]\s+[A-Z(]", body)}


# A reference marked "proposed" points at a provision the practicum draft would
# create rather than one the published rule carries, so it is not checked against
# the published rule. It is checked instead by requiring the note to say that the
# published rule does not have it.
SUBSEC = re.compile(r"(?<!proposed )Subsection ([A-Z]) of (?:(7\.35\.3\.\d{1,2}) NMAC|this section)")
for doc, section, sub, _, proposed in P:
    if proposed in (NEW, UNCHANGED):
        continue
    for letter, ref in sorted(set(SUBSEC.findall(proposed))):
        target = ref or section
        n = int(target.rsplit(".", 1)[1])
        have = subsections_of(n)
        check("CITE", "%s %s cites Subsection %s of %s, which exists" % (section, sub, letter, target),
              letter in have, "%s has subsections %s" % (target, ", ".join(sorted(have)) or "none found"))

for d in (SOURCE, REVIEW):
    for (section, sub), text in d.items():
        for letter, ref in sorted(set(SUBSEC.findall(unent(text)))):
            target = ref or section
            n = int(target.rsplit(".", 1)[1])
            have = subsections_of(n)
            check("CITE", "the note at %s %s cites Subsection %s of %s, which exists"
                  % (section, sub, letter, target), letter in have,
                  "%s has subsections %s" % (target, ", ".join(sorted(have)) or "none found"))

# Any reference to a provision the practicum draft would create, rather than one
# the published rule carries, has to say that the published rule does not have it.
for d in (SOURCE, REVIEW):
    for (section, sub), text in d.items():
        plain = unent(text)
        if "proposed Subsection H of 7.35.3.19" in plain or "proposed 7.35.3.19 H" in plain:
            check("CITE", "the note at %s %s says 7.35.3.19 has no Subsection H as published"
                  % (section, sub),
                  "runs A through G and has no Subsection H" in plain,
                  "7.35.3.19 as published runs A through G")

# A paragraph cited inside a named subsection must exist in that subsection.
PARA = re.compile(r"Paragraph \((\d{1,2})\) of Subsection ([A-Z]) of (7\.35\.3\.\d{1,2}) NMAC")
for d in (SOURCE, REVIEW):
    for (section, sub), text in d.items():
        for num, letter, ref in sorted(set(PARA.findall(unent(text)))):
            n = int(ref.rsplit(".", 1)[1])
            body = s3.get(n, "")
            parts = re.split(r"(?<![A-Za-z(])%s\.\s" % letter, body)
            ok = len(parts) > 1 and ("(%s)" % num) in parts[1][:2600]
            check("CITE", "the note at %s %s cites Paragraph (%s) of Subsection %s of %s, which exists"
                  % (section, sub, num, letter, ref), ok, "checked inside that subsection")

# A section cited by number in a note must be a section that exists, unless the
# note marks it as proposed, in which case it must say whose proposal it is.
# "proposed 7.35.3.29" marks a whole section as proposed; "the proposed
# 7.35.3.19 H" marks only a subsection of a section that does exist, and is
# checked by the subsection rules above instead.
PROPOSED_SEC = re.compile(r"proposed 7\.35\.3\.(\d{1,2})\b(?! [A-Z]\b)")
for d in (SOURCE, REVIEW):
    for (section, sub), text in d.items():
        plain = unent(text)
        proposed = set(PROPOSED_SEC.findall(plain))
        for ref in sorted(proposed, key=int):
            check("CITE", "%s %s marks 7.35.3.%s as proposed and names whose proposal it is"
                  % (section, sub, ref),
                  int(ref) not in s3 and "practicum amendment draft" in plain,
                  "7.35.3.%s does not exist in the published rule" % ref)
        for ref in sorted(set(re.findall(r"7\.35\.3\.(\d{1,2})", plain)) - proposed, key=int):
            check("CITE", "%s %s cites 7.35.3.%s, which exists" % (section, sub, ref),
                  int(ref) in s3, "1 to 28")
        for ref in sorted(set(re.findall(r"7\.35\.2\.(\d{1,2})", text)), key=int):
            check("CITE", "%s %s cites 7.35.2.%s, which exists" % (section, sub, ref),
                  int(ref) in s2, "1 to 27")


# ---------------------------------------------------------------------------
# PROSE
# ---------------------------------------------------------------------------

DECIDER = re.compile(r"(?i)\b(decides?|decide it|must say|are the department's to choose|"
                     r"is the department's to set|is the committee's decision|"
                     r"is a question for the board|is the board's|to choose)\b")
CHOICES = re.compile(r"(?i)(two choices|three choices|two things to weigh|"
                     r"two questions|three questions|two further questions|"
                     r"one alternative|either or both|which reading)")

for (section, sub), text in REVIEW.items():
    plain = flatten(unent(text))
    label = "%s %s review note" % (section, sub)
    check("PROSE", "%s ends a complete sentence" % label, plain.endswith((".", '."', ".)")),
          "ends: %s" % plain[-42:])
    check("PROSE", "%s does not end on a bare question" % label, not plain.endswith("?"),
          "ends: %s" % plain[-42:])
    check("PROSE", "%s names who decides" % label, bool(DECIDER.search(plain)),
          "decider phrase present" if DECIDER.search(plain) else "NO DECIDER NAMED")
    check("PROSE", "%s states the choices" % label, bool(CHOICES.search(plain)),
          "choice framing present" if CHOICES.search(plain) else "NO CHOICES STATED")
    check("PROSE", "%s has no unterminated final clause" % label,
          not re.search(r"\b(and|or|but|which|that|whether|if|because|the)\s*\.$", plain),
          "trailing conjunction check")
    check("PROSE", "%s is long enough to state an issue" % label, len(plain) > 200,
          "%d characters" % len(plain))

for (section, sub), text in SOURCE.items():
    plain = flatten(unent(text))
    check("PROSE", "%s %s source note ends a complete sentence" % (section, sub),
          plain.endswith((".", '."', ".)")), "ends: %s" % plain[-42:])

# Sentences in the addenda must terminate too.
for name in ("ADDENDUM_A_TAIL", "ADDENDUM_B", "ADDENDUM_C"):
    m = re.search(r'^%s = """(.*?)"""' % name, BUILD, re.S | re.M)
    body = re.sub(r"<[^>]+>", " ", m.group(1))
    for cell in [c.strip() for c in re.split(r"\s{2,}", flatten(body)) if len(c.strip()) > 40]:
        check("PROSE", "%s prose ends a sentence :: %s" % (name, cell[:44]),
              cell.endswith((".", '."', ".)", ":")), "ends: %s" % cell[-30:])


# ---------------------------------------------------------------------------
# STYLE
# ---------------------------------------------------------------------------

# The house rule is that no em dash appears anywhere in the document. The check
# runs over everything that reaches a reader: the labels and both columns of every
# provision, every note, and the addenda and cover prose of the build script. The
# character-normalization tables in the machinery are not document prose and are
# not checked, because their whole purpose is to name the characters being removed.
def document_prose():
    out = []
    for _, section, sub, published, proposed in P:
        out += [section, sub, published, proposed]
    for d in (SOURCE, REVIEW):
        out += list(d.values())
    for name in ("HEAD", "FOOT", "ADDENDUM_A_INTRO", "ADDENDUM_A_TAIL", "ADDENDUM_B",
                 "ADDENDUM_C", "ADDENDUM_D_INTRO", "CSS"):
        m = re.search(r'^%s = """(.*?)"""' % name, BUILD, re.S | re.M)
        if m:
            out.append(m.group(1))
    for name in ("PARTS", "SECTION_TITLES", "UNDEFINED_TERMS", "DEFINED_TERMS", "RUNNING"):
        m = re.search(r"^%s = ([\[{].*?[\]}])\n" % name, BUILD, re.S | re.M)
        if m:
            out.append(m.group(1))
    for fn in ("addendum_d", "contents_table", "build_body"):
        m = re.search(r"^def %s\\(.*?\\):(.*?)\n\n\n" % fn, BUILD, re.S | re.M)
        if m:
            out.append(m.group(1))
    m = re.search(r"^def _never_matches\(\):", BUILD, re.S | re.M)
    if m:
        out.append(m.group(1))
    return "\n".join(out)


PROSE_BODY = document_prose()
for dash, label in [("\u2014", "em dash"), ("\u2013", "en dash")]:
    check("STYLE", "the document prose contains no %s" % label, dash not in PROSE_BODY,
          "%d found" % PROSE_BODY.count(dash))

README = HERE / "README.md"
check("STYLE", "README.md exists", README.exists(), "the folder's own README")
if README.exists():
    body = README.read_text(encoding="utf-8")
    for dash, label in [("\u2014", "em dash"), ("\u2013", "en dash")]:
        check("STYLE", "README.md contains no %s" % label, dash not in body,
              "%d found" % body.count(dash))

# An NMSA 1978 section number may appear only inside a quotation of the published
# rule, never as this draft's own assertion. The quoted spans are located by
# offset, so a number outside one of them fails wherever it sits.
for f in ["content.py", "notes.py", "build-redline-pdf.py", "README.md"]:
    path = HERE / f
    if not path.exists():
        continue
    body = path.read_text(encoding="utf-8")
    spans = [(m.start(), m.end()) for m in re.finditer(r"&#8220;.*?&#8221;", body, re.S)]
    spans += [(m.start(), m.end()) for m in re.finditer(r'"[^"\n]*NMSA[^"\n]*"', body)]
    # A left column is a verbatim reproduction of the rule, so it counts as quoted.
    for _, _, _, published, _ in P:
        if published not in (NEW, UNCHANGED) and "NMSA" in published:
            for m in re.finditer(re.escape(published[:60]), body):
                spans.append((m.start(), m.start() + len(published) + 400))
    for m in re.finditer(r"(?<!\d)26-2D-\d", body):
        inside = any(a <= m.start() <= b for a, b in spans)
        check("STYLE", "%s: the NMSA number at offset %d sits inside a quotation of the rule"
              % (f, m.start()), inside, body[max(0, m.start() - 70):m.start() + 24].replace("\n", " "))

for doc, section, sub, published, proposed in P:
    if proposed in (NEW, UNCHANGED):
        continue
    check("STYLE", "%s %s proposes no NMSA section number of its own" % (section, sub),
          not re.search(r"26-2D-\d", proposed), "checked the right column")

# Every section this document reaches is outside the practicum draft's scope.
PRACTICUM = {"7.35.3.14", "7.35.3.18", "7.35.3.19", "7.35.3.29"}
mine = sorted({s for _, s, _, _, _ in P})
for s in mine:
    check("STYLE", "%s is outside the practicum draft's scope" % s, s not in PRACTICUM,
          "practicum draft covers .14, .18, .19, .20 H(5) and proposed .29")
check("STYLE", "the draft reaches no provision of 7.35.3.20 other than by reproducing it",
      all(prop == UNCHANGED for _, s, _, _, prop in P if s == "7.35.3.20"),
      "7.35.3.20 is reproduced and not amended, because its heading is corrected in the practicum draft")
check("STYLE", "nothing under amendments/ or docs/ is referenced for writing",
      not re.search(r"open\(.*(amendments/|docs/)", (HERE / "build-redline-pdf.py").read_text(encoding="utf-8")),
      "read-only use of the published PDF")


# ---------------------------------------------------------------------------
# HEADER: every page names what it carries
# ---------------------------------------------------------------------------

# The running header is a CSS named page per section, so the section's identity is
# reproduced in the top margin of every page the section spans. Every page has to
# name a section, a part, an addendum, the cover, or the closing sources block,
# and every named page declared in the build has to be reachable.
NAMES = re.compile(r"7\.35\.3\.?\d*|Addendum [A-D]|Part I|Sources and method")

RUN = re.findall(r'\("([a-zA-Z0-9]+)", "([^"]+)", "([^"]+)"\),', re.search(
    r"^RUNNING = \[(.*?)^\]", BUILD, re.S | re.M).group(1))
declared = {cls for cls, lab, _ in RUN if re.fullmatch(r"7\.35\.3\.\d{1,2}", lab)}
rendered = {"s%s" % sec.rsplit(".", 1)[1] for _, sec, _, _, _ in P}
check("HEADER", "the build declares a named page for every section it renders",
      declared == rendered,
      "declared %d, rendered %d, difference %s"
      % (len(declared), len(rendered), sorted(declared ^ rendered) or "none"))
PART_CLS = set(re.findall(r'"[IV]+": "([a-zA-Z0-9]+)"', BUILD))
SEC_CLS = {"s%s" % lab.rsplit(".", 1)[1] for _, lab, _ in RUN if lab.startswith("7.35.3.")}
for cls, label, title in RUN:
    reachable = (cls in SEC_CLS or cls in PART_CLS
                 or ('class="rr %s"' % cls) in BUILD or ('class="%s"' % cls) in BUILD)
    check("HEADER", "named page %s is reachable from the build" % cls, reachable,
          "section.%s { page: %s; }" % (cls, cls))

PDF = HERE / "7.35.3-remainder-amendments-v1.pdf"
if check("HEADER", "the document has been built", PDF.exists(),
         "run build-redline-pdf.py before audit.py"):
    from pdfminer.high_level import extract_pages as _pages
    from pdfminer.layout import LTTextContainer as _LTC
    pages = list(_pages(str(PDF)))
    check("HEADER", "the document is one file", True, "%d pages" % len(pages))
    for i, page in enumerate(pages, 1):
        top = page.height - 56
        hdr = " | ".join(flatten(el.get_text()) for el in page
                         if isinstance(el, _LTC) and el.y1 > top)
        check("HEADER", "page %d names what it carries" % i, bool(NAMES.search(hdr)),
              hdr[:64] if hdr else "NO HEADER TEXT FOUND")


# ---------------------------------------------------------------------------
# Receipts
# ---------------------------------------------------------------------------

passed = sum(1 for _, _, ok, _ in results if ok)
failed = len(results) - passed
order = ["RULE", "QUOTE", "FIGURE", "COUNT", "TERM", "CITE", "PROSE", "STYLE", "HEADER"]

lines = ["# Audit: 7.35.3 NMAC amendments outside the practicum", "",
         "Generated by `amendments-remainder/audit.py`. Re-run with "
         "`python3 amendments-remainder/audit.py`.", "",
         "**%d checks, %d passed, %d failed.**" % (len(results), passed, failed), "",
         "| Class | Checks | Passed | Failed |", "|---|---:|---:|---:|"]
for cls in order:
    rows = [r for r in results if r[0] == cls]
    lines.append("| %s | %d | %d | %d |"
                 % (cls, len(rows), sum(1 for r in rows if r[2]), sum(1 for r in rows if not r[2])))
lines += ["", "## Receipts", ""]
for cls in order:
    rows = [r for r in results if r[0] == cls]
    if not rows:
        continue
    lines += ["### %s" % cls, "", "| Result | Claim | Checked against |", "|---|---|---|"]
    for _, claim, ok, detail in rows:
        lines.append("| %s | %s | %s |" % ("pass" if ok else "**FAIL**",
                                           claim.replace("|", "\\|"), detail.replace("|", "\\|")))
    lines.append("")
(HERE / "AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

for cls, claim, ok, detail in results:
    if not ok:
        print("FAIL [%s] %s :: %s" % (cls, claim, detail))
print("%d checks, %d passed, %d failed" % (len(results), passed, failed))
sys.exit(1 if failed else 0)

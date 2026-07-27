# What to change when something happens

This is a propagation map. Something happens in the rulemaking: a meeting, a new draft, a
published document. This file says where that lands on the site.

It answers one question: **"I have new source material. What do I have to touch?"**

It is not a style guide and not a philosophy. If you need to know what a page is for, open
the page.

---

## Part 1: The four trigger events

### Event A. A new rule draft is published

The heaviest event. Every page citation is keyed to a section number and a PDF page number,
and **both move between drafts.** A published draft has always renumbered something.

| Order | Touch | Why |
|---|---|---|
| 1 | `docs/documents/rules-draft-YYYY-MM-DD-*.pdf` | the file itself, dated name |
| 2 | Extract text, diff against the draft it supersedes | see Part 4 |
| 3 | Write the diff to `analysis/DATE-delta.md` | before editing any page |
| 4 | `tools/sync-provenance.py` → `CHAIN` | add the doc, move `"current": True`, describe what changed |
| 5 | `docs/documents.html` | register entry: what it is, page count, size, current or superseded |
| 6 | `docs/changes.html` | **add a new diff layer on top.** Previous published vs new published. Older layers stay, unedited, with their own pagination |
| 7 | Every page in the fact index (Part 2) whose figure changed | |
| 8 | Every `#page=N` anchor on every page | old anchors are wrong the moment the PDF changes |
| 9 | `docs/history.html` | dated entry, newest first |
| 10 | `docs/index.html` | what is open now, what is settled, next dates |
| 11 | Run the checks (Part 3) | |

**The trap that has caught three sessions:** a figure that was deferred, tabled, or sent back
to committee can still change in the next published draft. July 23 raised the shared didactic
module from 25 to 30 while it was deferred. Diff every provision. Do not assume anything
carried forward.

### Event B. A meeting happens

| Touch | Why |
|---|---|
| `docs/documents/NMMPAB-YYYY-MM-DD-*-transcript.pdf` | and the plain text in `source-text/` so it is searchable |
| `docs/documents.html` | register entry, and state whether the transcript carries speaker labels |
| `docs/history.html` | dated entry |
| The page that owns whatever was decided | Part 2 |
| `docs/index.html` | only if it changed what is open |
| Status pills on `eligibility.html` and `pathways.html` | if a vote moved something between settled and open |

A meeting changes the *record*. It does not change the rule text until a draft is published.
Where the meeting and the current draft disagree, state both and attribute each.

### Event C. A document lands that is not a rule draft

Recommendations, public comment, presentations, the hearing notice.

| Touch |
|---|
| `docs/documents/` and `docs/documents.html` |
| The one page it bears on |
| `docs/history.html` if it is dated and consequential |

### Event D. A date or a deadline changes

Dates are the most duplicated fact on the site. Change one and you are changing it in up to
eleven places. Grep first, then edit. See the fact index.

---

## Part 2: The fact index

**Which pages assert which fact.** Measured from the site, excluding tool-generated blocks.
Regenerate this table when pages are added or content moves; it is the thing that goes stale
first, and a stale version of it is how one fact ended up owned by two pages.

| Fact | Pages that assert it | N |
|---|---|---|
| Hearing date | about, changes, cs-number, deferred, documents, eligibility, guide, history, hours, index, input | 11 |
| The 7-0 deferral vote | changes, cs-number, deferred, documents, eligibility, history, hours, index, pathways, specialization | 10 |
| CS number requirement | changes, cs-number, eligibility, guide, history, hours, index, input | 8 |
| Reciprocity route | changes, documents, eligibility, history, hours, index, input, pathways | 8 |
| Waiver deadlines (Dec 31, 2027) | changes, deferred, eligibility, history, hours, index, pathways | 7 |
| Practicum 100 / 120 | changes, deferred, eligibility, hours, pathways | 5 |
| Supervisory 20 | changes, eligibility, history, hours, pathways | 5 |
| Simulated patient 5 | changes, deferred, eligibility, history, hours | 5 |
| BLS / CPR+AED / NM EMT | changes, eligibility, history, hours, pathways | 5 |
| Didactic 30 + 5 | changes, deferred, eligibility, hours | 4 |
| Clinician 8 didactic / 8 CME | changes, eligibility, hours, pathways | 4 |
| Continuing education 20 / 8 | changes, eligibility, history, hours | 4 |
| Practicum entry gate | changes, deferred, history, hours | 4 |
| Metz 84-hour proposal | documents, eligibility, history, hours | 4 |
| Mentoring 10 | changes, eligibility, pathways | 3 |
| Test-out | changes, eligibility, pathways | 3 |

**Regenerate it:**

```bash
cd docs && python3 - <<'PY'
import glob, re, os
pages = {}
for f in sorted(glob.glob('*.html')):
    s = open(f).read(); b = s[s.index('</head>'):]
    b = re.sub(r'<nav class="tnav".*?</nav>', '', b, flags=re.S)
    b = re.sub(r'<!-- provenance.*?/provenance -->', '', b, flags=re.S)
    pages[os.path.basename(f)[:-5]] = b
FACTS = [("practicum 100/120", r'100 hours|120 hours'),
         ("hearing date", r'August 28'),
         ("waiver dates", r'December 31, 2027')]   # add rows as facts are added
for name, pat in FACTS:
    hits = sorted(p for p, b in pages.items() if re.search(pat, b))
    print(f"{name:<24}{len(hits):>3}  {' '.join(hits)}")
PY
```

### What each page owns

A fact lives on exactly one page in full. Other pages state it in one line and link.

| Page | Owns |
|---|---|
| `index.html` | What is open right now, what is settled, the next dates |
| `guide.html` | A directory of the site: which page holds what |
| `history.html` | The dated chain of meetings, votes and documents, newest first |
| `documents.html` | The register: what each document is, whether it is current, a download, and what the site does not have |
| `changes.html` | Provision-level diffs, one layer per document transition, newest on top |
| `deferred.html` | Every provision a practicum change touches, and what is broken in the published text |
| `pathways.html` | Route to each permit by starting license |
| `eligibility.html` | Which licenses map to which permit; the two status tables |
| `hours.html` | Hour requirements by role, cost, and the record of what was said about them |
| `specialization.html` | The specialized-domain overlay and its proposed hours. None of it is in the rule |
| `cs-number.html` | The controlled-substance number at the certifying-clinician access point |
| `about.html` | Method, sources, corrections |
| `input.html` | The community input form |

---

## Part 3: What is generated, and what is not

Four things are generated by a tool and identical on all thirteen pages. **Never hand-edit
them.** Edit the tool, run it.

| Block | Tool | Covers |
|---|---|---|
| Site nav | `tools/sync-nav.py` | all 13 pages |
| Document chain | `tools/sync-provenance.py` → `CHAIN` | all 13 pages |
| Per-page revisions | `tools/sync-provenance.py` → `REVISIONS` | per page |
| Visit-counter beacon | `tools/sync-count.py` | all 13 pages |

A new page needs nothing special from the third tool: run it and the beacon appears. The
counter's endpoint is the `ENDPOINT` constant in `tools/sync-count.py` and lives nowhere else,
so moving the counter is `python3 tools/sync-count.py --endpoint https://NEW-HOST`. What the
counter records is stated on `about.html`; the Worker behind it is in `analytics/`, which has
its own README.

**Never let a second Cloudflare Worker config into this repository.** `analytics/wrangler.toml`
is the only one. The Cloudflare GitHub integration will offer to add a `wrangler.jsonc` at the
root that claims the same Worker name and serves `docs/` as a static site; accepting it
silently replaces the counter with a copy of the website. Keep the build connection
disconnected. This has happened twice.

**Everything else is hand-maintained in every page that states it.** That is why the fact
index above exists, and it is the site's largest structural cost: each page is a standalone
HTML file carrying its own full copy of the stylesheet, so moving a block between pages
leaves its CSS and its JavaScript behind. This has shipped broken twice.

### The checks

```bash
python3 tools/sync-nav.py --check          # nav identical everywhere
python3 tools/sync-provenance.py --check   # chain and revisions identical
python3 tools/sync-count.py --check        # visit-counter beacon identical everywhere
```

And these, which have no script yet and are run by hand. Seven of the eight failure classes
below have already shipped to the live site. Each is mechanically detectable, and none is
detected today.

| Check | What it catches | Has shipped broken |
|---|---|---|
| Cited section appears on cited page | `#page=N` and section numbers that disagree with the PDF | Yes, 9 at once |
| Class used in a body has a CSS rule on that page | content moved without its styles | Yes |
| Class emitted by JS has a CSS rule on that page | same, via the renderer | Yes |
| Every JS handler target exists in the markup | buttons moved without their JavaScript | Yes |
| Internal links and `#anchors` resolve | links left dead by a page split | Yes |
| No nested `<a>` | invalid HTML, browsers break the layout apart | Yes |
| Every page parses; zero em dashes | | |
| Quoted fragments appear verbatim in the source | paraphrase inside quotation marks | Yes |

---

## Part 4: Extracting and diffing a new draft

`pypdf` needs the `cryptography` import blocked in some environments.

```bash
python3 - <<'PY'
import sys
class B:
    def find_module(s, f, p=None):
        if f == "cryptography" or f.startswith("cryptography."): return s
    def load_module(s, f): raise ImportError()
sys.meta_path.insert(0, B())
from pypdf import PdfReader
r = PdfReader('docs/documents/NEW.pdf')
open('/tmp/new.txt','w').write("".join(
    f"\n===== PAGE {i} =====\n" + (p.extract_text() or "") for i, p in enumerate(r.pages, 1)))
PY
```

Then build the section-to-page map, because every citation on the site depends on it:

```bash
python3 - <<'PY'
import re
raw = open('/tmp/new.txt').read()
pages, cur = {}, None
for line in raw.split('\n'):
    m = re.match(r'===== PAGE (\d+) =====', line)
    if m: cur = int(m.group(1)); pages[cur] = []; continue
    if cur: pages[cur].append(line)
for p in sorted(pages):
    for m in re.finditer(r'7\.3[45]\.3\.(\d+)', '\n'.join(pages[p])):
        print(f"7.35.3.{m.group(1)}\tp.{p}")
PY
```

Diff section by section against the previous extraction, aligning on headings rather than
order. Write the result to `analysis/DATE-delta.md` **before** touching a page.

PDF extraction inserts spaces inside words. `certification` extracts as `certif ication`.
Normalise in the comparison; never reproduce it on the page.

---

## Part 5: Non-negotiables

- **Verbatim means verbatim.** Never paraphrase inside quotation marks. Mark elisions with an
  ellipsis and verify each side of it separately against the source.
- **Cite to the subsection and the page.** "7.35.3.19 (A), p. 13", not "the practicum section".
- **Unlabelled transcripts stay unlabelled.** Some transcripts carry no speaker labels. Name a
  speaker only where the surrounding text fixes it, and state the basis.
- **A meeting is the source for what it decided. The published draft is the source for what
  the rule says.** Where they differ, state both.
- **No em dashes.** Commas, colons, or a full stop.
- **Never nest an `<a>` inside another `<a>`.**
- **Links to documents open in a new tab.**
- **The repository is public.** Everything committed is published, including commit messages
  and everything in `analysis/`. There is no internal directory.

---

## Part 6: Known gaps

Things the site asserts that have no source document **in this repository**. Not errors;
missing paperwork. Landing any of these closes a gap.

Meeting notes and transcripts originate in **Notion** and are copied here. Three of the four
gaps below have a Notion page and are retrievable; they were never missing, only uncopied.

| Missing here | What rests on it | Upstream |
|---|---|---|
| June 26 board transcript | the 3-2 vote, the motion, the named "reluctant yes" | Notion, "Medical Psilocybin Advisory Board Meeting (June 2026)" |
| June 25 meeting record | statements attributed to that meeting | Notion, "Training & Education Rules: Vote Record, Redline & Open Items (6/25 to 6/26)" |
| July 16 End-of-Life committee | all of `specialization.html`, the specialization sections of `hours.html` and `eligibility.html`, the nine-session curriculum | Notion, "End of life Care 7/16" and "Proposed Adjunct Training in End-of-Life Psychedelic Care (Slides)" |
| Hearing notice | the hearing date, asserted on eleven pages | Not located. The date itself is not in doubt; see `CLAUDE.md` |

**Copying one in is Event C** (Part 1). Put the PDF in `docs/documents/`, the searchable text
in `source-text/`, register it on `docs/documents.html`, and record on the document itself
whether the transcript carries speaker labels.

`docs/documents.html` carries this list for readers. Keep the two in step.

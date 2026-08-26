# What to change when something happens

This is a propagation map. Something happens in the rulemaking: a meeting, a new draft, a
published document. This file says where that lands on the site.

It answers one question: **"I have new source material. What do I have to touch?"**

It is not a style guide and not a philosophy. If you need to know what a page is for, open
the page. `WRITING-STANDARD.md` holds the writing rules and `CLAUDE.md` the standing facts.

The site is fourteen content pages and four redirect stubs in `docs/`, and the facts that go
stale fastest live in generated regions: five sync tools own the menu, the record, the status
surfaces, the routes, and the provenance blocks, and `tools/check-site.py` fails when any
page drifts from its tool. The order of work for any event is therefore: **documents first,
then the tool data, then the run, then the hand-maintained prose, then the checks.**

---

## Part 1: The four trigger events

### Event A. A new rule draft is published

The heaviest event. Every page citation is keyed to a section number and a PDF page number,
and **both move between drafts.** A published draft has always renumbered something.

| Order | Touch | Why |
|---|---|---|
| 1 | `docs/documents/rules-draft-YYYY-MM-DD-*.pdf` | the file itself, dated name |
| 2 | Extract text to `source-text/`, diff against the draft it supersedes | see Part 4 |
| 3 | Write the diff to `analysis/DATE-delta.md` | before editing any page |
| 4 | `tools/sync-record.py` | the DOCUMENT event in `EVENTS`, the new register row in `DOCUMENTS` with `"chain": True` and `"status": "current"`, and the superseded row restated as superseded. Run it |
| 5 | `tools/sync-provenance.py` | a `CHANGED` entry for the new document: what it changed, which is the chain narrative every page's provenance block carries. Run it |
| 6 | `tools/sync-nav.py` | `MENU_DOCUMENTS`: the dropdown carries the register, the current operative text, and the documents of the most recent meeting or filing, per `DOCUMENTS_CONTRACT`. Run it |
| 7 | `tools/build-rule-page.py` | point `SOURCE` at the new extraction, update `DOC`, `DOCDATE`, and the hero constants, review `ANNOTATIONS`, run it. The script regenerates `docs/rule.html` with the shared menu imported from `sync-nav.py` and then runs the stylesheet, counter, and provenance tools over the fresh page itself. The August 2026 refusal-to-run is retired with the chrome that caused it |
| 8 | `tools/sync-status.py` | any `STATUS` item whose state or summary the new draft changes, and any date in `DATES`. Run it |
| 9 | `tools/sync-pathways.py` | every step citation carries a section number and a `#page=N` anchor; re-cite against the new PDF. Run it |
| 10 | `docs/changes.html` | **add a new diff layer on top.** Previous published vs new published. Older layers stay, unedited, with their own pagination |
| 11 | Every page in the fact index (Part 2) whose figure changed, and every remaining `#page=N` anchor in hand-maintained prose | old anchors are wrong the moment the PDF changes |
| 12 | `tools/sync-provenance.py` → `REVISIONS` | a dated entry for each page whose content changed, then run it again |
| 13 | Run the checks (Part 3) | |

**The trap that has caught three sessions:** a figure that was deferred, tabled, or sent back
to committee can still change in the next published draft. July 23 raised the shared didactic
module from 25 to 30 while it was deferred. Diff every provision. Do not assume anything
carried forward.

### Event B. A meeting happens

| Touch | Why |
|---|---|
| `docs/documents/NMMPAB-YYYY-MM-DD-*-transcript.pdf` | and the plain text in `source-text/`, so it is searchable |
| `tools/sync-record.py` | the MEETING event: what happened, outcome first; what changed as one state transition per line, each linking the page that owns the fact; documents attached by slug, with a register row stating whether the transcript carries speaker labels; an absence stated with a gap id where no record is filed yet. Run it |
| `tools/sync-status.py` | any `STATUS` item the meeting moved, and any date in `DATES` it changed. Run it |
| The page that owns whatever was decided | Part 2 |
| `tools/sync-provenance.py` → `REVISIONS` | a dated entry per changed page. Run it |
| Run the checks (Part 3) | |

A meeting changes the *record*. It does not change the rule text until a draft is published.
Where the meeting and the current draft disagree, state both and attribute each.

### Event C. A document lands that is not a rule draft

Recommendations, public comment, presentations, the hearing notice.

| Touch |
|---|
| `docs/documents/`, and `source-text/` for anything that will be cited |
| `tools/sync-record.py`: a register row, attached to the event it belongs to; if it closes a gap, remove the gap row and the event's absence line together, because `validate()` requires the two to agree. Run it |
| `tools/sync-nav.py` if it is a document of the most recent meeting or filing, per the dropdown contract. Run it |
| The one page it bears on, and its `REVISIONS` entry |
| Run the checks (Part 3) |

### Event D. A date or a deadline changes

Dates are the most duplicated fact on the site, but most of the copies are now generated.
Change the date in `tools/sync-status.py` (`DATES`, and every `STATUS` summary that names
it) and in `tools/sync-record.py` (the SCHEDULED event), update the dropdown subtitles in
`tools/sync-nav.py` if they name it, and run all three. Then grep the fact index for the
copies that live in hand-maintained prose and correct each one. The hearing date currently
appears on nine pages outside the generated regions; see Part 2. Grep first, then edit.

---

## Part 2: The fact index

**Which pages assert which fact, in hand-maintained prose.** Measured from the site August
13, 2026, excluding the shared menu, scripts, and every tool-generated region. A fact that
also lives in a tool's data (a status summary, a record event, a pathways step, the rule
page's annotations) is corrected in that tool, once; this table maps the copies that are
still corrected page by page. Regenerate it when pages are added or content moves; a stale
version of it is how one fact ended up owned by two pages.

| Fact | Pages that assert it in prose | N |
|---|---|---|
| Hearing date (anticipated October 2 since August 21; August 28 remains in historical prose) | changes, comment, cs-number, deferred, eligibility, index, pathways, recommendation, rule | 9 |
| The 7-0 deferral vote | changes, comment, cs-number, deferred, eligibility, pathways, recommendation, rule, training-hours-record | 9 |
| July 27 submission of the recommendation | about, changes, comment, deferred, eligibility, hours, index, pathways, recommendation, rule | 10 |
| CS number requirement | changes, comment, cs-number, eligibility, index, rule, training-hours-record | 7 |
| Practicum 100 / 120 | changes, deferred, eligibility, hours, index, rule, training-hours-record | 7 |
| Waiver deadlines (Dec 31, 2027) | changes, deferred, eligibility, recommendation, rule, training-hours-record | 6 |
| Submitted 80 classroom hours | changes, deferred, hours, recommendation, rule, training-hours-record | 6 |
| Staged practicum 60 / 70 | hours, recommendation, rule | 3 |
| Case presentation and consultation, 20 | eligibility, hours, recommendation | 3 |
| Mentoring 10 | changes, eligibility, hours, index, recommendation, rule, training-hours-record | 7 |
| Didactic 30 + 5 | changes, deferred, eligibility, hours, recommendation, rule, training-hours-record | 7 |
| Simulated patient 5 | changes, deferred, eligibility, hours, recommendation, rule, specialization, training-hours-record | 8 |
| Supervisory 20 | changes, deferred, eligibility, hours, training-hours-record | 5 |
| Reciprocity route | changes, eligibility, recommendation, rule, training-hours-record | 5 |
| BLS / CPR+AED / NM EMT | changes, eligibility, rule, training-hours-record | 4 |
| Metz recommendations | changes, eligibility, hours, pathways, recommendation, training-hours-record | 6 |
| Test-out | changes, eligibility, recommendation, specialization, training-hours-record | 5 |

`rule.html` appears in these rows because the whole page, annotations included, is generated
by `tools/build-rule-page.py`; a change to it is made in that script's `ANNOTATIONS` and the
script is run. Hand-editing the page is how drift started in August 2026 and is over.

**Regenerate it:**

```bash
cd docs && python3 - <<'PY'
import glob, re, os
pages = {}
for f in sorted(glob.glob('*.html')):
    s = open(f).read()
    if 'http-equiv="refresh"' in s: continue
    b = s[s.index('</head>'):]
    b = re.sub(r'<header class="topbar">.*?</header>', '', b, flags=re.S)
    b = re.sub(r'<script.*?</script>', '', b, flags=re.S)
    b = re.sub(r'<!-- (\w+(?: \w+)?): generated by tools/[a-z-]+\.py, '
               r'do not hand-edit -->.*?<!-- /\1 -->', '', b, flags=re.S)
    pages[os.path.basename(f)[:-5]] = b
FACTS = [("hearing date", r'October 2|August 28'),
         ("practicum 100/120", r'100 hours|120 hours|100 and 120'),
         ("waiver dates", r'December 31, 2027')]   # add rows as facts are added
for name, pat in FACTS:
    hits = sorted(p for p, b in pages.items() if re.search(pat, b))
    print(f"{name:<24}{len(hits):>3}  {' '.join(hits)}")
PY
```

### What each page owns

A fact lives on exactly one page in full. Other pages state it in one line and link. Where a
tool is named, the page's content is edited in that tool and regenerated, never by hand.

| Page | Owns | Content tool |
|---|---|---|
| `index.html` | What is open right now, what is settled, the next dates; the portals; the page directory at `#directory` | status surfaces: `tools/sync-status.py` |
| `rule.html` | The operative text, all twenty-eight sections verbatim, with the state of each contested provision noted at the provision | the whole page: `tools/build-rule-page.py` |
| `record.html` | The dated chain of events, the document register at `#documents`, and the gaps register at `#gaps` | `tools/sync-record.py` |
| `hours.html` | The working model of the deferred quantities: the three positions, program totals, cost | status kicker: `tools/sync-status.py` |
| `recommendation.html` | The submitted figures of July 27, beside the published text | |
| `comment.html` | How public comment works in this rulemaking, and the input log: form submissions and their published texts | |
| `about.html` | Method, the three verification tiers, corrections | |
| `pathways.html` | The route to each permit by starting license, step by step | picker and panels: `tools/sync-pathways.py` |
| `eligibility.html` | Which licenses map to which permit: both tables, the scope test, the role map | status legend dates: `tools/sync-status.py` |
| `cs-number.html` | The controlled-substance number at the certifying-clinician access point | |
| `specialization.html` | The July 16 specialized-domain proposal. None of it is in the rule | |
| `deferred.html` | Every provision a practicum change touches, and the three that do not work as written | |
| `changes.html` | Provision-level diffs, one layer per document transition, newest on top | |
| `training-hours-record.html` | The dated record of the hours question: roles, benchmarks, cost, the July 9 and 17 records, and public comment given at meetings | status strip: `tools/sync-status.py` |

The four redirect stubs, `documents.html`, `guide.html`, `history.html`, and `input.html`,
are retired addresses. They own nothing, they redirect into the pages above, and
`check-site.py` verifies each stub's target holds the anchor it promises.

Two ownership rules that have been decided and should not drift back:

- **The input log.** `comment.html` owns form submissions and their published texts. Public
  comment given at a meeting stays where the meeting record lives (the hours comments are at
  `training-hours-record.html#community`), and `comment.html` links it in one line rather
  than pasting it.
- **Status is dated on record pages.** `training-hours-record.html` carries a status strip
  "as of" a date, written by `tools/sync-status.py`; the live state of the rulemaking lives
  on `index.html` only.

---

## Part 3: What is generated, and what is not

The blocks below are generated. **Never hand-edit them**; `tools/check-site.py` or the
tool's own `--check` fails when a page drifts from its tool. Edit the tool, run it. Every
generated region in a page is fenced by a marker comment naming its tool.

| Block | Tool | Covers |
|---|---|---|
| Shared menu and its script, including the Documents dropdown and every page name | `tools/sync-nav.py` (`NAMES`, `TITLE_SUFFIX`, `GROUPS`, `MENU_DOCUMENTS`, `DOCUMENTS_CONTRACT`) | all 14 content pages |
| The chain of events, the document register, the gaps register | `tools/sync-record.py` (`EVENTS`, `DOCUMENTS`, `GAPS`) | `record.html` |
| The four status surfaces: Where things stand and the Scheduled dates, the hours kicker, the eligibility legend dates, the training-hours-record strip | `tools/sync-status.py` (`STATUS`, `DATES`, `STAGES`, `SCHEDULED`) | `index.html`, `hours.html`, `eligibility.html`, `training-hours-record.html` |
| The starting-license picker and every route panel | `tools/sync-pathways.py` (`STARTS`) | `pathways.html` |
| The provenance block: chain narrative and the per-page revision log | `tools/sync-provenance.py` (`CHANGED`, `REVISIONS`; the chain data is read from `tools/sync-record.py`) | all 14 content pages |
| The whole rule page | `tools/build-rule-page.py` (`ANNOTATIONS`; runs the stylesheet, counter, and provenance tools itself after writing) | `rule.html` |
| Visit-counter beacon | `tools/sync-count.py` | all 18 pages, stubs included |
| The versioned stylesheet link, `style.css?v=<hash>` | `tools/sync-css-version.py` | every page that links `style.css` |

A new page needs nothing special from the counter tool: run it and the beacon appears. The
counter's endpoint is the `ENDPOINT` constant in `tools/sync-count.py` and lives nowhere
else, so moving the counter is `python3 tools/sync-count.py --endpoint https://NEW-HOST`.
What the counter records is stated on `about.html`; the Worker behind it is in `analytics/`,
which has its own README.

**Never let a second Cloudflare Worker config into this repository.** `analytics/wrangler.toml`
is the only one. The Cloudflare GitHub integration will offer to add a `wrangler.jsonc` at the
root that claims the same Worker name and serves `docs/` as a static site; accepting it
silently replaces the counter with a copy of the website. Keep the build connection
disconnected. This has happened twice.

**Everything else is hand-maintained in every page that states it.** That is why the fact
index above exists.

### The checks

One entry point runs everything:

```bash
python3 tools/check-site.py
```

It covers, on all 18 pages: HTML parses, no nested anchors, no em dashes, the counter and
the versioned stylesheet link are present; and on the 14 content pages: the shared menu is
byte-identical and complete, titles, headings, and menu labels agree with `sync-nav.NAMES`,
every document in the dropdown has a register row, every internal link and cited anchor
resolves (including `#start=` state links into `pathways.html`, checked against the routes
data), every page is reachable, no live-blog tense, and the record, pathways, and status
regions match their tools.

Each sync tool also takes `--check` and exits 1 when a page is stale against it:

```bash
for t in nav record status pathways provenance count css-version; do
  python3 tools/sync-$t.py --check
done
```

Two failure classes are still checked by hand, and both have shipped broken before:

| Check | What it catches |
|---|---|
| Cited section appears on cited PDF page | `#page=N` and section numbers that disagree with the PDF itself |
| Quoted fragments appear verbatim in the source | paraphrase inside quotation marks |

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
- **Unlabelled transcripts stay unlabelled.** Both July 17 transcripts carry no speaker
  labels. Name a speaker only where the surrounding text fixes it, and state the basis.
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
missing paperwork. The reader-facing list is the gaps register at `record.html#gaps`, whose
data is `GAPS` in `tools/sync-record.py`; keep this table, that data, and the upstream
pointers in step. Landing any of these closes a gap.

Meeting notes and transcripts originate in **Notion** and are copied here. Where a gap has a
known Notion page it is named below; that material was never missing, only uncopied.

| Missing here (gap id) | What rests on it | Upstream |
|---|---|---|
| Official minutes, any meeting (`gap-minutes`) | the June 26 motion's mover is attributed from a meeting-note summary | the department has posted none; the June 26 summary relied on is in Notion, "Medical Psilocybin Advisory Board Meeting (June 2026)" |
| June 12 and June 25 recordings or transcripts (`gap-june`) | statements attributed to those meetings; the documents they produced are held | Notion, "Training & Education Rules: Vote Record, Redline & Open Items (6/25 to 6/26)"; no upstream is located for June 12 |
| July 16 End-of-Life Care committee record (`gap-july16`) | all of `specialization.html` and the specialization notes elsewhere | Notion, "End of life Care 7/16" and "Proposed Adjunct Training in End-of-Life Psychedelic Care (Slides)" |
| May 22 committee meeting record (`gap-may22`) | nothing; it is recorded as held and unposted | none exists; the department did not record it |
| August 14 board meeting recording or transcript, and the set-aside notice (`gap-aug14`) | the set-aside of the July 23 publication, and the August 25 stated date | Notion, "Medical Psilocybin Advisory Board - 8/14"; the working record is `analysis/8-14-board-extraction.md` |
| August 21 committee meeting recording or transcript (`gap-aug21`) | the August 21 meeting record, the October 2 anticipation, and the department's side-by-side | Notion, "Training and Education - 8/21"; the department recorded the meeting for posting. The working record is `analysis/8-21-committee-extraction.md` |

**Copying one in is Event C** (Part 1). Put the PDF in `docs/documents/`, the searchable
text in `source-text/`, add the register row and remove the gap in `tools/sync-record.py`
in the same edit, and record on the register row whether the transcript carries speaker
labels.

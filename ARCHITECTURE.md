# Site architecture

What exists, what was decided on September 7, 2026, and what is still open. Read this before
adding a page, a part, a hostname, or a project. `OPERATIONS.md` holds the infrastructure
facts and the runbooks; `CLAUDE.md` holds the standing rules; `UPDATING.md` says what to
touch when the rulemaking moves.

The words used here: a **host** is a hostname such as `rules.medical-psilocybin.org`; a
**project** is one deployable thing that answers on one host; a **part** is one Part of
Chapter 35, Title 7 NMAC, such as 7.35.2; a **page** is one HTML file.

---

## Part 1: The hosts

One host per project. Projects link to each other by absolute URL and share nothing at build
time. This was decided before September 2026 and stands.

| Host | Serves | Today (built) | Decided (not yet built) |
|---|---|---|---|
| `medical-psilocybin.org` | The hub: what this is, what it covers, where each area lives | The hub Worker is deployed and routed on the host (repository `medical-psilocybin.org`); a Cloudflare redirect rule still sends every path to `rules.` until it is disabled in the dashboard (`OPERATIONS.md` 4.3) | The hub answers |
| `www.medical-psilocybin.org` | The hub, same page | Same route, same redirect rule | Same |
| `rules.medical-psilocybin.org` | Analysis of the rules, and only that | This repository, `docs/` on `main`, GitHub Pages | The same host, with one path per part: `/7.35.2/`, `/7.35.3/` |
| `count.medical-psilocybin.org` | The visit counter and its dashboard | The `nmmpab-count` Worker in `analytics/` | Unchanged. Every new host is added to its allowed origins |
| `pathways.medical-psilocybin.org` | Practical guides for applicants, jurisdiction by jurisdiction, and a drafter for the two documents 7.35.2.8 names | Built September 7, 2026: its own repository and Worker, six pages worked for the City of Santa Fe and Santa Fe County | Other jurisdictions added one at a time; other tools follow the same pattern, one project each |

The rules site is the neutral reference and stays free. Anything paid, donation-funded, or
signed lives on another host. The rules site itself names no author in any committed file.

---

## Part 2: The rules site

### 2.1 Paths

The part number is the path. `rules.medical-psilocybin.org/7.35.3/` is the Training and
Education rule; `/7.35.2/` is the producer and laboratory rule. The number is how the
department, the board, the Register, and the hearing notice refer to each document, and it
does not change when a part's subject is described differently.

Inside a part, page file names are short slugs (`pathways.html`, `rule.html`) and page
**names** are plain language chosen for the reader ("Routes to a permit", "For producers").
The name is set once, in `NAMES` in `tools/sync-nav.py`, and the title, the H1, and the menu
label are generated from it. `tools/check-site.py` fails when they differ.

Paths shared by every part sit beside the parts, not inside them:

```
docs/
  index.html          the parts and their states; the entry to the rules site
  CNAME               rules.medical-psilocybin.org; deleting it takes the host down
  style.css           one stylesheet, linked by content hash
  documents/          every source PDF, flat, dated file names (unchanged from today)
  statute/            Article 2D section by section, and which part carries each section
  about/              how the site is built: method, verification tiers, the counter, corrections; site-wide
  board/              the board and its seven committees; five have no rule part yet
  7.35.2/             Part 2 pages
  7.35.3/             Part 3 pages: everything that is at the root of docs/ today
```

Every address at the root of `docs/` today becomes a redirect stub pointing into `7.35.3/`,
the same pattern the four existing stubs use, and `check-site.py` verifies each stub's
target.

### 2.2 What a part contains

Every part follows the same shape, so a reader who has learned one can read the other and a
session that has built one can build the next.

| Page | Owns | Built by |
|---|---|---|
| `index.html` | Where this part stands: adopted, proposed, amendments pending, next fixed date | status tool |
| `rule.html` | The operative text, every section verbatim, annotated at the contested provisions | `tools/build-rule-page.py` from the official extraction |
| `changes.html` | What each publication changed, one layer per transition, newest on top | hand-maintained |
| `record.html` | The dated chain of meetings and filings for this part, and its document rows | record tool |
| Pages by audience | One page per kind of reader the rule reaches ("For producers", "For testing laboratories", "Routes to a permit") | hand-maintained or a content tool |
| `comment.html` | How public comment works for this part, and the input channel | hand-maintained |

Part 3 has fourteen content pages; Part 2, built September 7, 2026, has six: `index`,
`rule` with the August 25 amendments noted at the three sections they would change,
`producers`, `laboratories`, `record`, and `comment`.

### 2.3 The tools are per part

Since September 7, 2026 every tool asks `tools/partlib.py` which Part it is working on
(`--part 7.35.3`, the default) and where that Part's pages live, and `check-site.py` checks the
Part's pages and the root together. Each tool still holds its data in constants at the top of
the file (`NAMES`, `GROUPS`, `STATUS`, `EVENTS`, `DOCUMENTS`, `STARTS`, `ANNOTATIONS`), and
since September 7, 2026 that data lives in `tools/parts/<part>/<tool>.py`, one file per tool
per Part, executed into the tool's namespace by `partlib.load_data()`; the tools hold code
only. A tool with no data for a Part stops with a plain message rather than writing one
Part's content into another's folder, and the pathways tool does nothing for a Part with no
routes. `tools/check-all.py` runs the checks for every Part.

### 2.4 The statute layer

The statute is NMSA 1978, Sections 26-2D-1 through 26-2D-11, Article 2D of Chapter 26,
enacted as Laws 2025, Chapter 73, effective June 20, 2025. Its short title, set by 26-2D-1,
is the Medical Psilocybin Act, and that name is used in prose. Citations use the compiled
section: "Section 26-2D-7 NMSA 1978". The bill number, Senate Bill 219, is cited only for
legislative history and for the bill's Sections 12 through 14, which amended other chapters.

`docs/statute/` carries Article 2D section by section, and for each section the part that
carries it, built September 7, 2026: 26-2D-7 is cited as authority by Parts 2 and 3;
26-2D-8, -9, -10, and -11 are carried by no published part. The statute folder is a
site-wide page outside any Part, listed in `SITE_DIRS` in `tools/partlib.py` and checked by
`check-site.py` with the root pages.

### 2.5 The board layer

`docs/board/` carries the Medical Psilocybin Advisory Board and its seven committees:
Patient Qualification and Safety; Dosage, Administration and Clinical Practice; Propagation;
Research and Continuous Improvement; Equity, Access and Cultural Considerations; End of Life
Care; Training and Education. Two committees have produced a rule part. The other five have a
page that states their meetings on the record and that no rule part is published. A committee
page never predicts a part number.

---

## Part 3: Sources

Every statement on the site rests on a document that a member of the public can obtain
without asking anyone. The documents the site relies on are held in `docs/documents/`, with
a searchable extraction in `source-text/`, and listed in the register on the record page.

The official text of an adopted part is the New Mexico Register issue that adopted it, or
the compiled NMAC file for the part. Both are published by the State Records Center and
Archives. The Register issue is the source for the rule page; the compiled file is the source
once the part has been amended, because it carries the history notes.

Working notes, drafts, meeting summaries, and any material that lives in a private workspace
are research. They inform the site and are never linked from it. No committed file carries a
link to, an identifier of, or the name of a page in a private workspace. Material that was
copied from one is replaced by the public document it stands for.

---

## Part 4: The repository

### 4.1 Today

```
docs/                    the site: the parts index, the stubs, statute/, about/, 7.35.2/, 7.35.3/, style.css, documents/
analysis/                extractions, deltas, research (Part 3)
source-text/             plain-text extractions (Part 3, the statute, 7.35.2)
Document Register/       original PDFs as received
amendments/              drafting for the practicum sections (Part 3), own audit harness
amendments-remainder/    drafting for the sections outside the practicum (Part 3), own audit harness
analytics/               the counter Worker; the only wrangler config in the repository
tools/                   the site tools, Part-aware through partlib.py
CLAUDE.md  WRITING-STANDARD.md  UPDATING.md  ARCHITECTURE.md  OPERATIONS.md  README.md
```

### 4.2 Decided

```
docs/                    the site, as in Part 2.1
parts/7.35.2/            analysis/, source-text/, drafting/, site.py
parts/7.35.3/            analysis/, source-text/, amendments/, amendments-remainder/, site.py
statute/                 the enrolled bill, the compiled Article 2D, analysis
board/                   board and committee extractions that belong to no single part
tools/                   part-aware tools
analytics/               unchanged
Document Register/       unchanged
```

`redesign/` was removed on September 7, 2026 and is recoverable from history.

The `parts/` and `statute/` folders are not yet made. The two drafting harnesses in
`amendments/` and `amendments-remainder/` read `source-text/` and `docs/documents/` by fixed
path and pass every one of their checks (245 and 772 on September 7, 2026); they are in use
for the October 2 hearing. The folder move waits until after the hearing so that nothing
those harnesses read moves under them.

The repository is public today and may become private later. Neither state changes what is
committed: nothing that names the compiler, nothing from a private workspace, no secret.

---

## Part 5: State of the decisions

| Decision | State | Where it lands |
|---|---|---|
| One host per project; the hub at the apex; `rules.` for rule analysis only | Decided | Part 1 |
| Parts as paths named by part number | Built September 7, 2026: `docs/7.35.3/`, the parts index, the stubs | Part 2.1 |
| Page names in plain language, set in one place | Decided; already the rule for Part 3 | Part 2.1 |
| One repository for the rules site, all parts | Decided; the `parts/` folder move waits until after the October 2 hearing | Part 4 |
| Statute cited by compiled section; the Act's name kept | Done September 7, 2026: the sweep of the pages and the tool data, and `docs/statute/` | Part 2.4 |
| No private-workspace references in any committed file | Done September 7, 2026 | Part 3 |
| Status vocabulary | Kept as `tools/sync-status.py` has it until it is cleaned up | |
| Part 2 pages | Built September 7, 2026: six pages in `docs/7.35.2/`, from the Register text and the department's rulemaking documents | Part 2.2 |
| Hosting for `rules.` | GitHub Pages stays while the repository is public. Moves to Cloudflare when the repository goes private | `OPERATIONS.md` Part 4 |
| The hub at the apex | Built and deployed September 7, 2026; answers once the redirect rule is disabled, one dashboard action | `OPERATIONS.md` 4.3 |
| Application hosts | `pathways.` built September 7, 2026; each further one gets its own project and repository | Part 1 |
| Paid tools, donations | Later. Not on `rules.` | Part 1 |
| Diff of the enrolled bill against the compiled Article 2D | Parked; about an hour of work | Part 2.4 |

### The order of work

1. This document and `OPERATIONS.md`, and the pointers in `CLAUDE.md` and `README.md`.
2. The layout move: `docs/` by Part, redirect stubs, part-aware tools, `redesign/` removed,
   private-workspace references removed, the official 7.35.2 text held. Done September 7,
   2026. The `parts/` folder move is deferred to after the hearing (Part 4.2).
3. Part 2: the official adopted text, the March 24 notice, the hearing exhibits, the
   department's response to comments, and the hearing officer's report into
   `docs/documents/`; the rule page built; the index, the two audience pages, the record,
   and the comment page. Done September 7, 2026.
4. The citation sweep to compiled-section form, and `docs/statute/`. Done September 7, 2026.
5. The hub at the apex, its own project. Built September 7, 2026; the redirect rule is the
   owner's switch.

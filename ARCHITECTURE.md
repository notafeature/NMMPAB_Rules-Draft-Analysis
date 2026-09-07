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
| `medical-psilocybin.org` | The hub: what this is, what it covers, where each area lives | A Cloudflare redirect rule sends every path to `rules.` with a 301 | A hub page. Its own project, not this repository |
| `www.medical-psilocybin.org` | Nothing of its own | Same redirect to `rules.` | Redirects to the apex |
| `rules.medical-psilocybin.org` | Analysis of the rules, and only that | This repository, `docs/` on `main`, GitHub Pages | The same host, with one path per part: `/7.35.2/`, `/7.35.3/` |
| `count.medical-psilocybin.org` | The visit counter and its dashboard | The `nmmpab-count` Worker in `analytics/` | Unchanged. Every new host is added to its allowed origins |
| Application hosts, for example `pathways.` | Tools that do something for a reader rather than describe the rule | None | One project each, in its own repository. The hub lists them; the rules site links to them where a page hands off to a tool |

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

Part 3 today has fourteen content pages; not every part needs that many. Part 2 starts with
`index`, `rule`, the August 25 amendments beside the adopted text, and one page each for
producers and laboratories.

### 2.3 The tools are per part

The eight tools in `tools/` were written for one flat `docs/`. Each holds its data in
constants at the top of the file (`NAMES`, `GROUPS`, `STATUS`, `EVENTS`, `DOCUMENTS`,
`STARTS`, `ANNOTATIONS`). The multi-part layout moves each part's data into a module of its
own, `parts/7.35.N/site.py`, and the tools take the part as an argument. The checks in
`check-site.py` run over every part. This is the largest single piece of the layout move and
is done on one branch, before any Part 2 content.

### 2.4 The statute layer

The statute is NMSA 1978, Sections 26-2D-1 through 26-2D-11, Article 2D of Chapter 26,
enacted as Laws 2025, Chapter 73, effective June 20, 2025. Its short title, set by 26-2D-1,
is the Medical Psilocybin Act, and that name is used in prose. Citations use the compiled
section: "Section 26-2D-7 NMSA 1978". The bill number, Senate Bill 219, is cited only for
legislative history and for the bill's Sections 12 through 14, which amended other chapters.

`docs/statute/` carries Article 2D section by section, and for each section the part that
implements it. As of September 7, 2026: 26-2D-7 is cited as authority by Parts 2 and 3;
26-2D-9, assessment reporting, is implemented by no published part.

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
docs/                    the site
analysis/                extractions, deltas, research (Part 3)
source-text/             plain-text extractions (Part 3, the statute, 7.35.2)
Document Register/       original PDFs as received
amendments/              drafting for the practicum sections (Part 3), own audit harness
amendments-remainder/    drafting for the sections outside the practicum (Part 3), own audit harness
analytics/               the counter Worker; the only wrangler config in the repository
redesign/                the July 26 redesign working folder; nothing served
tools/                   the site tools
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

`redesign/` is removed in the layout move. It is recoverable from history.

The repository is public today and may become private later. Neither state changes what is
committed: nothing that names the compiler, nothing from a private workspace, no secret.

---

## Part 5: State of the decisions

| Decision | State | Where it lands |
|---|---|---|
| One host per project; the hub at the apex; `rules.` for rule analysis only | Decided | Part 1 |
| Parts as paths named by part number | Decided | Part 2.1 |
| Page names in plain language, set in one place | Decided; already the rule for Part 3 | Part 2.1 |
| One repository for the rules site, all parts | Decided | Part 4 |
| Statute cited by compiled section; the Act's name kept | Decided | Part 2.4 |
| No private-workspace references in any committed file | Decided | Part 3 |
| Status vocabulary | Kept as `tools/sync-status.py` has it until it is cleaned up | |
| Hosting for `rules.` | GitHub Pages stays while the repository is public. Moves to Cloudflare when the repository goes private | `OPERATIONS.md` Part 4 |
| The hub at the apex | Decided; not built. Replaces the redirect rule | `OPERATIONS.md` Part 4 |
| Application hosts | None built. Each gets its own project and repository when it exists | Part 1 |
| Paid tools, donations | Later. Not on `rules.` | Part 1 |
| Diff of the enrolled bill against the compiled Article 2D | Parked; about an hour of work | Part 2.4 |

### The order of work

1. This document and `OPERATIONS.md`, and the pointers in `CLAUDE.md` and `README.md`.
2. The layout move: folders, redirect stubs, part-aware tools, `redesign/` removed,
   private-workspace references removed. No content changes. One branch.
3. Part 2: the official adopted text and the August 25 amendments into `docs/documents/`,
   the rule page built, the index and the two audience pages.
4. The citation sweep to compiled-section form, and `docs/statute/`.
5. The hub at the apex, its own project.

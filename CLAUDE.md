# Standing facts and working rules

Read this first. It holds what does not change between sessions, so it does not have to be
explained again.

## Read these before writing anything

| File | For |
|---|---|
| `WRITING-STANDARD.md` | How everything here is written. Not optional, and it applies to commit messages and pull request bodies as well as to the site |
| `UPDATING.md` | What to change when a meeting happens or a document is published. The fact index in Part 2 is the blast radius of any change |

## The two workstreams

They are separate. Do not let one drift into the other.

**1. The draft recommendation.** Amendment language for the Training and Education Committee,
built against the published rule. Lives in `amendments/`, on its own branch. Deadline-driven.

**2. The site.** `docs/`, thirteen pages, served from `main` by GitHub Pages at
https://notafeature.github.io/NMMPAB_Rules-Draft-Analysis/. A reference for people following
the rulemaking. No external deadline.

## The timeline, and why the dates are what they are

| Date | Day | What |
|---|---|---|
| July 17, 2026 | Friday | Board meeting, morning; Training and Education Committee, afternoon. Practicum and didactic hours deferred to the committee. Definitions also deferred to the committee, with the instruction to get language back to the department "sooner than later." No publication date was given |
| July 23, 2026 | **Thursday** | The department published the proposed rule and scheduled the hearing |
| July 28, 2026 | **Tuesday** | One month before the hearing. The date by which the committee's recommendation should be in the department's hands to be folded into the draft that goes to the hearing |
| August 28, 2026 | **Friday** | Rule hearing |

**The hearing date is a fact.** The department could not schedule the hearing until the rule was
published, and a rule must be published more than a month before its hearing. Publication on
July 23 gives 36 days. The department published on Thursday July 23 rather than waiting, because
the responsible director was out of state the following week. None of this is inference; it is
the sequence.

**What the department did not specify** is the date by which the committee's recommendation must
reach it. July 28 is the working date, one month before the hearing, on the same logic that
fixed the publication date. Treat it as the operative deadline unless told otherwise.

**No hearing notice document is held in this repository.** The date is sourced to the scheduling,
not to a filing. That gap is tracked in `UPDATING.md`, Part 6. Do not report the date as
unverified; report the notice as absent.

## Named people

Zurlo, Leeman, Peskuski, Dezbaá, Fatemi, Wilson, Caldwell, Burgard, Dunn, Ryan, Truckner. These
are the corrected spellings for auto-generated transcripts.

The July 9 transcript carries speaker labels. **Both July 17 transcripts do not.** Name a speaker
from an unlabelled transcript only where the surrounding text fixes it, and state the basis.

## Constraints

- **Never name who compiles the information or who reviews it,** in any committed file. Not in
  page text, not in a commit message, not in a pull request body. Meeting participants are named
  as participants; that is different.
- **This repository is public.** Everything committed is published, including commit messages and
  everything in `analysis/`. There is no internal directory.
- **Do not push to `main`.** Branch, commit, open a pull request.
- **Nothing here is final, promulgated rule text.**

## Where things are

| Path | What |
|---|---|
| `docs/` | The site. Served from `main` |
| `docs/documents/` | Source PDFs, linked from the site |
| `source-text/` | Plain-text extractions, searchable |
| `analysis/` | Extractions, deltas, research. Public |
| `amendments/` | Draft amendment language. Branch work |
| `tools/` | `sync-nav.py` and `sync-provenance.py`. Both take `--check` |

## Current state of truth

The operative document is `docs/documents/rules-draft-2026-07-23-published.pdf`: the department's
published proposed rule 7.35.3 NMAC, 19 pages, sections 7.35.3.1 through .28.

Earlier documents are history. Cite them only where a page is comparing versions.

The chain is defined in one place, `tools/sync-provenance.py`. When a document supersedes the
current one, edit that file first.

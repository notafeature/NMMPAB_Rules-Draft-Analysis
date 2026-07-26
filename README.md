# NMMPAB Rules Draft Analysis: Training and Education

A neutral, plain-language community reference for the New Mexico Medical Psilocybin Advisory Board's **Training and Education** rulemaking.

Goal: let anyone, including people who do not follow the legislative process, see what is being decided, what is at stake, what the options are, and what happened at each meeting. No advocacy. Verbatim draft language and attributed input only.

**Live site:** https://notafeature.github.io/NMMPAB_Rules-Draft-Analysis/ (GitHub Pages serves the `docs/` folder from `main`).

## Read these first

- **[CLAUDE.md](CLAUDE.md)** holds the standing facts: the timeline and the reasoning behind each date, the two workstreams, the corrected transcript spellings, and the constraints.
- **[WRITING-STANDARD.md](WRITING-STANDARD.md)** sets the register for everything written here, including commit messages and pull request bodies.
- **[UPDATING.md](UPDATING.md)** is the propagation map: something happens in the rulemaking, and it says where that lands on the site. Part 2 is the fact index, which is the blast radius of any change.

## The two workstreams

They are separate and they have different clocks.

1. **The draft recommendation.** Amendment language for the Training and Education Committee, built against the published rule. Lives in `amendments/`, on its own branch. Deadline-driven.
2. **The site.** `docs/`, thirteen pages, served from `main`. No external deadline.

## Where things stand

The operative document is the department's **proposed rule 7.35.3 NMAC, published July 23, 2026**, 19 pages, sections 7.35.3.1 through .28. It goes to a rule hearing on **August 28, 2026**.

Earlier documents are history and are cited only where a page compares versions: the June 12 committee recommendation, the June 25 department draft, and the July 9 board-meeting draft.

For what changed and when, see `docs/history.html` and `docs/changes.html`. For why the dates are what they are, see [CLAUDE.md](CLAUDE.md).

## What's here

```
NMMPAB_Rules-Draft-Analysis/
├── docs/                     <- the site, published by GitHub Pages from main
│   ├── index.html            <- what is open, what is settled, the next dates
│   ├── guide.html            <- a directory of the site: which page holds what
│   ├── history.html          <- the dated chain of meetings and documents, newest first
│   ├── documents.html        <- the register: every document, and what is missing
│   ├── changes.html          <- provision-level diffs, newest layer on top
│   ├── deferred.html         <- every provision a practicum change touches
│   ├── pathways.html         <- route to each permit by starting license
│   ├── eligibility.html      <- which licenses map to which permit
│   ├── hours.html            <- hour requirements by role, cost, and the record
│   ├── specialization.html   <- the specialized-domain overlay. Not in the rule
│   ├── cs-number.html        <- the controlled-substance number access point
│   ├── about.html            <- method, sources, corrections
│   ├── input.html            <- community input form
│   └── documents/            <- source PDFs, linked from the site
├── amendments/               <- draft amendment language, and its own audit harness
├── analytics/                <- the visit-counter Worker. The only wrangler config in the repo
├── Document Register/        <- original source PDFs and the Medical Psilocybin Act
├── source-text/              <- plain-text extractions, searchable
├── analysis/                 <- extractions, deltas, research. Public
├── tools/                    <- sync-nav.py, sync-provenance.py, sync-count.py. All take --check
├── CLAUDE.md                 <- standing facts (read first)
├── WRITING-STANDARD.md       <- how everything here is written
├── UPDATING.md               <- what to change when something happens
└── README.md
```

## Sources

- **The rule and the drafts:** `docs/documents/`. The July 23 published proposed rule is current. The June 12 recommendation, June 25 draft and July 9 draft are superseded.
- **Transcripts:** `docs/documents/` as PDFs and `source-text/` as searchable text. The July 9 transcript carries speaker labels. **Both July 17 transcripts do not.** A speaker is named from an unlabelled transcript only where the surrounding text fixes it, and the basis is stated.
- **Upstream:** meeting notes and transcripts originate in Notion and are copied into this repository. `docs/documents.html` lists what the repository does not yet hold, and `UPDATING.md` Part 6 tracks the same gaps for editors.
- **Names corrected from garbled auto-transcripts:** Zurlo, Leeman, Peskuski, Dezbaá, Fatemi, Wilson, Caldwell, Burgard, Dunn, Ryan, Truckner.

This site is built from public meeting records with AI assistance; the transcripts it relies on are unofficial and may contain errors. See `docs/about.html` for the method and the corrections path.

**This repository is public.** Everything committed here is published, including commit messages and everything in `analysis/`.

Nothing in this repository is final, promulgated rule text.

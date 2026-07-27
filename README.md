# NMMPAB Rules Draft Analysis: Training and Education

A neutral, plain-language community reference for the New Mexico Medical Psilocybin Advisory Board's **Training and Education** rulemaking.

Goal: let anyone, including people who do not follow the legislative process, see what is being decided, what is at stake, what the options are, and what happened at each meeting. No advocacy. Verbatim draft language and attributed input only.

**Live site:** https://rules.medical-psilocybin.org (GitHub Pages serves the `docs/` folder from `main`; the address is set by `docs/CNAME`). The visit counter answers separately on `count.medical-psilocybin.org` and is described in `analytics/README.md`.

## Read these first

- **[CLAUDE.md](CLAUDE.md)** holds the standing facts: the timeline and the reasoning behind each date, the two workstreams, the corrected transcript spellings, and the constraints.
- **[WRITING-STANDARD.md](WRITING-STANDARD.md)** sets the register for everything written here, including commit messages and pull request bodies.
- **[UPDATING.md](UPDATING.md)** is the propagation map: something happens in the rulemaking, and it says where that lands on the site. Part 2 is the fact index, which is the blast radius of any change.

## The two workstreams

They are separate and they have different clocks.

1. **The draft recommendation.** Drafting work for the Training and Education Committee, built against the published rule. Lives in `amendments/` and `amendments-remainder/`, each with its own audit harness. Deadline-driven.
2. **The site.** `docs/`, served from `main`. Six primary pages, the retained record pages, and redirect stubs at retired addresses. No external deadline.

## Where things stand

The operative document is the department's **proposed rule 7.35.3 NMAC, published July 23, 2026**, 19 pages, sections 7.35.3.1 through .28. It goes to a rule hearing on **August 28, 2026**.

Earlier documents are history and are cited only where a page compares versions: the June 12 committee recommendation, the June 25 department draft, and the July 9 board-meeting draft.

For what changed and when, see `docs/record.html` and `docs/changes.html`. For why the dates are what they are, see [CLAUDE.md](CLAUDE.md).

## What's here

```
NMMPAB_Rules-Draft-Analysis/
├── docs/                     <- the site, published by GitHub Pages from main
│   ├── index.html            <- the overview: where the rulemaking stands, portals by role
│   ├── rule.html             <- the published text, all 28 sections, verbatim and annotated
│   ├── recommendation.html   <- the committee recommendation beside the published text
│   ├── hours.html            <- the working model of the three deferred quantities
│   ├── record.html           <- the dated chain of meetings and documents, and the register
│   ├── comment.html          <- the hearing facts and the community input form
│   ├── about.html            <- method, sources, corrections
│   ├── changes.html          <- provision-level diffs, retained record page
│   ├── eligibility.html      <- which licenses map to which permit, retained record page
│   ├── cs-number.html        <- the controlled-substance number access point, retained
│   ├── training-hours-record.html <- the pre-redesign hours page, retained
│   └── documents/            <- source PDFs, linked from the site
├── amendments/               <- drafting for the practicum sections, with its own audit harness
├── amendments-remainder/     <- drafting for the sections outside the practicum, with its own audit harness
├── analytics/                <- the visit-counter Worker. The only wrangler config in the repo
├── redesign/                 <- the working folder behind the redesign: brief, prototypes, audits
├── Document Register/        <- original source PDFs and the Medical Psilocybin Act
├── source-text/              <- plain-text extractions, searchable
├── analysis/                 <- extractions, deltas, research. Public
├── tools/                    <- build-rule-page.py and check-site.py for the site; sync-nav.py, sync-provenance.py, sync-count.py
├── CLAUDE.md                 <- standing facts (read first)
├── WRITING-STANDARD.md       <- how everything here is written
├── UPDATING.md               <- what to change when something happens
└── README.md
```

## Sources

- **The rule and the drafts:** `docs/documents/`. The July 23 published proposed rule is current. The June 12 recommendation, June 25 draft and July 9 draft are superseded.
- **Transcripts:** `docs/documents/` as PDFs and `source-text/` as searchable text. The July 9 transcript carries speaker labels. **Both July 17 transcripts do not.** A speaker is named from an unlabelled transcript only where the surrounding text fixes it, and the basis is stated.
- **Upstream:** meeting notes and transcripts originate in Notion and are copied into this repository. `docs/record.html` lists the documents the repository holds, and `UPDATING.md` Part 6 tracks the gaps for editors.
- **Names corrected from garbled auto-transcripts:** Zurlo, Leeman, Peskuski, Dezbaá, Fatemi, Wilson, Caldwell, Burgard, Dunn, Ryan, Truckner.

This site is built from public meeting records with AI assistance; the transcripts it relies on are unofficial and may contain errors. See `docs/about.html` for the method and the corrections path.

**This repository is public.** Everything committed here is published, including commit messages and everything in `analysis/`.

Nothing in this repository is final, promulgated rule text.

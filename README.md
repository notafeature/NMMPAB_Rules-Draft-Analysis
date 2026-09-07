# NMMPAB Rules Draft Analysis: Training and Education

A neutral, plain-language community reference for the New Mexico Medical Psilocybin Advisory Board's **Training and Education** rulemaking.

Goal: let anyone, including people who do not follow the legislative process, see what is being decided, what is at stake, what the options are, and what happened at each meeting. No advocacy. Verbatim draft language and attributed input only.

**Live site:** https://rules.medical-psilocybin.org (GitHub Pages serves the `docs/` folder from `main`; the address is set by `docs/CNAME`). The visit counter answers separately on `count.medical-psilocybin.org` and is described in `analytics/README.md`.

## Read these first

- **[CLAUDE.md](CLAUDE.md)** holds the standing facts: the timeline and the reasoning behind each date, the two workstreams, the corrected transcript spellings, and the constraints.
- **[WRITING-STANDARD.md](WRITING-STANDARD.md)** sets the register for everything written here, including commit messages and pull request bodies.
- **[UPDATING.md](UPDATING.md)** is the propagation map: something happens in the rulemaking, and it says where that lands on the site. Part 2 is the fact index, which is the blast radius of any change.
- **[ARCHITECTURE.md](ARCHITECTURE.md)** holds the hosts, the projects, the parts and their paths, and the decisions of September 7, 2026 with their state: built, decided, or open.
- **[OPERATIONS.md](OPERATIONS.md)** holds the infrastructure as it stands and the runbooks: DNS, hosting, the counter, credentials, and what must never be done.

## The two workstreams

They are separate and they have different clocks.

1. **The draft recommendation.** Drafting work for the Training and Education Committee, built against the published rule. Lives in `amendments/` and `amendments-remainder/`, each with its own audit harness. Deadline-driven.
2. **The site.** `docs/`, served from `main`. Six primary pages, the retained record pages, and redirect stubs at retired addresses. No external deadline.

## Where things stand

The operative document is the department's **revised proposed rule 7.35.3 NMAC, published August 25, 2026**, 20 pages, sections 7.35.3.1 through .28, published with proposed amendments to 7.35.2.7, .10, and .24 NMAC and the notice fixing the rule hearing for **October 2, 2026**. The adopted rule 7.35.2 NMAC, Producer and Laboratory Requirements, has been in effect since June 23, 2026. The full statement of the current state, and why the dates are what they are, is in [CLAUDE.md](CLAUDE.md).

Earlier documents are history and are cited only where a page compares versions: the June 12 committee recommendation, the June 25 department draft, the July 9 board-meeting draft, and the set-aside July 23 publication.

For what changed and when, see `docs/7.35.3/record.html` and `docs/7.35.3/changes.html`. For why the dates are what they are, see [CLAUDE.md](CLAUDE.md).

## What's here

```
NMMPAB_Rules-Draft-Analysis/
├── docs/                     <- the site, published by GitHub Pages from main
│   ├── index.html            <- the parts index: every Part of 7.35 NMAC and where it stands
│   ├── 7.35.3/               <- the Training and Education pages, listed below
│   ├── *.html                <- a redirect stub at every retired root address
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
├── Document Register/        <- original source PDFs and the Medical Psilocybin Act
├── source-text/              <- plain-text extractions, searchable
├── analysis/                 <- extractions, deltas, research. Public
├── tools/                    <- the site tools; partlib.py says which Part a tool works on (--part)
├── CLAUDE.md                 <- standing rules and facts (read first)
├── WRITING-STANDARD.md       <- how everything here is written
├── UPDATING.md               <- what to change when the rulemaking moves
├── ARCHITECTURE.md           <- hosts, parts, paths, and the state of each decision
├── OPERATIONS.md             <- infrastructure inventory and runbooks
└── README.md
```

The layout above is the one in place today. The multi-part layout that replaces it, with one path per Part of 7.35 NMAC, is set out in `ARCHITECTURE.md`, Part 4.

## Sources

- **The rule and the drafts:** `docs/documents/`. The August 25 revised proposed rule is current. The June 12 recommendation, the June 25 draft, the July 9 draft, and the set-aside July 23 publication are superseded.
- **Transcripts:** `docs/documents/` as PDFs and `source-text/` as searchable text. The July 9 transcript carries speaker labels. **Both July 17 transcripts do not.** A speaker is named from an unlabelled transcript only where the surrounding text fixes it, and the basis is stated.
- **Upstream:** meeting recordings and transcripts are obtained from the public record and copied into this repository. `docs/7.35.3/record.html` lists the documents the repository holds, and `UPDATING.md` Part 6 tracks the gaps for editors. Private working notes are never cited.
- **Names corrected from garbled auto-transcripts:** Zurlo, Leeman, Peskuski, Dezbaá, Fatemi, Wilson, Caldwell, Burgard, Dunn, Ryan, Truckner.

This site is built from public meeting records with AI assistance; the transcripts it relies on are unofficial and may contain errors. See `docs/7.35.3/about.html` for the method and the corrections path.

**Everything committed here is treated as published,** including commit messages and everything in `analysis/`, whether the repository is public or private.

Nothing in this repository is final, promulgated rule text.

# Proposed amendments: training and education, 7.35.3 NMAC

Drafting folder for proposed amendments to the medical psilocybin rule published July 23, 2026, in advance of the rule hearing set for August 28, 2026.

**This folder is internal drafting work, not published rule text and not a filing.** Nothing here has been submitted to the Department of Health. Nothing in this repository is final, promulgated rule text.

## Scope

Training and education only.

| Provision | Why it is here |
|---|---|
| 7.35.3.18, educational requirements | in scope |
| 7.35.3.19, practicum requirements | in scope |
| 7.35.3.14, authorized possession | plumbing that 7.35.3.19 depends on |
| 7.35.3.20 (H)(5), staffing ratios | plumbing that 7.35.3.19 depends on |
| 7.35.3.20 M, designation of owners and employees | new. The only way to fix the dangling registration condition in 7.35.3.14 (C) |
| 7.35.3.29, practicum with non-patient participants | new. Recommendation 3 step 1, drafted contingent on statutory authority |

Addendum A of the PDF maps every provision the practicum depends on, in and out of scope. Addendum B lists the ten proposed new provisions and what breaks if each is dropped.

Everything else is flagged, not drafted. The flags are collected at `metz-crosswalk.md`, Part 7, and summarized in Addendum F of the PDF.

**This is not a review of Part 3.** Part 3 runs to 28 sections. `analysis/july23-rule-concerns.md` records 5 blocking and 23 material findings across the whole of it. This folder drafts fixes for the practicum and for the provisions the practicum cannot function without. Anything wider belongs in a separate document.

**Out of scope by decision:** the controlled-substance number requirement for certifying clinicians. No file in this folder proposes reopening it.

**Permit title:** the drafts keep "practitioner." They do not adopt "licensed provider." The term is defined in 7.35.2.7 NMAC, a different part of Title 7, which 7.35.3.7 NMAC incorporates by reference. The title is carried as a variable so the decision can be made later and applied in one pass.

## Files

| File | What it is |
|---|---|
| `7.35.3-practicum-amendments-v5.pdf` | **The deliverable.** Side-by-side redline plus three addenda |
| `content.py` | The amendment content. Published text and proposed text, provision by provision |
| `notes.py` | The Source line and the Please review note for each change |
| `build-redline-pdf.py` | Builds the PDF. Aborts unless every left-column block matches the published PDF by exact contiguous match |
| `*.md` | Superseded working drafting. Numbers in these files were not all traceable and have been removed from the current draft |

## The rule for numbers

No figure enters a proposed change unless it exists in a source.

- Where the July 17 recommendation gives a range, the low end is drafted and the range is shown in a badge next to it.
- Where the rule as published is unclear, the published text is left alone and a Please review note records what is unclear.
- Where a figure follows from arithmetic rather than from a recommendation, the Source line says so and shows the arithmetic.
- Gaps are reported, not filled.

## The hours

| | Published | Proposed | Change |
|---|---|---|---|
| Module total, either permit | 40 | 84 | +44 |
| Practicum, facilitator | 100 | 62 | -38 |
| Practicum, practitioner | 120 | 72 | -48 |
| Supervision or consultation | 10 | 20 | +10 |
| **Program total, facilitator** | **150** | **166** | **+16** |
| **Program total, practitioner** | **170** | **176** | **+6** |

The practitioner row assumes the 20 supervision hours in 7.35.3.19 C sit inside the published 120. On the other reading the published total is 190 and the proposed 176 is below it. Flagged in the PDF at 7.35.3.19 C, not resolved here.

## Conventions

These follow the repository rules in `HANDOFF.md`, section 2.

- No em dashes.
- Verbatim means verbatim. Anything inside quotation marks is reproduced exactly, with PDF line breaks collapsed to single spaces and no other alteration.
- Every claim is cited to a section and page of the published rule, to a source document with a page, or to a transcript.
- Both July 17 transcripts are labeled "UNOFFICIAL AUTO-GENERATED TRANSCRIPT. NO SPEAKER ATTRIBUTION." A speaker is named only where the surrounding transcript text fixes it, and the basis is stated.
- No characterization of anyone's motives.
- This repository is public. Everything committed here is published.

## Sources

- `docs/documents/rules-draft-2026-07-23-published.pdf`, the published proposed rule, 19 pages
- `docs/documents/rules-draft-2026-07-09.pdf`, the prior board-meeting draft, used for new versus carried-over determinations
- `docs/documents/metz-recommendations-2026-07-17.pdf`, `docs/documents/metz-onepager-2026-07-17.pdf`, and `docs/documents/metz-slides-2026-07-17.pptx`
- `source-text/NMMPAB-2026-07-17-board-transcript.txt` and `source-text/NMMPAB-2026-07-17-committee-transcript.txt`
- `analysis/july23-rule-concerns.md`, `analysis/july23-published-delta.md`, `analysis/july17-to-july23-state-diff.md`
- `Document Register/SB0219-Medical-Psilocybin-Act-2025.pdf`, Senate Bill 219, 57th Legislature, First Session, 2025, as introduced. The enacted text at Sections 26-2D-1 through -11 NMSA 1978 has not been checked against it
- `source-text/7.35.2-NMAC-adopted-2026-06-23.txt`, 7.35.2 NMAC as adopted effective June 23, 2026, retrieved July 25, 2026. This is the part that supplies every defined term used in Part 3

Nothing in `docs/` was modified by this work.

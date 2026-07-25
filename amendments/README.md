# Proposed amendments: training and education, 7.35.3 NMAC

Drafting folder for proposed amendments to the medical psilocybin rule published July 23, 2026, in advance of the rule hearing set for August 28, 2026.

**This folder is internal drafting work, not published rule text and not a filing.** Nothing here has been submitted to the Department of Health. Nothing in this repository is final, promulgated rule text.

**Out of scope by decision:** the controlled-substance number requirement for certifying clinicians.

**Permit title:** the draft keeps "practitioner." The term is defined in 7.35.2.7 NMAC, which 7.35.3.7 NMAC incorporates by reference. It is held as a variable in `build-redline-pdf.py` and can be changed in one pass.

## Files

| File | What it is |
|---|---|
| `7.35.3-practicum-amendments-v6.pdf` | The document. Side-by-side redline plus three addenda |
| `content.py` | Published text and proposed amendment, provision by provision |
| `notes.py` | Citation and review note for each change |
| `build-redline-pdf.py` | Builds the PDF. Aborts unless every left-column block matches the published rule by exact contiguous match |

## What the document is

An analysis of the recommendation of Dr. Anne Metz to the Training and Education Committee dated July 17, 2026, stated as amendment language against the proposed rule published July 23, 2026, for the committee's consideration.

It covers 7.35.3.19, practicum requirements, and the three provisions on which the practicum depends: 7.35.3.18, 7.35.3.14, and Paragraph (5) of Subsection H of 7.35.3.20. One new section, 7.35.3.29, is proposed. No other provision of Part 3 is addressed.

Where the Metz recommendation states a range, the low end is drafted and marked with a badge. Where the rule as published is unclear, the published text is left as it stands and the question is stated at that provision.

## Hours

| | Published | Proposed | Change |
|---|---|---|---|
| Module total, either permit | 40 | 84 | +44 |
| Practicum, facilitator | 100 | 62 | -38 |
| Practicum, practitioner | 120 | 72 | -48 |
| Supervision or consultation | 10 | 20 | +10 |
| **Program total, facilitator** | **150** | **166** | **+16** |
| **Program total, practitioner** | **170** | **176** | **+6** |

The practitioner rows take the 20 supervision hours in 7.35.3.19 C to be within the published 120. On the other reading of that subsection the published total is 190. Stated at 7.35.3.19 C.

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

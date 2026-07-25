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
| `7.35.3-practicum-amendments-v4.pdf` | **The deliverable.** Side-by-side redline of every subsection being amended, plus six addenda: A the practicum dependency map, B the proposed new provisions including one withdrawn, C the arithmetic behind the practitioner practicum figure, D definitions that need updating, E the permit title laid out for decision, F the remaining twenty-four sections. Version history on the last page. Built and verified by `build-redline-pdf.py` |
| `build-redline-pdf.py` | Builds the PDF. Aborts unless every left-column block matches the published PDF by exact contiguous match. Carries `VERSION` and `VERSION_HISTORY` |
| `metz-crosswalk.md` | The four July 17 recommendations mapped against the published rule provision by provision, with the hours ledger, the answer to the open question on the permit title, and the cross-session flags |
| `7.35.3.18-19-redline.md` | Redline amendment language for 7.35.3.18 and 7.35.3.19 |
| `blocking-defects.md` | The blocking defects with proposed textual fixes, and the amendment language for 7.35.3.14 and 7.35.3.20 (H)(5) |
| `*-rendered.md` | Generated copies with the permit title substituted. Do not edit these |

**Everything a reviewer needs is in the PDF.** The markdown files are the working drafting behind it. There is no separate questions file; open items and calls made are stated in the PDF, on the page where they arise.

Every proposed change in the PDF carries a Source line. Where it reads "Drafting", the change appears in no source and was written to make something else work. Those are the ones to argue with first.

To rebuild the PDF after editing the drafting:

```
python3 amendments/build-redline-pdf.py
```

**Versioning.** Every issued PDF carries a version in its filename and a version history on its last page. Bump `VERSION` in `build-redline-pdf.py` and add a `VERSION_HISTORY` row whenever the content changes, so that no two copies in circulation share a name. v1 and v2 were issued unversioned on July 25, 2026 and are described in the history for the record; v3 is the first versioned issue.

## The permit-title variable

The three source files never write the permit title literally. They use six tokens:

| Token | Current value |
|---|---|
| `{{PT}}` | practitioner |
| `{{PTS}}` | practitioners |
| `{{PT_C}}` | Practitioner |
| `{{PTS_C}}` | Practitioners |
| `{{PT_UC}}` | PRACTITIONER |
| `{{PTS_UC}}` | PRACTITIONERS |

To change the title, edit the six values in `tools/render-permit-title.py` and run:

```
python3 tools/render-permit-title.py
```

This rewrites the three `*-rendered.md` files. To check whether the rendered files are current without rewriting them:

```
python3 tools/render-permit-title.py --check
```

The variable reaches only the four provisions in scope. A change of permit title also requires an amendment to 7.35.2.7 NMAC and a conforming pass over the rest of 7.35.3 NMAC, neither of which this folder covers. Whether that change would reach the practicum or the hours is answered at `metz-crosswalk.md`, Part 1. The short answer is no.

## The position these drafts serve

Hours shift. They do not shrink.

| | Published July 23 | Proposed | Change |
|---|---|---|---|
| Didactic hours | 35, plus a module with no hour count | 79 | +44 |
| Simulated patient experience | 5 | 5 | 0 |
| **Module total, either permit** | **40, plus an unpriced module** | **84** | **+44** |
| Practicum, facilitator | 100 | 80 | -20 |
| Practicum, practitioner | 120, or 140 on the second reading of 7.35.3.19 C | 90 | -30 |
| Supervision or consultation | 10 | 20 | +10 |
| **Program total, facilitator** | **150** | **184** | **+34** |
| **Program total, practitioner** | **170, or 190** | **194** | **+24** |

The 84-hour standard is inclusive of the 5-hour simulated patient experience, confirmed by the author of the July 17 recommendation. 7.35.3.18 H states it as a module total with a didactic floor of 79 inside it.

Total program hours rise for both permit types. Every patient and session minimum in the published practicum is carried forward unchanged. The argument rests on the published text, the July 17 record, and this arithmetic. It does not rest on comparison with Oregon or Colorado.

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

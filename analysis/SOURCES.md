# SOURCES — where to read the actual meetings, transcripts, and drafts

**Read this before writing anything. The job is to read the primary transcripts, not to summarize from memory.** Prior timeline/process synthesis was wrong; reconstruct the sequence verbatim from the transcripts below.

## How to read a transcript (Notion MCP)

The workspace has a Notion MCP connector. Each meeting exists as TWO objects:
- a **calendar container page** (the row in the Committee Meetings Calendar), and
- an **embedded meeting note** with its own ID, where the **actual spoken transcript** lives.

To get the transcript, call `notion-fetch` on the **note ID** with **`include_transcript: true`**. Fetching the container page alone may not return the full transcript.

Tool: `mcp__494024d9-f21b-48fc-9c26-58eccde35cf0__notion-fetch` (load via ToolSearch if deferred).

---

## The two meetings that matter most for the July 9 items

### June 25, 2026 — rules-draft hearing ("Draft Regulations Review")
- Container page: `de38d5ffbeba444d8c29d0ccb02ca4ad` — https://app.notion.com/p/de38d5ffbeba444d8c29d0ccb02ca4ad
- **Transcript note: `38aa2b7222dc80ec89cadaeed14ce519`** (fetch with include_transcript=true)
- Content: public review of the 6/25 rules draft; CS-number objection, 20-hr supervisory practicum, reciprocity 40-hr clarification, third-party evaluator, test-out, inspections.

### June 26, 2026 — Advisory Board meeting (the 3-2 vote)
- Container page: `9c05a6c8a0ea47068a138ac4776121f4` — https://app.notion.com/p/9c05a6c8a0ea47068a138ac4776121f4
- **Transcript note: `38ba2b7222dc80969c1ec6bb62a88fe5`** (fetch with include_transcript=true)
- Content: the motion, the 3-2 vote, all three tabled items debated, next-steps discussion. **The real process/sequence for what happens after July 9 is discussed here — read it directly.**

---

## All Training & Education meetings (chronological)

| Date | Meeting | Container page ID | Transcript note ID (if separate) |
|---|---|---|---|
| Jan 23 | T&E Committee mtg 1 | `2eea2b7222dc8077af51f6ca2395d8b6` | (working doc; no AI transcript) |
| Mar 6 | T&E Committee mtg 2 | `2f2a2b7222dc808e9f69c90e339d5fed` | (manual notes; no transcript) |
| Apr 10 | T&E Sub-Committee | `f92649a34abe410cbe482705562ff3c0` | (has AI summary) |
| May 8 | Joint T&E + End-of-Life | `9ee80614359f476a9a65cae9a6910cbf` | (has AI summary) + chat page `35aa2b7222dc8048a60ccd7c78654c50` |
| May 22 | Training & Education | `3d78c7ca27f945cc9359e00f1ef9f53b` | **EMPTY — held, not recorded, not published by DOH. No transcript exists.** |
| Jun 12 | T&E Committee | `c7ac6daf36844a8ab322cf31217f61c3` | note `37da2b7222dc80e1a8f1d1e27bdbeedf`; "Draft of Todays Recommendation" `37da2b7222dc80efb9ece7c327770b5a` |
| Jun 25 | Rules-draft hearing | `de38d5ffbeba444d8c29d0ccb02ca4ad` | **`38aa2b7222dc80ec89cadaeed14ce519`** |
| Jun 26 | Board — the vote | `9c05a6c8a0ea47068a138ac4776121f4` | **`38ba2b7222dc80969c1ec6bb62a88fe5`** |
| Jul 9 | Board (tabled items) | `b5cfdae09a1a40bdba19220a9ba59845` | (upcoming; empty) |
| Jul 17 | Board + T&E committee | `72ad3b3b50d54a209b1beba9fb247055` | (upcoming; empty) |

## Analysis / hub pages in Notion (secondary, built by us — verify against transcripts)

- Training & Education Committee hub: `2eea2b7222dc80388519c76971744a99`
- Advisory Board Sub Committee Overview: `2dca2b7222dc80629ca6cb4cb06ac65b`
- Committee Meetings Calendar (database): `2dca2b7222dc80a998fde89d78b04a8c` · data source `collection://2dca2b72-22dc-80b1-ba75-000ba131e4eb` (authoritative meeting list)
- 7.35.X Provider Training Rules — Draft Analysis: `38ea2b7222dc81b9bfbde900931d62dd`
- Redline / Vote Record (has BOTH source PDFs attached + the build spec): `5a89214943dd48b2a4e081c9755f7211`
- Tabled-item pages: CS number `38ea2b7222dc815e809cc54c37179e29` · Practicum `38ea2b7222dc81bd9048fa6afa4a192d` · Reciprocity `38ea2b7222dc81f3b158fe197da7a5a4`
- Adopted-but-unresolved (7): eligibility-clinician rename `38ea2b7222dc81e2bbe8f706de14e5e2` · facilitator 101 vs peer `38ea2b7222dc81d780effe507746693d` · mentoring `38ea2b7222dc8155b340f62f952827c6` · background-check `38ea2b7222dc813384a0dea33745b4ad` · healthy volunteers `38ea2b7222dc81d6aefcfe0df97aca0e` · condition-specific endorsements `38ea2b7222dc8181aa0ad40ff7cd9762` · wilderness first aid `38ea2b7222dc8165a7faeec7e228b95c`

## DOH public site (authoritative for what is officially posted)

- Main MPAB page: https://www.nmhealth.org/about/mcpp/mpp/mpab/
- Meeting Records: https://www.nmhealth.org/about/mcpp/mpp/mpab/mr/
- Resources (recordings): https://www.nmhealth.org/about/mcpp/mpp/mpab/resources/
- T&E recordings posted: Jan 23 `/resource/view/2835/` · Mar 6 `/resource/view/2914/` · Apr 10 `/resource/view/2949/` · May 8 `/resource/view/2955/` (prefix with `https://www.nmhealth.org`)
- June meetings and May 22 were NOT posted by DOH as of 7/8/2026.

## Local source files

- `Document Register/Draft for Training Requirements 6-12-26.pdf` (recommendation draft, 9 pp)
- `Document Register/Draft for Training and Education Committee for 6-25-26 (1).pdf` (rules draft, 11 pp)
- `source-text/raw-pdf-extraction.txt` — verbatim text of both PDFs (pypdf)
- `analysis/6-25-hearing-extraction.md`, `analysis/6-26-board-extraction.md` — attributed quotes (OLD name spellings; correct on use: Zurlo, Peskuski, Fatemi, Leeman)

## What still needs a verbatim read (do not synthesize)

- **The rulemaking sequence / what happens after July 9.** Reconstruct from the 6/26 transcript (and 6/25) directly, with attributed quotes and dates. The prior "timeline" on the site was removed because it was synthesized, not sourced.

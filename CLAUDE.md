# Standing rules and standing facts

Read this before any work, in every session. It holds the rules for how work is done here and the facts that do not change between sessions. These rules outrank habit, and they outrank whatever a model believes a website should look like.

## Read these before writing anything

| File | For |
|---|---|
| `WRITING-STANDARD.md` | How everything here is written. It applies to commit messages and pull request bodies as well as to the site |
| `UPDATING.md` | What to change when a meeting happens or a document is published. The fact index in Part 2 is the blast radius of any change. It was written for the pre-redesign site; re-pointing it at the current pages is open work |

## The two workstreams

They are separate. Do not let one drift into the other.

**1. The draft recommendation.** Drafting work for the Training and Education Committee, built against the published rule. Lives in `amendments/` and `amendments-remainder/`, each with its own audit harness. Deadline-driven.

**2. The site.** `docs/`, served from `main` by GitHub Pages at https://rules.medical-psilocybin.org. The address is set by `docs/CNAME`; deleting or overwriting that file takes the domain down. Six primary pages, the working model of the hours, the retained record pages, and redirect stubs at retired addresses. A reference for people following the rulemaking. No external deadline.

## What the site must do

Every page, name, layout, tool, and sentence is tested against these six functions. Anything that serves none of them is removed.

1. Tell a visitor where the rulemaking stands the moment they arrive, and be right every time.
2. Tell a person what the current draft, as written, would require of them in their own situation.
3. Show what is still open and what is proposed to change, beside the text it would change, and show what the change would mean for a person's life.
4. Back every statement with its source, one step away: citations open on hover, close on leave, and open the source in a new tab on click.
5. Stay current with less effort than it takes to go stale.
6. Remain, when the rulemaking ends, as the complete account of how the rule was made.

## Conduct in a session

- Never use blocking question dialogs. Write questions out fully, in prose, so they can be answered at any time.
- Fewer words. Lead with the point. A long message must earn every sentence.
- Before building anything substantial, state in two or three sentences what is about to be built and why. Let the owner correct the sentences, not the artifact.
- One thing at a time. Do not deliver a pile.
- When shown a reference, extract the philosophy behind it. Never copy it, and never let one reference take over the design.
- When corrected the same way twice, stop and restate the principle before trying again.

## Writing

`WRITING-STANDARD.md` holds the full standard. These rules come up most, and they apply to the site, this repository, commit messages, and conversation alike.

- Complete sentences a person would speak. No fragments, no headline rhythm, no punch lines written for effect.
- State what things are. A negative construction is used only when the negative fact itself is the point.
- No urgency or countdown language. Dates carry urgency by themselves.
- Clinical and emotionless. Facts, dates, attributions. A community position is stated as a fact about what is proposed.
- Every element introduces itself. No insider shorthand, no first names standing alone, no term used before its meaning.
- No em dashes anywhere.
- Process vocabulary is exact: the proposed rule or published text; a recommendation; public comment; the rule hearing; the adopted rule, published in the New Mexico Register as a Part of the NMAC. The word "docket" does not belong to this process. Nothing here is an "amendment," because nothing here changes an adopted rule. The folders `amendments/` and `amendments-remainder/` keep their historical names; new prose does not adopt the word.

## Design

- The site is an instrument, not a publication. Nothing on it may be shaped like a blog: no feed of posts, no stacked cards of prose, no page that is only a scroll of headed text.
- Light mode. Color belongs to meaning alone: state, category, encoding on a chart. Decoration gets no color.
- Typography does the structure: one quiet display voice, monospace for data, dates, and wayfinding. Space instead of boxes.
- Robust over fancy. Everything must render correctly everywhere, degrade cleanly without JavaScript, and survive a slow connection.
- Interactivity exists so a reader can interrogate the model: touch a quantity, see what changes for a person. It never exists for engagement.

## The timeline, and why the dates are what they are

| Date | Day | What |
|---|---|---|
| July 17, 2026 | Friday | Board meeting, morning; Training and Education Committee, afternoon. Practicum and didactic hours deferred to the committee. Definitions also deferred to the committee, with the instruction to get language back to the department "sooner than later." No publication date was given |
| July 23, 2026 | Thursday | The department published the proposed rule and scheduled the hearing |
| July 27, 2026 | Monday | The committee's recommendation reached the department as a summary of the recommended rules, one day ahead of the working date below |
| July 28, 2026 | Tuesday | One month before the hearing. The working date for the recommendation to be in the department's hands |
| August 14, 2026 | Friday | Advisory Board meeting. By this meeting the July 23 publication and its August 28 hearing had been set aside, spoken of on the record as an accomplished fact; no notice of the set-aside is held. Record: `analysis/8-14-board-extraction.md` |
| August 21, 2026 | Friday | Training and Education Committee meeting. Both education and training proposals, the subcommittee's and the department's, were shown side by side; no vote was taken; the department restated the schedule below. Record: `analysis/8-21-committee-extraction.md` |
| August 25, 2026 | Tuesday | The department's stated date for publishing revised proposed rules, stated August 14 and August 21 |
| September 4, 2026 | Friday | Training and Education Committee meeting, 9 to 11 AM, scheduled at the close of August 21 |
| October 2, 2026 | Friday | Rule hearing, anticipated. Stated by the department on August 21; the final notice, in preparation with the hearing officer, will fix the date. First set for August 28 with the July 23 publication |

**The hearing date moved with the set-aside.** The hearing was set for August 28 when the rule was published on July 23. The publication and hearing were then set aside, on the record by August 14; the department placed the hearing at the end of September or early October on August 14 and named October 2, virtual and in person, on August 21. The October date is an anticipation until the final notice issues; report it as the department's stated anticipation, not as noticed. The department's reason for the set-aside is not asserted anywhere on the site; the site reports the set-aside as fact and attributes the schedule statements.

**No hearing notice document is held in this repository.** The October 2 date is sourced to the department's statement at the August 21 meeting, not to a filing. That gap is tracked in `UPDATING.md`, Part 6. Do not report the date as unverified; report the notice as absent.

## Named people

Zurlo, Leeman, Peskuski, Dezbaá, Fatemi, Wilson, Caldwell, Burgard, Dunn, Ryan, Truckner. These are the corrected spellings for auto-generated transcripts.

The July 9 transcript carries speaker labels. **Both July 17 transcripts do not.** Name a speaker from an unlabelled transcript only where the surrounding text fixes it, and state the basis.

## Constraints

- **Never name who compiles the information or who reviews it,** in any committed file. Not in page text, not in a commit message, not in a pull request body. Meeting participants are named as participants; that is different.
- **This repository is public.** Everything committed is published, including commit messages and everything in `analysis/`. There is no internal directory.
- **The summary of the recommended rules, submitted July 27, 2026, is not committed to this repository and is not downloadable from the site.** Every page cites it by name and states its figures; the document itself stays out until the department places it in the public record.
- **Verbatim means verbatim.** Quoted text is never altered, and every claim carries its source.
- **Do not push to `main`.** Branch, commit, open a pull request.
- **Nothing here is final, promulgated rule text.**
- **A date the department states is never carried as a scheduled item.** Stated dates in this rulemaking have been set and overridden. The site reports a stated date only inside the record of the meeting that stated it, in the past tense and attributed. The status surfaces list a forward date only when a notice fixes it, or when a public body scheduled its own meeting on the record.
- **The recommendation stands alone.** There is one recommendation, the committee's, at its current position. It is not diffed against anything until a proposed rule is published; comparisons then run against that published text. Materials another party shows at a meeting, such as the department's August 21 side-by-side, are meeting record and live on the record pages, never as a standing position on the content pages.

## Where things are

| Path | What |
|---|---|
| `docs/` | The site. Served from `main` |
| `docs/documents/` | Source PDFs, linked from the site |
| `source-text/` | Plain-text extractions, searchable |
| `analysis/` | Extractions, deltas, research. Public |
| `amendments/` | Drafting for the practicum sections, with its own audit harness. Branch work |
| `amendments-remainder/` | Drafting for the sections outside the practicum, with its own audit harness |
| `analytics/` | The visit-counter Worker. The only wrangler config in the repo |
| `redesign/` | The working folder behind the redesign: brief, prototypes, audits |
| `tools/` | `build-rule-page.py` and `check-site.py` for the site; `sync-nav.py`, `sync-provenance.py`, and `sync-count.py`, which take `--check` and still target the pre-redesign pages |
| `tools/sync-pathways.py` | The content of `docs/pathways.html`: every starting license, every route, and every step. The page is generated from it, so a step, a verdict, or a citation is changed here and the tool is run. Hand-editing the page fails `check-site.py` |
| `tools/sync-status.py` | The status of the rulemaking: the dated events, each status item's state, date, and summary, and the procession. The status surfaces on `index.html`, `hours.html`, `eligibility.html`, and `training-hours-record.html` are generated from it, so a status change is made here and the tool is run. Hand-editing a status surface fails `check-site.py` |

## Current state of truth

No proposed rule is currently published. The July 23 publication and its August 28 hearing were set aside; the set-aside was an accomplished fact on the record by the August 14 board meeting, and no notice of it is held in this repository. `docs/documents/rules-draft-2026-07-23-published.pdf` is the **last published text**, 19 pages, sections 7.35.3.1 through .28: the site cites it for section numbers and rule text until revised rules publish, and frames it as set aside, never as operative.

The committee's recommendation stands at its **August 21 position**: 80 didactic hours with minimums in nine content areas, a staged practicum of 114 hours for licensed providers or 102 for facilitators closing in case presentation and consultation, stated in full on `docs/recommendation.html` and recorded in `analysis/8-21-committee-extraction.md`. It is in the department's hands for the revised rules.

Earlier documents are history. Cite them only where a page is comparing versions.

The chain is defined in one place, `tools/sync-provenance.py`. When a document supersedes the current one, edit that file first, and regenerate the rule page with `tools/build-rule-page.py` from the new extraction.

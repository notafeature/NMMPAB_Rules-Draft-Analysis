# Standing rules and standing facts

Read this before any work, in every session. It holds the rules for how work is done here and the facts that do not change between sessions. These rules outrank habit, and they outrank whatever a model believes a website should look like.

## Read these before writing anything

| File | For |
|---|---|
| `WRITING-STANDARD.md` | How everything here is written. It applies to commit messages and pull request bodies as well as to the site |
| `UPDATING.md` | What to change when a meeting happens or a document is published. The fact index in Part 2 is the blast radius of any change. It was written for the pre-redesign site; re-pointing it at the current pages is open work |
| `ARCHITECTURE.md` | The hosts, the projects, the parts, the paths, and what was decided on September 7, 2026 and not yet built. Read before adding a page, a part, or a host |
| `OPERATIONS.md` | The infrastructure as it stands (DNS, hosting, the counter, credentials) and the runbooks. Read before touching anything outside the content of `docs/` |

## The two workstreams

They are separate. Do not let one drift into the other.

**1. The draft recommendation.** Drafting work for the Training and Education Committee, built against the published rule. Lives in `amendments/` and `amendments-remainder/`, each with its own audit harness. Deadline-driven.

**2. The site.** `docs/`, served from `main` by GitHub Pages at https://rules.medical-psilocybin.org. The address is set by `docs/CNAME`; deleting or overwriting that file takes the domain down. Six primary pages, the working model of the hours, the retained record pages, and redirect stubs at retired addresses. A reference for people following the rulemaking. No external deadline. The site covers one Part of the NMAC today, 7.35.3, and is being reshaped to carry every Part as a path under the same host (`ARCHITECTURE.md`, Part 2).

## When something changes

`UPDATING.md` maps a change in the rulemaking to the pages and tools it touches. This table maps a change to the site's shape or its infrastructure. Every row names the file that holds the procedure; none of it is done from memory.

| Trigger | Touch | Procedure |
|---|---|---|
| A page is added or retired | `tools/sync-nav.py` (`NAMES`, `GROUPS`), then every sync tool, then `check-site.py` | `OPERATIONS.md` 3.1, 3.2 |
| A document lands | `docs/documents/`, `source-text/`, `tools/sync-record.py`, `tools/sync-nav.py` | `UPDATING.md` Events A and C |
| A Part is added | `docs/7.35.N/`, `parts/7.35.N/`, the rule page tool, the parts index, the statute crosswalk | `OPERATIONS.md` 3.4 |
| A host is added | its own repository and deploy config; `ALLOWED_ORIGINS` in `analytics/wrangler.toml` and a counter redeploy; the hub | `OPERATIONS.md` 4.1 |
| A host name changes or moves | `docs/CNAME`, the Pages setting, DNS, `ALLOWED_ORIGINS`, `ENDPOINT` in `tools/sync-count.py`, the apex redirect rule, `analytics/setup.sh`, absolute links on other hosts | `OPERATIONS.md` 4.2 |
| The hub is built at the apex | the placeholder A records, the redirect rule, the counter origins | `OPERATIONS.md` 4.3 |
| The repository goes private | the site moves to Cloudflare first, then the flip | `OPERATIONS.md` 4.4, 4.5 |
| The counter shows nothing, or the counter host serves the website | the Worker's bindings; a root wrangler config | `OPERATIONS.md` Part 6 and Part 5 |
| A standing fact in this file, `ARCHITECTURE.md`, or `OPERATIONS.md` is no longer true | that file, in the same pull request as the change that made it untrue | |

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
- Process vocabulary is exact: the proposed rule or published text; a recommendation; public comment; the rule hearing; the adopted rule, published in the New Mexico Register as a Part of the NMAC. The word "docket" does not belong to this process. The word "amendment" belongs to exactly one document: the proposed amendments to 7.35.2 NMAC published August 25, 2026, which genuinely amend an adopted rule. Nothing in the 7.35.3 rulemaking is an "amendment." The folders `amendments/` and `amendments-remainder/` keep their historical names; new prose does not adopt the word for their contents.
- **The statute is cited by its compiled section.** The statute is NMSA 1978, Sections 26-2D-1 through 26-2D-11, Article 2D of Chapter 26, enacted as Laws 2025, Chapter 73, effective June 20, 2025. Its short title, set by 26-2D-1, is the Medical Psilocybin Act, and that name is used in prose. The citation form is "Section 26-2D-7 NMSA 1978", never "SB 219, Section 7". The bill number is cited only for legislative history and for the bill's Sections 12 through 14, which amended other chapters. Existing bill-form citations are converted as pages are touched; the sweep is step 4 of the order of work in `ARCHITECTURE.md`.
- **Role vocabulary.** In the site's own voice the roles are the published text's names: the **certifying clinician**, the **practitioner**, and the **facilitator**. The August 25 text kept both contested names and defined them in the amended 7.35.2.7; the recommendation's proposed renames, **medical screener** for the screening role and **Licensed Provider** for the middle role, were not adopted and appear nowhere in the published texts. The proposed renames are stated where the recommendation itself is described, attributed to it. Verbatim quotes and printed section titles keep each document's own words. The earlier pair convention, certifying clinician / medical screener, is retired.

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
| August 25, 2026 | Tuesday | The department published the revised proposed rule for 7.35.3 NMAC, proposed amendments to 7.35.2.7, .10, and .24 NMAC, and the notice fixing the October 2 rule hearing. The date had been stated August 14 and August 21 |
| September 4, 2026 | Friday | Training and Education Committee meeting, 9 to 11 AM, scheduled at the close of August 21 |
| October 2, 2026 | Friday | Rule hearing, 9:00 AM, Harold Runnels Building auditorium, Santa Fe, and by video conference and telephone. Fixed by the notice published August 25. Written comment is due by the close of the hearing. First set for August 28 with the July 23 publication |

**The hearing date moved with the set-aside, and is now fixed by notice.** The hearing was set for August 28 when the rule was published on July 23. The publication and hearing were then set aside, on the record by August 14; the department placed the hearing at the end of September or early October on August 14, named October 2 on August 21, and fixed it by the notice published August 25. The department's reason for the set-aside is not asserted anywhere on the site; the site reports the set-aside as fact and attributes the schedule statements.

**The hearing notice is held**: `docs/documents/hearing-notice-2026-08-25.pdf`, 2 pages, covering the adoption of 7.35.3 NMAC and the amendments to 7.35.2.7, 7.35.2.10, and 7.35.2.24 in one hearing. The former gap over the missing notice is closed.

## Named people

Zurlo, Leeman, Peskuski, Dezbaá, Fatemi, Wilson, Caldwell, Burgard, Dunn, Ryan, Truckner. These are the corrected spellings for auto-generated transcripts.

The July 9 transcript carries speaker labels. **Both July 17 transcripts do not.** Name a speaker from an unlabelled transcript only where the surrounding text fixes it, and state the basis.

## Constraints

- **Never name who compiles the information or who reviews it,** in any committed file. Not in page text, not in a commit message, not in a pull request body. Meeting participants are named as participants; that is different.
- **This repository is public today and may become private later.** Neither state changes what may be committed: everything committed is treated as published, including commit messages and everything in `analysis/`. There is no internal directory. Making the repository private is a hosting change first (`OPERATIONS.md` 4.4 and 4.5).
- **No private workspace is referenced in any committed file.** No link to, identifier of, or page name from a private notes workspace appears in the repository or on the site. Such material is research; it informs the site and is never cited by it. Where a file was copied from one, the public document it stands for replaces it. Existing references are removed in the layout move (`ARCHITECTURE.md`, order of work, step 2).
- **Every statement on the site rests on a publicly obtainable document,** held in `docs/documents/` and listed in the register. A claim with no such document is stated as unsourced, per `WRITING-STANDARD.md` Part 1, or not stated.
- **The summary of the recommended rules, submitted July 27, 2026, is not committed to this repository and is not downloadable from the site.** Every page cites it by name and states its figures; the document itself stays out until the department places it in the public record.
- **Verbatim means verbatim.** Quoted text is never altered, and every claim carries its source.
- **Do not push to `main`.** Branch, commit, open a pull request.
- **Nothing here is final, promulgated rule text.**
- **A date the department states is never carried as a scheduled item.** Stated dates in this rulemaking have been set and overridden. The site reports a stated date only inside the record of the meeting that stated it, in the past tense and attributed. The status surfaces list a forward date only when a notice fixes it, as the August 25 notice fixes October 2, or when a public body scheduled its own meeting on the record.
- **One recommendation, compared against the published text.** There is one recommendation, the committee's, at its August 21 position, and since August 25 a published proposed rule exists to compare it against; the comparison runs on `docs/7.35.3/recommendation.html` and in `analysis/8-25-recommendation-comparison.md`. Materials another party shows at a meeting, such as the department's August 21 side-by-side, are meeting record and live on the record pages, never as a standing position on the content pages.

## Where things are

| Path | What |
|---|---|
| `docs/` | The site, served from `main`. `docs/index.html` is the parts index; `docs/7.35.2/` holds the producer and laboratory pages and `docs/7.35.3/` the Training and Education pages; a redirect stub sits at every retired root address; `style.css` and `documents/` are shared and linked by root-absolute path |
| `docs/documents/` | Source PDFs, linked from the site |
| `source-text/` | Plain-text extractions, searchable |
| `analysis/` | Extractions, deltas, research. Public |
| `amendments/` | Drafting for the practicum sections, with its own audit harness. Branch work |
| `amendments-remainder/` | Drafting for the sections outside the practicum, with its own audit harness |
| `analytics/` | The visit-counter Worker. The only wrangler config in the repo. Kept; the dashboard is at `count.medical-psilocybin.org` (`OPERATIONS.md` 1.4) |
| `ARCHITECTURE.md` | Hosts, projects, parts, paths; the decisions of September 7, 2026 and their state |
| `OPERATIONS.md` | The infrastructure inventory and the runbooks |
| `tools/` | `partlib.py` says which Part a tool works on (`--part 7.35.2` or `7.35.3`; the default is 7.35.3) and where its pages live; each tool's data for a Part is in `tools/parts/<part>/`, and `check-all.py` checks every Part. `build-rule-page.py` regenerates `docs/7.35.3/rule.html` from the current extraction, sourcing the shared menu from `sync-nav.py` and running the stylesheet, counter, and provenance tools over the fresh page; `check-site.py` runs every check; `sync-nav.py`, `sync-record.py`, `sync-provenance.py`, `sync-count.py`, and `sync-css-version.py` each take `--check` |
| `tools/sync-pathways.py` | The content of `docs/7.35.3/pathways.html`: every starting license, every route, and every step. The page is generated from it, so a step, a verdict, or a citation is changed here and the tool is run. Hand-editing the page fails `check-site.py` |
| `tools/sync-status.py` | The status of the rulemaking: the dated events, each status item's state, date, and summary, and the procession. The status surfaces on `index.html`, `hours.html`, `eligibility.html`, and `training-hours-record.html` are generated from it, so a status change is made here and the tool is run. Hand-editing a status surface fails `check-site.py` |

## Current state of truth

**Part 2.** 7.35.2 NMAC, Producer and Laboratory Requirements, is the adopted rule, in effect since June 23, 2026, published in the New Mexico Register, Volume XXXVII, Issue 12: `docs/documents/rules-7.35.2-adopted-2026-06-23-published.pdf`, 19 pages, sections 7.35.2.1 through .27. Proposed amendments to 7.35.2.7, .10, and .24 were published August 25 and go to the October 2 hearing; until adopted the text stands unamended. The record from the March 24 notice through the hearing officer's May 26 report is in `tools/parts/7.35.2/sync-record.py`.

**Part 3.**

The current proposed rule is the **revised proposed rule published August 25, 2026**: `docs/documents/rules-draft-2026-08-25-published.pdf`, 20 pages, sections 7.35.3.1 through .28. The site cites it for section numbers and rule text. It was published with **proposed amendments to 7.35.2 NMAC**, `docs/documents/rules-7.35.2-amendments-2026-08-25-published.pdf`, which carry the definitions 7.35.3.7 imports, certifying clinician and practitioner among them, and with the **hearing notice**, `docs/documents/hearing-notice-2026-08-25.pdf`, fixing the rule hearing for October 2, 2026, 9:00 AM, in Santa Fe and by video conference and telephone, with written comment due by the close of the hearing. The delta against the July 23 text is `analysis/8-25-published-delta.md`.

Against the July 23 text, the August 25 text raised the therapy module from 30 didactic hours to 65, at least one third in person, doubled the simulated patient hours to 10, added eleven curriculum topics without per-area minimums, kept the practicum at 100 and 120 hours, and added a case-presentation evaluation, a low-risk requirement on the first 20 administration-day hours, and a didactic waiver. It kept the role names certifying clinician and practitioner.

The committee's recommendation stands at its **August 21 position**: 80 didactic hours with minimums in nine content areas, a staged practicum of 114 hours for licensed providers or 102 for facilitators closing in case presentation and consultation, stated in full beside the published text on `docs/7.35.3/recommendation.html` and recorded in `analysis/8-21-committee-extraction.md`. What the published text took, altered, and declined is `analysis/8-25-recommendation-comparison.md`.

The July 23 publication was set aside, on the record by the August 14 board meeting with no set-aside notice held, and is superseded. Earlier documents are history. Cite them only where a page is comparing versions.

The chain data lives in `tools/sync-record.py` (`DOCUMENTS`, rows marked `chain`), and `tools/sync-provenance.py` reads it and holds the chain narrative (`CHANGED`). When a document supersedes the current one, edit those two first, and regenerate the rule page with `tools/build-rule-page.py` from the new extraction; the tool runs again since August 26 and stamps the shared chrome itself.

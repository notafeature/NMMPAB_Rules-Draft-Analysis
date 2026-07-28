# UX analysis and functional redesign specification

Written July 28, 2026, against `main` at commit `4f36883`, the state of the site after the
navigation pass merged. This document analyzes function and specifies changes; it changes
nothing. Implementation happens later, in bounded sessions, one page at a time.

Sources read for this analysis: every file in `docs/` (fourteen pages, four redirect stubs,
`style.css`), `tools/check-site.py`, `tools/sync-provenance.py` output as it appears on the
pages, `UX-REVIEW-2026-07-17.md`, `WRITING-STANDARD.md`, `UPDATING.md`, and the redesign
folder's `BRIEF.md`, `README.md`, `RESTORATION-PLAN.md`, and `copy-audit-2026-07-26.md`. Two
figures were checked against `source-text/rules-draft-2026-07-23-published.txt`; everything
else is grounded in the pages as committed.

Vocabulary used throughout: **family A** is the seven pages built in the July 27 redesign
idiom (`index`, `rule`, `record`, `hours`, `recommendation`, `comment`, `about`); **family B**
is the seven pages restored from the pre-redesign site (`pathways`, `eligibility`,
`cs-number`, `specialization`, `deferred`, `changes`, `training-hours-record`). The four
redirect stubs (`documents`, `guide`, `history`, `input`) are out of scope except as link
targets.

Every recommendation is numbered R1 through R36 and tagged **SMALL** (hours of work),
**STRUCTURAL** (needs its own session), or **OPEN** (a question the owner must answer, with a
recommended default). Settled owner decisions are built on, not reopened.

---

## Part 1: Function analysis

### 1.0 Page inventory and names

The three name surfaces disagree on most pages. This table is the reference for the naming
recommendation (R31) and for the seam inventory (section 1.17).

| File | `<title>` (before suffix) | H1 | Nav label | Family |
|---|---|---|---|---|
| index.html | Overview | Overview | Where things stand | A |
| rule.html | The rule | The rule | The published rule | A |
| record.html | Record | Record | Meetings and filings | A |
| hours.html | The hours, as a working model | The hours, as a working model | Training hours | A |
| recommendation.html | Recommendation | Recommendation | Committee recommendation | A |
| comment.html | Public comment | Public comment | How to comment, and the Community input call-to-action | A |
| about.html | About | About | How this site is built | A |
| pathways.html | Provider Routes | Routes to a provider permit | Can I become a provider? | B |
| eligibility.html | Who Can Qualify | Who can qualify, and what each permit takes | Which licenses qualify | B |
| cs-number.html | The controlled-substance number: the certifying-clinician access point | same as title | The controlled-substance number | B |
| specialization.html | Specialized Domains | Specialized domains | Specialized domains | B |
| deferred.html | Practicum Requirements | Practicum requirements | What practicum changes touch | B |
| changes.html | The Rules Draft, Section by Section | The rules draft, section by section | Section by section | B |
| training-hours-record.html | Training Hours: The Tabled Numbers and the July 17 Decision | Training hours | The training-hours record | B |

Title suffixes also disagree: family A uses "· 7.35.3 NMAC Training and Education" uniformly;
family B uses three different suffixes ("NM Medical Psilocybin Training & Education", "NM
Medical Psilocybin 7.35.3", "NM Medical Psilocybin Training Rules") and `cs-number.html` uses
none.

### 1.1 index.html

- **Job.** Answer site function 1 on arrival: where the rulemaking stands, and route each kind
  of reader to the page that answers their question.
- **Reader and moment.** Everyone, first screen, often their only screen.
- **On leaving.** The reader knows the published text is operative, the hearing is August 28,
  the hours are the open item with a submitted recommendation, and which door is theirs.
- **What does the work.** The plaque paragraph (four dated facts, no preamble); the six
  "Find your part" portals; the three-line "Where things stand" (OPEN, DEFECT, SETTLED); the
  five-stage procession diagram; the scheduled dates; the "What changed on July 23" column;
  the full page directory at `#directory`.
- **Inert or misplaced.** The portals and the directory partially restate each other; the
  directory earns its place as the reachability backstop (`check-site.py` counts on it), so
  the redundancy is acceptable and cheap.
- **What the job requires that the page does not do.** There is no door for the reader whose
  intent is to object or comment; `comment.html` is reachable only through the menu. There is
  no patient signpost; the one-sentence scope statement exists on `eligibility.html` only, and
  a patient or family member landing on the front page is not told this site governs provider
  training rather than patient access.

### 1.2 rule.html

- **Job.** Hold the operative text: all twenty-eight sections verbatim, with the state of each
  contested provision noted at the provision (site functions 2 and 3).
- **Reader and moment.** Anyone who needs what the text says, mid-journey; the citation target
  for every other page.
- **On leaving.** The reader has read the controlling language and knows whether the provision
  they care about is open, noted, or defective.
- **What does the work.** The table of contents with per-section status marks (Open, Settled,
  Note, Defect); the serif `.verbatim` blocks; the per-section PDF page links carrying
  `data-cite` hover disclosure; the `note open` / `note blue` / `note defect` annotations
  placed inside the section they concern.
- **Inert or misplaced.** Nothing; the page is the cleanest expression of the site's method.
- **What the job requires that the page does not do.** A defect note names its finding ("Finding
  B4" in the 7.35.3.19 note) without linking anywhere; the finding lives on `deferred.html`,
  which has no per-provision anchors to link to (R23, R5).

### 1.3 record.html

- **Job.** The chronology: every meeting, vote, and document as a dated chain, plus the
  document register and the gaps register (site function 6, and settled decision 2).
- **Reader and moment.** The process follower, the journalist, the board member reconstructing
  how a figure got here; also every reader the Documents menu sends to `#documents`.
- **On leaving.** The reader knows what happened on a given date, what changed because of it,
  and holds the document behind it.
- **What does the work.** Newest-first dated entries; the Scheduled block; the register table
  with status marks; the gaps table naming what the site does not hold; the "Deeper accounts"
  pointer to the three retained record pages.
- **Inert or misplaced.** Nothing is inert, but almost everything is underpowered for the job;
  the specific failures are in section 3.3, where the replacement is specified.
- **What the job requires that the page does not do.** Events have no anchors, so no page can
  cite an event; entries are single paragraphs in which outcome, figures, positions, and
  document links are not separable; the chain and the register do not reference each other;
  document absences are silent at the event and visible only in the separate gaps table.

### 1.4 hours.html

- **Job.** The working model of the deferred quantities: move the three numbers, see the
  program total and the cost for the person training, against the published and recommended
  positions (site functions 2 and 3).
- **Reader and moment.** The prospective provider weighing time and money; the committee
  member or commenter testing a position.
- **On leaving.** The reader knows the two positions, what each means in hours and forgone
  earnings, and that the department decides what enters the hearing text.
- **What does the work.** The three sliders with PUBLISHED and RECOMMENDED pins; the role
  toggle; the two set-to buttons; the program-total and cost reads; the meaning line that
  names which position is on screen; the sourced `src` paragraph; the `noscript` fallback
  stating both positions in prose.
- **Inert or misplaced.** Nothing.
- **What the job requires that the page does not do.** The third quantity is labeled
  "Supervision · consultation after certification begins · PUBLISHED 10", and the published
  10-hour figure is the mentoring requirement at 7.35.3.17
  (`source-text/rules-draft-2026-07-23-published.txt`, 7.35.3.17: "10 hours of mentoring
  sessions after graduation and after practicum hours are completed"), while the page's source
  paragraph cites only .18 and .19. The label and citation need to name mentoring (R12).

### 1.5 recommendation.html

- **Job.** State what the committee submitted on July 27 beside what the published text says,
  since the submission document itself is not published on this site.
- **Reader and moment.** Anyone who saw "recommendation submitted" and wants the figures; the
  department-watcher waiting for the revised text.
- **On leaving.** The reader knows the recommended figures in full, their basis in the July 17
  presentation, and that the department decides what enters the hearing text.
- **What does the work.** The Status pair (NOW, THEN); the two-positions table with citations;
  the six-row figure list; the July 17 basis section; the "what lands here next" note.
- **Inert or misplaced.** Nothing.
- **What the job requires that the page does not do.** The two-positions table cites
  "7.35.3.19 (C)" for the published 10-hour figure in the "Case presentation and consultation"
  row. 7.35.3.19 (C) carries the practitioner's 20 supervisory hours; the published 10-hour
  counterpart of the recommended consultation requirement is the mentoring requirement at
  7.35.3.17 (same extraction as cited in 1.4). The citation misdirects a reader who checks
  it (R13).

### 1.6 comment.html

- **Job.** Two jobs: state how public comment works in this rulemaking (the hearing), and
  operate the site's own input channel, including the published input log.
- **Reader and moment.** The reader who has formed a view and wants to act on it; the reader
  answering the site's request for documents and corrections.
- **On leaving.** The reader knows comment is taken and recorded at the August 28 hearing,
  that the department wants input sooner, and what happens to anything sent through the form.
- **What does the work.** The official-channel paragraph; the form with its consent checkbox
  and stated handling; the received-input entries with links into the record.
- **Inert or misplaced.** Nothing inert; the page is short and each block earns its place.
- **What the job requires that the page does not do.** It never says what is at issue. A reader
  arriving with the intent to comment is not shown the three surfaces comment could address
  (the open hours and the submitted recommendation, the kept controlled-substance number, the
  five defect notes in the published text), each of which has a page (R14). The two received
  entries also appear in full on `training-hours-record.html#community`, so one comment is
  maintained in two places (R15).

### 1.7 about.html

- **Job.** Method and trust: how the site is built, the verification tiers, corrections.
- **Reader and moment.** The skeptical reader, once; the official deciding whether to rely on
  a figure.
- **On leaving.** The reader knows the tier of every kind of statement, that primary sources
  win on disagreement, and how to report an error.
- **What does the work.** The three-tier ladder (VERBATIM, TRANSCRIPT, COMPILED); the named
  soft point (the June 26 attribution); the corrections route through the comment form.
- **Inert or misplaced.** Nothing.
- **What the job requires that the page does not do.** The correction promise ("the correction
  is recorded in the repository history") points at commit history, while family B pages carry
  human-readable per-page revision logs and family A pages carry none; where a reader can see
  what changed on a page is inconsistent across the site (R33).

### 1.8 pathways.html

- **Job.** Personal routing: pick a starting license, see the route to each of the three
  permits as ordered steps, each step with status, citation, and the recommendation's change
  shown beneath it (site functions 2 and 3, in one instrument).
- **Reader and moment.** The prospective provider, early, asking "can I do this and what would
  it take from where I stand."
- **On leaving.** The reader knows which permits are open to them, every step of the route,
  which steps are settled, open, or contested, and what changes if the recommendation is
  adopted.
- **What does the work.** The five starting-license profiles; the per-start verdict buttons;
  the step lists with Settled / Open / Contested flags, why-lines, per-step citations to the
  published rule by page, and the "If the committee recommendation is adopted" notes; the
  `eligref` line linking each profile to its band in the eligibility tables and to
  `cs-number.html`; the legend defining the three flags with dated status.
- **Inert or misplaced.** The footer link labeled "Recent developments" points at
  `record.html`, whose name is now "Meetings and filings"; a retired name survives in the
  chrome (R20). The provenance chain block restates four register entries (see 1.16).
- **What the job requires that the page does not do.** All content is JavaScript-rendered into
  empty `#starts` and `#panel` divs; browser find, search indexing, and no-JS readers get
  nothing but a pointer to `eligibility.html` (UX-REVIEW-2026-07-17 Finding 8, still open).
  Nothing on the page is addressable: a selection cannot be linked, so no other page can send
  a reader to "your row, already selected" (R17). The practicum steps state hours the model on
  `hours.html` exists to interrogate, without linking it (R19).

### 1.9 eligibility.html

- **Job.** The static reference: the steps for each permit side by side (Table 1), and the
  license-by-permit verdicts for nineteen starting licenses (Table 2). It is also the declared
  no-JavaScript fallback for `pathways.html`.
- **Reader and moment.** The provider who wants their license row, mid-journey; the reader
  comparing permits rather than following one route.
- **On leaving.** The reader knows the verdict for their license against each permit, and what
  each permit requires at every step.
- **What does the work.** The legend defining seven verdict and status words; both tables; the
  banded rows with anchors (`#band-medical` through `#band-outofstate`) that `pathways.html`
  links into; the certifying-clinician cells that link to `cs-number.html` with a
  title-attribute tooltip; the reciprocity bar; the patient signpost sentence; the sourced
  notes citing each subsection to its page; the "If the committee recommendation is adopted"
  block.
- **Inert or misplaced.** The specialization Options-raised zone duplicates the substance of
  `specialization.html`'s summary; it predates that page's existence and now overlaps it. The
  provenance chain block restates the register (1.16).
- **What the job requires that the page does not do.** Verdict cells dead-end: a reader who
  finds "Psychologist · Practitioner · Eligible" cannot get from that cell to the practitioner
  route for a therapy license, because `pathways.html` has no addressable state (R18). The
  tooltip on certifying-clinician cells uses the `title` attribute, which touch devices never
  show and which sits outside the site's citation-disclosure system (R21). The hero stamp
  reads "Updated July 25, 2026" while the recommendation block on the same page states the
  July 27 submission; the stamp contradicts the content's own date (R22).

### 1.10 cs-number.html

- **Job.** The deep reference on the one contested requirement: what the New Mexico
  controlled-substance number is, who needs it, what it does and does not do at this access
  point, comparators, liability, rural supply, and the verbatim July 9 record by speaker.
- **Reader and moment.** The certifying-clinician candidate; the commenter building an
  argument; the board member checking what was said.
- **On leaving.** The reader knows the requirement stands in the published text at two cited
  locations, what remains open, and the full argument landscape on both sides, each claim at
  its stated verification tier.
- **What does the work.** The "On this page" list with the update first; the update section
  through July 23; eight numbered sections, each opening with a thesis and closing with a
  per-section confidence statement; the verbatim speaker record in a collapsible; the tiered
  footer.
- **Inert or misplaced.** Nothing. This is the strongest page on the site, as the July 26 copy
  audit also concluded, and this specification changes nothing about it except its links
  inward and outward.
- **What the job requires that the page does not do.** Nothing material. It is the model the
  record rebuild should imitate for depth-with-structure.

### 1.11 specialization.html

- **Job.** Record the July 16 specialized-domain proposal: an endorsement layered on a core
  permit, its proposed hours, who raised what, with the standing caution that none of it is in
  the published rule.
- **Reader and moment.** The end-of-life practitioner or hospice-adjacent reader; the
  committee member tracking what was raised but not drafted.
- **On leaving.** The reader knows the proposal's shape, its proposed hour ranges, that
  nothing in the published text creates it, and where it could re-enter the process.
- **What does the work.** The hero caution; the single explanatory section with its
  positions-by-speaker boxes; the `#hours` anchor that `eligibility.html` and `hours.html`
  link into.
- **Inert or misplaced.** Nothing structurally.
- **What the job requires that the page does not do.** Attributions include first names alone
  ("Jenn", "Jamie", "Dom") and the term "Space Attendant" is used without definition, both
  against the standing rule that every element introduces itself (copy audit, items 8) (R24).
  The whole page rests on a source document the repository does not hold (UPDATING.md Part 6,
  the July 16 record), which the page should state where it cites (R24).

### 1.12 deferred.html

- **Job.** The blast radius: every provision a practicum change has to touch, quoted verbatim
  from the published rule, with the three provisions that do not work as written flagged.
- **Reader and moment.** The drafter, the department reader, the committee member; anyone
  editing or evaluating a practicum recommendation.
- **On leaving.** The reader knows all thirteen provisions a change reaches, what each says,
  and where the published text fails.
- **What does the work.** The provision-by-provision quoted blocks with per-provision status
  flags and page citations; the defect analyses.
- **Inert or misplaced.** The provenance chain block (1.16).
- **What the job requires that the page does not do.** Provisions have no anchors, so
  `rule.html`'s defect notes name findings they cannot link to, and no other page can cite a
  specific provision analysis (R23). The page's three name surfaces disagree with each other
  and with the job: the title says "Practicum Requirements", the H1 "Practicum requirements",
  the nav "What practicum changes touch" (R31).

### 1.13 changes.html

- **Job.** The provision-level comparison: what the training and education provisions say as
  published, and the full section-by-section history of the June 12 recommendation against the
  department drafts.
- **Reader and moment.** The record-checker; the reader tracing where a provision came from.
- **On leaving.** The reader knows what changed between versions, provision by provision, with
  each cell cited to its document and page.
- **What does the work.** The layered structure (published text first, comparison beneath);
  roughly one hundred fifty page-anchored citations into three documents; the column-hide
  control.
- **Inert or misplaced.** The provenance chain block (1.16).
- **What the job requires that the page does not do.** A 160 KB page has one content anchor
  (`#training-now`); no provision can be cited from outside, which for a comparison page is
  the main way it would be used by other pages (R25). The July 26 copy audit's findings stand:
  "Dr. Ann Metz" against the corrected "Anne", first-name-only rows in the agreements tables,
  and published to-do notes (R26).

### 1.14 training-hours-record.html

- **Job.** The retained record of the training-hours question: the published figures by role,
  who they fall on, benchmarks from other states, cost variables, the July 9 and July 17
  records, and community comment.
- **Reader and moment.** The reader who needs the full history and evidence behind the hours,
  arriving from `hours.html`, `record.html`, or the nav.
- **On leaving.** The reader knows the published figures, the positions stated on the record,
  what comparable programs require, and what training may cost.
- **What does the work.** The role cards; the benchmark table; the cost section; the
  per-speaker record anchors (`#rec-peskuski` and others); the community section that
  `comment.html` links into.
- **Inert or misplaced.** The status strip is doing `index.html`'s job on a record page, and
  doing it wrong (next bullet).
- **What the job requires that the page does not do.** The status strip states "The committee
  has not delivered a recommendation and was given no deadline"
  (training-hours-record.html:399). The recommendation was submitted July 27, as stated on
  `index.html`, `record.html`, `recommendation.html`, `hours.html`, and `pathways.html`. This
  is the one place on the site that currently fails function 1 ("be right every time"), and it
  is the predictable failure mode of a record page carrying a live status block (R27, R28).

### 1.15 The three instruments together

- **What each uniquely answers.**
  - `pathways.html`: "from my starting point, what is the ordered route to each permit, and
    what changes for me if the recommendation is adopted." It is the only page organized by
    the reader's situation and the only one that shows published text and recommendation
    per step.
  - `eligibility.html`: "which licenses map to which permit," all nineteen rows visible at
    once. It is the only page where permits can be compared side by side, and the only static,
    findable, no-JS rendering of the routing data.
  - `cs-number.html`: "what is this one contested requirement, in full." It is the only page
    that argues nothing and still equips a reader to argue either side.
- **Where they overlap.** Eligibility's Table 1 is the same requirements data as pathways'
  step lists, projected as columns instead of routes; the five pathways starting profiles are
  compressions of eligibility's nineteen Table 2 rows; both state the practicum hours, the
  waiver deadlines, and the controlled-substance requirement in one line each. The overlap is
  the design, not a defect: three projections of one model for three reading postures. What is
  missing is not less overlap but working passage between them.
- **How a reader should flow.** Arrive at either routing instrument; from an eligibility
  verdict cell, land on the matching pathways selection (missing today, R18); from a pathways
  profile, land on the matching eligibility band (exists today via `eligref`); from any
  certifying-clinician verdict or step, land on `cs-number.html` (exists today); from any
  practicum step, land on the hours model (missing today, R19); from `cs-number.html`, return
  to the two routing instruments that sent the reader (missing today, R16).

### 1.16 Document links: the inventory (settled decision 1)

The shared menu's Documents dropdown adds four PDF links and one register link to every page;
those are excluded from the per-page counts below, which are body links only.

| Page | Body document links | Character |
|---|---|---|
| index.html | none | routing only; correct |
| about.html | none | method prose; correct |
| comment.html | none | correct |
| record.html | 10 documents in the register, 8 repeated in chain entries, 2 supplementary (one-pager, slides) | the canonical home plus its own duplication |
| recommendation.html | 2 (committee transcript, Metz recommendations, each cited twice) | citations at the point of reading |
| hours.html | 3 (published rule, committee transcript twice) | citations at the point of reading |
| rule.html | ~25 page-anchored links into the published PDF | citations; the page's whole method |
| changes.html | ~150 page-anchored links into three documents | citations; the page's whole method |
| pathways.html | per-step page-anchored citations (JS-rendered), 1 in the sources footer, 4 in the chain block | citations, plus chain duplication |
| eligibility.html | 8 page-anchored citations in source notes, 4 in the chain block | citations, plus chain duplication |
| cs-number.html | 9 page-anchored citations, 4 in the chain block | citations, plus chain duplication |
| deferred.html | 10 page-anchored citations, 4 in the chain block | citations, plus chain duplication |
| specialization.html | 2 page-anchored citations, 4 in the chain block | citations, plus chain duplication |
| training-hours-record.html | ~20 page-anchored citations, 4 in the chain block | citations, plus chain duplication |

- The duplication with no citation function is exactly one pattern: the generated provenance
  chain block on the seven family B pages, which restates four register entries (with
  download links) at the foot of every page (R29).
- Everything else that links a document is a citation serving a claim at the point of reading,
  and stays under the citation discipline.
- The seven family A pages carry no body document links outside `record.html`, so the sprawl
  named in the task brief is, post-merge, concentrated in the chain blocks and in the
  register's own duplication between chain entries and register rows; the register
  specification in section 3.3 resolves the latter by making the chain reference the register
  rather than repeat it.

**What the register owes a reader** (specified in R6): for every document, in one row: what it
is in one sentence; its date; its status as one of Current, Superseded (naming what superseded
it and when), or Record; its page count; for transcripts, whether it carries speaker labels;
and a stable per-document anchor so any page can cite the register entry rather than restating
the document's identity. Beside it, the gaps table: every document the site does not hold,
what its absence means, and which event it belongs to.

**What the menu carries** (specified in R8): the register link, the current operative text,
and the documents of the most recent meeting or filing; nothing else. The dropdown changes
only when the chain changes.

**Which inline links stay:** every page-anchored citation at a claim. **Which go:** the chain
block's four download links on seven pages (replaced by one line linking the register), and
nothing else.

### 1.17 The seam: what changes at the family boundary (settled decision 3)

Crossing from any family A page to any family B page, these change. This is the inventory for
the later design-system pass; nothing here is fixed in this analysis.

1. **Stylesheet delivery.** A links `style.css?v=<hash>` (one shared file); B carries a
   per-page inline `<style>` block of 145 to 214 lines and does not link `style.css`.
2. **Tokens.** A: white ground `#FFFFFF`, ink `#16181D`, one blue `#2447C7`, semantic washes
   (amber open, green settled, red defect). B: tinted ground `#FBFAFC`, text `#1A1621`, violet
   accent `#5A4A88` with soft `#EBE6F5`, layered surface, border, and shadow tokens.
3. **Type.** A: sans for the site's voice, serif only inside `.verbatim`, mono for data and
   wayfinding. B: its own serif appears in display roles (hero headings), with different
   stacks.
4. **Hero.** A: `div.head` with mono uppercase `.kicker`, H1, `.lede`, mono `.stamp`. B:
   `header.hero` with `.eyebrow`, H1, a bold "Updated" sentence, `.lede`, and page-specific
   legend blocks.
5. **Layout.** A: `main.wrap` at 1080px, hairline rules, space instead of boxes. B: `div.col`
   containers with cards, borders, 8 to 11px radii, and shadows.
6. **Menu rendering.** Markup is byte-identical on all fourteen pages (`check-site.py`
   enforces it), but it is styled twice: `style.css` rules on A (blue active state, 4px radii,
   ink-bordered dropdown) and the per-page `#navpass` block on B (violet active state, 8 to
   10px radii, shadow tokens, different paddings). The same menu renders visibly differently
   on either side of the seam.
7. **Status vocabulary.** A: one `.mark` set (open, settled, defect, gray, blue), dot plus
   word. B: three per-page sets (`.pill`, `.fl`, `.tag`) with their own colors for the same
   meanings.
8. **Citations.** A: `data-cite` hover disclosure and the `.cite` popover (open on hover,
   close on leave, click opens the source in a new tab), per site function 4. B: plain
   new-tab links; `title`-attribute tooltips on eligibility's verdict cells; no hover
   disclosure anywhere. Function 4 is currently met on one family only.
9. **Footer.** A: `footer.foot`, two disclaimer lines, two links. B: a `Sources` prose block,
   the generated provenance details (chain plus revisions), then `.sitefoot` with different
   wording and a third link labeled "Recent developments".
10. **Provenance.** B pages carry the generated chain and per-page revision log; A pages carry
    neither.
11. **Naming.** Title suffixes and title/H1/nav agreement differ as inventoried in 1.0.

---

## Part 2: Reader journeys

### J1. "Can I do this work, and what will it take?"

- **Reader.** A prospective provider: an LCSW in Las Cruces, a hospice chaplain, an
  out-of-state facilitator.
- **Ideal path.** `index` portal → `pathways` (their start selected) → per-step statuses, with
  side trips to `cs-number` if they would certify, `hours` for time and cost, `eligibility`
  for their exact license row.
- **Where the site loses them.** A shared or searched link cannot land them on their
  situation, because pathways has no addressable state; browser find fails on pathways because
  the content is JS-rendered; from an eligibility verdict cell there is no way into the
  matching route; from a practicum step there is no way into the hours model; a patient or
  family member on this journey discovers only on `eligibility.html` that the site does not
  govern them.
- **Smallest change that keeps them moving.** R17 (pathways URL state), R18 (verdict-cell deep
  links), R19 (step-to-model links), R2 (patient signpost on the front page).

### J2. "What does the rule say now, as written?"

- **Reader.** A provider checking one requirement; an official; a commenter verifying a claim.
- **Ideal path.** `index` → `rule.html` table of contents → section, or a direct citation link
  from any page.
- **Where the site loses them.** Rarely; this journey works. The residual risk is arrival on
  `changes.html` or `training-hours-record.html` from a search engine, where older titles and,
  on the latter, a stale status strip can misstate the present (R27).
- **Smallest change.** R27 (fix the stale sentence), R31 (naming agreement so search results
  name the pages truthfully).

### J3. "How do I object, and what is at issue?"

- **Reader.** A community member preparing comment for the August 28 hearing.
- **Ideal path.** The menu call-to-action → `comment.html` → the hearing facts → the contested
  surfaces → the form or the hearing.
- **Where the site loses them.** `comment.html` states how to comment but not what is open to
  comment; the reader must already know the site to find the hours dispute, the
  controlled-substance argument, and the defect notes; the hearing notice is absent (stated
  honestly, tracked in the gaps register).
- **Smallest change.** R14 (a three-line "what is at issue" block linking
  `recommendation.html`, `cs-number.html`, and `rule.html`'s defect notes).

### J4. "What happened, and what changed because of it?"

- **Reader.** The process follower, the journalist, the board member; after the rulemaking
  ends, everyone (function 6).
- **Ideal path.** `record.html`, newest first, each event with its outcome, its consequences,
  and its documents.
- **Where the site loses them.** The chain entries are dense paragraphs; what changed is not
  separable from what was said; events cannot be cited or linked individually; depth lives on
  three retained pages the entry text does not always point to at the moment of need.
- **Smallest change.** None that is small and honest; this is the record rebuild (R5), which
  is why settled decision 2 exists.

### J5. "Give me the documents."

- **Reader.** Anyone: a reporter wanting the published rule, a researcher wanting the
  transcripts, a board member wanting the Metz materials.
- **Ideal path.** Documents menu → the wanted PDF directly, or the register for everything.
- **Where the site loses them.** The register has no date column and no per-document anchors;
  "Superseded" rows do not say what superseded them; the Metz one-pager and slides are links
  buried inside another row's sentence; the dropdown's membership rule (why these four) is
  stated nowhere and enforced only by a hardcoded list in `check-site.py`.
- **Smallest change.** R6 (register columns and anchors), R8 (the dropdown contract).

---

## Part 3: Functional redesign specification, per page

Verdicts use the task's vocabulary: keep, merge, split, retitle, re-scope. No page is deleted
or merged in this specification. Retitles are gathered in R31 so the naming lands as one
coordinated pass.

### 3.1 index.html: keep

- **R1 · SMALL.** Add a seventh portal: "I want to comment on the rule", one sentence, linking
  `comment.html`. Reason: J3 is a first-class intent with no door (1.1); the portals grid is
  currently six cells and takes a seventh without structural change.
- **R2 · SMALL.** Add the one-sentence patient signpost to the front page, reusing the
  sentence already on `eligibility.html` (its wording is settled and sourced): the site covers
  provider training; patient access is set by the Act; the qualifying conditions, linked to
  `cs-number.html#act`. Reason: the worst journey found by UX-REVIEW-2026-07-17 (Finding 3)
  was fixed on one page only; the front page is where search and shares land.
- **R3 · SMALL.** In the "Where things stand" DEFECT line, state both counts the site uses:
  five defect notes across four sections of the published text, three of them practicum
  provisions analyzed on `deferred.html`, and link both `rule.html` and `deferred.html`.
  Reason: today the front page says "five provisions" while its own directory row for
  deferred says "three flagged", and a reader who meets both has no way to reconcile them.

### 3.2 rule.html: keep

- **R4 · SMALL.** Where a note names a finding ("Finding B4"), link the finding to its
  provision analysis on `deferred.html`, once R23 gives that page anchors. Reason: 1.2; a
  named but unlinked cross-reference asks the reader to go search.
- The page is otherwise the model for the site and takes no other change in this
  specification.

### 3.3 record.html: re-scope: rebuild as the chronology instrument (settled decision 2)

Why the current form is not good enough, specifically:

- Each entry is one paragraph in which the outcome, the figures, the named positions, and the
  document links are typographically undifferentiated; the July 23 entry carries six distinct
  changes in ~120 words of running prose, and a reader cannot scan for "what changed" without
  reading everything (record.html:93).
- Events have no anchors, so no page can cite an event; the consequence, measured in
  UPDATING.md Part 2, is that other pages restate event facts (the 7-0 vote on ten pages, the
  hearing date on eleven) instead of linking them.
- What changed because of an event is not separable from what was said at it, so the page
  cannot answer J4's second half without full reading.
- Attachments are inline prose links; whether an event has a document at all is discoverable
  only by reading, and absences (June 26, July 16, May 22) are silent at the event, stated
  only in the separate gaps table.
- The chain entries and the register rows describe the same documents twice in different
  words, which is the drift pattern named in BRIEF.md diagnosis 1.
- The "Deeper accounts" block outsources depth to three retained pages in a closing paragraph
  rather than attaching each account to the events it covers.

**R5 · STRUCTURAL.** Rebuild `record.html` around an event schema. Every meeting, document
publication, filing, and scheduled date is one event:

```
<section class="event" id="e-2026-07-23">          (anchor: e-YYYY-MM-DD, suffixed
                                                    -am/-pm or -2 on multi-event days)
  date                                              mono, the wayfinding key
  kind                                              one of MEETING · DOCUMENT · FILING ·
                                                    SCHEDULED
  what happened                                     one to two sentences, outcome first
  what changed                                      a list, one state transition per line,
                                                    each linking the page that owns the fact
                                                    (e.g. "Practicum hours: deferred to
                                                    committee → published unchanged", linking
                                                    rule.html#s19)
  who said what                                     optional, collapsed by default, only
                                                    where the record page does not own it;
                                                    otherwise one line linking the deep
                                                    account (cs-number.html#record,
                                                    training-hours-record.html#record)
  attached                                          every document of the event: link, one-
                                                    line identity, label status for
                                                    transcripts, and a link to its register
                                                    row; where no document exists, one line
                                                    stating the absence and linking the gaps
                                                    register row
</section>
```

Content mapping from the current page, line by line (nothing is dropped):

| Current element | Destination |
|---|---|
| Scheduled block (Aug 14, 21, 28) | three SCHEDULED events at the top of the chain |
| JUL 27 entry | event `e-2026-07-27` (FILING); figures move to "what changed" lines linking `recommendation.html` |
| JUL 23 entry | event `e-2026-07-23` (DOCUMENT); its six changes become six "what changed" lines |
| JUL 17 afternoon entry | event `e-2026-07-17-pm` (MEETING); positions collapse into "who said what", linking `training-hours-record.html` |
| JUL 17 morning entry | event `e-2026-07-17-am` (MEETING); CS-number outcome links `cs-number.html#update` |
| JUL 16, JUL 9, JUN 26, JUN 25, JUN 12, JAN to MAY entries | events, same treatment; JUN 26 and JUL 16 carry absence lines to the gaps register |
| Document register | stays as `#documents`, rebuilt per R6 |
| Gaps table | stays as `#gaps`, rebuilt per R7 |
| "Deeper accounts" paragraph | dissolved; each pointer moves into the event it covers |

- **R6 · STRUCTURAL** (same session as R5). Rebuild the register per the contract in 1.16:
  columns Document (with anchor `id="doc-<slug>"`), Date, What it is, Status, Notes. Status
  values: Current; Superseded, always naming the superseding document and date; Record.
  The Metz one-pager and slides become their own rows. The unpublished summary of the
  recommended rules keeps its row, stating that its figures are on `recommendation.html` and
  the document itself is not published on this site.
- **R7 · SMALL** (rides with R5). Each gaps-register row names the event it belongs to and
  links its anchor; each affected event carries the reciprocal absence line.
- **R8 · SMALL.** State the Documents dropdown's contract and enforce it: the register link,
  the current operative text, and the documents of the most recent meeting or filing. Move the
  dropdown's document list into the generator (`tools/sync-nav.py`) so the menu, the register,
  and `check-site.py`'s hardcoded list cannot disagree; the check then reads the same source.
- **R9 · OPEN.** Should the events and register be generated from one data structure in a tool
  (extending `tools/sync-provenance.py`, whose `CHAIN` dict already holds the document data),
  or hand-maintained on the page? Recommended default: tool-generated. Every hand-maintained
  status fact on this site has drifted and no tool-owned block ever has (BRIEF.md diagnosis
  1); the record is the site's most update-frequent page.
- **R10 · OPEN.** Should the register remain a section of `record.html`, or return to a
  standalone `documents.html` (the stub currently redirects into `record.html#documents`)?
  Recommended default: remain on `record.html`. A document is an artifact of an event; one
  chronology page holding both keeps them adjacent, and RESTORATION-PLAN.md Phase 4 already
  leaves the standalone question to owner judgment. The stub stays either way.

### 3.4 hours.html: keep

- **R11 · SMALL.** Add one line beneath the model linking the two routing instruments: "Where
  these hours sit in your route" → `pathways.html`; "The license tables" →
  `eligibility.html`. Reason: 1.15; the model is a cul-de-sac today.
- **R12 · SMALL.** Rename the third quantity from "Supervision" to name mentoring and
  consultation explicitly, and add 7.35.3.17 to the source paragraph. Verify against the
  published PDF in the implementing session before editing. Reason: the published 10-hour
  figure the slider carries is the mentoring requirement at 7.35.3.17 (1.4); the current label
  and citation cannot be checked in thirty seconds, which is the site's own standard.

### 3.5 recommendation.html: keep

- **R13 · SMALL.** Correct the "Where" citation on the "Case presentation and consultation"
  row from 7.35.3.19 (C) to 7.35.3.17, verifying against the published PDF in the
  implementing session. Reason: 1.5; the cited subsection carries a different quantity.

### 3.6 comment.html: keep, re-scope lightly

- **R14 · SMALL.** Add a "What is at issue" section above the form: three one-line entries
  linking `recommendation.html` (the open hours and the submitted figures),
  `cs-number.html` (the kept requirement and the arguments on the record), and `rule.html`
  (the five defect notes). Each line states, not argues. Reason: J3.
- **R15 · OPEN.** One received comment currently lives in full on both `comment.html` and
  `training-hours-record.html#community`. Which page owns the input log? Recommended default:
  `comment.html` owns form submissions and their published texts; meeting public comment stays
  where the meeting record lives, and `comment.html` links it in one line instead of pasting
  it. This restores the one-page-owns-a-fact rule (UPDATING.md Part 2).

### 3.7 about.html: keep

- **R33 · OPEN** (cross-page, stated here). Family B pages carry per-page revision logs;
  family A pages carry none, and `about.html` points readers at raw repository history.
  Should the revision log return to all pages via `tools/sync-provenance.py`? Recommended
  default: yes, restore `REVISIONS` output on family A pages; the log is the reader-facing
  form of the corrections promise, and the tool already exists.

### 3.8 pathways.html: keep, improve (settled decision 4: never reduced)

- **R17 · STRUCTURAL.** Give the instrument URL state. Mechanism, precisely: the location hash
  carries `#start=<id>` or `#start=<id>&permit=<key>`, where `<id>` is one of the existing
  `STARTS[].id` values (`none`, `therapy`, `diagnose`, `otherhealth`, `elsewhere`) and
  `<key>` is one of the existing `PERMITS` keys (`dc`, `prac`, `fac`, `recip`). On load, parse
  the hash before the first `render()`: a matching `start` sets `current`; a matching `permit`
  sets `activePath[st.id]`; anything unrecognized falls through to the current default with no
  error. On every selection, write the canonical hash with `history.replaceState`, so the
  visible state is always the shareable URL. No content changes; the existing `render()` and
  `drawJourney()` are reused as is.
- **R18 · SMALL** (after R17; belongs to `eligibility.html` but specified here with its
  target). Eligibility Table 2 verdict cells link into the matching pathways state. The row
  band fixes the start; the column fixes the permit. Mapping: rows under `#band-medical` →
  `start=diagnose`; `#band-behavioral` → `start=therapy`; `#band-otherhealth` →
  `start=otherhealth`; `#band-community` → `start=none`; `#band-outofstate` →
  `start=elsewhere`. Columns: Certifying Clinician → `permit=dc`, Practitioner →
  `permit=prac`, Facilitator → `permit=fac`; out-of-state rows → `permit=recip`. Cells
  graded "No current path" or "Not specified" link the start only (`#start=<id>`), because
  there is no route to show. The existing links from certifying-clinician cells to
  `cs-number.html` are kept; the pathway link is added alongside, not in place of them, and
  never nested (UPDATING.md Part 5 forbids nested anchors). The "Other NM-licensed
  professional" row maps to `start=otherhealth`.
- **R19 · SMALL.** Every practicum step (`prac` step 4, `fac` step 4) adds one link: "the
  working model of these hours" → `hours.html`. Reason: 1.8; the step states quantities the
  model exists to interrogate.
- **R20 · SMALL.** The footer link labeled "Recent developments" is relabeled to the record
  page's canonical name (R31). Reason: a retired page name survives in the chrome.
- **R32 · OPEN.** Should the five start panels be pre-rendered statically (a build tool in the
  manner of `tools/build-rule-page.py` emitting all five panels into the HTML, with the
  existing script reduced to toggling visibility and managing the hash), or should the page
  stay JS-rendered with the `noscript` pointer to `eligibility.html`? Recommended default:
  pre-render. It closes UX-REVIEW Finding 8 (browser find, indexing, JS failure), it removes
  the last argument for site search, and the build-tool pattern already exists in this
  repository. This is its own session.

### 3.9 eligibility.html: keep, improve (settled decision 4)

- **R18** applies here (verdict-cell deep links; specified in 3.8).
- **R21 · SMALL.** Convert the `title`-attribute tooltips on certifying-clinician verdict
  cells to `data-cite` attributes carrying the same sentence. The attribute is inert on family
  B today and becomes live disclosure when the design-system pass extends the `a[data-cite]`
  CSS to these pages; the content work is done now, the styling later. Reason: seam item 8;
  `title` never shows on touch devices.
- **R22 · SMALL.** Currency sweep: the hero stamp reads July 25 while the
  recommendation-adopted block on the same page states the July 27 submission; restamp and
  reconcile. Reason: a page that disagrees with itself about its own date repeats the
  UX-REVIEW Finding 2 pattern.
- The specialization Options-raised zone stays; it is the page-local summary the tables need,
  and it links `specialization.html` for depth. No merge.

### 3.10 cs-number.html: keep (settled decision 4)

- **R16 · SMALL.** Add one line at the foot of the update section linking the two routing
  instruments that send readers here: the eligibility verdict cells and the certifying-
  clinician route on pathways. Reason: 1.15 flow; the page is an endpoint today and readers
  arriving from a verdict cell have no way back into their route.
- No other change. The page is the site's strongest and the record rebuild's model.

### 3.11 specialization.html: keep

- **R24 · SMALL, part OPEN.** Introduce every named participant with full name and role at
  first mention, define "Space Attendant" where it first appears, and state at the point of
  citation that the July 16 meeting record is not held in this repository (linking the gaps
  register row). OPEN: the full names and roles behind "Jenn" and "Jamie" are not in the
  repository; they need owner knowledge or the July 16 source document. Recommended default:
  use full names where the owner can supply them; where they cannot be fixed from a source,
  state the attribution basis explicitly rather than guessing.

### 3.12 deferred.html: keep, retitle (via R31)

- **R23 · SMALL.** Add a stable anchor per provision (`id="p-19-A"` pattern, one per quoted
  provision block), and add reciprocal links: each provision analysis links the same section
  on `rule.html` (`rule.html#s19`), and `rule.html` defect notes link back (R4). Reason: 1.12;
  the page is the reference for five defect analyses that nothing can point at.

### 3.13 changes.html: keep

- **R25 · SMALL.** Add a stable anchor per provision row, same pattern as R23. Reason: 1.13; a
  comparison page that cannot be cited into is used only by readers who already know it.
- **R26 · SMALL.** Apply the July 26 copy audit to this page: correct "Dr. Ann Metz" to
  "Dr. Anne Metz" (three instances), give first-name-only rows full names at first mention,
  and remove published to-do notes. Quoted verbatim material is not touched. Reason: the audit
  found these on July 26 and they are still in the file.

### 3.14 training-hours-record.html: re-scope: a dated record, not a live status page

- **R27 · SMALL, first in order of execution.** Correct the status strip sentence "The
  committee has not delivered a recommendation and was given no deadline"
  (training-hours-record.html:399) to state the July 27 submission, citing
  `recommendation.html`. Reason: 1.14; this is the site's one live factual failure, on a site
  whose entire product is being right.
- **R28 · SMALL.** Re-scope the page's frame from live status to dated record: the status
  strip becomes "Status as of <date>", states that the current state lives on `index.html`,
  and links it; the page keeps everything else it holds (roles, benchmarks, cost, the July 9
  and 17 records, community comment). Reason: a record page carrying a live status block is
  how R27's defect happened, and the page will otherwise fail the same way after August 14,
  August 21, and August 28.

### 3.15 Cross-page recommendations

- **R29 · SMALL.** On the seven family B pages, replace the four-document chain listing inside
  the provenance block with one line linking the register (`record.html#documents`), keeping
  the per-page revision log unchanged. Implemented in `tools/sync-provenance.py`, not by hand
  (UPDATING.md Part 3 forbids hand-editing generated blocks). Reason: 1.16; this is the only
  non-citation document-link duplication on the site.
- **R30 · STRUCTURAL.** Create `tools/sync-status.py` as designed in BRIEF.md section 7: one
  `STATUS` structure holding each item's state, date, and one-line summary, writing the marked
  status blocks on the pages that show status (`index.html` "Where things stand", the
  `hours.html` kicker, the `eligibility.html` legend dates, the `training-hours-record.html`
  "as of" strip after R28). Reason: R27's defect class is mechanical and the site's own
  history (BRIEF diagnosis 1) shows tool ownership is what ends it.
- **R31 · SMALL, adoption OPEN.** One naming pass: for each page, title, H1, and nav label
  agree, with the family A suffix everywhere. Proposed names, for the owner to amend: Where
  things stand (index); The published rule (rule); Meetings and filings (record); The training
  hours (hours); The committee recommendation (recommendation); Comment (comment, and the nav
  call-to-action reads Comment as well); How this site is built (about); Routes to a permit
  (pathways); Which licenses qualify (eligibility); The controlled-substance number
  (cs-number); Specialized domains (specialization); What a practicum change touches
  (deferred); Section by section (changes); The training-hours record
  (training-hours-record). OPEN: adopt this table as written, or amend; recommended default is
  adoption, because every pair of surfaces that disagrees today (1.0) costs a re-orientation
  on every navigation.
- **R34 · SMALL.** Extend `tools/check-site.py`: a title/H1/nav-label agreement check (data
  from the same table R31 lands); a check that every document in the Documents dropdown has a
  register row; a check that every `id` cited from another page exists (generalizing the
  existing stub-anchor check to all internal fragment links). Reason: each corresponds to a
  defect class found in this analysis (1.0, J5, R23/R25 anchors).
- **R35 · SMALL.** Re-point `UPDATING.md` Part 2 (the fact index and the ownership table) at
  the current fourteen pages once R5 through R28 land; CLAUDE.md already names this as open
  work. Reason: the propagation map is the maintenance instrument, and it still routes to the
  pre-redesign site.
- **R36 · STRUCTURAL** (design-system pass, listed for completeness, not executed from this
  document). Extend the `a[data-cite]` disclosure CSS to family B so function 4 holds
  site-wide; the content-side preparation is R21. The rest of the seam inventory (1.17) is
  that pass's input.

### 3.16 Verdict summary

| Page | Verdict |
|---|---|
| index.html | keep |
| rule.html | keep |
| record.html | re-scope (rebuild as the chronology instrument) |
| hours.html | keep |
| recommendation.html | keep |
| comment.html | keep, re-scope lightly (own the input log, add the at-issue block) |
| about.html | keep |
| pathways.html | keep, improve (URL state, pre-render, cross-links) |
| eligibility.html | keep, improve (deep links, disclosure attributes, currency) |
| cs-number.html | keep |
| specialization.html | keep |
| deferred.html | keep, retitle |
| changes.html | keep (anchors, copy corrections) |
| training-hours-record.html | re-scope (dated record, not live status) |
| documents/guide/history/input stubs | keep as redirect targets; out of scope |

---

## Appendix A: visual notes (ignorable)

These are opinions, recorded once and out of the way; the design-system pass decides.

- Family A's restraint (hairlines, space, one blue) reads closer to the design rules in
  CLAUDE.md than family B's cards and shadows; if one idiom absorbs the other, A is the
  better survivor.
- On `pathways.html` the legend precedes the picker; the picker is the action and could lead.
- The `.mark` dot-plus-word chip in `style.css` is the strongest status treatment on the site
  and is one vocabulary already; it is the natural replacement for family B's three pill
  systems when the seam is erased.

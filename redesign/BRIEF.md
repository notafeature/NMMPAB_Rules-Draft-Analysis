# Site overhaul brief

Written July 26, 2026, on the branch `claude/site-design-ux-overhaul-qazxu1`. This is the redesign session that `analysis/site-redesign-notes.md` reserved. It states the purpose, the diagnosis, the verdict on rebuilding, the new structure, the design system, and the sequence. The two HTML files beside it are a working probe of the design, not the migration.

## 1. Purpose

One paragraph, to be refined and then written once, in one place:

> The working reference for New Mexico's medical psilocybin Training and Education rulemaking, 7.35.3 NMAC. It exists so that the people shaping the rule, board and committee members, department staff, people preparing to comment at the August 28 hearing, and prospective providers, can see the current state of the text, what is still open, what changed, and the sourced record behind every claim, faster than any other route. Accuracy is the product. Neutrality is the method. Every claim carries a citation; everything verbatim is verbatim.

What it is not: a public-health explainer, an advocacy site, or a patient-facing service. One signpost sentence routes patients to what governs them; nothing else on the site is written for them.

The repository currently states two different purposes. `README.md` describes a plain-language reference "for anyone"; `UPDATING.md` describes a working tool for the people running the rulemaking. The July 25 correction in `analysis/site-redesign-notes.md` resolved this in favor of the working tool, and the site's pages have not caught up with that decision. The paragraph above is the working-tool purpose, stated once. When it is agreed, `README.md`, `about.html`, and the site lede all derive from it.

A clock runs on this purpose. Until August 28 the site's first job is the hearing: the deferred practicum recommendation reaching the department, and readers arriving to understand what is proposed and how to comment. After the hearing the rule finalizes and the site's center of gravity shifts to the record. The design has to serve the first job now without being disposable after it.

## 2. Who arrives, and the question each one carries

From `analysis/site-redesign-notes.md`, held: nobody in this audience needs the process explained from first principles, and none of them will read a page that explains itself before it says anything.

| Reader | First question | Target |
|---|---|---|
| Committee or board member | What is open, and what am I being asked to decide | Answered on the first screen of the front page |
| Department staff | What exactly is proposed against what was published | One click: the practicum workspace |
| Hearing commenter | What is proposed, where the problems are, how to comment | One click: comment page, hearing surface |
| Training provider, prospective permittee | What will be required of me, does what I hold count | One click: requirements, then their role |

## 3. Diagnosis

The full page-by-page audit is in the session record; the numbers that matter:

1. **The chrome never drifted. The prose did.** Nav, footer, provenance, and beacon are byte-identical on all 13 pages because three sync tools own them. Meanwhile the 7-0 deferral vote is hand-maintained on 9 pages, the Metz recommendations on 5, the hearing date on 11, and one public comment is pasted verbatim in two places. Everything a tool owns stayed correct; everything hand-copied drifted. That is the whole mechanism behind "update one section and not the rest," and it points directly at the fix.
2. **There is a design language but no design system.** 2,124 lines of CSS across 13 pages; 889 distinct declarations; 68 shared by all pages; 75 percent exist on exactly one page. `index.html` and `hours.html` are two forks of one stylesheet, diverged by a few pixels. `about.html` and `documents.html` are byte-identical clones. Every page looks the same because one card pattern is reused everywhere, and no page can look intentionally different because nothing is shared below the token layer.
3. **Names disagree at every layer.** Page titles use four different site suffixes. The front page has three names: the title says "The Published Rule," the H1 says the hearing date, the nav says "Where things stand." `deferred.html` is titled "Practicum requirements." `history.html` is titled "Recent developments" and labeled "History." A reader who clicks a label and lands on a different name has to re-orient on every navigation.
4. **Structure follows the filing cabinet, not the reader.** Thirteen pages under four dropdown groups, where six "Requirements" items are four projections of one underlying model: license in, permit out, hours per role, specialization on top. The site's own notes already made this diagnosis on July 25; the page count has grown since.
5. **Walls of text are a template problem, not a writing problem.** The prose itself is mostly disciplined. But `hours.html` stacks seven text blocks before its first content, runs 10,282 pixels tall at desktop width, and numbers its sections 2, 1, 3, 4, 5, 6 in that order. There are zero images, zero SVG, zero diagrams on the entire site; every visual distinction on the site is a colored text pill.
6. **The date stamp carries no signal.** Twelve of thirteen pages say "Updated July 25, 2026," so the stamp cannot tell a reader what actually changed, while `input.html` still says the committee "meets this afternoon," nine days after the afternoon in question.

## 4. Verdict: rebuild the shell, keep the content

Ground-up is the wrong move for the content and the right move for everything around it.

The content is the site's irreplaceable asset: verbatim quotes verified fragment by fragment, citations to subsection and page, a walkable document chain. The defect sweep of July 26 shows exactly what re-transcription costs; quotes that had been retyped drifted from the source in eight places on one page. Rebuilding pages from scratch re-runs that risk across the whole site for no reader benefit.

The shell has already proven which architecture works. The three sync tools kept their surfaces byte-identical through six weeks of parallel sessions while every hand-maintained fact drifted. So the overhaul is: **expand what the tools own** (status facts, the stylesheet, page chrome, the checks) **and transplant the verified content into a new structure**, verifying with the existing check suite as it moves. No framework, no build step, no new hosting. GitHub Pages keeps serving static files from `docs/`.

## 5. The new structure

Five destinations, no dropdown taxonomy. Thirteen pages become eight.

| Nav item | Page(s) | Job |
|---|---|---|
| **Now** | `index.html` | The dashboard: what is open, what is settled, the next three dates, what changed most recently. One screen. No quote records. |
| **The rule** | `requirements.html`, `cs-number.html`, `changes.html` | What the published text requires. Requirements by role with a starting-license selector (absorbs `hours`, `eligibility`, `pathways`, `specialization`); the CS number deep-dive; the full section-by-section record. |
| **The practicum fix** | `practicum.html` (today's `deferred.html`, renamed to match its own H1) | The active workspace: every provision a change touches, the defects in the published text, the committee record, the amendment drafts. |
| **The record** | `history.html`, `documents.html`, `about.html` | The dated chain, the document register, the method. |
| **Comment** | `input.html` | Community input, plus a time-boxed "commenting at the August 28 hearing" surface that retires after the hearing. |

What this removes: `guide.html` (a page that exists because the nav failed; the nav now does its job), the `Overview`/`Requirements`/`The record`/`Documents` dropdown grouping, and the duplicated quote records on `index.html`. Old URLs get one-line redirect stubs, because links to them are already in circulation.

The merge that matters: `hours`, `eligibility`, `pathways`, and `specialization` are one page. A reader picks a role or a starting license and sees the hours, the qualifying licenses, the route, and the specialization layer in one place, statically rendered for every role so nothing depends on JavaScript and browser find works. This kills the largest duplication cluster, the most JS-fragile page, and the "which page has my answer" problem in one operation.

Ownership stays the rule: a fact lives on exactly one page, and other pages link to it. The ownership table in `UPDATING.md` gets rewritten to the eight pages.

## 6. The design system

One stylesheet, `docs/site.css`, owned like the nav is owned. Per-page style blocks shrink to what is genuinely page-specific, with a target under 40 lines. The system in five decisions:

1. **Type carries epistemology.** Serif (Charter) is reserved for verbatim material: rule text and transcript quotes, always on a tinted ground with a citation. Everything in the site's own voice is the system sans stack. Mono is for dates, section numbers, and file names only. The site's core promise, what is the document versus what is us, becomes visible at a glance instead of being a footnote on the about page.
2. **Status is one vocabulary, five states, defined once.** Open (red), In committee (amber), Settled (green), Defect in published text (red outline), Record (slate). Same chips, same colors, everywhere a status appears: cards, tables, the timeline. Never color alone; the chip always carries its word. The current site has the vocabulary but redefines and restyles it per page.
3. **Four page templates, visibly different.** Dashboard (Now), Reference (the rule pages), Workspace (the practicum fix), Record (history, documents, about). Each has its own hero treatment and rhythm, so a reader knows what kind of page they are on before reading a word. "Everything looks the same" is the cost of one card pattern doing every job.
4. **Diagrams are the imagery.** Photos would be wrong for a records site; the absence of any graphic at all is also wrong. Inline SVG in one consistent style: the process pipeline (recommendation to draft to published rule to hearing to final) on Now and the record; the hours chart (published against proposed, by role) on requirements; the route map on requirements; a provision-dependency strip on the workspace. The chart palette is validated for color-vision deficiency and contrast (#5B3FA8, #1D8A6F, #A5690E on the paper ground).
5. **Density discipline as template law.** A hero is eyebrow, H1, one-sentence lede, and a dated stamp; nothing else. Every section leads with its point in two paragraphs or fewer before a structured element. Full records collapse by default with counts visible on the summary line. The per-page "Updated" stamp only changes when the page's content changes, so it means something again.

## 7. The maintenance model

The drift fix is to make the tools own more:

- **`tools/sync-status.py`**, new, modeled on `sync-nav.py`. One `STATUS` dict holds each item's state, date, one-line summary, and the next three dates. It writes the marked status blocks on every page that shows status. The nine-page drift class disappears the way nav drift did.
- **`tools/check.py`**, new, one entry point that runs everything: the existing parse, nested-anchor, em-dash, unstyled-class, and link checks; `check-citations.py` from the July 26 defect-sweep branch; a name-spelling check against the corrected list (Metz, Zurlo, Peskuski, Leeman, Dezbaá, Wong, Hawk); a title-equals-H1-equals-nav-label check; and a live-blog-tense check that greps site prose for "today," "this morning," and "this afternoon" outside quoted material. That trap has now bitten twice; it should be a check, not a memory.
- **The stylesheet is synced, not copied.** `site.css` is one file; pages link it. The unstyled-class check already catches content moved without its styles.

## 8. Sequence

The clock: Advisory Board August 14, Training and Education Committee August 21, rule hearing August 28. The amendments package is the near-term deliverable and nothing here may block content updates, so the overhaul ships in merge-sized slices, each leaving the site whole.

0. **First, the stranded work** (owner merges; found July 26): the `claude/site-defect-sweep` branch (accuracy corrections across 10 pages plus the citation checker; verified clean; no pull request was ever opened for it), a decision on `claude/nmmpab-rules-analysis-17khvs` (the `amendments-remainder/` package), and restoring the full July 16 EOL source document, of which `main` holds only the addendum. The redesign builds on corrected content or it re-fixes those errors by hand.
1. **Foundation.** `site.css`, `sync-status.py`, the four templates, the five-item nav, `check.py`. Rebuild `index.html` on the Dashboard template as proof. One pull request.
2. **The merge.** `requirements.html` absorbs hours, eligibility, pathways, and specialization; redirect stubs at the old names; `practicum.html` rename absorbs the committee record from `hours.html`. One pull request.
3. **The record and the comment surface.** History, documents, about on the Record template; the hearing surface on the comment page. One pull request.
4. **Diagrams and polish.** The pipeline, the chart, the route map; the naming pass that makes title, H1, nav label, and filename agree everywhere, enforced by the new check.

## 9. Open decisions

1. The purpose paragraph in section 1: adopt, or edit before it propagates to README, about, and the ledes.
2. The five-item nav and the four-page merge in section 5: the largest structural call in this brief.
3. `guide.html`: this brief deletes it. Its six map cards move to a "what is on this site" section at the foot of Now.
4. The serif-for-verbatim rule in section 6: it changes the site's look at every heading, which is the point, but it is a look change the owner should see in the probe before it ships.
5. The hearing surface on the comment page: scope and wording, given the department's own comment channels.
6. Whether `amendments-remainder/` merges now or waits; it is finished work sitting on an unmerged branch with no pull request.

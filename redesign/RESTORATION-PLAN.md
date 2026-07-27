# Restoration plan

The redesign merged on July 27, 2026 removed working instruments the site existed to provide. This file is the plan for putting them back. The governing decision: function returns first, verbatim, in the original design of each instrument. Visual harmonization with the redesign chrome is a separate, optional, final phase, judged by the owner. Nothing waits on that judgment except that phase.

The feature ledger behind this plan: the pre-redesign site had three site-wide systems (citation disclosure, error reporting, progressive disclosure) and about fourteen instruments. The redesign kept five instruments, buried or orphaned three of those, and added one new instrument. Every removed page is intact at commit `4d8561d` and every retired address still resolves through a redirect stub.

## Phase 1. The instruments return

Restore from `4d8561d`, replacing the redirect stubs, with only these changes: repair links that now point at moved content (the old hours page content lives at `training-hours-record.html`), update the small number of statements that events since made false (the committee recommendation was submitted July 27), and satisfy `check-site.py`. No redesign of these pages.

1. `pathways.html`: the routes instrument. Five starting-license profiles, the three-permit verdict matrix, the drawn journey, the per-permit step lists with settled and open flags and citations.
2. `deferred.html`: the practicum blast radius. Thirteen provisions a practicum change touches.
3. `specialization.html`: the specialized-domain layer, including the proposed hour figures.

Done means: all three pages live, their internal links resolve, their facts are current, the checker passes.

## Phase 2. The content blocks return to their right places

Ported into the redesign pages that are their correct homes, in the redesign's own idiom.

4. The gaps register ("documents this site does not have," with the consequence each gap causes) into `record.html`, beside the held-documents register. The send-a-document line points at the comment form.
5. The community input log (received submissions and public comment, de-identified by default) into `comment.html`, below the form.
6. The verification tier ladder into `about.html`, opening the Method section.
7. The site directory (every page, one plain sentence each) onto `index.html` at `#directory`; `guide.html` redirects there.
8. Record depth: the chain entries on `record.html` recover the substance the old `history.html` carried per event.

Done means: each block is on its page with its old substance, sourced as before.

## Phase 3. Reintegration

9. Navigation on the redesign pages becomes: Overview, The rule, Pathways, Recommendation, Hours, Record, Comment, About. Identical on every redesign page.
10. `eligibility.html` is linked from `pathways.html` and the directory, ending its orphanhood. Every retained page is reachable from the nav or the directory.
11. `check-site.py` gains two checks: every page in `docs/` must be reachable from the nav or the directory, and every redirect stub's target must contain the promised anchor.
12. The citation disclosure system returns to the redesign pages: citations open on hover, close on leave, click opens the source in a new tab, plain links without JavaScript. This is function 4 of the site specification and the redesign pages currently do not meet it.

Done means: no orphaned page, the checker enforces it, the redesign pages meet function 4.

## Phase 4. Owner judgment, later

Not executed without the owner.

- Visual harmonization of the three restored instruments with the redesign chrome, page by page, owner approving each.
- The citation redundancy review (repeated identical links to the same PDF within one page).
- Whether `history.html` and `documents.html` return as standalone pages or stay folded into `record.html`.

## Dropped by owner decision

- Error reporting as a per-page widget. Feedback goes through the comment form.

## Standing constraints that bind this work

The summary of the recommended rules stays out of the repository. No em dashes. Verbatim means verbatim. Branch and pull request, never a push to main. The full rules are in `CLAUDE.md`.

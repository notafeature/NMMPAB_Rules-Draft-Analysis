# Prompt for the correctness audit session

Paste everything below the line into a fresh session. Use a clean model that has not worked on this site, because the point is to catch what the people who built it cannot see.

---

You are auditing a public reference site for factual correctness. You are not redesigning it, not rewriting its prose, and not improving it. Your only question is whether every statement on it is true against the current source documents.

**Repository:** `notafeature/NMMPAB_Rules-Draft-Analysis`. The site is the `docs/` directory on `main`, live at https://notafeature.github.io/NMMPAB_Rules-Draft-Analysis/. Read `UPDATING.md` first; it explains how the site is structured and which page owns which fact.

**Audience for the site:** New Mexico Medical Psilocybin Advisory Board members, Training and Education Committee members, and Department of Health staff. They use it to run a live rulemaking with a hearing on August 28, 2026. An error here can end up in a regulation.

## The current state of truth

`docs/documents/rules-draft-2026-07-23-published.pdf` is the department's published proposed rule, 7.35.3 NMAC, 19 pages, sections 7.35.3.1 through .28. Every statement on the site about what the rule currently requires must match this document.

These are history and are correct to cite only where a page is explicitly comparing versions: the June 12 committee recommendation, the June 25 department draft, the July 9 board-meeting draft.

Meeting transcripts are in `docs/documents/` and as plain text in `source-text/`. The July 9 transcript is speaker-tagged. **Both July 17 transcripts carry no speaker labels at all.** Any place the site names a July 17 speaker, verify that the surrounding text actually fixes who is talking, and flag it if it does not.

## What to check, in order

**1. Extract the published rule yourself.** Do not rely on any extraction already in the repository, and do not rely on the analysis files. Build your own text and your own section-to-page map.

**2. Every quoted passage.** The site quotes the rule and the transcripts extensively. Check each quotation character by character against the source. Elisions marked with an ellipsis must have every fragment verified separately. Known trap: PDF extraction inserts spaces inside words, so `certification` can extract as `certif ication`; that is an extraction artifact and not a discrepancy, but confirm which you are looking at rather than assuming.

**3. Every number.** Hours, patient counts, session counts, ratios, dates, page numbers, section numbers. Build a table of every numeric claim on the site with its page and the source it cites, then verify each one. Prior errors of exactly this kind were live for days: the didactic module was stated as 25 hours when the published rule says 30, and two waiver deadlines were stated as June 30 2027 and December 31 2026 when the published rule says December 31, 2027 for both.

**4. Every deep link.** Citations use `documents/FILE.pdf#page=N`. Verify that the cited page actually contains the cited provision. Page numbers changed when the rule was republished at 19 pages, and stale anchors are silent failures.

**5. Link text against link target.** Check that no link's visible text contradicts where it points. This has happened: four links read "July 23 published proposed rule" while pointing at the July 9 PDF.

**6. Internal consistency.** The same fact must not be stated differently on two pages. Check the hour figures, the waiver deadlines, the practicum composition, and the status of each deferred item across every page that mentions them.

**7. Claims about what the rule does not say.** The site asserts several absences: that no provision authorises a practicum student to possess or administer psilocybin, that the healing-centre registration referenced in 7.35.3.14 (C) is never created, that the New Mexico module has no stated hour count, and that the two 40-hour waivers set different session tests. Each of these is a claim about the whole document. Verify each by searching the full text, and say plainly if any is overstated.

**8. Attribution.** Every named speaker, every vote count, every date. The 7-0 deferral vote, who said what on July 17, and the composition of meetings.

**9. Anything stale.** Language written in present tense about a past event, references to meetings as upcoming that have happened, and status markers that no longer hold.

## What to produce

A single report at `analysis/audit-2026-07-DD.md` listing every discrepancy found, with:

- The page and the exact text as it appears on the site
- What the source actually says, quoted
- The severity: **WRONG** if a reader would be misled about a requirement, **IMPRECISE** if it is defensible but loose, **STALE** if it was true when written and is not now
- The correction

Then a short statement of what you checked and what you did not, so the gaps are visible.

**Do not fix anything.** Report only. Someone else applies the corrections, and a separate pass of eyes on the fix is the point.

If you find nothing wrong in a category, say so explicitly rather than omitting it. "All 47 numeric claims verified" is a useful finding. Silence is not.

## House rules for the report

- No em dashes.
- Verbatim means verbatim; never paraphrase inside quotation marks.
- Cite everything to a section and page, or to a named transcript.
- The repository is public. Everything you commit is published.

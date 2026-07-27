# Copy audit of the live pages, July 26, 2026

Produced by a delegated session against the writing standard on the `claude/updating-map-rewrite` branch and the owner's eight rules, recorded here so the rewrite work has a checklist. Names inside quoted site text follow the live pages as they stand; two attributions (Kate Hawke, Amy Wong-Hope) are pending independent re-verification against the transcripts, which read Kate Hawk and Amy Wong.

## The three habits to break, site-wide

1. Compression into fragments. Nearly every page opens with a verbless lede, and the analytical pages land findings as punch lines ("No certified locations, no practicum"). The facts are right; the delivery is headline rhythm. The fix is almost always to give the fragment its subject and verb.
2. Urgency and engagement residue. "Needs to reach the department as soon as possible" in bold, "Why now.", "New to this?", "meets this afternoon". The urgent sentences are the ones that went stale and are now factually wrong; the plain dated sentences beside them aged correctly.
3. Insider shorthand. "Dom", "Jenn", "the register changes", "the full stack", "walkable", a June 25 committee meeting called a "hearing", and three uses of "amendment"/"amending". Every one assumes a reader already inside the project.

## Violations by page, worst first

1. input.html: stale urgency in the lede and context block ("meets this afternoon", twice); H1 "Send what the rule-writers should see" is a pitch and a coinage; "Why now." heading; a source line citing the July 9 transcript for July 17 facts; the lede's claim restated verbatim mid-page.
2. index.html: "needs to reach the department as soon as possible" in bold; "New to this?" hook; the recommendation-in-progress fact stated three times on one page.
3. deferred.html: four-word punch lines ("No certified locations, no practicum"; "Same 40 hours, different session test"); "Amending 19(G)" uses the banned word; three passages recommend outcomes, which about.html promises the site never does.
4. documents.html: "it is what it is"; a verdict heading ("...and the difference matters"); second-person instructions.
5. hours.html: "the full stack"; "In short:" restatement; "despite the Advisory Board voting 7-0" editorializes; fragment position summaries; the numbered sections render out of order (2 before 1).
6. pathways.html: June 25 called a "hearing" twice; "Dr. Ann Metz" against "Dr. Anne Metz" in the same file.
7. cs-number.html: two uses of "amendment" (statutory context, still banned); "Denali" first-name-only; otherwise the strongest page on the site.
8. specialization.html: "Below this line the register changes"; first-name attributions (Dom, Jenn, Jamie, Christine); "Space Attendant" never defined.
9. eligibility.html: same "register changes" line; "stays untestable-out-of" is not a phrase a person would speak.
10. changes.html: "kept so the chain stays walkable"; "Dr. Ann Metz" three times; first-name-only rows in the agreements tables; published to-do notes ("verify the spelling against PDF page 5").
11. history.html: fragment lede; "A neutral, dated record" grades its own work.
12. about.html: "Read this before relying on anything here" as a heading; "Strongest tier." fragment.
13. guide.html: "Eleven pages" on a thirteen-page site; H1 "What is on this site" followed immediately by H2 "What's on this site".

Site-wide: zero em dashes, zero uses of "docket". The provenance blocks that every page carries include generated aphorisms ("a page that needs instructions for reading it has already failed"); the fix belongs in tools/sync-provenance.py, which owns those blocks.

## Sample rewrite

The delegated session produced a full before-and-after rewrite of input.html, the worst page. It is held in the session record and applies once the container for that page is settled; the rewrite drops both stale "this afternoon" sentences, retitles the H1 to "Community input", corrects the transcript citation to July 9 and July 17, and removes the duplicated how-this-is-used sentences.

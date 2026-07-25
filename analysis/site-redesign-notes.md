# Site redesign: running notes

A brief that accumulates. The redesign is its own session; this file exists so nothing observed along the way gets lost before then.

Standing instruction: **nothing needs to stay the same.** The content is all there. The job is to make it usable. The time budget is explicitly not half a day, so the design has to be decisive rather than exploratory.

## The core diagnosis

The site is organized by **document structure**. It should be organized by **what a reader came to find out**.

Nine pages map roughly one-to-one onto the shape of the source material: a page for the draft, a page for the hours, a page for the history. That is how the material is filed, not how anyone arrives. Depth is present and unreachable.

## The writing standard, stated by the owner

Quote it directly, because it is the clearest statement of the bar:

> "This is not a fucking propaganda doc. This is not the news. This is not hyperbole. Just fucking make it clear."

> "We're not trying to get clicks. We want to say exactly what the current version of truth is."

> "Everything needs to hold the weight of its presence."

> "Assume nobody has ever been here and write and make the page so clear that you don't have to say what it is."

Concrete failures of that standard, all currently live:

- **"The rule is published"** as an index subtitle. That is a headline, not a statement of truth. The truth is: the rule hearing is scheduled for August 28. Say that and nothing else.
- **"The dated chain that produced the published rule, newest first: every meeting, vote, and document, each one sourced."** Too pleased with itself. Say what the page is.
- **"New here? How this process works."** Drop "New here?". Nobody should have to self-identify as a novice to get an explanation.
- **"Earlier layer, 104 provisions."** Means nothing to a reader. Does not describe what the section contains or why it exists.
- **"Purpose and how to read this page."** If a page needs instructions for reading it, the page has failed. Not against instructions in principle; against them in this form.

## Specific defects, page by page

### index.html

The whole page needs reconsidering. Owner: "Every single part of this entire page needs to be reconsidered."

1. **Title and subtitle misrepresent.** Replace with the plain fact: the rule hearing is scheduled for August 28.
2. **Must state the urgency, on the practicum hours section:** it is imperative that the deferred recommendation on practicum hours be submitted as soon as possible.
3. **The open-item highlight must be red, not purple.** Asked for twice. Purple is the site accent and reads as decoration; red reads as attention.
4. **Move "What is next" to the top,** directly under the opening paragraph and **above** "Where things stand". The roadmap belongs at the top.
5. **"Nothing on this page is final" belongs in the footer.** There is no real footer; build one.
6. **The context strip has no definition of what it is.** A reader hits a tile with no framing.
7. **Broken tile, fixed July 25:** an `<a>` was nested inside another `<a>`, which is invalid HTML. Browsers hoist the inner link out and shatter the layout, which is what the owner screenshotted. A nested-anchor check now runs across all pages. Note the general lesson: the HTML parser check passes on content-model violations, so it is not sufficient on its own.
8. **The "recommendations" tile has no reason to be there.** Remove or justify.
9. **"Find your way around this site" should be its own page**, not a section of the overview.
10. **The three lineage deep-dives** (CS number, practicum, reciprocity) are historical and do not belong on the overview.

Open question for the redesign: what actually belongs on an overview page, and which new pages absorb what comes off it.

### hours.html

11. **Remove "Purpose and how to read this page."** See the writing standard above.
12. **Role tiles should be three:** certifying clinician, practitioner, facilitator.
13. **Under practitioner, show Dr. Anne Metz's proposed alternative title as a parenthetical subtitle.** Her recommendation is to retitle "practitioner" as "licensed provider"; her argument is that "practitioner" is unspecific, colliding with nurse practitioner and, in the Medicaid rule, covering everyone from nursing assistant upward. Note: this is being carried as a **separate** recommendation from the practicum redline, so that it can be dropped without affecting the rest.
14. **"What changed on July 23" needs specific subsection references, not just links.** Example given: "the practicum cannot begin" must state which subsection that language is in. A link off to the side may not be seen.
15. **Everything needs specific reference.** This generalizes past this page.

### history.html

16. **Rewrite the lede.** See above.
17. **Drop "New here?"** from the process explainer.
18. **Sources must link.** External sources link out normally. For **internal** references, taking the reader off the page is the wrong move: consider a hover or click popover that shows the referenced block inline and dismisses on click-away. Owner flagged this as possibly redesign-scope.

### changes.html

19. **Improve the formatting of the provision column.**
20. **Make "Change from July 9" collapsible** so it is not in the way.
21. **State clearly and early that these are the provisions deferred to the committee.** It is stated, but it took too long to find.
22. **"Earlier layer, 104 provisions" is meaningless.** Retitle, and make the section explain its own value.
23. **The June 12 against July 9 comparison is not wanted as a standalone section.** That history exists elsewhere. Owner: "I don't care about exposing the difference between July 9th and June 12th."
24. **What is wanted instead: three columns, collapsible, per provision.**
    - June 12 recommendation
    - July 9 draft
    - July 23 published
    Format is an open design problem. The point is a reader can see one provision's whole life at a glance and collapse what they do not need.

## Who arrives, and what they want

To be sharpened before layout work:

1. **A prospective facilitator or practitioner.** "What do I have to do, how many hours, what does it cost, does my license shorten it?" Wants a path, not a rule.
2. **A student or someone trained elsewhere.** "Does what I already did count?" Wants reciprocity answered as a decision.
3. **A committee or board member.** "What changed, what is still open?" Wants a diff and a status, fast.
4. **A patient or family member.** "Can I get this, from whom, when?" Almost nothing on the site serves this person.
5. **Someone preparing to comment at the hearing.** "What is proposed, where do I object, how?" Time-boxed and specific.

Readers 2, 4 and 5 are underserved.

## What the redesign must preserve

- Facts only on public pages: dated events and attributed quotes. No characterization.
- Every current-state claim cites the published rule with a section and page.
- No em dashes.
- Identical nav, footer and provenance on every page. Enforced by `tools/sync-nav.py` and `tools/sync-provenance.py`.
- Unofficial sources labelled unofficial, including the difference between the speaker-tagged July 9 transcript and the unattributed July 17 transcripts.
- The document chain stays walkable: June 12, June 25, July 9, July 23.

## Ideas to evaluate, not yet decided

- **An hours comparison chart** as the centerpiece: role by state by draft version. Currently paragraphs; inherently a chart.
- **A "what applies to me" entry** selecting on starting license, routing to a subset rather than presenting everything. `pathways.html` gestures at this and could become the front door.
- **Status chips** so "settled", "open" and "deferred but published" are scannable.
- **A real footer**, which the site does not have, to hold the disclaimers currently sitting mid-page.
- **A hearing surface** for reader 5 that is time-boxed and retires after August 28.
- **Inline popovers for internal references**, per item 18.

## Sequencing

Content correctness came first and is done: all ten pages are current to the July 23 published rule as of July 25. The redesign is the next body of work and has not started.

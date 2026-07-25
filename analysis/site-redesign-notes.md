# Site redesign: running notes

A brief that accumulates. The redesign is its own session; this file exists so nothing observed along the way gets lost before then.

Standing instruction: **nothing needs to stay the same.** The content is all there. The job is to make it usable. The time budget is explicitly not half a day, so the design has to be decisive rather than exploratory.

## The core diagnosis

The site is organized by **document structure**. It should be organized by **what a reader came to find out**.

Nine pages map roughly one-to-one onto the shape of the source material: a page for the draft, a page for the hours, a page for the history. That is how the material is filed, not how anyone arrives. Depth is present and unreachable.

## The writing standard

The prose has to earn its place. Concretely, that means the following.

**Write in complete sentences, or write an actual list.** A list rendered as prose is neither. Sentence fragments strung together for rhythm, four or five words at a time, are a tic rather than a style, and they make a page harder to read rather than punchier.

**Every element introduces itself.** A reader arriving cold at any section should learn from the section what it is and why it exists. A heading that names a thing without explaining it, such as "Earlier layer, 104 provisions", fails this test. So does a section that needs a companion note explaining how to read it: if a page requires instructions, the page is the problem.

**Be specific rather than gestural.** Cite the subsection, not just the document. Name the figure, not just the fact that it changed. A link placed off to the side does not substitute for stating in the sentence which provision is being discussed.

**Assume the reader is intelligent and has never been here before.** These are compatible. It means explaining the thing without flattering the reader, and without labels like "New here?" that ask someone to self-identify as a novice before they are allowed an explanation.

**Cut anything that is only there for effect.** No headline energy, no hyperbole, no rhetorical framing. The site is a record, and its persuasive force comes entirely from being accurate and legible. Live examples that failed this and have been fixed or logged: "The rule is published" as a subtitle, and "the dated chain that produced the published rule, newest first: every meeting, vote, and document, each one sourced."

**Say what is true now, plainly.** For the index that meant replacing a headline with the fact that the rule hearing is scheduled for August 28.

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

## Four decisions taken on July 25

**The recommendation must read as an origin, not as a live document.** Committee members found it genuinely hard to grasp that the recommendation became the rules draft and no longer exists as a separate thing anyone can act on. Wherever the recommendation appears beside draft text it should be visually lighter: a summary, an expander, or a link, rather than equal weight with the operative rule. The distinction to carry is "this is what the committee proposed" against "this is what the rule says".

**Links must not take a reader away from what they are reading.** External links open in a new tab. Internal references should ideally open as a popover on desktop, showing the referenced block in place and dismissing on click away. The mobile equivalent is unresolved.

**Mobile is deferred to the redesign.** Build for desktop and make it robust there. A serious answer for narrow screens is a separate problem, and guessing at it now would compromise the desktop layout without solving the mobile one.

**The whole of Part 3 needs a home, but the deferred set needs its own.** The complete twenty-eight section rule has to be recorded somewhere. The provisions under active review, meaning the deferred practicum and didactic requirements, need a contained page of their own so a reader is not navigating around everything else to follow them. This produced `deferred.html` on July 25.

## A private analytics view

Wanted: a dashboard, visible only to the site owner, showing traffic to these pages. The specific question it needs to answer is whether the Department of Health is reading the site, which matters because nobody has sent it to them and that is a deliberate choice for now.

Design constraints that follow from the site's own commitments: it should not track individuals, and it should not add third-party scripts to public pages that would compromise the privacy of people reading about their own healthcare. A server-side or log-based approach fits the site better than an embedded analytics tag. GitHub Pages does not expose logs, so this likely means either a lightweight self-hosted collector or moving the site behind something that does.

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

# Site redesign: running notes

A brief that accumulates. Not a plan yet. The redesign is its own session; this file exists so that nothing observed along the way gets lost before then.

Standing instruction: **nothing needs to stay the same.** The content is all there. The job is to make it usable. Time budget is explicitly not half a day, so the design has to be decisive rather than exploratory.

## The core diagnosis

The site is organized by **document structure**. It should be organized by **what a reader came to find out**.

Nine pages currently map roughly one-to-one onto the shape of the source material: a page for the draft, a page for the hours, a page for the history, a page for the CS number. That is how the material is filed, not how anyone arrives. The result is that depth is present and unreachable: readers do not utilize it because they cannot find the part that applies to them, and every page opens onto a wall of prose.

Restating the same point in the owner's words: it is "a very useful but like wall-of-text," and "people are not utilizing the depth of it because it's just too much."

## Who arrives, and what they actually want

Rough cut, to be sharpened before any layout work:

1. **A prospective facilitator or practitioner.** "What do I personally have to do, how many hours, how much will it cost, and does my existing license shorten it?" Wants a path, not a rule.
2. **A current student or someone mid-training elsewhere.** "Does what I already did count? What about my Oregon or Colorado hours?" Wants reciprocity and waiver logic, answered as a decision, not as prose.
3. **A committee or board member.** "What changed since I last looked, and what is still open?" Wants a diff and a status, fast.
4. **A patient or family member.** "Can I get this, from whom, and when?" Almost nothing on the site currently serves this person.
5. **Someone preparing to comment at the hearing.** "What is actually being proposed, where do I object, and how?" Time-boxed and specific.

Most current pages serve reader 3 and partially serve reader 1. Readers 2, 4, and 5 are underserved.

## Specific defects observed so far

**history.html**
- A "how this process works" explainer sits in the middle of the chronology. A process explainer inside a timeline is a structural mistake, not a copy problem: it interrupts the one thing a chronology is for. Pull it out into its own surface.
- Reads as "updated, not reviewed." Entries were appended without anyone re-reading the whole.
- Missing the full July sequence: the July 17 board meeting and its 7-0 deferral vote, the July 17 committee meeting and summary, the July 23 publication, the August 28 hearing, and the August 14 and August 21 meetings.

**changes.html**
- Needs a prominent summary box at the top covering the practicum and training definitions, linking down to each, and showing what carried over versus what changed. Currently a reader must scan 104 entries to learn what they came for.
- Needs to carry the July 17 to July 23 comparison, not only the June to July one. See `july17-to-july23-state-diff.md`.

**Global**
- Every page opens with prose. None opens with an answer.
- Numbers that matter (25 to 30, 100, 120, 84, 62, 72) are buried in sentences. They should be legible at a glance and comparable across states.
- No visual representation anywhere of the one thing the whole site is about: a set of hour requirements that differ by role, by state, and by draft version. This is inherently a chart, and it is currently paragraphs.
- Citations are good and should survive. Every page anchors to a source PDF with a page deep link; that is the site's credibility and must not be traded away for visual polish.

## What the redesign must preserve

Non-negotiable, carried from HANDOFF.md:

- Facts only on public pages: dated events and attributed quotes. No characterization, no synthesized process.
- Every current-state claim cites the published rule with a page deep link.
- No em dashes.
- Identical nav and footer on every page. Now enforced by `tools/sync-nav.py`, which owns both the markup and the script.
- Unofficial sources labeled as unofficial, including the distinction between the speaker-tagged July 9 transcript and the unattributed July 17 transcripts.

## Ideas to evaluate, not yet decided

- **An hours comparison chart** as the site's centerpiece: role by state by draft version. Oregon 120, Colorado 150, New Mexico published 30 didactic plus 100 or 120 practicum, Metz proposal 84 didactic plus 62 or 72 practicum. One picture replaces several pages of prose.
- **A "what applies to me" entry**, selecting on starting license, which routes to the relevant subset rather than presenting everything. `pathways.html` gestures at this already and could become the front door.
- **A change ledger with visible status chips** rather than a long comparison page, so "settled," "open," and "deferred but published anyway" are scannable states.
- **A timeline as an actual timeline**, with the process explainer adjacent rather than embedded.
- **A hearing surface** for reader 5 that is time-boxed and disappears after August 28.

## Sequencing

The redesign happens after the rules work. Getting the record correct is the higher priority, and a redesign layered on top of unsettled content would just produce another layer of sediment.

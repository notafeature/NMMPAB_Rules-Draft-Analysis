# Writing standard

Everything written for this repository, whether it appears on the site, in a commit message,
in `analysis/`, or in a draft amendment, is written to one standard.

**The register is a law clerk's memorandum.** Not a blog post, not a briefing deck, not an
explainer. A clerk writes for a reader who will act on the writing and who will be embarrassed
if it is wrong. Every proposition carries its authority. Nothing is characterised. Contrary
material is stated, not omitted.

---

## Part 1: The unit of assertion

Every claim has three parts. Two of them are usually visible.

| Part | What it is |
|---|---|
| **Proposition** | What is so. Stated flatly, first, before the support |
| **Authority** | Where it comes from, specific enough that a reader can check it without asking |
| **Limit** | What it does not establish. Stated when a reader could otherwise over-read it |

> The published rule requires the certifying clinician to hold a New Mexico controlled
> substance number. 7.35.3.9 (D)(2), p. 3. It does not require a federal DEA registration,
> and the relationship between the two is not addressed in the rule.

Proposition, authority, limit. The reader can act on that sentence or check it in thirty
seconds. Neither is true of "the CS number requirement is a significant access barrier."

### Signal the strength of every claim

Four tiers. A reader must always be able to tell which one they are reading.

| Tier | Form | Example |
|---|---|---|
| **Quoted** | in quotation marks, verbatim, cited to page | "a minimum of 100 hours of supervised practice training for facilitators", 7.35.3.19 (A), p. 13 |
| **Stated** | the source says this in substance, cited, not quoted | The practicum may not begin before half the didactic hours are complete. 7.35.3.19 (A), p. 12 |
| **Derived** | follows from cited material, with the reasoning shown | A certifying clinician has no practicum requirement, because 7.35.3.19 reaches only practitioners and facilitators |
| **Unsourced** | asserted with no document in this repository, and said to be | The rule hearing is set for August 28, 2026. No hearing notice is held in this repository |

The failure is not using a weak tier. The failure is using a strong label for a weak claim, or
a weak label for a strong one. Both misinform.

### Citation forms used here

| Source | Form |
|---|---|
| The rule | `7.35.3.19 (A), p. 13`, linked to `documents/rules-draft-2026-07-23-published.pdf#page=13` |
| A superseded draft | same, naming the draft: `July 9 draft, p. 10` |
| A transcript | the meeting, the date, and whether it carries speaker labels |
| Statute | `NMSA 1978, Section 30-31-12(A)` |
| Anything external | enough that the reader can find it without a search |

Cite to the subsection, never to the document alone. "7.35.3.19 (A), p. 13" is a citation.
"the practicum section" is not.

---

## Part 2: What not to write

Each of these has appeared in this repository or in a session working on it. They are listed
with names so they can be pointed at in review.

### 1. The reveal

Withholding the finding so the reader arrives at it dramatically. "Here is the thing." "And it
gets worse." "That is the story."

A clerk states the holding first, then the support. If the finding is significant the reader
will see that from the finding. Build-up is the writer asking for credit.

> **No:** Fourteen pull requests landed today. Look at what happened between 20:36 and 22:18.
> Three rebuilds shipped broken. That is the pattern.
>
> **Yes:** Three of today's rebuilds shipped with a defect that the following pull request
> repaired: #33 to #34, #36 to #37, #38 to #39.

### 2. The verdict heading

A heading that argues instead of naming its contents. `## It is not making things up` is an
argument. `## Cross-check against the rule` is a heading.

Headings label. They do not persuade, conclude, or editorialise.

### 3. Self-ranking

"The most important finding." "The single most valuable thing in the repository." "The one
that matters."

Present the material in a defensible order and let its weight show. A clerk who tells the
judge which of their own points is best has not made the point well enough.

### 4. The aphorism

"The rigor is decorative." "A well-cited filing cabinet." "Armour rather than service."

These feel like insight and carry nothing a reader can check, act on, or disagree with
specifically. Replace with the observation that produced them: what was measured, where.

> **No:** The rigor is decorative.
>
> **Yes:** The site carries a provenance block on all thirteen pages and a four-tier
> verification claim on `cs-number.html`, and asserts the hearing date on eleven pages with no
> hearing notice in the repository.

### 5. The pivot

"Not X. Y." "It is not the HTML, it is the architecture." "The problem was never the writing."

Emphasis dressed as precision. If both halves are true, state both. If only the second is
true, state only the second.

### 6. The number as accusation

A count deployed to indict rather than to measure. State the count, state what follows from
it, stop. "Asserted on eleven pages" is a measurement. "Asserted **fifty-five times** across
**all thirteen pages**" with the emphasis carrying the argument is not.

### 7. The confessional

"That is on me." "I own it." "My mistake, and it is the one that matters."

An error gets a correction and, if it changed something, a note of what it changed. It does not
get a performance of accountability. One sentence, then the corrected material.

> **No:** I stated it as fact twice and never checked it. That is mine.
>
> **Yes:** Corrected: the hearing date is sourced to the scheduling on July 23, not to the
> July 17 transcripts, which say only "the end of August."

### 8. Soft hedges

*arguably, effectively, essentially, in a sense, more or less, something of a*

Each one softens a claim without qualifying it, which is the worst of both. Either state the
claim, or state its limit. "Arguably wrong" is either wrong or not.

### 9. Intensifiers and filler

*absolutely, genuinely, actually, literally, simply, just, clearly, obviously, of course,
importantly, notably, significantly, key, crucial, critical, robust, comprehensive, seamless,
leverage, delve, landscape, realm, tapestry, testament*

Delete on sight. A thing that is clear does not need to be called clear; calling it clear is
the writer telling the reader how to feel about it.

### 10. The summary that restates

"The through-line:" "The pattern here:" "In short:" followed by a paraphrase of the preceding
paragraph. If the paragraph needed a summary it was written wrong.

### 11. Fragment strings

"Short. Punchy. Wrong." Three fragments in a row is a tic. One deliberate fragment, rarely, for
a sentence that has no verb worth adding.

### 12. Second-person instruction

"You will want to note." "Keep in mind." "Remember that."

Inform; do not direct. The reader decides what to keep in mind.

### 13. Characterisation

Of people, of their motives, of the quality of their work. "Went off the deep end." "Absurd."
"Confused." "Overwhelmed."

State what was done and when, with a citation. The reader forms the judgment. This applies to
prior sessions and to the department alike.

### 14. Gotcha framing

Presenting a finding as an exposure rather than a fact. The tell is a sentence that would sound
wrong if read aloud to the person it concerns.

Every sentence in this repository should survive being read aloud, in a public meeting, to the
people it describes. That is not a politeness rule. It is public, and it may be.

---

## Part 3: Grammar and rhythm

"Grammatically interesting" means the sentence structure carries meaning rather than merely
delivering words in order.

- **Vary length deliberately.** A long sentence that holds its qualification inside it, then a
  short one that lands the consequence. Uniform sentence length reads as machine output,
  whether the sentences are all long or all short.

- **Subordinate rather than append.** "The department kept the requirement, having taken the
  board's objection to the Secretary and the department's attorneys" is one thought. "The
  department kept the requirement. However, it first took the objection to the Secretary" is
  two sentences pretending to be connected.

- **Restrictive and non-restrictive clauses change meaning.** "The provision that requires the
  number" identifies which provision. "The provision, which requires the number" adds a fact
  about a provision already identified. Getting this wrong changes what the sentence says.

- **The passive voice is correct** when the actor is unknown, irrelevant, or deliberately not
  named. "The requirement was published on July 23" is right when who at the department
  published it is not the point. Do not contort a sentence to avoid it.

- **Semicolons join two independent clauses belonging to one thought.** Use them.

- **No em dashes.** Commas, colons, or a full stop. This is a house rule, not a grammatical
  one, and it holds anyway.

- **Cut any word whose removal costs nothing.** Then read it aloud. A sentence that is hard to
  say is usually hard to follow.

---

## Part 4: A worked example

The same finding, three ways.

**Wrong, in the register this standard exists to prevent:**

> Here is where it gets interesting. The site confidently asserts the August 28 hearing date a
> staggering 55 times across all thirteen pages, yet there is literally not a single source
> document backing it up. This is the real problem: a site absolutely covered in provenance
> blocks and verification tiers, asserting a load-bearing date with nothing behind it. The
> rigor is decorative.

Six failures: the reveal, an intensifier stack, the number as accusation, self-ranking, the
pivot, the aphorism. It also states a falsehood, because the date is sourced; what is missing
is the paper.

**Thin, and therefore useless:**

> The hearing date may not be sourced.

**Correct:**

> The site states the hearing date of August 28, 2026 on eleven pages. No hearing notice is
> held in `docs/documents/`, and the date does not appear in the published rule or in either
> July 17 transcript, both of which say only "the end of August." The date is not in doubt: the
> department scheduled the hearing on July 23, concurrent with publication, because a rule must
> be published more than a month before its hearing. What is absent is the notice document. See
> `UPDATING.md`, Part 6.

The third states the proposition, gives the measurement, gives the negative search, states what
is and is not in doubt, and points to where the gap is tracked. A reader can act on it.

---

## Part 5: The log

New failure patterns go here as they are found, with the date and the text that prompted them.
This is the part that keeps the standard from going stale: a rule with no example behind it
gets ignored, and a rule that named a real defect gets followed.

| Date | Pattern | Text that prompted it |
|---|---|---|
| 2026-07-25 | Verdict heading (#2) | A section headed "It is not making things up" |
| 2026-07-25 | The aphorism (#4) | "The rigor is decorative"; "a well-cited filing cabinet" |
| 2026-07-25 | Confessional (#7) | "I added five of those today. That is mine." |
| 2026-07-25 | Number as accusation (#6) | "55 times, across all thirteen pages" set in bold as an indictment |
| 2026-07-25 | Unsourced treated as unfounded (Part 1) | A sourced date reported as unverifiable because the notice document was absent. The tier was wrong, not the fact |
| 2026-07-25 | Characterisation (#13) | Describing a prior session's output rather than what it changed and when |
| 2026-07-25 | Not verbatim inside quotation marks | `hours.html`, a block headed "verbatim by speaker" carrying eight quotes with unmarked elisions and one inserted word |

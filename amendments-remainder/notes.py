"""Citation and review note for each provision.

Every provision the document reproduces carries a source note. A review
callout enters only for a gap, a contradiction, a typo, or a drafting mistake;
it leads with the question and names who answers it.

Sources are the rule as published July 23, 2026; the prior board-meeting draft
of July 9, 2026; 7.35.2 NMAC as adopted effective June 23, 2026; the Medical
Psilocybin Act; the working redline of Denali Wilson of July 25, 2026, with its
comments; and the July 17, 2026 meeting transcripts.

Quotations are reproduced exactly. `audit.py` harvests every quoted span in this
file and in the addenda of the build script and checks each one against a source,
so a quotation cannot enter unchecked.
"""

SOURCE = {

    # ---- D1. Framework and defined terms ----

    ("7.35.3.7", "Entire section, definitions"):
        "Six definitions are added. Each is drawn from a single provision of the rule as published, and none "
        "is composed. Certificant: 7.35.3.26 NMAC, page 16. Facilitator: 7.35.3.13 NMAC Subsection B, page 8, "
        "with 7.35.3.9 NMAC Subsection F, page 3. Other approved location: 7.35.3.11 NMAC Subsection B, page "
        "6. Practicum: 7.35.3.19 NMAC Subsection A, page 12; that section is the practicum draft's, whose v9 "
        "keeps the defining phrase while amending the hour figures, and Addendum B records the dependency. "
        "Registrant of another approved location: 7.35.3.11 NMAC Subsection B, page 6. Student: 7.35.3.20 "
        "NMAC Paragraph (5) of Subsection H, page 14. As published the section reads in full: &#8220;The "
        "definitions in 7.35.2.7 NMAC apply to this part.&#8221; Amending 7.35.2 NMAC, adopted effective June "
        "23, 2026, is a separate rulemaking, so any term this part needs has to be carried here.",

    # ---- D2. Educational programs ----

    ("7.35.3.10", "Paragraph (2) of Subsection B, documentation of equivalency"):
        "Conforming amendment. Items (a)(ii) and (b)(ii) of 7.35.3.10 NMAC Paragraph (2) of Subsection B, "
        "page 4, require an individual applicant to produce a third-party evaluation of a curriculum. Under "
        "7.35.3.16 NMAC Subsection A, page 10, a third-party evaluation is commissioned by a psilocybin "
        "educational program, not by an individual. Item (c) of the same paragraph already lets an applicant "
        "rely on the list maintained under Subsection A, and this amendment extends that route to items "
        "(a)(ii) and (b)(ii). No figure is added.",

    ("7.35.3.10", "Subsection C, re-application after denial"):
        "Conforming amendment, one of four in the rule. 7.35.3.10 NMAC Subsection C, page 4, reads "
        "&#8220;the applicant may re-apply within six months&#8221;, which on its face sets a deadline. The "
        "next sentence of the same subsection reads &#8220;An applicant who is denied a second time may not "
        "re-apply for six months from the denial&#8221;, which sets a waiting period. The amendment conforms "
        "the first sentence to the second. The same pair appears at 7.35.3.9 NMAC Paragraphs (5) and (6) of "
        "Subsection A, page 2; 7.35.3.11 NMAC Subsection D, page 7; and 7.35.3.12 NMAC Subsection D, page 8. "
        "All four are drafted the same way in this document. No figure is added.",

    ("7.35.3.10", "Paragraph (1) of Subsection D, waiver of practicum requirements"):
        "Not amended. Reproduced, at page 5, for the conflict with Paragraph (4) of Subsection G of 7.35.3.19 "
        "NMAC, page 13, stated in the callout below. Addendum B and Addendum C carry the cross-references.",

    ("7.35.3.12", "Subsection D, re-application after denial"):
        "Conforming amendment. Same defect and same fix as 7.35.3.10 NMAC Subsection C. 7.35.3.12 NMAC "
        "Subsection D, page 8. Carried over from the July 9, 2026 draft.",

    ("7.35.3.16", "Section heading and Subsection A, general requirements"):
        "Finding B3 of `analysis/july23-rule-concerns.md`, verified against the published rule. 7.35.3.16 NMAC "
        "Subsection A, page 10, requires that a program &#8220;shall engage a qualified third-party evaluation "
        "team&#8221;. Item (b) of Paragraph (2) of Subsection C of the same section, page 10, disqualifies an "
        "evaluator for &#8220;receiving compensation from&#8230; the program or organization being "
        "evaluated&#8221;, with no exception for the engagement itself. The amendment states that the "
        "engagement fee is not a disqualifying conflict. Both provisions are carried over from the July 9, "
        "2026 draft.",

    ("7.35.3.16", "Paragraph (2) of Subsection B, minimum qualifications"):
        "Restoration. The July 9, 2026 draft read &#8220;Medical or research practice&#8221;. The published "
        "rule at 7.35.3.16 NMAC Paragraph (2) of Subsection B, page 10, reads &#8220;Medical and research "
        "practice&#8221;. On the published wording an evaluator in this domain needs both medical and research "
        "practice; on the July 9 wording either will do. The amendment restores the July 9 wording.",

    ("7.35.3.16", "Subsection C, conflict of interest prohibitions"):
        "Two changes. Correction: the heading at 7.35.3.16 NMAC Subsection C, page 10, reads &#8220;Conflict "
        "of -interest prohibitions&#8221;; the July 9, 2026 draft read &#8220;Conflict-of-interest "
        "prohibitions&#8221;. Substance: the carve-out for the engagement fee, consequential on the amendment "
        "to Subsection A of the same section. Finding B3.",

    ("7.35.3.17", "Subsection A, mentoring sessions"):
        "Not amended. 7.35.3.17 NMAC Subsection A, pages 10 and 11, carried over from the July 9, 2026 draft. "
        "The Wilson working redline of July 25, 2026 rewrites this subsection: it retitles the section heading "
        "to read &#8220;CASE-CONSULTATION&#8221; in place of &#8220;MENTORING&#8221;, replaces the 10 hours "
        "with &#8220;2 student case&#8221; consultations, adds that &#8220;Case presentations under "
        "consultation shall include discussion of individual case concerns, risk factors, supportive factors, "
        "treatment considerations, and recommendations for aftercare.&#8221;, and strikes the last two "
        "sentences of the subsection. Her comment on the strike reads &#8220;want to keep this in or strike "
        "it? Would change hours to cases.&#8221; and her comment on the added sentence reads &#8220;This "
        "probably does not need to live in regulation but can be part of a program guide for educational "
        "programs DOH could host and update regularly&#8221;. This document draws no figure and no text from "
        "the redline here, because the placement of the consultation requirement is an open question in the "
        "practicum amendment document.",

    ("7.35.3.17", "Subsection B, module evaluation without attendance"):
        "Not amended. 7.35.3.17 NMAC Subsection B, page 11, carried over from the July 9, 2026 draft. The "
        "Wilson working redline of July 25, 2026 strikes the whole subsection, and her comment on it reads "
        "&#8220;Strike, right? I don't think we want this test out provision.&#8221;",

    # ---- D3. Locations and oversight ----

    ("7.35.3.11", "Section heading and lead-in of Subsection A"):
        "Correction only. 7.35.3.11 NMAC Subsection A, page 5, is lettered &#8220;(A)&#8221;; Subsections B, "
        "C and D of the same section use the form &#8220;B.&#8221;, &#8220;C.&#8221; and &#8220;D.&#8221; The "
        "only other section of the rule that uses parenthetical subsection letters is 7.35.3.14 NMAC, page 9, "
        "which is addressed in the practicum amendment document. No substance is changed.",

    ("7.35.3.11", "Paragraph (11) of Subsection A, owners and employees"):
        "Finding B5 of `analysis/july23-rule-concerns.md`, verified against the published rule. Subsection C "
        "of 7.35.3.14 NMAC, page 9, conditions the authority of healing center owners and employees to "
        "purchase, possess, sell or administer medical psilocybin on their being &#8220;registered with the "
        "department&#8221;. The phrase &#8220;registered with the department&#8221; appears once in 7.35.3 "
        "NMAC, at that provision, and no registration for owners or employees exists in 7.35.3 NMAC or in "
        "7.35.2 NMAC. The amendment supplies the registration at the point where the healing center already "
        "files the names: Paragraph (11) of Subsection A already requires &#8220;A list of all owners or "
        "members of the board of directors, including corresponding contact information&#8221;, Paragraph (2) "
        "of the same subsection already requires &#8220;Names and contact information of primary contact "
        "person(s) and any affiliated practitioners or facilitators&#8221;, and Subsection C of 7.35.3.14 NMAC "
        "already requires that the individual be &#8220;designated to engage in each activity by the healing "
        "center&#8221;. Subsection C of 7.35.3.14 NMAC is new in the published rule; the July 9, 2026 draft "
        "contained no authorized-possession section. No figure is added.",

    ("7.35.3.11", "Paragraph (9) of Subsection B, proof of ownership"):
        "Wilson working redline of July 25, 2026, comment on this paragraph: &#8220;seems like this will "
        "require EOL patients who are getting at home treatment to get permission from their landlord. We "
        "don't require that for any other in home healthcare and it's not appropriate to require that for EOL "
        "patients. People should not have to get their landlords permission to have certain healthcare.&#8221; "
        "End-of-life care is a qualifying condition under Section 3(I) of the Medical Psilocybin Act and under "
        "7.35.2.7 NMAC. 7.35.3.11 NMAC Paragraph (9) of Subsection B, page 6. Carried over from the July 9, "
        "2026 draft.",

    ("7.35.3.11", "Paragraph (10) of Subsection B, outdoor or natural environments"):
        "Conforming amendment. Finding M16 of `analysis/july23-rule-concerns.md`, verified against the "
        "published rule. The outdoor requirements for a healing center at 7.35.3.11 NMAC Paragraph (22) of "
        "Subsection A, pages 5 and 6, run to item (e) and require &#8220;a basic first aid kit and an AED on "
        "site&#8221;. The outdoor requirements for an other approved location at Paragraph (10) of Subsection "
        "B of the same section, pages 6 and 7, stop at item (d). The added item is the text of item (e) of "
        "Paragraph (22) of Subsection A, reproduced. No figure is added; the 15 minutes is the figure already "
        "in both paragraphs.",

    ("7.35.3.11", "Subsection D, certification period; approval and denial"):
        "Two changes. Renewal: finding M22 of `analysis/july23-rule-concerns.md`, verified against the "
        "published rule. Subsection D gives an other approved location a 90-day certification and no renewal "
        "route, while Subsection C of the same section supplies a renewal route for healing centers only. The "
        "90 days in the amendment is the figure already in Subsection D. Re-application: the same conforming "
        "change as 7.35.3.10 NMAC Subsection C. 7.35.3.11 NMAC Subsection D, page 7. Carried over from the "
        "July 9, 2026 draft.",

    # ---- D4. Patients, applicants and process ----

    ("7.35.3.8", "Subsection D, review of a denied patient application"):
        "Conforming amendment. 7.35.3.8 NMAC Subsection D, page 2, gives a denied patient applicant &#8220;a "
        "record review to be conducted by the department&#8221;. The rule provides no proceeding called a "
        "record review. 7.35.3.25 NMAC, page 16, provides an informal administrative review for &#8220;An "
        "applicant for patient enrollment whose application has been denied&#8221;, which is the same class of "
        "person. The amendment names that proceeding and cites it. The July 9, 2026 draft titled the "
        "corresponding section &#8220;DENIAL OF AN INITIAL PATIENT APPLICATION; RECORD REVIEW&#8221;, and its "
        "Subsection A read that applicants &#8220;may request a record review from the department&#8221;, so "
        "the two names described one proceeding in that draft. Section 7.35.3.8 is new in the published rule.",

    ("7.35.3.9", "Paragraphs (5) and (6) of Subsection A, re-application after denial"):
        "Conforming amendment. Same defect and same fix as 7.35.3.10 NMAC Subsection C. 7.35.3.9 NMAC "
        "Paragraphs (5) and (6) of Subsection A, page 2.",

    ("7.35.3.9", "Subsection D, certifying clinician application requirements"):
        "Correction. Finding N3 of `analysis/july23-rule-concerns.md`, verified against the published rule. "
        "The paragraphs of 7.35.3.9 NMAC Subsection D, page 3, run (1), (2), (4), (5), (6). There is no (3). "
        "The amendment renumbers so that the list is consecutive and adds no item. The paragraph reproduced "
        "here contains the controlled substance number requirement at Paragraph (2), which is out of scope for "
        "this document by decision; that paragraph is reproduced as published and is not amended.",

    ("7.35.3.13", "Section heading"):
        "Correction only. Finding N1 of `analysis/july23-rule-concerns.md`, verified against the published "
        "rule. The heading at page 8 reads 7.34.3.13; the history note at the end of the same section reads "
        "&#8220;[7.35.3.13 NMAC, xx/xx/2026]&#8221;. Chapter 34 of Title 7 is a different chapter. Five "
        "headings in the rule read 7.34.3: those of 7.35.3.13, 7.35.3.14, 7.35.3.20, 7.35.3.23 and 7.35.3.25. "
        "The headings of 7.35.3.14 and 7.35.3.20 are corrected in the practicum amendment document; the other "
        "three are corrected here.",

    ("7.35.3.13", "Subsection B, facilitators; scope of work"):
        "Not amended. Recorded because it is the source of the facilitator definition drafted at 7.35.3.7 NMAC "
        "and because of finding M15 of `analysis/july23-rule-concerns.md`. 7.35.3.13 NMAC Subsection B, page "
        "8. Carried over from the July 9, 2026 draft.",

    ("7.35.3.23", "Entire section, dual ownership"):
        "Correction only. Finding N1. The heading at page 15 reads 7.34.3.23; the history note at the end of "
        "the same section reads &#8220;[7.35.3.23 NMAC, xx/xx/2026]&#8221;. The substance is not amended. "
        "&#8220;Permittee&#8221; is defined at 7.35.2.7 NMAC as a psilocybin producer or psilocybin testing "
        "laboratory that holds a permit, so the prohibition operates on the producer and laboratory side "
        "without further definition. Carried over from the July 9, 2026 draft.",

    ("7.35.3.24", "Entire section, complaints to the department"):
        "Three changes, all restorations or corrections. Confidentiality: finding M17 of "
        "`analysis/july23-rule-concerns.md`, verified against the July 9, 2026 draft, which required that a "
        "complaint include the &#8220;Name and contact information for the complainant which will remain "
        "confidential&#8221;. The published section, page 15, requires the name and contact information and "
        "drops the assurance. Mail: the July 9, 2026 draft read that a complaint &#8220;should be in writing "
        "and submitted by U.S. mail or through the electronic&#8221; system; the published section requires "
        "&#8220;U.S. certified mail&#8221;. Duplication: the published section reads &#8220;through the "
        "electronic system designated by the department electronic system&#8221;. Section 7.35.3.24 is new in "
        "the published rule; the July 9, 2026 draft carried the same substance as an unnumbered list headed "
        "&#8220;Complaint Reporting&#8221;.",

    ("7.35.3.25", "Section heading and Subsection A"):
        "Correction only. Finding N1. The heading at page 16 reads 7.34.3.25; the history note at the end of "
        "the same section reads &#8220;[7.35.3.25 NMAC, xx/xx/2026]&#8221;. The substance is not amended.",

    ("7.35.3.25", "Paragraph (1) of Subsection D, content and timeline"):
        "Two corrections. Grammar: finding N4 of `analysis/july23-rule-concerns.md`, verified against the "
        "published rule. The sentence at page 16 has no verb governing the decision, and is carried over "
        "verbatim from the July 9, 2026 draft. The amendment supplies the verb and changes nothing else. "
        "Terminology: the same sentence refers to &#8220;the written request for a record review&#8221;, while "
        "Subsection A of the same section and Paragraph (1) of Subsection B call the proceeding an "
        "administrative review. The 15 calendar days are not amended.",

    ("7.35.3.27", "Paragraph (1) of Subsection C, persons who may request a hearing"):
        "Conforming amendment. Paragraph (1) of Subsection C, page 17, reads &#8220;a certified patient&#8221;. "
        "A patient is enrolled rather than certified: 7.35.3.8 NMAC Subsection E, page 2, provides for "
        "&#8220;A qualified patient's enrollment&#8221;, 7.35.3.22 NMAC, page 15, distinguishes &#8220;a "
        "qualified patient or certificant&#8221;, and 7.35.2.7 NMAC defines &#8220;qualified patient&#8221;. "
        "The subsection is reproduced in full because it is the source of the certificant definition drafted at "
        "7.35.3.7 NMAC. Carried over from the July 9, 2026 draft.",

    ("7.35.3.27", "Paragraph (8) of Subsection B, grounds for disciplinary action"):
        "Correction. Paragraph (8) of Subsection B, page 17, opens &#8220;for certifying clinicians and "
        "practitioners&#8221; and then refers only to &#8220;the clinician&#8221;. The amendment names both "
        "classes the paragraph applies to. Carried over from the July 9, 2026 draft.",

    ("7.35.3.27", "Subsection M, continuances"):
        "Correction. Finding N4. Subsection M, page 18, reads &#8220;The hearing examiner may grant a "
        "continuance for good cause shown&#8221;. Every other subsection of 7.35.3.27 NMAC that names the "
        "presiding official calls that official the hearing officer, including Paragraph (1) of Subsection E, "
        "page 17: &#8220;All hearings held pursuant to this section shall be conducted by a hearing officer "
        "appointed by the secretary.&#8221; The 10 calendar days are not amended. Carried over from the July 9, "
        "2026 draft.",
}


REVIEW = {

    # A review callout enters this record only for a gap, a contradiction, a
    # typo, or a drafting mistake. It leads with the question, and it names who
    # answers. Machine-checked: question first, decision-maker named, length
    # capped, and the question re-appears verbatim on the sheet in Addendum E.

    ("7.35.3.7", "Entire section, definitions"):
        "Which of the ten undefined terms should the department be asked to define? Healing center, 54 uses, "
        "and certifying clinician, 53, lead; Addendum A assembles the material for each. Does the Act's "
        "exemption cover facilitators? Section 5 of the Act exempts a producer, a clinician and a qualified "
        "patient; a facilitator is none of these, and 7.35.3.14 B lets facilitators possess and provide "
        "medical psilocybin. The Training and Education Committee picks the slate; Department of Health staff "
        "and department counsel answer the exemption question.",

    ("7.35.3.8", "Subsection D, review of a denied patient application"):
        "Which denials get the informal review, and which the hearing? Three provisions overlap: this "
        "subsection covers incomplete applications, 7.35.3.25 A covers any denial, and 7.35.3.27 C(7) covers "
        "every denial except incomplete applications, so a patient denied on the merits may have both tracks. "
        "The amendment fixes only the name of the proceeding. Department of Health staff and department "
        "counsel align the scopes.",

    ("7.35.3.9", "Subsection D, certifying clinician application requirements"):
        "Numbering error, or a dropped requirement? The paragraphs run (1), (2), (4), (5), (6); there is no "
        "(3), and the section has no July 9 counterpart to show what stood there. The renumbering drafted "
        "here assumes an error. Department of Health staff confirm nothing was meant to fill the gap.",

    ("7.35.3.10", "Subsection C, re-application after denial"):
        "Is the six months after a first denial a waiting period or a deadline? This subsection says a denied "
        "applicant &#8220;may re-apply within six months&#8221;, then bars a second-time applicant &#8220;for "
        "six months from the denial&#8221;. The amendment reads both as waiting periods, and the same fix is "
        "drafted at 7.35.3.9 A, 7.35.3.11 D and 7.35.3.12 D. Department of Health staff confirm the intended "
        "reading.",

    ("7.35.3.10", "Paragraph (1) of Subsection D, waiver of practicum requirements"):
        "Two group sessions or one, inside the same 40 waiver hours? This paragraph requires &#8220;two "
        "separate group sessions&#8221;; 7.35.3.19 G(4) accepts &#8220;A minimum of one group session&#8221;, "
        "and an out-of-jurisdiction applicant whose program is on the department list can qualify under both "
        "at once. The July 9, 2026 draft read &#8220;or two separate group sessions&#8221; in both places, so "
        "no restoration conforms them. The Training and Education Committee chooses; the practicum draft "
        "records the same conflict and amends neither.",

    ("7.35.3.11", "Paragraph (11) of Subsection A, owners and employees"):
        "Is this the right home for the registration 7.35.3.14 C requires? That provision conditions healing "
        "center staff authority on being &#8220;registered with the department&#8221;, and no such "
        "registration exists in 7.35.3 NMAC or 7.35.2 NMAC. It is drafted here, where the healing center "
        "already files the names; the practicum draft assigns the fix to 7.35.3.11 or 7.35.3.20. Department "
        "of Health staff decide the home.",

    ("7.35.3.11", "Paragraph (9) of Subsection B, proof of ownership"):
        "Keep the owner's statement for a patient's own residence, or adopt the exemption drafted here? The "
        "Wilson redline records that the paragraph as published makes an end-of-life patient get a landlord's "
        "permission for treatment at home. The exemption removes that, and it also removes the only notice an "
        "owner gets. The board weighs access against notice.",

    ("7.35.3.11", "Paragraph (10) of Subsection B, outdoor or natural environments"):
        "Where does the two-person requirement belong? The Wilson redline adds it at the healing center "
        "paragraph and records that &#8220;the 2 person universal requirement did not make it into the "
        "published rules, though DOH did confirm they mean for it to be universal.&#8221; Ms. Wilson and "
        "Department of Health staff place it.",

    ("7.35.3.13", "Subsection B, facilitators; scope of work"):
        "Does direct supervision mean in the room, at the location, or available? This subsection limits a "
        "facilitator to peer support under a practitioner's &#8220;direct supervision&#8221;, while 7.35.3.14 "
        "B lets facilitators possess and provide psilocybin and 7.35.3.20 H(5) lets a facilitator be the only "
        "certificant with a patient in a group session. The rule never defines the term. The Training and "
        "Education Committee and Department of Health staff say what it means; the conflicting provisions are "
        "in the practicum draft's scope.",

    ("7.35.3.16", "Section heading and Subsection A, general requirements"):
        "Adopt the engagement-fee cure at Subsection A, at C(2)(b), or both? As published no evaluator can "
        "serve: a program &#8220;shall engage a qualified third-party evaluation team&#8221;, and C(2)(b) "
        "disqualifies anyone &#8220;receiving compensation from&#8230; the program or organization being "
        "evaluated&#8221;. Both cures are drafted. The Training and Education Committee chooses.",

    ("7.35.3.16", "Paragraph (2) of Subsection B, minimum qualifications"):
        "Was the change from or to and deliberate? The July 9, 2026 draft read &#8220;Medical or research "
        "practice&#8221;; the published rule reads &#8220;Medical and research practice&#8221;, so an "
        "evaluator in this domain now needs both. The amendment restores the July 9 reading. Department of "
        "Health staff confirm the intent.",

    ("7.35.3.17", "Subsection A, mentoring sessions"):
        "Hours or cases, and stated here or at the practicum draft's proposed 7.35.3.19 H? Open with Dr. "
        "Metz, Ms. Wilson and Dr. Leeman; as published, 7.35.3.19 runs A through G and has no Subsection H. "
        "One warning while it is open: the 10 mentoring hours here run &#8220;after graduation and after "
        "practicum hours are completed&#8221; and sit inside no program total, so if the consultation "
        "requirement lands at 7.35.3.19 H while this subsection stands, a graduate owes both sets of hours.",

    ("7.35.3.17", "Subsection B, module evaluation without attendance"):
        "Strike the test-out option, or keep it and restate the cap? The Wilson redline strikes the "
        "subsection: &#8220;Strike, right? I don't think we want this test out provision.&#8221; If it stays, "
        "the cap is broken for any program with a single price, because it is a fraction of the &#8220;normal "
        "price of each of the educational modules&#8221;. The Training and Education Committee decides "
        "whether it survives.",

    ("7.35.3.24", "Entire section, complaints to the department"):
        "Do staff regain standing to complain? The July 9, 2026 draft allowed &#8220;Patients or staff&#8221; "
        "to complain; the published section allows only a qualified patient or certificant, so a healing "
        "center employee who is neither has no route. Department of Health staff and department counsel "
        "decide whether staff standing returns.",

    ("7.35.3.25", "Paragraph (1) of Subsection D, content and timeline"):
        "Who is the administrative review committee? It decides every informal review and its decision is "
        "final, but nothing in 7.35.3 NMAC or 7.35.2 NMAC constitutes it, seats it, or appoints it. "
        "Department of Health staff must say who it is before the rule is filed.",
}


# ---------------------------------------------------------------------------
# The question sheet, Addendum E. Every row quotes its callout's question
# verbatim, grouped by who answers it, so the sheet cannot drift from the
# notes. Machine-checked in audit.py.
# ---------------------------------------------------------------------------

GROUPS = [
    ("staff", "Department of Health staff"),
    ("counsel", "Department of Health staff with department counsel"),
    ("committee", "The Training and Education Committee"),
    ("board", "The board"),
    ("named", "Dr. Metz, Ms. Wilson and Dr. Leeman"),
]

# (group key, section, subsection label, the question, verbatim from the note)
QUESTIONS = [
    ("staff", "7.35.3.9", "Subsection D, certifying clinician application requirements",
     "Numbering error, or a dropped requirement?"),
    ("staff", "7.35.3.10", "Subsection C, re-application after denial",
     "Is the six months after a first denial a waiting period or a deadline?"),
    ("staff", "7.35.3.11", "Paragraph (11) of Subsection A, owners and employees",
     "Is this the right home for the registration 7.35.3.14 C requires?"),
    ("staff", "7.35.3.16", "Paragraph (2) of Subsection B, minimum qualifications",
     "Was the change from or to and deliberate?"),
    ("staff", "7.35.3.25", "Paragraph (1) of Subsection D, content and timeline",
     "Who is the administrative review committee?"),

    ("counsel", "7.35.3.7", "Entire section, definitions",
     "Does the Act's exemption cover facilitators?"),
    ("counsel", "7.35.3.8", "Subsection D, review of a denied patient application",
     "Which denials get the informal review, and which the hearing?"),
    ("counsel", "7.35.3.24", "Entire section, complaints to the department",
     "Do staff regain standing to complain?"),

    ("committee", "7.35.3.7", "Entire section, definitions",
     "Which of the ten undefined terms should the department be asked to define?"),
    ("committee", "7.35.3.10", "Paragraph (1) of Subsection D, waiver of practicum requirements",
     "Two group sessions or one, inside the same 40 waiver hours?"),
    ("committee", "7.35.3.13", "Subsection B, facilitators; scope of work",
     "Does direct supervision mean in the room, at the location, or available?"),
    ("committee", "7.35.3.16", "Section heading and Subsection A, general requirements",
     "Adopt the engagement-fee cure at Subsection A, at C(2)(b), or both?"),
    ("committee", "7.35.3.17", "Subsection B, module evaluation without attendance",
     "Strike the test-out option, or keep it and restate the cap?"),

    ("board", "7.35.3.11", "Paragraph (9) of Subsection B, proof of ownership",
     "Keep the owner's statement for a patient's own residence, or adopt the exemption drafted here?"),

    ("named", "7.35.3.17", "Subsection A, mentoring sessions",
     "Hours or cases, and stated here or at the practicum draft's proposed 7.35.3.19 H?"),
    ("named", "7.35.3.11", "Paragraph (10) of Subsection B, outdoor or natural environments",
     "Where does the two-person requirement belong?"),
]


def source_for(section, sub):
    return SOURCE.get((section, sub), "")


def review_for(section, sub):
    return REVIEW.get((section, sub), "")

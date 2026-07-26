"""Citation and review note for each provision.

Every provision the document reproduces carries a source note. A provision that
raises a question the record cannot settle also carries a review note. Each
review note states the issue, the choices, and who decides.

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

    ("7.35.3.2", "Entire section, scope"):
        "Not amended. Recorded for the terminology it fixes. 7.35.3.2 NMAC, page 1, lists the regulated "
        "classes as &#8220;patients, practitioners, clinicians, facilitators, healing centers and other "
        "approved locations, and educational programs&#8221;. Of those, 7.35.2.7 NMAC defines practitioner, "
        "clinician and approved location, and does not define facilitator, healing center or educational "
        "program. Carried over from the July 9, 2026 draft.",

    ("7.35.3.3", "Entire section, statutory authority"):
        "Not amended. Recorded as a fact. 7.35.3.3 NMAC, page 1, cites &#8220;the Medical Psilocybin Act, "
        "Section 26-2D-7, NMSA 1978&#8221;. Section 1 of the Act provides that Sections 1 through 11 of the act "
        "may be cited as the Medical Psilocybin Act. Section 7 of the Act is the section creating the program "
        "in the department and directing what the department shall establish. This record does not verify the "
        "codification. Carried over from the July 9, 2026 draft.",

    ("7.35.3.5", "Entire section, effective date"):
        "Not amended. Recorded for its interaction with the history notes. 7.35.3.5 NMAC, page 1, reads "
        "&#8220;xx/xx, 2026, unless a later date is cited at the end of a section&#8221;. Twenty-six of the "
        "twenty-eight history notes in the rule read &#8220;xx/xx/2026&#8221;. The notes for 7.35.3.27 and "
        "7.35.3.28, page 19, read &#8220;9/22/2026&#8221;. Carried over from the July 9, 2026 draft, which "
        "read &#8220;XXXX,XX,2026&#8221;.",

    ("7.35.3.7", "Entire section, definitions"):
        "Four definitions are added. Each is drawn from a single provision of the rule as published, cited "
        "here, and none is composed for this draft. Certificant: 7.35.3.26 NMAC, page 16, which names the six "
        "classes that hold a certification. Facilitator: 7.35.3.13 NMAC Subsection B, page 8, which states the "
        "scope of work, together with 7.35.3.9 NMAC Subsection F, page 3, which requires certification. "
        "Registrant of another approved location: 7.35.3.11 NMAC Subsection B, page 6. Student: 7.35.3.20 NMAC "
        "Paragraph (5) of Subsection H, page 14. Section 7.35.3.7 as published reads in full: &#8220;The "
        "definitions in 7.35.2.7 NMAC apply to this part.&#8221; This section is new; the July 9, 2026 draft "
        "carried no definitions section. Addendum A maps every undefined term. Amending 7.35.2 NMAC is a "
        "separate rulemaking, because that part was adopted effective June 23, 2026, so any term this part "
        "needs and 7.35.2.7 NMAC does not supply has to be carried here.",

    # ---- D2. Educational programs ----

    ("7.35.3.10", "Paragraph (2) of Subsection A, additions to the list"):
        "Not amended. Recorded for the sequence it creates. 7.35.3.10 NMAC Paragraph (2) of Subsection A, "
        "page 4, is the only route by which a program reaches the list. Carried over from the July 9, 2026 "
        "draft, where the section was titled &#8220;RECIPROCITY FOR CERTIFYING CLINICIANS, PRACTITIONERS AND "
        "FACILITATORS&#8221;.",

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

    ("7.35.3.12", "Subsection D, re-application after denial"):
        "Conforming amendment. Same defect and same fix as 7.35.3.10 NMAC Subsection C. 7.35.3.12 NMAC "
        "Subsection D, page 8. Carried over from the July 9, 2026 draft.",

    ("7.35.3.15", "Subsection A, required reporting of updates"):
        "The 60 calendar days are taken from 7.35.3.15 NMAC Subsection B, page 9, which gives the department "
        "60 calendar days to decide a curriculum approval application. No new figure is introduced. Subsection "
        "A as published bars a program from implementing a reported change &#8220;until written approval is "
        "issued by the department&#8221; and sets no period within which the department must act. Carried over "
        "from the July 9, 2026 draft.",

    ("7.35.3.16", "Section heading and Subsection A, general requirements"):
        "Finding B3 of `analysis/july23-rule-concerns.md`, verified against the published rule. 7.35.3.16 NMAC "
        "Subsection A, page 10, requires that a program &#8220;shall engage a qualified third-party evaluation "
        "team&#8221;. Item (b) of Paragraph (2) of Subsection C of the same section, page 10, disqualifies an "
        "evaluator for &#8220;receiving compensation from&#8230; the program or organization being "
        "evaluated&#8221;, with no exception for the engagement itself. The amendment states that the "
        "engagement fee is not a disqualifying conflict. Both provisions are carried over from the July 9, "
        "2026 draft. On why the evaluation exists, the July 17, 2026 Training and Education Committee "
        "transcript records that programs &#8220;also will have a need to have that third-party evaluation "
        "that's looking to ensure that the curriculum is implemented with fidelity&#8221;.",

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

    ("7.35.3.20", "Section heading, lead-in, and Subsection A"):
        "Not amended here. The section heading reads 7.34.3.20 and its correction is drafted in the practicum "
        "amendment document, so it is not duplicated. Recorded for two other things. Terminology: the lead-in "
        "and Subsection A, page 13, use &#8220;a registrant of another approved location&#8221;, and the term "
        "&#8220;registrant&#8221; appears 10 times in 7.35.3.20 NMAC and nowhere else in the rule, while "
        "Subsection B of 7.35.3.11 NMAC, page 6, issues a certification for such a location rather than a "
        "registration; the definition drafted at 7.35.3.7 NMAC ties the two together. Patient roster: finding "
        "M18. Carried over from the July 9, 2026 draft.",

    ("7.35.3.21", "Subsection A, authority to conduct assessments"):
        "Not amended. Recorded for two things. Patient interviews: Subsection A, page 15, permits the "
        "department to &#8220;interview staff and patients&#8221;, subject to the exception in the same "
        "subsection for an on-site assessment during a patient session or at a patient's home. Frequency: "
        "7.35.3.21 NMAC sets no interval at which assessments occur, while 7.35.3.16 NMAC Subsection E, page "
        "10, requires a third-party evaluation report without stating how often. Carried over from the July 9, "
        "2026 draft, where the section was titled &#8220;PSILOCYBIN EDUCATIONAL PROGRAMS, HEALING CENTERS, "
        "OTHER APPROVED LOCATIONS; EVALUATION AND ASSESSMENT BY THE DEPARTMENT&#8221;.",

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

    ("7.35.3.11", "Paragraph (11) of Subsection A, owners and employees"):
        "The registration drafted here operates on the list the healing center files with its application, "
        "which fixes the position as at the date of the application. Nothing in 7.35.3.11 NMAC requires a "
        "healing center to update that list, and 7.35.3.11 NMAC has four subsections, A through D, none of "
        "which is a reporting duty; the only comparable duty in the rule is Subsection A of 7.35.3.15 NMAC, "
        "page 9, which applies to educational programs and not to healing centers. So an owner or employee "
        "who joins after certification would not be registered until the renewal under Subsection C of this "
        "section, which falls at two years. Three choices. Add a reporting duty for changes to the list, "
        "which is a new obligation that no source in this record proposes and which is therefore not drafted "
        "here. Rely on the two-year renewal. Or strike the registration condition from Subsection C of "
        "7.35.3.14 NMAC instead of supplying a registration, which would leave the designation by the healing "
        "center as the only requirement. Department of Health staff decide, and the third choice has to be "
        "coordinated with the practicum amendment document because Subsection C of 7.35.3.14 NMAC is in that "
        "draft's scope. Whichever is chosen, the condition in Subsection C of 7.35.3.14 NMAC cannot be "
        "satisfied as published.",


    ("7.35.3.2", "Entire section, scope"):
        "The scope names six regulated classes, and 7.35.2.7 NMAC defines three of them. The rule uses "
        "&#8220;clinician&#8221; here and &#8220;certifying clinician&#8221; 53 times elsewhere, and 7.35.2.7 "
        "NMAC defines the first and not the second. Two choices. Leave the scope as published and rely on the "
        "definitions drafted at 7.35.3.7 NMAC to carry the undefined terms, or conform this section to the "
        "vocabulary the rest of the part uses. The Training and Education Committee and Department of Health "
        "staff decide which, and the choice governs the definition slate at 7.35.3.7 NMAC.",

    ("7.35.3.3", "Entire section, statutory authority"):
        "This document does not verify any NMSA 1978 section number, and the codification asserted here has "
        "not been checked against the enacted text in this record. Two choices. Leave the citation as "
        "published, or ask the department to confirm the codification before the rule is filed. Department of "
        "Health staff and department counsel decide, and no board action is needed either way.",

    ("7.35.3.5", "Entire section, effective date"):
        "Because 7.35.3.5 NMAC gives effect to a later date cited at the end of a section, the rule as "
        "published takes effect on an unfilled date except for 7.35.3.27 and 7.35.3.28, which take effect "
        "September 22, 2026. The rule hearing is set for August 28, 2026. No source in this record supplies "
        "the intended effective date, so none is drafted. Three choices. Conform the two history notes to the "
        "placeholder the other twenty-six carry, fill 7.35.3.5 NMAC with a date and leave the two notes as "
        "they stand if a later date for those two sections is intended, or fill all twenty-eight with one "
        "date. Department of Health staff decide, because the department sets the filing and effective dates.",

    ("7.35.3.7", "Entire section, definitions"):
        "Two questions here, and the second is the larger one. First, the slate. Sixteen terms that carry "
        "regulatory consequence in this part are defined nowhere: the four definitions drafted here are the "
        "only ones a single provision of the rule supplies, and twelve remain, including healing center, which "
        "appears 54 times, and certifying clinician, which appears 53 times. No source in this record defines "
        "either, so neither is drafted. Addendum A lists all sixteen with counts. The Training and Education "
        "Committee decides which to send to the department, and the department decides what each says. Second, "
        "the facilitator. Section 3(B) of the Medical Psilocybin Act defines a clinician as an approved health "
        "care provider licensed in New Mexico who holds a permit from the department to provide medical "
        "services to qualified patients. Section 5 of the Act exempts from arrest, prosecution and penalty a "
        "producer, a clinician and a qualified patient, and Paragraph (2) of Subsection B of Section 5 makes "
        "lawful the conduct of &#8220;a clinician administering or a qualified patient taking psilocybin in an "
        "approved setting&#8221;. A facilitator holds no professional license under this rule: Subsection F of "
        "7.35.3.9 NMAC, page 3, requires no license of a facilitator applicant. Subsection B of 7.35.3.14 "
        "NMAC, page 9, nonetheless authorizes facilitators to possess medical psilocybin products and to "
        "provide them to qualified patients. Whether a facilitator falls within Section 3(B) of the Act, and "
        "so within the Section 5 exemption, is a question of statutory construction that this record cannot "
        "settle and that a definition in this part cannot cure if the answer is no. Department of Health staff "
        "and department counsel decide it, and the board should be told the answer before the rule is filed.",

    ("7.35.3.10", "Paragraph (2) of Subsection A, additions to the list"):
        "A program reaches the list only when an individual application relying on that program is approved, "
        "and an application filed on or after January 1, 2028 needs either a third-party evaluation or a "
        "program already on the list. On the first day the list is empty, so the first applicants must supply "
        "an evaluation, and finding M6 of `analysis/july23-rule-concerns.md` records that the list can only "
        "populate after the fact. Two choices. Leave the paragraph as published and rely on the amendment "
        "drafted at Paragraph (2) of Subsection B of this section, which lets an applicant point to the list "
        "once a program is on it, or add a route by which the department may place a program on the list on "
        "its own initiative. The second is a new grant of authority and no source in this record proposes its "
        "terms, so it is not drafted. The Training and Education Committee decides whether to ask for it, and "
        "Department of Health staff decide its terms.",

    ("7.35.3.10", "Subsection C, re-application after denial"):
        "The amendment reads the six months as a waiting period, because the following sentence of the same "
        "subsection sets a waiting period for a second denial and the two sentences otherwise contradict each "
        "other. The other reading is that a denied applicant has six months in which to re-apply and loses the "
        "right afterwards. Finding M21 of `analysis/july23-rule-concerns.md` records the ambiguity. Department "
        "of Health staff decide which reading was intended, and the same answer governs all four places the "
        "sentence appears.",

    ("7.35.3.15", "Subsection A, required reporting of updates"):
        "Finding M8 of `analysis/july23-rule-concerns.md`. Until the department approves, a program may not "
        "replace an instructor who has resigned, change a practicum site, or move a classroom, and the rule as "
        "published binds the department to no period. The 60 calendar days drafted here are the period the "
        "rule already sets for curriculum approval in Subsection B of this section, and no source in this "
        "record proposes a period for this subsection. Three choices. Adopt the 60 days by analogy as drafted, "
        "set a shorter period for changes that do not touch curriculum, or provide that a reported change may "
        "be implemented if the department does not act within the period. Department of Health staff decide, "
        "because the period binds the department.",

    ("7.35.3.16", "Section heading and Subsection A, general requirements"):
        "The amendment cures the conflict by naming the engagement fee as something other than a disqualifying "
        "conflict. One alternative is to place the same words in item (b) of Paragraph (2) of Subsection C "
        "instead, and this document drafts that too so that the committee can adopt either or both. A second "
        "alternative is to have the department, rather than the program, engage and pay the team, which would "
        "remove the conflict entirely but requires a funding source that no document in this record identifies. "
        "The Training and Education Committee decides which route to send forward, and Department of Health "
        "staff decide whether the second is available.",

    ("7.35.3.16", "Paragraph (2) of Subsection B, minimum qualifications"):
        "Finding M10 of `analysis/july23-rule-concerns.md`. Two questions sit on this paragraph. First, "
        "whether the change from &#8220;or&#8221; to &#8220;and&#8221; between the July 9 and July 23 drafts "
        "was deliberate. Two choices follow from the answer: keep the amendment, which restores the July 9 "
        "wording, or withdraw it if the narrowing was intended. Department of Health staff decide, because "
        "only the department knows whether the change was made on purpose. Second, whether a three-person "
        "team can in fact cover all three domains at three years of experience each in New Mexico. Two "
        "choices there as well: leave the standard as published, or lower it. No source in this record "
        "proposes a lower standard, so none is drafted. The Training and Education Committee decides whether "
        "to ask for one, because the committee is the body that will hear from programs that cannot find a "
        "qualifying team.",

    ("7.35.3.17", "Subsection A, mentoring sessions"):
        "This subsection is left exactly as published, deliberately. The Wilson working redline would change "
        "the obligation from 10 hours of mentoring to 2 student case consultations, and the practicum "
        "amendment document holds open, for Dr. Metz, Ms. Wilson and Dr. Leeman, whether the consultation "
        "requirement is stated in hours, in cases, or in both, and whether it belongs at the proposed "
        "Subsection H of 7.35.3.19 NMAC, which exists only in that draft's re-lettering of that section, or "
        "at Subsection A of this section. As published, 7.35.3.19 NMAC runs A through G and has no Subsection "
        "H. Drafting either figure here would answer that question, so neither is drafted. Two choices, and "
        "they are theirs: state the requirement here, in which case this subsection is redrafted and the "
        "proposed 7.35.3.19 H carries a cross-reference, or state it at the proposed 7.35.3.19 H, in which "
        "case this subsection is struck. Dr. Metz, Ms. Wilson and Dr. Leeman decide "
        "which, and this section should be redrafted once they do. Findings M11 and M12 of "
        "`analysis/july23-rule-concerns.md` record the separate points that the obligation is unfunded and "
        "survives the program.",

    ("7.35.3.17", "Subsection B, module evaluation without attendance"):
        "Finding M12 of `analysis/july23-rule-concerns.md`: the price cap is stated as a fraction of the "
        "&#8220;normal price of each of the educational modules&#8221;, which assumes that programs price "
        "modules separately rather than pricing the program as a whole. Two choices. Strike the subsection, as "
        "the Wilson working redline proposes, or keep it and restate the cap so that it works for a program "
        "with a single price. No source in this record supplies a restated cap, so none is drafted. The "
        "Training and Education Committee decides whether the option survives at all, and only then is a "
        "restated cap worth drafting.",

    ("7.35.3.11", "Paragraph (9) of Subsection B, proof of ownership"):
        "The amendment exempts the qualified patient's own residence from the ownership proof and the owner's "
        "written statement. Two things to weigh. Subsection B of this section makes an other approved location "
        "available in part &#8220;for purposes of improving patient access in rural and frontier "
        "counties&#8221;, and a patient's residence is the leading example the same subsection gives. Against "
        "that, the owner's statement is the only place in the rule where a property owner is told what will "
        "occur on the premises, so exempting the residence removes that notice for the location where "
        "sessions are most likely to be unsupervised by a healing center. Two choices. Adopt the exemption as "
        "drafted, or keep the requirement and allow the patient's own attestation in place of the owner's "
        "statement. The board decides, because the trade is patient access against notice to a third party.",

    ("7.35.3.11", "Paragraph (10) of Subsection B, outdoor or natural environments"):
        "Two further questions on the same paragraph, neither answered here. The 15 minutes: the Wilson "
        "working redline comments on both places the figure appears, &#8220;Is this a reasonable limit? "
        "Everything feels at least 15 minutes away - should we say 30?&#8221; and &#8220;again - I think this "
        "should maybe be 30. Everything is 15 minutes away from everything.&#8221; Those are questions rather "
        "than a recommendation, and no source in this record supplies a figure, so the 15 minutes is left as "
        "published in both paragraphs. The two-person requirement: the redline adds at the healing center "
        "paragraph that &#8220;For the purposes of this section, an individual is a DOH-permitted "
        "practitioner, a DOH-premitted facilitator, or an individual who is a DOH registered student with an "
        "approved training program who has completed a minimum of 30 practicum hours and who is accompanied by "
        "a DOH-permitted practitioner.&#8221;, and the comment on it reads &#8220;Not sure where this goes - "
        "the 2 person universal requirement did not make it into the published rules, though DOH did confirm "
        "they mean for it to be universal.&#8221; Because the author records that she does not know where the "
        "provision belongs, it is not drafted. Ms. Wilson and Department of Health staff decide where it goes "
        "and whether the 15 minutes becomes 30.",

    ("7.35.3.11", "Subsection D, certification period; approval and denial"):
        "The renewal drafted here repeats the 90 days the subsection already sets, so nothing new is "
        "introduced, but three questions remain. Whether 90 days is the right term at all, which no source in "
        "this record addresses. Whether a renewal application needs its own contents, or whether the "
        "application under Subsection B of this section is resubmitted. Whether the department is bound to any "
        "period in deciding a renewal, since Subsection D binds it to 30 calendar days only for a denial. "
        "Department of Health staff decide all three, because each one binds the department, and the Training "
        "and Education Committee should say whether a 90-day term with renewal is workable for a practicum "
        "site.",

    ("7.35.3.20", "Section heading, lead-in, and Subsection A"):
        "Two questions, neither drafted here. Terminology: this section calls the holder of an other approved "
        "location certification a registrant 10 times, and Subsection B of 7.35.3.11 NMAC issues a "
        "certification. Two choices. Adopt the definition drafted at 7.35.3.7 NMAC, which ties the two words "
        "together and leaves this section untouched, or conform all 10 occurrences here to certificant. "
        "Department of Health staff decide which, and the second choice requires 10 edits this document does "
        "not make. Patient roster: finding M18 of `analysis/july23-rule-concerns.md` records that Subsection A "
        "requires a list of all qualified patients intended to use and who have used the location, which read "
        "with Subsection A of 7.35.3.21 NMAC allows the department to obtain patient identities and interview "
        "patients. Whether the roster should instead be kept in a form that does not identify patients to the "
        "department is a question for the board, and it turns on the department's data needs, which "
        "Department of Health staff would have to state.",

    ("7.35.3.21", "Subsection A, authority to conduct assessments"):
        "Two questions, neither drafted here. Patient interviews: the exception in this subsection protects a "
        "patient during a session and at home, and does not otherwise limit whom the department may interview "
        "or require that the patient consent. Whether an additional consent requirement should apply to any "
        "patient interview is a question for the board. Frequency: the rule does not say how often the "
        "department assesses a program, a healing center or an other approved location, and it does not say "
        "how often a third-party evaluation must be repeated once the initial one is filed under Paragraph "
        "(20) of Subsection A of 7.35.3.12 NMAC. Finding M10 of `analysis/july23-rule-concerns.md` records the "
        "second point. No source in this record supplies an interval, so none is drafted. Department of Health "
        "staff decide both, because each is a demand on department capacity.",

    ("7.35.3.8", "Subsection D, review of a denied patient application"):
        "Finding M23 of `analysis/july23-rule-concerns.md`. Three provisions describe review of a denial, and "
        "their scopes do not line up. This subsection covers a patient applicant denied for an incomplete "
        "application or a missed submittal requirement. Subsection A of 7.35.3.25 NMAC covers any patient "
        "applicant whose application has been denied. Paragraph (7) of Subsection C of 7.35.3.27 NMAC gives a "
        "hearing to an applicant denied for any reason other than an incomplete application or a missed "
        "submittal requirement. Read together, the informal review reaches every denial and the hearing "
        "reaches every denial except the two that this subsection covers, so a patient applicant denied on the "
        "merits may have both. The amendment drafted here only fixes the name of the proceeding and leaves the "
        "overlap alone. Two choices on the overlap. Narrow Subsection A of 7.35.3.25 NMAC to the grounds this "
        "subsection names, or state that the informal review and the hearing are alternatives and which one a "
        "patient applicant elects. Department of Health staff and department counsel decide, because the "
        "answer affects what process a denied applicant is owed.",

    ("7.35.3.9", "Subsection D, certifying clinician application requirements"):
        "The renumbering assumes that the gap is a numbering error rather than the trace of a deleted "
        "requirement. Section 7.35.3.9 has no counterpart in the July 9, 2026 draft, so this record cannot "
        "show what, if anything, stood at Paragraph (3). Two choices. Renumber as drafted, or restore the "
        "missing requirement if one was intended. Department of Health staff decide, because only the "
        "department knows what the paragraph held.",

    ("7.35.3.13", "Subsection B, facilitators; scope of work"):
        "Finding M15 of `analysis/july23-rule-concerns.md`. This subsection puts a facilitator under the "
        "direct supervision of a practitioner and limits the facilitator to peer support and to logistical and "
        "administrative support. Three provisions sit against it, and all three are in the practicum "
        "amendment document rather than this one. Subsection B of 7.35.3.14 NMAC, page 9, lets a facilitator "
        "possess psilocybin products and provide them to qualified patients. Paragraph (5) of Subsection H of "
        "7.35.3.20 NMAC, page 14, permits a group session staffed by one facilitator or qualified student for "
        "every two patients with one practitioner for every eight patients, so a facilitator may be the only "
        "certificant with a given patient. Subsection C of 7.35.3.19 NMAC, page 13, has practitioners "
        "supervising facilitators during administration sessions as part of the practicum. Whether "
        "&#8220;direct supervision&#8221; means presence in the room, presence at the location, or "
        "availability is not stated anywhere in the rule. Three choices. Define direct supervision in this "
        "part, which the definitions drafted at 7.35.3.7 NMAC could carry; narrow the facilitator authority "
        "in the three provisions named above to match this subsection; or widen this subsection to match "
        "them. No source in this record chooses among the three, so none is drafted. The Training and "
        "Education Committee and Department of Health staff decide the meaning, and because the conflicting "
        "provisions belong to the practicum draft, any amendment has to be coordinated with that document "
        "rather than made here.",

    ("7.35.3.24", "Entire section, complaints to the department"):
        "Two questions the amendment does not reach. Standing: the July 9, 2026 draft provided that "
        "&#8220;Patients or staff may lodge a complaint with the department.&#8221; The published section "
        "allows a complaint from a qualified patient or a certificant, so an employee of a healing center who "
        "is neither has no route under this section. Two choices. Restore standing for staff, or leave the "
        "section as published and rely on the adverse health event reporting in Subsection L of 7.35.3.20 "
        "NMAC. Scope of the confidentiality restored here: the July 9 wording protected the complainant's name "
        "and contact information and said nothing about disclosure to the certificant complained of, or about "
        "the application of the Inspection of Public Records Act. Department of Health staff and department "
        "counsel decide both, and the board should be told whether a complainant can be assured of "
        "confidentiality before the rule is filed.",

    ("7.35.3.25", "Paragraph (1) of Subsection D, content and timeline"):
        "Two questions on this section that the corrections do not reach. The administrative review committee: "
        "Subsection C of this section and Paragraph (2) of Subsection D assign the review to &#8220;the "
        "administrative review committee&#8221;, and nothing in 7.35.3 NMAC or 7.35.2 NMAC constitutes that "
        "committee, states who sits on it, or says how it is appointed. The term appears four times in the "
        "rule, all in this section, and it is carried over from the July 9, 2026 draft. Judicial review: "
        "Subsection E provides that &#8220;Except as otherwise provided by law, there shall be no right to "
        "judicial review of a decision by the administrative review committee.&#8221; and the Wilson working "
        "redline comments on that subsection &#8220;they really went in the opposite direction of due process "
        "here...&#8221; Neither is drafted, because constituting a committee and limiting judicial review are "
        "both beyond what a correction can carry, and no source in this record proposes terms for either. "
        "Department of Health staff must say who the committee is, and department counsel must say whether "
        "Subsection E is within the department's authority. The board should have both answers before the rule "
        "is filed.",

    ("7.35.3.27", "Subsection M, continuances"):
        "Finding N5 of `analysis/july23-rule-concerns.md`, which the correction to this subsection does not "
        "reach. Subsection A of this section newly allows the department to suspend a certification "
        "immediately. After a suspension, Subsection F allows the hearing to be held up to 60 calendar days "
        "after the request, Paragraph (2) of Subsection O allows the hearing officer 30 calendar days after "
        "the last submission to recommend, and Paragraph (3) of Subsection O allows the secretary 45 calendar "
        "days after receipt to decide, so a suspended certificant can be out of practice for more than 135 "
        "days before a final decision. The rule provides no expedited track. Two choices. Add an expedited "
        "schedule for a hearing that follows an immediate suspension, or leave the timeline as published. No "
        "source in this record supplies a shorter period, so none is drafted. Department of Health staff and "
        "department counsel decide, because the periods bind the department and the secretary.",
}


def source_for(section, sub):
    return SOURCE.get((section, sub), "")


def review_for(section, sub):
    return REVIEW.get((section, sub), "")

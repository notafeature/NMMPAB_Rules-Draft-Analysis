"""Citation and review note for each proposed change.

Sources are the Metz recommendation of July 17, 2026; the Wilson working redline
of July 25, 2026; the July 17, 2026 meeting transcripts; the Medical Psilocybin
Act; and the rule as published.

Every review note states the issue, the choices, and who decides. No note ends
on a bare question.
"""

SOURCE = {
    ("7.35.3.14", "Section heading"):
        "Two changes. Correction: the heading as published reads 7.34.3.14, while the history note at the end of the "
        "same section reads 7.35.3.14. Permit name: recommendation 1 of the Metz recommendation, page 1, which renames "
        "the practitioner permit to licensed provider. Addendum C maps the full extent of that renaming.",
    ("7.35.3.14", "Subsection A"):
        "Consequential on proposed 7.35.3.29. The permit name is conformed in the same subsection.",
    ("7.35.3.14", "Subsection B"):
        "Consequential on proposed 7.35.3.29.",
    ("7.35.3.14", "Subsection C"):
        "Not amended.",
    ("7.35.3.18", "Section heading"):
        "Permit name only. Metz recommendation, page 1, recommendation 1, which renames the practitioner permit to "
        "licensed provider. Addendum C.",
    ("7.35.3.18", "Subsection A"):
        "Metz recommendation, page 2, curriculum table: New Mexico module, 6 to 8 hours.",
    ("7.35.3.18", "Subsection C, {{PT_C}} and facilitator psilocybin therapy module, lead-in"):
        "Metz recommendation, page 2: “Adopt a single state-level standard of 84 didactic hours for both "
        "Facilitator and Licensed Provider permits, with the curriculum allocation below.” The curriculum table "
        "on the same page lists the New Mexico module as one of its ten content areas, so the New Mexico module sits "
        "inside the 84. The arithmetic follows: 84 less the New Mexico module at Subsection A (6), less the "
        "role-specific module at Subsection D or E (5, unchanged), less the simulated patient experience "
        "(5, unchanged), leaves 68 didactic hours for this subsection.",
    ("7.35.3.18", "Subsection C, required topics"):
        "Metz recommendation, pages 2 and 3, curriculum table, for paragraphs (16), (17), (20), (21), (22) and (23). "
        "July 17, 2026 Training and Education Committee transcript for paragraphs (18) and (19); both are qualifying "
        "conditions under Section 3(I) of the Medical Psilocybin Act. The Wilson redline adds the same content areas.",
    ("7.35.3.18", "Subsection E"):
        "Permit name only. Metz recommendation, page 1, recommendation 1. Addendum C. The five didactic hours are not "
        "amended.",
    ("7.35.3.18", "Subsection F"):
        "Correction. The sentence as published does not complete. The permit name is conformed in the same subsection.",
    ("7.35.3.18", "Subsection G"):
        "Permit name only. Metz recommendation, page 1, recommendation 1. Addendum C. The 20 continuing education "
        "hours and the life support requirement are not amended.",
    ("7.35.3.18", "Subsection H"):
        "Metz recommendation, page 3: “Component ranges are illustrative; the binding minimum is the total.”",
    ("7.35.3.19", "Section heading"):
        "Permit name only. Metz recommendation, page 1, recommendation 1. Addendum C.",
    ("7.35.3.19", "Subsection A"):
        "Metz recommendation, page 4: “approximately 62 hours for Facilitators (steps 1-3); approximately 72 hours "
        "for Licensed Providers (steps 1-4).” The permit name is conformed in the same subsection.",
    ("7.35.3.19", "Subsection B"):
        "Not amended.",
    ("7.35.3.19", "Subsection C"):
        "Metz recommendation, page 4, step 4: “Supervisory hours, Licensed Providers only (10 hours).”",
    ("7.35.3.19", "Subsection D"):
        "Metz recommendation, pages 3 and 4, steps 1 through 4, for the sequence and the hour figures. Wilson redline "
        "for the drafting: the steps are stated as sessions, and Paragraph (4) carries the remaining balance of hours, "
        "to be completed “in any manner of co-facilitation designed by the school or healing center hosting "
        "practicums that otherwise complies with the regulations of these provisions” (Wilson redline). "
        "Paragraph (1) is drafted in two versions; see the review note.",
    ("7.35.3.19", "Subsection E"):
        "Metz recommendation, page 4: “an approved supervisor at an approved location can host practicum students "
        "who are not enrolled at a co-located training program.”",
    ("7.35.3.19", "Subsection F"):
        "Wilson redline, new subsection: “A training program overseeing practicum treatments cannot also medically "
        "screen patients.”",
    ("7.35.3.19", "Subsection G"):
        "Not amended. Re-lettered.",
    ("7.35.3.19", "Subsection H"):
        "Metz recommendation, pages 4 and 5: 20 to 30 hours of supervision or consultation, with sign-off tied to two "
        "presented cases and a standardized evaluation form.",
    ("7.35.3.19", "Subsection I"):
        "Metz recommendation, page 5, end-of-life checkpoint.",
    ("7.35.3.19", "Subsection J"):
        "Not amended. Re-lettered.",
    ("7.35.3.19", "Subsection K"):
        "Not amended. Re-lettered.",
    ("7.35.3.20", "Section heading"):
        "Correction. The heading as published reads 7.34.3.20, while the history note at the end of the same section "
        "reads 7.35.3.20.",
    ("7.35.3.20", "Subsection H(5)"):
        "Permit name only. Metz recommendation, page 1, recommendation 1. Addendum C. No ratio is amended, and the "
        "qualified student provision is carried forward exactly as the department published it.",
    ("7.35.3.29", "Version 1"):
        "Medical Psilocybin Act, Section 5(B)(2), which exempts “a clinician administering or a qualified patient "
        "taking psilocybin in an approved setting”. Version 1 keeps the practicum inside that exemption, so no new "
        "section is required.",
    ("7.35.3.29", "Version 2"):
        "Metz recommendation, page 3, step 1: “Initial facilitation experience with well participants "
        "(approximately 30 hours). Two to three sessions as a facilitator in a retreat or peer-support model.” "
        "Version 2 requires an amendment to the Medical Psilocybin Act, stated in Subsection D of the section.",
}

REVIEW = {
    ("7.35.3.14", "Subsection C"):
        "This subsection conditions healing center staff authority on being “registered with the department.” "
        "No such registration is created anywhere in 7.35.3 NMAC or in 7.35.2 NMAC, so as published the condition "
        "cannot be satisfied. This draft does not fix it, because the fix is a new registration provision that belongs "
        "at 7.35.3.11 or 7.35.3.20, and neither section is within the scope of this document. The department should "
        "either create the registration or strike the condition.",
    ("7.35.3.18", "Subsection A"):
        "The rule sets no date by which the department must create or publish the New Mexico module, and every "
        "certification pathway in the rule is conditioned on completing it. No source in the record supplies a date, "
        "so none is drafted here. The committee should ask the department to state a date on the record.",
    ("7.35.3.18", "Subsection C, {{PT_C}} and facilitator psilocybin therapy module, lead-in"):
        "Settled at 68, and recorded here only so the divergence is visible. The New Mexico module is one of the ten "
        "content areas inside the 84 in the curriculum table on page 2 of the Metz recommendation, so it is subtracted "
        "along with the role-specific module and the simulated patient experience, leaving 68. The Wilson redline "
        "reads the same 84 as 80 didactic hours and strikes the simulated patient experience from the lead-in; that "
        "reading is not adopted. Either way the program totals 84 module hours, so nothing else in this draft moves "
        "if the committee later prefers her allocation.",
    ("7.35.3.18", "Subsection C, required topics"):
        "The Metz recommendation gives an illustrative range for each content area and states that the binding "
        "minimum is the total, so no per-topic minimum is drafted here. The Wilson redline reaches the same "
        "conclusion: “I haven’t added the specific hour requirements for each because I think that is a bit "
        "much for what needs to live in regulation” (comment 13). The ranges in the recommendation are: core "
        "psychotherapy skills and ethics 25 to 30; end-of-life and palliative care 10 to 15; trauma 8; medicine, "
        "dosing and clinical research literacy 8 to 10; New Mexico module 6 to 8; treatment models 6 to 8; screening, "
        "suicidality and crisis response 5 to 8; somatic awareness and therapeutic touch 4 to 6; history and "
        "traditional use 3 to 4; challenging experiences 2 to 4. No hour figure is given anywhere for "
        "post-traumatic stress disorder or for substance use disorder. If the committee wants any content area to "
        "carry a floor of its own, it has to say which areas and what floor, because nothing in the record supplies "
        "either.",
    ("7.35.3.19", "Subsection A"):
        "Three points, each of which needs a decision. First, the published phrase “half of the didactic "
        "requirements” does not identify half of what; the Wilson redline strikes the entry gate entirely, and "
        "this draft leaves it exactly as published rather than guess at the referent. Second, the published figure of "
        "80 hours of administration day sessions cannot fit inside a 62-hour practicum, so it is struck here and the "
        "step hours in Subsection D govern instead. Third, the published minimums of 14 different patients over eight "
        "different administration and same-day sessions are carried forward unchanged in this draft, while the Wilson "
        "redline strikes them; the committee should confirm whether those minimums are attainable within 62 hours, "
        "because if they are not, either the minimums or the total has to move.",
    ("7.35.3.19", "Subsection C"):
        "Settled: the supervision hours sit inside the practicum total, not on top of it. The published text is "
        "ambiguous, because it adds “an additional minimum of 20 hours” without saying what it is additional "
        "to, and this draft resolves it as inside. Two things confirm that reading. The Metz totals of approximately "
        "62 and 72 differ by exactly her 10 supervisory hours, so the recommendation treats supervision as inside the "
        "practicum total. The committee has directed the same reading. The published program total for the licensed "
        "provider is therefore 170 and the proposed total is 176.",
    ("7.35.3.19", "Subsection D"):
        "Two matters. First, Paragraph (1) is drafted in two versions because the Medical Psilocybin Act does not "
        "authorize a person who is not a qualified patient to take psilocybin. Version 1 performs the initial "
        "experience with qualified patients and works under the Act exactly as it stands today. Version 2 performs it "
        "with well participants in a retreat or peer-support model, as the Metz recommendation describes, and cannot "
        "operate until the Act is amended. Both versions carry the same hours, so the practicum total is 62 and 72 "
        "either way. The committee should choose one and, if it chooses Version 2, adopt the statutory request stated "
        "at 7.35.3.29. Second, the Metz recommendation states each step in hours while the Wilson redline states the "
        "first two in sessions; both are carried, with session minimums drafted and the Metz hour figures shown "
        "alongside. The Wilson redline sets the practicum totals at 60 and 70, and the Metz figures of 62 and 72 are "
        "the ones drafted at Subsection A.",
    ("7.35.3.19", "Subsection F"):
        "From the Wilson redline. The stated concern is that a training program has an interest in its own students "
        "being medically cleared, because practicum hours cannot be completed until patients are cleared. Separating "
        "the two functions removes that interest. No change to the drafting is needed unless the committee disagrees "
        "with the separation.",
    ("7.35.3.19", "Subsection H"):
        "The two sources put this requirement in different places and state it in different units. The Metz "
        "recommendation states 20 to 30 hours of supervision or consultation, drafted here at the low end of 20, with "
        "sign-off tied to two presented cases. The Wilson redline instead replaces the 10 mentoring hours at "
        "7.35.3.17 A with two student case consultations, states the requirement in cases rather than hours, and "
        "strikes the 12-month validity period. Dr. Metz, Ms. Wilson and Dr. Leeman should settle two things: whether "
        "the requirement is stated in hours, in cases, or in both, and whether it sits here at 7.35.3.19 H or at "
        "7.35.3.17 A. Note that 7.35.3.17 A is outside the scope of this document, so if they choose 7.35.3.17 A the "
        "amendment has to be drafted there.",
    ("7.35.3.19", "Subsection K"):
        "Two provisions set different group session minimums for the same 40 hours of contact time. Paragraph (4)(b) "
        "of this subsection requires “A minimum of one group session” while Subsection D(1) of 7.35.3.10 "
        "requires “two separate group sessions”. Neither is amended here, because 7.35.3.10 is outside the "
        "scope of this document and the two have to be reconciled together. The department should align them.",
    ("7.35.3.20", "Subsection H(5)"):
        "No training permit is proposed anywhere in this draft, and none is needed. At the July 17, 2026 Training and "
        "Education Committee meeting the department stated that a training permit “really wouldn’t be "
        "necessary with the model that we have” because a student is already covered “as them being a "
        "registered student with an educational program where they have that ability to be a part of those training "
        "sessions, including to conduct them under supervision” and that “those students already will have "
        "that kind of protection ability to be there as a part of being registered as a student with an educational "
        "program.” The department undertook to count students toward the ratio “rather than needing to "
        "create an entire other permit or certification level.” This paragraph as published is the result. "
        "Nothing further is required: a student conducts facilitation under supervision, while the acts 7.35.3.14 "
        "authorizes, purchase, possession, sale and administration, remain with the {{PT}}, the facilitator and the "
        "healing center. The rule is consistent with that division throughout. 7.35.3.19 B permits a student to "
        "“experience, observe, or conduct (when licensure allows) preparation or integration sessions.” "
        "7.35.3.20 D permits “students completing their practicums” to be present at an administration "
        "session. 7.35.3.17 C(2)(e) requires a program to record the “Names of facilitators supervised by "
        "practitioner students during practicum.” The phrase “training permit” appears nowhere in the "
        "rule as published, and the qualification parameter is the qualified student definition in this paragraph.",
    ("7.35.3.29", "Version 1"):
        "This is the version that operates under the Medical Psilocybin Act exactly as it stands today, and it "
        "requires no new section at all. Section 5(B)(2) of the Act exempts “a clinician administering or a "
        "qualified patient taking psilocybin in an approved setting”, and Section 3(H) defines a qualified "
        "patient by diagnosis with a qualifying condition, so psilocybin may lawfully be taken only by a qualified "
        "patient. Version 1 therefore performs the initial practicum experience with qualified patients, in the same "
        "settings and under the same supervision as the rest of the practicum. The cost is that a student first "
        "encounters a supervised administration session with a clinical population rather than before one, which is "
        "the sequencing the Metz recommendation was designed to avoid. The benefit is that the practicum is lawful "
        "on the day the rule takes effect. If the committee adopts Version 1, delete proposed 7.35.3.29 entirely and "
        "adopt Paragraph (1) of Subsection D of 7.35.3.19 in its Version 1 form.",
    ("7.35.3.29", "Version 2"):
        "This is the version the Metz recommendation describes, and it cannot operate until the Medical Psilocybin "
        "Act is amended. This draft states that requirement expressly rather than burying it. Section 5(B)(2) of the "
        "Act exempts only “a clinician administering or a qualified patient taking psilocybin in an approved "
        "setting”, and a practicum participant who is not a qualified patient falls outside it. Subsection D of "
        "the proposed section names the amendment required: the exemption in Section 5 has to reach a practicum "
        "participant taking psilocybin in an approved setting under department rule. Subsection C conditions the "
        "whole section on that amendment, so if the section is adopted and the Act is never amended, the section "
        "simply does not operate and nothing unlawful is authorized. The committee should decide whether to pursue "
        "the statutory amendment. If it does not, adopt Version 1.",
}


def source_for(section, sub):
    for (sec, key), text in SOURCE.items():
        if sec == section and sub.startswith(key):
            return text
    return None


def review_for(section, sub):
    for (sec, key), text in REVIEW.items():
        if sec == section and sub.startswith(key):
            return text
    return None

"""Citation and review note for each proposed change.

Sources are the Metz recommendation of July 17, 2026; the Wilson working redline
of July 25, 2026; the July 17, 2026 meeting transcripts; the Medical Psilocybin
Act; and the rule as published.
"""

SOURCE = {
    ("7.35.3.14", "Section heading"):
        "Two changes. Correction: the heading as published reads 7.34.3.14; the history note at the end of the same "
        "section reads 7.35.3.14. Permit title: Metz recommendation, page 1, recommendation 1. Addendum C.",
    ("7.35.3.14", "Subsection A"):
        "Consequential on proposed 7.35.3.29. The permit title is also conformed.",
    ("7.35.3.14", "Subsection B"):
        "Consequential on proposed 7.35.3.29.",
    ("7.35.3.14", "Subsection C"):
        "Not amended.",
    ("7.35.3.18", "Section heading"):
        "Permit title only. Metz recommendation, page 1, recommendation 1: retitle “Practitioner” as "
        "“Licensed Provider”. Addendum C.",
    ("7.35.3.18", "Subsection A"):
        "Metz recommendation, page 2, curriculum table: New Mexico module, 6 to 8 hours.",
    ("7.35.3.18", "Subsection C, {{PT_C}} and facilitator psilocybin therapy module, lead-in"):
        "Arithmetic. Metz recommendation, page 1, states a total of 84 hours. 84 less Subsection A (6), less "
        "Subsection D or E (5, unchanged), less the simulated patient experience (5, unchanged) leaves 68.",
    ("7.35.3.18", "Subsection C, required topics"):
        "Metz recommendation, pages 2 and 3, curriculum table, for paragraphs (16), (17), (20), (21), (22) and (23). "
        "July 17, 2026 Training and Education Committee transcript for paragraphs (18) and (19); both are qualifying "
        "conditions under Section 3(I) of the Medical Psilocybin Act. The Wilson redline adds the same content areas.",
    ("7.35.3.18", "Subsection E"):
        "Permit title only. Metz recommendation, page 1, recommendation 1. Addendum C. The five didactic hours are "
        "not amended.",
    ("7.35.3.18", "Subsection F"):
        "Correction. The sentence as published does not complete. The permit title is also conformed.",
    ("7.35.3.18", "Subsection G"):
        "Permit title only. Metz recommendation, page 1, recommendation 1. Addendum C. The 20 continuing education "
        "hours and the life support requirement are not amended.",
    ("7.35.3.18", "Subsection H"):
        "Metz recommendation, page 3: \u201cComponent ranges are illustrative; the binding minimum is the total.\u201d",
    ("7.35.3.19", "Section heading"):
        "Permit title only. Metz recommendation, page 1, recommendation 1. Addendum C.",
    ("7.35.3.19", "Subsection A"):
        "Metz recommendation, page 4: \u201capproximately 62 hours for Facilitators (steps 1-3); approximately 72 hours "
        "for Licensed Providers (steps 1-4).\u201d The permit title is also conformed.",
    ("7.35.3.19", "Subsection B"):
        "Not amended.",
    ("7.35.3.19", "Subsection C"):
        "Metz recommendation, page 4, step 4: \u201cSupervisory hours, Licensed Providers only (10 hours).\u201d",
    ("7.35.3.19", "Subsection D"):
        "Metz recommendation, pages 3 and 4, steps 1 through 4, for the sequence and the hour figures. Wilson redline "
        "for the drafting: the steps are stated as sessions, and Paragraph (4) carries the remaining balance of hours, "
        "to be completed \u201cin any manner of co-facilitation designed by the school or healing center hosting "
        "practicums that otherwise complies with the regulations of these provisions\u201d (Wilson redline).",
    ("7.35.3.19", "Subsection E"):
        "Metz recommendation, page 4: \u201can approved supervisor at an approved location can host practicum students "
        "who are not enrolled at a co-located training program.\u201d",
    ("7.35.3.19", "Subsection F"):
        "Wilson redline, new subsection: \u201cA training program overseeing practicum treatments cannot also medically "
        "screen patients.\u201d",
    ("7.35.3.19", "Subsection G"):
        "Not amended. Re-lettered.",
    ("7.35.3.19", "Subsection H"):
        "Metz recommendation, pages 4 and 5: 20 to 30 hours of supervision or consultation, sign-off tied to two "
        "presented cases with a standardized evaluation form.",
    ("7.35.3.19", "Subsection I"):
        "Metz recommendation, page 5, end-of-life checkpoint.",
    ("7.35.3.19", "Subsection J"):
        "Not amended. Re-lettered.",
    ("7.35.3.19", "Subsection K"):
        "Not amended. Re-lettered.",
    ("7.35.3.20", "Section heading"):
        "Correction. The heading as published reads 7.34.3.20; the history note at the end of the same section reads "
        "7.35.3.20.",
    ("7.35.3.20", "Subsection H(5)"):
        "Permit title only. Metz recommendation, page 1, recommendation 1. Addendum C. No ratio is amended.",
    ("7.35.3.29", "Entire section"):
        "Metz recommendation, page 3, step 1: \u201cInitial facilitation experience with well participants "
        "(approximately 30 hours). Two to three sessions as a facilitator in a retreat or peer-support model.\u201d",
}

REVIEW = {
    ("7.35.3.14", "Subsection C"):
        "This subsection conditions healing center staff authority on being registered with the department. No such "
        "registration appears in 7.35.3 NMAC or in 7.35.2 NMAC.",
    ("7.35.3.18", "Subsection A"):
        "The rule sets no date by which the department must create or publish this module. Every certification "
        "pathway is conditioned on it.",
    ("7.35.3.18", "Subsection C, {{PT_C}} and facilitator psilocybin therapy module, lead-in"):
        "68 follows from the 84-hour total after Subsection A, Subsection D or E, and the simulated patient "
        "experience. The Wilson redline reads the same 84 differently and sets this subsection at 80 didactic hours, "
        "striking the simulated patient experience from the lead-in. Which reading of the 84 governs?",
    ("7.35.3.18", "Subsection C, required topics"):
        "The Metz recommendation gives an illustrative range for each content area and states that the binding "
        "minimum is the total, so no per-topic minimum is drafted. The Wilson redline reaches the same conclusion: "
        "\u201cI haven\u2019t added the specific hour requirements for each because I think that is a bit much for what "
        "needs to live in regulation\u201d (comment 13). Ranges: core psychotherapy skills and ethics 25 to 30; end-of-life and "
        "palliative care 10 to 15; trauma 8; medicine, dosing and clinical research literacy 8 to 10; New Mexico module "
        "6 to 8; treatment models 6 to 8; screening, suicidality and crisis response 5 to 8; somatic awareness and "
        "therapeutic touch 4 to 6; history and traditional use 3 to 4; challenging experiences 2 to 4. Should any be "
        "drafted as a minimum? No hour figure is given for post-traumatic stress disorder or substance use disorder.",
    ("7.35.3.19", "Subsection A"):
        "Three points. The published phrase \u201chalf of the didactic requirements\u201d does not identify half of what; the "
        "Wilson redline strikes the entry gate entirely, this draft leaves it as published. The published figure of 80 "
        "hours of administration day sessions cannot sit within a 62-hour practicum, so it is struck and the step hours "
        "in Subsection D govern. The published minimums of 14 different patients over eight different sessions are "
        "carried forward here; the Wilson redline strikes them. Do they survive a 62-hour practicum?",
    ("7.35.3.19", "Subsection C"):
        "Subsection A sets 120 hours for a practitioner. This subsection adds \u201can additional minimum of 20 "
        "hours\u201d without identifying what it is additional to. Within the 120, the published practitioner total is "
        "170. On top of the 120, it is 190. The Metz totals of approximately 62 and 72 differ by exactly her 10 "
        "supervisory hours, so the recommendation treats them as within. This draft follows the recommendation, "
        "giving a proposed total of 176. Which reading governs?",
    ("7.35.3.19", "Subsection D"):
        "The Metz recommendation states each step in hours and the Wilson redline states the first two in sessions. "
        "Both are carried: the session minimums are drafted, the Metz hour figures are shown alongside, and Paragraph "
        "(4) carries the balance. The Wilson redline sets the totals at 60 and 70; the Metz figures of 62 and 72 are "
        "the ones drafted at Subsection A.",
    ("7.35.3.19", "Subsection F"):
        "From the Wilson redline. The stated concern is that a training program has an inherent interest in its own "
        "students being medically cleared so that practicum hours can be completed.",
    ("7.35.3.19", "Subsection H"):
        "The Wilson redline instead replaces the 10 mentoring hours at 7.35.3.17 A with two student case "
        "consultations, stating the requirement in cases rather than hours and striking the 12-month validity period. "
        "For Dr. Metz, Ms. Wilson and Dr. Leeman: hours, cases, or both, and does the requirement sit here or at "
        "7.35.3.17 A?",
    ("7.35.3.19", "Subsection K"):
        "Paragraph (4)(b) of this subsection requires \u201cA minimum of one group session\u201d while Subsection D(1) of "
        "7.35.3.10 requires \u201ctwo separate group sessions\u201d for the same 40 hours of contact time.",
    ("7.35.3.20", "Subsection H(5)"):
        "No ratio is amended here, and no training permit is proposed anywhere in this draft. At the July 17, 2026 "
        "Training and Education Committee meeting the department stated that a training permit \u201creally wouldn\u2019t be "
        "necessary with the model that we have\u201d because a student would already be covered \u201cas them being a "
        "registered student with an educational program\u201d and undertook to look at counting students toward the ratio "
        "\u201crather than needing to create an entire other permit or certification level.\u201d This paragraph is the "
        "result. The phrase \u201ctraining permit\u201d appears nowhere in the rule as published; the qualification "
        "parameter is the \u201cqualified student\u201d definition in this paragraph.",
    ("7.35.3.29", "Entire section"):
        "Section 5(B)(2) of the Medical Psilocybin Act reaches \u201ca clinician administering or a qualified patient "
        "taking psilocybin in an approved setting\u201d. Section 3(H) defines a qualified patient by diagnosis with a "
        "qualifying condition. A participant who is not a qualified patient falls outside both. Subsection C conditions "
        "this section accordingly.",
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

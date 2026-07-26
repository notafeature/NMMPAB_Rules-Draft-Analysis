"""Citation and review note for each proposed change."""

SOURCE = {
    ("7.35.3.14", "Section heading"):
        "Metz recommendation, page 4, training permit. Heading as published reads 7.34.3.14; the history note at the "
        "end of the same section reads 7.35.3.14.",
    ("7.35.3.14", "Subsection A"):
        "Consequential on proposed 7.35.3.29.",
    ("7.35.3.14", "Subsection B"):
        "Consequential on proposed 7.35.3.29.",
    ("7.35.3.14", "Subsection C"):
        "Not amended.",
    ("7.35.3.14", "Subsection D"):
        "Metz recommendation, page 4: a training permit “authorizing them to practice under supervision.”",
    ("7.35.3.18", "Subsection A"):
        "Metz recommendation, page 2, curriculum table: New Mexico module, 6 to 8 hours.",
    ("7.35.3.18", "Subsection C, {{PT_C}} and facilitator psilocybin therapy module, lead-in"):
        "Arithmetic. Metz recommendation, page 1, states a total of 84 hours. 84 less Subsection A (6), less "
        "Subsection D or E (5, unchanged), less the simulated patient experience (5, unchanged) leaves 68.",
    ("7.35.3.18", "Subsection C, required topics"):
        "Metz recommendation, pages 2 and 3, curriculum table, for paragraphs (16), (17), (20), (21), (22) and (23). "
        "July 17, 2026 Training and Education Committee transcript for paragraphs (18) and (19); both are qualifying "
        "conditions under Section 3(I) of the Medical Psilocybin Act.",
    ("7.35.3.18", "Subsection F"):
        "Correction. The sentence as published does not complete.",
    ("7.35.3.18", "Subsection H"):
        "Metz recommendation, page 3: “Component ranges are illustrative; the binding minimum is the total.”",
    ("7.35.3.19", "Subsection A"):
        "Metz recommendation, page 4: “approximately 62 hours for Facilitators (steps 1-3); approximately 72 hours "
        "for Licensed Providers (steps 1-4).”",
    ("7.35.3.19", "Subsection B"):
        "Not amended.",
    ("7.35.3.19", "Subsection C"):
        "Metz recommendation, page 4, step 4: “Supervisory hours, Licensed Providers only (10 hours).”",
    ("7.35.3.19", "Subsection D"):
        "Metz recommendation, pages 3 and 4, steps 1 through 4.",
    ("7.35.3.19", "Subsection E"):
        "Metz recommendation, page 4: “an approved supervisor at an approved location can host practicum students "
        "who are not enrolled at a co-located training program.”",
    ("7.35.3.19", "Subsection F"):
        "Not amended. Re-lettered.",
    ("7.35.3.19", "Subsection G"):
        "Metz recommendation, page 4, training permit.",
    ("7.35.3.19", "Subsection H"):
        "Metz recommendation, pages 4 and 5: 20 to 30 hours of supervision or consultation, sign-off tied to two "
        "presented cases with a standardized evaluation form.",
    ("7.35.3.19", "Subsection I"):
        "Metz recommendation, page 5, end-of-life checkpoint.",
    ("7.35.3.19", "Subsection J"):
        "Not amended. Re-lettered.",
    ("7.35.3.19", "Subsection K"):
        "Not amended. Re-lettered.",
    ("7.35.3.20", "Subsection H(5)"):
        "Consequential on the training permit at proposed 7.35.3.19 G. The 50-hour threshold is as published.",
    ("7.35.3.29", "Entire section"):
        "Metz recommendation, page 3, step 1: “Initial facilitation experience with well participants "
        "(approximately 30 hours). Two to three sessions as a facilitator in a retreat or peer-support model.”",
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
        "experience. If any of those three changes, 68 changes.",
    ("7.35.3.18", "Subsection C, required topics"):
        "The Metz recommendation gives an illustrative range for each content area and states that the binding "
        "minimum is the total, so no per-topic minimum is drafted. Ranges: core psychotherapy skills and ethics 25 to "
        "30; end-of-life and palliative care 10 to 15; trauma 8; medicine, dosing and clinical research literacy 8 to "
        "10; New Mexico module 6 to 8; treatment models 6 to 8; screening, suicidality and crisis response 5 to 8; "
        "somatic awareness and therapeutic touch 4 to 6; history and traditional use 3 to 4; challenging experiences "
        "2 to 4. Should any be drafted as a minimum? No hour figure is given for post-traumatic stress disorder or "
        "substance use disorder.",
    ("7.35.3.19", "Subsection A"):
        "Two points. The published phrase “half of the didactic requirements” does not identify half of "
        "what. The published figure of 80 hours of administration day sessions cannot sit within a 62-hour practicum, "
        "so it is struck and the step hours in Subsection D govern; the minimums of 14 different patients over eight "
        "different sessions are carried forward and should be confirmed as achievable in 62 hours.",
    ("7.35.3.19", "Subsection C"):
        "Subsection A sets 120 hours for a practitioner. This subsection adds “an additional minimum of 20 "
        "hours” without identifying what it is additional to. Within the 120, the published practitioner total is "
        "170. On top of the 120, it is 190. The Metz totals of approximately 62 and 72 differ by exactly her 10 "
        "supervisory hours, so the recommendation treats them as within. This draft follows the recommendation, "
        "giving a proposed total of 176. Which reading governs?",
    ("7.35.3.19", "Subsection G"):
        "The Metz recommendation states when the permit issues and what it authorizes. It states no term, renewal "
        "period, or application process, and none is drafted.",
    ("7.35.3.19", "Subsection K"):
        "Paragraph (4)(b) of this subsection requires \u201cA minimum of one group session.\u201d Subsection D(1) of "
        "7.35.3.10 requires \u201ctwo separate group sessions\u201d for the same 40 hours of contact time.",
    ("7.35.3.29", "Entire section"):
        "Section 5(B)(2) of the Medical Psilocybin Act reaches “a clinician administering or a qualified patient "
        "taking psilocybin in an approved setting.” Section 3(H) defines a qualified patient by diagnosis with a "
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

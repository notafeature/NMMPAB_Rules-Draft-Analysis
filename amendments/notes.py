"""Source line and review note for each proposed change.

SOURCE says where the change came from. Every entry names a document or the
meeting record. There is no "drafting" category, because nothing in the draft
is drafted from nothing.

REVIEW is the short note shown to reviewers where the published rule is
unclear or where a figure follows from arithmetic rather than from a
recommendation. It says what is unclear, what was done, and what to confirm.
"""

REC = "docs/documents/metz-recommendations-2026-07-17.pdf"

SOURCE = {
    ("7.35.3.14", "Section heading"):
        "Recommendation 3, training permit, page 4. Section-number correction: the heading as published reads "
        "7.34.3.14 while the history note at the end of the same section reads 7.35.3.14.",
    ("7.35.3.14", "Subsection A"):
        "Follows from proposed 7.35.3.29. Strike if 7.35.3.29 is not adopted.",
    ("7.35.3.14", "Subsection B"):
        "Follows from proposed 7.35.3.29. Strike if 7.35.3.29 is not adopted.",
    ("7.35.3.14", "Subsection C"):
        "Not amended.",
    ("7.35.3.14", "Subsection D"):
        "Recommendation 3, page 4: a training permit “authorizing them to practice under supervision”.",
    ("7.35.3.18", "Subsection A"):
        "Recommendation 2, curriculum table, page 2: New Mexico module 6 to 8 hours. Low end of the range.",
    ("7.35.3.18", "Subsection C, {{PT_C}} and facilitator psilocybin therapy module, lead-in"):
        "Arithmetic. Recommendation 2 sets a total of 84 hours, page 1. 84 less Subsection A (6), less Subsection D or "
        "E (5, unchanged), less the simulated patient experience (5, unchanged) leaves 68.",
    ("7.35.3.18", "Subsection C, required topics"):
        "Recommendation 2, curriculum table, pages 2 and 3, for content areas (16), (17), (20), (21), (22) and (23). "
        "July 17 Training and Education Committee record for (18) and (19), which were requested there and are "
        "qualifying conditions under Section 3(I) of the Medical Psilocybin Act.",
    ("7.35.3.18", "Subsection F"):
        "Correction only. The sentence as published does not complete.",
    ("7.35.3.18", "Subsection H"):
        "Recommendation 2, page 3: “Component ranges are illustrative; the binding minimum is the total.”",
    ("7.35.3.19", "Subsection A"):
        "Recommendation 3, page 4: “approximately 62 hours for Facilitators (steps 1-3); approximately 72 hours for "
        "Licensed Providers (steps 1-4)”.",
    ("7.35.3.19", "Subsection B"):
        "Not amended.",
    ("7.35.3.19", "Subsection C"):
        "Recommendation 3, step 4, page 4: “Supervisory hours, Licensed Providers only (10 hours)”.",
    ("7.35.3.19", "Subsection D"):
        "Recommendation 3, steps 1 to 4, pages 3 and 4. Hour figures and sequence as stated there.",
    ("7.35.3.19", "Subsection E"):
        "Recommendation 3, page 4: “an approved supervisor at an approved location can host practicum students who "
        "are not enrolled at a co-located training program”.",
    ("7.35.3.19", "Subsection F"):
        "Not amended. Re-lettered only.",
    ("7.35.3.19", "Subsection G"):
        "Recommendation 3, page 4, training permit paragraph. Wording tracks that paragraph.",
    ("7.35.3.19", "Subsection H"):
        "Recommendation 4, pages 4 and 5. Low end of the stated 20 to 30 range.",
    ("7.35.3.19", "Subsection I"):
        "Recommendation 4, page 5, end-of-life checkpoint.",
    ("7.35.3.19", "Subsection J"):
        "Not amended. Re-lettered only.",
    ("7.35.3.19", "Subsection K"):
        "Not amended. Re-lettered only.",
    ("7.35.3.20", "Subsection H(5)"):
        "Follows from the training permit in proposed 7.35.3.19 G. The 50-hour threshold is carried forward from the "
        "rule as published, unchanged.",
    ("7.35.3.29", "Entire section"):
        "Recommendation 3, step 1, page 3: “Initial facilitation experience with well participants (approximately 30 "
        "hours). Two to three sessions as a facilitator in a retreat or peer-support model.”",
}

REVIEW = {
    ("7.35.3.14", "Subsection C"):
        "Please review. The rule as published conditions healing center staff authority on being “registered with the "
        "department.” No registration for healing center owners or employees appears anywhere in 7.35.3 or in "
        "7.35.2 NMAC. Not amended here.",
    ("7.35.3.18", "Subsection A"):
        "Please review. The rule sets no date by which the department must create or publish this module, and every "
        "certification pathway is gated on it. Not amended here.",
    ("7.35.3.18", "Subsection C, {{PT_C}} and facilitator psilocybin therapy module, lead-in"):
        "Please review. 68 is arithmetic, not a recommended figure. It is what remains of the recommended 84-hour total "
        "after Subsection A, Subsection D or E, and the simulated patient experience. If any of those three change, "
        "this number changes with them.",
    ("7.35.3.18", "Subsection C, required topics"):
        "Please review. The recommendation gives an illustrative hour range for each content area and states that the "
        "binding minimum is the total, so no per-topic minimum is drafted. The ranges are: core psychotherapy skills "
        "and ethics 25 to 30; end-of-life and palliative care 10 to 15; trauma 8; medicine, dosing and clinical "
        "research literacy 8 to 10; New Mexico module 6 to 8; treatment models 6 to 8; screening, suicidality and "
        "crisis response 5 to 8; somatic awareness and therapeutic touch 4 to 6; history and traditional use 3 to 4; "
        "challenging experiences 2 to 4. Do you want any of these drafted as a minimum? The recommendation gives no "
        "hour figure for post-traumatic stress disorder or substance use disorder.",
    ("7.35.3.19", "Subsection A"):
        "Please review, two points. First, “half of the didactic requirements” does not say half of what; not "
        "amended here. Second, the published figure of 80 hours of administration day sessions cannot sit inside a "
        "62-hour practicum, so it is struck and the step hours in Subsection D govern; the minimums of 14 different "
        "patients over eight different sessions are carried forward unchanged and should be confirmed as achievable in "
        "62 hours.",
    ("7.35.3.19", "Subsection C"):
        "Please review. This is the one place where the rule as published can be read two ways, and it decides whether "
        "the recommendation raises or lowers the total. As published, Subsection A sets 120 hours for a practitioner "
        "and this subsection adds “an additional minimum of 20 hours” without saying what it is additional to. "
        "Inside the 120, the published practitioner total is 170. On top of the 120, it is 190. The recommendation's "
        "own totals of approximately 62 and 72 differ by exactly its 10 supervisory hours, so the recommendation treats "
        "them as inside. This draft follows the recommendation. The proposed practitioner total is 176, which is above "
        "170 and below 190. Please confirm which reading is correct.",
    ("7.35.3.19", "Subsection G"):
        "Please review. The recommendation describes the permit and when it issues. It does not state a term, a renewal "
        "period, or an application process, and none is drafted.",
    ("7.35.3.19", "Subsection K"):
        "Please review. Paragraph (4)(b) of this subsection requires “a minimum of one group session.” "
        "7.35.3.10 D(1) requires “two separate group sessions” for the same 40 hours of contact time. The two "
        "waivers do not agree. Not amended here.",
    ("7.35.3.29", "Entire section"):
        "Please review. Section 5(B)(2) of the Medical Psilocybin Act makes lawful “a clinician administering or a "
        "qualified patient taking psilocybin in an approved setting,” and Section 3(H) defines a qualified patient "
        "by diagnosis with a qualifying condition. A practicum participant who is not a qualified patient falls outside "
        "that. This section is offered as the language that would be needed if the Act is amended, and Subsection C "
        "says so.",
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

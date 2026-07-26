"""Published text and proposed amendment, provision by provision.

Where the Metz recommendation states a range, the low end is used and the range
is shown in a badge. Where the rule as published is unclear, the published text
is left as it stands and the question is stated at that provision.
"""

NEW = "There is no current language. This provision does not exist in the proposed rule as published."
UNCHANGED = "__UNCHANGED__"


def ins(t):
    return '<ins>%s</ins>' % t


def dele(t):
    return '<del>%s</del>' % t


def rng(t):
    """Badge showing the recommended range behind a figure."""
    return '<span class="rangebadge">%s</span>' % t


# (section, subsection label, published text, proposed html)
P = []

# ---------------------------------------------------------------------------
# 7.35.3.14
# ---------------------------------------------------------------------------

P.append((
    "7.35.3.14",
    "Section heading and lead-in",
    "7.34.3.14 AUTHORIZED POSSESSION, PURCHASE, OR SALE OF MEDICAL PSILOCYBIN BY "
    "PRACTITIONERS, FACILITATORS, HEALING CENTER OWNERS AND EMPLOYEES: Certification of "
    "a practitioner, facilitator, or healing center shall enable practitioners, facilitators, and owners and employees of "
    "healing centers to do the following, in accordance with medical psilocybin program rules:",
    dele("7.34.3.14") + " " + ins("7.35.3.14") + " AUTHORIZED POSSESSION, PURCHASE, OR SALE OF MEDICAL PSILOCYBIN BY "
    "{{PTS_UC}}, FACILITATORS, HEALING CENTER OWNERS AND EMPLOYEES: Certification of "
    "a {{PT}}, facilitator, or healing center shall enable {{PTS}}, facilitators, and owners and employees of "
    "healing centers to do the following, in accordance with medical psilocybin program rules:",
))

P.append((
    "7.35.3.14",
    "Subsection A, {{PTS_C}}",
    "(A) Practitioners: Practitioners may purchase and possess medical psilocybin products obtained from "
    "permitted producers, and may sell or otherwise provide medical psilocybin products to qualified patients during "
    "administration sessions conducted at a healing center location or other approved location. A practitioner may only "
    "sell or otherwise provide psilocybin products that are obtained from permitted producers.",
    "(A) {{PTS_C}}: {{PTS_C}} may purchase and possess medical psilocybin products obtained from "
    "permitted producers, and may sell or otherwise provide medical psilocybin products to qualified patients"
    + ins(", or to practicum participants in accordance with 7.35.3.29 NMAC,") + " during "
    "administration sessions conducted at a healing center location or other approved location. A {{PT}} may only "
    "sell or otherwise provide psilocybin products that are obtained from permitted producers.",
))

P.append((
    "7.35.3.14",
    "Subsection B, Facilitators",
    "(B) Facilitators: Facilitators may possess medical psilocybin products, for the purpose of providing "
    "those products to qualified patients in administration sessions conducted at healing centers and other approved "
    "locations.",
    "(B) Facilitators: Facilitators may possess medical psilocybin products, for the purpose of providing "
    "those products to qualified patients" + ins(", or to practicum participants in accordance with 7.35.3.29 NMAC,")
    + " in administration sessions conducted at healing centers and other approved locations.",
))

P.append((
    "7.35.3.14",
    "Subsection C, Healing centers",
    "(C) Healing centers: Owners and employees of healing centers who are registered with the "
    "department may purchase medical psilocybin products from permitted producers, may possess medical psilocybin "
    "products, and may sell or otherwise administer those products to qualified patients in administration sessions "
    "conducted at the healing center or other approved locations, provided that such individuals are also designated to "
    "engage in each activity by the healing center. A healing center may only sell or otherwise provide psilocybin "
    "products that are obtained from permitted producers.",
    UNCHANGED,
))

# ---------------------------------------------------------------------------
# 7.35.3.18
# ---------------------------------------------------------------------------

P.append((
    "7.35.3.18",
    "Section heading",
    "7.35.3.18 EDUCATIONAL REQUIREMENTS FOR CERTIFYING CLINICIANS, PRACTITIONERS, AND FACILITATORS:",
    "7.35.3.18 EDUCATIONAL REQUIREMENTS FOR CERTIFYING CLINICIANS, {{PTS_UC}}, AND FACILITATORS:",
))

P.append((
    "7.35.3.18",
    "Subsection A, New Mexico educational module",
    "A. Requirements for certifying clinician, practitioner, and facilitator certification: All certifying "
    "clinicians, practitioners, and facilitators who provide medical psilocybin services, including all such providers who "
    "are certified by the department on the basis of having completed an educational program from another jurisdiction, "
    "shall complete a New Mexico educational module created or approved by the department prior to applying for "
    "certification, which shall include at a minimum:",
    "A. Requirements for certifying clinician, {{PT}}, and facilitator certification: All certifying "
    "clinicians, {{PTS}}, and facilitators who provide medical psilocybin services, including all such providers who "
    "are certified by the department on the basis of having completed an educational program from another jurisdiction, "
    "shall complete a New Mexico educational module created or approved by the department"
    + ins(", consisting of a minimum of six didactic hours,") + rng("Metz: 6 to 8")
    + " prior to applying for certification, which shall include at a minimum: "
    "<span class='note'>Paragraphs (1) through (5) not amended.</span>",
))

P.append((
    "7.35.3.18",
    "Subsection B, certifying clinician module",
    UNCHANGED,
    UNCHANGED,
))

P.append((
    "7.35.3.18",
    "Subsection C, {{PT_C}} and facilitator psilocybin therapy module, lead-in",
    "C. Requirements for initial practitioner and facilitator certification: All practitioners and "
    "facilitators shall complete a psilocybin therapy module consisting of a minimum of 30 didactic hours and 5 hours of "
    "simulated patient experience, prior to applying for certification, which shall include:",
    "C. Requirements for initial {{PT}} and facilitator certification: All {{PTS}} and "
    "facilitators shall complete a psilocybin therapy module consisting of a minimum of " + dele("30") + " " + ins("68")
    + " didactic hours and 5 hours of simulated patient experience, prior to applying for certification, which shall "
    "include:",
))

P.append((
    "7.35.3.18",
    "Subsection C, required topics",
    "(1) Overview of practitioner/facilitator responsibilities including how to work as part of a care team;\n"
    "(2) 42 CFR part 2;\n"
    "(3) Trauma-Informed Care\n"
    "(4) Psychedelic emergencies/urgencies/medical monitoring;\n"
    "(5) Psilocybin actions, interactions and pharmacology;\n"
    "(6) Set and setting;\n"
    "(7) Ethics in therapeutic settings;\n"
    "(8) Patient-centered approaches and care;\n"
    "(9) Preparation and integration sessions;\n"
    "(10) Administration session;\n"
    "(11) Dosing;\n"
    "(12) Psychedelic de-escalation techniques;\n"
    "(13) Non-ordinary states of consciousness;\n"
    "(14) Self-care;\n"
    "(15) Research and data collection requirements;\n"
    "(16) A simulated patient experience of no less than 5 hours; and\n"
    "(17) Evaluation to demonstrate competency in the above areas.",
    "(1) Overview of {{PT}}/facilitator responsibilities including how to work as part of a care team;<br>"
    "(2) 42 CFR part 2;<br>"
    "(3) Trauma-Informed Care;<br>"
    "(4) Psychedelic emergencies/urgencies/medical monitoring;<br>"
    "(5) Psilocybin actions, interactions and pharmacology;<br>"
    "(6) Set and setting;<br>"
    "(7) Ethics in therapeutic settings;<br>"
    "(8) Patient-centered approaches and care;<br>"
    "(9) Preparation and integration sessions;<br>"
    "(10) Administration session;<br>"
    "(11) Dosing;<br>"
    "(12) Psychedelic de-escalation techniques;<br>"
    "(13) Non-ordinary states of consciousness;<br>"
    "(14) Self-care;<br>"
    "(15) Research and data collection requirements;<br>"
    + ins("(16) End-of-life and palliative care;") + "<br>"
    + ins("(17) Screening, suicidality, and crisis response;") + "<br>"
    + ins("(18) Substance use disorder;") + "<br>"
    + ins("(19) Post-traumatic stress disorder;") + "<br>"
    + ins("(20) Somatic awareness and therapeutic touch;") + "<br>"
    + ins("(21) History and traditional use of psilocybin and other psychedelics;") + "<br>"
    + ins("(22) Individual and group treatment models;") + "<br>"
    + ins("(23) Challenging experiences, including hallucinogen persisting perception disorder;") + "<br>"
    + dele("(16)") + " " + ins("(24)") + " A simulated patient experience of no less than 5 hours; and<br>"
    + dele("(17)") + " " + ins("(25)") + " Evaluation to demonstrate competency in the above areas.",
))

P.append((
    "7.35.3.18",
    "Subsection D, additional facilitator module",
    UNCHANGED,
    UNCHANGED,
))

P.append((
    "7.35.3.18",
    "Subsection E, additional {{PT_C}} module, lead-in",
    "E. Additional requirements for initial practitioner certification: All practitioners shall complete a "
    "module on psychedelic and psilocybin therapeutic approaches consisting of a minimum of five didactic hours, prior "
    "to applying for certification, which shall include:",
    "E. Additional requirements for initial {{PT}} certification: All {{PTS}} shall complete a "
    "module on psychedelic and psilocybin therapeutic approaches consisting of a minimum of five didactic hours, prior "
    "to applying for certification, which shall include: "
    "<span class='note'>Paragraphs (1) through (3) not amended.</span>",
))

P.append((
    "7.35.3.18",
    "Subsection F, {{PT_C}} and facilitator trainings, lead-in",
    "F. Practitioner and facilitator trainings: All practitioners and facilitators shall also complete and "
    "maintain proof of current certification prior to applying for medical psilocybin certification in:",
    "F. {{PT_C}} and facilitator trainings: All {{PTS}} and facilitators shall "
    + dele("also complete and maintain proof of current certification prior to applying for medical psilocybin certification in:")
    + ins("complete and maintain the following prior to applying for medical psilocybin certification:")
    + " <span class='note'>Paragraphs (1) and (2) not amended. Corrects a sentence that does not complete as published. "
      "No obligation changes.</span>",
))

P.append((
    "7.35.3.18",
    "Subsection G, continuing education",
    "G. Continuing education requirements for certifying clinicians, practitioners and facilitators:\n"
    "(1) Certifying clinicians: Certifying clinicians shall complete a minimum of eight hours of continuing medical "
    "education credits specific to psychedelic medicine or therapy every two years.\n"
    "(2) Practitioners and facilitators: Practitioners and facilitators shall complete a minimum of 20 hours of "
    "continuing education credits specific to psychedelic therapy and practice every two years. Practitioners and "
    "facilitators shall also keep current with their basic life support, or cardiopulmonary resuscitation and automated "
    "external defibrillation certification, or emergency medical technician licensure in addition to the 20 hours of "
    "continuing education credits.",
    "G. Continuing education requirements for certifying clinicians, {{PTS}} and facilitators:<br>"
    "(1) Certifying clinicians: Certifying clinicians shall complete a minimum of eight hours of continuing medical "
    "education credits specific to psychedelic medicine or therapy every two years.<br>"
    "(2) {{PTS_C}} and facilitators: {{PTS_C}} and facilitators shall complete a minimum of 20 hours of "
    "continuing education credits specific to psychedelic therapy and practice every two years. {{PTS_C}} and "
    "facilitators shall also keep current with their basic life support, or cardiopulmonary resuscitation and automated "
    "external defibrillation certification, or emergency medical technician licensure in addition to the 20 hours of "
    "continuing education credits.",
))

P.append((
    "7.35.3.18",
    "Subsection H, total module hours",
    NEW,
    ins("H. Total module hours: The requirements of Subsections A, C and D of this section shall together total a "
        "minimum of 84 hours for a facilitator applicant. The requirements of Subsections A, C and E of this section "
        "shall together total a minimum of 84 hours for a {{NPT}} applicant. The hours stated for each module in this "
        "section are minimums within that total."),
))

# ---------------------------------------------------------------------------
# 7.35.3.19
# ---------------------------------------------------------------------------

P.append((
    "7.35.3.19",
    "Section heading",
    "7.35.3.19 PRACTICUM REQUIREMENTS FOR PRACTITIONERS AND FACILITATORS:",
    "7.35.3.19 PRACTICUM REQUIREMENTS FOR {{PTS_UC}} AND FACILITATORS:",
))

P.append((
    "7.35.3.19",
    "Subsection A, minimum practicum hours; administration day sessions",
    "A. Minimum practicum hours; administration day sessions: An individual who seeks to become "
    "certified as a practitioner or facilitator shall participate in supervised practice training, otherwise referred to as a "
    "\u201cpracticum\u201d, after completing at least half of the didactic requirements and all of the simulated patient requirements "
    "of the educational requirements. The practicum shall consist of a minimum of 100 hours of supervised practice "
    "training for facilitators and 120 hours for practitioners and shall be completed prior to applying for certification. "
    "Students shall participate in a minimum of 80 hours of administration day sessions, where students are provided the "
    "opportunity to experience, observe, or conduct supervised facilitation of administration day sessions in-person with "
    "a minimum of 14 different patients over a minimum of eight different administration and same-day sessions with the "
    "following criteria:",
    "A. Minimum practicum hours; administration day sessions: An individual who seeks to become "
    "certified as a {{PT}} or facilitator shall participate in supervised practice training, otherwise referred to as a "
    "\u201cpracticum\u201d, after completing at least half of the didactic requirements and all of the simulated patient "
    "requirements of the educational requirements. The practicum shall consist of a minimum of "
    + dele("100") + " " + ins("62") + rng("Metz: approx. 62")
    + " hours of supervised practice training for facilitators and " + dele("120") + " " + ins("72")
    + rng("Metz: approx. 72")
    + " hours for {{PTS}} and shall be completed prior to applying for certification. Students shall participate in "
    + dele("a minimum of 80 hours of administration day sessions, where students are")
    + ins("administration day sessions as required by Subsection D of this section, where students are")
    + " provided the opportunity to experience, observe, or conduct supervised facilitation of administration day "
    "sessions in-person with a minimum of 14 different patients over a minimum of eight different administration and "
    "same-day sessions with the following criteria: "
    "<span class='note'>Paragraphs (1) and (2), the patient and session minimums, not amended.</span>",
))

P.append((
    "7.35.3.19",
    "Subsection B, minimum practicum hours; preparation and integration sessions",
    "B. Minimum practicum hours; in-person and integration sessions: Students shall participate in a "
    "minimum of 20 hours of in-person preparation and integration sessions, where students are provided the opportunity "
    "to experience, observe, or conduct (when licensure allows) preparation or integration sessions. This shall include a "
    "minimum of six different patients during individual sessions. This shall include at least one group preparatory and "
    "one group integration session with a minimum of four or more patients.",
    UNCHANGED,
))

P.append((
    "7.35.3.19",
    "Subsection C, {{PT_C}} supervision hours",
    "C. Practitioner supervision hours: Practitioners shall complete an additional minimum of 20 hours "
    "as a practitioner supervising facilitators during in-person administration day sessions, which shall include a "
    "minimum of two different patients during individual administration day sessions, and a minimum of one group "
    "administration day sessions with a minimum of four or more patients in the group.",
    "C. {{PT_C}} supervision hours: {{PTS_C}} shall complete an additional minimum of "
    + dele("20") + " " + ins("10") + rng("Metz: 10")
    + " hours as a {{PT}} supervising facilitators during in-person administration day sessions, which shall include a "
    "minimum of two different patients during individual administration day sessions, and a minimum of one group "
    "administration day sessions with a minimum of four or more patients in the group.",
))

P.append((
    "7.35.3.19",
    "Subsection D, practicum sequence",
    NEW,
    ins("D. Practicum sequence: The practicum required by Subsection A of this section consists of the following, in "
        "sequence:") + "<br>"
    + ins("(1) Initial facilitation experience: students shall begin the practicum by completing a minimum of two "
          "sessions as a facilitator in a retreat or peer-support model with well participants, in accordance with "
          "7.35.3.29 NMAC. Practicum session experience shall include preparation, administration, and integration;")
    + rng("Metz: approx. 30 hours") + "<br>"
    + ins("(2) Co-facilitation experience: after completing the initial facilitation experience, students shall complete "
          "a minimum of two sessions co-facilitated with a department-permitted {{NPT}}, with patients presenting a "
          "low-acuity qualifying condition. Practicum session experience shall include preparation, administration, and "
          "integration;") + rng("Metz: approx. 20 hours") + "<br>"
    + ins("(3) Group practicum: direct participation in group preparation, administration, and integration sessions; "
          "and") + rng("Metz: approx. 12 hours") + "<br>"
    + ins("(4) Additional experience: students may complete the remaining balance of the hours required by Subsection A "
          "of this section in any manner of co-facilitation designed by the educational program or healing center "
          "hosting the practicum that otherwise complies with this rule. For {{NPT}} applicants, the supervision hours "
          "required by Subsection C of this section count toward that balance."),
))

P.append((
    "7.35.3.19",
    "Subsection E, practicum location (published Subsection D)",
    "D. Practicum location: All practicum hours shall take place in an approved healing center or other "
    "approved location.",
    dele("D.") + " " + ins("E.") + " Practicum location: All practicum hours shall take place in an approved healing "
    "center or other approved location. "
    + ins("An approved supervisor at an approved location may host practicum students who are not enrolled at a "
          "co-located training program."),
))

P.append((
    "7.35.3.19",
    "Subsection F, independent medical screening",
    NEW,
    ins("F. Independent medical screening required: A training program overseeing practicum treatments shall not also "
        "medically screen patients. Medical screening shall be conducted independently by the clinician with the "
        "hosting healing center or another certifying clinician not affiliated with the training program."),
))

P.append((
    "7.35.3.19",
    "Subsection G, practicum standards (published Subsection E)",
    "E. Practicum standards: Practicum supervisors and students shall follow these rules as they apply "
    "to facilitation and therapy, shall comply with HIPAA and HITECH confidentiality requirements, and shall comport "
    "with applicable limits on scope of practice.",
    dele("E.") + " " + ins("G.") + " Practicum standards: Practicum supervisors and students shall follow these rules as "
    "they apply to facilitation and therapy, shall comply with HIPAA and HITECH confidentiality requirements, and shall "
    "comport with applicable limits on scope of practice. <span class='note'>Re-lettered only. Text not amended.</span>",
))

P.append((
    "7.35.3.19",
    "Subsection H, supervision and consultation; case presentation sign-off",
    NEW,
    ins("H. Supervision and consultation; case presentation sign-off:") + "<br>"
    + ins("(1) An applicant for certification shall complete a minimum of 20 hours of supervision or consultation after "
          "the practicum is completed, in addition to the practicum hours required by this section;") + rng("Metz: 20 to 30") + "<br>"
    + ins("(2) sign-off is tied to case presentation. The applicant shall present a minimum of two cases of clients the "
          "applicant has personally worked with using regulated medicine. Each case presentation shall take the form of "
          "a biopsychosocial case conceptualization, including a discussion of presenting concerns, risk factors, "
          "supportive factors, treatment considerations, and recommendations for aftercare; and") + "<br>"
    + ins("(3) the consultant or supervisor shall complete a standardized evaluation form on each case presented."),
))

P.append((
    "7.35.3.19",
    "Subsection I, end-of-life practice",
    NEW,
    ins("I. End-of-life practice: Before serving end-of-life participants independently, a {{NPT}} or facilitator shall "
        "complete at least one co-facilitated end-of-life case and present at least one end-of-life case in supervision "
        "or consultation."),
))

P.append((
    "7.35.3.19",
    "Subsection J, waiver of practicum requirements (published Subsection F)",
    "F. Waiver of practicum requirements: The department may otherwise waive, temporarily suspend, "
    "or reduce the practicum requirements for individuals applying for certification, in order to facilitate the certification "
    "of individuals trained by other government-approved programs, and to build the initial infrastructure of the program.",
    dele("F.") + " " + ins("J.") + " Waiver of practicum requirements: The department may otherwise waive, temporarily "
    "suspend, or reduce the practicum requirements for individuals applying for certification, in order to facilitate "
    "the certification of individuals trained by other government-approved programs, and to build the initial "
    "infrastructure of the program. <span class='note'>Re-lettered only. Text not amended.</span>",
))

P.append((
    "7.35.3.19",
    "Subsection K, waiver for applications received by December 31, 2027 (published Subsection G)",
    "G. Waiver of practicum hours requirement for applications received by December 31, 2027: An "
    "applicant for certification shall not be required to satisfy the full New Mexico practicum hours requirement if the "
    "applicant:\n"
    "(1) Applies for certification by December 31, 2027;\n"
    "(2) Completes the didactic requirements by December 31, 2027;\n"
    "(3) Graduates from an educational program that the department certifies by December 31, 2027 or that the "
    "department has included on the department-approved list of educational programs by December 31, 2027; and\n"
    "(4) Demonstrates completion of at least 40 hours of contact time through logs or other records of the sessions, "
    "including:\n"
    "(a) A minimum of two separate individual sessions including the appointments for preparation, administration and "
    "integration; and\n"
    "(b) A minimum of one group session including the appointments for preparation, administration, and integration.",
    dele("G.") + " " + ins("K.") + " Waiver of practicum hours requirement for applications received by December 31, "
    "2027: <span class='note'>Re-lettered only. Paragraphs (1) through (4) not amended.</span>",
))

# ---------------------------------------------------------------------------
# 7.35.3.20
# ---------------------------------------------------------------------------

P.append((
    "7.35.3.20",
    "Section heading and lead-in",
    "7.34.3.20 REQUIREMENTS FOR HEALING CENTERS AND OTHER APPROVED LOCATIONS: A healing center and a "
    "registrant of another approved location shall comply with the following requirements:",
    dele("7.34.3.20") + " " + ins("7.35.3.20") + " REQUIREMENTS FOR HEALING CENTERS AND OTHER APPROVED LOCATIONS: A "
    "healing center and a registrant of another approved location shall comply with the following requirements: "
    "<span class='note'>Subsections A through G and I not amended. Of Subsection H, only Paragraph (5) is "
    "reproduced.</span>",
))

P.append((
    "7.35.3.20",
    "Subsection H(5), staffing ratios",
    "(5) Includes procedures to ensure that there are practitioners and facilitators present at all "
    "times during an administration session with a minimum of one practitioner and one facilitator for individual patient "
    "sessions; and in group administration sessions a minimum of one practitioner for every eight patients and a "
    "minimum of one facilitator or qualified student for every two patients. For purposes of the foregoing provision, a "
    "student shall be deemed qualified if they are registered with a certified educational program and they have "
    "completed at least 50 hours of their practicum. Exception: the department may waive or decrease this ratio if the "
    "department determines that the ratio specified presents a barrier for patients and that safety concerns are otherwise "
    "alleviated.",
    "(5) Includes procedures to ensure that there are {{PTS}} and facilitators present at all "
    "times during an administration session with a minimum of one {{PT}} and one facilitator for individual patient "
    "sessions; and in group administration sessions a minimum of one {{PT}} for every eight patients and a "
    "minimum of one facilitator or qualified student for every two patients. For purposes of the foregoing provision, a "
    "student shall be deemed qualified if they are registered with a certified educational program and they have "
    "completed at least 50 hours of their practicum. Exception: the department may waive or decrease this ratio if the "
    "department determines that the ratio specified presents a barrier for patients and that safety concerns are otherwise "
    "alleviated.",
))

# ---------------------------------------------------------------------------
# 7.35.3.29
# ---------------------------------------------------------------------------

P.append((
    "7.35.3.29",
    "Entire section, practicum participants who are not qualified patients",
    NEW,
    ins("7.35.3.29 PRACTICUM PARTICIPANTS WHO ARE NOT QUALIFIED PATIENTS:") + "<br>"
    + ins("A. Purpose: This section provides for the stage of the practicum described in Paragraph (1) of Subsection D "
          "of 7.35.3.19 NMAC to be conducted with practicum participants who are not qualified patients, so that a "
          "student gains supervised exposure to non-ordinary states before working with clinical populations.") + "<br>"
    + ins("B. Practicum participant: A practicum participant is an individual who is not a qualified patient and who "
          "takes part in a practicum session in a retreat or peer-support model. Preparation and integration sessions "
          "are required for each participant.") + "<br>"
    + ins("C. Effect: This section applies only to the extent that the Medical Psilocybin Act, Sections 26-2D-1 through "
          "-11 NMSA 1978, authorizes the administration of medical psilocybin to a person who is not a qualified "
          "patient."),
))

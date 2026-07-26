"""Published text and proposed amendment, provision by provision.

Scope: the twenty-four sections of 7.35.3 NMAC that the practicum amendment
draft in `amendments/` does not reach, namely 7.35.3.1 through .13, .15, .16,
.17, and .21 through .28.

Every left-column string is the rule as published on July 23, 2026, reproduced
verbatim, with line breaks introduced by the PDF collapsed to single spaces and
hyphenation introduced by a line break rejoined. Nothing else is altered.
`build-redline-pdf.py` aborts unless every one of them matches the text layer of
the published PDF by exact contiguous match.

No figure appears in a right column unless a source carries it. Where the fix
for a defect would require a figure that no source supplies, or would require a
choice this record cannot make, the published text is left as it stands and the
question is stated at that provision in `notes.py`.
"""

NEW = "There is no current language. This provision does not exist in the proposed rule as published."
UNCHANGED = "__UNCHANGED__"

# Document keys. `build-redline-pdf.py` builds one PDF per key, in this order.
# Regrouping the draft is an edit to this table and to the `doc` field of each
# entry below. Nothing else depends on the split.
D1 = "framework"
D2 = "education"
D3 = "locations"
D4 = "process"


def ins(t):
    return '<ins>%s</ins>' % t


def dele(t):
    return '<del>%s</del>' % t


def rng(t):
    """Badge showing the range or the source figure behind a figure."""
    return '<span class="rangebadge">%s</span>' % t


# (doc, section, subsection label, published text, proposed html)
P = []


# ===========================================================================
# D1. Framework and defined terms: 7.35.3.1 through .7
# ===========================================================================

P.append((
    D1,
    "7.35.3.2",
    "Entire section, scope",
    "7.35.3.2 SCOPE: This rule applies to all patients, practitioners, clinicians, facilitators, healing "
    "centers and other approved locations, and educational programs who participate or seek to participate in "
    "the New Mexico medical psilocybin program.",
    UNCHANGED,
))

P.append((
    D1,
    "7.35.3.3",
    "Entire section, statutory authority",
    "7.35.3.3 STATUTORY AUTHORITY: This rule is promulgated pursuant to the following statutory authorities: "
    "the New Mexico Department of Health Act, Subsection E of Section 9-7-6 NMSA 1978; and the Medical "
    "Psilocybin Act, Section 26-2D-7, NMSA 1978.",
    UNCHANGED,
))

P.append((
    D1,
    "7.35.3.5",
    "Entire section, effective date",
    "7.35.3.5 EFFECTIVE DATE: xx/xx, 2026, unless a later date is cited at the end of a section.",
    UNCHANGED,
))

P.append((
    D1,
    "7.35.3.7",
    "Entire section, definitions",
    "7.35.3.7 DEFINITIONS: The definitions in 7.35.2.7 NMAC apply to this part.",
    "7.35.3.7 DEFINITIONS: " + ins("A.") + " The definitions in 7.35.2.7 NMAC apply to this part."
    + "<br>" + ins("B. In addition to the definitions in 7.35.2.7 NMAC, the following definitions apply to this "
                   "part:") + "<br>"
    + ins("(1) &#8220;Certificant&#8221; means a practitioner, certifying clinician, facilitator, healing "
          "center or other approved location, or educational program that holds a certification issued by the "
          "department under this part.") + "<br>"
    + ins("(2) &#8220;Facilitator&#8221; means an individual who is certified by the department under this "
          "part to work alongside a practitioner during medical psilocybin services, under the direct "
          "supervision of a practitioner, and to provide peer support to qualified patients as well as "
          "logistical and administrative support to the practitioner and to the healing center.") + "<br>"
    + ins("(3) &#8220;Other approved location&#8221; means a physical location at which medical psilocybin "
          "is intended to be consumed, that is not the location of a healing center, and that holds a "
          "temporary certification issued by the department under Subsection B of 7.35.3.11 NMAC.") + "<br>"
    + ins("(4) &#8220;Practicum&#8221; means the supervised practice training required of an individual who "
          "seeks to become certified as a practitioner or facilitator under 7.35.3.19 NMAC.") + "<br>"
    + ins("(5) &#8220;Registrant of another approved location&#8221; means the practitioner or facilitator "
          "who holds a certification of an other approved location issued under Subsection B of 7.35.3.11 "
          "NMAC.") + "<br>"
    + ins("(6) &#8220;Student&#8221; means an individual who is registered with a psilocybin educational "
          "program certified by the department under this part."),
))


# ===========================================================================
# D2. Educational programs: 7.35.3.10, .12, .15, .16, .17
# ===========================================================================

P.append((
    D2,
    "7.35.3.10",
    "Paragraph (2) of Subsection A, additions to the list",
    "(2) Educational programs shall be added to the list when an application for certification as a "
    "certifying clinician, practitioner, or facilitator is submitted and approved based on the applicant's "
    "completion of the out-of-state educational program.",
    UNCHANGED,
))

P.append((
    D2,
    "7.35.3.10",
    "Paragraph (2) of Subsection B, documentation of equivalency",
    "(2) Documentation of either: (a) Completion of a government approved psilocybin educational program from "
    "another jurisdiction, which shall include: (i) Documentation that the curriculum of the educational "
    "program is equivalent to the didactic educational requirements applicable for New Mexico certification; "
    "and (ii) For all applications received on or after January 1, 2028, documentation of a third-party "
    "evaluation of the curriculum demonstrating such equivalency; (b) Completion of a psilocybin educational "
    "program from another jurisdiction that is developed in collaboration with higher education institutions "
    "or government-approved psychedelic research studies, which shall include: (i) Documentation that the "
    "curriculum of the educational program is equivalent to the didactic educational requirements applicable "
    "for New Mexico certification, and (ii) For all applications received on or after January 1, 2028, "
    "documentation of a third-party evaluation of the curriculum demonstrating such equivalency; or (c) "
    "Completion of an educational program that is currently included on the list of department-approved "
    "psilocybin educational programs from other jurisdictions.",
    "(2) Documentation of either: (a) Completion of a government approved psilocybin educational program from "
    "another jurisdiction, which shall include: (i) Documentation that the curriculum of the educational "
    "program is equivalent to the didactic educational requirements applicable for New Mexico certification; "
    "and (ii) For all applications received on or after January 1, 2028, documentation of a third-party "
    "evaluation of the curriculum demonstrating such equivalency"
    + ins(", except that an applicant may satisfy this item by documenting that the educational program is "
          "included on the list maintained under Subsection A of this section")
    + "; (b) Completion of a psilocybin educational "
    "program from another jurisdiction that is developed in collaboration with higher education institutions "
    "or government-approved psychedelic research studies, which shall include: (i) Documentation that the "
    "curriculum of the educational program is equivalent to the didactic educational requirements applicable "
    "for New Mexico certification, and (ii) For all applications received on or after January 1, 2028, "
    "documentation of a third-party evaluation of the curriculum demonstrating such equivalency"
    + ins(", except that an applicant may satisfy this item by documenting that the educational program is "
          "included on the list maintained under Subsection A of this section")
    + "; or (c) "
    "Completion of an educational program that is currently included on the list of department-approved "
    "psilocybin educational programs from other jurisdictions.",
))

P.append((
    D2,
    "7.35.3.10",
    "Subsection C, re-application after denial",
    "C. Application approval and denial; certification period: If the application is approved, the "
    "certification shall be effective on the date of notice and shall be valid for two years. If the "
    "department denies an application, the department shall provide notice of the denial in accordance with "
    "this rule. If the application is denied, the applicant may re-apply within six months. An applicant who "
    "is denied a second time may not re-apply for six months from the denial. An applicant whose application "
    "is denied may appeal the denial in accordance with this rule.",
    "C. Application approval and denial; certification period: If the application is approved, the "
    "certification shall be effective on the date of notice and shall be valid for two years. If the "
    "department denies an application, the department shall provide notice of the denial in accordance with "
    "this rule. If the application is denied, the applicant may re-apply "
    + dele("within") + " " + ins("no earlier than") + " six months "
    + ins("after the date of the denial") + ". An applicant who "
    "is denied a second time may not re-apply for six months from the denial. An applicant whose application "
    "is denied may appeal the denial in accordance with this rule.",
))

P.append((
    D2,
    "7.35.3.10",
    "Paragraph (1) of Subsection D, waiver of practicum requirements",
    "D. Waiver of practicum requirements: (1) An applicant for certification as a practitioner or facilitator "
    "on the basis of an educational program from another jurisdiction, whose application is received by the "
    "department by December 31, 2027, shall not be required to complete the full practicum hours required by "
    "New Mexico, but shall demonstrate completion of at least 40 hours of contact time with a minimum of two "
    "separate individual sessions and two separate group sessions for preparation, administration, and "
    "integrative therapy with psilocybin treatment.",
    UNCHANGED,
))

P.append((
    D2,
    "7.35.3.12",
    "Subsection D, re-application after denial",
    "D. Approval and denial; certification period: If the application is approved, the certification shall be "
    "effective on the date of notice and shall be valid for two years. If the department denies an "
    "application, the department shall provide notice of the denial in accordance with this rule. If the "
    "application is denied, the applicant may re-apply within six months. An applicant who is denied a second "
    "time may not re-apply for six months from the denial. An applicant whose application is denied may "
    "appeal the denial in accordance with this rule.",
    "D. Approval and denial; certification period: If the application is approved, the certification shall be "
    "effective on the date of notice and shall be valid for two years. If the department denies an "
    "application, the department shall provide notice of the denial in accordance with this rule. If the "
    "application is denied, the applicant may re-apply "
    + dele("within") + " " + ins("no earlier than") + " six months "
    + ins("after the date of the denial") + ". An applicant who is denied a second "
    "time may not re-apply for six months from the denial. An applicant whose application is denied may "
    "appeal the denial in accordance with this rule.",
))

P.append((
    D2,
    "7.35.3.15",
    "Subsection A, required reporting of updates",
    "A. Required reporting of updates: A department-certified psilocybin educational program shall notify the "
    "department, through the department-approved electronic system designated by the department, of any of "
    "the following changes, and shall not implement the change until written approval is issued by the "
    "department: (1) Any revision to the program's curriculum; revised curricula shall be submitted to the "
    "department for review and may not be implemented until the department grants approval; (2) Any change in "
    "ownership, including changes in controlling interest or organizational structure; (3) Any change in "
    "physical locations utilized for instruction or educational activities; (4) Any modification, "
    "termination, or addition of practicum site agreements; and (5) Any change in instructional staff, "
    "including submission of curricula vitae or résumés for all newly added instructors.",
    "A. Required reporting of updates: A department-certified psilocybin educational program shall notify the "
    "department, through the department-approved electronic system designated by the department, of any of "
    "the following changes, and shall not implement the change until written approval is issued by the "
    "department"
    + ins(". The department shall notify the program of its approval or denial of a change reported under "
          "this subsection within 60 calendar days of receiving the report") + " " + rng("60 from 7.35.3.15 B")
    + ": (1) Any revision to the program's curriculum; revised curricula shall be submitted to the "
    "department for review and may not be implemented until the department grants approval; (2) Any change in "
    "ownership, including changes in controlling interest or organizational structure; (3) Any change in "
    "physical locations utilized for instruction or educational activities; (4) Any modification, "
    "termination, or addition of practicum site agreements; and (5) Any change in instructional staff, "
    "including submission of curricula vitae or résumés for all newly added instructors.",
))

P.append((
    D2,
    "7.35.3.16",
    "Section heading and Subsection A, general requirements",
    "7.35.3.16 REQUIREMENTS FOR THIRD-PARTY EVALUATORS OF EDUCATIONAL PROGRAMS: A. General requirements: A "
    "psilocybin educational program shall engage a qualified third-party evaluation team to conduct the "
    "evaluations required under this rule. The evaluation team shall consist of no fewer than three "
    "individuals who collectively meet all competency requirements set forth in this section.",
    "7.35.3.16 REQUIREMENTS FOR THIRD-PARTY EVALUATORS OF EDUCATIONAL PROGRAMS: A. General requirements: A "
    "psilocybin educational program shall engage a qualified third-party evaluation team to conduct the "
    "evaluations required under this rule. The evaluation team shall consist of no fewer than three "
    "individuals who collectively meet all competency requirements set forth in this section."
    + ins(" A program may compensate the evaluation team for conducting an evaluation required under this "
          "rule, and that compensation is not a conflict of interest under Subsection C of this section."),
))

P.append((
    D2,
    "7.35.3.16",
    "Paragraph (2) of Subsection B, minimum qualifications",
    "B. Minimum qualifications: Each evaluator shall possess at least three years of professional experience "
    "in one or more of the following fields, and the evaluation team as a whole shall demonstrate expertise "
    "covering all listed domains: (1) Psilocybin therapy practice, supported by a master's or doctoral degree "
    "in counseling, therapy, social work, public health, behavioral health, or a closely related field; (2) "
    "Medical and research practice, supported by a master's or doctoral degree in medicine, pharmacy, "
    "nursing, or another related clinical or scientific field; and (3) Educational curriculum development and "
    "evaluation, supported by a master's or doctoral degree in education, educational psychology, or a "
    "closely related field.",
    "B. Minimum qualifications: Each evaluator shall possess at least three years of professional experience "
    "in one or more of the following fields, and the evaluation team as a whole shall demonstrate expertise "
    "covering all listed domains: (1) Psilocybin therapy practice, supported by a master's or doctoral degree "
    "in counseling, therapy, social work, public health, behavioral health, or a closely related field; (2) "
    "Medical " + dele("and") + " " + ins("or") + " research practice, supported by a master's or doctoral "
    "degree in medicine, pharmacy, "
    "nursing, or another related clinical or scientific field; and (3) Educational curriculum development and "
    "evaluation, supported by a master's or doctoral degree in education, educational psychology, or a "
    "closely related field.",
))

P.append((
    D2,
    "7.35.3.16",
    "Subsection C, conflict of interest prohibitions",
    "C. Conflict of -interest prohibitions: (1) All evaluators shall be free from actual or perceived "
    "conflicts of interest regarding the organization or curriculum under review. (2) The following "
    "conflicts, at minimum, shall disqualify an individual from serving as an evaluator: (a) Participation in "
    "the design, development, or teaching of the curriculum being evaluated; or (b) Holding a financial "
    "interest in, receiving compensation from, or serving in any governance or advisory capacity with the "
    "program or organization being evaluated.",
    "C. Conflict " + dele("of -interest") + " " + ins("of-interest") + " prohibitions: (1) All evaluators "
    "shall be free from actual or perceived "
    "conflicts of interest regarding the organization or curriculum under review. (2) The following "
    "conflicts, at minimum, shall disqualify an individual from serving as an evaluator: (a) Participation in "
    "the design, development, or teaching of the curriculum being evaluated; or (b) Holding a financial "
    "interest in, receiving compensation from, or serving in any governance or advisory capacity with the "
    "program or organization being evaluated"
    + ins(", other than compensation for conducting an evaluation required under this rule as provided in "
          "Subsection A of this section") + ".",
))

P.append((
    D2,
    "7.35.3.17",
    "Subsection A, mentoring sessions",
    "A. All educational programs shall provide each practitioner and facilitator student with a minimum of 10 "
    "hours of mentoring sessions after graduation and after practicum hours are completed. The purpose of the "
    "mentoring sessions is to allow new graduates to consult with the educational program faculty regarding "
    "cases, patients, situations, and how they handle them. These mentoring sessions may not have additional "
    "associated charges beyond the cost of the educational program itself. The 10 hours are valid for up to 12 "
    "months after practicum hours are completed. If students request more than 10 hours of mentoring "
    "sessions, this will be at the purview of the educational program and may have an additional associated "
    "cost.",
    UNCHANGED,
))

P.append((
    D2,
    "7.35.3.17",
    "Subsection B, module evaluation without attendance",
    "B. Educational programs shall offer an option for a student to complete the evaluation for each "
    "educational module (not including the New Mexico module) without attending the lessons or classes for "
    "the module. The cost to complete the evaluation for each module shall not be greater than one-fourth of "
    "the normal price of each of the educational modules. If the student receives a passing grade for a "
    "module evaluation, they will have been considered to have completed the module; and if a student does "
    "not receive a passing grade for a module evaluation, they will not have completed the module. The "
    "educational program may at its discretion allow students to re-take the evaluation without attending the "
    "lessons or classes for the modules. Students who utilize this option shall complete all other "
    "requirements for the educational program, including the New Mexico Module, certifications, simulated "
    "patient, and practicum requirements to graduate from the educational program.",
    UNCHANGED,
))


# ===========================================================================
# D3. Locations and oversight: 7.35.3.11, .20, .21
# ===========================================================================

P.append((
    D3,
    "7.35.3.11",
    "Section heading and lead-in of Subsection A",
    "7.35.3.11 APPLICATION PROCESS FOR HEALING CENTERS AND OTHER APPROVED LOCATIONS: (A) Applications for "
    "healing centers: An applicant seeking certification as a healing center shall submit a complete "
    "application through the electronic system designated by the department. A complete application shall "
    "include, at minimum, the following:",
    "7.35.3.11 APPLICATION PROCESS FOR HEALING CENTERS AND OTHER APPROVED LOCATIONS: "
    + dele("(A)") + " " + ins("A.") + " Applications for "
    "healing centers: An applicant seeking certification as a healing center shall submit a complete "
    "application through the electronic system designated by the department. A complete application shall "
    "include, at minimum, the following:",
))

P.append((
    D3,
    "7.35.3.11",
    "Paragraph (11) of Subsection A, owners and employees",
    "(11) A list of all owners or members of the board of directors, including corresponding contact "
    "information;",
    "(11) A list of all owners or members of the board of directors, including corresponding contact "
    "information"
    + ins("; and a list of all owners and employees whom the healing center designates to purchase, possess, "
          "sell, or otherwise administer medical psilocybin products under Subsection C of 7.35.3.14 NMAC, "
          "including corresponding contact information. An owner or employee named on the list submitted "
          "under this paragraph is registered with the department for purposes of Subsection C of 7.35.3.14 "
          "NMAC")
    + ";",
))

P.append((
    D3,
    "7.35.3.11",
    "Paragraph (9) of Subsection B, proof of ownership",
    "(9) Proof of ownership by the qualified patient or attending practitioner or facilitator of any property "
    "on which medical psilocybin administration sessions will be conducted, or a signed, written statement "
    "from the owner of such property acknowledging that the owner understands that persons will be "
    "participating in the medical psilocybin program on the premises, and what those persons are authorized "
    "to do within the terms of their certification;",
    "(9) Proof of ownership by the qualified patient or attending practitioner or facilitator of any property "
    "on which medical psilocybin administration sessions will be conducted, or a signed, written statement "
    "from the owner of such property acknowledging that the owner understands that persons will be "
    "participating in the medical psilocybin program on the premises, and what those persons are authorized "
    "to do within the terms of their certification"
    + ins(". This paragraph does not apply where the location is the residence of the qualified patient")
    + ";",
))

P.append((
    D3,
    "7.35.3.11",
    "Paragraph (10) of Subsection B, outdoor or natural environments",
    "(10) For outdoor or natural environments: (a) A detailed description of the administration area, "
    "including identification of safe entrances and exits, and verification that the area is free from "
    "hazards; (b) An emergency safety and response plan; (c) Proof that emergency medical services can "
    "reliably be contacted from, and respond to, the location at which medical psilocybin administration "
    "sessions will occur; and (d) If the natural environment setting is 15 minutes or more away from "
    "emergency medical service response or a hospital, urgent care, or other emergency medical services, then "
    "there must be at least two individuals present who are not receiving treatment and who have: (i) "
    "Wilderness first aid certification; (ii) Wilderness first responder certification; or (iii) Licensure as "
    "a New Mexico emergency medical technician (e.g., EMT-basic, EMT-intermediate, EMT-paramedic);",
    "(10) For outdoor or natural environments: (a) A detailed description of the administration area, "
    "including identification of safe entrances and exits, and verification that the area is free from "
    "hazards; (b) An emergency safety and response plan; (c) Proof that emergency medical services can "
    "reliably be contacted from, and respond to, the location at which medical psilocybin administration "
    "sessions will occur; and (d) If the natural environment setting is 15 minutes or more away from "
    "emergency medical service response or a hospital, urgent care, or other emergency medical services, then "
    "there must be at least two individuals present who are not receiving treatment and who have: (i) "
    "Wilderness first aid certification; (ii) Wilderness first responder certification; or (iii) Licensure as "
    "a New Mexico emergency medical technician (e.g., EMT-basic, EMT-intermediate, EMT-paramedic)"
    + ins("; and (e) If the natural environment setting is 15 minutes or more away from emergency medical "
          "service response or a hospital, urgent care, or other emergency medical services, then there must "
          "be a basic first aid kit and an AED on site") + ";",
))

P.append((
    D3,
    "7.35.3.11",
    "Subsection D, certification period; approval and denial",
    "D. Certification period; approval and denial: Certification of a healing center shall be effective on "
    "the date of department issuance and shall be valid for two years. Certification of other approved "
    "locations shall be effective on the date of department issuance and shall be valid for 90 days. If the "
    "department denies an application for a healing center or other approved location, the department shall "
    "provide notice of the denial within 30 calendar days in accordance with this rule. If the application is "
    "denied, the applicant may re-apply within six months. An applicant who is denied a second time may not "
    "re-apply for six months from the denial. An applicant whose application is denied may appeal the denial "
    "in accordance with this rule.",
    "D. Certification period; approval and denial: Certification of a healing center shall be effective on "
    "the date of department issuance and shall be valid for two years. Certification of other approved "
    "locations shall be effective on the date of department issuance and shall be valid for 90 days"
    + ins(", and may be renewed for additional 90-day terms on application to the department") + " "
    + rng("90 from 7.35.3.11 D") + ". If the "
    "department denies an application for a healing center or other approved location, the department shall "
    "provide notice of the denial within 30 calendar days in accordance with this rule. If the application is "
    "denied, the applicant may re-apply "
    + dele("within") + " " + ins("no earlier than") + " six months "
    + ins("after the date of the denial") + ". An applicant who is denied a second time may not "
    "re-apply for six months from the denial. An applicant whose application is denied may appeal the denial "
    "in accordance with this rule.",
))

P.append((
    D3,
    "7.35.3.20",
    "Section heading, lead-in, and Subsection A",
    "7.34.3.20 REQUIREMENTS FOR HEALING CENTERS AND OTHER APPROVED LOCATIONS: A healing center and a "
    "registrant of another approved location shall comply with the following requirements: A. A healing "
    "center and a registrant of another approved location shall maintain a list of all qualified patients who "
    "are intended to utilize, and who have utilized, the location for administration sessions.",
    UNCHANGED,
))

P.append((
    D3,
    "7.35.3.21",
    "Subsection A, authority to conduct assessments",
    "A. Authority to conduct assessments: The department or its designee may conduct remote or on-site "
    "assessments of a psilocybin education program, healing center or other approved location, with or "
    "without prior notice, during normal business hours, for the purpose of determining compliance with the "
    "Medical Psilocybin Act and this rule. In conducting assessments, the department may review "
    "documentation, inspect premises and equipment, and interview staff and patients. Exception: except in "
    "emergency circumstances, the department or its designee shall not conduct an on-site assessment during a "
    "patient session or at a patient's home without prior written consent from the patient(s).",
    UNCHANGED,
))


# ===========================================================================
# D4. Patients, applicants and process: 7.35.3.8, .9, .13, .22 through .28
# ===========================================================================

P.append((
    D4,
    "7.35.3.8",
    "Subsection D, review of a denied patient application",
    "D. A person whose application for patient enrollment is denied for failure to complete an application or "
    "failure to meet a submittal requirement of this rule may request a record review to be conducted by the "
    "department, in accordance with this rule.",
    "D. A person whose application for patient enrollment is denied for failure to complete an application or "
    "failure to meet a submittal requirement of this rule may request "
    + dele("a record review to be conducted by the department") + " "
    + ins("an informal administrative review under 7.35.3.25 NMAC") + ", in accordance with this rule.",
))

P.append((
    D4,
    "7.35.3.9",
    "Paragraphs (5) and (6) of Subsection A, re-application after denial",
    "(5) If the application is denied, the applicant may re-apply within six months. (6) An applicant who is "
    "denied a second time may not re-apply for six months from the denial.",
    "(5) If the application is denied, the applicant may re-apply "
    + dele("within") + " " + ins("no earlier than") + " six months "
    + ins("after the date of the denial") + ". (6) An applicant who is "
    "denied a second time may not re-apply for six months from the denial.",
))

P.append((
    D4,
    "7.35.3.9",
    "Subsection D, certifying clinician application requirements",
    "D. Certifying clinician application requirements: An applicant for certification as a certifying "
    "clinician shall additionally submit the following, using the electronic system designated by the "
    "department: (1) Documentation of current professional license to practice in New Mexico (e.g. MD, NP); "
    "(2) NM controlled substance number; (4) Documentation of HIPAA certification completed within the "
    "preceding two years; (5) Completed W-9 form; and (6) Such additional information as the department may "
    "reasonably require.",
    "D. Certifying clinician application requirements: An applicant for certification as a certifying "
    "clinician shall additionally submit the following, using the electronic system designated by the "
    "department: (1) Documentation of current professional license to practice in New Mexico (e.g. MD, NP); "
    "(2) NM controlled substance number; " + dele("(4)") + " " + ins("(3)")
    + " Documentation of HIPAA certification completed within the "
    "preceding two years; " + dele("(5)") + " " + ins("(4)") + " Completed W-9 form; and "
    + dele("(6)") + " " + ins("(5)") + " Such additional information as the department may "
    "reasonably require.",
))

P.append((
    D4,
    "7.35.3.13",
    "Section heading",
    "7.34.3.13 REQUIREMENTS AND PROHIBITIONS FOR CERTIFYING CLINICIANS, PRACTITIONERS, AND FACILITATORS:",
    dele("7.34.3.13") + " " + ins("7.35.3.13")
    + " REQUIREMENTS AND PROHIBITIONS FOR CERTIFYING CLINICIANS, PRACTITIONERS, AND FACILITATORS:",
))

P.append((
    D4,
    "7.35.3.13",
    "Subsection B, facilitators; scope of work",
    "B. Facilitators; scope of work: A facilitator is authorized to work alongside a practitioner during "
    "medical psilocybin services. A facilitator works under the direct supervision of a practitioner, and "
    "provides peer support to qualified patients, as well as logistical and administrative support to the "
    "practitioner and to the healing center. A facilitator shall not perform any patient care outside this "
    "scope, unless another license held by the facilitator permits it.",
    UNCHANGED,
))

P.append((
    D4,
    "7.35.3.23",
    "Entire section, dual ownership",
    "7.34.3.23 PROHIBITION AGAINST DUAL OWNERSHIP IN CERTIFICANT AND PERMITTEE: A certificant or a person who "
    "holds an ownership interest in a certificant shall not hold an ownership interest in a permittee.",
    dele("7.34.3.23") + " " + ins("7.35.3.23")
    + " PROHIBITION AGAINST DUAL OWNERSHIP IN CERTIFICANT AND PERMITTEE: A certificant or a person who "
    "holds an ownership interest in a certificant shall not hold an ownership interest in a permittee.",
))

P.append((
    D4,
    "7.35.3.24",
    "Entire section, complaints to the department",
    "7.35.3.24 COMPLAINTS TO THE DEPARTMENT: A qualified patient or certificant may submit a complaint to the "
    "department regarding a certificant in the medical psilocybin program, or regarding any activity or "
    "concern related to the medical psilocybin program. The complaint should be in writing, addressed to the "
    "medical psilocybin program, and submitted by U.S. certified mail or through the electronic system "
    "designated by the department electronic system. The department may request additional information for "
    "purposes of its own inquiry. A complaint shall include the name and contact information for the "
    "complainant; and a statement of the nature of the complaint and any individuals who may be involved. The "
    "department may, within its discretion, choose to conduct a subsequent inquiry, and may request "
    "additional information from the complainant for this purpose.",
    "7.35.3.24 COMPLAINTS TO THE DEPARTMENT: A qualified patient or certificant may submit a complaint to the "
    "department regarding a certificant in the medical psilocybin program, or regarding any activity or "
    "concern related to the medical psilocybin program. The complaint should be in writing, addressed to the "
    "medical psilocybin program, and submitted by U.S. "
    + dele("certified") + " mail or through the electronic system "
    "designated by the department " + dele("electronic system") + ". The department may request additional "
    "information for "
    "purposes of its own inquiry. A complaint shall include the name and contact information for the "
    "complainant"
    + ins(", which shall remain confidential") + "; and a statement of the nature of the complaint and any "
    "individuals who may be involved. The "
    "department may, within its discretion, choose to conduct a subsequent inquiry, and may request "
    "additional information from the complainant for this purpose.",
))

P.append((
    D4,
    "7.35.3.25",
    "Section heading and Subsection A",
    "7.34.3.25 INFORMAL ADMINISTRATIVE REVIEW OF DENIED PATIENT APPLICATIONS: A. Administrative review: An "
    "applicant for patient enrollment whose application has been denied may request an informal "
    "administrative review from the department.",
    dele("7.34.3.25") + " " + ins("7.35.3.25")
    + " INFORMAL ADMINISTRATIVE REVIEW OF DENIED PATIENT APPLICATIONS: A. Administrative review: An "
    "applicant for patient enrollment whose application has been denied may request an informal "
    "administrative review from the department.",
))

P.append((
    D4,
    "7.35.3.25",
    "Paragraph (1) of Subsection D, content and timeline",
    "(1) Content and timeline: The administrative review shall be completed, and a decision setting forth the "
    "reasons for the decision and the evidence upon which the decision is based, no later than 15 calendar "
    "days from the date that the program receives the written request for a record review.",
    "(1) Content and timeline: The administrative review shall be completed, and a decision "
    + ins("shall be issued") + " setting forth the "
    "reasons for the decision and the evidence upon which the decision is based, no later than 15 calendar "
    "days from the date that the program receives the written request for "
    + dele("a record review") + " " + ins("an informal administrative review") + ".",
))

P.append((
    D4,
    "7.35.3.27",
    "Paragraph (1) of Subsection C, persons who may request a hearing",
    "C. Persons who may request a hearing: The following persons may request a hearing to contest an action "
    "or proposed action of the department, in accordance with this rule: (1) a certified patient; (2) a "
    "certified practitioner; (3) a certifying clinician who was certified by the department; (4) a certified "
    "facilitator; (5) a certified healing center or other approved location; (6) a certified educational "
    "program; and (7) an applicant for enrollment or certification as any of the foregoing, whose application "
    "is denied for any reason other than failure to submit a completed application or failure to meet a "
    "submittal requirement of this rule.",
    "C. Persons who may request a hearing: The following persons may request a hearing to contest an action "
    "or proposed action of the department, in accordance with this rule: (1) a "
    + dele("certified") + " " + ins("qualified") + " patient; (2) a "
    "certified practitioner; (3) a certifying clinician who was certified by the department; (4) a certified "
    "facilitator; (5) a certified healing center or other approved location; (6) a certified educational "
    "program; and (7) an applicant for enrollment or certification as any of the foregoing, whose application "
    "is denied for any reason other than failure to submit a completed application or failure to meet a "
    "submittal requirement of this rule.",
))

P.append((
    D4,
    "7.35.3.27",
    "Paragraph (8) of Subsection B, grounds for disciplinary action",
    "(8) for certifying clinicians and practitioners: any determination by the individual's licensing body "
    "that the clinician has engaged in unprofessional or dishonorable conduct;",
    "(8) for certifying clinicians and practitioners: any determination by the individual's licensing body "
    "that the " + dele("clinician") + " " + ins("certifying clinician or practitioner")
    + " has engaged in unprofessional or dishonorable conduct;",
))

P.append((
    D4,
    "7.35.3.27",
    "Subsection M, continuances",
    "M. Continuances: The hearing examiner may grant a continuance for good cause shown. A motion to continue "
    "a hearing shall be made at least 10 calendar days before the hearing date.",
    "M. Continuances: The hearing " + dele("examiner") + " " + ins("officer")
    + " may grant a continuance for good cause shown. A motion to continue "
    "a hearing shall be made at least 10 calendar days before the hearing date.",
))

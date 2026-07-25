#!/usr/bin/env python3
"""Build the side-by-side redline PDF for the subsections being amended.

Left column: the text as published July 23, 2026, verbatim.
Right column: the text as proposed, with insertions and deletions marked.

Only the subsections actually being amended appear. Subsections of the same
sections that are not being amended are named and marked "not amended" so the
reader can see the whole of what is and is not touched.

Every left-column block is verified character by character against the text
layer of docs/documents/rules-draft-2026-07-23-published.pdf before the PDF is
written. If any block fails, the build aborts.

Usage:  python3 amendments/build-redline-pdf.py
Output: amendments/7.35.3-training-redline-2026-07-23.pdf
"""

import html
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PUBLISHED_PDF = REPO / "docs/documents/rules-draft-2026-07-23-published.pdf"
# Version this document on every rebuild that changes its content, so that no two
# copies in circulation carry the same name. History is in VERSION_HISTORY below.
VERSION = "v4"
VERSION_DATE = "July 25, 2026"
OUT_PDF = REPO / ("amendments/7.35.3-practicum-amendments-%s.pdf" % VERSION)

VERSION_HISTORY = [
    ("v1", "July 25, 2026", "First side-by-side draft. 84 read as a didactic total. Consultation at 30. "
                            "Practicum step 1 with well participants not drafted."),
    ("v2", "July 25, 2026", "84 restated as a module total inclusive of the 5 simulated patient hours. "
                            "Practicum entry gate changed from a fraction to a flat 40 didactic hours. "
                            "Step 1 drafted as proposed new section 7.35.3.29."),
    ("v3", "July 25, 2026", "Consultation set to 20. Medical Psilocybin Act read and applied. 7.35.2 NMAC "
                            "read and applied. Post-traumatic stress disorder added as a required content "
                            "area. Addenda A, B and C added. First versioned issue."),
    ("v4", "July 25, 2026", "Proposed 7.35.3.19 F, practicum supervisors, withdrawn as invented and not "
                            "traceable to the July 17 recommendation. The withdrawal is recorded in Addendum B "
                            "rather than dropped silently, and the remaining subsections are re-lettered. A "
                            "provenance line added to every proposed change. The two readings of 7.35.3.19 C "
                            "raised to the front of the document as a call-out. Addenda D, E and F added."),
]

# The permit title, carried as a variable exactly as in the markdown drafts.
PERMIT_TITLE = {
    "{{PT}}": "practitioner",
    "{{PTS}}": "practitioners",
    "{{PT_C}}": "Practitioner",
    "{{PTS_C}}": "Practitioners",
    "{{PT_UC}}": "PRACTITIONER",
    "{{PTS_UC}}": "PRACTITIONERS",
}

NEW = "There is no current language. This provision does not exist in the proposed rule as published."

# Baseline distance, in points, within which two text lines are the same visual line.
LINE_TOLERANCE = 3.0
UNCHANGED = "__UNCHANGED__"


def ins(t):
    return '<ins>%s</ins>' % t


def dele(t):
    return '<del>%s</del>' % t


# ---------------------------------------------------------------------------
# Content. Each entry is (anchor, heading, published_text, proposed_html).
# published_text is plain text, verified against the PDF. Use UNCHANGED for a
# subsection that is carried forward untouched.
# ---------------------------------------------------------------------------

P = []  # (section, subsection, published, proposed)

# ---- 7.35.3.14 -------------------------------------------------------------

P.append((
    "7.35.3.14",
    "Section heading and lead-in",
    "7.34.3.14 AUTHORIZED POSSESSION, PURCHASE, OR SALE OF MEDICAL PSILOCYBIN BY "
    "PRACTITIONERS, FACILITATORS, HEALING CENTER OWNERS AND EMPLOYEES: Certification of "
    "a practitioner, facilitator, or healing center shall enable practitioners, facilitators, and owners and employees of "
    "healing centers to do the following, in accordance with medical psilocybin program rules:",
    dele("7.34.3.14") + " " + ins("7.35.3.14") + " AUTHORIZED POSSESSION, PURCHASE, OR SALE OF MEDICAL PSILOCYBIN BY "
    "{{PTS_UC}}, FACILITATORS, " + ins("TRAINING PERMITTEES,") + " HEALING CENTER OWNERS AND EMPLOYEES: Certification of "
    "a {{PT}}, facilitator, or healing center" + ins(", and issuance of a training permit under Subsection G of 7.35.3.19 NMAC,") +
    " shall enable {{PTS}}, facilitators, " + ins("training permittees,") + " and owners and employees of "
    "healing centers to do the following, in accordance with medical psilocybin program rules:",
))

P.append((
    "7.35.3.14",
    "Subsection A, {{PTS_C}}",
    "(A) Practitioners: Practitioners may purchase and possess medical psilocybin products obtained from "
    "permitted producers, and may sell or otherwise provide medical psilocybin products to qualified patients during "
    "administration sessions conducted at a healing center location or other approved location. A practitioner may only "
    "sell or otherwise provide psilocybin products that are obtained from permitted producers.",
    dele("(A)") + " " + ins("A.") + " {{PTS_C}}: {{PTS_C}} may purchase and possess medical psilocybin products obtained from "
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
    dele("(B)") + " " + ins("B.") + " Facilitators: Facilitators may possess medical psilocybin products, for the purpose of providing "
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
    dele("(C)") + " " + ins("C.") + " Healing centers: Owners and employees of healing centers who are "
    + dele("registered with the department")
    + ins("designated to the department by the healing center in accordance with Subsection M of 7.35.3.20 NMAC")
    + " may purchase medical psilocybin products from permitted producers, may possess medical psilocybin "
    "products, and may sell or otherwise administer those products to qualified patients in administration sessions "
    "conducted at the healing center or other approved locations, provided that such individuals are also designated to "
    "engage in each activity by the healing center. A healing center may only sell or otherwise provide psilocybin "
    "products that are obtained from permitted producers.",
))

P.append((
    "7.35.3.14",
    "Subsection D, Training permittees",
    NEW,
    ins("D. Training permittees: A student who holds a current training permit issued under Subsection G of "
        "7.35.3.19 NMAC may possess medical psilocybin products, and may administer or otherwise provide those products "
        "to qualified patients, or to practicum participants in accordance with 7.35.3.29 NMAC, in administration "
        "sessions conducted at a healing center or other approved location, in each case only while under the direct, "
        "on-site supervision of a practicum supervisor, and only to the "
        "extent required by the practicum under 7.35.3.19 NMAC. A training permittee shall not purchase medical "
        "psilocybin products."),
))

# ---- 7.35.3.18 -------------------------------------------------------------

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
    + ins(", consisting of a minimum of eight didactic hours,") + " prior to applying for "
    "certification, which shall include at a minimum: <span class='note'>Paragraphs (1) through (5) not amended.</span>",
))

P.append((
    "7.35.3.18",
    "Subsection B, certifying clinician module",
    UNCHANGED,
    UNCHANGED,
))

P.append((
    "7.35.3.18",
    "Subsection C, {{PT}} and facilitator psilocybin therapy module, lead-in",
    "C. Requirements for initial practitioner and facilitator certification: All practitioners and "
    "facilitators shall complete a psilocybin therapy module consisting of a minimum of 30 didactic hours and 5 hours of "
    "simulated patient experience, prior to applying for certification, which shall include:",
    "C. Requirements for initial {{PT}} and facilitator certification: All {{PTS}} and "
    "facilitators shall complete a psilocybin therapy module consisting of a minimum of " + dele("30") + " " + ins("65")
    + " didactic hours and 5 hours of simulated patient experience, prior to applying for certification, which shall include:",
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
    "(3) Trauma-Informed Care" + ins(", a minimum of eight didactic hours;") + "<br>"
    "(4) Psychedelic emergencies/urgencies/medical monitoring;<br>"
    "(5) Psilocybin actions, interactions and pharmacology;<br>"
    "(6) Set and setting;<br>"
    "(7) Ethics in therapeutic settings" + ins(", a minimum of 14 didactic hours") + ";<br>"
    "(8) Patient-centered approaches and care;<br>"
    "(9) Preparation and integration sessions;<br>"
    "(10) Administration session;<br>"
    "(11) Dosing;<br>"
    "(12) Psychedelic de-escalation techniques"
    + ins(", and recognition of and support for challenging experiences during and after administration sessions, "
          "including hallucinogen persisting perception disorder") + ";<br>"
    "(13) Non-ordinary states of consciousness;<br>"
    "(14) Self-care;<br>"
    "(15) Research and data collection requirements;<br>"
    + ins("(16) End-of-life and palliative care, a minimum of 10 didactic hours;") + "<br>"
    + ins("(17) Screening, suicidality, and crisis response, a minimum of five didactic hours;") + "<br>"
    + ins("(18) Substance use disorder, including nicotine use disorder, a minimum of four didactic hours;") + "<br>"
    + ins("(19) Post-traumatic stress disorder: recognition, screening, contraindications, and collaboration "
          "with or referral to a provider trained in the treatment of post-traumatic stress disorder, a minimum of four "
          "didactic hours. This paragraph does not require training in the treatment of post-traumatic stress "
          "disorder;") + "<br>"
    + ins("(20) Somatic awareness and therapeutic touch, including consent, a minimum of four didactic hours;") + "<br>"
    + ins("(21) History and traditional use of psilocybin and other psychedelics, a minimum of three didactic hours;") + "<br>"
    + ins("(22) Individual and group treatment models and group dynamics;") + "<br>"
    + dele("(16)") + " " + ins("(23)") + " A simulated patient experience of no less than 5 hours; and<br>"
    + dele("(17)") + " " + ins("(24)") + " Evaluation to demonstrate competency in the above areas.",
))

P.append((
    "7.35.3.18",
    "Subsection D, additional facilitator module, lead-in",
    "D. Additional requirements for initial facilitator certification: All facilitators shall complete a "
    "facilitator-specific training module consisting of a minimum of five didactic hours, prior to applying for "
    "certification, which shall include:",
    "D. Additional requirements for initial facilitator certification: All facilitators shall complete a "
    "facilitator-specific training module consisting of a minimum of " + dele("five") + " " + ins("six")
    + " didactic hours, prior to applying for certification, which shall include: "
    "<span class='note'>Paragraphs (1) through (5) not amended.</span>",
))

P.append((
    "7.35.3.18",
    "Subsection E, additional {{PT}} module, lead-in",
    "E. Additional requirements for initial practitioner certification: All practitioners shall complete a "
    "module on psychedelic and psilocybin therapeutic approaches consisting of a minimum of five didactic hours, prior "
    "to applying for certification, which shall include:",
    "E. Additional requirements for initial {{PT}} certification: All {{PTS}} shall complete a "
    "module on psychedelic and psilocybin therapeutic approaches consisting of a minimum of " + dele("five") + " " + ins("six")
    + " didactic hours, prior to applying for certification, which shall include: "
    "<span class='note'>Paragraphs (1) through (3) not amended.</span>",
))

P.append((
    "7.35.3.18",
    "Subsection F, {{PT}} and facilitator trainings, lead-in",
    "F. Practitioner and facilitator trainings: All practitioners and facilitators shall also complete and "
    "maintain proof of current certification prior to applying for medical psilocybin certification in:",
    "F. {{PT_C}} and facilitator trainings: All {{PTS}} and facilitators shall "
    + dele("also complete and maintain proof of current certification prior to applying for medical psilocybin certification in:")
    + ins("complete and maintain the following prior to applying for medical psilocybin certification:")
    + " <span class='note'>Paragraphs (1) and (2) not amended. This corrects a sentence that does not complete as "
      "published; no obligation changes.</span>",
))

P.append((
    "7.35.3.18",
    "Subsection G, continuing education",
    UNCHANGED,
    UNCHANGED,
))

P.append((
    "7.35.3.18",
    "Subsection H, total module hours",
    NEW,
    ins("H. Total module hours: The requirements of Subsections A, C and D of this section shall together total a "
        "minimum of 84 hours for a facilitator applicant. The requirements of Subsections A, C and E of this section "
        "shall together total a minimum of 84 hours for a {{PT}} applicant. Of that total, no fewer than 79 hours shall "
        "be didactic hours, and 5 hours shall be the simulated patient experience required by Subsection C of this "
        "section, which is in addition to the didactic hours required by that subsection. The hour minimums stated for "
        "individual content areas within Subsection C are floors within the 84-hour total and do not limit an "
        "educational program's allocation of the balance of the hours."),
))

P.append((
    "7.35.3.18",
    "Subsection I, New Mexico educational module; availability",
    NEW,
    ins("I. New Mexico educational module; availability: The department shall create or approve, and shall "
        "publish, the New Mexico educational module required by Subsection A of this section no later than 90 calendar "
        "days after the effective date of this rule. An applicant who is otherwise qualified for certification shall not "
        "be denied certification on the ground that the New Mexico educational module was unavailable, and shall "
        "complete the module within 90 calendar days after the department publishes it."),
))

# ---- 7.35.3.19 -------------------------------------------------------------

P.append((
    "7.35.3.19",
    "Subsection A, minimum practicum hours; administration day sessions",
    "A. Minimum practicum hours; administration day sessions: An individual who seeks to become "
    "certified as a practitioner or facilitator shall participate in supervised practice training, otherwise referred to as a "
    "“practicum”, after completing at least half of the didactic requirements and all of the simulated patient requirements "
    "of the educational requirements. The practicum shall consist of a minimum of 100 hours of supervised practice "
    "training for facilitators and 120 hours for practitioners and shall be completed prior to applying for certification. "
    "Students shall participate in a minimum of 80 hours of administration day sessions, where students are provided the "
    "opportunity to experience, observe, or conduct supervised facilitation of administration day sessions in-person with "
    "a minimum of 14 different patients over a minimum of eight different administration and same-day sessions with the "
    "following criteria:",
    "A. Minimum practicum hours; administration day sessions: An individual who seeks to become "
    "certified as a {{PT}} or facilitator shall participate in supervised practice training, otherwise referred to as a "
    "“practicum”, after completing at least " + dele("half of the didactic requirements")
    + ins("40 of the didactic hours required by 7.35.3.18 NMAC")
    + " and all of the simulated patient requirements "
    "of the educational requirements. The practicum shall consist of a minimum of " + dele("100") + " " + ins("80")
    + " hours of supervised practice training for facilitators and " + dele("120") + " " + ins("90")
    + " hours for {{PTS}} and shall be completed prior to applying for certification. "
    "Students shall participate in a minimum of " + dele("80") + " " + ins("60") + " hours of administration day sessions, "
    "where students are provided the opportunity to experience, observe, or conduct supervised facilitation of "
    "administration day sessions in-person with a minimum of 14 different patients over a minimum of eight different "
    "administration " + dele("and same-day") + " " + ins("day") + " sessions with the following criteria: "
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
    "B. Minimum practicum hours; in-person and integration sessions: Students shall participate in a "
    "minimum of 20 hours of in-person preparation and integration sessions, where students are provided the opportunity "
    "to experience, observe, or conduct (when licensure allows) preparation or integration sessions. This shall include a "
    "minimum of six different patients during individual sessions. This shall include at least one group preparatory and "
    "one group integration session with a minimum of four or more patients. "
    + ins("The patients counted under this subsection and the sessions counted under this subsection may be the same "
          "patients and the same group cohorts counted under Subsection A of this section."),
))

P.append((
    "7.35.3.19",
    "Subsection C, {{PT}} supervision hours",
    "C. Practitioner supervision hours: Practitioners shall complete an additional minimum of 20 hours "
    "as a practitioner supervising facilitators during in-person administration day sessions, which shall include a "
    "minimum of two different patients during individual administration day sessions, and a minimum of one group "
    "administration day sessions with a minimum of four or more patients in the group.",
    "C. {{PT_C}} supervision hours: {{PTS_C}} shall complete an additional minimum of " + dele("20") + " " + ins("10")
    + " hours as a {{PT}} supervising facilitators during in-person administration day sessions, "
    + ins("which hours are included within the 90 hours required by Subsection A of this section and are additional to "
          "the hours required of facilitators,")
    + " which shall include a minimum of two different patients during individual administration day sessions, and a "
      "minimum of one group administration " + dele("day sessions") + " " + ins("day session")
    + " with a minimum of four or more patients in the group.",
))

P.append((
    "7.35.3.19",
    "Subsection D, practicum sequence",
    NEW,
    ins("D. Practicum sequence: A student shall complete the 60 hours of administration day sessions required by "
        "Subsection A of this section in the following sequence. The hour figures stated in this subsection are minimums "
        "within the practicum totals required by Subsection A and do not limit the discretion of a practicum supervisor "
        "to assign a student duties of greater responsibility as the student demonstrates proficiency. Hours of "
        "preparation and integration sessions are counted under Subsection B of this section and not under this "
        "subsection.") + "<br>"
    + ins("(1) Stage one, initial supervised experience: a minimum of 20 hours. Stage one shall be completed with "
          "practicum participants who are not qualified patients, in accordance with 7.35.3.29 NMAC. If and for so long "
          "as 7.35.3.29 NMAC is not in effect, stage one shall consist of a minimum of 20 hours during which the student "
          "observes administration day sessions and provides support to the {{PT}} or facilitator conducting them, and "
          "the student shall not possess or administer medical psilocybin products during stage one. Preparation and "
          "integration sessions are required for each participant. Stage one shall be completed before a training permit "
          "is issued under Subsection G of this section.") + "<br>"
    + ins("(2) Stage two, co-facilitation: a minimum of 25 hours during which the student, holding a current training "
          "permit issued under Subsection G of this section, serves as the second person of a co-facilitation pair with a "
          "certified {{PT}} or facilitator. A practicum supervisor shall assign stage two cases on the basis of the "
          "acuity of the patient's presentation and the student's demonstrated proficiency.") + "<br>"
    + ins("(3) Stage three, group practicum: a minimum of 15 hours of direct participation in group administration day "
          "sessions.") + "<br>"
    + ins("(4) Stage four applies to {{PT}} applicants only and consists of the supervision hours required by Subsection "
          "C of this section."),
))

P.append((
    "7.35.3.19",
    "Subsection E, practicum location (published Subsection D)",
    "D. Practicum location: All practicum hours shall take place in an approved healing center or other "
    "approved location.",
    dele("D.") + " " + ins("E.") + " Practicum location: All practicum hours shall take place in an approved healing "
    "center or other approved location. "
    + ins("A healing center or other approved location may host a practicum student who is not enrolled in an "
          "educational program with which the healing center or other approved location is affiliated, provided that the "
          "student is supervised by a practicum supervisor. A healing center "
          "or other approved location that hosts a practicum student shall not be required to hold certification as a "
          "psilocybin educational program by reason of hosting the student."),
))

P.append((
    "7.35.3.19",
    "Subsection F, practicum standards (published Subsection E)",
    "E. Practicum standards: Practicum supervisors and students shall follow these rules as they apply "
    "to facilitation and therapy, shall comply with HIPAA and HITECH confidentiality requirements, and shall comport "
    "with applicable limits on scope of practice.",
    dele("E.") + " " + ins("F.") + " Practicum standards: Practicum supervisors and students shall follow these rules as "
    "they apply to facilitation and therapy, shall comply with HIPAA and HITECH confidentiality requirements, and shall "
    "comport with applicable limits on scope of practice. <span class='note'>Re-lettered only. Text not amended.</span>",
))

P.append((
    "7.35.3.19",
    "Subsection G, training permit",
    NEW,
    ins("G. Training permit:") + "<br>"
    + ins("(1) Issuance: The department shall issue a training permit to an applicant who: (a) is registered as a student "
          "with a psilocybin educational program certified under 7.35.3.12 NMAC; (b) has completed the didactic "
          "requirement for entry to the practicum stated in Subsection A of this section; (c) has completed stage one of "
          "the practicum sequence under Subsection D of this section; (d) submits documentation of current certification "
          "or licensure meeting Subsection F of 7.35.3.18 NMAC; (e) submits an attestation that the applicant is not "
          "registered in any jurisdiction as a sex offender; and (f) submits the applicant's legal name, address, "
          "telephone number, e-mail address, signature, and date of application submittal.") + "<br>"
    + ins("(2) Decision: Once the department has received a completed application, it will review the application and "
          "render a decision within 30 calendar days. If the department denies an application, the department shall "
          "provide notice of the denial within 30 calendar days in accordance with this rule. An applicant whose "
          "application is denied may appeal the denial in accordance with this rule.") + "<br>"
    + ins("(3) Authority conferred: A training permit authorizes the permittee to possess and administer medical "
          "psilocybin products to qualified patients, and to practicum participants in accordance with 7.35.3.29 NMAC, "
          "as provided in 7.35.3.14 NMAC, and to conduct supervised facilitation of administration day sessions and "
          "supervised preparation and integration sessions as required by this section, in each case only while under "
          "the direct, on-site supervision of a practicum supervisor. A training permittee shall not purchase medical "
          "psilocybin products, shall not provide medical psilocybin services other than as part of the practicum or the "
          "consultation requirement in Subsection H of this section, and shall not hold themselves out as a certified "
          "{{PT}} or facilitator.") + "<br>"
    + ins("(4) Term: A training permit is valid for 24 months from the date of issuance and may be renewed once for a "
          "further 12 months. A training permit expires on the earlier of the end of its term, the date the permittee "
          "ceases to be registered as a student with a certified psilocybin educational program, or the date the "
          "department issues the permittee a {{PT}} or facilitator certification.") + "<br>"
    + ins("(5) Status: A training permittee is a certificant for purposes of this rule."),
))

P.append((
    "7.35.3.19",
    "Subsection H, supervision and consultation; case presentation sign-off",
    NEW,
    ins("H. Supervision and consultation; case presentation sign-off:") + "<br>"
    + ins("(1) A training permittee shall complete a minimum of 20 hours of supervision or consultation during the "
          "training permit period, in addition to the practicum hours required by this section.") + "<br>"
    + ins("(2) Sign-off requires the permittee to present a minimum of two cases of qualified patients with whom the "
          "permittee has personally worked in the medical psilocybin program. Each case presentation shall take the form "
          "of a biopsychosocial case conceptualization addressing presenting concerns, risk factors, supportive factors, "
          "treatment considerations, and recommendations for aftercare.") + "<br>"
    + ins("(3) The supervisor or consultant shall complete an evaluation on a form approved by the department for each "
          "case presented, and shall submit it through the electronic system designated by the department.") + "<br>"
    + ins("(4) The 10 hours of mentoring sessions required by Subsection A of 7.35.3.17 NMAC are credited toward the 20 "
          "hours required by this subsection.") + "<br>"
    + ins("(5) The requirements of this subsection shall be completed prior to applying for certification."),
))

P.append((
    "7.35.3.19",
    "Subsection I, end-of-life practice",
    NEW,
    ins("I. End-of-life practice: Before providing medical psilocybin services to a patient enrolled on the basis of "
        "end-of-life care other than under the direct supervision of a {{PT}} or facilitator who meets the requirements "
        "of this subsection, a {{PT}} or facilitator shall have completed at least one co-facilitated end-of-life case "
        "during the practicum and presented at least one end-of-life case under Subsection H of this section."),
))

P.append((
    "7.35.3.19",
    "Subsection J, waiver of practicum requirements (published Subsection F)",
    "F. Waiver of practicum requirements: The department may otherwise waive, temporarily suspend, "
    "or reduce the practicum requirements for individuals applying for certification, in order to facilitate the certification "
    "of individuals trained by other government-approved programs, and to build the initial infrastructure of the program.",
    dele("F.") + " " + ins("J.") + " Waiver of practicum requirements: The department may otherwise waive, temporarily "
    "suspend, or reduce the practicum requirements for individuals applying for certification, in order to facilitate the "
    "certification of individuals trained by other government-approved programs, and to build the initial infrastructure "
    "of the program. "
    + ins("The department shall act on a request under this subsection within 30 calendar days and shall state the basis "
          "for its decision in writing. The department shall not under this subsection: (1) reduce an applicant's "
          "practicum below 40 hours of contact time with qualified patients; (2) waive the requirements of Subsection H "
          "of this section; or (3) authorize any person to possess or administer medical psilocybin products who is not "
          "certified or does not hold a current training permit. The department shall publish the number of waivers "
          "granted under this subsection and the general grounds for them, at least annually."),
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
    dele("G.") + " " + ins("K.") + " Waiver of practicum hours requirement for applications received by December 31, 2027: "
    "An applicant for certification shall not be required to satisfy the full New Mexico practicum hours requirement if "
    "the applicant:<br>"
    "(1) Applies for certification by December 31, 2027;<br>"
    "(2) Completes the didactic requirements by December 31, 2027;<br>"
    "(3) Graduates from an educational program that the department certifies by December 31, 2027 or that the "
    "department has included on the department-approved list of educational programs by December 31, 2027; and<br>"
    "(4) Demonstrates completion of at least 40 hours of contact time through logs or other records of the sessions, "
    "including:<br>"
    "(a) A minimum of two separate individual sessions including the appointments for preparation, administration and "
    "integration; and<br>"
    "(b) A minimum of " + dele("one group session") + " " + ins("two separate group sessions")
    + " including the appointments for preparation, administration, and integration.",
))

# ---- 7.35.3.20 -------------------------------------------------------------

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
    "student shall be deemed qualified if they "
    + dele("are registered with a certified educational program and they have completed at least 50 hours of their practicum.")
    + ins("hold a current training permit issued under Subsection G of 7.35.3.19 NMAC and have completed at least 50 "
          "hours of their practicum. Qualified students shall not fill more than half of the facilitator positions "
          "required by this paragraph in any administration session, and a session staffed in part by qualified students "
          "shall include at least one certified facilitator.")
    + " Exception: the department may waive or decrease this ratio if the department determines that the ratio specified "
      "presents a barrier for patients and that safety concerns are otherwise alleviated.",
))

P.append((
    "7.35.3.20",
    "Subsection M, designation of owners and employees",
    NEW,
    ins("M. Designation of owners and employees: A healing center shall submit to the department, through the "
        "electronic system designated by the department, a current list of the owners and employees the healing center "
        "designates to purchase, possess, sell or administer medical psilocybin products, identifying which of those "
        "activities each designated individual is authorized to engage in. A healing center shall update the list within "
        "five business days of a change. An individual is designated for purposes of Subsection C of 7.35.3.14 NMAC on "
        "submission of the list identifying them."),
))

# ---- 7.35.3.29 -------------------------------------------------------------

P.append((
    "7.35.3.29",
    "Entire section, supervised practice with practicum participants who are not qualified patients",
    NEW,
    ins("7.35.3.29 SUPERVISED PRACTICE WITH PRACTICUM PARTICIPANTS WHO ARE NOT QUALIFIED PATIENTS:") + "<br>"
    + ins("A. Purpose: This section provides for stage one of the practicum sequence required by Subsection D of "
          "7.35.3.19 NMAC to be conducted with practicum participants who are not qualified patients, so that a student "
          "gains supervised experience of administration sessions before the student works with qualified patients.") + "<br>"
    + ins("B. Practicum participant: A practicum participant is an individual who: (1) is 21 years of age or older; "
          "(2) is not a qualified patient and is not enrolled in the medical psilocybin program; (3) volunteers to take "
          "part in a practicum session, pays no fee for the session and receives no compensation for taking part; (4) has "
          "been screened for contraindications by a certifying clinician, or by a {{PT}} acting within the scope of the "
          "{{PT}}'s professional license, using criteria approved by the department; and (5) has given written informed "
          "consent on a form approved by the department, which shall state that the session is a training session, that "
          "the participant is not receiving medical psilocybin services for a qualifying condition, and that the "
          "participant may withdraw at any time.") + "<br>"
    + ins("C. Conduct of practicum sessions: A practicum session under this section shall: (1) take place at a healing "
          "center or other approved location; (2) be supervised on site by a practicum supervisor; "
          "(3) meet the staffing ratios in Paragraph (5) of Subsection H of 7.35.3.20 "
          "NMAC, counting practicum participants as patients for that purpose; (4) include a preparation session and an "
          "integration session for each practicum participant; and (5) use only medical psilocybin products obtained "
          "from permitted producers.") + "<br>"
    + ins("D. Records and reporting: A healing center or registrant of another approved location shall record practicum "
          "sessions in the daily log required by Subsection E of 7.35.3.20 NMAC, and shall report any potential adverse "
          "health event arising from a practicum session in accordance with Subsection L of 7.35.3.20 NMAC. An "
          "educational program shall record practicum sessions under this section in the records required by Subsection "
          "C of 7.35.3.17 NMAC.") + "<br>"
    + ins("E. Limits: A practicum participant shall not be charged for, and shall not purchase, medical psilocybin "
          "products. Hours completed under this section count only toward stage one of the practicum sequence and shall "
          "not be counted toward the patient and session minimums in Subsections A and B of 7.35.3.19 NMAC.") + "<br>"
    + ins("F. Effect: This section applies only to the extent that the Medical Psilocybin Act, Sections 26-2D-1 through "
          "-11 NMSA 1978, authorizes the administration of medical psilocybin to a person who is not a qualified "
          "patient. If and for so long as it does not, stage one of the practicum sequence is governed by the second "
          "sentence of Paragraph (1) of Subsection D of 7.35.3.19 NMAC."),
))


# ---------------------------------------------------------------------------
# Verification of the left column against the published PDF
# ---------------------------------------------------------------------------

def flatten(t):
    t = t.replace("’", "'").replace("‘", "'")
    t = t.replace("“", '"').replace("”", '"')
    t = t.replace("‐", "-").replace("‑", "-")
    return re.sub(r"\s+", " ", t).strip()


def read_published():
    """Reconstruct the published rule's text in true reading order.

    pdfminer's container order does not follow the page for this PDF: subsection
    letters and paragraph numbers are emitted separately from their body text.
    Text lines are therefore clustered into visual lines by baseline proximity,
    ordered top to bottom, and read left to right within each line. That rebuilds
    the single-column reading order, which lets the left column be verified by
    exact contiguous match rather than by a fuzzy one.
    """
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LTTextContainer, LTTextLine
    out = []
    for page in extract_pages(str(PUBLISHED_PDF)):
        items = []
        for element in page:
            if not isinstance(element, LTTextContainer):
                continue
            for line in element:
                if isinstance(line, LTTextLine) and line.get_text().strip():
                    items.append((line.y0, line.x0, line.get_text().rstrip("\n")))
        items.sort(key=lambda r: -r[0])
        clusters = []
        for y, x, text in items:
            if clusters and abs(clusters[-1][0] - y) <= LINE_TOLERANCE:
                clusters[-1][1].append((x, text))
            else:
                clusters.append((y, [(x, text)]))
        for _, parts in clusters:
            parts.sort(key=lambda r: r[0])
            out.append(" ".join(t for _, t in parts))
    return flatten(" ".join(out))


def verify():
    corpus = read_published()
    failures = []
    for section, sub, published, _ in P:
        if published in (NEW, UNCHANGED):
            continue
        for chunk in published.split("\n"):
            c = flatten(chunk)
            if c and c not in corpus:
                failures.append((section, sub, c[:110]))
    return failures


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

CSS = """
@page { size: letter landscape; margin: 0.55in 0.5in 0.6in 0.5in;
        @bottom-center { content: counter(page); } }
* { box-sizing: border-box; }
body { font-family: "Times New Roman", Times, Georgia, serif; font-size: 8.6pt;
       line-height: 1.34; color: #111; margin: 0; }
h1 { font-family: Helvetica, Arial, sans-serif; font-size: 15pt; margin: 0 0 2pt 0;
     letter-spacing: -0.2pt; }
.sub { font-family: Helvetica, Arial, sans-serif; font-size: 8.6pt; color: #444;
       margin: 0 0 5pt 0; line-height: 1.45; max-width: 7.2in; }
.cover { border-bottom: 2px solid #111; padding-bottom: 12pt; margin-bottom: 16pt; }
.keybox { border: 1px solid #bbb; background: #fafafa; padding: 11pt 14pt; margin: 0 0 16pt 0;
          font-family: Helvetica, Arial, sans-serif; font-size: 8.1pt; line-height: 1.62; }
.keybox b { font-size: 8.4pt; }
.keybox, .status { break-inside: avoid; }
.keybox p { margin: 0 0 7pt 0; }
.keybox p:last-child { margin-bottom: 0; }
.status { border: 1.5px solid #111; background: #fff; padding: 11pt 14pt; margin: 0 0 16pt 0;
          font-family: Helvetica, Arial, sans-serif; font-size: 8.4pt; line-height: 1.62; }
.status p { margin: 0 0 7pt 0; }
.status p:last-child { margin-bottom: 0; }
.thsub { display: block; font-weight: normal; text-transform: none; letter-spacing: 0;
         font-size: 7.1pt; color: #777; margin-top: 2pt; }
p.intro { font-family: Helvetica, Arial, sans-serif; font-size: 8.1pt; line-height: 1.5;
          color: #333; margin: 0 0 8pt 0; padding: 0 0 0 8pt; border-left: 2.5px solid #bbb;
          break-after: avoid; }
h2 { font-family: Helvetica, Arial, sans-serif; font-size: 11pt; margin: 18pt 0 7pt 0;
     padding: 3pt 0 3pt 0; border-top: 1.5px solid #111; border-bottom: 0.5px solid #111;
     break-after: avoid; }
h2 .ttl { font-weight: normal; color: #555; font-size: 9pt; }
table { width: 100%; border-collapse: collapse; }
tr { break-inside: avoid; }
th { font-family: Helvetica, Arial, sans-serif; font-size: 7.6pt; text-transform: uppercase;
     letter-spacing: 0.4pt; color: #333; text-align: left; padding: 5pt 9pt 6pt 9pt;
     border-bottom: 1px solid #999; width: 50%; vertical-align: top; }
td { vertical-align: top; padding: 8pt 9pt 10pt 9pt; border-bottom: 0.5px solid #ddd; width: 50%; }
td.left { border-right: 1px solid #ccc; color: #333; background: #fcfcfc; }
.label { font-family: Helvetica, Arial, sans-serif; font-size: 7.6pt; font-weight: bold;
         color: #000; margin-bottom: 3pt; }
ins { text-decoration: underline; color: #0a5c2e; font-weight: bold; }
del { text-decoration: line-through; color: #9b1c1c; }
.none { color: #888; font-style: italic; }
.note { color: #666; font-style: italic; font-size: 7.9pt; }
.unch { color: #666; font-style: italic; }
.foot { margin-top: 16pt; border-top: 1.5px solid #111; padding-top: 8pt;
        font-family: Helvetica, Arial, sans-serif; font-size: 7.9pt; line-height: 1.5; }
.hours { width: 100%; border-collapse: collapse; font-family: Helvetica, Arial, sans-serif;
         font-size: 8pt; margin-top: 6pt; }
.hours th, .hours td { border: 0.5px solid #bbb; padding: 4pt 8pt; width: auto; text-align: left;
                      vertical-align: middle; }
.hours th { background: #f2f2f2; text-transform: none; letter-spacing: 0; color: #222; }
.hours td.n { text-align: right; }
h2.addendum { break-before: page; }
table.dep { width: 100%; border-collapse: collapse; font-family: Helvetica, Arial, sans-serif;
            font-size: 7.9pt; margin: 4pt 0 10pt 0; }
table.dep th, table.dep td { border: 0.5px solid #bbb; padding: 4pt 7pt; width: auto; text-align: left;
                             vertical-align: top; text-transform: none; letter-spacing: 0; }
table.dep th { background: #f2f2f2; color: #222; font-size: 7.6pt; }
table.dep td.amd { color: #0a5c2e; font-weight: bold; }
table.dep td.flag { color: #9b1c1c; }
table.dep td.ok { color: #0a5c2e; font-weight: bold; }
table.dep td.bad { color: #9b1c1c; font-weight: bold; }
.prov { margin-top: 6pt; padding-top: 4pt; border-top: 0.5px dashed #bbb;
        font-family: Helvetica, Arial, sans-serif; font-size: 7.2pt; line-height: 1.45; color: #555; }
.prov span { display: inline-block; text-transform: uppercase; letter-spacing: 0.5pt; font-size: 6.5pt;
             color: #888; margin-right: 5pt; }
.callout { border: 1.5px solid #9b1c1c; background: #fdf6f6; padding: 11pt 14pt; margin: 0 0 16pt 0;
           font-family: Helvetica, Arial, sans-serif; font-size: 8.2pt; line-height: 1.6; break-inside: avoid; }
.callout p { margin: 0 0 7pt 0; }
.callout p:last-child { margin-bottom: 0; }
.callout b { color: #9b1c1c; }
"""


def render(t):
    for k, v in PERMIT_TITLE.items():
        t = t.replace(k, v)
    return t


def esc_plain(t):
    return html.escape(t).replace("\n", "<br>")


def build_html():
    rows = []
    current = None
    for section, sub, published, proposed in P:
        if section != current:
            if current is not None:
                rows.append("</table>")
            current = section
            rows.append('<h2>%s <span class="ttl">%s</span></h2>' % (section, SECTION_TITLES[section]))
            if section in SECTION_INTRO:
                rows.append('<p class="intro">%s</p>' % SECTION_INTRO[section])
            rows.append('<table><tr><th>Current language<span class="thsub">Proposed rule as published July 23, 2026</span></th>'
                        '<th>Proposed amendment<span class="thsub">Draft for review. Not filed, not adopted</span></th></tr>')
        if published == UNCHANGED:
            rows.append('<tr><td class="left"><div class="label">%s</div>'
                        '<span class="unch">Not amended.</span></td>'
                        '<td><div class="label">%s</div>'
                        '<span class="unch">Not amended.</span></td></tr>'
                        % (render(sub), render(sub)))
            continue
        left = ('<span class="none">%s</span>' % NEW) if published == NEW else esc_plain(published)
        prov = provenance_for(section, sub)
        prov_html = ('<div class="prov"><span>Source</span>%s</div>' % render(prov)) if prov else ''
        rows.append('<tr><td class="left"><div class="label">%s</div>%s</td>'
                    '<td><div class="label">%s</div>%s%s</td></tr>'
                    % (render(sub), left, render(sub), render(proposed), prov_html))
    rows.append("</table>")
    return "\n".join(rows)


# Where every proposed change comes from. "Drafting" means it appears in no source
# and was written to make something else work; those are the ones to argue with first.
PROVENANCE = {
    ("7.35.3.14", "Section heading"): "Drafting, required to make the training permit operative. The section-number "
        "correction is a defect in the rule as published.",
    ("7.35.3.14", "Subsection A"): "Drafting, consequential on proposed 7.35.3.29. Strike if 7.35.3.29 is not adopted.",
    ("7.35.3.14", "Subsection B"): "Drafting, consequential on proposed 7.35.3.29. Strike if 7.35.3.29 is not adopted.",
    ("7.35.3.14", "Subsection C"): "Defect in the rule as published: the condition points at a registration that the "
        "rule never creates.",
    ("7.35.3.14", "Subsection D"): "Metz, Recommendation 3, training permit, page 4.",
    ("7.35.3.18", "Subsection A"): "Metz, Recommendation 2, New Mexico module 6 to 8 hours, page 2. Eight is the top "
        "of her range.",
    ("7.35.3.18", "Subsection C, {{PT_C}} and facilitator psilocybin therapy module, lead-in"):
        "Metz, Recommendation 2, single 84-hour standard, page 1.",
    ("7.35.3.18", "Subsection C, required topics"): "Metz, Recommendation 2 curriculum table, pages 2 and 3, for every "
        "topic and every hour figure except post-traumatic stress disorder, which comes from the July 17 committee "
        "record and is scoped to the limits Metz states at page 2.",
    ("7.35.3.18", "Subsection D"): "Drafting. One hour added to each role-specific module so the components reach the "
        "84-hour total.",
    ("7.35.3.18", "Subsection E"): "Drafting. One hour added to each role-specific module so the components reach the "
        "84-hour total.",
    ("7.35.3.18", "Subsection F"): "Defect in the rule as published: the sentence does not complete. Grammar only.",
    ("7.35.3.18", "Subsection H"): "Metz, Recommendation 2, page 3: \u201cComponent ranges are illustrative; the "
        "binding minimum is the total.\u201d",
    ("7.35.3.18", "Subsection I"): "Drafting. Addresses a defect in the rule as published: the module gates every "
        "pathway and carries no delivery date. The 90 days is a drafting choice.",
    ("7.35.3.19", "Subsection A"): "Metz, Recommendation 3, practicum totals, page 4. The entry-gate wording is "
        "drafting, addressing an ambiguity in the rule as published.",
    ("7.35.3.19", "Subsection B"): "Drafting. Resolves an ambiguity in the rule as published about whether the "
        "patients counted here may be the same patients counted in Subsection A. Hours unchanged.",
    ("7.35.3.19", "Subsection C"): "Metz, Recommendation 3 step 4, 10 hours, page 4. The sentence stating that the "
        "hours sit inside the total is drafting.",
    ("7.35.3.19", "Subsection D"): "Metz, Recommendation 3 steps 1 to 4, pages 3 and 4. The stage hour figures are "
        "hers; the lead-in preserving supervisor discretion is drafting, written to the objection recorded on July 17.",
    ("7.35.3.19", "Subsection E"): "Metz, Recommendation 3, placement logistics, page 4: an approved supervisor at an "
        "approved location may host students not enrolled at a co-located program.",
    ("7.35.3.19", "Subsection F"): "Not amended. Re-lettered only.",
    ("7.35.3.19", "Subsection G"): "Metz, Recommendation 3, training permit, page 4. The application items, the term, "
        "and the appeal route are drafting.",
    ("7.35.3.19", "Subsection H"): "Metz, Recommendation 4, pages 4 and 5. Twenty is the bottom of her stated range.",
    ("7.35.3.19", "Subsection I"): "Metz, Recommendation 4, end-of-life checkpoint, page 5.",
    ("7.35.3.19", "Subsection J"): "Drafting. Addresses a defect in the rule as published: the waiver has no criteria, "
        "no procedure and no time limit. Every figure in the added text is a drafting choice.",
    ("7.35.3.19", "Subsection K"): "Defect in the rule as published: this waiver and 7.35.3.10 D(1) set different "
        "group-session floors for the same 40 hours.",
    ("7.35.3.20", "Subsection H(5)"): "July 17 committee record, where counting students toward the ratio was "
        "proposed and taken back for review. The substitution of the training permit for bare registration, and the "
        "cap on how many positions students may fill, are drafting.",
    ("7.35.3.20", "Subsection M"): "Drafting. Required by 7.35.3.14 C, which points at a registration the rule does "
        "not create.",
    ("7.35.3.29", "Entire section"): "Metz, Recommendation 3 step 1, page 3. The participant definition, the consent "
        "and screening requirements, and the contingency clause are drafting.",
}


def provenance_for(section, sub):
    for (sec, key), text in PROVENANCE.items():
        if sec == section and sub.startswith(key):
            return text
    return None


SECTION_INTRO = {
    "7.35.3.14": "This section is the one that grants authority to hold and hand over the medicine. Everything the "
                 "practicum asks a student to do depends on it. The amendments add a fourth class of person, the "
                 "training permittee, and repair a condition in Subsection C that cannot currently be satisfied.",
    "7.35.3.18": "The educational requirements. The amendments set a single binding standard of 84 module hours for "
                 "both permit types, give the New Mexico module an hour count and a delivery date it currently lacks, "
                 "and add the content areas that were requested on the record on July 17 and did not appear in the "
                 "rule as published.",
    "7.35.3.19": "The practicum. This is the section the work was commissioned to address, and the other three "
                 "sections in this document are here because this one depends on them. The amendments move hours out "
                 "of the practicum and into the classroom and consultation, add a staged sequence, create the "
                 "training permit that makes the practicum lawful, open practicum placement beyond a student's own "
                 "program, and put standards on a waiver that currently has none.",
    "7.35.3.20": "Healing centers and other approved locations. Only two provisions are touched: the staffing ratio, "
                 "because it counts students toward mandatory staffing, and a new subsection creating the "
                 "designation that 7.35.3.14 C requires and the rule never established.",
    "7.35.3.29": "PROPOSED NEW SECTION. Nothing in the rule as published corresponds to it. It would provide for the "
                 "first stage of the practicum to be conducted with participants who are not qualified patients, "
                 "which is step 1 of the July 17 recommendation. It is drafted with an express contingency, because "
                 "the Medical Psilocybin Act as read for this draft does not extend its criminal and civil exemption "
                 "to a person who is not a qualified patient, a clinician, or a producer. Read it as the text that "
                 "would be needed if the Legislature supplies that authority, and as a statement of the ask if it "
                 "does not.",
}

SECTION_TITLES = {
    "7.35.3.14": "Authorized possession, purchase, or sale of medical psilocybin",
    "7.35.3.18": "Educational requirements for certifying clinicians, practitioners, and facilitators",
    "7.35.3.19": "Practicum requirements for practitioners and facilitators",
    "7.35.3.20": "Requirements for healing centers and other approved locations",
    "7.35.3.29": "New section. Supervised practice with practicum participants who are not qualified patients",
}

HEAD = """
<div class="cover">
<h1>7.35.3 NMAC: proposed amendments to the training and education provisions</h1>
<p class="sub"><b>Version {VERSION}, {VERSION_DATE}.</b> A side-by-side working draft, prepared against the proposed
rule published July 23, 2026. Rule hearing set for August 28, 2026. Version history is at the end.</p>
</div>

<div class="status">
<p><b>What this is, and what it is not.</b> This is a working draft for review. Nothing in it is definitive,
nothing has been filed, and nothing has been adopted. It is offered so that counsel and the committee can work from
specific proposed language rather than from a list of concerns, and can see, provision by provision, exactly what
would change and exactly what would not.</p>
<p><b>What has been done to it.</b> Every word in the left column has been checked against the text layer of the
published rule and matches it exactly; the document does not build if any block fails that check. Every proposed
change traces to the rule as published, to the July 17, 2026 recommendations, or to what was said on the record at
the two July 17, 2026 meetings. The reasoning and the citation for each one sit in the accompanying files, which
are named at the end.</p>
<p><b>What it deliberately leaves alone.</b> It covers the practicum and the provisions the practicum cannot
function without. It is not a review of the whole of Part 3, and it is not a filing. Where a fix would require
changing something outside that scope, the point is flagged and the language is not drafted.</p>
</div>

<div class="keybox">
<p><b>How to read the columns.</b> The left column is the rule as published, verbatim, with line breaks introduced
by the PDF collapsed to single spaces and no other alteration. The right column is the proposed amendment:
<ins>underlined bold green is inserted</ins>, <del>struck red is deleted</del>, and unmarked text is carried forward
unchanged. Where a section has subsections that are not being amended, they are named and marked so the extent of
what is and is not touched is visible on the page.</p>
<p><b>Permit title.</b> The draft keeps &ldquo;practitioner.&rdquo; It does not adopt &ldquo;licensed provider.&rdquo;
The title is held as a variable in the source and substituted here, so that if the committee changes it, it changes
everywhere in one pass. The term is defined in 7.35.2.7 NMAC, a different part, which 7.35.3.7 NMAC incorporates by
reference, so a retitle is an amendment to that part as well.</p>
<p><b>Section numbering.</b> The published headings for 7.35.3.14 and 7.35.3.20 read 7.34.3.14 and 7.34.3.20, which
point at a different chapter of Title 7, while the bracketed history note at the end of each of those sections reads
7.35.3. Three further headings carry the same error. The corrections are shown in the right column.</p>
<p><b>Proposed new provisions.</b> Four provisions in this document do not exist in the rule as published:
7.35.3.14 D, 7.35.3.19 D, F, H, I and J, 7.35.3.20 M, and the whole of 7.35.3.29. Each is introduced where it
appears. 7.35.3.29 in particular is drafted with an express contingency and should be read with the note above it.</p>
</div>


<div class="callout">
<p><b>Please comb this one twice: 7.35.3.19 C, the supervision hours.</b> It is the one place where the rule as
published can be read two ways, and the reading decides a number in this draft.</p>
<p><b>What the rule says.</b> 7.35.3.19 A sets the practicum at "100 hours ... for facilitators and 120 hours for
practitioners". 7.35.3.19 C then says practitioners "shall complete an additional minimum of 20 hours as a
practitioner supervising facilitators", without saying what the 20 hours are additional to.</p>
<p><b>Reading 1, which this draft assumes.</b> The 20 sit inside the 120. A facilitator does 100, a practitioner does
the same 100 plus 20 supervision, which is the 120 already stated. Published practitioner program total: 170.</p>
<p><b>Reading 2, which the word "additional" supports on its face.</b> The 20 sit on top of the 120, so the
practitioner practicum is 140. Published practitioner program total: 190.</p>
<p><b>What Metz recommended.</b> "Supervisory hours, Licensed Providers only (10 hours) ... Reduced from the 20 hours
in the 6-12-26 draft" (July 17 recommendation, page 4). Her totals read as inclusive: 62 hours for a Facilitator and
72 for a Licensed Provider, a difference of exactly the 10 supervisory hours. So her model uses reading 1.</p>
<p><b>What this draft does.</b> Adopts reading 1 and says so in terms, so the ambiguity does not survive into the
amended rule. It then sets the practitioner practicum at 90 rather than at Metz's 72, purely so that the proposed
total clears the published requirement on reading 2 as well. That single defensive choice is the only reason the
number is not 72. Addendum C sets out the arithmetic.</p>
<p><b>The questions for this group.</b> Is reading 1 what the department intended? Is 170 the number everyone has in
their head, or does anyone read the published draft as 190? If reading 1 is confirmed, the practitioner practicum can
drop to 72 and the total still rises, from 170 to 176. If it is not confirmed, 90 stays. Either way the amended text
should say which reading governs, because as published it does not.</p>
</div>

<div class="keybox">
<p><b>The hours, at a glance.</b> Hours shift. They do not shrink. Total program hours rise for both permit types.
The 84-hour standard is inclusive of the 5-hour simulated patient experience.</p>
<table class="hours">
<tr><th>Component</th><th>As published July 23</th><th>Proposed</th><th>Change</th></tr>
<tr><td>Didactic hours</td><td>35, plus a New Mexico module with no hour count</td><td>79</td><td class="n">+44</td></tr>
<tr><td>Simulated patient experience</td><td>5</td><td>5</td><td class="n">0</td></tr>
<tr><td><b>Module total, either permit</b></td><td><b>40, plus an unpriced module</b></td><td><b>84</b></td><td class="n"><b>+44</b></td></tr>
<tr><td>Practicum, facilitator</td><td>100</td><td>80</td><td class="n">&minus;20</td></tr>
<tr><td>Practicum, practitioner</td><td>120, or 140 on the second reading of 7.35.3.19 C</td><td>90</td><td class="n">&minus;30</td></tr>
<tr><td>Supervision or consultation</td><td>10</td><td>20</td><td class="n">+10</td></tr>
<tr><td><b>Program total, facilitator</b></td><td><b>150</b></td><td><b>184</b></td><td class="n"><b>+34</b></td></tr>
<tr><td><b>Program total, practitioner</b></td><td><b>170, or 190</b></td><td><b>194</b></td><td class="n"><b>+24</b></td></tr>
</table>
<p>Every patient and session minimum in the published practicum is carried forward unchanged: 14 different patients,
eight different administration day sessions, six individual sessions with six different patients, two group sessions
with four or more patients each, and 20 hours of preparation and integration sessions. Only hours move.</p>
</div>
"""


ADDENDA = """
<h2 class="addendum">Addendum A <span class="ttl">Practicum dependency map</span></h2>
<p class="intro">Every provision the practicum depends on, in and out of this document. The practicum is
7.35.3.19. It cannot function without each row below. The Status column says whether this draft touches it.</p>
<table class="dep">
<tr><th>Provision</th><th>Page</th><th>What the practicum needs from it</th><th>Status in this draft</th></tr>
<tr><td>7.35.2.7 NMAC</td><td>n/a</td><td>Supplies every defined term used in Part 3, by force of 7.35.3.7. Defines practitioner, guide, clinician, qualified patient, approved location, administration session</td><td class="flag">Not amended. Defect flagged: facilitator, healing center, certifying clinician and student are used throughout Part 3 and defined nowhere</td></tr>
<tr><td>Medical Psilocybin Act, Section 5</td><td>n/a</td><td>The criminal and civil exemption. Reaches producers, clinicians and qualified patients, and protects presence only for anyone else</td><td class="flag">Statute. Cannot be reached by rule</td></tr>
<tr><td>7.35.3.9 C(3)</td><td>3</td><td>Certification application requires documentation of completed practicum</td><td>Not amended</td></tr>
<tr><td>7.35.3.9 E(1)</td><td>3</td><td>Practitioner licensure predicate. Decides what a practitioner student may do under 7.35.3.19 B "when licensure allows"</td><td class="flag">Not amended. Flagged</td></tr>
<tr><td>7.35.3.9 E(2), F(1)</td><td>3</td><td>Both certification lists require documentation of the department-approved practicum</td><td>Not amended</td></tr>
<tr><td>7.35.3.10 D</td><td>5</td><td>Out-of-jurisdiction 40-hour practicum waiver</td><td class="flag">Not amended. Conflicts with 7.35.3.19 L; conforming amendment flagged</td></tr>
<tr><td>7.35.3.11 A, B</td><td>5 to 7</td><td>Healing centers and other approved locations. The practicum may only happen in them</td><td>Not amended</td></tr>
<tr><td>7.35.3.12 A</td><td>7</td><td>Educational program certification. A training permit requires registration with a certified program</td><td>Not amended</td></tr>
<tr><td>7.35.3.13 B</td><td>8</td><td>Facilitator scope of work. Limits what a facilitator may do after certification, and so what the practicum can usefully train</td><td class="flag">Not amended. Flagged</td></tr>
<tr><td class="amd">7.35.3.14</td><td>9</td><td>The authority to possess and administer. Without it no student may lawfully handle the medicine</td><td class="amd">AMENDED. New Subsection D</td></tr>
<tr><td>7.35.3.15 A(4)</td><td>9</td><td>Practicum site agreements need prior written departmental approval, with no deadline on the department</td><td class="flag">Not amended. Flagged</td></tr>
<tr><td>7.35.3.17 A</td><td>10 to 11</td><td>The 10 mentoring hours, credited toward the consultation requirement</td><td class="flag">Not amended. Flagged</td></tr>
<tr><td>7.35.3.17 B</td><td>11</td><td>Test-out. Makes practicum completion a condition of graduation, which may empty the December 31, 2027 waiver</td><td class="flag">Not amended. Flagged</td></tr>
<tr><td>7.35.3.17 C(2)(d), (e)</td><td>11</td><td>Records of practicum sessions, dates, locations, patient counts, and supervised facilitators</td><td>Not amended</td></tr>
<tr><td class="amd">7.35.3.18 A, C, D, E</td><td>11 to 12</td><td>The didactic requirement the practicum entry gate is measured against</td><td class="amd">AMENDED</td></tr>
<tr><td>7.35.3.18 F</td><td>12</td><td>Life support and HIPAA currency, carried into the training permit application</td><td class="amd">Amended for grammar only</td></tr>
<tr><td class="amd">7.35.3.19</td><td>12 to 13</td><td>The practicum itself</td><td class="amd">AMENDED throughout. Re-lettered A to K</td></tr>
<tr><td>7.35.3.20 D</td><td>14</td><td>Students may be present at an administration session. This is the full reach of Section 5(D) of the Act and no further</td><td>Not amended</td></tr>
<tr><td>7.35.3.20 E, L</td><td>14 to 15</td><td>Daily log and adverse event reporting, which the proposed 7.35.3.29 relies on</td><td>Not amended</td></tr>
<tr><td class="amd">7.35.3.20 H(5)</td><td>14</td><td>Staffing ratio. Counts a qualified student toward mandatory session staffing</td><td class="amd">AMENDED</td></tr>
<tr><td>7.35.3.21 A</td><td>15</td><td>Department assessment authority over records and premises</td><td>Not amended</td></tr>
<tr><td>7.35.3.22</td><td>15</td><td>Prohibitions. Reaches "the qualified patient or certificant", which as published does not include a student</td><td class="flag">Not amended. Flagged</td></tr>
<tr><td>7.35.3.27</td><td>16 to 19</td><td>Discipline and appeal, which the proposed training permit denial appeal runs through</td><td>Not amended</td></tr>
</table>

<h2 class="addendum">Addendum B <span class="ttl">Proposed new provisions</span></h2>
<p class="intro">Nine provisions in this draft do not exist in the rule as published, and one more was drafted and
then withdrawn. Each is listed with what it does, what it depends on, and whether it can be dropped without breaking
anything else. The withdrawn one is kept on the page rather than deleted, so that the decision is visible and can be
reversed by asking.</p>
<table class="dep">
<tr><th>Proposed provision</th><th>What it does</th><th>Depends on</th><th>If dropped</th></tr>
<tr><td>7.35.3.14 D</td><td>Authorizes a training permittee to possess and administer under direct on-site supervision</td><td>7.35.3.19 G</td><td class="flag">The practicum stays unlawful. This and 7.35.3.19 H stand or fall together</td></tr>
<tr><td>7.35.3.18 H</td><td>States the 84-hour module total in one place, with a didactic floor of 79 inside it</td><td>7.35.3.18 A, C, D, E</td><td>Hour figures survive module by module; no total is stated anywhere</td></tr>
<tr><td>7.35.3.18 I</td><td>90-day deadline for the department to publish the New Mexico module, and relief for applicants meanwhile</td><td>7.35.3.18 A</td><td class="flag">Every certification pathway stays gated on a module with no delivery date</td></tr>
<tr><td>7.35.3.19 D</td><td>Staged practicum sequence, as minimums rather than blocks</td><td>7.35.3.19 G, 7.35.3.29</td><td>Practicum hours and patient minimums survive; the risk gradient is lost</td></tr>
<tr><td class="flag"><b>7.35.3.19 F, WITHDRAWN</b></td><td class="flag">Would have registered practicum supervisors, set a one-year experience floor, and required the department to publish a list of supervisors and available sites. <b>Withdrawn from this draft at v4.</b> The one-year floor, the registration scheme and the published list appear in no source: not in the July 17 recommendation, not in either July 17 transcript, and not in the rule as published. They were written to make Subsection E workable and are therefore invention. Subsection E, which does come from Metz at page 4, stands without them and leaves vetting where the rule already leaves it, with the department. <b>If the committee wants a supervisor provision, say so and it goes back in as a new Subsection F before the present F.</b> The underlying problem it addressed is real and is on the record: "the current draft requires that all hours be held in an approved healing center, which I think can potentially be a bottleneck for rural trainees", and the open question "who is going to vet site supervisors" was left to the committee by Metz at page 6.</td><td class="flag">Was 7.35.3.19 E</td><td class="flag">Withdrawn. Nothing else depends on it</td></tr>
<tr><td>7.35.3.19 G</td><td>Creates the training permit</td><td>7.35.3.14 D</td><td class="flag">The practicum stays unlawful. See 7.35.3.14 D</td></tr>
<tr><td>7.35.3.19 H</td><td>20 consultation hours with two presented cases and a departmental evaluation form</td><td>7.35.3.17 A for the credit</td><td>7.35.3.17 A survives at 10 hours with no requirement to have seen a client</td></tr>
<tr><td>7.35.3.19 I</td><td>End-of-life checkpoint before unsupervised end-of-life practice</td><td>7.35.3.19 H</td><td>Severable. No end-of-life competency gate remains</td></tr>
<tr><td>7.35.3.20 M</td><td>Creates the designation that 7.35.3.14 C requires</td><td>7.35.3.14 C</td><td class="flag">7.35.3.14 C keeps pointing at a registration that does not exist</td></tr>
<tr><td>7.35.3.29</td><td>Practicum with participants who are not qualified patients</td><td>Statutory change</td><td>Severable. 7.35.3.19 D(1) falls to its second limb and stage one becomes observation</td></tr>
</table>

<h2 class="addendum">Addendum C <span class="ttl">Why the practitioner practicum is drafted at 90</span></h2>
<p class="intro">7.35.3.19 C as published requires "an additional minimum of 20 hours" of supervision without
saying what the 20 hours are additional to. That single ambiguity is the only reason this number is not simply the
72 in the July 17 recommendation. The two readings, and what each makes the published requirement:</p>
<table class="dep">
<tr><th>Reading of the published 7.35.3.19 C</th><th>Published practitioner practicum</th><th>Published practitioner program total</th></tr>
<tr><td><b>Reading 1.</b> The 20 hours are inside the 120. 100 for a facilitator plus 20 gives the 120 stated in Subsection A. This is the natural reading and the one this draft adopts and states expressly</td><td>120</td><td><b>170</b></td></tr>
<tr><td><b>Reading 2.</b> The 20 hours are on top of the 120, which is what the word "additional" says on its face</td><td>140</td><td><b>190</b></td></tr>
</table>
<p class="intro" style="border:0;padding-left:0;margin-top:9pt">The proposal must exceed the published requirement on
both readings, because the draft cannot settle what the published text means, only what the amended text will mean.
With the module fixed at 84 and consultation at 20, the practitioner program total is 104 plus the practicum:</p>
<table class="dep">
<tr><th>Practitioner practicum</th><th>Program total</th><th>Against reading 1 (170)</th><th>Against reading 2 (190)</th></tr>
<tr><td>72, as recommended July 17</td><td>176</td><td class="ok">clears by 6</td><td class="bad">short by 14</td></tr>
<tr><td>80</td><td>184</td><td class="ok">clears by 14</td><td class="bad">short by 6</td></tr>
<tr><td>86</td><td>190</td><td class="ok">clears by 20</td><td class="bad">ties, does not clear</td></tr>
<tr><td><b>90, as drafted</b></td><td><b>194</b></td><td class="ok"><b>clears by 24</b></td><td class="ok"><b>clears by 4</b></td></tr>
</table>
<p class="intro" style="border:0;padding-left:0;margin-top:9pt">The facilitator side is never at risk. The published
facilitator total is 150 on both readings and the module alone rises by 44, so any practicum at or above 36 hours
clears it. The decision is only about the practitioner number, and only about whether it matters to be safe against
reading 2.</p>

<h2 class="addendum">Addendum D <span class="ttl">Definitions that need to be updated, and where</span></h2>
<p class="intro">Not proposed here and not for the August 28 hearing draft in this document. Recorded because it
affects every provision in it, and because it cannot be fixed inside Part 3. 7.35.3.7, page 1, provides in full:
"The definitions in 7.35.2.7 NMAC apply to this part." 7.35.2 NMAC was adopted effective June 23, 2026.</p>
<table class="dep">
<tr><th>Term used in Part 3</th><th>Defined in 7.35.2.7?</th><th>What 7.35.2.7 has instead</th><th>Consequence</th></tr>
<tr><td><b>Facilitator</b></td><td class="bad">No. Appears zero times in 7.35.2 NMAC</td><td>"Guide" an individual who has completed training and education approved by the department to be able to assist practitioners during the administration sessions and who has been registered with the department</td><td class="flag">Every facilitator provision in Part 3 rests on an undefined term. A guide holds no professional license, so a facilitator is not a "clinician" under Section 3(B) of the Act, while 7.35.3.14 B authorizes facilitators to possess and provide</td></tr>
<tr><td><b>Healing center</b></td><td class="bad">No</td><td>"Approved location" means a location approved by the department for psilocybin administration sessions</td><td class="flag">Healing centers are certified, inspected and regulated throughout Part 3 with no definition</td></tr>
<tr><td><b>Certifying clinician</b></td><td class="bad">No</td><td>"Clinician" means an approved health care provider licensed in New Mexico who holds a certification from the department to provide medical services to qualified patients</td><td>Probably the same role renamed. Should be confirmed rather than assumed</td></tr>
<tr><td><b>Student</b></td><td class="bad">No</td><td>Nothing</td><td class="flag">Carries consequence at 7.35.3.19, 7.35.3.20 D and 7.35.3.20 H(5)</td></tr>
<tr><td>Practitioner</td><td class="ok">Yes</td><td>"Practitioner" means an individual who is a licensed healthcare professional who is certified by the department to provide medical psilocybin integrative therapy, supervise guides, and who has completed department required trainings</td><td class="ok">Carries the same licensure predicate as the Act's "clinician". 7.35.3.14 A is on solid ground</td></tr>
<tr><td>Qualified patient, approved location, administration session, medical services</td><td class="ok">Yes</td><td>All present and consistent with the Act</td><td class="ok">No action</td></tr>
</table>
<p class="intro" style="border:0;padding-left:0">Two ways to fix it, both amendments outside this document: amend
7.35.2.7 to define facilitator, healing center, certifying clinician and student; or conform Part 3 to the terms
7.35.2.7 already defines. The first is cleaner and is what this drafting assumes. Either way it needs settling
before August 28, and it is a terminology pass across all 19 pages rather than a change to any one provision.</p>

<h2 class="addendum">Addendum E <span class="ttl">The permit title, laid out for decision</span></h2>
<p class="intro">Recommendation 1 of the July 17 document proposes retitling "Practitioner" as "Licensed Provider".
This draft keeps "practitioner" because the decision had not been made. The title is held as a variable in the source,
so changing it is one command and one rebuild. What follows is what the decision does and does not reach.</p>
<table class="dep">
<tr><th>Question</th><th>Answer</th><th>Basis</th></tr>
<tr><td>Does the title change any hour count?</td><td class="ok">No</td><td>Every hour figure attaches to the permit type by a bare reference to it. Substituting a different word leaves every number unchanged</td></tr>
<tr><td>Does the title change what the practicum is?</td><td class="ok">No</td><td>What the practicum is turns on the licensure predicate at 7.35.3.9 E(1), which already requires a practitioner applicant to hold a New Mexico professional license, and on facilitator scope at 7.35.3.13 B</td></tr>
<tr><td>Is the proposed name accurate to the rule as it stands?</td><td class="ok">Yes</td><td>7.35.3.9 E(1) requires "Documentation of current professional license to practice in New Mexico (e.g. PSY, LSW, LCSW)". 7.35.2.7 defines practitioner as "a licensed healthcare professional". The permit is already a licensed-provider permit</td></tr>
<tr><td>What does the change actually cost?</td><td>An amendment to 7.35.2.7 NMAC, which is a different part, plus a conforming pass over every occurrence in Part 3</td><td>7.35.3.7 imports the definitions from 7.35.2.7. The title cannot be changed inside Part 3 alone</td></tr>
<tr><td>Is there a way the change could reach the practicum after all?</td><td class="flag">Only if it comes with an eligibility change</td><td>Metz describes the title as naming "a professional license permitting delivery of medical, counseling, mental health, or behavioral health care", which is wider than the examples at 7.35.3.9 E(1). Widening that list would change who is standing in the practicum, though still not what it contains</td></tr>
</table>
<p class="intro" style="border:0;padding-left:0"><b>The test.</b> If a proposed retitle comes with no amendment to
7.35.3.9 E(1), it is a rename and nothing more, and nothing in this document changes. If it comes with one, the
eligibility question is the real proposal and should be argued as such.</p>

<h2 class="addendum">Addendum F <span class="ttl">The remaining twenty-four sections</span></h2>
<p class="intro">This document covers the practicum and the provisions it cannot function without. Part 3 has
twenty-eight sections. The rest are inventoried but not drafted. This is the map, so that the scope of what is here
is visible and the scope of what is not is not a surprise. Findings are from
<i>analysis/july23-rule-concerns.md</i>, which records five blocking and twenty-three material findings across the
whole part, and <i>analysis/july23-published-delta.md</i>, which maps ninety substantive changes between the July 9
draft and the rule as published.</p>
<table class="dep">
<tr><th>Group</th><th>Sections</th><th>Known findings</th><th>Status</th></tr>
<tr><td><b>0. Terminology</b></td><td>7.35.3.7, and 7.35.2.7 NMAC</td><td>Facilitator, healing center, certifying clinician and student are undefined</td><td class="flag">Should go first. It touches every other section, so drafting anything else before it settles means drafting twice. Addendum D</td></tr>
<tr><td><b>1. The practicum chain</b></td><td>7.35.3.14, .18, .19, .20 H(5) and M, .29</td><td>B1, B2, B4, and material findings M1, M2, M13, M14</td><td class="amd">THIS DOCUMENT</td></tr>
<tr><td>2. Educational programs</td><td>7.35.3.12, .15, .16, .17</td><td>B3 the evaluator conflict rule disqualifies the evaluators a program must hire; M5 the deferral expires the day it becomes available; M8 no deadline binds the department on instructor changes; M9 the denial grounds were deleted; M10 the evaluator standard may be unmeetable; M11 mentoring is unfunded and untied to certification; M12 the test-out price cap assumes per-module pricing</td><td>Adjacent to this document. Natural second</td></tr>
<tr><td>3. Out-of-jurisdiction pathway</td><td>7.35.3.10</td><td>M3 the two 40-hour waivers disagree; M4 the 2027 waiver may cancel itself; M6 the approved list is empty at launch and populates only retroactively; M7 individuals must commission an evaluation only a program can commission</td><td>Not drafted</td></tr>
<tr><td>4. Locations and oversight</td><td>7.35.3.11, .20, .21</td><td>B5 healing center staff authority hangs on a registration that does not exist; M16 outdoor locations need no AED while healing centers do; M18 the patient roster and the new patient-interview authority; M22 other approved locations have a 90-day term and no renewal path</td><td>Partly reached here at 7.35.3.20 H(5) and M</td></tr>
<tr><td>5. Patients, applicants, process</td><td>7.35.3.8, .9, .13, .22, .23, .24, .25, .26, .27</td><td>M15 facilitator scope conflicts with the practicum and the ratios; M17 complainants lose confidentiality and must use certified mail; M19 the benefit-risk attestation; M20 renewals can lapse while pending; M21 the re-application clause reads as a deadline; M23 two review tracks with inconsistent scope; N5 a suspended certificant can be out of practice 135 days</td><td>Not drafted. Includes the controlled-substance number, which is out of scope by decision</td></tr>
<tr><td>6. Mechanical</td><td>Throughout</td><td>N1 five section headings read 7.34.3 instead of 7.35.3; N2 two sections carry a real effective date while the rest carry placeholders; N3 a numbering gap at 7.35.3.9 D; N4 nine further drafting defects</td><td>Two of the five heading errors are corrected here. The rest are not</td></tr>
</table>
<p class="intro" style="border:0;padding-left:0">Suggested order if the whole part is taken on: terminology, then
educational programs, then out-of-jurisdiction, then locations, then patients and process, with the mechanical items
swept last in a single pass. Anything already settled here would be marked as handled in this document rather than
redrafted.</p>

<h2 class="addendum">Version history</h2>
<table class="dep">
<tr><th>Version</th><th>Date</th><th>What changed</th></tr>
%s
</table>
"""

FOOT = """
<div class="foot">
<b>Sources.</b> Published rule: <i>docs/documents/rules-draft-2026-07-23-published.pdf</i>, 19 pages, sections 7.35.3.1
through 7.35.3.28. 7.35.3.14 is at page 9, 7.35.3.18 at pages 11 and 12, 7.35.3.19 at pages 12 and 13, 7.35.3.20 at
pages 13 to 15. Recommendations: Dr. Anne Metz, <i>Recommendations on Education and Training Requirements for
Facilitators and Licensed Providers</i>, July 17, 2026, six pages, with the one-page summary and the six-slide committee
deck of the same date. July 17, 2026 transcripts, morning Advisory Board and afternoon Training and Education Committee,
both labeled &ldquo;UNOFFICIAL AUTO-GENERATED TRANSCRIPT. NO SPEAKER ATTRIBUTION.&rdquo;<br><br>
<b>Reasoning and citations for every change in this document</b> are in the repository at <i>amendments/metz-crosswalk.md</i>,
<i>amendments/7.35.3.18-19-redline.md</i>, and <i>amendments/blocking-defects.md</i>.<br><br>
<b>Addenda.</b> A, the practicum dependency map. B, the proposed new provisions, including one withdrawn. C, the arithmetic behind the practitioner practicum figure. D, definitions that need updating. E, the permit title laid out for decision. F, the remaining twenty-four sections.<br><br>
<b>Status.</b> Internal drafting work. Not a filing, not submitted to the Department of Health, and not promulgated rule
text.
</div>
"""


def main():
    failures = verify()
    if failures:
        print("VERIFICATION FAILED. Published-column text not found in the PDF:")
        for section, sub, chunk in failures:
            print("  %s %s :: %s" % (section, render(sub), chunk))
        return 1
    print("verified: every published-column block matches the published PDF")

    version_rows = "\n".join(
        "<tr><td><b>%s</b></td><td>%s</td><td>%s</td></tr>" % v for v in VERSION_HISTORY)
    doc = ("<!doctype html><html><head><meta charset='utf-8'>"
           "<title>7.35.3 NMAC practicum amendments %s</title>"
           "<style>%s</style></head><body>%s%s%s%s</body></html>"
           % (VERSION, CSS, HEAD, build_html(), ADDENDA % version_rows, FOOT))

    tmp = Path(tempfile.mkdtemp()) / "redline.html"
    tmp.write_text(doc, encoding="utf-8")

    chrome = None
    for cand in ["/opt/pw-browsers/chromium", "chromium", "chromium-browser", "google-chrome"]:
        c = shutil.which(cand) or (cand if Path(cand).exists() else None)
        if c:
            chrome = c
            break
    if not chrome:
        print("no chromium found")
        return 1

    subprocess.run([chrome, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", "--print-to-pdf=%s" % OUT_PDF,
                    tmp.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("wrote %s (%.0f KB)" % (OUT_PDF.relative_to(REPO), OUT_PDF.stat().st_size / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())

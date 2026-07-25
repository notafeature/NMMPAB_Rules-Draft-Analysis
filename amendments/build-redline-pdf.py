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
OUT_PDF = REPO / "amendments/7.35.3-training-redline-2026-07-23.pdf"

# The permit title, carried as a variable exactly as in the markdown drafts.
PERMIT_TITLE = {
    "{{PT}}": "practitioner",
    "{{PTS}}": "practitioners",
    "{{PT_C}}": "Practitioner",
    "{{PTS_C}}": "Practitioners",
    "{{PT_UC}}": "PRACTITIONER",
    "{{PTS_UC}}": "PRACTITIONERS",
}

NEW = "No counterpart in the published rule. This is new text."

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
    "a {{PT}}, facilitator, or healing center" + ins(", and issuance of a training permit under Subsection H of 7.35.3.19 NMAC,") +
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
    ins("D. Training permittees: A student who holds a current training permit issued under Subsection H of "
        "7.35.3.19 NMAC may possess medical psilocybin products, and may administer or otherwise provide those products "
        "to qualified patients, or to practicum participants in accordance with 7.35.3.29 NMAC, in administration "
        "sessions conducted at a healing center or other approved location, in each case only while under the direct, "
        "on-site supervision of a practicum supervisor registered under Subsection F of 7.35.3.19 NMAC, and only to the "
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
    "facilitators shall complete a psilocybin therapy module consisting of a minimum of " + dele("30") + " " + ins("70")
    + " didactic hours and 5 hours of simulated patient experience "
    + ins("in addition to those didactic hours") + ", prior to applying for certification, which shall include:",
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
    + ins("(19) Somatic awareness and therapeutic touch, including consent, a minimum of four didactic hours;") + "<br>"
    + ins("(20) History and traditional use of psilocybin and other psychedelics, a minimum of three didactic hours;") + "<br>"
    + ins("(21) Individual and group treatment models and group dynamics;") + "<br>"
    + dele("(16)") + " " + ins("(22)") + " A simulated patient experience of no less than 5 hours; and<br>"
    + dele("(17)") + " " + ins("(23)") + " Evaluation to demonstrate competency in the above areas.",
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
    "Subsection H, total didactic hours",
    NEW,
    ins("H. Total didactic hours: The didactic hours required by Subsections A, C and D of this section shall "
        "together total a minimum of 84 didactic hours for a facilitator applicant. The didactic hours required by "
        "Subsections A, C and E of this section shall together total a minimum of 84 didactic hours for a {{PT}} "
        "applicant. The 5 hours of simulated patient experience required by Subsection C of this section are in addition "
        "to the 84 didactic hours. The hour minimums stated for individual content areas within Subsection C are floors "
        "within the 84-hour total and do not limit an educational program's allocation of the balance of the hours."),
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
    "“practicum”, after completing at least half of the didactic " + dele("requirements")
    + ins("hours required by Subsection A of 7.35.3.18 NMAC and by Subsection C of that section, together with the "
          "didactic hours required by Subsection D or E of that section as applicable to the certification sought,")
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
          "is issued under Subsection H of this section.") + "<br>"
    + ins("(2) Stage two, co-facilitation: a minimum of 25 hours during which the student, holding a current training "
          "permit issued under Subsection H of this section, serves as the second person of a co-facilitation pair with a "
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
          "student is supervised by a practicum supervisor approved under Subsection F of this section. A healing center "
          "or other approved location that hosts a practicum student shall not be required to hold certification as a "
          "psilocybin educational program by reason of hosting the student."),
))

P.append((
    "7.35.3.19",
    "Subsection F, practicum supervisors",
    NEW,
    ins("F. Practicum supervisors:") + "<br>"
    + ins("(1) A practicum supervisor for a facilitator student shall be a certified {{PT}} or a certified facilitator. "
          "A practicum supervisor for a {{PT}} student shall be a certified {{PT}}.") + "<br>"
    + ins("(2) A practicum supervisor shall have held the applicable certification for at least one year, or shall have "
          "been certified on the basis of an educational program from another jurisdiction under 7.35.3.10 NMAC and have "
          "practiced under that jurisdiction's authority for at least one year.") + "<br>"
    + ins("(3) A practicum supervisor shall register with the department through the electronic system designated by the "
          "department, and shall submit documentation of the requirements of Paragraphs (1) and (2) of this subsection. "
          "The department shall act on a registration within 30 calendar days.") + "<br>"
    + ins("(4) The department shall maintain and publish a list of registered practicum supervisors and of healing "
          "centers and other approved locations available to host practicum students.") + "<br>"
    + ins("(5) A practicum supervisor shall provide direct, on-site supervision during any session in which a student "
          "possesses or administers medical psilocybin products."),
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
    "Subsection H, training permit",
    NEW,
    ins("H. Training permit:") + "<br>"
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
          "consultation requirement in Subsection I of this section, and shall not hold themselves out as a certified "
          "{{PT}} or facilitator.") + "<br>"
    + ins("(4) Term: A training permit is valid for 24 months from the date of issuance and may be renewed once for a "
          "further 12 months. A training permit expires on the earlier of the end of its term, the date the permittee "
          "ceases to be registered as a student with a certified psilocybin educational program, or the date the "
          "department issues the permittee a {{PT}} or facilitator certification.") + "<br>"
    + ins("(5) Status: A training permittee is a certificant for purposes of this rule."),
))

P.append((
    "7.35.3.19",
    "Subsection I, supervision and consultation; case presentation sign-off",
    NEW,
    ins("I. Supervision and consultation; case presentation sign-off:") + "<br>"
    + ins("(1) A training permittee shall complete a minimum of 30 hours of supervision or consultation during the "
          "training permit period, in addition to the practicum hours required by this section.") + "<br>"
    + ins("(2) Sign-off requires the permittee to present a minimum of two cases of qualified patients with whom the "
          "permittee has personally worked in the medical psilocybin program. Each case presentation shall take the form "
          "of a biopsychosocial case conceptualization addressing presenting concerns, risk factors, supportive factors, "
          "treatment considerations, and recommendations for aftercare.") + "<br>"
    + ins("(3) The supervisor or consultant shall complete an evaluation on a form approved by the department for each "
          "case presented, and shall submit it through the electronic system designated by the department.") + "<br>"
    + ins("(4) The 10 hours of mentoring sessions required by Subsection A of 7.35.3.17 NMAC are credited toward the 30 "
          "hours required by this subsection.") + "<br>"
    + ins("(5) The requirements of this subsection shall be completed prior to applying for certification."),
))

P.append((
    "7.35.3.19",
    "Subsection J, end-of-life practice",
    NEW,
    ins("J. End-of-life practice: Before providing medical psilocybin services to a patient enrolled on the basis of "
        "end-of-life care other than under the direct supervision of a {{PT}} or facilitator who meets the requirements "
        "of this subsection, a {{PT}} or facilitator shall have completed at least one co-facilitated end-of-life case "
        "during the practicum and presented at least one end-of-life case under Subsection I of this section."),
))

P.append((
    "7.35.3.19",
    "Subsection K, waiver of practicum requirements (published Subsection F)",
    "F. Waiver of practicum requirements: The department may otherwise waive, temporarily suspend, "
    "or reduce the practicum requirements for individuals applying for certification, in order to facilitate the certification "
    "of individuals trained by other government-approved programs, and to build the initial infrastructure of the program.",
    dele("F.") + " " + ins("K.") + " Waiver of practicum requirements: The department may otherwise waive, temporarily "
    "suspend, or reduce the practicum requirements for individuals applying for certification, in order to facilitate the "
    "certification of individuals trained by other government-approved programs, and to build the initial infrastructure "
    "of the program. "
    + ins("The department shall act on a request under this subsection within 30 calendar days and shall state the basis "
          "for its decision in writing. The department shall not under this subsection: (1) reduce an applicant's "
          "practicum below 40 hours of contact time with qualified patients; (2) waive the requirements of Subsection I "
          "of this section; or (3) authorize any person to possess or administer medical psilocybin products who is not "
          "certified or does not hold a current training permit. The department shall publish the number of waivers "
          "granted under this subsection and the general grounds for them, at least annually."),
))

P.append((
    "7.35.3.19",
    "Subsection L, waiver for applications received by December 31, 2027 (published Subsection G)",
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
    dele("G.") + " " + ins("L.") + " Waiver of practicum hours requirement for applications received by December 31, 2027: "
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
    + ins("hold a current training permit issued under Subsection H of 7.35.3.19 NMAC and have completed at least 50 "
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
          "center or other approved location; (2) be supervised on site by a practicum supervisor registered under "
          "Subsection F of 7.35.3.19 NMAC; (3) meet the staffing ratios in Paragraph (5) of Subsection H of 7.35.3.20 "
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
.sub { font-family: Helvetica, Arial, sans-serif; font-size: 8.4pt; color: #444;
       margin: 0 0 2pt 0; }
.cover { border-bottom: 2px solid #111; padding-bottom: 8pt; margin-bottom: 10pt; }
.keybox { border: 1px solid #bbb; background: #fafafa; padding: 7pt 9pt; margin: 0 0 12pt 0;
          font-family: Helvetica, Arial, sans-serif; font-size: 7.9pt; line-height: 1.5; }
.keybox b { font-size: 8.1pt; }
h2 { font-family: Helvetica, Arial, sans-serif; font-size: 11pt; margin: 14pt 0 5pt 0;
     padding: 3pt 0 3pt 0; border-top: 1.5px solid #111; border-bottom: 0.5px solid #111;
     break-after: avoid; }
h2 .ttl { font-weight: normal; color: #555; font-size: 9pt; }
table { width: 100%; border-collapse: collapse; }
tr { break-inside: avoid; }
th { font-family: Helvetica, Arial, sans-serif; font-size: 7.4pt; text-transform: uppercase;
     letter-spacing: 0.4pt; color: #555; text-align: left; padding: 3pt 7pt; border-bottom: 1px solid #999;
     width: 50%; }
td { vertical-align: top; padding: 6pt 7pt 8pt 7pt; border-bottom: 0.5px solid #ddd; width: 50%; }
td.left { border-right: 1px solid #ccc; color: #333; }
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
.hours th, .hours td { border: 0.5px solid #bbb; padding: 3pt 6pt; width: auto; text-align: left; }
.hours th { background: #f2f2f2; text-transform: none; letter-spacing: 0; color: #222; }
.hours td.n { text-align: right; }
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
            rows.append('<table><tr><th>As published, July 23, 2026</th>'
                        '<th>As proposed</th></tr>')
        if published == UNCHANGED:
            rows.append('<tr><td class="left"><div class="label">%s</div>'
                        '<span class="unch">Not amended.</span></td>'
                        '<td><div class="label">%s</div>'
                        '<span class="unch">Not amended.</span></td></tr>'
                        % (render(sub), render(sub)))
            continue
        left = ('<span class="none">%s</span>' % NEW) if published == NEW else esc_plain(published)
        rows.append('<tr><td class="left"><div class="label">%s</div>%s</td>'
                    '<td><div class="label">%s</div>%s</td></tr>'
                    % (render(sub), left, render(sub), render(proposed)))
    rows.append("</table>")
    return "\n".join(rows)


SECTION_TITLES = {
    "7.35.3.14": "Authorized possession, purchase, or sale of medical psilocybin",
    "7.35.3.18": "Educational requirements for certifying clinicians, practitioners, and facilitators",
    "7.35.3.19": "Practicum requirements for practitioners and facilitators",
    "7.35.3.20": "Requirements for healing centers and other approved locations",
    "7.35.3.29": "New section. Supervised practice with practicum participants who are not qualified patients",
}

HEAD = """
<div class="cover">
<h1>7.35.3 NMAC, proposed amendments: training and education</h1>
<p class="sub">Side-by-side redline against the proposed rule published July 23, 2026. Rule hearing August 28, 2026.</p>
<p class="sub">Only the subsections being amended appear. Where a section has subsections that are not being amended,
they are named and marked so the reader can see the full extent of what is and is not touched.</p>
</div>

<div class="keybox">
<b>How to read this.</b> Left column is the text as published, verbatim, with line breaks introduced by the PDF
collapsed to single spaces and no other alteration. Right column is the text as proposed:
<ins>underlined bold green is inserted</ins>, <del>struck red is deleted</del>, unmarked text is carried forward
unchanged. Every left-column block was verified against the text layer of the published PDF before this file was
generated.<br>
<b>Permit title.</b> The drafts keep &ldquo;practitioner.&rdquo; They do not adopt &ldquo;licensed provider.&rdquo;
The title is carried in the source as a variable and substituted here, so it can be changed later in one pass.
The term is defined in 7.35.2.7 NMAC, a different part, which 7.35.3.7 NMAC incorporates by reference.<br>
<b>Section numbering.</b> The published headings for 7.35.3.14 and 7.35.3.20 read 7.34.3.14 and 7.34.3.20, which point
at a different chapter of Title 7, while the bracketed history note at the end of each section reads 7.35.3. Three other
headings carry the same error. The corrections are shown.<br>
<b>7.35.3.29.</b> The new section is numbered after the last section in the published rule, 7.35.3.28 SEVERABILITY.
If the department prefers severability to remain last, the new section becomes 7.35.3.28 and severability becomes
7.35.3.29.
</div>

<div class="keybox">
<b>The hours, at a glance.</b> Hours shift. They do not shrink.
<table class="hours">
<tr><th>Component</th><th>Published July 23</th><th>Proposed</th><th>Change</th></tr>
<tr><td>Didactic</td><td>35, plus a New Mexico module with no hour count</td><td>84</td><td class="n">+49</td></tr>
<tr><td>Simulated patient experience</td><td>5</td><td>5</td><td class="n">0</td></tr>
<tr><td>Practicum, facilitator</td><td>100</td><td>80</td><td class="n">&minus;20</td></tr>
<tr><td>Practicum, practitioner</td><td>120, or 140 on the second reading of 7.35.3.19 C</td><td>90</td><td class="n">&minus;30</td></tr>
<tr><td>Supervision or consultation</td><td>10</td><td>30</td><td class="n">+20</td></tr>
<tr><td><b>Program total, facilitator</b></td><td><b>150</b></td><td><b>199</b></td><td class="n"><b>+49</b></td></tr>
<tr><td><b>Program total, practitioner</b></td><td><b>170, or 190</b></td><td><b>209</b></td><td class="n"><b>+39</b></td></tr>
</table>
Every patient and session minimum in the published practicum is carried forward unchanged: 14 different patients, eight
different administration day sessions, six individual sessions with six different patients, two group sessions with four
or more patients each, and 20 hours of preparation and integration sessions. Only hours move.
</div>
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

    doc = ("<!doctype html><html><head><meta charset='utf-8'>"
           "<title>7.35.3 NMAC training and education redline</title>"
           "<style>%s</style></head><body>%s%s%s</body></html>"
           % (CSS, HEAD, build_html(), FOOT))

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

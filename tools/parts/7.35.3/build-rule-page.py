"""Part 7.35.3 data for tools/build-rule-page.py. Executed into that tool's namespace by
tools/partlib.py; the tool holds the code, this file holds what is true of the Part."""

SOURCE = os.path.join(ROOT, "source-text", "rules-draft-2026-08-25-published.txt")
CITE = "Revised proposed rule 7.35.3 NMAC"
HAS_DEFS = True
DOC = "/documents/rules-draft-2026-08-25-published.pdf"
DOCDATE = "August 25, 2026"
NSECTIONS = 28

# The rule defines nothing of its own: 7.35.3.7 imports every definition from
# 7.35.2.7 NMAC, which the amendments published August 25 rewrite. The program
# rulemaking's definitions therefore live inside the producer rule's section,
# and every future Part's definitions will land there the same way. The
# section built from AMEND_SOURCE reproduces the program-side definitions on
# this page, verbatim in the amendment's own strike-and-add notation, so a
# reader of the rule is never sent to a different document for the words the
# rule runs on.
AMEND_SOURCE = os.path.join(ROOT, "source-text",
                            "rules-7.35.2-amendments-2026-08-25-published.txt")
AMEND_DOC = "/documents/rules-7.35.2-amendments-2026-08-25-published.pdf"

# The program-side terms, in the amendment's own order. Producer-side terms
# (cultivation, lots, testing) stay with the producer rule.
DEF_TERMS = [
    "Administration session", "Administrative review committee",
    "Adverse health event", "Approved location", "Certificant",
    "Certification", "Certifying clinician", "Clinician",
    "Educational program", "Electronic system", "Enrollment", "Facilitator",
    "Guide", "Healing center", "Integration session",
    "Medical psilocybin service", "Medical services", "New Mexico module",
    "Other approved location", "Practicum", "Practitioner",
    "Preparation session", "Qualified patient", "Qualifying condition",
    "Registrant of another approved location",
]

# Notes under individual definitions. Every claim is sourced.
# type: open | settled | defect | blue
DEF_NOTES = {
    "Certifying clinician": [("open", "The contested scope of the screening role",
        "The definition authorizes the certifying clinician “to diagnose or confirm a "
        "previous diagnosis of a qualifying condition,” and carries the controlled-substance "
        "number inside it. At the August 21 committee meeting the department described the role "
        "more narrowly: ensuring the medical clearance, so that the person does indeed have the "
        "diagnosis and treatment is medically appropriate, with the counseling-side judgment "
        "sitting with the treating role. The committee recommendation proposes renaming the role "
        "the medical screener and confining it to medical screening. The number requirement is "
        "analyzed on <a href='cs-number.html'>the controlled-substance number page</a>; the "
        "August 21 exchange is on <a href='record.html#e-2026-08-21'>the record</a>.")],
    "Clinician": [("defect", "A definition that does not cover the certifying clinician",
        "Both clinical roles are defined as subtypes of this term: the certifying clinician and "
        "the practitioner each &ldquo;means a clinician who&rdquo; meets their further conditions. "
        "But this definition reaches only a provider certified to provide &ldquo;medical "
        "services&rdquo;, and medical services means the three sessions, preparation, "
        "administration, and integration. The certifying clinician provides none of the three. "
        "The amendments define the broader term that would close the gap, &ldquo;medical "
        "psilocybin service&rdquo;, two entries below. The facilitator is defined as an "
        "individual, not a clinician.")],
    "Qualified patient": [("open", "The Act's word is clinician",
        "The Medical Psilocybin Act defines a qualified patient as one &ldquo;whose clinician "
        "has judged the patient to be a medically appropriate candidate for the use of medical "
        "psilocybin based on being diagnosed with a qualifying condition.&rdquo; This definition "
        "substitutes the narrower defined term, whose certifying clinician has judged, which "
        "places the statutory judgment of medical appropriateness in the one role that carries "
        "the controlled-substance number inside its definition. The Act's own definition of "
        "clinician names no license type and no controlled-substance number; the requirement is "
        "analyzed on <a href='cs-number.html'>the controlled-substance number page</a>.")],
    "Practitioner": [("blue", "Rewritten, and the rename declined",
        "The amendment strikes the adopted definition, “an individual who is a licensed "
        "healthcare professional,” for a certified clinician providing psilocybin "
        "integrative therapy and supervising facilitators. The committee recommendation proposes "
        "renaming the role the Licensed Provider; the published texts keep practitioner. The "
        "recommendation's position is on "
        "<a href='recommendation.html'>the recommendation page</a>.")],
    "Guide": [("blue", "Struck into an alias",
        "The adopted rule defined the guide as its own registered role, assisting practitioners. "
        "The amendment strikes that definition; guide survives only as the alternate name inside "
        "the facilitator definition above.")],
    "Qualifying condition": [("blue", "Where the conditions bind the curriculum",
        "End-of-life care, post-traumatic stress disorder, and substance use disorders are three "
        "of the four qualifying conditions, and none is a named topic in the didactic list at "
        "7.35.3.18 (C); the list's nearest counterpart is “Education on the qualifying "
        "conditions and appropriate treatment practices.”")],
}

# What the section says about itself before the entries.
DEFS_LEDE = (
    "This rule defines nothing of its own: 7.35.3.7 imports every definition from 7.35.2.7 "
    "NMAC, the producer rule's definitions section, which the amendments published August 25 "
    "rewrite. The program-side definitions are reproduced here verbatim from that amendment, "
    "in its own notation: <s>bracketed struck text</s> is language the amendment removes from "
    "the adopted rule, and the rest is what would stand. Every future Part of the program's "
    "rules will carry its definitions into 7.35.2.7 the same way. The full amendment, with the "
    "producer-side definitions and the changes to producer sales and transportation, is the "
    "source PDF each entry links."
)

KICKER = ('Published August 25, 2026 &middot; <b>the current proposed rule</b> &middot; '
          'rule hearing October 2, 2026')
LEDE = ("The full text of 7.35.3 NMAC as published August 25, 2026, all twenty-eight "
        "sections, with the state of each contested provision noted where it lives. This "
        "text supersedes the set-aside July 23 publication and goes to hearing on "
        "October 2, 2026; public comment continues through the hearing. The rule&rsquo;s "
        "definitions are in amendments to 7.35.2.7 NMAC published the same day. Line "
        "breaks are collapsed for reading; where the extraction stumbles, the linked PDF "
        "governs.")

# Notes placed under the section they describe. Every claim is sourced.
# type: open | settled | defect | blue
ANNOTATIONS = {
    7: [("blue", "The definitions live in the 7.35.2 amendments",
         "This rule defines nothing of its own. The definitions it runs on, certifying clinician, "
         "practitioner, facilitator, and the New Mexico module among them, are in the amendments to "
         "7.35.2.7 NMAC published August 25 alongside this text. The definitions were sent to the "
         "Training and Education Committee on July 17 with the hours; the amendments carry the "
         "department's language. The program-side definitions are reproduced, verbatim and "
         "annotated, in <a href='#defs'>the section directly below</a>; the amendments PDF is in "
         "the register on the <a href='record.html#documents'>record page</a>.")],
    9: [("settled", "Controlled-substance number, kept",
         "The requirement that a certifying clinician hold a New Mexico controlled-substance number was "
         "contested through June and July and kept by the department on July 17. It stands in this "
         "section, and the amended definition of certifying clinician in 7.35.2.7 now carries the "
         "number inside it. The full account is on the "
         "<a href='cs-number.html'>controlled-substance number page</a>.")],
    10: [("settled", "Reciprocity deadlines, settled July 9",
         "Both reciprocity waiver deadlines were extended to December 31, 2027 at the July 9 board meeting, "
         "resolved without objection. The board chair described December 31 as a legislative backstop. "
         "Source: July 9 meeting transcript.")],
    11: [("open", "The owner statement at a patient's home",
         "An other approved location may be a patient's residence, and the pathway exists in the first "
         "instance for a patient who cannot be physically transported to a healing center. Paragraph (9) of "
         "Subsection B requires proof of ownership of the property by the patient, practitioner, or "
         "facilitator, or &ldquo;a signed, written statement from the owner of such property acknowledging "
         "that the owner understands that persons will be participating in the medical psilocybin program "
         "on the premises&rdquo;. A patient who rents cannot receive treatment at home unless the landlord "
         "signs that statement, which discloses the household's program participation to a party with no "
         "role in the patient's care; Paragraph (7) of the same subsection requires a plan for maintaining "
         "patient confidentiality at the same location. The at-home pathway exists in the first instance "
         "for patients who cannot be transported to a healing center, end-of-life patients among them. "
         "Landlord approval and patient privacy were raised at the August 21 committee meeting, from "
         "the chat and read into the record by the chair, who called it a sticky subject to be "
         "discussed further; the question had been raised at an earlier end-of-life meeting. The "
         "exchange is on <a href='record.html#e-2026-08-21'>the record</a>. Public comment continues "
         "through the October 2 hearing.")],
    13: [("blue", "New in this text",
         "Two provisions appear here for the first time in the August 25 text: a certifying clinician, "
         "practitioner, or facilitator shall not consume or be under the influence of psilocybin or any "
         "other intoxicant when providing services to a patient, Subsection F, and certifying "
         "clinicians, practitioners, and facilitators must provide the department access to records on "
         "request, Subsection G.")],
    14: [("defect", "Students are not authorized here",
         "The practicum in 7.35.3.19 requires students to conduct administration sessions, and 7.35.3.20 lets "
         "students count toward staffing, but this section authorizes no student to possess or administer "
         "psilocybin. Stated in the July 25 concerns inventory, finding B1, and analyzed at "
         "<a href='deferred.html#s14'>7.35.3.14 on What a practicum change touches</a>."),
        ("defect", "A registration this rule does not create",
         "Subsection C conditions healing-center owner and employee authorization on registration with the "
         "department, and the rule creates no such registration. Finding B5, analyzed at "
         "<a href='deferred.html#new2'>the missing healing-center registration on What a "
         "practicum change touches</a>."),
        ("blue", "New in this text: chain of custody",
         "Paragraph D, new in the August 25 text, requires a practitioner, facilitator, or healing "
         "center owner or employee who obtains or transfers medical psilocybin to generate or verify a "
         "chain of custody form, and to carry identification and the form when transporting. It pairs "
         "with the amended transportation rules in 7.35.2.24, published the same day.")],
    15: [("blue", "New in this text",
         "Subsection A, new in the August 25 text, puts every educational program curriculum through "
         "department review and approval, initial applications and later modifications alike, with five "
         "stated grounds for denial.")],
    16: [("defect", "Paid evaluators are disqualified by the conflict rule",
         "The program must engage and pay the third-party evaluation team, and the section's own conflict rule "
         "disqualifies paid evaluators. Finding B3.")],
    17: [("blue", "New in this text",
         "Educational programs must collect structured student feedback within 30 calendar days of each "
         "module's completion, Subsection F, new in the August 25 text.")],
    18: [("open", "The didactic hours, doubled and still contested",
         "The board sent the didactic hours to committee by a 7-0 vote on July 17. The July 23 text set "
         "the therapy module at 30 didactic hours with 5 simulated patient hours; this text sets 65 "
         "didactic hours, at least one third in person, with 10 simulated patient hours, matching the "
         "recommendation's 80-hour total while declining its per-area minimums. The committee's "
         "recommendation, at its August 21 position, sets minimums in nine content areas; it is on the "
         "<a href='recommendation.html'>recommendation page</a>, and public comment continues through "
         "the October 2 hearing."),
        ("blue", "New in this text",
         "Eleven topics enter the required list, legal considerations, cultural competencies, "
         "traditional and ceremonial practices, equity and access, informed consent, touch and somatic "
         "awareness, and continuity of care among them, none with an hour minimum. A new waiver at "
         "Subsection H lets the department reduce the didactic hourly and topic requirements."),
        ("blue", "Drafting slip in the published PDF",
         "Paragraph (2) of Subsection C states its competency-evaluation sentence twice and carries a "
         "stray punctuation mark after &ldquo;five hours&rdquo;. Quoted as published; the PDF governs."),
        ("defect", "A module with no date it must exist",
         "Every certification pathway requires a New Mexico module created or approved by the department, and "
         "the rule sets no date by which that module must exist. Finding B2.")],
    19: [("open", "The practicum totals, published unchanged a second time",
         "The board voted 7-0 on July 17 to send the practicum hours to committee. The July 23 text "
         "carried them unchanged, and this text carries them unchanged again: 100 hours for "
         "facilitators, 120 for practitioners. The committee's recommendation, at its August 21 "
         "position, proposes a staged practicum of 102 hours for facilitators and 114 for licensed "
         "providers, the recommendation's name for the role this text calls the practitioner; the two "
         "positions can be compared on the <a href='hours.html'>working model of the hours</a>."),
        ("blue", "New in this text",
         "Three additions inside the unchanged totals: the first 20 administration-day hours are with "
         "patients the supervising practitioner determines to be low-risk, Paragraph (3) of Subsection "
         "A; same-day sessions must include patients with a diversity of the qualifying conditions, "
         "Paragraph (4); and the student must pass case presentations on two of their last four "
         "patients to complete the practicum, Subsection C."),
        ("defect", "A practicum that requires patients it cannot lawfully use",
         "Subsection A requires a minimum of 14 qualified patients at approved locations, no provision "
         "authorizes practicum with non-patients, and the only relief is a discretionary waiver with no "
         "stated standard. Finding B4. The provision is quoted, with everything else a practicum "
         "change reaches, at <a href='deferred.html#s19a'>7.35.3.19 (A) on What a practicum "
         "change touches</a>.")],
    20: [("blue", "Students in the staffing ratio, now including billing",
         "Paragraph 5 of Subsection H counts qualified students toward staffing ratios once past 50 "
         "practicum hours, which is how the department said students would participate instead of a "
         "training permit, and the August 25 text adds that the substitution includes the purpose of "
         "billing. It depends on the authorization missing from 7.35.3.14. Source: July 17 committee "
         "transcript; finding B1."),
        ("blue", "Moved here from the application sections",
         "The natural-environment requirements, two wilderness-certified individuals present and a "
         "first aid kit and AED on site when the setting is 15 minutes or more from emergency medical "
         "services, were application items in 7.35.3.11 in the July 23 text. The August 25 text makes "
         "them an operational duty during administration sessions, Subsection K.")],
}

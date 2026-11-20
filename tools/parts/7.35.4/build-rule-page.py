"""Part 7.35.4 data for tools/build-rule-page.py. Executed into that tool's namespace by
tools/partlib.py; the tool holds the code, this file holds what is true of the Part."""

SOURCE = os.path.join(ROOT, "source-text", "rules-7.35.4-proposed-2026-10-20-published.txt")
CITE = "Proposed 7.35.4 NMAC"
HAS_DEFS = False
DOC = "/documents/rules-7.35.4-proposed-2026-10-20-published.pdf"
DOCDATE = "October 20, 2026"
NSECTIONS = 20

AMEND_DOC = "/documents/rules-7.35.2-amendments-2026-10-20-published.pdf"

KICKER = ('Proposed October 20, 2026 &middot; <b>not in effect</b> &middot; rule hearing '
          'November 20, 2026')
LEDE = ("The full text of 7.35.4 NMAC, Treatment Equity Fund, as the department proposed it on "
        "October 20, 2026, all twenty sections. It is a proposed rule and is not in effect; "
        "every history note reads N, xx/xx/2026, the date left blank until adoption. Where the "
        "text departs from the recommendation the Advisory Board voted on September 11, a note "
        "sits under the section and the full comparison is on "
        "<a href='recommendation.html'>The board recommendation</a>. A note marked New from the "
        "department sits under each provision that is in neither the committee's August 18 "
        "framework nor the board's September 11 vote and was not found in the captions of the "
        "recorded committee and board meetings; the list is at "
        "<a href='recommendation.html#new'>The board recommendation</a>. A note marked Update "
        "terminology sits where a term in this Part rests on a term in 7.35.3 or 7.35.2.7 that the "
        "department's November 9 response on 7.35.3 proposes to change, or where this Part uses two "
        "terms for one thing or a term it never establishes. "
        "Line breaks are collapsed "
        "for reading; where the extraction stumbles, the linked PDF governs.")

_A = (f"<a href='{AMEND_DOC}' target='_blank' rel='noopener' data-cite='Proposed amendment to "
      f"7.35.2.7 NMAC, October 20, 2026'>proposed amendment to 7.35.2.7 published the same day</a>")

# Notes placed under the section they describe. Every claim is sourced.
# type: open | settled | defect | blue
ANNOTATIONS = {
    7: [("blue", "The definitions are imported",
         f"This Part defines nothing of its own. The {_A} would add eleven defined terms to "
         "7.35.2.7 for it: allowable amount, claim, claimant, covered treatment, director, federal "
         "poverty guidelines, fund, household, other payer, program manager, and SHARE "
         "(amendment pp. 1 to 5). Covered treatment is defined as \"a service, psilocybin product, "
         "or travel expense eligible for payment under 7.35.4 NMAC\" (amendment p. 2). Until "
         "adopted, 7.35.2.7 stands as published June 23, 2026, which carries none of these terms.")],
    10: [("open", "Medicaid named as a payer to pursue first",
          "Subsection B requires an attestation that the claimant pursued reimbursement from "
          "third parties that \"may include private insurance, Medicaid, Medicare\" before "
          "billing the fund. At the September 11 board meeting the HCA delegate said that "
          "\"specifically saying you have to bill Medicaid first might get you into some legal "
          "trouble\", and the department answered that its attorneys were working on the "
          "language. The board voted the intent, not the wording. "
          "<a href='recommendation.html#vs-lastpayer'>The comparison</a>.")],
    14: [("open", "Two sessions per later administration; the board voted three",
          "Paragraphs (2) and (3) of Subsection A allow \"a combined total of two preparatory and "
          "integrative sessions\" with the second and third administration sessions. The motion "
          "the Advisory Board passed 7-0 on September 11 was \"to have a vote on the three\", "
          "three sessions per additional administration; two was the committee's August 18 "
          "figure. <a href='recommendation.html#vs-later'>The comparison</a>."),
         ("open", "No diagnostic evaluation, and no medication, in the list",
          "Subsection A lists administration sessions and preparatory and integrative sessions; "
          "Subsections B and C cover travel. The diagnostic evaluation and the cost of "
          "medication, both in the recommendation the committee and the board voted, are not "
          "named here. A psilocybin product is reached elsewhere: 7.35.4.11 (C) directs a fee "
          "schedule for it and 7.35.4.12 (B)(7) states how it is claimed. "
          "<a href='recommendation.html#vs-eval'>The comparison</a>.")],
    20: [("blue", "No review where the money has run out",
          "Subsection H excludes from administrative review any adverse payment determination "
          "\"based solely on the lack or unavailability of funding\". 7.35.4.17 (E) states that "
          "such a suspension is not a finding that anyone violated the rule.")],
}

# New from the department: in the proposed text, in neither recommendation, and not found
# in the captions of the 23 recorded committee and board meetings, December 5, 2025 to
# September 14, 2026, searched for its terms on October 22, 2026.
def _dept(what):
    return ("dept", "Not in the recommendation or the recorded meetings", what)

for _n, _what in [
    (8, "Subsection D (5): eligibility ends 12 months after funding approval. The committee "
        "and the board set no duration."),
    (9, "Subsection B (3): the three forms of residency proof, among them a letter of "
        "accommodation from a licensed medical or behavioral health provider, and a tribal "
        "identification card with a utility bill. The recommendation required residency and "
        "named no proof."),
    (10, "Subsection E: when another payer pays after the fund has, the claimant notifies the "
         "department within 30 calendar days and returns the overpayment."),
    (11, "Subsection A (1) and (3), and Subsection B: payment is capped at the claimant's usual "
         "and customary charge as well as the rate, the rate may be Medicaid's or Medicare's, and "
         "where neither applies the department may use the most analogous one. The recommendation "
         "capped reimbursement at Medicaid rates."),
    (12, "Subsection D: a claim is due within 180 calendar days after the date of service. "
         "Claims through the department's system and SHARE were discussed; the deadline was not."),
    (15, "Subsection A: claim records are kept at least seven years after payment or the final "
         "resolution of an audit, investigation, or recovery."),
    (16, "Subsection D: requested records are due within 10 business days. Audit procedures "
         "were recommended; the deadline and the specific powers in Subsection C were not."),
    (18, "The whole section: what counts as an overpayment, repayment within 30 calendar days, "
         "and recovery by offset against future payments."),
    (20, "The whole section: administrative review on written request within 30 calendar days, "
         "a review of documents and not a hearing, no stay of the action under review, and "
         "Subsection H, no review of a determination based solely on the lack of funding."),
]:
    ANNOTATIONS.setdefault(_n, []).append(_dept(_what))

# Update terminology: where this Part's words rest on terms in 7.35.3 or 7.35.2.7 that the department's
# November 9, 2026 response on 7.35.3 proposes to change, or where one thing carries two names.
# Facts and sources only; no proposed language. Added November 20, 2026.
_R = ("<a href='/documents/rules-7.35.3-response-to-comments-2026-11-09.pdf' target='_blank' "
      "rel='noopener' data-cite='Department of Health response to public comments on 7.35.3 NMAC, "
      "November 9, 2026'>November 9 response on 7.35.3 NMAC</a>")
_P3 = ("<a href='/documents/rules-draft-2026-08-25-published.pdf#page=17' target='_blank' "
       "rel='noopener' data-cite='Proposed 7.35.3 NMAC, August 25, 2026, page 17'>7.35.3 text "
       "published August 25</a>")

def _w(title, text):
    return ("clarify", title, text)

for _n, _note in [
    (2, _w("Roles named in the scope",
           f"The scope names certifying clinicians among those who submit claims. The department's "
           f"{_R} proposes to remove the certifying clinician from 7.35.3 (Response, pp. 2 to 3); "
           "it does not address 7.35.4. Facilitators and other approved locations are not named "
           "in the scope, and 7.35.4.14 (B) names an other approved location as a place of "
           "treatment.")),
    (7, _w("Two imported definitions rest on the certifying clinician",
           f"The {_A} defines a claimant as \"an authorized certifying clinician, practitioner, "
           "healing center, producer, or other vendor\" (amendment p. 1), and a qualified patient "
           "as a patient \"whose certifying clinician has judged the patient to be a medically "
           "appropriate candidate\" (amendment p. 4). This Part uses qualified patient for "
           f"eligibility throughout. The {_R} proposes that a practitioner certify the patient in "
           "place of a certifying clinician (Response, pp. 2 to 3) and does not address the "
           "7.35.2.7 definitions.")),
    (8, _w("Enrollment, and two names for the date of approval",
           "Subsection A (1) requires current enrollment in the program, and Subsection D (1) ends "
           f"fund eligibility when enrollment ends. The {_R} proposes that 7.35.3 state that joining "
           "the program is an enrollment rather than an application (Response, p. 1). Eligibility "
           "for the fund is still applied for, under 7.35.4.9. Subsection D dates eligibility from "
           "\"the date of approval\", and paragraph (5) from \"the date of funding approval\".")),
    (9, _w("The patient identifier, and the word applicant",
           "Subsection B (1) asks for the patient's \"medical psilocybin program identification "
           "number\", and 7.35.4.12 (B)(3) for the patient's \"program identification number\". "
           f"The {_P3} sets enrollment at 7.35.3.8 and issues no patient identification number; its "
           "one such term is \"registry identification number\", at 7.35.3.24 (C) (p. 17). "
           "Subsections A and C call the patient an applicant; the response proposes replacing "
           "applicant with patient in 7.35.3 (Response, p. 1).")),
    (10, _w("Two names for a claim",
            "The heading and Subsections A and B speak of a request for reimbursement. Subsection "
            "C and the rest of this Part speak of a claim, the defined term: \"an electronic "
            f"request for payment from the fund\" ({_A}, p. 1).")),
    (12, _w("Claimants, and the roles that are not named",
            "Subsection A names certifying clinicians as claimants; see the note at 7.35.4.2. Under "
            f"the {_R}, a practitioner refers a patient to a medical provider when the screening "
            "tool indicates risk or the patient has not seen a medical provider in 12 months "
            "(Response, pp. 2 to 3). That medical provider is not among the claimants. Facilitators "
            "are not named; Subsection E lets the same session be billed separately \"for distinct "
            "services or roles authorized by the department\".")),
    (12, _w("Words that differ from the defined terms",
            "Subsection C requires \"all enrollment documents required for payment through "
            "SHARE\"; the proposed 7.35.2.7 defines enrollment as \"enrollment as a qualified "
            "patient\" (amendment p. 2). Subsection E says \"administration-day session\"; the "
            "defined term is administration session (amendment p. 1).")),
    (13, _w("Authorization",
            "Subsection C records each \"authorization\". No section of this Part establishes an "
            "authorization step. The word also appears at 7.35.4.14 (B) and (C), 7.35.4.15 (B), "
            "and 7.35.4.16 (A) and (B).")),
    (14, _w("Who submits a travel claim",
            "Subsection B makes a qualified patient \"eligible for reimbursement for travel "
            f"expenses\". A patient is not within the definition of claimant ({_A}, p. 1), and a "
            "claim carries a tax identification number, a SHARE vendor identification number, and "
            "a department certification or permit number (7.35.4.12 (B)(1) and (2)). No section "
            "states who submits a travel claim or to whom it is paid.")),
    (14, _w("Session names, and prior authorization",
            "Subsection A says \"preparatory and integrative sessions\"; the defined terms are "
            "preparation session and integration session (amendment pp. 3 to 4). Subsection C (8) "
            "requires \"any prior authorization required by the department\"; no section "
            "establishes prior authorization.")),
    (15, _w("Two retention periods",
            "Subsection A keeps claim records at least seven years, and Subsection B includes "
            f"clinical documentation among them. The {_R} proposes that healing centers, "
            "practitioners, and facilitators keep treatment records at least five years under "
            "7.35.3 (Response, p. 10).")),
    (20, _w("Burden of proof",
            "This section does not state who bears the burden in a review. For 7.35.3.27 (L), the "
            f"{_R} proposes that the appellant bear it on denial of an initial application, and "
            "the department on suspension or revocation of an existing certificate (Response, "
            "p. 10).")),
]:
    ANNOTATIONS.setdefault(_n, []).append(_note)

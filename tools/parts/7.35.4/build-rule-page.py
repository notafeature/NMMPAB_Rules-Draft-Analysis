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
        "<a href='recommendation.html'>The board recommendation</a>. Line breaks are collapsed "
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

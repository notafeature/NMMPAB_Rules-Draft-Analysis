"""Part 7.35.2 data for tools/build-rule-page.py. Executed into that tool's namespace by
tools/partlib.py; the tool holds the code, this file holds what is true of the Part."""

SOURCE = os.path.join(ROOT, "source-text", "rules-7.35.2-adopted-2026-06-23-published.txt")
CITE = "7.35.2 NMAC as adopted"
HAS_DEFS = False
DOC = "/documents/rules-7.35.2-adopted-2026-06-23-published.pdf"
DOCDATE = "June 23, 2026"
NSECTIONS = 27
ABOUT_HREF = "/7.35.3/about.html"

AMEND_DOC = "/documents/rules-7.35.2-amendments-2026-08-25-published.pdf"

KICKER = ('Adopted and in effect since June 23, 2026 &middot; <b>amendments to three sections '
          'proposed August 25</b> &middot; rule hearing October 2, 2026')
LEDE = ("The full text of 7.35.2 NMAC as published in the New Mexico Register on June 23, 2026, "
        "all twenty-seven sections, in effect from that day. The three sections the department "
        "proposes to amend are noted where they sit; nothing in this text is amended until the "
        "department adopts the amendments after the October 2 hearing. Line breaks are collapsed "
        "for reading, and the four testing tables read as run-on text; where the extraction "
        "stumbles, the linked PDF governs.")

# Notes placed under the section they describe. Every claim is sourced.
# type: open | settled | defect | blue
_A = (f"<a href='{AMEND_DOC}' target='_blank' rel='noopener' data-cite='Proposed amendments to "
      f"7.35.2.7, .10, and .24 NMAC, August 25, 2026'>proposed amendments published August 25</a>")
ANNOTATIONS = {
    7: [("open", "Amendment proposed: twenty-one defined terms added",
         f"The {_A} would add twenty-one defined terms to this section, among them administrative "
         "review committee, adverse health event, certificant, certifying clinician, educational "
         "program, facilitator, healing center, integration session, New Mexico module, practicum, "
         "and preparation session; would strike the standalone Guide definition so that guide "
         "survives only as an alias inside the facilitator definition; would rewrite Practitioner "
         "as a clinician certified by the department to provide psilocybin integrative therapy and "
         "supervise facilitators; and would correct Satchet to sachet (amendments pp. 1 to 4). The "
         "proposed rule 7.35.3 NMAC defines nothing of its own and imports every definition from "
         "this section, so these terms are the vocabulary of the program rulemaking as well; the "
         "program-side definitions are reproduced and annotated on "
         "<a href='/7.35.3/rule.html#defs'>the 7.35.3 rule page</a>. The hearing is October 2.")],
    10: [("open", "Amendment proposed: sales to healing centers",
          f"The {_A} would restructure this section into a lead-in and eight numbered items and "
          "change one of them: Subsection G, which permits sale only to other producers and to "
          "practitioners, would become item (7) and permit sale \"to other producers, healing "
          "centers, and practitioners\" (amendments pp. 4 to 5). Healing centers are defined in the "
          "same amendments and assumed as buyers by 7.35.3.14 of the proposed program rule. The "
          "hearing is October 2.")],
    24: [("open", "Amendment proposed: who may transport, who verifies",
          f"The {_A} would open transport beyond producer permittees: Paragraph (1) of Subsection A "
          "would read \"persons holding a permit or designated employees, or contractors of a "
          "permittee, certified practitioner, or certified healing center\", where the adopted text "
          "ends at \"certified practitioner\". Verification of the chain of custody form would move "
          "from \"the permittee receiving the psilocybin shipment\" to \"the person receiving\" it, "
          "and the rejection prohibition from \"Permittees\" to \"Persons\" (amendments pp. 5 to 6). "
          "Paired with 7.35.3.14 (D) of the proposed program rule, this is the chain of custody for "
          "the treatment side of the program. The hearing is October 2.")],
    19: [("blue", "Start dates are the department's to set",
          "Subsection A lets the department delay or suspend the sample collection, testing, and "
          "labeling requirements in whole or in part, considering whether a laboratory has "
          "validated a method for each test and the laboratories' capacity to collect and "
          "transport samples. No start date is stated in the rule.")],
}

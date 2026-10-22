"""Part 7.35.2 data for tools/sync-record.py. Executed into that tool's namespace by
tools/partlib.py; the tool holds the code, this file holds what is true of the Part."""

# The register. Newest first. `file` is None where the site cites a document it
# does not publish. `status` is one of current, superseded, record; a superseded
# document names its successor. `chain` marks the successive texts of the rule.
DOCUMENTS = [
    {
        "slug": "rules-7.35.3-exhibit-binder-2026-10-01",
        "name": "The exhibit binder for the October 2 hearing",
        "file": "documents/rules-7.35.3-exhibit-binder-2026-10-01.pdf",
        "cite": "Department of Health exhibits for the October 2, 2026 hearing on 7.35.3 NMAC "
                "and the amendments to 7.35.2 NMAC, published October 1, 2026",
        "date": "2026-10-01",
        "event": "e-2026-10-01",
        "what": "The department's final exhibit binder for the hearing, with the proposed texts "
                "and the written public comments",
        "status": "record",
        "notes": "153 pages. The department's exhibits for the October 2 hearing: Exhibit 1 the proposed 7.35.3 NMAC and Exhibit 2 the proposed amendments to 7.35.2 NMAC, each identical in its words to the August 25 publication; the notice; the affidavits of publication; the hearing officer's appointment; and, as Exhibit 8, 51 written public comments, 8.A through 8.YY. It lists no anticipated revisions",
    },
    {
        "slug": "rules-7.35.2-amendments-2026-10-20-published",
        "name": "Proposed amendment to 7.35.2.7 NMAC, for the equity fund",
        "file": "documents/rules-7.35.2-amendments-2026-10-20-published.pdf",
        "cite": "Proposed amendment to 7.35.2.7 NMAC, October 20, 2026",
        "date": "2026-10-20",
        "event": "e-2026-10-20",
        "what": "Strike-and-add text for the definitions section, carrying the terms of the "
                "August 25 amendment and adding eleven for the proposed 7.35.4 NMAC, Treatment "
                "Equity Fund. Proposed, not adopted; heard November 20",
        "status": "record",
        "notes": "5 pages. The added terms are allowable amount, claim, claimant, covered "
                 "treatment, director, federal poverty guidelines, fund, household, other payer, "
                 "program manager, and SHARE. Published with the proposed 7.35.4 NMAC, which has "
                 "<a href=\"/7.35.4/index.html\">its own pages</a>",
    },
    {
        "slug": "rules-7.35.2-amendments-2026-08-25-published",
        "name": "Proposed amendments to 7.35.2 NMAC",
        "file": "documents/rules-7.35.2-amendments-2026-08-25-published.pdf",
        "cite": "Proposed amendments to 7.35.2.7, .10, and .24 NMAC, August 25, 2026",
        "date": "2026-08-25",
        "event": "e-2026-08-25",
        "what": "Proposed amendments to three sections of the adopted rule: the definitions, "
                "producer sales, and the transportation of psilocybin. Proposed, not adopted; "
                "the October 2 hearing was set to take them up",
        "status": "record",
        "notes": "6 pages. Strike-and-add text for 7.35.2.7, 7.35.2.10, and 7.35.2.24; each "
                 "is noted at its section on <a href=\"rule.html#s7\">The adopted rule</a>. The "
                 "header names Sections 7, 10, and 22; the body amends 7, 10, and 24",
    },
    {
        "slug": "hearing-notice-2026-08-25",
        "name": "Notice of the October 2 rule hearing",
        "file": "documents/hearing-notice-2026-08-25.pdf",
        "cite": "The notice of the October 2, 2026 rule hearing",
        "date": "2026-08-25",
        "event": "e-2026-08-25",
        "what": "The notice fixing the rule hearing on the proposed 7.35.3 NMAC and on the "
                "amendments to 7.35.2.7, 7.35.2.10, and 7.35.2.24 for October 2, 2026",
        "status": "record",
        "notes": "2 pages, published in the New Mexico Register, Volume XXXVII, Issue 16",
    },
    {
        "slug": "rules-7.35.2-adopted-2026-06-23-published",
        "name": "The adopted rule, 7.35.2 NMAC",
        "file": "documents/rules-7.35.2-adopted-2026-06-23-published.pdf",
        "cite": "7.35.2 NMAC as adopted, June 23, 2026, 19 pages",
        "date": "2026-06-23",
        "event": "e-2026-06-23",
        "what": "Producer and Laboratory Requirements as adopted and published in the New "
                "Mexico Register, Volume XXXVII, Issue 12, in effect from June 23, 2026; the "
                "operative text, and the text this site cites for section numbers and rule text",
        "status": "current",
        "chain": True,
        "superseded_by": None,
        "notes": "19 pages. Sections 7.35.2.1 through .27, typeset on this site at "
                 "<a href=\"rule.html\">The adopted rule</a>; every section carries the history "
                 "note N, 6/23/2026",
    },
    {
        "slug": "rules-7.35.2-hearing-officer-report-2026-05-26",
        "name": "Report of the hearing officer",
        "file": "documents/rules-7.35.2-hearing-officer-report-2026-05-26.pdf",
        "cite": "Report of the hearing officer on the proposed adoption of 7.35.2 NMAC, May 26, 2026",
        "date": "2026-05-26",
        "event": "e-2026-05-26",
        "what": "The hearing officer's account of the April 24 hearing, the public comment, "
                "the department's anticipated revisions and written response, and the "
                "recommendation that the secretary adopt the rule with those amendments",
        "status": "record",
        "notes": "38 pages, signed by Craig T. Erickson, hearing officer. Records the revisions "
                 "announced at the hearing, among them the total yeast and molds action level "
                 "raised from 20 to 1,000 CFU, the water content limit stated as less than 10 "
                 "percent, an e-mail courtesy copy of disciplinary notices, and three pesticide "
                 "action levels corrected. Posted on the department's rules page",
    },
    {
        "slug": "rules-7.35.2-response-to-comments-2026-05-13",
        "name": "The department's response to public comments",
        "file": "documents/rules-7.35.2-response-to-comments-2026-05-13.pdf",
        "cite": "Department of Health response to public comments on 7.35.2 NMAC, May 13, 2026",
        "date": "2026-05-13",
        "event": "e-2026-05-13",
        "what": "The office of general counsel's written responses to the substantive proposals "
                "in the public comments, stating which the department proposed to adopt and "
                "which it declined, with reasons",
        "status": "record",
        "notes": "9 pages, addressed to the hearing officer. Adopted proposals include a "
                 "definition of certificate of analysis and the 10 percent water content limit. "
                 "Posted on the department's rules page",
    },
    {
        "slug": "rules-7.35.2-hearing-package-2026-04-24",
        "name": "The hearing exhibits, with the proposed rule",
        "file": "documents/rules-7.35.2-hearing-package-2026-04-24.pdf",
        "cite": "Department of Health exhibits for the April 24, 2026 hearing on 7.35.2 NMAC",
        "date": "2026-04-24",
        "event": "e-2026-04-24",
        "what": "The department's nine exhibits for the hearing: the chapter approval, the "
                "proposed new rule as noticed, the notice, the affidavits of publication, the "
                "hearing officer's appointment, the list of anticipated revisions, and the "
                "public comments received",
        "status": "superseded",
        "superseded_by": "rules-7.35.2-adopted-2026-06-23-published",
        "chain": True,
        "notes": "93 pages. Exhibit 2 is the proposed text; Exhibit 8 the revisions the department "
                 "announced at the hearing; Exhibit 9 the written public comments. Posted on the "
                 "department's rules page",
    },
    {
        "slug": "hearing-notice-7.35.2-2026-03-24",
        "name": "Notice of the April 24 rule hearing",
        "file": "documents/hearing-notice-7.35.2-2026-03-24.pdf",
        "cite": "The notice of the April 24, 2026 rule hearing on 7.35.2 NMAC, March 24, 2026",
        "date": "2026-03-24",
        "event": "e-2026-03-24",
        "what": "The notice of proposed rulemaking, setting the hearing on the proposed 7.35.2 "
                "NMAC for April 24, 2026 and listing what each section of the proposed rule does",
        "status": "record",
        "notes": "2 pages, published in the New Mexico Register, Volume XXXVII, Issue 6, page 348",
    },
    {
        "slug": "medical-psilocybin-act-sb219-2025",
        "name": "The Medical Psilocybin Act",
        "file": "documents/medical-psilocybin-act-sb219-2025.pdf",
        "cite": "The Medical Psilocybin Act, Sections 26-2D-1 through 26-2D-11 NMSA 1978, as enacted in 2025",
        "date": "2025-06-20",
        "event": "e-2025-06-20",
        "what": "The enabling statute, Laws 2025, Chapter 73, compiled as Sections 26-2D-1 "
                "through 26-2D-11 NMSA 1978. Section 26-2D-7 is the authority the rule cites; it "
                "directs the department to establish training, safety protocols, and best "
                "practices for producers",
        "status": "record",
        "notes": "18 pages, the enrolled bill. The producer is defined at Section 3 of the bill, "
                 "compiled as 26-2D-3",
    },
]


# The gaps register. Every row names the event it belongs to, and every event it
# names carries the reciprocal absence line.
GAPS = [
    {
        "id": "gap-hearing-2026-10-02",
        "name": "The record of the October 2 hearing",
        "means": "No recording, transcript, or hearing officer's report of the October 2 hearing "
                 "is posted, and no response to the written comments. What was said at the "
                 "hearing, and whether the department announced revisions there, is not held. "
                 "The exhibit binder published October 1 is the last department document on "
                 "this rulemaking",
        "at_event": "No recording, transcript, or hearing officer's report of the hearing is "
                    "held on this site.",
        "events": ["e-2026-10-02"],
    },
    {
        "id": "gap-committee",
        "name": "Propagation Committee agendas, minutes, and recordings",
        "means": "The committee's nine meetings from January 9 to April 15, 2026 shaped the "
                 "recommendation the proposed rule rests on. The department posts an agenda, "
                 "minutes, and a recording for each on its "
                 "<a href=\"https://www.nmhealth.org/about/mcpp/mpp/mpab/mr/\" target=\"_blank\" "
                 "rel=\"noopener\">meeting records page</a>; none is copied here yet, and nothing "
                 "on this site quotes them",
        "at_event": "The agenda, minutes, and recording of this meeting are posted by the "
                    "department and not held on this site.",
        "events": ["e-2026-04-15", "e-2026-03-18", "e-2026-03-11", "e-2026-02-18",
                   "e-2026-02-11", "e-2026-02-04", "e-2026-01-30", "e-2026-01-21",
                   "e-2026-01-09"],
    },
    {
        "id": "gap-hearing-record",
        "name": "The April 24 hearing recording or transcript",
        "means": "The hearing officer's report is the account of the hearing this site holds; "
                 "the recording the report says was made on Microsoft Teams is not held, and "
                 "the department's meeting records page posts a recording of the board meeting "
                 "of the same day, not of the hearing",
        "at_event": "No recording or transcript of the hearing is held on this site; the "
                    "hearing officer's report of May 26 is the account held.",
        "events": ["e-2026-04-24"],
    },
]


# The chain. Newest first. Each event: id (e-YYYY-MM-DD), date, kind (meeting,
# document, filing, scheduled, anticipated), what, and optionally changed
# (state transitions linking the page that owns each), attached (register
# slugs), absent (gap ids), and deeper (the fuller account).
EVENTS = [
    {
        "id": "e-2026-10-20",
        "date": "2026-10-20",
        "kind": "document",
        "what": "<b>The department published a further proposed amendment to 7.35.2.7 NMAC</b>, "
                "with the proposed 7.35.4 NMAC, Treatment Equity Fund, which imports its "
                "definitions from this section, and fixed a rule hearing on both for November "
                "20, 2026. The adopted text stands unamended until the department adopts an "
                "amendment.",
        "changed": [
            ("<b>Definitions.</b> Eleven terms for the equity fund would be added to 7.35.2.7.",
             "rule.html#s7", "7.35.2.7"),
        ],
        "attached": ["rules-7.35.2-amendments-2026-10-20-published"],
        "deeper": [("/7.35.4/index.html", "The proposed 7.35.4 NMAC")],
    },
    {
        "id": "e-2026-10-02",
        "date": "2026-10-02",
        "kind": "meeting",
        "what": "<b>The rule hearing on the proposed amendments to 7.35.2 NMAC and on the "
                "proposed 7.35.3 NMAC, 9:00 AM, Harold Runnels Building auditorium, Santa Fe</b>, "
                "in person, by video conference, and by telephone. Fixed by the <a href=\"#doc-hearing-notice-2026-08-25\">notice published "
                "August 25</a>; written comment was due by the close of the hearing. No recording, transcript, hearing officer's report, or response to comments has been posted, and no adopted text appears in the New Mexico Register through Volume XXXVII, Issue 20, October 20, 2026.",
        "absent": ["gap-hearing-2026-10-02"],
    },
    {
        "id": "e-2026-10-01",
        "date": "2026-10-01",
        "kind": "filing",
        "what": "<b>The department posted its exhibit binder for the October 2 hearing</b>: the "
                "proposed 7.35.3 NMAC and the proposed amendments to 7.35.2 NMAC as exhibited, "
                "each identical in its words to the August 25 publication, and 51 written "
                "public comments. The binder lists no anticipated revisions.",
        "attached": ["rules-7.35.3-exhibit-binder-2026-10-01"],
    },
    {
        "id": "e-2026-08-25",
        "date": "2026-08-25",
        "kind": "document",
        "what": "<b>The department published proposed amendments to 7.35.2.7, 7.35.2.10, and "
                "7.35.2.24 NMAC</b>, together with the revised proposed rule for 7.35.3 NMAC and "
                "the notice of the October 2 hearing on both. The adopted rule stands unamended "
                "until the department adopts the amendments after the hearing.",
        "changed": [
            ("<b>Definitions.</b> Twenty-one defined terms would be added to 7.35.2.7, the "
             "standalone Guide definition struck, Practitioner rewritten, and Satchet corrected "
             "to sachet.", "rule.html#s7", "7.35.2.7"),
            ("<b>Producer sales.</b> Producers would be permitted to sell to healing centers as "
             "well as to other producers and practitioners.", "rule.html#s10", "7.35.2.10"),
            ("<b>Transportation.</b> Designated employees or contractors of a certified healing "
             "center could transport psilocybin, and the person receiving a shipment would "
             "verify the chain of custody form.", "rule.html#s24", "7.35.2.24"),
        ],
        "attached": ["rules-7.35.2-amendments-2026-08-25-published", "hearing-notice-2026-08-25"],
    },
    {
        "id": "e-2026-06-23",
        "date": "2026-06-23",
        "kind": "document",
        "what": "<b>7.35.2 NMAC was adopted and took effect</b>, published in the New Mexico "
                "Register, Volume XXXVII, Issue 12. Twenty-seven sections, each carrying the "
                "history note N, 6/23/2026.",
        "changed": [
            ("<b>From the proposed text.</b> Per the hearing officer's report, the adopted text "
             "carries the revisions the department announced at the hearing and in its May 13 "
             "response: among them a certificate of analysis definition, the water content "
             "limit of less than 10 percent, the total yeast and molds action level raised "
             "from 20 to 1,000 CFU, three pesticide action levels corrected, and an e-mail "
             "courtesy copy of disciplinary notices.", "rule.html", "The adopted rule"),
        ],
        "attached": ["rules-7.35.2-adopted-2026-06-23-published"],
        "deeper": [("producers.html", "What the rule requires of a producer"),
                   ("laboratories.html", "What the rule requires of a testing laboratory")],
    },
    {
        "id": "e-2026-05-26",
        "date": "2026-05-26",
        "kind": "filing",
        "what": "<b>The hearing officer reported to the secretary</b>, recommending adoption of "
                "the proposed rule as set out in the hearing exhibits, with the amendments in "
                "the department's list of anticipated revisions and in its May 13 written "
                "response to public comments.",
        "attached": ["rules-7.35.2-hearing-officer-report-2026-05-26"],
    },
    {
        "id": "e-2026-05-13",
        "date": "2026-05-13",
        "kind": "filing",
        "what": "<b>The department's office of general counsel responded in writing to the "
                "substantive proposals in the public comments</b>, addressed to the hearing "
                "officer, stating for each whether the department proposed to adopt it.",
        "attached": ["rules-7.35.2-response-to-comments-2026-05-13"],
    },
    {
        "id": "e-2026-04-24",
        "date": "2026-04-24",
        "kind": "meeting",
        "what": "<b>The rule hearing on the proposed 7.35.2 NMAC</b>, 9:02 AM, in person at the "
                "Harold Runnels Building and by Microsoft Teams and telephone, before hearing "
                "officer Craig T. Erickson. The department introduced nine exhibits and a list "
                "of anticipated revisions; public comment was taken section by section and in "
                "writing through the close of business that day. Source: the hearing officer's "
                "report.",
        "attached": ["rules-7.35.2-hearing-package-2026-04-24"],
        "absent": ["gap-hearing-record"],
    },
    {
        "id": "e-2026-04-15",
        "date": "2026-04-15",
        "kind": "meeting",
        "what": "<b>Propagation Committee meeting.</b> Minutes and a recording are posted by the "
                "department.",
        "absent": ["gap-committee"],
    },
    {
        "id": "e-2026-03-24",
        "date": "2026-03-24",
        "kind": "document",
        "what": "<b>The department noticed the proposed rule</b> in the New Mexico Register, "
                "Volume XXXVII, Issue 6, setting the hearing for April 24, 2026 and listing what "
                "each section of the proposed 7.35.2 NMAC would do.",
        "attached": ["hearing-notice-7.35.2-2026-03-24"],
    },
    {
        "id": "e-2026-03-18",
        "date": "2026-03-18",
        "kind": "meeting",
        "what": "<b>Propagation Committee meeting.</b> Minutes and a recording are posted by the "
                "department, with a document titled Disciplinary Action and Appeal Process.",
        "absent": ["gap-committee"],
    },
    {
        "id": "e-2026-03-11",
        "date": "2026-03-11",
        "kind": "meeting",
        "what": "<b>Propagation Committee meeting.</b> An agenda, minutes, and a recording are "
                "posted by the department.",
        "absent": ["gap-committee"],
    },
    {
        "id": "e-2026-02-18",
        "date": "2026-02-18",
        "kind": "meeting",
        "what": "<b>Propagation Committee meeting.</b> An agenda, minutes, and a recording are "
                "posted by the department.",
        "absent": ["gap-committee"],
    },
    {
        "id": "e-2026-02-11",
        "date": "2026-02-11",
        "kind": "meeting",
        "what": "<b>Propagation Committee meeting.</b> An agenda, minutes, and a recording are "
                "posted by the department.",
        "absent": ["gap-committee"],
    },
    {
        "id": "e-2026-02-04",
        "date": "2026-02-04",
        "kind": "meeting",
        "what": "<b>Propagation Committee meeting.</b> An agenda, minutes, and a recording are "
                "posted by the department.",
        "absent": ["gap-committee"],
    },
    {
        "id": "e-2026-01-30",
        "date": "2026-01-30",
        "kind": "meeting",
        "what": "<b>Propagation Committee meeting.</b> An agenda, minutes, and a recording are "
                "posted by the department.",
        "absent": ["gap-committee"],
    },
    {
        "id": "e-2026-01-21",
        "date": "2026-01-21",
        "kind": "meeting",
        "what": "<b>Propagation Committee meeting.</b> An agenda, minutes, and a recording are "
                "posted by the department.",
        "absent": ["gap-committee"],
    },
    {
        "id": "e-2026-01-09",
        "date": "2026-01-09",
        "kind": "meeting",
        "what": "<b>Propagation Committee meeting, the first.</b> An agenda, minutes, the "
                "committee's bylaws, and a recording are posted by the department.",
        "absent": ["gap-committee"],
    },
    {
        "id": "e-2025-06-20",
        "date": "2025-06-20",
        "kind": "document",
        "what": "<b>The Medical Psilocybin Act took effect</b>, ninety days after the 2025 "
                "regular session adjourned, having passed as Senate Bill 219 and been enacted as "
                "Laws 2025, Chapter 73. It creates the program, defines the producer, and at "
                "Section 26-2D-7 directs the department to establish training, safety protocols, "
                "and best practices for producers, the authority 7.35.2.3 cites.",
        "attached": ["medical-psilocybin-act-sb219-2025"],
    },
]

CHAIN_NOTE = (
    "Every meeting, publication, filing, and scheduled date is one event with its own address, "
    "so another page can cite the day rather than restate it. The Propagation Committee's "
    "meetings are listed by date from the department's meeting records page; their content is "
    "not held here."
)
REGISTER_NOTE = (
    "Every document this site holds for this Part, what it is, when it landed, and whether it "
    "is current. The date in each row opens the event the document belongs to."
)
GAPS_NOTE = (
    "Named here so the gaps are visible rather than silent, each beside the event it belongs "
    "to."
)

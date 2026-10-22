"""Part 7.35.4 data for tools/sync-record.py. Executed into that tool's namespace by
tools/partlib.py; the tool holds the code, this file holds what is true of the Part."""


def _yt(video, hms, label=None):
    """A link to a department recording at a moment, labeled with the time."""
    h, m, s = (int(x) for x in hms.split(":"))
    return (f'<a href="https://www.youtube.com/watch?v={video}&amp;t={h * 3600 + m * 60 + s}s" '
            f'target="_blank" rel="noopener">{label or hms}</a>')


# The department's recordings this Part cites, by meeting. Captions are
# YouTube's automatic captions and carry no speaker labels.
REC_0721 = "EwlEKGsq11E"
REC_0818 = "BkJgUrcFk50"
REC_0911 = "HYyUImvtYGQ"

# The register. Newest first. `file` is None where the site cites a document it
# does not publish. `status` is one of current, superseded, record; a superseded
# document names its successor. `chain` marks the successive texts of the rule.
DOCUMENTS = [
    {
        "slug": "rules-7.35.4-proposed-2026-10-20-published",
        "name": "The proposed rule, 7.35.4 NMAC",
        "file": "documents/rules-7.35.4-proposed-2026-10-20-published.pdf",
        "cite": "Proposed 7.35.4 NMAC, Treatment Equity Fund, October 20, 2026, 7 pages",
        "date": "2026-10-20",
        "event": "e-2026-10-20",
        "what": "Treatment Equity Fund as proposed by the department: eligibility, the "
                "application, reimbursement and claims, allowable expenses, records, audits, "
                "denial and suspension, overpayments, monitoring, and administrative review. "
                "Proposed, not adopted; the text this site cites for section numbers and rule text",
        "status": "current",
        "chain": True,
        "superseded_by": None,
        "notes": "7 pages. Sections 7.35.4.1 through .20, typeset on this site at "
                 "<a href=\"rule.html\">The proposed rule</a>; every history note reads N, "
                 "xx/xx/2026",
    },
    {
        "slug": "rules-7.35.2-amendments-2026-10-20-published",
        "name": "Proposed amendment to 7.35.2.7 NMAC, the definitions",
        "file": "documents/rules-7.35.2-amendments-2026-10-20-published.pdf",
        "cite": "Proposed amendment to 7.35.2.7 NMAC, October 20, 2026",
        "date": "2026-10-20",
        "event": "e-2026-10-20",
        "what": "Strike-and-add text for the definitions section of the producer and laboratory "
                "rule, which 7.35.4.7 imports. Proposed, not adopted; heard November 20",
        "status": "record",
        "notes": "5 pages. Carries the terms of the August 25 amendment and adds eleven for the "
                 "fund: allowable amount, claim, claimant, covered treatment, director, federal "
                 "poverty guidelines, fund, household, other payer, program manager, and SHARE",
    },
    {
        "slug": "hearing-notice-7.35.4-2026-10-20",
        "name": "Notice of the November 20 rule hearing",
        "file": "documents/hearing-notice-7.35.4-2026-10-20.pdf",
        "cite": "The notice of the November 20, 2026 rule hearing on 7.35.4 NMAC",
        "date": "2026-10-20",
        "event": "e-2026-10-20",
        "what": "The notice fixing the rule hearing on the proposed 7.35.4 NMAC and the "
                "proposed amendment to 7.35.2.7 NMAC for November 20, 2026, and stating the "
                "legal authority and how to comment",
        "status": "record",
        "notes": "2 pages. It carries the video conference code, the telephone number, the written comment address, and the deadline: the close of the hearing",
    },
    {
        "slug": "medical-psilocybin-act-sb219-2025",
        "name": "The Medical Psilocybin Act",
        "file": "documents/medical-psilocybin-act-sb219-2025.pdf",
        "cite": "The Medical Psilocybin Act, Sections 26-2D-1 through 26-2D-11 NMSA 1978, as enacted in 2025",
        "date": "2025-06-20",
        "event": "e-2025-06-20",
        "what": "The enabling statute, Laws 2025, Chapter 73. Section 26-2D-11 creates the "
                "treatment equity fund, for treatment of qualified patients who meet income "
                "requirements set by department rule; the proposed rule cites it with 26-2D-7",
        "status": "record",
        "notes": "18 pages, the enrolled bill. The fund is bill Section 11, compiled as 26-2D-11",
    },
]


# The gaps register. Every row names the event it belongs to, and every event it
# names carries the reciprocal absence line.
GAPS = [
    {
        "id": "gap-written-recommendation",
        "name": "The written equity fund recommendation",
        "means": "On August 18 the department said it would write the committee's framework "
                 "in formal language for the board; on September 11 it read an outline into the "
                 "meeting and put it in the meeting chat. No written recommendation is posted. "
                 "The recommendation on this site is taken from the recordings",
        "at_event": "No written recommendation is held; the terms are taken from the recording.",
        "events": ["e-2026-09-11", "e-2026-08-18"],
    },
]


# The chain. Newest first. Each event: id (e-YYYY-MM-DD), date, kind (meeting,
# document, filing, scheduled, anticipated), what, and optionally changed
# (state transitions linking the page that owns each), attached (register
# slugs), absent (gap ids), said, and deeper (the fuller account).
EVENTS = [
    {
        "id": "e-2026-11-20",
        "date": "2026-11-20",
        "kind": "scheduled",
        "what": "<b>The rule hearing on the proposed 7.35.4 NMAC and the proposed amendment to "
                "7.35.2.7 NMAC, 9:00 AM, Harold Runnels Building auditorium, 1190 St. Francis "
                "Drive, Santa Fe</b>, in person, by video conference, and by telephone. Fixed by "
                "the <a href=\"#doc-hearing-notice-7.35.4-2026-10-20\">notice published October "
                "20</a>. Written comment must be received by the close of the hearing.",
    },
    {
        "id": "e-2026-10-20",
        "date": "2026-10-20",
        "kind": "document",
        "what": "<b>The department published the proposed 7.35.4 NMAC, Treatment Equity "
                "Fund</b>, with a proposed amendment to the definitions at 7.35.2.7 NMAC and the "
                "notice of the November 20 hearing on both.",
        "changed": [
            ("<b>A new Part.</b> Twenty sections; the first published text of the rule the "
             "Medical Psilocybin Act, Section 26-2D-11, leaves to the department.",
             "rule.html", "The proposed rule"),
            ("<b>Against the board vote.</b> Two preparatory or integrative sessions per later "
             "administration where the board voted three; the diagnostic evaluation and the "
             "cost of medication not named among allowable expenses.",
             "recommendation.html", "The board recommendation"),
        ],
        "attached": ["rules-7.35.4-proposed-2026-10-20-published",
                     "rules-7.35.2-amendments-2026-10-20-published",
                     "hearing-notice-7.35.4-2026-10-20"],
        "deeper": [("fund.html", "What the proposed rule would require, by who it reaches")],
    },
    {
        "id": "e-2026-09-11",
        "date": "2026-09-11",
        "kind": "meeting",
        "what": "<b>The Medical Psilocybin Advisory Board voted 7-0 to recommend the equity fund "
                "framework</b> from the Equity, Access and Cultural Considerations Committee, "
                "with three preparatory or integrative sessions for each additional "
                "administration session in place of the committee's two. The department read the "
                "framework as an outline of intent; the HCA delegate asked that the payer of last "
                "resort language be settled by the attorneys. Source: the department's "
                + _yt(REC_0911, "0:43:40", "recording") + ", automatic captions without speaker "
                "labels.",
        "said": {
            "basis": "From the automatic captions of the department's recording. The captions "
                     "carry no speaker labels; a name is given only where a speaker names "
                     "themself or is addressed by name.",
            "lines": [
                "The department, reading the outline: coverage \"for individuals who are at or "
                "below 200% of the poverty level\", the \"diagnostic evaluation\" and \"any of the "
                "medical evaluations\", \"6 preparatory or integration sessions with an "
                "administration session\", and two more per additional administration. "
                + _yt(REC_0911, "0:43:40") + " to " + _yt(REC_0911, "0:44:55"),
                "A speaker addressed as Chris: \"I initially said two, but I might bump it up to "
                "three.\" " + _yt(REC_0911, "0:45:49"),
                "\"But this is Larry. I like 3. I would support three.\" "
                + _yt(REC_0911, "0:49:55"),
                "A speaker called on as Keenan: \"specifically saying you have to bill Medicaid "
                "first might get you into some legal trouble.\" The department: \"our attorneys "
                "are already working on that specific language.\" "
                + _yt(REC_0911, "0:50:21") + ", " + _yt(REC_0911, "0:51:46"),
                "The department: \"the cost of medication\", travel \"if the patient resides "
                "more than 100 miles\", reimbursements not exceeding \"the rates for Medicaid "
                "reimbursement\", audit procedures, the ability \"to hold or suspend payments\", "
                "and New Mexico residency. " + _yt(REC_0911, "0:52:43") + " to "
                + _yt(REC_0911, "0:54:04"),
                "On provider travel to a homebound patient: \"That's not a part of this "
                "proposal.\" " + _yt(REC_0911, "0:54:32"),
                "The motion: \"to have a vote on the three. And after the first administration "
                "and for the first administration, 6 sessions of either prep and integration "
                "along with the equity fund tapering off to 200%.\" "
                + _yt(REC_0911, "1:01:53"),
                "\"seven in support\"; \"any no votes. I see none from the board members.\" "
                + _yt(REC_0911, "1:03:08") + ", " + _yt(REC_0911, "1:03:26"),
            ],
        },
        "absent": ["gap-written-recommendation"],
        "deeper": [("recommendation.html", "The recommendation beside the proposed text")],
    },
    {
        "id": "e-2026-08-18",
        "date": "2026-08-18",
        "kind": "meeting",
        "what": "<b>The Equity, Access and Cultural Considerations Committee voted 5-0 to send "
                "an equity fund framework to the Advisory Board</b>: 200 percent of the federal "
                "poverty level, the diagnostic evaluation, six preparatory or integrative "
                "sessions, up to three administration days with two more sessions for each "
                "additional day, the cost of medication, travel beyond 100 miles, the fund as "
                "last payer, a Medicaid rate cap, audit and hold or suspend clauses, and New "
                "Mexico residency. Source: the department's "
                + _yt(REC_0818, "1:03:57", "recording") + ", automatic captions without speaker "
                "labels.",
        "said": {
            "basis": "From the automatic captions of the department's recording, held at "
                     "source-text/recordings/2026-08-18-eacc-BkJgUrcFk50.txt. The captions carry "
                     "no speaker labels.",
            "lines": [
                "The read-out put to the vote: \"individuals at or below 200% of the poverty "
                "level items that would be covered are diagnostic evaluation up to six "
                "preparatory and or integrative sessions, administration day up to three "
                "administrations, cost of the medication, travel if patient resides more than "
                "100 miles\". " + _yt(REC_0818, "1:03:57"),
                "The addendum: \"up to three administration days with an additional two "
                "preparatory integrative\" sessions. " + _yt(REC_0818, "1:10:22"),
                "On distance: \"based on the travel distance. So, not necessarily straight as "
                "the crow flies.\" " + _yt(REC_0818, "1:09:53"),
                "A hardship application for a patient \"far off a road\" without a car was "
                "suggested and not put into the read-out. " + _yt(REC_0818, "1:09:01"),
                "Department discretion \"to ensure the intent of the fund and its geographic\" "
                "reach was suggested and not put into the read-out. " + _yt(REC_0818, "0:54:28"),
                "\"looks like we have five people\"; \"There are zero no votes.\" "
                + _yt(REC_0818, "1:11:33") + ", " + _yt(REC_0818, "1:12:33"),
            ],
        },
        "absent": ["gap-written-recommendation"],
        "deeper": [("recommendation.html", "The recommendation beside the proposed text")],
    },
    {
        "id": "e-2026-07-21",
        "date": "2026-07-21",
        "kind": "meeting",
        "what": "<b>The Equity, Access and Cultural Considerations Committee adopted 200 percent "
                "of the federal poverty level as the starting income threshold</b> for the "
                "fund, by a show of hands: \"we have adopted so far that 200% is a starting "
                "point\" (" + _yt(REC_0721, "1:14:38") + "). Automatic qualification of "
                "Medicaid recipients was raised and set aside without a vote (" + _yt(REC_0721,
                "1:54:08") + "). Source: the department's recording, automatic captions "
                "without speaker labels.",
    },
    {
        "id": "e-2025-06-20",
        "date": "2025-06-20",
        "kind": "document",
        "what": "<b>The Medical Psilocybin Act took effect.</b> Section 26-2D-11 creates the "
                "medical psilocybin treatment equity fund, a nonreverting fund administered by "
                "the department, for treatment of qualified patients who meet income "
                "requirements set by department rule; the proposed 7.35.4.3 cites it.",
        "attached": ["medical-psilocybin-act-sb219-2025"],
    },
]

CHAIN_NOTE = (
    "Every meeting, publication, and scheduled date is one event with its own address, so "
    "another page can cite the day rather than restate it. The committee and board meetings "
    "are cited to the department's recordings at the moment quoted; the captions are "
    "automatic and carry no speaker labels."
)
REGISTER_NOTE = (
    "Every document this site holds for this Part, what it is, when it landed, and whether it "
    "is current. The date in each row opens the event the document belongs to."
)
GAPS_NOTE = (
    "Named here so the gaps are visible rather than silent, each beside the event it belongs "
    "to."
)

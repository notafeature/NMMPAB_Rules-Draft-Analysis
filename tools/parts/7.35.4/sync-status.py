"""Part 7.35.4 data for tools/sync-status.py. Executed into that tool's namespace by
tools/partlib.py; the tool holds the code, this file holds what is true of the Part."""

# The dated events of the rulemaking. Every date a status surface states is
# one of these, so a date that moves is corrected here and nowhere else.
DATES = {
    "board":    "2026-09-11",   # the Advisory Board voted the equity fund recommendation 7-0
    "proposed": "2026-10-20",   # proposed 7.35.4 NMAC, the amendment to 7.35.2.7, and the notice
    "hearing":  "2026-11-20",   # the rule hearing, fixed by the notice
}

# The status items. Newest date first. state: open, defect, or settled.
STATUS = [
    {
        "id": "proposed",
        "state": "open",
        "date": DATES["proposed"],
        "summary": "7.35.4 NMAC, Treatment Equity Fund, was proposed October 20 and goes to a "
                   "rule hearing on November 20",
        "stand": "The department published the proposed 7.35.4 NMAC, Treatment Equity Fund, on "
                 "October 20, 2026, with a proposed amendment to the definitions at 7.35.2.7 NMAC "
                 "and a notice fixing the rule hearing for November 20, 2026, 9:00 AM, in the "
                 "Harold Runnels Building auditorium in Santa Fe, in person, by video conference, "
                 "and by telephone. The rule is proposed and not in effect. Written comment must "
                 "be received by the close of the hearing; how comment works is on "
                 "<a href=\"comment.html\">Comment</a>. The text is on "
                 "<a href=\"rule.html\">The proposed rule</a>.",
    },
    {
        "id": "board",
        "state": "open",
        "date": DATES["board"],
        "summary": "The proposed text departs from the September 11 board recommendation on "
                   "the session count and leaves two voted items unnamed",
        "stand": "The Advisory Board voted 7-0 on September 11, 2026 to recommend the equity fund "
                 "framework from the Equity, Access and Cultural Considerations Committee, with "
                 "three preparatory or integrative sessions for each additional administration "
                 "session. The proposed 7.35.4.14 (A) allows two. The diagnostic evaluation and "
                 "the cost of medication, both voted, are not named in the section that lists "
                 "allowable expenses. Item by item on "
                 "<a href=\"recommendation.html\">The board recommendation</a>.",
    },
]

# The scheduled dates, oldest first, as the front page lists them.
SCHEDULED = [
    (DATES["hearing"], "Rule hearing on the proposed 7.35.4 NMAC and the proposed amendment to "
                       "7.35.2.7 NMAC, 9:00 AM, Harold Runnels Building auditorium, Santa Fe, "
                       "and by video conference and telephone; fixed by the notice published "
                       "October 20. Written comment is due by the close of the hearing."),
]

ANTICIPATED = []

# The stages of this Part's rulemaking, drawn as the procession on the front page.
STAGES = [
    ("Committee vote", "EACC AUG 18", ""),
    ("Board vote", "SEP 11 · 7-0", ""),
    ("Proposed", "PUBLISHED OCT 20", "here"),
    ("Rule hearing", "NOV 20 · BY NOTICE", "todo"),
    ("Adopted", "NOT YET", "todo"),
]

# No eligibility legend on this Part.
LEGEND = []

BLOCKS = [
    ("index.html", "status stand", render_stand),
    ("index.html", "status scheduled", render_scheduled),
]

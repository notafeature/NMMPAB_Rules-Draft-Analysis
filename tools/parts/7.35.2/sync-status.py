"""Part 7.35.2 data for tools/sync-status.py. Executed into that tool's namespace by
tools/partlib.py; the tool holds the code, this file holds what is true of the Part."""

# The dated events of the rulemaking. Every date a status surface states is
# one of these, so a date that moves is corrected here and nowhere else.
DATES = {
    "notice":   "2026-03-24",   # notice of proposed rulemaking, New Mexico Register, Issue 6
    "hearing1": "2026-04-24",   # the rule hearing on the proposed 7.35.2 NMAC
    "adopted":  "2026-06-23",   # adopted, effective, published in the Register, Issue 12
    "amend":    "2026-08-25",   # proposed amendments to .7, .10, .24, and the hearing notice
    "hearing":  "2026-10-02",   # the rule hearing on the amendments, fixed by the notice
}

# The status items. Newest date first. state: open, defect, or settled.
STATUS = [
    {
        "id": "amendments",
        "state": "open",
        "date": DATES["amend"],
        "summary": "Amendments to the definitions, the general producer requirements, and the "
                   "transportation of psilocybin were proposed August 25 and go to the October 2 "
                   "rule hearing",
        "stand": "The department published proposed amendments to 7.35.2.7, 7.35.2.10, and "
                 "7.35.2.24 on August 25, with the notice fixing a rule hearing for October 2, "
                 "9:00 AM, in the Harold Runnels Building auditorium in Santa Fe, in person, by "
                 "video conference, and by telephone. The amendments would add twenty-one defined "
                 "terms, let producers sell to healing centers, and let certified practitioners and "
                 "healing centers transport psilocybin. Each is noted at the section it changes on "
                 "<a href=\"rule.html#s7\">The adopted rule</a>. Written comment must reach the "
                 "department by the close of the hearing; how comment works is on "
                 "<a href=\"comment.html\">Comment</a>.",
    },
    {
        "id": "text",
        "state": "settled",
        "date": DATES["adopted"],
        "summary": "7.35.2 NMAC, Producer and Laboratory Requirements, is in effect: adopted and "
                   "published June 23, 2026 in the New Mexico Register",
        "stand": "7.35.2 NMAC is the adopted rule for psilocybin producers and testing "
                 "laboratories, in effect since June 23, 2026, published that day in the New "
                 "Mexico Register, Volume XXXVII, Issue 12. Every section carries the history note "
                 "N, 6/23/2026: nothing in it has been amended. What it requires of a producer is on "
                 "<a href=\"producers.html\">For producers</a>, and of a laboratory on "
                 "<a href=\"laboratories.html\">For testing laboratories</a>; the text is on "
                 "<a href=\"rule.html\">The adopted rule</a>.",
    },
]

# The scheduled dates, oldest first, as the front page lists them.
SCHEDULED = [
    (DATES["hearing"], "Rule hearing on the proposed amendments to 7.35.2 NMAC and on the "
                       "proposed 7.35.3 NMAC, 9:00 AM, Harold Runnels Building auditorium, "
                       "Santa Fe, and by video conference and telephone; fixed by the notice "
                       "published August 25. Written comment is due by the close of the hearing."),
]

ANTICIPATED = []

# The stages of this Part's rulemaking, drawn as the procession on the front page.
STAGES = [
    ("Proposed", "NOTICED MAR 24", ""),
    ("Rule hearing", "APR 24", ""),
    ("Adopted", "IN EFFECT JUN 23", ""),
    ("Amendments proposed", "PUBLISHED AUG 25", "here"),
    ("Hearing on amendments", "OCT 2 · BY NOTICE", "todo"),
]

# No eligibility legend on this Part.
LEGEND = []

BLOCKS = [
    ("index.html", "status stand", render_stand),
    ("index.html", "status scheduled", render_scheduled),
]

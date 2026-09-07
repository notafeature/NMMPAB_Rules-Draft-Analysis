"""Part 7.35.3 data for tools/sync-status.py. Executed into that tool's namespace by
tools/partlib.py; the tool holds the code, this file holds what is true of the Part."""

# # The dated events of the rulemaking. Every date a status surface states is
# one of these, so a date that moves is corrected here and nowhere else.
# ---------------------------------------------------------------------------

DATES = {
    "deferred":  "2026-07-17",   # the 7-0 vote sending the hours to committee
    "published": "2026-07-23",   # the proposed rule published, hearing set for August 28
    "submitted": "2026-07-27",   # the committee recommendation reached the department
    "board":     "2026-08-14",   # Advisory Board meeting
    "committee": "2026-08-21",   # Training and Education Committee meeting: both proposals
                                 # side by side, no vote, the schedule restated
    "republish": "2026-08-25",   # the revised proposed rule, the 7.35.2 amendments, and
                                 # the hearing notice published
    "committee2": "2026-09-04",  # next Training and Education Committee meeting
    "board2":    "2026-09-11",   # full Advisory Board, afternoon, on the committee's work
    "hearing":   "2026-10-02",   # the rule hearing, fixed by the notice published
                                 # August 25. First set for August 28 with the July 23
                                 # publication, which was set aside
}


# ---------------------------------------------------------------------------
# The status items. Newest date first. Each item:
#
#   state     open, defect, or settled, which sets the label on the front page
#   date      the item's most recent state change, one of the DATES above
#   summary   the item in one line
#   stand     the full statement the front page carries, an HTML fragment
# ---------------------------------------------------------------------------

STATUS = [
    {
        "id": "text",
        "state": "open",
        "date": DATES["republish"],
        "summary": "The revised proposed rule published August 25, with amendments to 7.35.2 "
                   "NMAC and the notice fixing the rule hearing for October 2; comment "
                   "continues through the hearing",
        "stand": "The department published the revised proposed rule for 7.35.3 NMAC on "
                 "August 25, with proposed amendments to 7.35.2 NMAC and the notice fixing "
                 "the rule hearing for October 2, 9:00 AM, in the Harold Runnels Building "
                 "auditorium in Santa Fe, in person, by video conference, and by telephone. "
                 "The revised rule supersedes the set-aside July 23 publication and is "
                 "typeset in full at <a href=\"rule.html\">The published rule</a>; what it "
                 "changed is on <a href=\"changes.html\">Section by section</a>. Written "
                 "comment must reach the department by the close of the hearing; how comment "
                 "works is on <a href=\"comment.html\">Comment</a>.",
    },
    {
        "id": "hours",
        "state": "open",
        "date": DATES["republish"],
        "summary": "The revised text doubles the therapy module to 65 didactic hours with 10 "
                   "simulated patient hours and keeps the 100 and 120 practicum hours; the "
                   "recommendation stands at its August 21 position, and comment continues",
        "stand": "The revised text answers the hours question the board sent to committee: "
                 "the therapy module doubles to 65 didactic hours, at least one third in "
                 "person, with 10 simulated patient hours, an 80-hour module total matching "
                 "the recommendation's, without the recommendation's minimums in nine "
                 "content areas; the practicum keeps 100 hours for facilitators and 120 for "
                 "practitioners, adding a case-presentation evaluation inside them. The "
                 "committee's recommendation stands at its "
                 "<a href=\"recommendation.html\">August 21 position</a>, and the two "
                 "positions can be compared on the <a href=\"hours.html\">working model of "
                 "the hours</a>. Public comment continues through the October 2 hearing.",
    },
    {
        "id": "defects",
        "state": "defect",
        "date": DATES["republish"],
        "summary": "Five defect notes across four sections, re-verified against the August 25 "
                   "text; three practicum provisions flagged as not working as written",
        "stand": "The published text carries five defect notes across four sections, each "
                 "<a href=\"rule.html#s14\">at the provision it sits in</a>, re-verified "
                 "against the August 25 text. Three provisions a "
                 "practicum change reaches are flagged as not working as written on "
                 "<a href=\"deferred.html\">What a practicum change touches</a>. Two of those "
                 "three are among the five; the third, a conflict between the two waivers that "
                 "set 40 contact hours, is analyzed there and carries no note in the rule.",
    },
    {
        "id": "cs-number",
        "state": "settled",
        "date": DATES["republish"],
        "summary": "The certifying clinician's controlled-substance number, kept July 17 and "
                   "now inside the amended definition; the reciprocity deadlines stand",
        "stand": "The certifying clinician's controlled-substance number, kept July 17, now "
                 "sits inside the definition of certifying clinician in the amended "
                 "7.35.2.7 as well as in the <a href=\"rule.html#s9\">application "
                 "requirements</a>. The reciprocity deadlines, set to December 31, 2027 on "
                 "July 9, stand unchanged in the revised text.",
    },
]


# The scheduled dates, oldest first, as the front page lists them under
# "Scheduled". Each date is one of the DATES above. Only a meeting a public
# body scheduled on its own record belongs here; a date the department has
# stated but no notice fixes belongs in ANTICIPATED, under its own label.

SCHEDULED = [
    (DATES["committee2"], "Training and Education Committee meets, 9 to 11 AM."),
    (DATES["board2"], "Full Advisory Board meets, afternoon, on the committee's work."),
    (DATES["hearing"], "Rule hearing, 9:00 AM, Harold Runnels Building auditorium, Santa "
                       "Fe, and by video conference and telephone; fixed by the notice "
                       "published August 25. Written comment is due by the close of the "
                       "hearing."),
]

ANTICIPATED = []


# The five stages of the rulemaking, drawn as the procession on the front
# page. `flag` is empty, "here" for the current stage, or "todo".

STAGES = [
    ("Committee recommendation", "JAN – AUG 21", ""),
    ("First published text", "JUL 23 · SET ASIDE", ""),
    ("Revised rules", "PUBLISHED AUG 25", "here"),
    ("Rule hearing", "OCT 2 · BY NOTICE", "todo"),
    ("Adopted rule", "AFTER THE HEARING", "todo"),
]


# The two dated status definitions in the eligibility legend: the class on the
# swatch, the word, and the definition. The rest of that legend defines the
# verdict vocabulary of the tables and stays with the page.

LEGEND = [
    ("set", "Settled", "The published text of August 25 states it, and it was not changed "
                       "on the record."),
    ("open", "Open", "The published text of August 25 states it, and it is still moving: "
                     "the didactic, practicum, mentoring, and supervisory hours carry the "
                     "committee's August 21 recommendation beside the revised text, and "
                     "public comment continues through the October 2 hearing."),
]


# ---------------------------------------------------------------------------


def render_kicker():
    """The kicker line on the training-hours page."""
    return ('    <p class="kicker">7.35.3.17, .18, and .19 · '
            f'<b>revised text published {abbr_date(DATES["republish"])}</b> · '
            f'rule hearing {abbr_date(DATES["hearing"])}</p>')


def render_strip():
    """The status strip on the training-hours record: a dated record, not a
    live status block. The label carries the date of the newest status change
    the strip states, and the strip closes by naming the front page as where
    the current state of the rulemaking lives. A record page carrying a live
    status block is how this page came to misstate the recommendation for a
    day, and this frame is what ends that failure mode."""
    asof = max(i["date"] for i in STATUS)
    return (
        '      <div class="statusline">\n'
        f'        <span class="lab">Status as of {long_date(asof)}</span>\n'
        f'        <p>On <b>{short_date(DATES["deferred"])}</b> the Advisory Board voted '
        "<b>7-0</b> to defer the didactic and practicum hours to the Training and Education "
        f'Committee. On <b>{short_date(DATES["published"])}</b> the department published its '
        "proposed rule with the practicum hours unchanged; that publication and its August "
        "28 hearing were later set aside. The committee's recommendation was submitted on "
        f'<b>{short_date(DATES["submitted"])}</b> and refined at the '
        f'<b>{short_date(DATES["committee"])}</b> committee meeting to 80 didactic hours and '
        "a staged practicum of <b>114 or 102 hours</b> by role; the "
        '<a href="recommendation.html">recommendation page</a> holds it in full. On '
        f'<b>{short_date(DATES["republish"])}</b> the department published the revised '
        "proposed rule: the therapy module <b>doubled to 65 didactic hours</b> with 10 "
        "simulated patient hours, the practicum <b>unchanged at 100 and 120 hours</b> with "
        "a case-presentation evaluation added inside them. The rule hearing is "
        f'<b>{short_date(DATES["hearing"])}</b>, fixed by notice. The figures below are '
        "from the August 25 published text. The current state of the rulemaking is on "
        '<a href="index.html">Where things stand</a>.</p>\n'
        "      </div>"
    )


BLOCKS = [
    ("index.html", "status stand", render_stand),
    ("index.html", "status scheduled", render_scheduled),
    ("hours.html", "status kicker", render_kicker),
    ("eligibility.html", "status legend", render_legend),
    ("training-hours-record.html", "status strip", render_strip),
]

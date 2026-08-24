#!/usr/bin/env python3
"""Generate the live status surfaces across the site from one STATUS structure.

Four places on the site tell a reader where the rulemaking stands, and until
this tool existed every one of them was hand-written HTML: the "Where things
stand" block on index.html, the kicker line on hours.html, the two dated
status definitions in the legend on eligibility.html, and the status strip on
training-hours-record.html. Every hand-maintained status fact on this site has
drifted and no tool-owned block ever has; the strip on the training-hours
record said the committee recommendation was undelivered for a day after five
other pages said it was submitted, which is the defect class this tool ends.
The department stated on August 21 that it will publish revised proposed
rules on August 25, with the rule hearing anticipated for October 2; each
such change is made here once and written everywhere.

Three structures hold the status once:

    DATES      the dated events of the rulemaking, each named once, so a date
               that moves is corrected in one place
    STATUS     each status item's state, date, and one-line summary, with the
               full statement the front page carries; newest date first
    SCHEDULED  the dates ahead, as the front page lists them
    STAGES     the five stages of the rulemaking and which one is current,
               drawn as the procession on the front page

LEGEND holds the two status definitions the eligibility legend carries; the
rest of that legend defines the verdict vocabulary of the tables and belongs
to the page.

Five regions are generated, each between its own markers, and nothing
outside them is touched:

    index.html                   the "Where things stand" section, with the
                                 procession, and the "Scheduled" column
    hours.html                   the kicker line under the page head
    eligibility.html             the Settled and Open rows of the legend
    training-hours-record.html   the status strip

tools/check-site.py imports this module and calls stale() to fail the build
if any of the four pages no longer matches the data here.

Usage:
    python3 tools/sync-status.py           # write the four regions into the pages
    python3 tools/sync-status.py --check   # exit 1 if any page is stale
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


# ---------------------------------------------------------------------------
# The dated events of the rulemaking. Every date a status surface states is
# one of these, so a date that moves is corrected here and nowhere else.
# ---------------------------------------------------------------------------

DATES = {
    "deferred":  "2026-07-17",   # the 7-0 vote sending the hours to committee
    "published": "2026-07-23",   # the proposed rule published, hearing set for August 28
    "submitted": "2026-07-27",   # the committee recommendation reached the department
    "board":     "2026-08-14",   # Advisory Board meeting
    "committee": "2026-08-21",   # Training and Education Committee meeting: both proposals
                                 # side by side, no vote, the schedule restated
    "republish": "2026-08-25",   # revised proposed rules publish, per the department's
                                 # August 21 statement
    "committee2": "2026-09-04",  # next Training and Education Committee meeting
    "board2":    "2026-09-11",   # full Advisory Board, afternoon, on the committee's work
    "hearing":   "2026-10-02",   # the rule hearing, anticipated; the final notice, in
                                 # preparation with the hearing officer, will fix the date.
                                 # First set for August 28 with the July 23 publication
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
        "date": DATES["committee"],
        "summary": "No proposed rule is currently published: the July 23 publication and its "
                   "August 28 hearing were set aside; the department's stated date for revised "
                   "rules is August 25, with the rule hearing anticipated for early October",
        "stand": "No proposed rule is currently published. The July 23 publication and its "
                 "August 28 hearing were set aside; the July 23 text remains on this site as "
                 "the <a href=\"rule.html\">last published text</a>. The department's stated "
                 "date for publishing revised proposed rules is August 25, and the rule "
                 "hearing is anticipated for early October, October 2 named at the "
                 "<a href=\"record.html#e-2026-08-21\">August 21 committee meeting</a>, "
                 "virtual and in person; the final notice, in preparation with the hearing "
                 "officer, will fix the date. Public comment continues after publication, "
                 "through the hearing.",
    },
    {
        "id": "hours",
        "state": "open",
        "date": DATES["committee"],
        "summary": "The committee's recommendation stands at the August 21 position: 80 "
                   "didactic hours and a staged practicum of 114 or 102 hours by role; it is "
                   "in the department's hands for the revised rules",
        "stand": "The training hours are the committee's to recommend and the department's to "
                 "write. The recommendation stands at the "
                 "<a href=\"recommendation.html\">August 21 position</a>: 80 didactic hours "
                 "with minimums in nine content areas, and a staged practicum of 114 hours "
                 "for licensed providers or 102 for facilitators, closing with case "
                 "presentation and consultation. The department's own proposal, shown beside "
                 "it on August 21, also sets 80 didactic hours and reaches 120 or 100 "
                 "practicum hours, structured differently. No vote was taken; the "
                 "recommendation is in the department's hands for the revised rules.",
    },
    {
        "id": "defects",
        "state": "defect",
        "date": DATES["published"],
        "summary": "Five defect notes across four sections of the last published text; three "
                   "practicum provisions flagged as not working as written",
        "stand": "The last published text carries five defect notes across four sections, each "
                 "<a href=\"rule.html#s14\">at the provision it sits in</a>. Three provisions a "
                 "practicum change reaches are flagged as not working as written on "
                 "<a href=\"deferred.html\">What a practicum change touches</a>. Two of those "
                 "three are among the five; the third, a conflict between the two waivers that "
                 "set 40 contact hours, is analyzed there and carries no note in the rule.",
    },
    {
        "id": "cs-number",
        "state": "settled",
        "date": DATES["deferred"],
        "summary": "The certifying-clinician controlled-substance number, kept July 17, and the "
                   "reciprocity deadlines, set July 9; both stand in the last published text",
        "stand": "The certifying-clinician controlled-substance number, kept July 17, and the "
                 "reciprocity deadlines, set to December 31, 2027 on July 9. Both stand in the "
                 "<a href=\"rule.html#s9\">last published text</a>, and neither is changed by "
                 "the August 21 recommendation.",
    },
]


# The scheduled dates, oldest first, as the front page lists them under
# "Scheduled". Each date is one of the DATES above.

SCHEDULED = [
    (DATES["republish"], "The department's stated date for publishing revised proposed "
                         "rules, stated August 14 and August 21."),
    (DATES["committee2"], "Training and Education Committee meets, 9 to 11 AM."),
    (DATES["board2"], "Full Advisory Board meets, afternoon, on the committee's work."),
    (DATES["hearing"], "Rule hearing on 7.35.3 NMAC, anticipated; the final notice will fix "
                       "the date. Public comment is taken and recorded there."),
]


# The five stages of the rulemaking, drawn as the procession on the front
# page. `flag` is empty, "here" for the current stage, or "todo".

STAGES = [
    ("Committee recommendation", "JAN – AUG 21", ""),
    ("Published text", "JUL 23 · SET ASIDE", ""),
    ("Revised rules", "AUG 25 · STATED", "here"),
    ("Rule hearing", "EARLY OCT · ANTICIPATED", "todo"),
    ("Adopted rule", "AFTER THE HEARING", "todo"),
]


# The two dated status definitions in the eligibility legend: the class on the
# swatch, the word, and the definition. The rest of that legend defines the
# verdict vocabulary of the tables and stays with the page.

LEGEND = [
    ("set", "Settled", "The last published text states it, and it was not changed on the "
                       "record."),
    ("open", "Open", "The last published text states it, but it is still moving: the "
                     "practicum and didactic hours carry the committee's August 21 "
                     "recommendation, and the department writes the revised rules."),
]


# ---------------------------------------------------------------------------

def validate():
    """Fail on a state outside the vocabulary, a date the site does not record,
    or a procession without exactly one current stage."""
    problems = []
    if len({i["id"] for i in STATUS}) != len(STATUS):
        problems.append("two status items share an id")
    for iso in DATES.values():
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", iso):
            problems.append(f"date {iso!r} is not ISO")
    for i in STATUS:
        if i["state"] not in ("open", "defect", "settled"):
            problems.append(f"item {i['id']} has state {i['state']!r}")
        if i["date"] not in DATES.values():
            problems.append(f"item {i['id']} carries date {i['date']}, which is not in DATES")
        if "\n" in i["summary"]:
            problems.append(f"item {i['id']}: the summary is more than one line")
    order = [i["date"] for i in STATUS]
    if order != sorted(order, reverse=True):
        problems.append("STATUS is not in newest-first order")
    for iso, _ in SCHEDULED:
        if iso not in DATES.values():
            problems.append(f"a scheduled date {iso} is not in DATES")
    if [iso for iso, _ in SCHEDULED] != sorted(iso for iso, _ in SCHEDULED):
        problems.append("SCHEDULED is not in oldest-first order")
    if [f for _, _, f in STAGES].count("here") != 1:
        problems.append("the procession does not have exactly one current stage")
    for _, _, f in STAGES:
        if f not in ("", "here", "todo"):
            problems.append(f"a stage carries flag {f!r}")
    if problems:
        raise SystemExit("tools/sync-status.py: " + "; ".join(problems))


validate()


def long_date(iso):
    y, m, d = iso.split("-")
    return f"{MONTHS[int(m) - 1]} {int(d)}, {y}"


def short_date(iso):
    y, m, d = iso.split("-")
    return f"{MONTHS[int(m) - 1]} {int(d)}"


def abbr_date(iso):
    y, m, d = iso.split("-")
    return f"{MONTHS[int(m) - 1][:3]} {int(d)}"


def render_stand():
    """The "Where things stand" section on the front page: the three status
    items and the procession."""
    out = ["  <section>", '    <p class="seclabel">Where things stand</p>']
    for i in STATUS:
        out.append(f'    <div class="fix"><b>{i["state"].upper()}</b>'
                   f'<span class="what">{i["stand"]}</span></div>')
    out.append('    <div class="procession" aria-label="The rulemaking in five stages">')
    for name, dates, flag in STAGES:
        cls = "pstage" + (f" {flag}" if flag else "")
        out.append(f'      <div class="{cls}"><div class="n">{name}</div>'
                   f'<div class="d">{dates}</div></div>')
    out.append("    </div>")
    out.append("  </section>")
    return "\n".join(out)


def render_scheduled():
    """The "Scheduled" column on the front page."""
    out = ["    <div>", '      <p class="seclabel">Scheduled</p>']
    for iso, text in SCHEDULED:
        out.append(f'      <div class="fix"><b>{abbr_date(iso).upper()}</b>'
                   f'<span class="what">{text}</span></div>')
    out.append("    </div>")
    return "\n".join(out)


def render_kicker():
    """The kicker line on the training-hours page."""
    return ('    <p class="kicker">7.35.3.17, .18, and .19 · '
            f'<b>recommendation refined {abbr_date(DATES["committee"])}</b> · '
            f'hearing anticipated {abbr_date(DATES["hearing"])}</p>')


def render_legend():
    """The Settled and Open rows of the eligibility legend."""
    return "\n".join(
        f'        <div class="li"><span class="sw {cls}">{word}</span>'
        f"<span>{text}</span></div>"
        for cls, word, text in LEGEND
    )


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
        "proposed rule with the practicum hours unchanged and the shared didactic module "
        "<b>raised from 25 hours to 30</b>; that publication and its August 28 hearing were "
        "later set aside, and the July 23 text stands as the last published text. The "
        "committee's recommendation was submitted on "
        f'<b>{short_date(DATES["submitted"])}</b> and refined at the '
        f'<b>{short_date(DATES["committee"])}</b> committee meeting to 80 didactic hours and '
        "a staged practicum of <b>114 or 102 hours</b> by role; the "
        '<a href="recommendation.html">recommendation page</a> holds it in full. The '
        "department's stated date for revised rules is "
        f'<b>{short_date(DATES["republish"])}</b>, with the rule hearing anticipated for '
        f'<b>{short_date(DATES["hearing"])}</b>. The figures below are from the last '
        "published text. The current state of the rulemaking is on "
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


def render(name, src):
    """Return the named page with its generated region rewritten."""
    for page, region, build in BLOCKS:
        if page != name:
            continue
        open_mark = f"<!-- {region}: generated by tools/sync-status.py, do not hand-edit -->"
        close_mark = f"<!-- /{region} -->"
        pattern = re.compile(r"(?m)^([ \t]*)" + re.escape(open_mark) + r".*?"
                             + re.escape(close_mark), re.S)
        m = pattern.search(src)
        if not m:
            raise SystemExit(f"tools/sync-status.py: {name} has no {open_mark} block")
        pad = m.group(1)
        replacement = pad + open_mark + "\n" + build() + "\n" + pad + close_mark
        src = pattern.sub(lambda _: replacement, src, count=1)
    return src


def stale():
    """The pages that no longer match the data here, empty when none do."""
    out = []
    for name in dict.fromkeys(page for page, _, _ in BLOCKS):
        src = open(os.path.join(DOCS, name)).read()
        if render(name, src) != src:
            out.append(name)
    return out


def main():
    check = "--check" in sys.argv
    changed = []
    for name in dict.fromkeys(page for page, _, _ in BLOCKS):
        path = os.path.join(DOCS, name)
        src = open(path).read()
        new = render(name, src)
        if new == src:
            print("in sync     " + name)
            continue
        if check:
            print("STALE       " + name)
        else:
            open(path, "w").write(new)
            print("updated     " + name)
        changed.append(name)
    print()
    for i in STATUS:
        print(f"{i['state'].upper():8}{long_date(i['date'])}: {i['summary']}.")
    if check and changed:
        print("\n%d page(s) stale. Run without --check to fix." % len(changed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

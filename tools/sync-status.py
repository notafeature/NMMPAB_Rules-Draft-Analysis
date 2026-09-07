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
The July 23 publication was set aside, the recommendation stands at the
committee's August 21 position, and the rule hearing is anticipated for
early October; each such change is made here once and written everywhere.
A date the department states is never carried as a scheduled item: stated
dates in this rulemaking have been set and overridden.

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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import partlib
PART = partlib.current_part()
DOCS = partlib.docs_dir(PART)

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]



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
    for iso, _ in SCHEDULED + ANTICIPATED:
        if iso not in DATES.values():
            problems.append(f"a scheduled or anticipated date {iso} is not in DATES")
    if [iso for iso, _ in SCHEDULED] != sorted(iso for iso, _ in SCHEDULED):
        problems.append("SCHEDULED is not in oldest-first order")
    if [f for _, _, f in STAGES].count("here") != 1:
        problems.append("the procession does not have exactly one current stage")
    for _, _, f in STAGES:
        if f not in ("", "here", "todo"):
            problems.append(f"a stage carries flag {f!r}")
    if problems:
        raise SystemExit("tools/sync-status.py: " + "; ".join(problems))




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
    """The "Scheduled" column on the front page, with the anticipated dates
    under their own label so a stated date is never listed as scheduled."""
    out = ["    <div>", '      <p class="seclabel">Scheduled</p>']
    for iso, text in SCHEDULED:
        out.append(f'      <div class="fix"><b>{abbr_date(iso).upper()}</b>'
                   f'<span class="what">{text}</span></div>')
    if ANTICIPATED:
        out.append('      <p class="seclabel">Anticipated</p>')
        for iso, text in ANTICIPATED:
            out.append(f'      <div class="fix"><b>{abbr_date(iso).upper()}</b>'
                       f'<span class="what">{text}</span></div>')
    out.append("    </div>")
    return "\n".join(out)

def render_legend():
    """The Settled and Open rows of the eligibility legend."""
    return "\n".join(
        f'        <div class="li"><span class="sw {cls}">{word}</span>'
        f"<span>{text}</span></div>"
        for cls, word, text in LEGEND
    )

# The Part's data: the dates, the status items, the scheduled and anticipated
# dates, the stages, the legend, the two prose renders, and BLOCKS. Loaded after
# the helpers above, which the data file's renders call.
partlib.load_data(PART, "sync-status", globals())
validate()


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

#!/usr/bin/env python3
"""Generate the starting-license picker and the five panels on docs/pathways.html.

pathways.html is the one page organized by the reader's own situation: pick a
starting license, and every step to each permit it opens is listed with its
status, its citation, and what the committee recommendation would change. All of
it used to be built by JavaScript into two empty divs, which meant browser find
found nothing, a search engine indexed nothing, and a reader without JavaScript
was handed a pointer to another page instead of the routes.

This script owns that data and writes every panel into the page, in the manner
of tools/build-rule-page.py. Three structures hold it once:

    PERMITS   the four routes, each an ordered list of steps; a step carries its
              text, its status, its flag word, its why-line, its citation, the
              committee recommendation's change to it, and whether it points at
              the working model of the hours
    STARTS    the five starting licenses, each with the verdict on every permit
              and the eligibility band its rows sit in
    STATE     the four verdict words and the classes that carry them

The page then holds every panel and every route's step list at once. The script
at the foot of the page no longer renders anything; it moves the selection, and
the CSS this script generates narrows the page to the selected starting license
and the selected route. Without JavaScript nothing is narrowed, so every panel
and every step stays in view and browser find reaches all of it. The one-line
script in the head marks the document as scripted before anything paints, so a
reader with JavaScript never sees the page collapse from five panels to one.

Three regions of docs/pathways.html are generated, each between its own markers,
and nothing outside them is touched: the selection rules in the page's
stylesheet, the picker at #starts, and the panels at #panel.

tools/check-site.py imports this module and calls stale() to fail the build if
the page no longer matches the data here.

Usage:
    python3 tools/sync-pathways.py           # write the three blocks into the page
    python3 tools/sync-pathways.py --check   # exit 1 if pathways.html is stale
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
PAGE = os.path.join(DOCS, "pathways.html")

# The published rule, cited by page, and the July 9 meeting transcript. Every
# step's citation is built from one of these two.
J7 = "documents/rules-draft-2026-07-23-published.pdf#page="
T7 = "documents/NMMPAB-2026-07-09-transcript.pdf"


def L(text, href):
    """A citation link, opening the source in a new tab."""
    return f'<a href="{href}" target="_blank">{text}</a>'


# ---------------------------------------------------------------------------
# The four routes. A step's keys:
#
#   t      the requirement, as the reader meets it
#   s      set | open | chal, which sets the step's status treatment
#   flag   the word on the status pill, on open and contested steps only
#   why    why the step is open or contested, or what the published text does
#          and does not say
#   src    the citation, built with L()
#   metz   what the committee recommendation submitted July 27 would change
#   model  1 where the step states hours the working model on hours.html exists
#          to move
#
# `dot` is a per-permit colour the page has never rendered. It is kept because
# it is data the page carried, not because anything reads it.
# ---------------------------------------------------------------------------

PERMITS = {
    "dc": {
        "name": "Certifying Clinician",
        "dot": "#256E8C",
        "steps": [
            {"t": "Hold a current NM professional license (for example MD, NP).",
             "s": "set",
             "why": "The published rule names license examples; it does not describe a diagnosing scope.",
             "src": L("published rule 7.35.3.9, p.2", J7 + "2")},
            {"t": "Approved <b>Certifying Clinician training</b>: an 8-hour module covering pharmacology, "
                  "42 CFR Part 2, diagnosis of qualifying conditions, medical clearance, monitoring, and "
                  "data-collection requirements.",
             "s": "set",
             "src": L("published rule 7.35.3.18, p.11", J7 + "11")},
            {"t": "Hold a <b>New Mexico Controlled Substance number</b> (state number, not the federal "
                  "DEA number).",
             "s": "open", "flag": "Open",
             "why": "On July 17 the department said it will keep this requirement in the rule and revised "
                    "the certifying-clinician exam language. Not final; it goes to a public hearing.",
             "src": L("published rule 7.35.3.9, p.2", J7 + "2") + " &middot; "
                    + L("July 17 update", "cs-number.html#update")},
            {"t": "<b>No practicum.</b>",
             "s": "set",
             "why": "The practicum section applies to practitioners and facilitators only; the Certifying "
                    "Clinician packet lists no practicum item.",
             "src": L("published rule 7.35.3.18, p.12", J7 + "12") + " &middot; " + L("p.8", J7 + "8")},
            {"t": "Apply to NMDOH. Certification is valid <b>2 years</b> from approval.",
             "s": "set",
             "src": L("published rule 7.35.3.9, p.2", J7 + "2")},
            {"t": "Continuing education: <b>8 CME hours every 2 years</b>.",
             "s": "set",
             "src": L("published rule 7.35.3.18, p.12", J7 + "12")},
        ],
    },
    "recip": {
        "name": "Reciprocity",
        "dot": "#5A4A88",
        "steps": [
            {"t": "Trained and licensed outside New Mexico. Your program must be on <b>NMDOH's approved "
                  "reciprocity list</b>, which names Oregon and Colorado programs, or you must show your "
                  "program has other governmental approval and a curriculum substantially equivalent to "
                  "New Mexico's.",
             "s": "set",
             "src": L("published rule 7.35.3.10 and 7.35.3.19", J7 + "6")},
            {"t": "Complete the <b>New Mexico Module</b>.",
             "s": "set",
             "src": L("published rule 7.35.3.17, p.10", J7 + "10")},
            {"t": "Apply by the waiver deadline for a reduced practicum: at least <b>40 hours of contact "
                  "time</b> instead of the full practicum.",
             "s": "set",
             "why": "The published rule sets this deadline at December 31, 2027. The July 9 draft still "
                    "read December 31, 2026; the board moved it without objection that day and the "
                    "published text now carries it. Board chair Ian Dunn noted that date is a legislative "
                    "backstop, not the target date.",
             "src": L("published rule 7.35.3.10, p.4", J7 + "4") + " &middot; "
                    + L("July 9 meeting transcript", T7)},
            {"t": "NMDOH may further reduce the practicum requirement at its discretion, to build the "
                  "program's initial infrastructure.",
             "s": "set",
             "why": "The published rule sets no end date for this discretion, at 7.35.3.19 (F). The "
                    "related waiver deadline is December 31, 2027.",
             "src": L("published rule 7.35.3.10, p.4", J7 + "4") + " &middot; "
                    + L("July 9 meeting transcript", T7)},
            {"t": "Apply as Practitioner or Facilitator. The reciprocity application packet lists items "
                  "for those two permits only.",
             "s": "open", "flag": "Unresolved",
             "why": "The published rule is inconsistent here. Reciprocity now sits inside 7.35.3.10, "
                    "which names certifying clinicians as eligible to apply on the basis of a program "
                    "from another jurisdiction, while the application items listed there are for "
                    "practitioners and facilitators.",
             "src": L("published rule 7.35.3.10 and 7.35.3.19", J7 + "6") + " &middot; "
                    + L("p.9", J7 + "9")},
        ],
    },
    "prac": {
        "name": "Practitioner",
        "dot": "#5A4A88",
        "steps": [
            {"t": "Hold a current NM professional license (for example PSY, LSW, LCSW).",
             "s": "set",
             "why": "The published rule names license examples; it does not describe a therapy or "
                    "counseling scope.",
             "src": L("published rule 7.35.3.9, p.2", J7 + "2")},
            {"t": "Certifications and attestation, same as Facilitator.",
             "s": "set",
             "src": L("published rule 7.35.3.18, p.12", J7 + "12") + " &middot; " + L("pp.2-3", J7 + "2")},
            {"t": "Approved <b>Practitioner training</b>: the 30-hour core module plus a 5-hour module on "
                  "psychedelic and psilocybin therapeutic approaches.",
             "s": "set",
             "src": L("published rule 7.35.3.18, p.11", J7 + "11"),
             "metz": "80 didactic hours in place of 35, on one standard shared with facilitators rather "
                     "than tiered by role, with minimum hours in nine content areas. The recommendation "
                     "also renames the permit: practitioner becomes licensed provider."},
            {"t": "Practicum at a healing center or other approved location. Published rule: "
                  "<b>120 hours</b>.",
             "s": "open", "flag": "Open",
             "why": "Deferred to the Training and Education Committee by a 7-0 board vote July 17; the "
                    "committee recommendation was submitted July 27.",
             "src": L("published rule 7.35.3.18, p.12", J7 + "12"),
             "model": 1,
             "metz": "70 hours, staged: the facilitator sequence plus 10 hours leading sessions with a "
                     "licensed provider as second chair."},
            {"t": "Includes an additional <b>20 hours supervising facilitators</b> during administration "
                  "day sessions.",
             "s": "chal", "flag": "Contested",
             "why": "Dr. Anne Metz asked to make this optional at the June 25 committee meeting. The "
                    "department kept it; it remains in the published rule.",
             "src": L("published rule 7.35.3.18, p.12", J7 + "12") + " &middot; "
                    + L("committee meeting, 6/25", "changes.html"),
             "metz": "Reduced to 10 hours and folded into step four of the scaffolded practicum."},
            {"t": "Mentoring: <b>10 hours</b> after graduation and after the practicum.",
             "s": "set",
             "src": L("published rule 7.35.3.17, p.10", J7 + "10"),
             "metz": "Replaced by 20 hours of case presentation and consultation after the practicum, "
                     "with sign-off requiring two presented cases of the permittee&rsquo;s own "
                     "regulated-medicine clients."},
            {"t": "Apply to NMDOH. Certification is valid <b>2 years</b> from approval.",
             "s": "set",
             "src": L("published rule 7.35.3.9, p.2", J7 + "2")},
            {"t": "Continuing education: <b>20 hours every 2 years</b>. Keep BLS or CPR/AED current.",
             "s": "set",
             "src": L("published rule 7.35.3.18, p.12", J7 + "12")},
        ],
    },
    "fac": {
        "name": "Facilitator",
        "dot": "#3E8E6E",
        "steps": [
            {"t": "Apply for certification. <b>No professional license required.</b>",
             "s": "set",
             "src": L("published rule 7.35.3.10, p.4", J7 + "4")},
            {"t": "Certifications: <b>HIPAA, plus BLS or (CPR and AED)</b>. Attestation you are not a "
                  "registered sex offender.",
             "s": "set",
             "src": L("published rule 7.35.3.18, p.12", J7 + "12") + " &middot; " + L("p.9", J7 + "9")},
            {"t": "Approved <b>Facilitator training</b>. Begins with the New Mexico Module, the one "
                  "module you cannot test out of.",
             "s": "set",
             "src": L("published rule 7.35.3.18, p.11", J7 + "11") + " &middot; " + L("p.7", J7 + "7"),
             "metz": "80 didactic hours in place of 35, with minimum hours in nine content areas. The "
                     "New Mexico module stays required of every role, with no exemption by reciprocity."},
            {"t": "Practicum at a healing center or other approved location. Published rule: "
                  "<b>100 hours</b>.",
             "s": "open", "flag": "Open",
             "why": "Deferred to the Training and Education Committee by a 7-0 board vote July 17; the "
                    "committee recommendation was submitted July 27.",
             "src": L("published rule 7.35.3.18, p.12", J7 + "12"),
             "model": 1,
             "metz": "60 hours, staged: well participants first, then co-facilitation with a "
                     "department-permitted licensed provider, then group work, with every stage spanning "
                     "preparation, administration, and integration."},
            {"t": "Mentoring: <b>10 hours</b> after graduation and after the practicum.",
             "s": "set",
             "src": L("published rule 7.35.3.17, p.10", J7 + "10"),
             "metz": "Replaced by 20 hours of case presentation and consultation after the practicum, "
                     "with sign-off requiring two presented cases of the permittee&rsquo;s own "
                     "regulated-medicine clients."},
            {"t": "Apply to NMDOH. Certification is valid <b>2 years</b> from approval.",
             "s": "set",
             "src": L("published rule 7.35.3.9, p.2", J7 + "2")},
            {"t": "Continuing education: <b>20 hours every 2 years</b>. Keep BLS or CPR/AED current.",
             "s": "set",
             "src": L("published rule 7.35.3.18, p.12", J7 + "12")},
        ],
    },
}

# ---------------------------------------------------------------------------
# The five starting licenses, in the order the picker offers them. `elig` is the
# band on eligibility.html whose rows this profile summarizes; `cs` marks the
# two profiles whose certifying-clinician verdict turns on the
# controlled-substance number. Routes are listed in the order they are shown,
# and the first route that is not a dead end is the one whose steps open.
# ---------------------------------------------------------------------------

STARTS = [
    {"elig": "band-community", "id": "none", "title": "No health license",
     "ex": "Community, peer, lived experience, chaplain, hospice, spiritual care, traditional healer.",
     "routes": [
         {"permit": "dc", "state": "nopath", "line": "Needs a NM professional license."},
         {"permit": "prac", "state": "nopath", "line": "Needs a NM professional license."},
         {"permit": "fac", "state": "open", "line": "No professional license required."},
     ]},
    {"elig": "band-behavioral", "cs": True, "id": "therapy", "title": "Therapy or counseling license",
     "ex": "Psychologist, LCSW, LPCC, LMFT, psychiatric NP.",
     "routes": [
         {"permit": "dc", "state": "part",
          "line": "Only with a NM Controlled Substance number. That requirement is the open July 9 "
                  "question, not your license scope."},
         {"permit": "prac", "state": "open", "line": "Direct route."},
         {"permit": "fac", "state": "open", "line": "Also open. No license needed for this one."},
     ]},
    {"elig": "band-medical", "cs": True, "id": "diagnose", "title": "License to diagnose",
     "ex": "Physician (MD/DO), psychiatrist, nurse practitioner, physician assistant.",
     "routes": [
         {"permit": "dc", "state": "open",
          "line": "Direct route, with the open Controlled Substance number question."},
         {"permit": "prac", "state": "part",
          "line": "Requires a NM professional license (the published rule gives PSY, LSW, LCSW as "
                  "examples; it does not describe a therapy or counseling scope)."},
         {"permit": "fac", "state": "open", "line": "Also open."},
     ]},
    {"elig": "band-otherhealth", "id": "otherhealth", "title": "Other health license",
     "ex": "Registered nurse, pharmacist, licensed massage therapist. No diagnosis or therapy scope.",
     "routes": [
         {"permit": "dc", "state": "nopath", "line": "Needs a diagnosing license."},
         {"permit": "prac", "state": "nopath", "line": "Needs a therapy license."},
         {"permit": "fac", "state": "open", "line": "Direct route."},
     ]},
    {"elig": "band-outofstate", "id": "elsewhere", "title": "Trained outside New Mexico",
     "ex": "Out-of-state, international, or Tribal, Pueblo, and Nation programs NMDOH approves.",
     "routes": [
         {"permit": "recip", "state": "recip",
          "line": "Enter by reciprocity, as Practitioner or Facilitator."},
         {"permit": "dc", "state": "part",
          "line": "The published rule names certifying clinicians as eligible under 7.35.3.10, but the "
                  "application items listed there are for practitioners and facilitators. Unresolved in "
                  "the draft."},
     ]},
]

STATE = {
    "open": {"tag": "open", "cls": "isopen", "lab": "Open"},
    "part": {"tag": "part", "cls": "part", "lab": "Partial"},
    "recip": {"tag": "recip", "cls": "recip", "lab": "By reciprocity"},
    "nopath": {"tag": "nopath", "cls": "nopath", "lab": "No current path"},
}


# ---------------------------------------------------------------------------
# Rendering. Nothing here breaks a line inside an element: newlines separate
# block-level siblings only, so no whitespace is added where it would render.
# ---------------------------------------------------------------------------

def live_routes(st):
    """The permits this starting license opens, in the order they are shown."""
    return [d["permit"] for d in st["routes"] if d["state"] != "nopath"]


def step_html(step, n):
    cls = "s-open" if step["s"] == "open" else ("s-chal" if step["s"] == "chal" else "s-set")
    flag = ""
    if step["s"] == "open":
        flag = '<span class="flag open">&#9670; ' + step["flag"] + "</span>"
    if step["s"] == "chal":
        flag = '<span class="flag chal">&#9660; ' + step["flag"] + "</span>"
    why = '<p class="why">' + step["why"] + "</p>" if step.get("why") else ""
    metz = ('<p class="metz"><span class="mz">If the committee recommendation is adopted</span>'
            + step["metz"] + "</p>") if step.get("metz") else ""
    model = ('<p class="model"><a href="hours.html">The working model of these hours</a></p>'
             if step.get("model") else "")
    return (f'<li class="step {cls}"><span class="num">{n}</span><div class="card">'
            f'<p class="txt">{step["t"]}</p>{flag}{why}{metz}{model}'
            f'<p class="src">{step.get("src", "")}</p></div></li>')


def journey_html(key, indent):
    pad = " " * indent
    items = "\n".join(pad + "  " + step_html(s, i + 1)
                      for i, s in enumerate(PERMITS[key]["steps"]))
    return pad + '<ol class="steps">\n' + items + "\n" + pad + "</ol>"


def route_html(d, active):
    S = STATE[d["state"]]
    label = ("Practitioner or Facilitator, by reciprocity" if d["permit"] == "recip"
             else PERMITS[d["permit"]]["name"])
    inner = (f'<div class="rb"><p class="rn">{label} '
             f'<span class="tag {S["tag"]}">{S["lab"]}</span></p>'
             f'<p class="rl">{d["line"]}</p></div>')
    if d["state"] == "nopath":
        return '<div class="route nopath">' + inner + "</div>"
    sel = d["permit"] == active
    return ('<button type="button" class="route ' + S["cls"] + (" sel" if sel else "")
            + '" data-k="' + d["permit"] + '" aria-pressed="' + ("true" if sel else "false")
            + '">' + inner + '<span class="rgo">'
            + ("Shown below" if sel else "View pathway &darr;") + "</span></button>")


def eligref_html(st):
    cs = (', and the certifying-clinician verdict turns on the '
          '<a href="cs-number.html">controlled-substance number</a>') if st.get("cs") else ""
    return ('These verdicts summarize the <a href="eligibility.html#' + st["elig"] + '">rows for this '
            'group in the eligibility tables</a>' + cs + ".")


def jhead_html(st, key):
    title = ("Pathway by reciprocity: Practitioner or Facilitator" if key == "recip"
             else "Pathway to the " + PERMITS[key]["name"] + " permit")
    route = next((r for r in st["routes"] if r["permit"] == key), None)
    line = '<p class="routeline">' + route["line"] + "</p>" if route else ""
    return "<h3>" + title + "</h3>" + line


def panel_html(st):
    """One starting license: the heading, the verdicts, the eligibility line, and
    the step list of every route it opens."""
    keys = live_routes(st)
    active = keys[0]
    out = [f'      <div class="youare" data-start="{st["id"]}">'
           f'<p class="k">Starting license</p><h2>{st["title"]}</h2></div>',
           f'      <div class="routes" data-start="{st["id"]}">']
    for d in st["routes"]:
        out.append("        " + route_html(d, active))
    out.append("      </div>")
    out.append(f'      <p class="eligref" data-start="{st["id"]}">{eligref_html(st)}</p>')
    out.append(f'      <div class="journeywrap" data-start="{st["id"]}" data-active="{active}">')
    for key in keys:
        out.append(f'        <div class="jhead" data-k="{key}">{jhead_html(st, key)}</div>')
        out.append(f'        <div class="jholder" data-k="{key}">')
        out.append(journey_html(key, 10))
        out.append("        </div>")
    out.append("      </div>")
    return "\n".join(out)


def render_picker():
    rows = []
    for i, st in enumerate(STARTS):
        on = " on" if i == 0 else ""
        rows.append(f'        <button type="button" class="start{on}" data-start="{st["id"]}">'
                    f'<span class="stt">{st["title"]}</span>'
                    f'<span class="stex">{st["ex"]}</span></button>')
    return ('      <div class="starts" id="starts">\n' + "\n".join(rows) + "\n      </div>")


def render_panels():
    return (f'    <div id="panel" data-current="{STARTS[0]["id"]}">\n'
            + "\n".join(panel_html(st) for st in STARTS)
            + "\n    </div>")


def render_css():
    """The rules that narrow the page to one starting license and one route.

    Every rule is gated on .js, which the one-line script in the head adds
    before the page paints. Without JavaScript no rule applies, every panel and
    every step stays in view, and browser find reaches all of it."""
    lines = ["  /* Every panel and every route's steps are in the page. These rules narrow it to",
             "     the selected starting license and the selected route, and they apply only when",
             "     JavaScript has marked the document. Without it, nothing is hidden. */"]
    for st in STARTS:
        i = st["id"]
        lines.append(f'  .js #panel[data-current="{i}"] [data-start]:not([data-start="{i}"])'
                     "{display:none;}")
    for key in sorted({k for st in STARTS for k in live_routes(st)}):
        lines.append(f'  .js .journeywrap[data-active="{key}"] [data-k]:not([data-k="{key}"])'
                     "{display:none;}")
    return "\n".join(lines)


BLOCKS = [
    ("/* pathways panels: generated by tools/sync-pathways.py, do not hand-edit */",
     "/* /pathways panels */", render_css),
    ("<!-- pathways picker: generated by tools/sync-pathways.py, do not hand-edit -->",
     "<!-- /pathways picker -->", render_picker),
    ("<!-- pathways panels: generated by tools/sync-pathways.py, do not hand-edit -->",
     "<!-- /pathways panels -->", render_panels),
]


def render(src):
    """Return pathways.html with all three generated regions rewritten."""
    for open_mark, close_mark, build in BLOCKS:
        pattern = re.compile(r"(?m)^([ \t]*)" + re.escape(open_mark) + r".*?"
                             + re.escape(close_mark), re.S)
        m = pattern.search(src)
        if not m:
            raise SystemExit(f"tools/sync-pathways.py: pathways.html has no {open_mark} block")
        pad = m.group(1)
        replacement = pad + open_mark + "\n" + build() + "\n" + pad + close_mark
        src = pattern.sub(lambda _: replacement, src, count=1)
    return src


def stale():
    """True when pathways.html no longer matches the data here."""
    src = open(PAGE).read()
    return render(src) != src


def main():
    check = "--check" in sys.argv
    src = open(PAGE).read()
    new = render(src)
    steps = sum(len(PERMITS[k]["steps"]) for st in STARTS for k in live_routes(st))
    tally = "\n%d starting licenses, %d routes, %d steps." % (
        len(STARTS), sum(len(live_routes(st)) for st in STARTS), steps)
    if new == src:
        print("in sync     pathways.html")
        print(tally)
        return 0
    if check:
        print("STALE       pathways.html")
        print("\npathways.html is stale. Run without --check to fix.")
        return 1
    open(PAGE, "w").write(new)
    print("updated     pathways.html")
    print(tally)
    return 0


if __name__ == "__main__":
    sys.exit(main())

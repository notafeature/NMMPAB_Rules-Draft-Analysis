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

The selection is also in the URL. The location hash carries #start=<id>, or
#start=<id>&permit=<key> when the shown route is not the starting license's
first, so the visible state is always a shareable address. Three parts carry
it, and the two that know the valid ids and keys are generated here so they
cannot drift from the data:

    the head script, hand-held in the page, veils the picker and the panels
    with one class when the hash looks like a state, so a shared link never
    flashes the default before the state applies;
    a script this file writes directly after the panels applies the hash
    against what the panels actually hold, then lifts the veil; a value the
    panels do not hold falls through to the default with no error;
    the foot script, hand-held in the page, rewrites the hash with
    history.replaceState on every selection.

Without JavaScript the hash is inert: the veil class is never added, nothing
is narrowed, and the page reads in full as before.

Three regions of docs/pathways.html are generated, each between its own markers,
and nothing outside them is touched: the selection rules in the page's
stylesheet, the picker at #starts, and the panels at #panel with the
state-applying script beside them.

tools/check-site.py imports this module and calls stale() to fail the build if
the page no longer matches the data here.

Usage:
    python3 tools/sync-pathways.py           # write the three blocks into the page
    python3 tools/sync-pathways.py --check   # exit 1 if pathways.html is stale
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import partlib
PART = partlib.current_part()
DOCS = partlib.docs_dir(PART)
PAGE = os.path.join(DOCS, "pathways.html")

# Not every Part has routes. A Part with no pathways data has no pathways.html,
# and this tool reports that and does nothing.
HAS_PATHWAYS = partlib.has_data(PART, "sync-pathways")
if HAS_PATHWAYS:
    partlib.load_data(PART, "sync-pathways", globals())
else:
    PERMITS, STARTS, STATE = {}, [], {}



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
    out.append(f'      <div class="journeywrap" data-start="{st["id"]}" data-active="{active}" data-default="{active}">')
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
            + "\n    </div>\n"
            + state_script())


def state_script():
    """The script that applies the location hash to the panels.

    It sits directly after the panels so it runs the moment they exist, before
    anything below them has parsed, which is what keeps a shared link from
    flashing the default view. It validates the hash against the panels
    themselves rather than against a second copy of the ids and keys: a start
    is real when a journey wrap carries it, a permit is real for that start
    when the wrap holds its journey head. Anything else falls through to the
    default silently. The last line always lifts the veil the head script may
    have raised, whether or not a state applied."""
    return """    <script>
    (function(){
      var h=document.documentElement;
      try{
        var m=/^#start=([a-z]+)(?:&permit=([a-z]+))?$/.exec(location.hash);
        var panel=document.getElementById('panel');
        var wrap=m&&panel?panel.querySelector('.journeywrap[data-start="'+m[1]+'"]'):null;
        if(wrap){
          panel.setAttribute('data-current',m[1]);
          var bs=document.querySelectorAll('#starts button.start');
          for(var i=0;i<bs.length;i++) bs[i].classList.toggle('on',bs[i].getAttribute('data-start')===m[1]);
          if(m[2]&&wrap.querySelector('.jhead[data-k="'+m[2]+'"]')){
            wrap.setAttribute('data-active',m[2]);
            var rs=panel.querySelectorAll('.routes[data-start="'+m[1]+'"] button.route');
            for(var j=0;j<rs.length;j++){
              var sel=rs[j].getAttribute('data-k')===m[2];
              rs[j].classList.toggle('sel',sel);
              rs[j].setAttribute('aria-pressed',sel?'true':'false');
              var go=rs[j].querySelector('.rgo');
              if(go) go.innerHTML=sel?'Shown below':'View pathway &darr;';
            }
          }
        }
      }catch(e){}
      h.classList.remove('hs');
    })();
    </script>"""


def render_css():
    """The rules that narrow the page to one starting license and one route.

    Every rule is gated on .js, which the one-line script in the head adds
    before the page paints. Without JavaScript no rule applies, every panel and
    every step stays in view, and browser find reaches all of it."""
    lines = ["  /* Every panel and every route's steps are in the page. These rules narrow it to",
             "     the selected starting license and the selected route, and they apply only when",
             "     JavaScript has marked the document. Without it, nothing is hidden. */",
             "  /* When the head script sees a state in the location hash it adds hs, and the",
             "     script after the panels applies the state and removes it, so a shared link",
             "     shows the arrived-at selection rather than a flash of the default. */",
             "  .js.hs #starts,.js.hs #panel{visibility:hidden;}"]
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
    if not HAS_PATHWAYS:
        return False
    src = open(PAGE).read()
    return render(src) != src


def main():
    check = "--check" in sys.argv
    if not HAS_PATHWAYS:
        print(f"Part {PART} has no routes; nothing to write.")
        return 0
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

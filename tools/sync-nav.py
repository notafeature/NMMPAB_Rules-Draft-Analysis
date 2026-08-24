#!/usr/bin/env python3
"""Keep the primary nav byte-identical across every page in docs/.

The site is hand-written static HTML with no build step, so the nav block is
physically duplicated in each page. The house rule is that it must be identical
everywhere, apart from the aria-current marker on the current page. This script
is the enforcement: edit the data below, run it, and every page gets the same
block.

Three things live here and nowhere else:

1. NAMES. The canonical name of every page. The nav label, the <title>, and the
   H1 all read the same words, so a reader never has to re-orient after a
   navigation. tools/check-site.py reads NAMES to check that agreement.

2. MENU_DOCUMENTS. The membership of the Documents dropdown. The contract is
   stated in the DOCUMENTS_CONTRACT constant below and enforced by check-site.py,
   which reads this list rather than carrying its own copy.

3. The nav markup itself, and the script that drives it.

Usage:
    python3 tools/sync-nav.py           # rewrite every page, report changes
    python3 tools/sync-nav.py --check   # exit 1 if any page is out of sync
"""
import glob
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

# The canonical name of each page. One name per page, used as the nav label, as
# the <title> before the suffix, and as the H1. Changing a name here is half the
# job: the <title> and the H1 are in the page and are checked, not written, by
# this tool.
NAMES = {
    "index": "Where things stand",
    "rule": "The published rule",
    "record": "Meetings and filings",
    "hours": "The training hours",
    "recommendation": "The committee recommendation",
    "comment": "Comment",
    "about": "How this site is built",
    "pathways": "Routes to a permit",
    "eligibility": "Which licenses qualify",
    "cs-number": "The controlled-substance number",
    "specialization": "Specialized domains",
    "deferred": "What a practicum change touches",
    "changes": "Section by section",
    "training-hours-record": "The training-hours record",
}

# Every page title ends with this, so a search result or a browser tab names the
# rulemaking as well as the page.
TITLE_SUFFIX = "7.35.3 NMAC Training and Education"

# What the Documents dropdown carries, and why. A reader opening this menu is
# looking for a document, not for a history of documents; the register at
# record.html#documents holds the history.
DOCUMENTS_CONTRACT = (
    "The register, the current operative text, and the documents of the most "
    "recent meeting or filing. Nothing else. The list changes when the document "
    "chain changes, and at no other time."
)

# The dropdown's members, in the order they appear. The register comes first,
# then the operative text, then that meeting's or filing's own documents.
# check-site.py reads this list, so the menu and the check cannot disagree.
MENU_DOCUMENTS = [
    {
        "href": "record.html#documents",
        "label": "All documents",
        "sub": "The register: what each one is and whether it is current",
    },
    {
        "href": "documents/rules-draft-2026-07-23-published.pdf",
        "label": "Last published text &middot; July 23",
        "sub": "July 23, set aside; the last published text",
    },
    {
        "href": "documents/NMMPAB-2026-07-17-board-transcript.pdf",
        "label": "Transcript &middot; July 17 board",
        "sub": "Unofficial, no speaker attribution",
    },
    {
        "href": "documents/NMMPAB-2026-07-17-committee-transcript.pdf",
        "label": "Transcript &middot; July 17 committee",
        "sub": "Unofficial, no speaker attribution",
    },
    {
        "href": "documents/metz-recommendations-2026-07-17.pdf",
        "label": "Recommendations &middot; July 17",
        "sub": "Dr. Anne Metz, presented to the committee",
    },
]

# The nav groups. Each entry is (href, data-nav slug or None, sub-line). The
# label comes from NAMES where a slug is given, so a name is written once.
GROUPS = [
    ("start", "Start here", [
        ("index.html", "index", "What is open, what is settled, what is next"),
        ("index.html#directory", None, "Every page, in one list", "What is on this site"),
        ("about.html", "about", "Sources, method, and how to report an error"),
    ]),
    ("provider", "Becoming a provider", [
        ("pathways.html", "pathways", "Pick where you start; the route to each permit"),
        ("eligibility.html", "eligibility", "The license-by-permit tables"),
        ("hours.html", "hours", "The working model of the deferred quantities"),
        ("specialization.html", "specialization", "An overlay on a core permit, not in the rule"),
        ("cs-number.html", "cs-number", "The certifying-clinician requirement"),
        ("deferred.html", "deferred", "Every provision a practicum change reaches"),
    ]),
    ("rule", "The rule", [
        ("rule.html", "rule", "All twenty-eight sections, verbatim, annotated"),
        ("changes.html", "changes", "All 104 provisions, and what changed"),
        ("recommendation.html", "recommendation", "The August 21 position, in the department's hands"),
        ("comment.html", "comment", "The rule hearing, anticipated early October, and the input channel"),
    ]),
    ("record", "The record", [
        ("record.html", "record", "The dated chain, newest first"),
        ("record.html#documents", None, "The register: every document and its status", "All documents"),
        ("training-hours-record.html", "training-hours-record",
         "July 9 and 17, benchmarks, and community comment"),
    ]),
]

# The call to action sits between the groups and the Documents dropdown. It
# carries no data-nav, so the active-page marker stays on the dropdown entry.
CTA = ("comment.html", "Comment")


def build_nav(page=None):
    """The nav block, with aria-current on `page` if that page is in it."""
    lines = ['    <nav class="tnav" id="tnav" aria-label="Primary">']
    for key, summary, entries in GROUPS:
        lines.append(f'      <details class="tdrop navgrp" data-navgrp="{key}">')
        lines.append(f'        <summary>{summary} <span class="caret">&#9662;</span></summary>')
        lines.append('        <div class="tdrop-menu">')
        for entry in entries:
            href, slug, sub = entry[0], entry[1], entry[2]
            label = entry[3] if len(entry) > 3 else NAMES[slug]
            cur = ' aria-current="page"' if slug and slug == page else ""
            nav = f' data-nav="{slug}"' if slug else ""
            lines.append(
                f'          <a href="{href}"{cur}{nav}>{label}'
                f'<span class="sub">{sub}</span></a>'
            )
        lines.append("        </div>")
        lines.append("      </details>")
    lines.append(f'      <a href="{CTA[0]}" class="navcta">{CTA[1]}</a>')
    lines.append('      <details class="tdrop navgrp" data-navgrp="docs">')
    lines.append('        <summary>Documents <span class="caret">&#9662;</span></summary>')
    lines.append('        <div class="tdrop-menu">')
    for d in MENU_DOCUMENTS:
        tab = "" if d["href"].endswith(".html") or "#" in d["href"] else \
            ' target="_blank" rel="noopener"'
        lines.append(
            f'          <a href="{d["href"]}"{tab}>{d["label"]}'
            f'<span class="sub">{d["sub"]}</span></a>'
        )
    lines.append("        </div>")
    lines.append("      </details>")
    lines.append("    </nav>")
    return "\n".join(lines)


NAV_JS = """<script id="navjs">
(function(){
  var nav=document.getElementById('tnav');
  if(!nav) return;
  var b=document.getElementById('hbtn');
  if(b){ b.addEventListener('click', function(){ var o=nav.classList.toggle('open'); b.setAttribute('aria-expanded', o?'true':'false'); }); }
  var f=(location.pathname.split('/').pop()||'index.html').toLowerCase();
  var cur=f.replace('.html','')||'index';
  var el=document.querySelector('.tnav [data-nav="'+cur+'"]');
  if(el){ el.classList.add('on'); var g=el.closest('.navgrp'); if(g){ var s=g.querySelector('summary'); if(s) s.classList.add('on'); } }

  // Dropdowns are native <details>, which stay open until their own summary is
  // clicked again. On a nav that is wrong: clicking anywhere else should close
  // them. Close on outside click, on Escape, and when a sibling opens.
  var groups=[].slice.call(nav.querySelectorAll('details.navgrp'));
  if(!groups.length) return;
  function closeAll(except){
    groups.forEach(function(d){ if(d!==except) d.open=false; });
  }
  groups.forEach(function(d){
    d.addEventListener('toggle', function(){ if(d.open) closeAll(d); });
  });
  document.addEventListener('click', function(e){
    if(!nav.contains(e.target)) closeAll(null);
  });
  document.addEventListener('keydown', function(e){
    if(e.key==='Escape'||e.key==='Esc'){
      var open=groups.filter(function(d){ return d.open; });
      if(open.length){ closeAll(null); var s=open[0].querySelector('summary'); if(s) s.focus(); }
    }
  });
  // Choosing a destination should not leave the menu hanging open behind it.
  nav.addEventListener('click', function(e){
    if(e.target.closest('.tdrop-menu a')) closeAll(null);
  });
})();
</script>"""

PATTERN = re.compile(
    r'^    <nav class="tnav" id="tnav" aria-label="Primary">.*?^    </nav>', re.S | re.M)
JS_PATTERN = re.compile(r'<script id="navjs">.*?</script>', re.S)


def main():
    check = "--check" in sys.argv
    changed, missing, ok = [], [], []

    for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        name = os.path.basename(path)
        src = open(path).read()
        if 'http-equiv="refresh"' in src:
            # a redirect stub at a retired address; not this tool's surface
            continue
        if not PATTERN.search(src) or not JS_PATTERN.search(src):
            missing.append(name)
            continue
        nav = build_nav(name[:-5])
        new = PATTERN.sub(lambda _: nav, src, count=1)
        new = JS_PATTERN.sub(lambda _: NAV_JS, new, count=1)
        if new == src:
            ok.append(name)
        elif check:
            changed.append(name)
        else:
            open(path, "w").write(new)
            changed.append(name)

    for name in changed:
        print(("OUT OF SYNC " if check else "updated     ") + name)
    for name in ok:
        print("in sync     " + name)
    for name in missing:
        print("NO NAV      " + name)

    if missing:
        print("\n%d page(s) have no recognizable nav block." % len(missing))
        return 1
    if check and changed:
        print("\n%d page(s) out of sync. Run without --check to fix." % len(changed))
        return 1
    print("\n%d page(s), nav identical." % (len(changed) + len(ok)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import partlib
PART = partlib.current_part()
DOCS = partlib.docs_dir(PART)
# Every page title ends with this, so a search result or a browser tab names the
# rulemaking as well as the page.
TITLE_SUFFIX = partlib.suffix(PART)

# What the Documents dropdown carries, and why. A reader opening this menu is
# looking for a document, not for a history of documents; the register at
# record.html#documents holds the history.
DOCUMENTS_CONTRACT = (
    "The register, the current operative text, and the documents of the most "
    "recent meeting or filing. Nothing else. The list changes when the document "
    "chain changes, and at no other time."
)

partlib.load_data(PART, "sync-nav", globals())


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

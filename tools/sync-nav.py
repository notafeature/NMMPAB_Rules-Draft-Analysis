#!/usr/bin/env python3
"""Keep the primary nav byte-identical across every page in docs/.

The site is hand-written static HTML with no build step, so the nav block is
physically duplicated in each page. The house rule is that it must be identical
everywhere. This script is the enforcement: edit NAV below, run it, and every
page gets the same block.

Usage:
    python3 tools/sync-nav.py           # rewrite every page, report changes
    python3 tools/sync-nav.py --check   # exit 1 if any page is out of sync
"""
import glob
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

NAV = """      <nav class="tnav" id="tnav" aria-label="Primary">
        <details class="tdrop navgrp" data-navgrp="ov">
          <summary>Overview <span class="caret">&#9662;</span></summary>
          <div class="tdrop-menu">
            <a href="index.html" data-nav="index">Where things stand<span class="sub">What is open, what is settled, what is next</span></a>
            <a href="guide.html" data-nav="guide">What is on this site<span class="sub">Which page holds what</span></a>
          </div>
        </details>
        <details class="tdrop navgrp" data-navgrp="req">
          <summary>Requirements <span class="caret">&#9662;</span></summary>
          <div class="tdrop-menu">
            <a href="deferred.html" data-nav="deferred">Practicum requirements<span class="sub">Every provision a practicum change has to touch</span></a>
            <a href="pathways.html" data-nav="pathways">Provider routes<span class="sub">Routes to each permit by starting license</span></a>
            <a href="eligibility.html" data-nav="eligibility">Who can qualify<span class="sub">Which licenses map to which permit</span></a>
            <a href="hours.html" data-nav="hours">Training hours<span class="sub">Didactic, practicum, and specialization</span></a>
            <a href="cs-number.html" data-nav="cs-number">CS number<span class="sub">The certifying-clinician access point</span></a>
          </div>
        </details>
        <details class="tdrop navgrp" data-navgrp="record">
          <summary>The record <span class="caret">&#9662;</span></summary>
          <div class="tdrop-menu">
            <a href="changes.html" data-nav="changes">The draft, section by section<span class="sub">All 104 provisions, and what changed</span></a>
            <a href="history.html" data-nav="history">History<span class="sub">The dated chain, newest first</span></a>
            <a href="about.html" data-nav="about">How this site is built<span class="sub">Sources, method, and how to report an error</span></a>
          </div>
        </details>
        <a href="input.html" data-nav="input" class="navcta">Community input</a>
        <details class="tdrop navgrp" data-navgrp="docs">
          <summary>Documents <span class="caret">&#9662;</span></summary>
          <div class="tdrop-menu">
            <a href="documents.html" data-nav="documents">All documents<span class="sub">The register: what each one is and whether it is current</span></a>
            <a href="documents/rules-draft-2026-07-23-published.pdf" target="_blank" rel="noopener">Published rule &middot; July 23<span class="sub">The proposed rule going to the August 28 hearing</span></a>
            <a href="documents/NMMPAB-2026-07-17-board-transcript.pdf" target="_blank" rel="noopener">Transcript &middot; July 17 board<span class="sub">Unofficial, no speaker attribution</span></a>
            <a href="documents/NMMPAB-2026-07-17-committee-transcript.pdf" target="_blank" rel="noopener">Transcript &middot; July 17 committee<span class="sub">Unofficial, no speaker attribution</span></a>
            <a href="documents/metz-recommendations-2026-07-17.pdf" target="_blank" rel="noopener">Recommendations &middot; July 17<span class="sub">Dr. Anne Metz, presented to the committee</span></a>
          </div>
        </details>
      </nav>"""

NAV_JS = """<script id="navjs">
(function(){
  var f=(location.pathname.split('/').pop()||'index.html').toLowerCase();
  var cur=f.replace('.html','')||'index';
  var el=document.querySelector('.tnav [data-nav="'+cur+'"]');
  if(el){ el.classList.add('on'); var g=el.closest('.navgrp'); if(g){ var s=g.querySelector('summary'); if(s) s.classList.add('on'); } }

  // Dropdowns are native <details>, which stay open until their own summary is
  // clicked again. On a nav that is wrong: clicking anywhere else should close
  // them. Close on outside click, on Escape, and when a sibling opens.
  var nav=document.getElementById('tnav');
  if(!nav) return;
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

PATTERN = re.compile(r'      <nav class="tnav" id="tnav" aria-label="Primary">.*?\n      </nav>', re.S)
JS_PATTERN = re.compile(r'<script id="navjs">.*?</script>', re.S)


def main():
    check = "--check" in sys.argv
    changed, missing, ok = [], [], []

    for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        name = os.path.basename(path)
        src = open(path).read()
        if not PATTERN.search(src) or not JS_PATTERN.search(src):
            missing.append(name)
            continue
        new = PATTERN.sub(lambda _: NAV, src, count=1)
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

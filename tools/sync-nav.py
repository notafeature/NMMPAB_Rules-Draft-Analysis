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
        <a href="index.html" data-nav="index">Overview</a>
        <details class="tdrop navgrp" data-navgrp="req">
          <summary>Requirements <span class="caret">&#9662;</span></summary>
          <div class="tdrop-menu">
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

PATTERN = re.compile(r'      <nav class="tnav" id="tnav" aria-label="Primary">.*?\n      </nav>', re.S)


def main():
    check = "--check" in sys.argv
    changed, missing, ok = [], [], []

    for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        name = os.path.basename(path)
        src = open(path).read()
        if not PATTERN.search(src):
            missing.append(name)
            continue
        new = PATTERN.sub(lambda _: NAV, src, count=1)
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

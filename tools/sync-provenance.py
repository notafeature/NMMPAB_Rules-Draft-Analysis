#!/usr/bin/env python3
"""Keep the provenance block identical and current across every page in docs/.

Two things a reader needs and the site did not have:

1. The document chain. Four successive documents govern this subject. Each
   supersedes the one before it. A reader looking at a number on any page
   should be able to walk back and see where it came from and what changed at
   each step, without that history sprawling across the page.

2. A per-page revision log. What was changed on this page, and when. Only
   index.html had one, buried in its footer.

Both live in a single collapsed <details> block at the foot of every page:
zipped up by default, walkable when opened.

CHAIN is identical on every page. REVISIONS is per page, newest first.

Usage:
    python3 tools/sync-provenance.py           # write into every page
    python3 tools/sync-provenance.py --check   # exit 1 if any page is stale
"""
import glob
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")

# The document chain. Newest last. Identical on every page.
CHAIN = [
    {
        "date": "June 12, 2026",
        "name": "Committee recommendation",
        "file": "documents/recommendation-2026-06-12.pdf",
        "what": "The Training and Education Committee's own recommendation. Origin of the 100 and 120 practicum hours and the 20 supervisory hours. The Advisory Board voted 3-2 on June 26 to accept it, setting three items aside.",
    },
    {
        "date": "June 25, 2026",
        "name": "Department draft",
        "file": "documents/rules-draft-2026-06-25.pdf",
        "what": "The department's first rules-style draft of the same subject. Introduced the module test-out mechanism that every later draft keeps, and the first reciprocity provision, which the June 12 recommendation did not contain.",
    },
    {
        "date": "July 9, 2026",
        "name": "Board-meeting draft",
        "file": "documents/rules-draft-2026-07-09.pdf",
        "what": "The draft the Advisory Board went through section by section on July 9. Used placeholder section numbers shown as 7.35.3.X. Set the shared didactic module at 25 hours. Carried the older waiver dates of December 31, 2026 and June 30, 2027, which the board extended by vote that day without the text being updated.",
    },
    {
        "date": "July 23, 2026",
        "name": "Published proposed rule",
        "file": "documents/rules-draft-2026-07-23-published.pdf",
        "what": "The department's published proposed rule, and the text going to the August 28 hearing. First version with final section numbering, 7.35.3.1 through .28. Raised the shared didactic module from 25 hours to 30 and added three curriculum topics. Carried the 100 and 120 practicum hours forward unchanged, six days after the board voted 7-0 to send those hours back to committee. Wrote both waiver dates as December 31, 2027. Added a rule that the practicum may not begin before half the didactic and all simulated patient hours are complete.",
        "current": True,
    },
]

# Per-page revision entries, newest first. Keep each one specific: what changed,
# not that something changed.
REVISIONS = {
    "index": [
        ("July 25, 2026", "Clarified that the published rule contains no committee recommendation on the training hours because the committee has not delivered one to the department. Brought current to the July 23 published rule. Headline changed from \"The three open items\" to \"The rule is published\". Removed live-meeting language (\"this morning, July 17\", \"the committee meets at 1 PM today\") and a link to a live-notes anchor that no longer exists. Item 3 previously said the reciprocity extension was \"not yet written in\", which was true of the July 9 draft and is no longer true. All three lineage blocks now compare the June 12 recommendation against the published rule."),
        ("July 17, 2026", "Updated to the July 17 full Advisory Board meeting. The board voted 7-0 to defer the practicum and didactic hours to the Training and Education Committee."),
        ("July 10, 2026", "Parallel working drafts reconciled into this page. The July 9 meeting description corrected: it was an Advisory Board meeting, and the chair barred formal votes only after the scheduled adjournment."),
        ("July 9, 2026", "Updated to the outcome of the July 9 Advisory Board meeting. Reciprocity: both waiver deadlines extended to December 31, 2027. Practicum and didactic hours: tabled."),
    ],
    "hours": [
        ("July 25, 2026", "Brought current to the July 23 published rule. The page had no Updated date at all and was written in live-blog present tense from July 17: the Dr. Anne Metz presentation carried an \"In progress\" tag and a section was headed \"Open questions for July 17\". Role cards updated from the July 9 numbers to the published ones. Corrected two live errors: the in-state bridge deadline read June 30, 2027 and the reciprocity deadline read December 31, 2026, and both are December 31, 2027 in the published rule. Added a \"What changed on July 23\" summary."),
        ("July 17, 2026", "Added the live log of the July 17 Training and Education Committee meeting, including the Dr. Anne Metz presentation."),
    ],
    "history": [
        ("July 25, 2026", "Two entries added: the July 23 publication of the proposed rule, and the July 17 afternoon Training and Education Committee meeting, which the page had omitted entirely while carrying the morning board meeting. The July 17 board entry is now labelled morning so the two are distinguishable. \"What is next\" replaced its stale July 17 contents with August 14, August 21, and the August 28 hearing. The \"How this process works\" explainer was moved out of the middle of the chronology, where it split the timeline into two lists, and now sits above it."),
        ("July 17, 2026", "Added the July 17 Advisory Board meeting: the 7-0 deferral, the department keeping the controlled-substance number, and the revised certifying-clinician exam language."),
    ],
    "documents": [
        ("July 25, 2026", "Page created. A register of every source document with what it is, when it landed, whether it is current or superseded, page count, size, and a direct download, plus a section naming the documents this site does not have."),
    ],
}

CSS = """  .prov{margin:26px 0 0; border:1px solid var(--border-strong); border-radius:12px; background:var(--surface); overflow:hidden;}
  .prov>summary{list-style:none; cursor:pointer; padding:13px 16px; display:flex; align-items:center; gap:10px; font-size:13.5px; color:var(--text-muted); background:var(--surface-2);}
  .prov>summary::-webkit-details-marker{display:none;}
  .prov>summary:hover{color:var(--text);}
  .prov .provsum{font-weight:650;}
  .prov .provchev{margin-left:auto; font-size:11px; transition:transform .15s;}
  .prov[open] .provchev{transform:rotate(90deg);}
  .provbody{padding:4px 16px 18px;}
  .provsec{margin-top:16px;}
  .provk{font-size:11px; font-weight:700; letter-spacing:.09em; text-transform:uppercase; color:var(--accent); margin:0 0 10px;}
  .chain{list-style:none; margin:0; padding:0; counter-reset:ch;}
  .chain li{position:relative; padding:0 0 14px 26px; border-left:2px solid var(--border-strong); margin-left:5px;}
  .chain li:last-child{border-left-color:transparent; padding-bottom:2px;}
  .chain li::before{content:""; position:absolute; left:-6px; top:4px; width:10px; height:10px; border-radius:50%; background:var(--border-strong); border:2px solid var(--surface);}
  .chain li.cur::before{background:var(--accent);}
  .chain .cd{font-size:12px; font-family:var(--mono); color:var(--text-faint);}
  .chain .cn{font-size:14.5px; font-weight:650; color:var(--text); margin:1px 0 0;}
  .chain .cw{font-size:13.5px; color:var(--text-muted); line-height:1.55; margin:4px 0 0;}
  .chain .curflag{display:inline-block; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.05em; color:var(--agree); background:var(--agree-bg); border:1px solid var(--agree-border); border-radius:20px; padding:1px 8px; margin-left:7px; vertical-align:1px;}
  .revs{list-style:none; margin:0; padding:0;}
  .revs li{font-size:13.5px; color:var(--text-muted); line-height:1.55; padding:8px 0; border-top:1px solid var(--border);}
  .revs li:first-child{border-top:none; padding-top:0;}
  .revs b{color:var(--text); font-weight:650;}
"""

MARK = "<!-- provenance: generated by tools/sync-provenance.py, do not hand-edit -->"
BLOCK_RE = re.compile(re.escape(MARK) + r".*?" + re.escape("<!-- /provenance -->"), re.S)
CSS_MARK = "/* provenance block */"
CSS_RE = re.compile(re.escape(CSS_MARK) + r".*?" + re.escape("/* /provenance block */"), re.S)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(page):
    rows = []
    for c in CHAIN:
        cur = ' class="cur"' if c.get("current") else ""
        flag = '<span class="curflag">Current state of truth</span>' if c.get("current") else ""
        rows.append(
            f'          <li{cur}>\n'
            f'            <p class="cd">{c["date"]}</p>\n'
            f'            <p class="cn"><a href="{c["file"]}" target="_blank" rel="noopener">{esc(c["name"])}</a>{flag}</p>\n'
            f'            <p class="cw">{esc(c["what"])}</p>\n'
            f'          </li>'
        )
    chain = "\n".join(rows)

    revs = REVISIONS.get(page)
    if revs:
        items = "\n".join(
            f'          <li><b>{d}</b> {esc(t)}</li>' for d, t in revs
        )
        revblock = (
            '        <div class="provsec">\n'
            '          <p class="provk">Revisions to this page</p>\n'
            '          <ul class="revs">\n' + items + "\n"
            "          </ul>\n"
            "        </div>\n"
        )
    else:
        revblock = ""

    return (
        f"{MARK}\n"
        '      <details class="prov">\n'
        '        <summary><span class="provsum">Provenance: the document chain and this page&rsquo;s revisions</span><span class="provchev">&#9656;</span></summary>\n'
        '        <div class="provbody">\n'
        '        <div class="provsec">\n'
        '          <p class="provk">The document chain, oldest first</p>\n'
        '          <ol class="chain">\n' + chain + "\n"
        "          </ol>\n"
        "        </div>\n"
        + revblock +
        "        </div>\n"
        "      </details>\n"
        "      <!-- /provenance -->"
    )


def main():
    check = "--check" in sys.argv
    changed, ok, missing = [], [], []

    for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        name = os.path.basename(path)
        page = name[:-5]
        src = open(path).read()
        anchor = '<div class="sitefoot">'
        if anchor not in src:
            missing.append(name)
            continue

        new = src
        # CSS
        css_block = CSS_MARK + "\n" + CSS + "  " + "/* /provenance block */"
        if CSS_RE.search(new):
            new = CSS_RE.sub(lambda _: css_block, new, count=1)
        else:
            new = new.replace("</style>\n<style id=\"navpass\">", css_block + "\n</style>\n<style id=\"navpass\">", 1)

        # Block
        block = build(page)
        if BLOCK_RE.search(new):
            new = BLOCK_RE.sub(lambda _: block, new, count=1)
        else:
            new = new.replace(anchor, block + "\n      " + anchor, 1)

        if new == src:
            ok.append(name)
        elif check:
            changed.append(name)
        else:
            open(path, "w").write(new)
            changed.append(name)

    for n in changed:
        print(("STALE       " if check else "updated     ") + n)
    for n in ok:
        print("in sync     " + n)
    for n in missing:
        print("NO ANCHOR   " + n)

    if missing:
        print("\n%d page(s) missing the sitefoot anchor." % len(missing))
        return 1
    if check and changed:
        print("\n%d page(s) stale. Run without --check to fix." % len(changed))
        return 1
    print("\n%d page(s), provenance identical." % (len(changed) + len(ok)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

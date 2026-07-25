#!/usr/bin/env python3
"""Render the permit-title variable in the amendment drafts.

The amendment drafts in amendments/ never write the permit title literally.
They use six tokens. This script substitutes them in one pass and writes a
rendered copy alongside each source file.

To change the permit title, change the six values in PERMIT_TITLE below and
re-run this script. Nothing else needs to be touched.

The current title is "practitioner", which is the title used in the proposed
rule published July 23, 2026. The term is defined in 7.35.2.7 NMAC, a
different part of Title 7, which 7.35.3.7 NMAC incorporates by reference.
Changing the title in these drafts does not change that definition; a title
change requires a separate amendment to 7.35.2.7 NMAC.

Usage:
    python3 tools/render-permit-title.py            # write rendered files
    python3 tools/render-permit-title.py --check    # exit 1 if rendered files are stale
"""

import sys
from pathlib import Path

PERMIT_TITLE = {
    "{{PT}}": "practitioner",
    "{{PTS}}": "practitioners",
    "{{PT_C}}": "Practitioner",
    "{{PTS_C}}": "Practitioners",
    "{{PT_UC}}": "PRACTITIONER",
    "{{PTS_UC}}": "PRACTITIONERS",
}

REPO_ROOT = Path(__file__).resolve().parent.parent

SOURCES = [
    "amendments/7.35.3.18-19-redline.md",
    "amendments/blocking-defects.md",
    "amendments/metz-crosswalk.md",
]

BANNER = (
    "<!-- GENERATED FILE. Do not edit. Source: {src}\n"
    "     Regenerate with: python3 tools/render-permit-title.py\n"
    "     Permit title rendered as: {title} -->\n\n"
)


def render(text):
    for token, value in PERMIT_TITLE.items():
        text = text.replace(token, value)
    return text


def unresolved(text):
    """Return tokens that look like permit-title tokens but were not substituted."""
    out = []
    i = 0
    while True:
        start = text.find("{{", i)
        if start == -1:
            return out
        end = text.find("}}", start)
        if end == -1:
            return out
        token = text[start:end + 2]
        if token not in PERMIT_TITLE:
            out.append(token)
        i = end + 2


def main():
    check = "--check" in sys.argv
    stale = []
    for rel in SOURCES:
        src = REPO_ROOT / rel
        if not src.exists():
            print("skip (missing): %s" % rel)
            continue
        raw = src.read_text(encoding="utf-8")
        bad = unresolved(raw)
        if bad:
            print("error: %s has unknown tokens: %s" % (rel, ", ".join(sorted(set(bad)))))
            return 1
        rendered = BANNER.format(src=rel, title=PERMIT_TITLE["{{PT}}"]) + render(raw)
        dest = src.with_name(src.stem + "-rendered" + src.suffix)
        if check:
            if not dest.exists() or dest.read_text(encoding="utf-8") != rendered:
                stale.append(str(dest.relative_to(REPO_ROOT)))
        else:
            dest.write_text(rendered, encoding="utf-8")
            print("wrote %s" % dest.relative_to(REPO_ROOT))
    if check and stale:
        print("stale rendered files: %s" % ", ".join(stale))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

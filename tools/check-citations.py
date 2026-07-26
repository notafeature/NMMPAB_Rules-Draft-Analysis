#!/usr/bin/env python3
"""Verify every citation on the site against the published rule.

Nine of the fifteen factual errors found in the July 25 audit were a citation
pointing at the wrong section or the wrong page. That is mechanically
detectable, and this is the detector.

Two checks:

  1. Page anchors. Every link to the published rule carries `#page=N`. The text
     of the link, or the sentence around it, usually names a section. If it
     does, the section must actually appear on page N of the PDF.

  2. Stated pages. Prose of the form "7.35.3.19 (A), p. 13" must agree with the
     section-to-page map built from the PDF itself.

Usage:
    python3 tools/check-citations.py           # report
    python3 tools/check-citations.py --quiet   # exit code only
Exit 1 if any citation is wrong.
"""
import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")
RULE = "rules-draft-2026-07-23-published.pdf"
RULE_PATH = os.path.join(DOCS, "documents", RULE)


def read_rule_pages():
    """Return {page_number: text}. pypdf's crypt provider imports cryptography,
    whose rust bindings are broken in some containers; block it so pypdf falls
    back to its no-crypt provider."""
    class Block:
        def find_module(self, name, path=None):
            if name == "cryptography" or name.startswith("cryptography."):
                return self

        def load_module(self, name):
            raise ImportError("blocked")

    sys.meta_path.insert(0, Block())
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("pypdf is not installed: pip install pypdf")
    reader = PdfReader(RULE_PATH)
    return {i: re.sub(r"\s+", " ", p.extract_text() or "")
            for i, p in enumerate(reader.pages, 1)}


def section_pages(pages):
    """{'7.35.3.19': {12, 13}, ...}.

    A section occupies every page from its heading to the page before the next
    section's heading, not only the pages on which its number is printed.
    7.35.3.20 runs 13 to 15 but its number appears on 13 and 15 alone, so a
    citation to p.14 is correct and a naive scan calls it wrong.

    The published rule misnumbers a few headings as 7.34.3.N; accept both.
    """
    heading_page = {}
    for page in sorted(pages):
        for m in re.finditer(r"7\.3[45]\.3\.(\d+)\s+[A-Z][A-Z]", pages[page]):
            n = int(m.group(1))
            heading_page.setdefault(n, page)
    # fall back to any mention for sections whose heading did not match
    for page in sorted(pages):
        for m in re.finditer(r"7\.3[45]\.3\.(\d+)", pages[page]):
            heading_page.setdefault(int(m.group(1)), page)

    order = sorted(heading_page)
    out = {}
    for i, n in enumerate(order):
        start = heading_page[n]
        end = heading_page[order[i + 1]] if i + 1 < len(order) else max(pages)
        out["7.35.3.%d" % n] = set(range(start, end + 1))
    return out


def subsection_pages(pages):
    """{('7.35.3.19','A'): {12,13}, ...}.

    A subsection spans from its own heading to the next heading, like a
    section. 7.35.3.19 (A) begins on p.12 and the sentence carrying the 100 and
    120 practicum hours is on p.13, so both pages are correct for it.
    """
    seq, current = [], None
    for page in sorted(pages):
        for m in re.finditer(r"7\.3[45]\.3\.(\d+)|(?<![A-Za-z])([A-G])\.\s+[A-Z]", pages[page]):
            if m.group(1):
                current = "7.35.3." + m.group(1)
                seq.append((None, page))
            elif current:
                seq.append(((current, m.group(2)), page))

    out = {}
    for i, (key, page) in enumerate(seq):
        if key is None:
            continue
        # runs until the next heading of any kind
        end = seq[i + 1][1] if i + 1 < len(seq) else max(pages)
        out.setdefault(key, set()).update(range(page, end + 1))
    return out


def strip(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def main():
    quiet = "--quiet" in sys.argv
    pages = read_rule_pages()
    secmap = section_pages(pages)
    submap = subsection_pages(pages)
    problems = []
    unattributed = []

    for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        name = os.path.basename(path)
        raw = open(path).read()

        # --- 1. anchored links: find the section named in or near the link ---
        for m in re.finditer(
                r'href="documents/' + re.escape(RULE) + r'#page=(\d+)"[^>]*>(.*?)</a>',
                raw, re.S):
            page = int(m.group(1))
            # Only the link's own text is authoritative. Guessing the subject
            # from surrounding prose misattributes citations in any block that
            # discusses more than one provision, which most of them do.
            named = re.findall(r"7\.35\.3\.(\d+)\s*\(?([A-G])?\)?", strip(m.group(2)))
            if not named:
                line = raw[:m.start()].count("\n") + 1
                unattributed.append(
                    f"{name}:{line}  link text names no section: "
                    f"'{strip(m.group(2))[:48]}' -> #page={page}")
                continue
            sec = "7.35.3." + named[-1][0]
            sub = named[-1][1] or None
            valid = secmap.get(sec, set())
            if page not in valid:
                line = raw[:m.start()].count("\n") + 1
                problems.append(
                    f"{name}:{line}  #page={page} but {sec} is on "
                    f"p.{sorted(valid) or '?'}  [{strip(m.group(2))[:44]}]")
            elif sub and (sec, sub) in submap and page not in submap[(sec, sub)]:
                line = raw[:m.start()].count("\n") + 1
                problems.append(
                    f"{name}:{line}  #page={page} but {sec} ({sub}) is on "
                    f"p.{sorted(submap[(sec, sub)])}  [{strip(m.group(2))[:44]}]")

        # --- 2. prose of the form "7.35.3.19 (A), p. 13" ---
        text = strip(raw)
        for m in re.finditer(
                r"7\.35\.3\.(\d+)\s*(?:\(([A-G])\))?[^.]{0,40}?,?\s*p{1,2}\.\s*(\d+)",
                text):
            sec, sub, page = "7.35.3." + m.group(1), m.group(2), int(m.group(3))
            valid = secmap.get(sec, set())
            if valid and page not in valid:
                problems.append(
                    f"{name}  prose: '{m.group(0)[:52]}' but {sec} is on p.{sorted(valid)}")
            elif sub and (sec, sub) in submap and page not in submap[(sec, sub)]:
                problems.append(
                    f"{name}  prose: '{m.group(0)[:52]}' but {sec} ({sub}) is on "
                    f"p.{sorted(submap[(sec, sub)])}")

    if not quiet:
        print("Section-to-page map, from " + RULE + ":")
        for sec in sorted(secmap, key=lambda s: int(s.split(".")[-1])):
            print(f"  {sec:<12} p.{sorted(secmap[sec])}")
        print()
        if problems:
            print(f"{len(problems)} citation problem(s):\n")
            for p in problems:
                print("  " + p)
        else:
            print("Every citation that names a section resolves to a page containing it.")
        if unattributed:
            print(f"\n{len(unattributed)} citation(s) whose link text names no section,")
            print("so nothing can verify them. Cite to the subsection:\n")
            for u in unattributed:
                print("  " + u)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()

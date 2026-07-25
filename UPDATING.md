# How to update this site

Read this before changing anything in `docs/`. It exists so that a session starting with "we had another meeting, here is the transcript" can bring the site current without rediscovering how any of it works.

## What this site is

A working reference for the people running New Mexico's medical psilocybin training and education rulemaking: Advisory Board members, Training and Education Committee members, and department staff. They arrive knowing the subject. It is not a public explainer and not an advocacy site.

**Live:** https://notafeature.github.io/NMMPAB_Rules-Draft-Analysis/ served from `docs/` on `main`.

Two things are always true and must stay true:

1. Every statement about what the rule requires cites the **current published rule** by section and page.
2. Nothing is characterised. Dated events and attributed quotes only.

## The current state of truth

As of July 25, 2026 the operative document is **`docs/documents/rules-draft-2026-07-23-published.pdf`**, the department's published proposed rule 7.35.3 NMAC, 19 pages, sections 7.35.3.1 through .28, going to a rule hearing on **August 28, 2026**.

Everything earlier is history: the June 12 committee recommendation, the June 25 department draft, and the July 9 board-meeting draft. They are cited only where a page is explicitly comparing versions.

The document chain lives in one place, `tools/sync-provenance.py`, and is written into the foot of every page. **When a new document supersedes the current one, that file is the first thing you edit.**

## The update loop

When a meeting happens or a document is published, work in this order. Skipping ahead produces pages that contradict each other.

### 1. Get the source in

Put the document in `docs/documents/` with a dated name matching the existing pattern, for example `rules-draft-2026-07-23-published.pdf`. Transcripts go in as PDFs and also as plain text in `source-text/` so they can be searched and quoted.

If a transcript has no speaker labels, say so on the document itself and everywhere it is quoted. The July 9 transcript is speaker-tagged; both July 17 transcripts are not. Never add a speaker label you inferred without recording the basis.

### 2. Extract and diff before writing anything

Extract the text and compare it against the version it supersedes. Do not summarise from the meeting notes and do not trust your memory of what changed.

```
pip install pypdf
python3 -c "
from pypdf import PdfReader
r = PdfReader('docs/documents/NEW.pdf')
for i, p in enumerate(r.pages, 1):
    print(f'\n===== PAGE {i} =====\n' + (p.extract_text() or ''))
" > /tmp/new.txt
```

Then diff section by section against the previous extraction. Section numbering changes between drafts, so align on headings rather than on order. Write the result into `analysis/` as a dated delta file before touching any page.

**This step has caught real errors.** The July 23 publication raised the shared didactic module from 25 hours to 30, and every page on the site said 25 because everyone assumed the deferred figures had been carried forward untouched.

### 3. Build the section-to-page map

Deep links use `documents/FILE.pdf#page=N`. Page numbers change between drafts, so every citation on the site breaks when a document is superseded. Build the map once and reuse it:

```
python3 -c "
import re
raw = open('/tmp/new.txt').read()
for part in re.split(r'(===== PAGE \d+ =====)', raw):
    m = re.match(r'===== PAGE (\d+) =====', part)
    if m: page = m.group(1); continue
    for h in re.finditer(r'(7\.\d+\.\d+\.\d+)\s+([A-Z][A-Z ,;:/&-]+):', part):
        print(f'{h.group(1)}\tp.{page}\t{h.group(2).strip()}')
"
```

### 4. Update the provenance chain

Edit `CHAIN` in `tools/sync-provenance.py`: add the new document, mark it `"current": True`, remove `current` from the old one, and describe what it changed. Then run the tool.

### 5. Update the pages

Which page owns which fact:

| Page | Owns |
|---|---|
| `index.html` | What is open right now, what is settled, the next three dates |
| `deferred.html` | Every provision a practicum change touches, and what is broken in the published text |
| `hours.html` | Hour requirements by role, cost, and the record of what was said about them |
| `pathways.html` | Route to each permit by starting license |
| `eligibility.html` | Which licenses map to which permit |
| `cs-number.html` | The controlled-substance number at the certifying-clinician access point |
| `changes.html` | Provision-level record, current layer first, earlier comparisons below |
| `history.html` | The dated chain of meetings, votes, and documents, newest first |
| `documents.html` | The register: what each document is, whether it is current, and a download |
| `about.html` | Method, sources, verification, corrections |
| `input.html` | The community input form |

A fact belongs on exactly one page. Other pages link to it.

### 6. Record what you did

Add an entry to `REVISIONS` in `tools/sync-provenance.py` for every page you changed, stating **what changed**, not that something changed. "Corrected the in-state bridge deadline from June 30 2027 to December 31 2027" is an entry. "Updated for the published rule" is not.

Then set the date marker at the top of the page: **Updated** if the content changed, **Reviewed** if you checked it and it needed nothing.

### 7. Run the tools and the verification pass

```
python3 tools/sync-nav.py          # nav markup and script, identical everywhere
python3 tools/sync-provenance.py   # document chain and per-page revisions
```

Both accept `--check` to verify without writing. Never hand-edit the blocks they own; edit the tool and re-run.

Then the checks in the next section. All of them, every time.

### 8. Commit, pull request, merge

Branch, commit with a message that says what changed and why, open a pull request, merge it. The site owner reviews on the live site, so unmerged work is invisible to them.

Squash-merging rewrites history on `main`, so the branch diverges after every merge. Expect to `git merge origin/main` and resolve before the next merge. The conflicts are almost always your newer work against the squashed older version, and the resolution is almost always to keep yours, but read them rather than assuming.

## The verification pass

Run all of it before opening a pull request.

```
# every page parses, no unclosed or mismatched tags
# nested anchors: invalid HTML that browsers silently break apart
# em dashes: house rule, zero anywhere
python3 - <<'EOF'
import glob, html.parser, re
for f in sorted(glob.glob("docs/*.html")):
    s = open(f).read()
    class P(html.parser.HTMLParser):
        def __init__(s): super().__init__(); s.st=[]; s.bad=[]
        def handle_starttag(s,t,a):
            if t not in ('meta','link','br','hr','img','input'): s.st.append(t)
        def handle_endtag(s,t):
            if s.st and s.st[-1]==t: s.st.pop()
            elif t in s.st: s.bad.append(t)
    p = P(); p.feed(s)
    nested = [m for m in re.finditer(r'<a\b[^>]*>', s) if '<a ' in s[m.end():s.find('</a>', m.end())]]
    problems = []
    if p.bad or p.st: problems.append(f"parse {p.bad or p.st}")
    if nested: problems.append(f"{len(nested)} nested anchor(s)")
    if s.count(chr(8212)): problems.append(f"{s.count(chr(8212))} em dash(es)")
    if problems: print(f, "|", "; ".join(problems))
EOF

# link text must not contradict its target
python3 - <<'EOF'
import glob, re
for f in sorted(glob.glob("docs/*.html")):
    s = open(f).read()
    for m in re.finditer(r'<a href="(documents/[^"]*)"[^>]*>([^<]*)</a>', s):
        href, txt = m.group(1), m.group(2)
        for tag in ("2026-06-12", "2026-06-25", "2026-07-09", "2026-07-23"):
            if tag in href: break
        else: continue
        if "published" in txt.lower() and "07-23" not in href:
            print(f, "| text says published, href is", href)
EOF

# internal links resolve.
# Skips anything containing a quote or a plus, which is an href built in
# JavaScript rather than a literal link. pathways.html constructs its citation
# links that way, and a naive grep reports them as broken.
cd docs && grep -oh 'href="[^"]*"' *.html | sed 's/href="//;s/"//' | sort -u \
  | while read h; do
      case "$h" in http*|\#*|*@*|*\'*|*+*) continue;; esac
      [ -e "${h%%[#?]*}" ] || echo "MISS $h"
    done
```

**Verify every quotation against the source.** Do not trust your own transcription. Split on ellipses and check each fragment:

```
python3 - <<'EOF'
import re, html
src = re.sub(r"===== PAGE \d+ =====", "", open("/tmp/new.txt").read())
norm = lambda t: re.sub(r"\s+"," ",t).replace(chr(8220),'"').replace(chr(8221),'"').replace(chr(8217),"'")
src = norm(src).replace("certif ication","certification").replace("in -person","in-person")
page = open("docs/PAGE.html").read()
for q in re.findall(r'<blockquote>(.*?)</blockquote>', page, re.S):
    t = norm(html.unescape(re.sub(r'<[^>]+>','',q)))
    for frag in [f.strip(' .;') for f in t.split(chr(8230))]:
        if len(frag) > 24 and frag not in src:
            print("NOT VERBATIM:", frag[:120])
EOF
```

PDF extraction inserts spaces inside words from character spacing, so `certification` can extract as `certif ication`. Normalise those in the comparison rather than reproducing them on the page.

## House rules

- **No em dashes.** Commas, colons, or a full stop.
- **Verbatim means verbatim.** Never paraphrase inside quotation marks. Mark elisions with an ellipsis and verify each side separately.
- **Cite to the subsection**, not just the document. "7.35.3.19 (A), p. 12" rather than "the practicum section".
- **Every claim carries its source.** A page cite or a named transcript.
- **The repository is public.** Everything committed is published, including commit messages and everything in `analysis/`. There is no internal directory.
- **Links to documents open in a new tab**, so a reader is not taken away from what they are comparing.
- **Never nest an `<a>` inside another `<a>`.** It is invalid, browsers break the layout apart, and a parser check will not catch it.

## Writing standard

- Complete sentences, or an actual list. A list written as prose is neither, and strings of four-word fragments are a tic rather than a style.
- Every element introduces itself. If a page needs a note explaining how to read it, rewrite the page.
- Specific rather than gestural. Name the subsection and the figure.
- The reader is intelligent and has never been here. Both at once.
- Cut anything present only for effect. No headlines, no hyperbole.

## Traps that have already caught someone

- **Live-blog tense.** Pages written during a meeting said "this morning" and "the committee meets at 1 PM today" for eight days. If you write during a meeting, put a date on it and close it out afterwards.
- **Assuming deferred figures were carried forward.** The July 23 rule raised the didactic module while it was deferred. Diff, do not assume.
- **Page anchors after a new draft.** Every `#page=N` is wrong the moment a document is superseded.
- **Blanket find-and-replace on link text.** Replacing "July 9 draft" with "published rule" left four links whose text and target disagreed. The check above exists because of that.
- **Currency work is not review.** Repointing citations does not tell you whether a page still makes sense, still says what it is, or still holds its weight. Do both, and do not report one as the other.

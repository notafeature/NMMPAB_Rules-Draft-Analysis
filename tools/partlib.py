"""Which Part of 7.35 NMAC a tool is working on, and where that Part's pages live.

The site is one host with one folder per Part: docs/7.35.3/ holds the Training
and Education pages, docs/7.35.2/ will hold the producer and laboratory pages,
and docs/ itself holds the parts index, the shared stylesheet, the documents,
and a redirect stub at every retired root address. Every tool that reads or
writes pages asks this module which folder to work in, so the answer lives in
one place.

    --part 7.35.3        the Part to work on; the default is the only Part
                         that has data today

A tool that is given a Part with no data fails here with a plain message,
because the alternative is a tool that silently writes Part 3's content into
Part 2's folder. When Part 2's pages are built, its data joins the tools and
its entry joins PARTS.

Shared assets are linked by root-absolute path, /style.css and /documents/...,
because pages live one level down and the site is served at the root of its
host. resolve() turns any internal href into the file it names.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_ROOT = os.path.join(ROOT, "docs")

# One entry per Part whose pages exist. The suffix ends every page title in
# that Part; the brand is the text on the top bar's home link.
PARTS = {
    "7.35.2": {
        "suffix": "7.35.2 NMAC Producers and Laboratories",
        "brand": "7.35.2 NMAC &middot; Producers &amp; Laboratories",
    },
    "7.35.3": {
        "suffix": "7.35.3 NMAC Training and Education",
        "brand": "7.35.3 NMAC &middot; Training &amp; Education",
    },
}

DEFAULT = "7.35.3"


def current_part(argv=None):
    """The Part named by --part on the command line, or the default."""
    argv = sys.argv[1:] if argv is None else argv
    if "--part" in argv:
        i = argv.index("--part")
        if i + 1 >= len(argv):
            raise SystemExit("--part needs a Part number, such as 7.35.3")
        part = argv[i + 1]
        if part not in PARTS:
            raise SystemExit(f"tools/partlib.py: no page data for Part {part}; "
                             f"the Parts with pages are {', '.join(PARTS)}")
        return part
    return DEFAULT


def docs_dir(part):
    return os.path.join(DOCS_ROOT, part)


def data_path(part, name):
    """The file that holds a Part's data for one tool: tools/parts/<part>/<name>.py."""
    return os.path.join(ROOT, "tools", "parts", part, name + ".py")


def has_data(part, name):
    return os.path.exists(data_path(part, name))


def load_data(part, name, namespace):
    """Execute a Part's data file for one tool into that tool's namespace.

    A tool holds its code; what is true of a Part lives in tools/parts/<part>/,
    one file per tool, executed here so the tool's own helpers are in scope
    for anything the data file defines. A tool that has no data for the Part
    stops here rather than running on another Part's facts.
    """
    path = data_path(part, name)
    if not os.path.exists(path):
        raise SystemExit(f"tools/partlib.py: Part {part} has no data for {name}; "
                         f"expected {os.path.relpath(path, ROOT)}")
    with open(path) as f:
        code = compile(f.read(), path, "exec")
    exec(code, namespace)


def suffix(part):
    return PARTS[part]["suffix"]


def brand(part):
    return PARTS[part]["brand"]


def all_html_dirs():
    """Every folder that holds pages: the root, then each Part."""
    return [DOCS_ROOT] + [docs_dir(p) for p in PARTS]


def resolve(href, page_dir):
    """The file an internal href names, or None for an external or in-page link.

    A root-absolute href resolves from docs/; anything else resolves from the
    folder of the page that carries it. Fragments and query strings are
    dropped. A bare "/" names the parts index.
    """
    if href.startswith(("http", "#", "mailto:")):
        return None
    target = href.split("#")[0].split("?")[0]
    if not target:
        return None
    if target.startswith("/"):
        rest = target.lstrip("/") or "index.html"
        return os.path.join(DOCS_ROOT, rest)
    return os.path.join(page_dir, target)

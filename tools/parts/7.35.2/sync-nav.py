"""Part 7.35.2 data for tools/sync-nav.py. Executed into that tool's namespace by
tools/partlib.py; the tool holds the code, this file holds what is true of the Part."""

# The canonical name of each page. One name per page, used as the nav label, as
# the <title> before the suffix, and as the H1.
NAMES = {
    "index": "Where things stand",
    "rule": "The adopted rule",
    "producers": "For producers",
    "laboratories": "For testing laboratories",
    "record": "Meetings and filings",
}

# The dropdown's members, in the order they appear: the register, the operative
# text, then the documents of the most recent filing.
MENU_DOCUMENTS = [
    {
        "href": "record.html#documents",
        "label": "All documents",
        "sub": "The register: what each one is and whether it is current",
    },
    {
        "href": "/documents/rules-7.35.2-adopted-2026-06-23-published.pdf",
        "label": "The adopted rule &middot; June 23",
        "sub": "7.35.2 NMAC as published in the New Mexico Register, in effect",
    },
    {
        "href": "/documents/rules-7.35.2-amendments-2026-08-25-published.pdf",
        "label": "Proposed amendments &middot; August 25",
        "sub": "The definitions, producer sales, and transportation",
    },
    {
        "href": "/documents/rules-7.35.3-exhibit-binder-2026-10-01.pdf",
        "label": "Hearing exhibits &middot; October 1",
        "sub": "The texts as heard October 2, and 51 written comments",
    },
    {
        "href": "/documents/rules-7.35.2-amendments-2026-10-20-published.pdf",
        "label": "Proposed definitions &middot; October 20",
        "sub": "Eleven terms for the treatment equity fund; heard November 20",
    },
]

# The nav groups. Each entry is (href, data-nav slug or None, sub-line[, label]).
GROUPS = [
    ("start", "Start here", [
        ("/", None, "Every Part of Chapter 35, and where each stands", "All parts of 7.35 NMAC"),
        ("index.html", "index", "In effect since June 23; amendments heard October 2, not adopted"),
        ("/about/", None, "Sources, method, and how to report an error", "How this site is built"),
    ]),
    ("who", "Who the rule reaches", [
        ("producers.html", "producers", "The permit, the premises, testing, labeling, transport"),
        ("laboratories.html", "laboratories", "Accreditation, sampling, the required tests, reporting"),
    ]),
    ("rule", "The rule", [
        ("rule.html", "rule", "All twenty-seven sections, verbatim, the proposed amendments noted"),
    ]),
    ("record", "The record", [
        ("record.html", "record", "The dated chain, newest first"),
        ("record.html#documents", None, "The register: every document and its status", "All documents"),
    ]),
]

# The call to action between the groups and the Documents dropdown.
CTA = None

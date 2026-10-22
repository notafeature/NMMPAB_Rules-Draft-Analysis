"""Part 7.35.4 data for tools/sync-nav.py. Executed into that tool's namespace by
tools/partlib.py; the tool holds the code, this file holds what is true of the Part."""

# The canonical name of each page. One name per page, used as the nav label, as
# the <title> before the suffix, and as the H1.
NAMES = {
    "index": "Where things stand",
    "rule": "The proposed rule",
    "fund": "Who the fund would pay, and for what",
    "recommendation": "The board recommendation",
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
        "href": "/documents/rules-7.35.4-proposed-2026-10-20-published.pdf",
        "label": "The proposed rule &middot; October 20",
        "sub": "7.35.4 NMAC, Treatment Equity Fund, as proposed; not in effect",
    },
    {
        "href": "/documents/rules-7.35.2-amendments-2026-10-20-published.pdf",
        "label": "Proposed definitions &middot; October 20",
        "sub": "The amendment to 7.35.2.7 NMAC that 7.35.4.7 imports",
    },
    {
        "href": "/documents/hearing-notice-7.35.4-2026-10-20.pdf",
        "label": "Hearing notice &middot; October 20",
        "sub": "November 20, 9:00 AM, Santa Fe, and by video and telephone",
    },
]

# The nav groups. Each entry is (href, data-nav slug or None, sub-line[, label]).
GROUPS = [
    ("start", "Start here", [
        ("/", None, "Every Part of Chapter 35, and where each stands", "All parts of 7.35 NMAC"),
        ("index.html", "index", "Proposed October 20; rule hearing November 20"),
        ("/about/", None, "Sources, method, and how to report an error", "How this site is built"),
    ]),
    ("who", "Who the rule reaches", [
        ("fund.html", "fund", "Patients, the providers who bill the fund, and the department"),
    ]),
    ("rule", "The rule", [
        ("rule.html", "rule", "All twenty sections, verbatim, as proposed"),
        ("recommendation.html", "recommendation", "The September 11 board vote, beside the proposed text"),
    ]),
    ("record", "The record", [
        ("record.html", "record", "The dated chain, newest first"),
        ("record.html#documents", None, "The register: every document and its status", "All documents"),
    ]),
]

# The call to action between the groups and the Documents dropdown.
CTA = None

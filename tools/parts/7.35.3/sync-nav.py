"""Part 7.35.3 data for tools/sync-nav.py. Executed into that tool's namespace by
tools/partlib.py; the tool holds the code, this file holds what is true of the Part."""

# The canonical name of each page. One name per page, used as the nav label, as
# the <title> before the suffix, and as the H1. Changing a name here is half the
# job: the <title> and the H1 are in the page and are checked, not written, by
# this tool.
NAMES = {
    "index": "Where things stand",
    "rule": "The published rule",
    "record": "Meetings and filings",
    "hours": "The training hours",
    "recommendation": "The committee recommendation",
    "comment": "Comment",
    "pathways": "Routes to a permit",
    "eligibility": "Which licenses qualify",
    "cs-number": "The controlled-substance number",
    "specialization": "Specialized domains",
    "deferred": "What a practicum change touches",
    "changes": "Section by section",
    "training-hours-record": "The training-hours record",
}


# The dropdown's members, in the order they appear. The register comes first,
# then the operative text, then that meeting's or filing's own documents.
# check-site.py reads this list, so the menu and the check cannot disagree.
MENU_DOCUMENTS = [
    {
        "href": "record.html#documents",
        "label": "All documents",
        "sub": "The register: what each one is and whether it is current",
    },
    {
        "href": "/documents/rules-draft-2026-08-25-published.pdf",
        "label": "Revised proposed rule &middot; August 25",
        "sub": "The current proposed rule, 7.35.3.1 through .28",
    },
    {
        "href": "/documents/rules-7.35.2-amendments-2026-08-25-published.pdf",
        "label": "7.35.2 amendments &middot; August 25",
        "sub": "The definitions, producer sales, and transportation",
    },
    {
        "href": "/documents/hearing-notice-2026-08-25.pdf",
        "label": "Hearing notice &middot; August 25",
        "sub": "October 2, 9:00 AM, Santa Fe, and by video and telephone",
    },
]

# The nav groups. Each entry is (href, data-nav slug or None, sub-line). The
# label comes from NAMES where a slug is given, so a name is written once.
GROUPS = [
    ("start", "Start here", [
        ("/", None, "Every Part of Chapter 35, and where each stands", "All parts of 7.35 NMAC"),
        ("index.html", "index", "What is open, what is settled, what is next"),
        ("index.html#directory", None, "Every page, in one list", "What is on this site"),
        ("/about/", None, "Sources, method, and how to report an error", "How this site is built"),
    ]),
    ("provider", "Becoming a provider", [
        ("pathways.html", "pathways", "Pick where you start; the route to each permit"),
        ("eligibility.html", "eligibility", "The license-by-permit tables"),
        ("hours.html", "hours", "The working model of the training hours"),
        ("specialization.html", "specialization", "An overlay on a core permit, not in the rule"),
        ("cs-number.html", "cs-number", "The certifying clinician requirement"),
        ("deferred.html", "deferred", "Every provision a practicum change reaches"),
    ]),
    ("rule", "The rule", [
        ("rule.html", "rule", "All twenty-eight sections, verbatim, annotated"),
        ("changes.html", "changes", "What each publication changed, layer by layer"),
        ("recommendation.html", "recommendation", "The August 21 position, beside the published text"),
        ("comment.html", "comment", "The October 2 rule hearing, and the input channel"),
    ]),
    ("record", "The record", [
        ("record.html", "record", "The dated chain, newest first"),
        ("record.html#documents", None, "The register: every document and its status", "All documents"),
        ("training-hours-record.html", "training-hours-record",
         "July 9 through August 25, with benchmarks and community comment"),
    ]),
]

# The call to action sits between the groups and the Documents dropdown. It
# carries no data-nav, so the active-page marker stays on the dropdown entry.
CTA = ("comment.html", "Comment")

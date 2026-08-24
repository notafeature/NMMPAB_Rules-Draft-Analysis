#!/usr/bin/env python3
"""Generate the chain, the register, and the gaps register on docs/record.html.

record.html is the site's most update-frequent page, and until this tool existed
every event, every document row, and every stated absence was hand-written HTML.
The same document was then described twice in different words, once in a chain
entry and once in a register row, which is the drift pattern the redesign brief
names first. Three structures here hold that content once:

    EVENTS      every meeting, publication, filing, and scheduled date, newest
                first, each with a stable anchor of the form e-YYYY-MM-DD, with
                -am or -pm appended where a day carries more than one event
    DOCUMENTS   the register: every document the site holds or cites, each with
                a stable anchor of the form doc-<slug>
    GAPS        the register of documents the site does not hold, each naming
                the event it belongs to

The three reference each other, and the references are checked rather than
trusted: an event attaches documents by slug, states an absence by gap id, and
every gap names its events. validate() below fails on a reference that does not
resolve, and on an absence a gap claims that its event does not carry back.

Text fields are HTML fragments. They carry their own links and entities, and
they are written to the standard in WRITING-STANDARD.md: every figure, date,
vote, and quotation comes from the published rule, a named transcript, or
another page of this site, and an absence is stated rather than left silent.

Four regions of docs/record.html are generated, each between its own markers,
and nothing outside them is touched: the page's own stylesheet block, the
chain, the register at #documents, and the gaps register at #gaps.

tools/check-site.py imports this module, which runs validate() at import, and
calls stale() to fail the build if record.html no longer matches the data.
tools/sync-provenance.py reads DOCUMENTS as well, for the four documents of the
drafting chain it names at the foot of the seven pages that carry a provenance
block, so the register is the one place a document's identity is written.

Usage:
    python3 tools/sync-record.py           # write the four blocks into record.html
    python3 tools/sync-record.py --check   # exit 1 if record.html is stale
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
PAGE = os.path.join(DOCS, "record.html")

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


# ---------------------------------------------------------------------------
# The register. Newest first. `file` is None where the site cites a document it
# does not publish. `status` is one of current, superseded, record; a superseded
# document always names the document that superseded it. `chain` marks the four
# documents of the drafting line, each superseding the one before it;
# tools/sync-provenance.py reads them from here rather than keeping its own copy.
# ---------------------------------------------------------------------------

DOCUMENTS = [
    {
        "slug": "summary-recommended-rules",
        "name": "Summary of the recommended rules",
        "file": None,
        "date": "2026-07-27",
        "event": "e-2026-07-27",
        "what": "The Training and Education Committee's recommendation on the practicum and "
                "didactic hours, stated in plain language",
        "status": "current",
        "notes": "Five pages. Not published on this site; its figures are stated in full on "
                 "<a href=\"recommendation.html\">The committee recommendation</a>",
    },
    {
        "slug": "rules-draft-2026-07-23-published",
        "name": "Published proposed rule",
        "file": "documents/rules-draft-2026-07-23-published.pdf",
        "cite": "The published proposed rule, July 23, 2026, 19 pages",
        "date": "2026-07-23",
        "event": "e-2026-07-23",
        "what": "The proposed rule as published July 23, set aside with its August 28 "
                "hearing; the last published text of this rulemaking, and the text this "
                "site cites for section numbers until revised rules publish",
        "status": "current",
        "chain": True,
        "notes": "19 pages. Sections 7.35.3.1 through .28, typeset on this site at "
                 "<a href=\"rule.html\">The last published text</a>",
    },
    {
        "slug": "nmmpab-2026-07-17-board-transcript",
        "name": "Advisory Board transcript",
        "file": "documents/NMMPAB-2026-07-17-board-transcript.pdf",
        "cite": "July 17 board transcript, unofficial, no speaker labels",
        "date": "2026-07-17",
        "event": "e-2026-07-17-am",
        "what": "The morning Advisory Board meeting, at which the hours went to committee and "
                "the controlled-substance number was kept",
        "status": "record",
        "notes": "23 pages. Unofficial. No speaker labels",
    },
    {
        "slug": "nmmpab-2026-07-17-committee-transcript",
        "name": "Training and Education Committee transcript",
        "file": "documents/NMMPAB-2026-07-17-committee-transcript.pdf",
        "cite": "July 17 committee transcript, unofficial, no speaker labels",
        "date": "2026-07-17",
        "event": "e-2026-07-17-pm",
        "what": "The afternoon committee session that took up the deferred hours",
        "status": "record",
        "notes": "23 pages. Unofficial. No speaker labels",
    },
    {
        "slug": "metz-recommendations-2026-07-17",
        "name": "Dr. Anne Metz's written recommendations",
        "file": "documents/metz-recommendations-2026-07-17.pdf",
        "cite": "Dr. Anne Metz's written recommendations, presented July 17",
        "date": "2026-07-17",
        "event": "e-2026-07-17-pm",
        "what": "The four recommendations presented to the committee, in writing",
        "status": "record",
        "notes": "6 pages",
    },
    {
        "slug": "metz-onepager-2026-07-17",
        "name": "Dr. Anne Metz's one-page summary",
        "file": "documents/metz-onepager-2026-07-17.pdf",
        "cite": "Dr. Anne Metz's one-page summary, July 17",
        "date": "2026-07-17",
        "event": "e-2026-07-17-pm",
        "what": "The same four recommendations on one page",
        "status": "record",
        "notes": "1 page",
    },
    {
        "slug": "metz-slides-2026-07-17",
        "name": "Dr. Anne Metz's slides",
        "file": "documents/metz-slides-2026-07-17.pptx",
        "cite": "Dr. Anne Metz's slides, July 17",
        "date": "2026-07-17",
        "event": "e-2026-07-17-pm",
        "what": "The slides shown with the presentation",
        "status": "record",
        "notes": "6 slides. PowerPoint, not PDF",
    },
    {
        "slug": "rules-draft-2026-07-09",
        "name": "Board-meeting draft",
        "file": "documents/rules-draft-2026-07-09.pdf",
        "cite": "The July 9 board-meeting draft, superseded",
        "date": "2026-07-09",
        "event": "e-2026-07-09",
        "what": "The draft the Advisory Board went through section by section on July 9",
        "status": "superseded",
        "superseded_by": "rules-draft-2026-07-23-published",
        "chain": True,
        "notes": "17 pages. Placeholder section numbers, shown as 7.35.3.X. Carried the older "
                 "waiver dates of December 31, 2026 and June 30, 2027, which the board extended "
                 "by vote that day without the text being updated",
    },
    {
        "slug": "nmmpab-2026-07-09-transcript",
        "name": "Advisory Board transcript",
        "file": "documents/NMMPAB-2026-07-09-transcript.pdf",
        "cite": "July 9 board transcript, unofficial, speaker-tagged",
        "date": "2026-07-09",
        "event": "e-2026-07-09",
        "what": "The Advisory Board meeting that resolved reciprocity and tabled the hours",
        "status": "record",
        "notes": "34 pages. Unofficial. Speaker-tagged",
    },
    {
        "slug": "rules-draft-2026-06-25",
        "name": "Department draft",
        "file": "documents/rules-draft-2026-06-25.pdf",
        "cite": "The June 25 department draft, superseded",
        "date": "2026-06-25",
        "event": "e-2026-06-25",
        "what": "The department's first rules-style draft of the training subject",
        "status": "superseded",
        "superseded_by": "rules-draft-2026-07-09",
        "chain": True,
        "notes": "11 pages. Introduced the module test-out mechanism that every later draft "
                 "keeps, and the first reciprocity provision",
    },
    {
        "slug": "recommendation-2026-06-12",
        "name": "Committee recommendation",
        "file": "documents/recommendation-2026-06-12.pdf",
        "cite": "The June 12 committee recommendation, the origin document",
        "date": "2026-06-12",
        "event": "e-2026-06-12",
        "what": "The Training and Education Committee's own recommendation, the origin document "
                "of this rulemaking",
        "status": "record",
        "chain": True,
        "notes": "9 pages. Origin of the 100 and 120 practicum hours and the 20 supervisory "
                 "hours. Compared provision by provision on "
                 "<a href=\"changes.html\">Section by section</a>",
    },
]


# ---------------------------------------------------------------------------
# The gaps register. Every row names the event it belongs to, and every event it
# names carries the reciprocal absence line. `at_event` is the sentence the
# event shows; `means` is the sentence the register shows.
# ---------------------------------------------------------------------------

GAPS = [
    {
        "id": "gap-minutes",
        "name": "Official minutes, any meeting",
        "means": "Nothing on this site is official minutes. One consequence: the mover of the "
                 "June 26 motion is attributed from a meeting-note summary, because the raw "
                 "transcript is unlabeled at that point",
        "at_event": "No transcript or official minutes of this meeting is held on this site, "
                    "and the mover of the motion is attributed from a meeting-note summary.",
        "events": ["e-2026-06-26"],
    },
    {
        "id": "gap-june",
        "name": "Recordings or transcripts, June 12 and June 25",
        "means": "The recommendation and the department draft from those dates are held; the "
                 "meetings themselves are not",
        "at_event": "No recording or transcript of the meeting on this date is held on this "
                    "site. The document it produced is.",
        "events": ["e-2026-06-25", "e-2026-06-12"],
    },
    {
        "id": "gap-july16",
        "name": "July 16 End-of-Life Care committee meeting, any record",
        "means": "Everything on <a href=\"specialization.html\">Specialized domains</a> rests "
                 "on it: the endorsement proposal, the proposed hour ranges, the nine-session "
                 "curriculum, and the positions attributed to named participants",
        "at_event": "No record of this meeting is held on this site, and everything this site "
                    "states about it rests on that meeting.",
        "events": ["e-2026-07-16"],
    },
    {
        "id": "gap-may22",
        "name": "May 22 committee meeting, any record",
        "means": "Held, but not recorded or posted by the department",
        "at_event": "No record of this meeting exists. It was held, and the department did not "
                    "record or post it.",
        "events": ["e-2026-05-22"],
    },
    {
        "id": "gap-hearing-notice",
        "name": "The rule hearing notice as published",
        "means": "The official time, place, and comment instructions. The October 2 date on "
                 "this site is sourced to the department's statement at the August 21 "
                 "committee meeting, not to a filing; the department said the final notice is "
                 "in preparation with the hearing officer",
        "at_event": "The hearing notice as published is not held on this site. The date is "
                    "sourced to the department's August 21 statement, not to a filing.",
        "events": ["e-2026-10-02"],
    },
    {
        "id": "gap-aug14",
        "name": "August 14 board meeting recording or transcript, and the set-aside notice",
        "means": "The meeting at which the set-aside of the July 23 publication was on the "
                 "record and the August 25 date was stated. The department's announcement "
                 "setting aside the publication and the August 28 hearing is not held either; "
                 "the set-aside is sourced to how it was spoken of at the meeting. A live "
                 "auto-generated transcript exists in Notion; the working record is "
                 "analysis/8-14-board-extraction.md in the repository",
        "at_event": "No recording, transcript, or set-aside notice is held on this site for "
                    "this meeting. The department recorded the meeting for posting.",
        "events": ["e-2026-08-14"],
    },
    {
        "id": "gap-aug21",
        "name": "August 21 committee meeting recording or transcript",
        "means": "The meeting at which both hours proposals were shown side by side and the "
                 "October 2 hearing was stated. The department recorded it for posting; a "
                 "live auto-generated transcript exists in Notion",
        "at_event": "No recording or transcript of this meeting is held on this site yet. The "
                    "department recorded the meeting for posting on its website.",
        "events": ["e-2026-08-21"],
    },
]


# ---------------------------------------------------------------------------
# The chain. Newest first. Each event is one meeting, publication, filing, or
# scheduled date.
#
#   id        e-YYYY-MM-DD, with -am or -pm where a day carries two events
#   kind      meeting, document, filing, or scheduled
#   part      the mono line under the date, where a day carries two events
#   what      what happened, outcome first
#   changed   one state transition per line, each naming the page that owns it
#   said      what was said, where this page does not own the account
#   attached  document slugs, newest first within the event
#   absent    gap ids; the reciprocal of the gap row's `events`
#   deeper    the account that holds this event in full
# ---------------------------------------------------------------------------

EVENTS = [
    {
        "id": "e-2026-10-02",
        "date": "2026-10-02",
        "kind": "scheduled",
        "what": "<b>The rule hearing on 7.35.3 NMAC, anticipated.</b> The department placed the "
                "hearing at the end of September or early October at the August 14 board "
                "meeting, and named October 2, virtual and in person, at the August 21 "
                "committee meeting; the final notice, in preparation with the hearing officer, "
                "will fix the date. The hearing was first set for August 28 with the July 23 "
                "publication, which was set aside. Public comment is taken and recorded at the "
                "hearing, and comment given there becomes part of the rulemaking record the "
                "department must consider.",
        "absent": ["gap-hearing-notice"],
        "deeper": [("comment.html", "How comment works, and what is at issue")],
    },
    {
        "id": "e-2026-09-11",
        "date": "2026-09-11",
        "kind": "scheduled",
        "what": "<b>The full Advisory Board meets in the afternoon</b>, to take up the "
                "Training and Education Committee's work; the Research and Continuous "
                "Improvement Committee meets that morning. Scheduled at the August 14 board "
                "meeting.",
    },
    {
        "id": "e-2026-09-04",
        "date": "2026-09-04",
        "kind": "scheduled",
        "what": "<b>The Training and Education Committee meets, 9 to 11 AM.</b> Scheduled at "
                "the close of the August 21 meeting, after the September 11 and 18 mornings "
                "were found taken.",
    },
    {
        "id": "e-2026-08-25",
        "date": "2026-08-25",
        "kind": "scheduled",
        "what": "<b>The department's stated date for publishing revised proposed rules</b>, "
                "stated at the August 14 board meeting and restated August 21, taking the "
                "committee's suggestions under advisement. Public comment continues after "
                "publication, through the rule hearing, and the department said changes can "
                "still be made in that period.",
    },
    {
        "id": "e-2026-08-21",
        "date": "2026-08-21",
        "kind": "meeting",
        "what": "<b>The Training and Education Committee reviewed its subcommittee's education "
                "and training proposal beside the department's, and took no vote.</b> The "
                "chair held a vote off deliberately, with the proposals close and the "
                "department's stated publication date the following Tuesday. The department "
                "restated the schedule: revised rules on August 25, and the rule hearing, "
                "whose first setting of August 28 was set aside with the July 23 publication, "
                "anticipated for October 2.",
        "changed": [
            ("<b>The schedule.</b> Revised proposed rules publish August 25, and the rule "
             "hearing, first set for August 28, is anticipated for October 2; the final "
             "notice will fix the date.",
             "index.html", "Where things stand"),
            ("<b>The hours question.</b> Both proposals now set 80 classroom hours in place "
             "of the published 40. The subcommittee's practicum stands at 114 hours for "
             "licensed providers and 102 for facilitators; the department's at 120 and 100, "
             "structured differently, with case presentation folded into the practicum "
             "rather than separate.",
             "index.html", "Where things stand"),
        ],
        "said": {
            "basis": "The account rests on a live auto-generated transcript with no speaker "
                     "labels; names are fixed by the surrounding text. The department's "
                     "recording, once posted, is the record.",
            "lines": [
                "Dominic Zurlo said the current statute does not allow practicum work with "
                "individuals who do not have a qualifying condition, which is why the "
                "department's proposal carries no well-participants stage.",
                "Zurlo said the department's proposal permits trainee compensation after 50 "
                "practicum hours, and that its 10 post-graduation mentoring hours are an "
                "obligation on programs, optional for graduates.",
                "Anne Metz argued for hour minimums per content area as objective criteria; "
                "Zurlo said the department recommends content areas in the rule without "
                "per-area hours; no resolution was reached.",
                "Senator Jeff Steinborn asked how post-session adverse impact training, "
                "including hallucinogen persisting perception disorder, is ensured in the "
                "language; the chair suggested naming it.",
            ],
        },
        "absent": ["gap-aug21"],
    },
    {
        "id": "e-2026-08-14",
        "date": "2026-08-14",
        "kind": "meeting",
        "what": "<b>The full Advisory Board met, and the set-aside of the July 23 publication "
                "was on the record as an accomplished fact.</b> The department stated it would "
                "publish revised proposed rules on August 25 and placed the rule hearing at "
                "the end of September or early October. A pathway for the committee's work "
                "into the revised rules was arranged: the committee chair and Larry Leeman "
                "were to present the training and education recommendations to the department "
                "the following week, for potential incorporation before publication.",
        "changed": [
            ("<b>The published text.</b> The July 23 publication and its August 28 hearing "
             "were set aside; the July 23 text stands as the last published text of this "
             "rulemaking.",
             "rule.html", "The last published text"),
            ("<b>The schedule.</b> Revised proposed rules stated for August 25; the rule "
             "hearing placed at the end of September or early October. The full board meets "
             "September 11, afternoon, on the committee's work.",
             "index.html", "Where things stand"),
        ],
        "said": {
            "basis": "The account rests on a live auto-generated transcript with no speaker "
                     "labels; names are fixed by the surrounding text. The department's "
                     "recording, once posted, is the record.",
            "lines": [
                "Larry Leeman, on the set-aside: \"one of the reasons why I think the regs "
                "were postponed is because there had been a commitment to the training "
                "committee to be able to work on them.\" No department statement of the "
                "reason appears in the transcript.",
                "Dominic Zurlo said published rules are not set in stone: public comment and "
                "adjustments continue through the rule hearing and after it.",
                "Zurlo stated the program's goal of first patients seen by December, with "
                "rulemaking continuing beyond it.",
            ],
        },
        "absent": ["gap-aug14"],
        "deeper": [],
    },
    {
        "id": "e-2026-07-27",
        "date": "2026-07-27",
        "kind": "filing",
        "what": "<b>The committee recommendation was submitted to the department</b> as a "
                "plain-language summary of the recommended rules, resolving the practicum and "
                "didactic hours the board sent to committee on July 17.",
        "changed": [
            ("<b>Didactic hours.</b> The recommendation sets one standard of 80 hours for both "
             "permits, with minimum hours in nine content areas, where the published text sets "
             "40. Certifying clinicians complete 8.",
             "recommendation.html", "The committee recommendation"),
            ("<b>Practicum, facilitator.</b> The recommendation reduces it from 100 hours to "
             "60, staged from well participants onward.",
             "recommendation.html", "The committee recommendation"),
            ("<b>Practicum, practitioner.</b> The recommendation reduces it from 120 hours to "
             "70, staged the same way.",
             "recommendation.html", "The committee recommendation"),
            ("<b>Hours after the practicum.</b> The published 10 hours of mentoring become 20 "
             "hours of case presentation and consultation, on two cases the student personally "
             "provided.",
             "recommendation.html", "The committee recommendation"),
            ("<b>The permit name.</b> \"Practitioner\" becomes \"Licensed Provider\".",
             "recommendation.html", "The committee recommendation"),
            ("<b>The transition pathway.</b> Applicants who complete their didactic "
             "requirements by December 31, 2027 may satisfy a reduced practicum of 40 contact "
             "hours, or an approved out-of-state practicum.",
             "recommendation.html", "The committee recommendation"),
        ],
        "attached": ["summary-recommended-rules"],
        "deeper": [("recommendation.html",
                    "The recommended figures beside the published text")],
    },
    {
        "id": "e-2026-07-23",
        "date": "2026-07-23",
        "kind": "document",
        "what": "<b>The department published the proposed rule</b>, 19 pages, and the hearing "
                "was set for August 28. This is the first version with final section numbering, "
                "7.35.3.1 through .28.",
        "changed": [
            ("<b>Practicum hours.</b> Published unchanged at 100 hours for facilitators and 120 "
             "for practitioners, six days after the board voted to send them to committee.",
             "rule.html#s19", "7.35.3.19"),
            ("<b>The shared didactic module.</b> Raised from 25 hours to 30, adding "
             "trauma-informed care, dosing, and non-ordinary states of consciousness.",
             "rule.html#s18", "7.35.3.18"),
            ("<b>Both practicum waiver deadlines.</b> Written as December 31, 2027 at "
             "7.35.3.10 (D)(1) and 7.35.3.19 (G), where the July 9 draft carried December 31, "
             "2026 and June 30, 2027.",
             "rule.html#s10", "7.35.3.10 (D)"),
            ("<b>Certifying-clinician exam pathways.</b> The three ways to meet the in-person "
             "requirement, read into the record on July 17, appear in the published text.",
             "cs-number.html#update", "The controlled-substance number"),
            ("<b>When the practicum may begin.</b> New in the published text: it may not begin "
             "until half the didactic requirements and all the simulated-patient requirements "
             "are complete.",
             "rule.html#s19", "7.35.3.19 (A)"),
            ("<b>The healing-center staffing ratio.</b> New in the published text: a student "
             "registered with a certified educational program who has completed at least 50 "
             "practicum hours counts as qualified.",
             "rule.html#s20", "7.35.3.20"),
        ],
        "attached": ["rules-draft-2026-07-23-published"],
        "deeper": [("rule.html", "All twenty-eight sections, verbatim and annotated"),
                   ("changes.html", "What changed, provision by provision")],
    },
    {
        "id": "e-2026-07-17-pm",
        "date": "2026-07-17",
        "part": "Afternoon",
        "kind": "meeting",
        "what": "<b>The Training and Education Committee took up the hours the board had "
                "deferred that morning.</b> Dr. Anne Metz, a clinical facilitator who has "
                "worked in the Oregon and Colorado programs, presented four recommendations: "
                "retitle \"practitioner,\" a single 84-hour didactic standard, a four-step "
                "scaffolded practicum of roughly 62 to 72 hours, and consultation sign-off tied "
                "to two presented cases.",
        "changed": [
            ("<b>The deferred hours.</b> The committee took them up the same day the board sent "
             "them, and its recommendation reached the department on July 27.",
             "recommendation.html", "The committee recommendation"),
            ("<b>Dr. Anne Metz's figures.</b> In the submission the 84 didactic hours became "
             "80, the 62 to 72 practicum hours became 60 and 70, and the 20 to 30 consultation "
             "hours became 20.",
             "recommendation.html", "The committee recommendation"),
        ],
        "said": {
            "basis": "The committee transcript carries no speaker labels. The names below are "
                     "fixed by the surrounding text, not by a label.",
            "lines": [
                "Denali Wilson asked that substance use disorder, end-of-life, suicidality, and "
                "PTSD be added as didactic requirements, and raised whether students could "
                "count toward the staffing ratio.",
                "Chris Caldwell argued for 19 or more live end-of-life instruction hours, and "
                "Larry Leeman supported roughly 10 to 15 in the core curriculum.",
                "Several participants asked for a legacy practitioner pathway.",
                "Dominic Zurlo told the committee the department \"really need[s] them sooner "
                "rather than later,\" with no deadline given.",
            ],
        },
        "attached": ["nmmpab-2026-07-17-committee-transcript", "metz-recommendations-2026-07-17",
                     "metz-onepager-2026-07-17", "metz-slides-2026-07-17"],
        "deeper": [("training-hours-record.html#july17",
                    "The July 17 committee session in full, with benchmarks and cost")],
    },
    {
        "id": "e-2026-07-17-am",
        "date": "2026-07-17",
        "part": "Morning",
        "kind": "meeting",
        "what": "<b>The Advisory Board voted 7-0</b> to send the practicum and didactic hours, "
                "with the definitions, to the Training and Education Committee.",
        "changed": [
            ("<b>Practicum and didactic hours.</b> Sent to the Training and Education Committee "
             "by a 7-0 vote, with the definitions.",
             "recommendation.html", "The committee recommendation"),
            ("<b>The certifying-clinician controlled-substance number.</b> Kept in the rule the "
             "department puts forward, after the department took the earlier concerns to the "
             "Secretary of Health and its attorneys. The board did not vote to remove it.",
             "cs-number.html#update", "The controlled-substance number"),
            ("<b>Certifying-clinician exam language.</b> The department read in revised "
             "language with three ways to meet the in-person requirement.",
             "cs-number.html#update", "The controlled-substance number"),
            ("<b>A question to the department.</b> The board asked how many New Mexico "
             "providers hold prescriptive authority without the state controlled-substance "
             "number.",
             "cs-number.html", "The controlled-substance number"),
        ],
        "said": {
            "basis": "The board transcript carries no speaker labels. The names below are fixed "
                     "by the surrounding text, not by a label.",
            "lines": [
                "Dominic Zurlo said that after taking the earlier concerns to the Secretary of "
                "Health and the department's attorneys, the certifying-clinician "
                "controlled-substance number stays in the rule the department puts forward.",
                "Chris Peskuski restated his objection that the requirement is an access "
                "bottleneck placing liability on a clinician who is not in the room.",
                "Larry Leeman noted that federal rescheduling to Schedule III, which he "
                "considers likely by mid-2027, could reopen the requirement.",
            ],
        },
        "attached": ["nmmpab-2026-07-17-board-transcript"],
        "deeper": [("cs-number.html#update",
                    "The controlled-substance number, through July 23, with the verbatim exam "
                    "language")],
    },
    {
        "id": "e-2026-07-16",
        "date": "2026-07-16",
        "kind": "meeting",
        "what": "<b>The End-of-Life Care committee raised specialization</b> as an endorsement "
                "layered on a core permit, with end-of-life care as the worked example.",
        "changed": [
            ("<b>Specialization.</b> Raised as a proposal. Nothing in the published rule "
             "creates one.",
             "specialization.html", "Specialized domains"),
        ],
        "absent": ["gap-july16"],
        "deeper": [("specialization.html",
                    "The proposal, its hour ranges, and who raised what")],
    },
    {
        "id": "e-2026-07-09",
        "date": "2026-07-09",
        "kind": "meeting",
        "what": "<b>The Advisory Board resolved reciprocity</b> without objection, extending "
                "both waiver deadlines to December 31, 2027, and voted to table the practicum "
                "and didactic hours for the committee. The controlled-substance number was sent "
                "back to the department to weigh alternatives.",
        "changed": [
            ("<b>Both practicum waiver deadlines.</b> Extended to December 31, 2027 by vote, "
             "without the draft text being updated that day; it carried December 31, 2026 and "
             "June 30, 2027.",
             "rule.html#s10", "7.35.3.10 (D)"),
            ("<b>Practicum and didactic hours.</b> Tabled for the Training and Education "
             "Committee.",
             "hours.html", "The training hours"),
            ("<b>The controlled-substance number.</b> Sent back to the department to weigh "
             "alternatives.",
             "cs-number.html#record", "The controlled-substance number"),
            ("<b>The role name.</b> \"Diagnostic clinician\" became \"certifying clinician\" "
             "throughout the draft.",
             "cs-number.html", "The controlled-substance number"),
            ("<b>Individual training certifications.</b> AED certification was added alongside "
             "BLS and CPR.",
             "rule.html#s9", "7.35.3.9 (A)"),
            ("<b>Outdoor locations.</b> EMT certification was added as a staffing alternative.",
             "rule.html#s11", "7.35.3.11"),
            ("<b>The board's Medicaid seat.</b> Keenan Ryan appeared as the new member.",
             None, None),
        ],
        "attached": ["rules-draft-2026-07-09", "nmmpab-2026-07-09-transcript"],
        "deeper": [("cs-number.html#record",
                    "The full July 9 record on the controlled-substance number, by speaker"),
                   ("training-hours-record.html#record",
                    "The July 9 record on the hours")],
    },
    {
        "id": "e-2026-06-26",
        "date": "2026-06-26",
        "kind": "meeting",
        "what": "<b>The Advisory Board voted 3-2 to accept the committee recommendation</b> and "
                "submit it to the department, setting aside the controlled-substance number, "
                "the practicum and didactic hours, and the reciprocity timeline.",
        "changed": [
            ("<b>The June 12 committee recommendation.</b> Accepted 3-2 and sent to the "
             "department, with three items set aside.",
             "changes.html", "Section by section"),
        ],
        "said": {
            "basis": "No transcript or official minutes of this meeting is held on this site. "
                     "The account below comes from a meeting-note summary.",
            "lines": [
                "Only Larry Leeman's \"reluctant yes\" is named on the record. The two votes "
                "against are not.",
            ],
        },
        "absent": ["gap-minutes"],
    },
    {
        "id": "e-2026-06-25",
        "date": "2026-06-25",
        "kind": "document",
        "what": "<b>The department presented a rules-style draft</b> of the training subject to "
                "the Training and Education Committee. The July 9 board-meeting draft "
                "superseded it two weeks later.",
        "changed": [
            ("<b>The module test-out.</b> Introduced here, and kept by every later draft. The "
             "June 12 recommendation did not contain it.",
             "rule.html#s17", "7.35.3.17 (B)"),
            ("<b>Reciprocity.</b> The first reciprocity provision appears here. The June 12 "
             "recommendation did not contain one.",
             "rule.html#s10", "7.35.3.10"),
        ],
        "attached": ["rules-draft-2026-06-25"],
        "absent": ["gap-june"],
    },
    {
        "id": "e-2026-06-12",
        "date": "2026-06-12",
        "kind": "document",
        "what": "<b>The Training and Education Committee issued its recommendation</b>, the "
                "origin document of this rulemaking: permit qualifications by role, curriculum "
                "modules, the 100 and 120 practicum hours with 20 supervisory hours, mentoring, "
                "record-keeping, and continuing education.",
        "changed": [
            ("<b>The 100 and 120 practicum hours, with 20 supervisory hours.</b> They originate "
             "in this document, and they stand in the published text.",
             "rule.html#s19", "7.35.3.19"),
        ],
        "attached": ["recommendation-2026-06-12"],
        "absent": ["gap-june"],
        "deeper": [("changes.html",
                    "This recommendation against the department drafts, provision by provision")],
    },
    {
        "id": "e-2026-05-22",
        "date": "2026-05-22",
        "kind": "meeting",
        "what": "<b>The Training and Education Committee met</b>, the last of the five meetings "
                "that developed the recommendation it issued on June 12.",
        "absent": ["gap-may22"],
    },
    {
        "id": "e-2026-05-08",
        "date": "2026-05-08",
        "kind": "meeting",
        "what": "<b>The Training and Education Committee met jointly with the End-of-Life Care "
                "committee</b>, developing the recommendation it issued on June 12.",
    },
    {
        "id": "e-2026-04-10",
        "date": "2026-04-10",
        "kind": "meeting",
        "what": "<b>The Training and Education Committee met</b>, developing the recommendation "
                "it issued on June 12.",
    },
    {
        "id": "e-2026-03-06",
        "date": "2026-03-06",
        "kind": "meeting",
        "what": "<b>The Training and Education Committee met</b>, developing the recommendation "
                "it issued on June 12.",
    },
    {
        "id": "e-2026-01-23",
        "date": "2026-01-23",
        "kind": "meeting",
        "what": "<b>The Training and Education Committee met</b>, the first of the five "
                "meetings that developed the recommendation it issued on June 12.",
    },
]


# The prose that introduces each generated section. Held here so the section and
# the data it introduces cannot drift apart.
CHAIN_NOTE = (
    "Every meeting, publication, filing, and scheduled date is one event with its own address, "
    "so another page can cite the day rather than restate it. Three pages from before this "
    "site's redesign hold deeper accounts, and each is linked from the events it covers. They "
    "keep their earlier design until their content is fully absorbed here."
)
REGISTER_NOTE = (
    "Every document this site holds or cites, what it is, when it landed, and whether it is "
    "current. The date in each row opens the event the document belongs to."
)
GAPS_NOTE = (
    "Named here so the gaps are visible rather than silent, each beside the event it belongs "
    "to. If you hold any of these, or know where they are posted, send them through the "
    "<a href=\"comment.html\">comment form</a> with the source stated."
)


CSS = r"""/* record: generated by tools/sync-record.py, do not hand-edit */
.chainnote,.regnote{font-size:14px;color:var(--ink2);max-width:76ch;margin:0 0 18px}
.event{display:grid;grid-template-columns:112px 1fr;gap:20px;padding:20px 0;border-top:1px solid var(--hair)}
.event:first-of-type{border-top:1.5px solid var(--ink)}
.ekey{font:650 12px var(--mono);color:var(--ink);line-height:1.6}
.ekey .yr,.ekey .pt{display:block;font-weight:400;color:var(--faint)}
.ekey .kd{display:block;margin-top:9px;font:650 9.5px var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--ink2)}
.ebody{min-width:0;max-width:72ch}
.ewhat{font-size:14.5px;color:var(--ink2);line-height:1.6;margin:0;max-width:none}
.ewhat b{color:var(--ink);font-weight:650}
.elabel{font:650 9.5px var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--faint);margin:16px 0 2px}
.elist{list-style:none;margin:0;padding:0;font-size:14px;color:var(--ink2)}
.elist li{padding:6px 0;border-top:1px solid var(--hair);line-height:1.55}
.elist li:first-child{border-top:none}
.elist b{color:var(--ink);font-weight:650}
.elist .w{font:12px var(--mono);color:var(--ink2)}
.elist .none{color:var(--faint)}
.esaid{margin-top:14px;border-left:2px solid var(--hair);padding-left:14px}
.esaid>summary{list-style:none;cursor:pointer;font:650 9.5px var(--mono);letter-spacing:.15em;text-transform:uppercase;color:var(--ink2);padding:2px 0}
.esaid>summary::-webkit-details-marker{display:none}
.esaid>summary::after{content:"\25B8";color:var(--faint);padding-left:5px}
.esaid[open]>summary::after{content:"\25BE"}
.ebasis{font-size:13px;color:var(--faint);line-height:1.55;margin:8px 0 2px;max-width:70ch}
.tscroll{overflow-x:auto}
.event,#documents,#gaps,.reg tbody tr,#gaps tbody tr{scroll-margin-top:70px}
.reg .fn{display:block;font:11.5px var(--mono);color:var(--faint);overflow-wrap:anywhere;margin-top:3px}
.reg .sup{display:block;font-size:12.5px;color:var(--ink2);line-height:1.5;margin-top:5px}
.reg td:nth-child(2){white-space:nowrap}
@media(max-width:620px){
  .event{grid-template-columns:1fr;gap:8px;padding:18px 0}
  .ekey{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline}
  .ekey .yr,.ekey .pt,.ekey .kd{display:inline;margin:0}
}
/* /record */"""


# ---------------------------------------------------------------------------

BY_SLUG = {d["slug"]: d for d in DOCUMENTS}
BY_ID = {e["id"]: e for e in EVENTS}
BY_GAP = {g["id"]: g for g in GAPS}


def validate():
    """Fail on a reference that does not resolve, or an absence with no reciprocal."""
    problems = []
    if len(BY_SLUG) != len(DOCUMENTS):
        problems.append("two documents share a slug")
    if len(BY_ID) != len(EVENTS):
        problems.append("two events share an id")
    if len(BY_GAP) != len(GAPS):
        problems.append("two gaps share an id")

    for d in DOCUMENTS:
        if d["event"] not in BY_ID:
            problems.append(f"document {d['slug']} names event {d['event']}, which does not exist")
        if d["status"] == "superseded":
            if d.get("superseded_by") not in BY_SLUG:
                problems.append(f"document {d['slug']} is superseded by nothing that exists")
        elif d.get("superseded_by"):
            problems.append(f"document {d['slug']} is not superseded but names a successor")
        if d["status"] not in ("current", "superseded", "record"):
            problems.append(f"document {d['slug']} has status {d['status']!r}")
        if d["file"] and not os.path.exists(os.path.join(DOCS, d["file"])):
            problems.append(f"document {d['slug']} points at {d['file']}, which is not in docs/")

    for e in EVENTS:
        if e["kind"] not in ("meeting", "document", "filing", "scheduled"):
            problems.append(f"event {e['id']} has kind {e['kind']!r}")
        if not e["id"].startswith("e-" + e["date"]):
            problems.append(f"event {e['id']} does not carry its own date")
        for slug in e.get("attached", []):
            if slug not in BY_SLUG:
                problems.append(f"event {e['id']} attaches {slug}, which is not in the register")
        for gid in e.get("absent", []):
            if gid not in BY_GAP:
                problems.append(f"event {e['id']} states absence {gid}, which is not a gap row")

    # R7 both ways: a gap names its events, and each of those events says so.
    for g in GAPS:
        if not g["events"]:
            problems.append(f"gap {g['id']} names no event")
        for eid in g["events"]:
            if eid not in BY_ID:
                problems.append(f"gap {g['id']} names event {eid}, which does not exist")
            elif g["id"] not in BY_ID[eid].get("absent", []):
                problems.append(f"gap {g['id']} names event {eid}, which does not state the absence")

    order = [e["date"] for e in EVENTS]
    if order != sorted(order, reverse=True):
        problems.append("the chain is not in newest-first order")

    if problems:
        raise SystemExit("tools/sync-record.py: " + "; ".join(problems))


validate()


def long_date(iso):
    y, m, d = iso.split("-")
    return f"{MONTHS[int(m) - 1]} {int(d)}, {y}"


def short_date(iso):
    y, m, d = iso.split("-")
    return f"{MONTHS[int(m) - 1]} {int(d)}"


def key_date(iso):
    y, m, d = iso.split("-")
    return MONTHS[int(m) - 1][:3].upper() + " " + str(int(d)), y


def doc_link(d, text=None):
    """A document as a link where the site holds it, as plain text where it does not."""
    label = text or d["name"]
    if not d["file"]:
        return label
    return (f'<a href="{d["file"]}" target="_blank" rel="noopener" '
            f'data-cite="{d["cite"]}">{label}</a>')


def render_event(e):
    day, year = key_date(e["date"])
    out = [f'      <section class="event" id="{e["id"]}">']
    key = [f'<b>{day}</b><span class="yr">{year}</span>']
    if e.get("part"):
        key.append(f'<span class="pt">{e["part"]}</span>')
    key.append(f'<span class="kd">{e["kind"].capitalize()}</span>')
    out.append('        <div class="ekey">' + "".join(key) + "</div>")
    out.append('        <div class="ebody">')
    out.append(f'          <p class="ewhat">{e["what"]}</p>')

    if e.get("changed"):
        out.append('          <p class="elabel">What changed</p>')
        out.append('          <ul class="elist">')
        for text, href, label in e["changed"]:
            where = f' <a class="w" href="{href}">{label}</a>' if href else ""
            out.append(f"            <li>{text}{where}</li>")
        out.append("          </ul>")

    if e.get("said"):
        s = e["said"]
        out.append('          <details class="esaid">')
        out.append("            <summary>Who said what</summary>")
        out.append(f'            <p class="ebasis">{s["basis"]}</p>')
        out.append('            <ul class="elist">')
        for line in s["lines"]:
            out.append(f"              <li>{line}</li>")
        out.append("            </ul>")
        out.append("          </details>")

    attached = e.get("attached", [])
    absent = e.get("absent", [])
    if attached or absent:
        out.append('          <p class="elabel">Attached</p>')
        out.append('          <ul class="elist">')
        for slug in attached:
            d = BY_SLUG[slug]
            out.append(f'            <li>{doc_link(d)}. {d["notes"]}. '
                       f'<a class="w" href="#doc-{slug}">In the register</a></li>')
        for gid in absent:
            g = BY_GAP[gid]
            out.append(f'            <li class="none">{g["at_event"]} '
                       f'<a class="w" href="#{gid}">In the gaps register</a></li>')
        out.append("          </ul>")

    if e.get("deeper"):
        out.append('          <p class="elabel">The account in full</p>')
        out.append('          <ul class="elist">')
        for href, label in e["deeper"]:
            out.append(f'            <li><a href="{href}">{label}</a></li>')
        out.append("          </ul>")

    out.append("        </div>")
    out.append("      </section>")
    return "\n".join(out)


def render_chain():
    body = "\n".join(render_event(e) for e in EVENTS)
    return (
        '    <section>\n'
        '      <p class="seclabel">The chain</p>\n'
        f'      <p class="chainnote">{CHAIN_NOTE}</p>\n'
        f"{body}\n"
        "    </section>"
    )


def render_register():
    rows = []
    for d in DOCUMENTS:
        # The file name, so a reader can match a row to what they downloaded. A
        # document the site does not publish has none; its Notes cell says so.
        fn = f'<span class="fn">{os.path.basename(d["file"])}</span>' if d["file"] else ""
        if d["status"] == "current":
            status = '<span class="mark blue">Current</span>'
        elif d["status"] == "superseded":
            s = BY_SLUG[d["superseded_by"]]
            status = ('<span class="mark gray">Superseded</span>'
                      f'<span class="sup">by the {s["name"].lower()}, '
                      f'<a href="#doc-{s["slug"]}">{long_date(s["date"])}</a></span>')
        else:
            status = '<span class="mark gray">Record</span>'
        rows.append(
            f'          <tr id="doc-{d["slug"]}">\n'
            f'            <td>{doc_link(d)}{fn}</td>\n'
            f'            <td><a href="#{d["event"]}">{long_date(d["date"])}</a></td>\n'
            f'            <td>{d["what"]}</td>\n'
            f"            <td>{status}</td>\n"
            f'            <td>{d["notes"]}</td>\n'
            "          </tr>"
        )
    return (
        '    <section id="documents">\n'
        '      <p class="seclabel">Document register</p>\n'
        f'      <p class="regnote">{REGISTER_NOTE}</p>\n'
        '      <div class="tscroll">\n'
        '      <table class="data reg">\n'
        "        <thead><tr><th>Document</th><th>Date</th><th>What it is</th>"
        "<th>Status</th><th>Notes</th></tr></thead>\n"
        "        <tbody>\n" + "\n".join(rows) + "\n"
        "        </tbody>\n"
        "      </table>\n"
        "      </div>\n"
        "    </section>"
    )


def render_gaps():
    rows = []
    for g in GAPS:
        links = [f'<a href="#{eid}">{short_date(BY_ID[eid]["date"])}</a>' for eid in g["events"]]
        if len(links) > 1:
            where = ", ".join(links[:-1]) + " and " + links[-1]
        else:
            where = links[0]
        where += ", " + BY_ID[g["events"][-1]]["date"][:4]
        rows.append(
            f'          <tr id="{g["id"]}">\n'
            f'            <td>{g["name"]}</td>\n'
            f'            <td>{g["means"]}</td>\n'
            f"            <td>{where}</td>\n"
            '            <td><span class="mark gray">Absent</span></td>\n'
            "          </tr>"
        )
    return (
        '    <section id="gaps">\n'
        '      <p class="seclabel">Documents this site does not hold</p>\n'
        f'      <p class="regnote">{GAPS_NOTE}</p>\n'
        '      <div class="tscroll">\n'
        '      <table class="data">\n'
        "        <thead><tr><th>Document</th><th>What its absence means</th>"
        "<th>The event it belongs to</th><th>Status</th></tr></thead>\n"
        "        <tbody>\n" + "\n".join(rows) + "\n"
        "        </tbody>\n"
        "      </table>\n"
        "      </div>\n"
        "    </section>"
    )


BLOCKS = [
    ("/* record: generated by tools/sync-record.py, do not hand-edit */", "/* /record */", CSS),
    ("<!-- record chain: generated by tools/sync-record.py, do not hand-edit -->",
     "<!-- /record chain -->", None),
    ("<!-- record register: generated by tools/sync-record.py, do not hand-edit -->",
     "<!-- /record register -->", None),
    ("<!-- record gaps: generated by tools/sync-record.py, do not hand-edit -->",
     "<!-- /record gaps -->", None),
]


def render(src):
    """Return record.html with all four generated regions rewritten."""
    bodies = [CSS, render_chain(), render_register(), render_gaps()]
    for (open_mark, close_mark, _), body in zip(BLOCKS, bodies):
        pattern = re.compile(re.escape(open_mark) + r".*?" + re.escape(close_mark), re.S)
        if not pattern.search(src):
            raise SystemExit(f"tools/sync-record.py: record.html has no {open_mark} block")
        if open_mark.startswith("/*"):
            replacement = body
        else:
            replacement = open_mark + "\n" + body + "\n" + close_mark
        src = pattern.sub(lambda _: replacement, src, count=1)
    return src


def stale():
    """True when record.html no longer matches the data here."""
    src = open(PAGE).read()
    return render(src) != src


def main():
    check = "--check" in sys.argv
    src = open(PAGE).read()
    new = render(src)
    if new == src:
        print("in sync     record.html")
        print("\n%d events, %d documents, %d gaps." % (len(EVENTS), len(DOCUMENTS), len(GAPS)))
        return 0
    if check:
        print("STALE       record.html")
        print("\nrecord.html is stale. Run without --check to fix.")
        return 1
    open(PAGE, "w").write(new)
    print("updated     record.html")
    print("\n%d events, %d documents, %d gaps." % (len(EVENTS), len(DOCUMENTS), len(GAPS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

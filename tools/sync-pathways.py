#!/usr/bin/env python3
"""Generate the starting-license picker and the five panels on docs/pathways.html.

pathways.html is the one page organized by the reader's own situation: pick a
starting license, and every step to each permit it opens is listed with its
status, its citation, and what the committee recommendation would change. All of
it used to be built by JavaScript into two empty divs, which meant browser find
found nothing, a search engine indexed nothing, and a reader without JavaScript
was handed a pointer to another page instead of the routes.

This script owns that data and writes every panel into the page, in the manner
of tools/build-rule-page.py. Three structures hold it once:

    PERMITS   the four routes, each an ordered list of steps; a step carries its
              text, its status, its flag word, its why-line, its citation, the
              committee recommendation's change to it, and whether it points at
              the working model of the hours
    STARTS    the five starting licenses, each with the verdict on every permit
              and the eligibility band its rows sit in
    STATE     the four verdict words and the classes that carry them

The page then holds every panel and every route's step list at once. The script
at the foot of the page no longer renders anything; it moves the selection, and
the CSS this script generates narrows the page to the selected starting license
and the selected route. Without JavaScript nothing is narrowed, so every panel
and every step stays in view and browser find reaches all of it. The one-line
script in the head marks the document as scripted before anything paints, so a
reader with JavaScript never sees the page collapse from five panels to one.

The selection is also in the URL. The location hash carries #start=<id>, or
#start=<id>&permit=<key> when the shown route is not the starting license's
first, so the visible state is always a shareable address. Three parts carry
it, and the two that know the valid ids and keys are generated here so they
cannot drift from the data:

    the head script, hand-held in the page, veils the picker and the panels
    with one class when the hash looks like a state, so a shared link never
    flashes the default before the state applies;
    a script this file writes directly after the panels applies the hash
    against what the panels actually hold, then lifts the veil; a value the
    panels do not hold falls through to the default with no error;
    the foot script, hand-held in the page, rewrites the hash with
    history.replaceState on every selection.

Without JavaScript the hash is inert: the veil class is never added, nothing
is narrowed, and the page reads in full as before.

Three regions of docs/pathways.html are generated, each between its own markers,
and nothing outside them is touched: the selection rules in the page's
stylesheet, the picker at #starts, and the panels at #panel with the
state-applying script beside them.

tools/check-site.py imports this module and calls stale() to fail the build if
the page no longer matches the data here.

Usage:
    python3 tools/sync-pathways.py           # write the three blocks into the page
    python3 tools/sync-pathways.py --check   # exit 1 if pathways.html is stale
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
PAGE = os.path.join(DOCS, "pathways.html")

# The published rule, cited by page, and the July 9 meeting transcript. Every
# step's citation is built from one of these two.
J7 = "documents/rules-draft-2026-08-25-published.pdf#page="
J72 = "documents/rules-7.35.2-amendments-2026-08-25-published.pdf#page=3"
T7 = "documents/NMMPAB-2026-07-09-transcript.pdf"


def L(text, href):
    """A citation link, opening the source in a new tab."""
    return f'<a href="{href}" target="_blank">{text}</a>'


# ---------------------------------------------------------------------------
# The four routes. A step's keys:
#
#   t      the requirement, as the reader meets it
#   s      set | open | chal, which sets the step's status treatment
#   flag   the word on the status pill, on open and contested steps only
#   why    why the step is open or contested, or what the published text does
#          and does not say
#   src    the citation, built with L()
#   metz   what the committee recommendation, at its August 21 position, would change
#   model  1 where the step states hours the working model on hours.html exists
#          to move
#
# `dot` is a per-permit colour the page has never rendered. It is kept because
# it is data the page carried, not because anything reads it.
# ---------------------------------------------------------------------------

PERMITS = {
    "dc": {
        "name": "Certifying Clinician",
        "dot": "#256E8C",
        "steps": [
            {"t": "Hold a current NM professional license that permits diagnosing the qualifying "
                  "conditions (for example MD, NP).",
             "s": "set",
             "why": "New in the August 25 text: the license must permit diagnosis of the qualifying "
                    "conditions. The July 23 text gave examples without describing a scope.",
             "src": L("published rule 7.35.3.9, p.3", J7 + "3")},
            {"t": "Approved <b>certifying clinician training</b>: an 8-hour module covering pharmacology, "
                  "42 CFR Part 2, diagnosis of qualifying conditions, medical clearance, monitoring, and "
                  "data-collection requirements.",
             "s": "set",
             "src": L("published rule 7.35.3.18 (B), p.12", J7 + "12")},
            {"t": "Hold a <b>New Mexico Controlled Substance number</b> (state number, not the federal "
                  "DEA number).",
             "s": "set",
             "why": "Contested through June and July, and kept by the department on July 17. It stands "
                    "in the August 25 text, and the amended definition of certifying clinician in "
                    "7.35.2.7 carries the number inside it.",
             "src": L("published rule 7.35.3.9, p.3", J7 + "3") + " &middot; "
                    + L("July 17 update", "cs-number.html#update")},
            {"t": "<b>No practicum.</b>",
             "s": "set",
             "why": "The practicum section applies to practitioners and facilitators only; the "
                    "certifying clinician's packet lists no practicum item.",
             "src": L("published rule 7.35.3.19, p.13", J7 + "13") + " &middot; "
                    + L("7.35.3.9, p.3", J7 + "3")},
            {"t": "Apply to NMDOH. Certification is valid <b>2 years</b> from approval.",
             "s": "set",
             "src": L("published rule 7.35.3.9, p.2", J7 + "2")},
            {"t": "Continuing education: <b>8 CME hours every 2 years</b>.",
             "s": "set",
             "src": L("published rule 7.35.3.18 (G), p.13", J7 + "13")},
        ],
    },
    "recip": {
        "name": "Reciprocity",
        "dot": "#5A4A88",
        "steps": [
            {"t": "Trained and licensed outside New Mexico. Your program must be on <b>NMDOH's approved "
                  "reciprocity list</b>, which names Oregon and Colorado programs, or you must show your "
                  "program has other governmental approval and a curriculum substantially equivalent to "
                  "New Mexico's.",
             "s": "set",
             "src": L("published rule 7.35.3.10, p.4", J7 + "4") + " &middot; "
                    + L("7.35.3.19 (G), p.14", J7 + "14")},
            {"t": "Complete the <b>New Mexico Module</b>.",
             "s": "set",
             "src": L("published rule 7.35.3.18 (A), p.11", J7 + "11") + " &middot; "
                    + L("7.35.3.10, p.4", J7 + "4")},
            {"t": "Apply by the waiver deadline for a reduced practicum: at least <b>40 hours of contact "
                  "time</b> instead of the full practicum.",
             "s": "set",
             "why": "The published rule sets this deadline at December 31, 2027, unchanged since July "
                    "23. The July 9 draft still read December 31, 2026; the board moved it without "
                    "objection that day. Board chair Ian Dunn noted that date is a legislative "
                    "backstop, not the target date.",
             "src": L("published rule 7.35.3.10 (D), p.5", J7 + "5") + " &middot; "
                    + L("July 9 meeting transcript", T7)},
            {"t": "NMDOH may further reduce the practicum requirement at its discretion, to build the "
                  "program's initial infrastructure.",
             "s": "set",
             "why": "The published rule sets no end date for this discretion, at 7.35.3.19 (G). The "
                    "related waiver deadline is December 31, 2027. The August 25 text adds the same "
                    "discretion for the didactic requirements, at 7.35.3.18 (H).",
             "src": L("published rule 7.35.3.10 (D), p.5", J7 + "5") + " &middot; "
                    + L("July 9 meeting transcript", T7)},
            {"t": "Apply as practitioner or facilitator. The reciprocity application packet lists items "
                  "for those two permits only.",
             "s": "open", "flag": "Unresolved",
             "why": "The published rule is inconsistent here, unchanged in the August 25 text. "
                    "Reciprocity sits inside 7.35.3.10, which names certifying clinicians as eligible "
                    "to apply on the basis of a program from another jurisdiction, while the "
                    "application items listed there are for practitioners and facilitators.",
             "src": L("published rule 7.35.3.10, p.4", J7 + "4") + " &middot; "
                    + L("7.35.3.19, p.13", J7 + "13")},
        ],
    },
    "prac": {
        "name": "Practitioner",
        "dot": "#5A4A88",
        "steps": [
            {"t": "Hold a current NM professional license <b>to practice therapy, counseling, or "
                  "behavioral services</b> (for example PSY, LSW, LCSW).",
             "s": "set",
             "why": "New in the August 25 text: the license type is stated. The July 23 text gave "
                    "examples without describing a scope.",
             "src": L("published rule 7.35.3.9, p.3", J7 + "3")},
            {"t": "Certifications and attestation, same as Facilitator.",
             "s": "set",
             "src": L("published rule 7.35.3.18 (F), p.13", J7 + "13") + " &middot; " + L("pp.2-3", J7 + "2")},
            {"t": "Approved <b>practitioner training</b>: the 65-hour therapy module, at least one "
                  "third in person, with 10 hours of simulated patient experience, plus a 5-hour module "
                  "on psychedelic and psilocybin therapeutic approaches.",
             "s": "set",
             "why": "The August 25 text doubled the module: the July 23 text set 30 didactic hours "
                    "with 5 simulated patient hours.",
             "src": L("published rule 7.35.3.18 (C), p.12", J7 + "12") + " &middot; "
                    + L("7.35.3.18 (E), p.13", J7 + "13"),
             "metz": "The recommendation, at its August 21 position, sets the same 80-hour total, with "
                     "minimum hours in nine content areas and 2 simulated patient hours inside it; the "
                     "published text sets no per-area minimums and 10 simulated hours. The "
                     "recommendation also proposed renaming the roles, the practitioner to the "
                     "licensed provider and the certifying clinician to the medical screener; the "
                     "August 25 text keeps certifying clinician and practitioner."},
            {"t": "Practicum at a healing center or other approved location. Published rule: "
                  "<b>120 hours</b>.",
             "s": "open", "flag": "Open",
             "why": "Deferred to the Training and Education Committee by a 7-0 board vote July 17, "
                    "published unchanged July 23, and published unchanged again August 25, now with a "
                    "case-presentation evaluation, a low-risk requirement on the first 20 hours, and a "
                    "qualifying-condition diversity requirement inside the total. Public comment "
                    "continues through the October 2 hearing.",
             "src": L("published rule 7.35.3.19 (A), pp.13-14", J7 + "13"),
             "model": 1,
             "metz": "114 hours, staged: the facilitator sequence of 102 plus 12 provider supervisory "
                     "hours, with an 18-hour case presentation and consultation group inside the "
                     "total. The published text takes the two-case presentation, evaluated by the "
                     "practicum supervisor at 7.35.3.19 (C), without the 18-hour consultation group."},
            {"t": "Includes an additional <b>20 hours supervising facilitators</b> during administration "
                  "day sessions.",
             "s": "chal", "flag": "Contested",
             "why": "Dr. Anne Metz asked to make this optional at the June 25 committee meeting. The "
                    "department kept it in the July 23 text and again in the August 25 text. The 20 "
                    "hours sit inside the 120 rather than adding to them.",
             "src": L("published rule 7.35.3.19 (D), p.14", J7 + "14") + " &middot; "
                    + L("committee meeting, 6/25", "changes.html"),
             "metz": "Becomes 12 provider supervisory hours, a stage of the staged practicum."},
            {"t": "Mentoring: <b>10 hours</b> after graduation and after the practicum.",
             "s": "set",
             "src": L("published rule 7.35.3.17 (A), p.11", J7 + "11"),
             "metz": "Removed as a separate step: the recommendation closes the practicum with an "
                     "18-hour case presentation and consultation group inside the practicum total, with "
                     "sign-off requiring two presented cases the permittee personally provided. The "
                     "August 25 text keeps the mentoring and adds its own two-case evaluation inside "
                     "the practicum."},
            {"t": "Apply to NMDOH. Certification is valid <b>2 years</b> from approval.",
             "s": "set",
             "src": L("published rule 7.35.3.9, p.2", J7 + "2")},
            {"t": "Continuing education: <b>20 hours every 2 years</b>. Keep BLS or CPR/AED current.",
             "s": "set",
             "src": L("published rule 7.35.3.18 (G), p.13", J7 + "13")},
        ],
    },
    "fac": {
        "name": "Facilitator",
        "dot": "#3E8E6E",
        "steps": [
            {"t": "Apply for certification. <b>No professional license required.</b>",
             "s": "set",
             "src": L("published rule 7.35.3.9 (F), p.3", J7 + "3")},
            {"t": "Certifications: <b>HIPAA, plus BLS, or (CPR and AED), or New Mexico EMT "
                  "licensure</b>. Attestation you are not a registered sex offender.",
             "s": "set",
             "src": L("published rule 7.35.3.18 (F), p.13", J7 + "13") + " &middot; "
                    + L("7.35.3.9, p.3", J7 + "3")},
            {"t": "Approved <b>facilitator training</b>: the 65-hour therapy module, at least one third "
                  "in person, with 10 hours of simulated patient experience, plus a 5-hour "
                  "facilitator-specific module. Begins with the New Mexico Module, the one "
                  "module you cannot test out of.",
             "s": "set",
             "why": "The August 25 text doubled the module: the July 23 text set 30 didactic hours "
                    "with 5 simulated patient hours.",
             "src": L("published rule 7.35.3.18 (A), p.11", J7 + "11") + " &middot; "
                    + L("7.35.3.18 (C), p.12", J7 + "12") + " &middot; "
                    + L("7.35.3.17 (B), p.11", J7 + "11"),
             "metz": "The recommendation, at its August 21 position, sets the same 80-hour total, with "
                     "minimum hours in nine content areas and 2 simulated patient hours inside it; the "
                     "published text sets no per-area minimums and 10 simulated hours. The New Mexico "
                     "module stays required of every role, with no exemption by reciprocity."},
            {"t": "Practicum at a healing center or other approved location. Published rule: "
                  "<b>100 hours</b>.",
             "s": "open", "flag": "Open",
             "why": "Deferred to the Training and Education Committee by a 7-0 board vote July 17, "
                    "published unchanged July 23, and published unchanged again August 25, now with a "
                    "case-presentation evaluation, a low-risk requirement on the first 20 hours, and a "
                    "qualifying-condition diversity requirement inside the total. Public comment "
                    "continues through the October 2 hearing.",
             "src": L("published rule 7.35.3.19 (A), pp.13-14", J7 + "13"),
             "model": 1,
             "metz": "102 hours, staged: 24 with well participants, 24 co-facilitating with a "
                     "department-permitted licensed provider, 12 of group work, and 42 of supervised "
                     "practice on two cases, with an 18-hour case presentation and consultation group "
                     "inside the total, and every stage spanning preparation, administration, and "
                     "integration. The published text takes the two-case presentation without the "
                     "consultation group, and the department stated on August 21 that the statute "
                     "does not allow a well-participants stage."},
            {"t": "Mentoring: <b>10 hours</b> after graduation and after the practicum.",
             "s": "set",
             "src": L("published rule 7.35.3.17 (A), p.11", J7 + "11"),
             "metz": "Removed as a separate step: the recommendation closes the practicum with an "
                     "18-hour case presentation and consultation group inside the practicum total, with "
                     "sign-off requiring two presented cases the permittee personally provided. The "
                     "August 25 text keeps the mentoring and adds its own two-case evaluation inside "
                     "the practicum."},
            {"t": "Apply to NMDOH. Certification is valid <b>2 years</b> from approval.",
             "s": "set",
             "src": L("published rule 7.35.3.9, p.2", J7 + "2")},
            {"t": "Continuing education: <b>20 hours every 2 years</b>. Keep BLS or CPR/AED current.",
             "s": "set",
             "src": L("published rule 7.35.3.18 (G), p.13", J7 + "13")},
        ],
    },
    "hc": {
        "name": "Healing Center",
        "dot": "#1F7A5A",
        "steps": [
            {"t": "<b>No license, training, or examination is required of the applicant.</b> The "
                  "healing center is the one certification in this rule that any person may apply "
                  "for. &ldquo;Person&rdquo; is defined to include a natural person as well as a "
                  "corporation, partnership, or limited liability company, so an individual may hold "
                  "it. The center itself is certified; the people who work in it are certified "
                  "separately.",
             "s": "set",
             "why": "Compare the practitioner and facilitator applications at 7.35.3.9, which require "
                    "a professional license, completed practicum, life support certification, and "
                    "HIPAA training. None of that attaches here.",
             "src": L("published rule 7.35.3.11 (A), p.5", J7 + "5") + " &middot; "
                    + L("7.35.2.7 definition of person", J72)},
            {"t": "<b>Stand up the business.</b> Register with the New Mexico secretary of state and "
                  "with taxation and revenue, and obtain any business licenses your city or county "
                  "requires.",
             "s": "set",
             "src": L("published rule 7.35.3.11 (A)(4) to (6), p.5", J7 + "5")},
            {"t": "<b>Secure the premises.</b> A certificate of occupancy for each New Mexico location "
                  "where you will operate, and either proof that you own the property or a signed "
                  "written statement from the owner acknowledging that people will be participating "
                  "in the medical psilocybin program there and what they are authorized to do.",
             "s": "open", "flag": "Contested",
             "why": "The same owner-statement instrument governs treatment at a patient's home under "
                    "Subsection B, where it means a renting patient needs the landlord's signature "
                    "before being treated at home. Landlord approval and patient privacy were raised "
                    "at the August 21 committee meeting and the chair called it a subject to be "
                    "discussed further. Public comment continues through the October 2 hearing.",
             "src": L("published rule 7.35.3.11 (A)(7) and (8), p.5", J7 + "5")},
            {"t": "<b>Make the location safe and reachable.</b> Proof of compliance with disability "
                  "access law, proof of a working communication device that reliably reaches emergency "
                  "medical services, a plan for secured storage of the psilocybin, and a plan for "
                  "wastage of what is not used.",
             "s": "set",
             "src": L("published rule 7.35.3.11 (A)(9), (16), (17), (20), pp.5-6", J7 + "5")},
            {"t": "<b>Write the operating plans.</b> Record retention; patient confidentiality, which "
                  "the list asks for twice at items (13) and (18); a safety and emergency response plan "
                  "covering adverse health event response and reporting; written complaint and "
                  "grievance procedures available to patients; and a plan for transparency and "
                  "disclosure of fees to patients.",
             "s": "set",
             "src": L("published rule 7.35.3.11 (A)(12) to (15), (18), (19), pp.5-6", J7 + "5")},
            {"t": "<b>If sessions will happen outdoors</b>, add a detailed description of the outdoor "
                  "area identifying safe entrances and exits and verifying it is free of hazards, an "
                  "emergency safety and response plan, and proof that emergency medical services can "
                  "be contacted from the location and can respond to it.",
             "s": "set",
             "why": "A separate operating duty applies once you are running: a natural-environment "
                    "setting 15 minutes or more from emergency services needs a first aid kit, an AED, "
                    "and two people present holding wilderness first aid, wilderness first responder, "
                    "or New Mexico emergency medical technician credentials.",
             "src": L("published rule 7.35.3.11 (A)(21), p.6", J7 + "6") + " &middot; "
                    + L("7.35.3.20 (K), p.16", J7 + "16")},
            {"t": "<b>Name everyone.</b> An organizational chart of governance and operations, a list "
                  "of all owners or board members with contact information, the primary program "
                  "contact, a list of all employees by legal name, and the contact details of any "
                  "affiliated practitioners or facilitators.",
             "s": "set",
             "why": "The employee list matters twice over: 7.35.3.14 (C) grants medicine-handling "
                    "authority to owners and employees &ldquo;who are registered with the "
                    "department,&rdquo; and no section of the rule creates that registration. The "
                    "application list is the nearest thing the rule has to one.",
             "src": L("published rule 7.35.3.11 (A)(2), (3), (10), (11), (22), pp.5-6", J7 + "5")},
            {"t": "<b>Sign the affirmations.</b> Consent to publication of the center's contact "
                  "information if certified, an affirmation that everything submitted is true and "
                  "accurate, an attestation that no person associated with the applicant is registered "
                  "as a sex offender in any jurisdiction, and the authorized representative's signature "
                  "and date.",
             "s": "set",
             "src": L("published rule 7.35.3.11 (A)(23), (24), p.6", J7 + "6")},
            {"t": "<b>Submit and wait.</b> The whole application goes through the department's "
                  "electronic system. <b>The rule sets no application or certification fee</b>, here or for "
                  "any other certification; the only fees it names are the ones a center discloses to "
                  "patients and the ones an educational program charges students. Certification takes "
                  "effect the day the department issues it "
                  "and runs <b>two years</b>.",
             "s": "set",
             "why": "If the application is denied the department gives notice within 30 calendar days, "
                    "and you may re-apply after six months. A second denial means another six months. "
                    "A denial may be appealed.",
             "src": L("published rule 7.35.3.11 (D), pp.6-7", J7 + "6")},
            {"t": "<b>You cannot run a session alone.</b> The center holds the certification, but an "
                  "administration session needs certified people in the room: at least one practitioner "
                  "and one facilitator for an individual session, and for a group session one "
                  "practitioner for every eight patients and one facilitator or qualified student for "
                  "every two.",
             "s": "open", "flag": "Open",
             "why": "Read literally the individual-session rule requires exactly one of each, so two "
                    "practitioners would not satisfy it. The department may waive or decrease the ratio "
                    "if it finds the ratio is a barrier for patients and safety concerns are otherwise "
                    "alleviated.",
             "src": L("published rule 7.35.3.20 (H)(5), p.16", J7 + "16")},
            {"t": "<b>Then the operating duties begin</b>, and they are in a different section from "
                  "the application. Fourteen of them: keep a list of qualified patients and a daily log, "
                  "no firearms on the premises, consumption only on the premises, limit who may be "
                  "present, display the certification publicly, give patients specified information, "
                  "maintain the safety plan and provide it to everyone who uses the location, storage "
                  "rules, adverse health event reporting, and record access for the department.",
             "s": "set",
             "why": "An applicant reading only 7.35.3.11 would not meet most of this. The obligations "
                    "that decide how the center actually runs live at 7.35.3.20.",
             "src": L("published rule 7.35.3.20, pp.15-17", J7 + "15")},
            {"t": "<b>Renew every two years</b>, filing the renewal packet no more than 60 and no less "
                  "than 30 calendar days before the certification expires.",
             "s": "set",
             "src": L("published rule 7.35.3.11 (C), p.6", J7 + "6")},
            {"t": "<b>One ownership rule, and one silence.</b> A certificant, or a person who owns part "
                  "of one, may not hold an ownership interest in a permittee, which means a psilocybin "
                  "producer or a testing laboratory. The rule says nothing about whether a certifying "
                  "clinician, practitioner, or facilitator may own a healing center.",
             "s": "open", "flag": "Unresolved",
             "why": "The wall the rule builds runs between treatment and supply, not inside treatment. "
                    "No provision permits a provider to own a center and none forbids it, so a person "
                    "deciding whether to invest has nothing in the text to rely on. Nothing in the rule "
                    "addresses a certifying clinician certifying a patient into a center the clinician "
                    "holds an interest in.",
             "src": L("published rule 7.35.3.23, p.18", J7 + "18")},
        ],
    },
}

# ---------------------------------------------------------------------------
# The five starting licenses, in the order the picker offers them. `elig` is the
# band on eligibility.html whose rows this profile summarizes; `cs` marks the
# two profiles whose certifying-clinician verdict turns on the
# controlled-substance number. Routes are listed in the order they are shown,
# and the first route that is not a dead end is the one whose steps open.
# ---------------------------------------------------------------------------

STARTS = [
    {"elig": "band-community", "id": "none", "title": "No health license",
     "ex": "Community, peer, lived experience, chaplain, hospice, spiritual care, end-of-life doula "
           "(death doula), traditional healer.",
     "routes": [
         {"permit": "dc", "state": "nopath", "line": "Needs a NM professional license."},
         {"permit": "prac", "state": "nopath", "line": "Needs a NM professional license."},
         {"permit": "fac", "state": "open",
          "line": "No professional license required. An end-of-life doula enters here, on the same "
                  "terms as any other applicant. The rule gives a doula no permit or scope of their "
                  "own; it allows any other individual to be present at an administration session on "
                  "each patient's prior written consent, at 7.35.3.20 (D)."},
         {"permit": "hc", "state": "open",
          "line": "Open to anyone. The rule sets no license, training, or examination for the applicant; the certification is held by the center, and the people who work in it are certified separately."},
     ]},
    {"elig": "band-behavioral", "cs": True, "id": "therapy", "title": "Therapy or counseling license",
     "ex": "Psychologist, LCSW, LPCC, LMFT, psychiatric NP.",
     "routes": [
         {"permit": "dc", "state": "part",
          "line": "Only with a NM Controlled Substance number, and the August 25 text requires a "
                  "license that permits diagnosing the qualifying conditions. The number requirement "
                  "was contested and kept by the department on July 17."},
         {"permit": "prac", "state": "open", "line": "Direct route."},
         {"permit": "fac", "state": "open", "line": "Also open. No license needed for this one."},
         {"permit": "hc", "state": "open",
          "line": "Open. No license is required of the applicant, and holding one adds nothing to this application."},
     ]},
    {"elig": "band-medical", "cs": True, "id": "diagnose", "title": "License to diagnose",
     "ex": "Physician (MD/DO), psychiatrist, nurse practitioner, physician assistant.",
     "routes": [
         {"permit": "dc", "state": "open",
          "line": "Direct route, for a licensee holding a NM Controlled Substance number, a "
                  "requirement the department kept on July 17."},
         {"permit": "prac", "state": "part",
          "line": "Requires a license to practice therapy, counseling, or behavioral services, "
                  "stated in the August 25 text (examples PSY, LSW, LCSW)."},
         {"permit": "fac", "state": "open", "line": "Also open."},
         {"permit": "hc", "state": "open",
          "line": "Open. No license is required of the applicant, and holding one adds nothing to this application."},
     ]},
    {"elig": "band-otherhealth", "id": "otherhealth", "title": "Other health license",
     "ex": "Registered nurse, pharmacist, licensed massage therapist. No diagnosis or therapy scope.",
     "routes": [
         {"permit": "dc", "state": "nopath", "line": "Needs a diagnosing license."},
         {"permit": "prac", "state": "nopath", "line": "Needs a therapy license."},
         {"permit": "fac", "state": "open", "line": "Direct route."},
         {"permit": "hc", "state": "open",
          "line": "Open. No license is required of the applicant, and holding one adds nothing to this application."},
     ]},
    {"elig": "endoflife-roles", "id": "palliative", "title": "A specialty rather than a license",
     "ex": "Palliative care specialist, hospice clinician, and anyone whose field of practice is not "
           "itself a New Mexico license.",
     "routes": [
         {"permit": "dc", "state": "part",
          "line": "Set by the license held. A hospice and palliative medicine physician or nurse "
                  "practitioner reads on the prescribing and medical group; a palliative care social "
                  "worker reads on the behavioral health group."},
         {"permit": "prac", "state": "part",
          "line": "Set by the license held. A palliative care social worker has a direct route; a "
                  "palliative care physician's license is not one to practice therapy, counseling, "
                  "or behavioral services, which the August 25 text requires for this permit."},
         {"permit": "fac", "state": "open",
          "line": "Open whatever license is held, because this route turns on no license at all. It is "
                  "the one route the whole palliative care team shares."},
         {"permit": "hc", "state": "open",
          "line": "Open. No license is required of the applicant, and holding one adds nothing to this application."},
     ]},
    {"elig": "band-outofstate", "id": "elsewhere", "title": "Trained outside New Mexico",
     "ex": "Out-of-state, international, or Tribal, Pueblo, and Nation programs NMDOH approves.",
     "routes": [
         {"permit": "recip", "state": "recip",
          "line": "Enter by reciprocity, as practitioner or facilitator."},
         {"permit": "dc", "state": "part",
          "line": "The published rule names certifying clinicians as eligible under 7.35.3.10, but the "
                  "application items listed there are for practitioners and facilitators. Unresolved in "
                  "the draft."},
         {"permit": "hc", "state": "open",
          "line": "Open. No New Mexico license is required of the applicant, but the location itself must be in New Mexico and carry a certificate of occupancy."},
     ]},
]

STATE = {
    "open": {"tag": "open", "cls": "isopen", "lab": "Open"},
    "part": {"tag": "part", "cls": "part", "lab": "Partial"},
    "recip": {"tag": "recip", "cls": "recip", "lab": "By reciprocity"},
    "nopath": {"tag": "nopath", "cls": "nopath", "lab": "No current path"},
}


# ---------------------------------------------------------------------------
# Rendering. Nothing here breaks a line inside an element: newlines separate
# block-level siblings only, so no whitespace is added where it would render.
# ---------------------------------------------------------------------------

def live_routes(st):
    """The permits this starting license opens, in the order they are shown."""
    return [d["permit"] for d in st["routes"] if d["state"] != "nopath"]


def step_html(step, n):
    cls = "s-open" if step["s"] == "open" else ("s-chal" if step["s"] == "chal" else "s-set")
    flag = ""
    if step["s"] == "open":
        flag = '<span class="flag open">&#9670; ' + step["flag"] + "</span>"
    if step["s"] == "chal":
        flag = '<span class="flag chal">&#9660; ' + step["flag"] + "</span>"
    why = '<p class="why">' + step["why"] + "</p>" if step.get("why") else ""
    metz = ('<p class="metz"><span class="mz">If the committee recommendation is adopted</span>'
            + step["metz"] + "</p>") if step.get("metz") else ""
    model = ('<p class="model"><a href="hours.html">The working model of these hours</a></p>'
             if step.get("model") else "")
    return (f'<li class="step {cls}"><span class="num">{n}</span><div class="card">'
            f'<p class="txt">{step["t"]}</p>{flag}{why}{metz}{model}'
            f'<p class="src">{step.get("src", "")}</p></div></li>')


def journey_html(key, indent):
    pad = " " * indent
    items = "\n".join(pad + "  " + step_html(s, i + 1)
                      for i, s in enumerate(PERMITS[key]["steps"]))
    return pad + '<ol class="steps">\n' + items + "\n" + pad + "</ol>"


def route_html(d, active):
    S = STATE[d["state"]]
    label = ("Practitioner or Facilitator, by reciprocity" if d["permit"] == "recip"
             else PERMITS[d["permit"]]["name"])
    inner = (f'<div class="rb"><p class="rn">{label} '
             f'<span class="tag {S["tag"]}">{S["lab"]}</span></p>'
             f'<p class="rl">{d["line"]}</p></div>')
    if d["state"] == "nopath":
        return '<div class="route nopath">' + inner + "</div>"
    sel = d["permit"] == active
    return ('<button type="button" class="route ' + S["cls"] + (" sel" if sel else "")
            + '" data-k="' + d["permit"] + '" aria-pressed="' + ("true" if sel else "false")
            + '">' + inner + '<span class="rgo">'
            + ("Shown below" if sel else "View pathway &darr;") + "</span></button>")


def eligref_html(st):
    cs = (', and the certifying-clinician verdict turns on the '
          '<a href="cs-number.html">controlled-substance number</a>') if st.get("cs") else ""
    return ('These verdicts summarize the <a href="eligibility.html#' + st["elig"] + '">rows for this '
            'group in the eligibility tables</a>' + cs + ".")


def jhead_html(st, key):
    title = ("Pathway by reciprocity: Practitioner or Facilitator" if key == "recip"
             else "Pathway to the " + PERMITS[key]["name"] + " permit")
    route = next((r for r in st["routes"] if r["permit"] == key), None)
    line = '<p class="routeline">' + route["line"] + "</p>" if route else ""
    return "<h3>" + title + "</h3>" + line


def panel_html(st):
    """One starting license: the heading, the verdicts, the eligibility line, and
    the step list of every route it opens."""
    keys = live_routes(st)
    active = keys[0]
    out = [f'      <div class="youare" data-start="{st["id"]}">'
           f'<p class="k">Starting license</p><h2>{st["title"]}</h2></div>',
           f'      <div class="routes" data-start="{st["id"]}">']
    for d in st["routes"]:
        out.append("        " + route_html(d, active))
    out.append("      </div>")
    out.append(f'      <p class="eligref" data-start="{st["id"]}">{eligref_html(st)}</p>')
    out.append(f'      <div class="journeywrap" data-start="{st["id"]}" data-active="{active}" data-default="{active}">')
    for key in keys:
        out.append(f'        <div class="jhead" data-k="{key}">{jhead_html(st, key)}</div>')
        out.append(f'        <div class="jholder" data-k="{key}">')
        out.append(journey_html(key, 10))
        out.append("        </div>")
    out.append("      </div>")
    return "\n".join(out)


def render_picker():
    rows = []
    for i, st in enumerate(STARTS):
        on = " on" if i == 0 else ""
        rows.append(f'        <button type="button" class="start{on}" data-start="{st["id"]}">'
                    f'<span class="stt">{st["title"]}</span>'
                    f'<span class="stex">{st["ex"]}</span></button>')
    return ('      <div class="starts" id="starts">\n' + "\n".join(rows) + "\n      </div>")


def render_panels():
    return (f'    <div id="panel" data-current="{STARTS[0]["id"]}">\n'
            + "\n".join(panel_html(st) for st in STARTS)
            + "\n    </div>\n"
            + state_script())


def state_script():
    """The script that applies the location hash to the panels.

    It sits directly after the panels so it runs the moment they exist, before
    anything below them has parsed, which is what keeps a shared link from
    flashing the default view. It validates the hash against the panels
    themselves rather than against a second copy of the ids and keys: a start
    is real when a journey wrap carries it, a permit is real for that start
    when the wrap holds its journey head. Anything else falls through to the
    default silently. The last line always lifts the veil the head script may
    have raised, whether or not a state applied."""
    return """    <script>
    (function(){
      var h=document.documentElement;
      try{
        var m=/^#start=([a-z]+)(?:&permit=([a-z]+))?$/.exec(location.hash);
        var panel=document.getElementById('panel');
        var wrap=m&&panel?panel.querySelector('.journeywrap[data-start="'+m[1]+'"]'):null;
        if(wrap){
          panel.setAttribute('data-current',m[1]);
          var bs=document.querySelectorAll('#starts button.start');
          for(var i=0;i<bs.length;i++) bs[i].classList.toggle('on',bs[i].getAttribute('data-start')===m[1]);
          if(m[2]&&wrap.querySelector('.jhead[data-k="'+m[2]+'"]')){
            wrap.setAttribute('data-active',m[2]);
            var rs=panel.querySelectorAll('.routes[data-start="'+m[1]+'"] button.route');
            for(var j=0;j<rs.length;j++){
              var sel=rs[j].getAttribute('data-k')===m[2];
              rs[j].classList.toggle('sel',sel);
              rs[j].setAttribute('aria-pressed',sel?'true':'false');
              var go=rs[j].querySelector('.rgo');
              if(go) go.innerHTML=sel?'Shown below':'View pathway &darr;';
            }
          }
        }
      }catch(e){}
      h.classList.remove('hs');
    })();
    </script>"""


def render_css():
    """The rules that narrow the page to one starting license and one route.

    Every rule is gated on .js, which the one-line script in the head adds
    before the page paints. Without JavaScript no rule applies, every panel and
    every step stays in view, and browser find reaches all of it."""
    lines = ["  /* Every panel and every route's steps are in the page. These rules narrow it to",
             "     the selected starting license and the selected route, and they apply only when",
             "     JavaScript has marked the document. Without it, nothing is hidden. */",
             "  /* When the head script sees a state in the location hash it adds hs, and the",
             "     script after the panels applies the state and removes it, so a shared link",
             "     shows the arrived-at selection rather than a flash of the default. */",
             "  .js.hs #starts,.js.hs #panel{visibility:hidden;}"]
    for st in STARTS:
        i = st["id"]
        lines.append(f'  .js #panel[data-current="{i}"] [data-start]:not([data-start="{i}"])'
                     "{display:none;}")
    for key in sorted({k for st in STARTS for k in live_routes(st)}):
        lines.append(f'  .js .journeywrap[data-active="{key}"] [data-k]:not([data-k="{key}"])'
                     "{display:none;}")
    return "\n".join(lines)


BLOCKS = [
    ("/* pathways panels: generated by tools/sync-pathways.py, do not hand-edit */",
     "/* /pathways panels */", render_css),
    ("<!-- pathways picker: generated by tools/sync-pathways.py, do not hand-edit -->",
     "<!-- /pathways picker -->", render_picker),
    ("<!-- pathways panels: generated by tools/sync-pathways.py, do not hand-edit -->",
     "<!-- /pathways panels -->", render_panels),
]


def render(src):
    """Return pathways.html with all three generated regions rewritten."""
    for open_mark, close_mark, build in BLOCKS:
        pattern = re.compile(r"(?m)^([ \t]*)" + re.escape(open_mark) + r".*?"
                             + re.escape(close_mark), re.S)
        m = pattern.search(src)
        if not m:
            raise SystemExit(f"tools/sync-pathways.py: pathways.html has no {open_mark} block")
        pad = m.group(1)
        replacement = pad + open_mark + "\n" + build() + "\n" + pad + close_mark
        src = pattern.sub(lambda _: replacement, src, count=1)
    return src


def stale():
    """True when pathways.html no longer matches the data here."""
    src = open(PAGE).read()
    return render(src) != src


def main():
    check = "--check" in sys.argv
    src = open(PAGE).read()
    new = render(src)
    steps = sum(len(PERMITS[k]["steps"]) for st in STARTS for k in live_routes(st))
    tally = "\n%d starting licenses, %d routes, %d steps." % (
        len(STARTS), sum(len(live_routes(st)) for st in STARTS), steps)
    if new == src:
        print("in sync     pathways.html")
        print(tally)
        return 0
    if check:
        print("STALE       pathways.html")
        print("\npathways.html is stale. Run without --check to fix.")
        return 1
    open(PAGE, "w").write(new)
    print("updated     pathways.html")
    print(tally)
    return 0


if __name__ == "__main__":
    sys.exit(main())

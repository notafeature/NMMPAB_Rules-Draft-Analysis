#!/usr/bin/env python3
"""Keep the provenance block identical and current across every page in docs/.

Two things a reader needs and the site did not have:

1. The document chain. Four successive documents govern this subject. Each
   supersedes the one before it. A reader looking at a number on any page
   should be able to walk back and see where it came from and what changed at
   each step, without that history sprawling across the page.

   The chain is stated once, in the register at record.html#documents, whose
   data lives in tools/sync-record.py and is read from there by this script.
   The register holds each document's identity, date, status, and download; the
   block at the foot of a page names the current document, says what it changed,
   and links the register. It used to restate all four documents with their own
   download links, which put the same description of the same document on eight
   pages in different words, and that is the one document-link duplication on
   the site that serves no citation.

2. A per-page revision log. What was changed on this page, and when. Only
   index.html had one, buried in its footer.

Both live in a single collapsed <details> block at the foot of every page:
zipped up by default, opened when a reader wants it.

CHAIN is identical on every page. REVISIONS is per page, newest first.

Usage:
    python3 tools/sync-provenance.py           # write into every page
    python3 tools/sync-provenance.py --check   # exit 1 if any page is stale
"""
import glob
import importlib.util
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")

# The document chain lives in the register, in tools/sync-record.py, which is
# where record.html reads it from as well. This block used to carry its own copy
# of every document's date, name, and file, which is two homes for one fact and
# the drift pattern the register exists to end. What stays here is the one thing
# the register does not hold: what the current document changed, which is the
# chain narrative rather than the document's identity.
_spec = importlib.util.spec_from_file_location(
    "syncrecord", os.path.join(ROOT, "tools", "sync-record.py"))
syncrecord = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(syncrecord)

CHAIN = [d for d in syncrecord.DOCUMENTS if d.get("chain")]

CHANGED = {
    "rules-draft-2026-07-23-published":
        "The department's published proposed rule, and the text going to the August 28 hearing. "
        "First version with final section numbering, 7.35.3.1 through .28. Raised the shared "
        "didactic module from 25 hours to 30 and added three curriculum topics. Carried the 100 "
        "and 120 practicum hours forward unchanged, six days after the board voted 7-0 to send "
        "those hours back to committee. Wrote both waiver dates as December 31, 2027. Added a "
        "rule that the practicum may not begin before half the didactic and all simulated "
        "patient hours are complete.",
}

# Per-page revision entries, newest first. Keep each one specific: what changed,
# not that something changed.


REVISIONS = {
    "index": [
        ("July 25, 2026", "Title capitalisation corrected: the first word after the line break was lower case. Added the CSS rules for the section headings introduced with the document strip, which had none and were rendering unstyled."),
        ("July 25, 2026", "Rebuilt against the page review. The title read \"The rule is published\", which is a headline rather than a statement of fact, and now states that the rule hearing is August 28, 2026. \"What is next\" moved from mid-page into the hero, above \"Where things stand\". The open item now carries a red border and states that the committee recommendation needs to reach the department as soon as possible; it had been the site accent colour, which reads as decoration rather than attention. The \"Nothing on this page is final\" disclaimer moved into the footer. The document strip now carries a heading saying what it is, and the input tile was removed from it. The three lineage deep-dives on the controlled-substance number, the practicum and reciprocity were removed as history that belongs elsewhere, and the two in-page links into them were repointed to the practicum and draft pages. \"Find your way around\" moved to its own page at guide.html."),
        ("July 17, 2026", "Updated to the July 17 full Advisory Board meeting. The board voted 7-0 to defer the practicum and didactic hours to the Training and Education Committee."),
        ("July 10, 2026", "Parallel working drafts reconciled into this page. The July 9 meeting description corrected: it was an Advisory Board meeting, and the chair barred formal votes only after the scheduled adjournment."),
        ("July 9, 2026", "Updated to the outcome of the July 9 Advisory Board meeting. Reciprocity: both waiver deadlines extended to December 31, 2027. Practicum and didactic hours: tabled."),
    ],
    "training-hours-record": [
        ("August 13, 2026", "The status strip is re-scoped from live status to a dated record, and is now written by tools/sync-status.py, which holds the site's status facts once and writes every page that shows them. The strip's label now carries the date of the newest status change it states, currently July 27, and the strip closes by naming Where things stand as the page that holds the current state of the rulemaking, because a record page carrying a live status block is how this page came to say, for a day, that the committee recommendation was undelivered. The hero stamp read July 25 while the strip beneath it stated the July 27 submission; it now carries the date of this change."),
        ("July 28, 2026", "The page name is now the same in the title, the heading, and the menu: the training-hours record. The title had read \"Training Hours: The Tabled Numbers and the July 17 Decision\" and the heading \"Training hours\", which is the name of a different page."),
        ("July 25, 2026", "The specialization section moved off this page onto Specialized domains, which already held the same subject, so the two are no longer split across pages. What moved: the addendum framing, the core-baseline and end-of-life range cards, the nine-session curriculum table, and the questions left open for the training committee. What is left here is a pointer at the same anchor, so links in from other pages still land. Two boxes were dropped rather than moved, because Specialized domains already carried both: the four qualifying-condition domains as parallel options, and whether the hours belong in the core or in a separate add-on."),
        ("July 25, 2026", "Role tiles reordered to certifying clinician, practitioner, facilitator, as asked. The totals could not be reconciled with the rows above them: the tile listed 30, 5 and 5 while the total read \"35 + 100\". Totals now read \"35 didactic + 5 sim + 100 practicum\" and the rows name their units, so the arithmetic is visible."),
        ("July 25, 2026", "Page review applied. Removed the \"Purpose and how to read this page\" panel: a page that needs instructions for reading it has already failed. Added Dr. Anne Metz's proposed alternative permit title as a parenthetical under the Practitioner tile, since that is a separate recommendation that can be dropped without affecting the practicum work. Every entry in \"What changed on July 23\" now names its subsection in the sentence itself rather than relying on a link placed to one side."),
        ("July 25, 2026", "Brought current to the July 23 published rule. The page had no Updated date at all and was written in live-blog present tense from July 17: the Dr. Anne Metz presentation carried an \"In progress\" tag and a section was headed \"Open questions for July 17\". Role cards updated from the July 9 numbers to the published ones. Corrected two live errors: the in-state bridge deadline read June 30, 2027 and the reciprocity deadline read December 31, 2026, and both are December 31, 2027 in the published rule. Added a \"What changed on July 23\" summary."),
        ("July 17, 2026", "Added the live log of the July 17 Training and Education Committee meeting, including the Dr. Anne Metz presentation."),
    ],
    "history": [
        ("July 25, 2026", "Page review applied. The lede was rewritten: it had been describing itself rather than saying what the page holds. \"New here?\" was removed from the process explainer, which asked a reader to identify as a novice before being given an explanation."),
        ("July 25, 2026", "Two entries added: the July 23 publication of the proposed rule, and the July 17 afternoon Training and Education Committee meeting, which the page had omitted entirely while carrying the morning board meeting. The July 17 board entry is now labelled morning so the two are distinguishable. \"What is next\" replaced its stale July 17 contents with August 14, August 21, and the August 28 hearing. The \"How this process works\" explainer was moved out of the middle of the chronology, where it split the timeline into two lists, and now sits above it."),
        ("July 17, 2026", "Added the July 17 Advisory Board meeting: the 7-0 deferral, the department keeping the controlled-substance number, and the revised certifying-clinician exam language."),
    ],
    "pathways": [
        ("August 13, 2026", "The selection is now in the address. Picking a starting license, or a route under it, writes the choice into the URL as #start followed by the license's id, with &permit and the route's key added when the shown route is not that license's first, so the page a reader is looking at can be shared as a link and the link lands with the same panel and the same route open. A link carrying a value the page does not hold falls through to the default with nothing shown or hidden along the way. Without JavaScript the address changes nothing, and the page reads in full as before. The second table on Which licenses qualify links into these addresses from every verdict cell in the bands the starting licenses summarize."),
        ("August 13, 2026", "Every starting license, every route, and every step is now written into the page itself, by tools/sync-pathways.py, instead of being built by JavaScript when the page loads. Nothing a reader sees has changed: the profiles, the verdicts, the steps, the status flags, the citations, and the notes on what the committee recommendation would change all read exactly as before. What changed is that a browser's find command now reaches every step, a search engine can index them, and a reader without JavaScript is shown every starting license in turn, each with all of its routes, rather than a pointer to another page."),
        ("July 31, 2026", "A sixth starting point added, for a specialty that is not itself a New Mexico license, with the palliative care specialist and the hospice clinician as its examples. Its routes state that the certifying clinician and practitioner verdicts are set by the license the person holds, and that the facilitator route is open whatever license that is, because it turns on none. The end-of-life doula is named among the examples on the no-health-license start, where the facilitator route now states that a doula enters on the same terms as any other applicant and that the rule gives a doula no permit or scope, allowing any other individual to be present at an administration session on each patient's prior written consent at 7.35.3.20 (D). Three citations corrected on the practitioner and facilitator routes: the two practicum steps and the supervisory-hours step cited 7.35.3.18, and the practicum is 7.35.3.19, with the hour figures at Subsection A, pages 12 to 13, and the 20 supervisory hours at Subsection C, page 13, which sit inside the 120 rather than adding to them. The recommendation note on the two didactic steps read \"80 didactic hours in place of 35\" while the working model of the hours compared 80 against a module total of 40. The submission settles it: the recommendation page states its 80 across nine content areas running from 20 hours in core psychotherapy skills and ethics down to 2 hours in simulated patient work, so the 80 counts simulated patient hours inside the total exactly as the published 40 does. Both notes now say so and name the published 40 as the figure that compares."),
        ("July 28, 2026", "The two practicum steps, one on each of the practitioner and facilitator routes, now link the working model of the hours, which is where the quantities they state can be moved. The footer link to the record page read \"Recent developments\", a name that page no longer carries, and now reads \"Meetings and filings\". The page name is now the same in the title, the heading, and the menu: routes to a permit."),
        ("July 27, 2026", "Restored. The July 27 redesign merge replaced this page with a redirect; it returns unchanged from the July 25 version except for this: the committee recommendation is now recorded as submitted to the department on July 27 as a summary of the recommended rules, and the recommendation notes beneath the steps carry the submitted figures, 80 didactic hours, a 60 or 70 hour staged practicum by role, 20 hours of case presentation and consultation, and the renaming of practitioner to licensed provider, in place of the July 17 presentation ranges."),
        ("July 25, 2026", "Rebuilt. The page now says what it is in a lede, which it did not. Every step that the committee recommendation would change now shows the change directly beneath it, so a reader sees the published requirement and the proposed one together: 84 didactic hours in place of 35, a 62 or 72 hour scaffolded practicum in place of 100 or 120, supervisory hours from 20 to 10, and mentoring replaced by consultation with two presented cases. The certifying clinician route carries no such note, because the recommendation addresses facilitators and practitioners only and nothing on that route changes. The specialized-domain material from July 16 moved to its own page, and the JavaScript that rendered it was removed rather than left orphaned."),
        ("July 25, 2026", "Reviewed and brought current to the July 23 published rule. All route steps re-cited: the citation helper and 25 step links pointed at the superseded July 9 draft and now point at the published rule with section numbers. The practitioner core module was corrected from 25 hours to 30. \"Administration and same-day therapy sessions\" corrected to \"administration day sessions\". The status legend said the committee \"meets 1 PM today\" and now states that the hours were published unchanged on July 23 with the committee recommendation in progress. The reciprocity waiver step read December 31, 2026; the published rule reads December 31, 2027. The note about the draft's internal inconsistency on certifying-clinician reciprocity was rechecked against the published text, where reciprocity now sits inside 7.35.3.10, and the inconsistency persists."),
    ],
    "eligibility": [
        ("August 13, 2026", "The scope-test section now records the question the supervised tiers leave open: if a supervised licensee were certified as a practitioner, would the clinical supervisor their own board requires also need a permit under this program? No document and no meeting record held in this repository asks it. The published rule's supervision language sits entirely inside the program, the facilitator under the direct supervision of a practitioner at 7.35.3.13 (B) and the practicum supervision at 7.35.3.19, and never reaches the supervision a supervised license carries from its own licensing board. A starting point for the supervised tiers on Routes to a permit waits on that answer."),
        ("August 13, 2026", "Every verdict cell in the second table now carries a small route link into Routes to a permit, landing with the matching starting license selected, and with the matching route open where that page offers one. The prescribing and medical band lands on the license-to-diagnose start, the independent behavioral health band on the therapy-or-counseling start, the other-licensed-health band on the other-health-license start, the non-clinical and community band on the no-health-license start, the specialty band on the specialty start, and the out-of-state band on the trained-outside-New-Mexico start. Two rows leave their band's mapping because their verdicts do not: the psychiatric mental health nurse practitioner lands on the license-to-diagnose start, whose three verdicts match that row, and the psychiatric clinical nurse specialist on the therapy-or-counseling start. The supervised behavioral health band carries no route links, because no starting license on Routes to a permit summarizes a supervised tier. A cell graded No current path or Not specified, and any cell whose column that start does not open, links the starting license alone, because there is no route to show. The section on the end-of-life doula and the palliative care specialist links both of its readings the same way. Existing links on the cells, to the controlled-substance number page, the scope test, and that section, are kept beside the new ones."),
        ("July 31, 2026", "A section maps chaplains, pastoral counselors, and spiritual care, a group that sits outside the licensing system entirely. No state in the United States licenses, certifies, registers, or title-protects a chaplain, and New Mexico issues no chaplain credential of any kind; the national certifications are private and are made compulsory by hospitals rather than by governments. Pastoral counselor is a licensed title in six states, New Mexico is not among them, and contemporary accounts state those laws were passed principally so that pastoral counselors could bill insurance, which makes them a precedent about payment rather than competence. The certification a New Mexico statute once pointed at, from the American Association of Pastoral Counselors, no longer exists: that body stopped certifying and dissolved in March 2019 and no successor inherited the credential. Two New Mexico exemptions carry this population instead, one of which expressly covers practitioners of Native American healing arts, and neither is a route into this program because an exemption is permission to practice without a license rather than a license. The consequence under the rule is stated plainly: none of it qualifies a person and none of it disqualifies one, because the certifying clinician and practitioner routes need a New Mexico license that a national certification is not, and the facilitator route asks for no license at all, so a board certified chaplain and a person holding nothing stand in the same position. The section also records that the Board of Chaplaincy Certification already credits up to 7,200 hours of mentored study in place of a graduate degree for applicants trained in Buddhist and Indigenous traditions, which is a worked example of the recognition question the legacy pathway raises. The whole section carries Need source marks, because none of the underlying statutes or certifying-body standards is held in this repository and none has been read directly.")
        ,("July 31, 2026", "Two additions. The scope-test section now states who may issue a certification the rule asks for: the rule names an issuer only where it writes New Mexico, and every other credential it requires, being basic life support, cardiopulmonary resuscitation, automated external defibrillator, HIPAA, wilderness first aid and wilderness first responder, is named with no issuer at all. The words national, nationally and accredited appear nowhere in the 19 pages. That decides the question for anyone holding a national board certification rather than a state license: it cannot satisfy Paragraph (1) of Subsection D or E of 7.35.3.9, and it does not need to, because the facilitator route asks for no license. The role map gains the co-facilitation route. Nothing requires one person to hold the whole role, and Paragraph (5) of Subsection H of 7.35.3.20 already puts a practitioner and a facilitator in every individual session, with Subsection B of 7.35.3.13 setting the relationship. A traditional healer, chaplain, peer supporter or death doula can be the certified facilitator, which requires no license, working alongside a licensed practitioner, so the pair satisfies the rule where the individual does not. Two limits are stated with it: Subsection B of 7.35.3.13 bounds a facilitator to peer support and logistical and administrative support, and Subsection D of 7.35.3.19 still requires every practicum hour inside an approved location.")
        ,("July 31, 2026", "The page now maps every route into the program rather than the three permits alone. Table 2 gains eleven license rows: the professional art therapist, whose statutory scope is the licensed practice of counseling or therapy services and which therefore grades as a clinical counselor does; the alcohol and drug abuse counselor; the supervised tiers LMHC, LMHC-AS, LAMFT, LMSW and psychologist associate; LBSW and LSAA; the psychiatric nurse practitioner and clinical nurse specialist; the occupational therapist; and the certified peer support worker, certified community health worker, New Mexico-certified perinatal doula, and creative arts therapists other than art therapy. Two verdicts are added to the legend because the rule cannot express what New Mexico actually licenses. Supervised only marks a scope that reaches the work under a supervisor the rule never accounts for. One condition marks the alcohol and drug abuse counselor, whose scope reaches substance use disorder and expressly excludes mental health disorders, which makes it the first verdict on the site that runs by condition rather than by license. A section states the scope test itself, that it defers to each licensing board, that the published rule does not restate it, and that the controlled-substance number rather than scope is what holds the certifying column at Partial. A second section maps every role the rule names, grouped by how a person comes to hold it: certified on application; authorized to handle the medicine without being certified, which is the healing center owner and employee whose registration the rule never creates; required on site with a credential from somebody else, which is the wilderness first aid or EMT pair for remote outdoor sessions; engaged privately with criteria the department never checks, which is the third-party evaluator, the instructor, the certified faculty member and the practicum supervisor; present by the patient's consent; and named in the record with no route in the rule. The fourth class, admitted under 7.35.3.20 (D) as \"the other individual(s)\", is named in full for the first time: support person, space attendant, end-of-life doula, chaplain or religious leader, interpreter, caregiver, and traditional healer or elder, none of which appears anywhere in the rule, together with the four consequences that follow from the class being unnamed. The doula paragraph is rewritten around a fact that changes it: New Mexico credentials doulas under the Doula Credentialing and Access Act, with a registry and a Medicaid pathway, and scopes that certification to birth, so the end-of-life doula falls outside a framework that exists rather than one that does not. Anything asserted from a source this repository does not hold now carries a Need source mark, which is a legend entry of its own, so unfinished sourcing is visible on the page instead of being invisible.")
        ,("July 31, 2026", "Two starting points added that the second table did not carry. The end-of-life doula, also called the death doula, joins the non-clinical and community band, graded No current path for certifying clinician and practitioner and Eligible for facilitator: 7.35.3.9 (D) and (E) each require a current New Mexico professional license, New Mexico issues none for doulas, and 7.35.3.9 (F) requires no license at all. The palliative care specialist sits in a new band, a specialty rather than a license, because palliative care is a field of practice and the rule never grades a specialty. Its two licensed columns read By license held, a new verdict added to the legend, and its facilitator column reads Eligible. A section beneath the table reads both routes in full, names which existing row each kind of palliative care worker is read on, and records the second question separately: 7.35.3.20 (D) allows any other individual to be present at an administration session on each patient's prior written consent, while the rule gives neither role a permit, a scope, a training standard, or a place in the staffing ratio at 7.35.3.20 (H)(5). Larry Leeman named that gap at the July 16 End-of-Life Care committee meeting, and the rule published July 23 does not close it. A block above that section now states two limits on the second table. The rows are starting points rather than the set of New Mexico licenses, because no document in the chain lists licenses: the Act defines one provider role, 7.35.2 NMAC defines a practitioner as a licensed healthcare professional, the published rule gives parenthetical examples, and the only scope-of-practice test in the chain sits in the June 12 recommendation, which the published rule does not restate. And the certifying clinician column carries one verdict where the rule needs one per condition, because 7.35.3.8 (B)(8)(a) requires an attestation of a qualifying diagnosis and the qualifying conditions are not one kind of thing, so no behavioral health license establishes end-of-life care and that pathway is gated by a medical prognosis at its first step. Separately, the block on what the committee recommendation would change described its classroom figure as \"a single 80-hour standard\" without saying what it replaces or what it counts. It now states the published 40 it stands against, and that the submission spreads its 80 across nine content areas from 20 hours in core psychotherapy skills and ethics down to 2 hours in simulated patient work, so the two figures count the same things and compare directly."),
        ("July 28, 2026", "The hero stamp read July 25 while the block beneath the tables stated the July 27 submission, so the page disagreed with itself about its own date. The stamp now reads July 28 and says what the recommendation would change, that nothing in the tables changes unless the department adopts it, and links the block. The tooltip on the nine certifying-clinician verdict cells moved from the title attribute, which a touch device never shows, to the data-cite attribute the rest of the site uses for citation disclosure. The page name is now the same in the title, the heading, and the menu: which licenses qualify."),
        ("July 25, 2026", "Both tables re-ordered to certifying clinician, practitioner, facilitator, the order used on the other provider pages. Every hour figure and every eligibility pill was then checked against the published rule, and five things were wrong. The certifying clinician's prerequisites read \"License only\"; 7.35.3.9 (D) also requires HIPAA certification completed within the preceding two years and the sex-offender attestation, so the cell now names those and says the BLS, CPR and EMT requirement does not apply to that role. The approved-program row named only the role curricula; 7.35.3.18 (A) requires the New Mexico module of all three, so all three cells now name it. Both out-of-jurisdiction rows graded the certifying clinician column \"Not specified\"; 7.35.3.10 (B) names certifying clinician alongside practitioner and facilitator, so both are now Reciprocity, and the note under the table states how that route works instead of saying there is no packet for it. The source notes under both tables cited pages the material is not on: table 1 pointed at p.11 for content described as pp.4-9, and table 2 pointed at p.2 for entry credentials that are on p.3. Both now cite each subsection to its own page. The \"If the committee recommendation is adopted\" block appeared twice in a row; one copy was removed. Every remaining figure was confirmed correct: 8 didactic and 8 CME hours for the clinician, 30 shared and 5 role-specific didactic with 5 simulated patient hours, 100 and 120 practicum hours, 20 supervisory hours, 10 mentoring hours, and 20 continuing education hours."),
        ("July 25, 2026", "The two links to the proposed specialization hours pointed at Training hours, which no longer holds them; both now point at Specialized domains."),
        ("July 25, 2026", "Figures corrected. The practicum read \"~100 hours\" and \"~120 hours\"; the rule says a minimum of 100 and 120, so the tildes are gone. The prerequisites row read \"BLS, HIPAA, attestation\" and now records that the published rule accepts BLS, or CPR and AED, or New Mexico EMT licensure. The curriculum row named a curriculum without ever giving its hours, and now states 30 shared plus 5 role-specific didactic with 5 simulated patient hours, and 8 for the certifying clinician. Added a block setting out what changes if the committee recommendation is adopted, including that the certifying clinician does not change."),
        ("July 25, 2026", "Reviewed and brought current to the July 23 published rule. Both tables re-cited from the July 9 draft to the published rule with section numbers. The reciprocity entry read that the draft set two waiver deadlines of December 31 2026 and June 30 2027; the published rule sets both at December 31, 2027, and the older dates are kept only as history. Four links whose text named the published rule while still pointing at the July 9 PDF were repaired."),
    ],
    "cs-number": [
        ("July 28, 2026", "The update section now closes with a line back to the two pages that send readers here, the license tables and the routes, because a reader arriving from a verdict cell had no way back into their own situation. The page name is now the same in the title, the heading, and the menu: the controlled-substance number, with the site's title suffix, which this page alone had been carrying without."),
        ("July 25, 2026", "First full review of this page. Its central citation was wrong in two places: the lede and section 1 cited the controlled-substance-number requirement to 7.35.3.13 on p.8, which is the clinician-patient relationship and telemedicine section and contains no such requirement. The requirement is at 7.35.3.9 (D)(2), p.3, and a second location the page never mentioned, 7.35.3.8 (B)(3), p.1, which requires every patient enrollment application to record the certifying clinician's controlled substance number. Section 1 stated as verified that the state application requires a current DEA registration and that the state number must be obtained before the DEA issues the federal one, which is circular and which the July 17 record puts in dispute; it now states the dispute and that the department is checking with the Board of Pharmacy. The hearing was described as something the department was targeting for the end of August, which was accurate on July 17 and was superseded when the rule was published with the hearing set for August 28. Three sections ended at a decision point that has since been decided: section 2 called the non-prescribing certifying clinician an open rulemaking question, section 4 ended with the board sending the question back to the department on July 9, and section 6 presented telemedicine only as an external federal precedent when the published rule now contains a telemedicine pathway of its own at 7.35.3.13 (A)(2), p.8. All three now carry the outcome. The update section was dated to July 17 and now runs through the July 23 publication. The footer said the page was compiled July 9 from the record through the July 9 meeting."),
        ("July 25, 2026", "Reviewed and brought current. The page had no Updated date; one was added. The note that \"the July 9 draft PDF still shows the earlier text; an updated draft document has not been posted\" is no longer true: all three certifying-clinician exam pathways appear in the published rule at 7.35.3.8 (B)(8)(c) and 7.35.3.13 (A)(2), and the note now says so. Citations repointed to the published rule. No change to the substance of the page, which was accurate."),
    ],
    "input": [
        ("July 25, 2026", "Reviewed. No change to the form or its handling. A Reviewed date was added, since the page had none. Topics for the August 28 rule hearing and for submitting a document to the register were added earlier in the day, together with the querystring map entries they depend on."),
    ],
    "changes": [
        ("July 28, 2026", "Every provision on the page can now be linked from outside it: the thirteen published-provision rows carry section anchors in the same form the practicum worksheet uses, and each of the 104 comparison entries carries an anchor derived from its heading. The July 26 copy audit was applied: \"Dr. Ann Metz\" is corrected to \"Dr. Anne Metz\" in three places, \"Warnock\" is given as Catherine Warnock, and the deferrals log now states how its attributions are sourced and names the six rows that carry a first name alone, because no surname for them appears in any document this site holds. The four notes that told a reader to verify a passage against the source PDF were resolved instead: all four readings are confirmed against the July 9 draft at pages 5, 8, 11, and 14, and each note now states the finding and links the page. The page name is now the same in the title, the heading, and the menu: section by section."),
        ("July 25, 2026", "Added the CSS rules for the body, citation and note classes used in the published-provisions section, which had none on this page and were rendering unstyled."),
        ("July 25, 2026", "Page review applied. The section headed \"Earlier layer, 104 provisions\" told a reader nothing and is now \"Where the rules came from\", with a heading that says what the comparison actually is. The published-provisions table states in its opening line that these are the provisions deferred to the committee, rather than leaving it to be found. The \"Change from July 9\" column can now be hidden, since it is context rather than the thing most readers came for."),
        ("July 25, 2026", "Restructured into layers rather than re-citing 108 anchors that were already correct for what they compare. A new section, \"The training and education provisions, as published\", now leads the page: thirteen provisions with the July 23 text, the section and page, and what changed from July 9. It covers the didactic increase from 25 to 30 hours, the unchanged practicum, the new rule that the practicum cannot begin before half the didactic and all simulated patient hours, both waiver deadlines moving to December 31 2027, the disagreement between the two waivers on group session counts, and the new qualified-student staffing ratio. The existing 104-provision comparison was mis-framed as the current draft when it is a comparison of the June 12 recommendation against the July 9 draft; it is relabelled as the earlier layer and kept intact, with its July 9 page anchors, which are correct for that comparison."),
    ],
    "deferred": [
        ("July 28, 2026", "Every provision block now carries a link to the same section on the published rule page, and the two provisions that do not exist in the rule carry one as well, so the reference runs in both directions. The reciprocal links from the rule page's defect notes to findings B1, B4, and B5 landed in the same pass. The page name is now the same in the title, the heading, and the menu: what a practicum change touches."),
        ("July 27, 2026", "Restored. The July 27 redesign merge replaced this page with a redirect; it returns unchanged from the July 25 version. The committee recommendation on the deferred hours reached the department the same day; nothing on this page changes with it, because this page quotes the published text."),
        ("July 25, 2026", "Rebuilt as a worksheet. The first version led with a reading guide and a three-column history of how each requirement reached the published text, which is not what this page is for; that history belongs on the History page. The page now lists the thirteen provisions a practicum change has to touch, quotes each from the published rule, states what it does, and flags the three that do not work as written: 7.35.3.14 authorises nobody to let a student handle psilocybin, 7.35.3.19 (G) and 7.35.3.10 (D)(1) set different session tests for the same 40-hour waiver, and 7.35.3.14 (C) conditions healing-centre authority on a registration no section creates. Two provisions were added after checking the dependency chain: 7.35.3.11, which creates the approved locations 19 (D) requires, and 7.35.3.10 (D)(1), the second practicum waiver. The reading guide and the closing scope section were removed. All eighteen quotation fragments verified against the published text."),
    ],
    "about": [
        ("July 25, 2026", "Added to the primary navigation under The record. The page existed but was reachable only from the footer link at the foot of each page, so it had no route in from the nav at all. Sources updated: the list named the July 9 draft as the current source and now names the July 23 published rule, with the three earlier documents marked as history. The transcripts entry now distinguishes the speaker-tagged June and July 9 transcripts from the two July 17 transcripts, which carry no speaker labels."),
    ],
    "guide": [
        ("July 25, 2026", "Shipped broken and fixed the same day. The page was created by moving the site map section out of the overview, and the CSS the tiles depend on was left behind, so the cards rendered as one run-on block of underlined text. Seven classes had no rule. The styles were restored and a check for unstyled classes was added to the verification pass in UPDATING.md. The page also moved in the navigation from The record to Overview, where a directory of the site belongs, and its opening line no longer refers to three items that are no longer above it."),
        ("July 25, 2026", "Page created from the site map that was previously a section of the overview. It lists what each page holds, so the overview does not have to carry a directory of itself."),
    ],
    "specialization": [
        ("July 31, 2026", "The core-baseline card stated \"35 didactic + 100 practicum\" and said the working model of the hours held the same figures, which it did not: the model compares module totals, so its published baseline is 40. The card now names the 5 simulated patient hours as their own quantity and states which basis the model uses, so the two pages no longer disagree about the same rule text."),
        ("July 28, 2026", "The July 16 material now states how it is sourced before it states anything else: no recording, transcript, or minutes of that meeting is held in this repository, the absence is registered on the record page, and every source line beneath says so. Dom is named as Dominic Zurlo, director of the Department of Health Center for Medical Cannabis and Psilocybin, with the note that the July 16 notes recorded him by first name. Space Attendant is defined where it first appears. Jenn, Jamie, and Christine keep the first names the notes recorded, because no surname for them appears in any document this site holds, and the page now says that rather than leaving it to be noticed."),
        ("July 27, 2026", "Restored. The July 27 redesign merge replaced this page with a redirect; it returns unchanged from the July 25 version except that the core-figure link points at the retained record page, training-hours-record.html, where the pre-redesign Training hours material lives."),
        ("July 25, 2026", "This page now holds the specialization hours, which had been maintained on Training hours as well. Added at a new #hours anchor: the addendum framing, the core-baseline and end-of-life range cards, the nine-session 17-hour curriculum presented on July 16, and the three questions left open for the training committee. The banner said \"The routes above are unchanged\", which was left over from when this material sat at the foot of the provider routes page and there were routes above it."),
        ("July 25, 2026", "Page created from the specialized-domain section that was previously at the foot of the provider routes page, where it sat below unrelated material and carried July 16 dates with no indication of their status. It now states that none of it is in the published rule. Added the citation showing where end-of-life sits in the published text: the curriculum at 7.35.3.18 (C) lists seventeen required subjects and end-of-life is not among them, nor are suicidality, substance use disorder or PTSD, all four of which were asked for on the record on July 17."),
    ],
    "documents": [
        ("July 25, 2026", "Descriptions tightened to one line each after review; the page was over-written on creation. Page created earlier the same day: a register of every source document with what it is, when it landed, whether it is current or superseded, page count, size, and a direct download, plus a section naming the documents this site does not have."),
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
  .provsec .cd{font-size:12px; font-family:var(--mono); color:var(--text-faint); margin:0;}
  .provsec .cn{font-size:14.5px; font-weight:650; color:var(--text); margin:1px 0 0;}
  .provsec .cw{font-size:13.5px; color:var(--text-muted); line-height:1.55; margin:6px 0 0;}
  .provsec .curflag{display:inline-block; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:.05em; color:var(--agree); background:var(--agree-bg); border:1px solid var(--agree-border); border-radius:20px; padding:1px 8px; margin-left:7px; vertical-align:1px;}
  .revs{list-style:none; margin:0; padding:0;}
  .revs li{font-size:13.5px; color:var(--text-muted); line-height:1.55; padding:8px 0; border-top:1px solid var(--border);}
  .revs li:first-child{border-top:none; padding-top:0;}
  .revs b{color:var(--text); font-weight:650;}
"""

MARK = "<!-- provenance: generated by tools/sync-provenance.py, do not hand-edit -->"
BLOCK_RE = re.compile(re.escape(MARK) + r".*?" + re.escape("<!-- /provenance -->"), re.S)
CSS_MARK = "/* provenance block */"
CSS_RE = re.compile(re.escape(CSS_MARK) + r".*?" + re.escape("/* /provenance block */"), re.S)


WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six",
         7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(page):
    cur = next(c for c in CHAIN if c["status"] == "current")
    superseded = len(CHAIN) - 1
    chain = (
        '          <p class="cd">{date}</p>\n'
        '          <p class="cn"><a href="{file}" target="_blank" rel="noopener">{name}</a>'
        '<span class="curflag">Current state of truth</span></p>\n'
        '          <p class="cw">{what}</p>\n'
        '          <p class="cw">This document supersedes {n} earlier ones. Each of them, what it '
        'is, what superseded it and when, and a download, is in the register at '
        '<a href="record.html#documents">Meetings and filings</a>.</p>'
    ).format(date=syncrecord.long_date(cur["date"]), file=cur["file"], name=esc(cur["name"]),
             what=esc(CHANGED[cur["slug"]]), n=WORDS.get(superseded, superseded))

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
        '        <summary><span class="provsum">Provenance: the source document and this page&rsquo;s revisions</span><span class="provchev">&#9656;</span></summary>\n'
        '        <div class="provbody">\n'
        '        <div class="provsec">\n'
        '          <p class="provk">The document this page is read from</p>\n'
        + chain + "\n"
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

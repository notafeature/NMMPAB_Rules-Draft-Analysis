# HANDOFF: NMMPAB Training and Education reference site

Rewritten July 10, 2026, superseding the earlier handoff, which had drifted across parallel sessions. This file states the current state, the calls made when parallel work collided, and the open to-dos.

## 1. What this is

A neutral, plain-language community reference for the New Mexico Medical Psilocybin Advisory Board's **Training and Education** rulemaking. Audience is the whole community, including people who do not follow the legislative process. Clarity, not persuasion.

**Live site:** https://notafeature.github.io/NMMPAB_Rules-Draft-Analysis/ (GitHub Pages serves `docs/`).

## 2. Working rules (do not relax these)

- No em dashes anywhere. Grep before shipping.
- Facts only on public pages: dated events and attributed quotes. No characterizations ("overwhelmed," "confused"), no synthesized process or timeline.
- Site-usable vs internal: a sentence that explains a fact or a distinction can be public; a sentence that recommends an outcome stays internal (in `analysis/`).
- Nav identical on every page: same items, same order.
- Plain-label headings. Say more with less.
- No direct pushes to main. Branches and PRs; Gregory merges.

## 3. Site pages (all in docs/, identical nav)

| Page | Content |
|---|---|
| index.html | The tabled items: the three set-aside items, layered per item (recommendation verbatim, committee input, July 9 draft language, where it stands) |
| pathways.html | Provider routes by starting license |
| eligibility.html | Who can qualify: permits vs license types |
| hours.html | Training hours: the tabled numbers, verified benchmarks, cost variables (NM figures deliberately blank), July 17 open questions |
| cs-number.html | The CS number at the certifying-clinician access point: what it is, who can diagnose vs who can hold it, statute, comparators, July 9 record |
| input.html | Community input form (Formspree mjgqnkvv), opt-in contact only |
| history.html | Recent developments: the dated record from Jan 23 committee meetings through July 17 schedule |

## 4. Facts baseline (verified against the June 26 and July 9 transcripts)

- Process: committee writes a recommendation; the Advisory Board votes at a quorum meeting to accept and submit it to the Department of Health; the department turns it into rule language, which goes through a public rule hearing before promulgation; the department is not obligated to adopt it. (Zurlo, June 26.)
- Committee meetings: Jan 23, Mar 6, Apr 10, May 8 (joint with End of Life), May 22 (held, not recorded or posted by DOH).
- June 12: committee recommendation issued. June 25: department presented a rules-style draft of the same subject (state as fact only).
- June 26: board voted 3-2 to accept, setting aside (1) the CS number for the certifying clinician, (2) practicum hours (100/120 plus 20 supervisory), (3) the reciprocity timeline. Only Leeman's "reluctant yes" is named; the two against are not.
- July 9: an Advisory Board meeting with votes; the chair barred formal votes only after the scheduled adjournment. Reciprocity resolved without objection, both waiver deadlines to December 31, 2027 (Ian Dunn, board chair: December 31 is a legislative backstop). Board voted to table practicum and didactic hours to the committee. CS number sent back to the department. Renamed "certifying clinician." EMT training certification added alongside BLS/CPR. "Therapy sessions" removed. "Experience, observe or conduct" became "and conduct." Keenan Ryan is the new Medicaid seat.
- July 17: full Advisory Board 9 AM; Training and Education Committee 1 PM.
- Name corrections for auto-transcripts: Zurlo, Leeman, Peskuski, Dezbaá, Fatemi. Committee name is "Training and Education."

## 5. Reconciliation decision log (July 10 integration)

- hours.html existed in two versions. Kept PR #7's (source-verified, zero em dashes, NM costs left blank on purpose). The branch draft's unique facts (trainee-training dependency chain) were already present in PR #7's version; its "Options for setting the numbers" and illustrative cost estimates were dropped as synthesis.
- An embedded "Suggest a resource" form on index.html (unwired placeholder ID) was removed; the dedicated input.html (wired to Formspree) is the single input surface, linked from index and nav.
- PR #8's claude-work/ pages were byte-identical to docs/pathways.html and docs/reference.html already on main; not merged.
- PR #9 was a bundle; its unique content (history.html, two CS analysis notes) was taken, the rest were byte-duplicates of PR #6/#8/#10 files or of docs/documents/.
- docs/archive/ deleted (superseded pages; recoverable from git history).
- reference.html renamed eligibility.html (from the orphaned branch commit 1cc1781); mobile hamburger nav adopted from the same commit.

## 6. Open to-dos

Parked pending team discussion (Gregory decides):
- [ ] NM cost figures on hours.html: healing-center session pricing for trainees, trainee-on-trainee legality, real tuition once programs are approved, provider counts needed. Deliberately blank until researched.
- [ ] Whether any additional nav or homepage emphasis changes are wanted after review.

Verification and content:
- [ ] Soft point: the June 26 motion mover is attributed to Brenda Burgard per the meeting-note summary; the raw transcript is unlabeled at that segment. Confirm when DOH posts official minutes.
- [ ] Wire in the June 12 and June 25 recordings if DOH posts them.
- [ ] Possible future: transcript subpage per meeting, with quotes linked to their spot.
- [ ] After July 17: record outcomes on history.html and the affected pages.

## 7. Sources

- `docs/documents/`: June 12 recommendation, June 25 draft (superseded), July 9 rules draft (7.35.3), July 9 transcript (unofficial, speaker-tagged).
- `analysis/`: attributed extractions of June 25 and June 26, CS-number research (internal backing for cs-number.html), SOURCES.md, meeting inventory.
- `source-text/`: verbatim pypdf extraction of the drafts.

Nothing in this repository is final, promulgated rule text.

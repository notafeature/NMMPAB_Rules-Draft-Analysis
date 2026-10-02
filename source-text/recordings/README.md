# Caption transcripts of the department's public meeting recordings

This folder holds the YouTube caption transcripts of every recording the New Mexico Department of Health has published of the Medical Psilocybin Advisory Board, its committees, its two 2025 listening sessions, and the April 24, 2026 rule hearing on 7.35.2 NMAC. The recordings are on the department's YouTube channel, NMHEALTH, and most are linked from the department's meeting records page at https://www.nmhealth.org/about/mcpp/mpp/mpab/mr/. Each link there redirects to the YouTube video. Five recordings are on the channel and not on that page; `MISSING.md` lists them.

## Files

Each recording has two files, named by meeting date, body, and YouTube video ID.

- `.vtt` is the caption file as YouTube serves it.
- `.txt` is the same captions as plain text, one line per caption line in the form `[HH:MM:SS] text`, stamped with the start of its cue. Automatic captions served as rolling captions show each line twice, once as it is spoken and once above the next line; the repeat is dropped on an exact match and nothing else is removed. `tools/sync-recordings.py` makes every `.txt` from its `.vtt`, and its `--check` fails if one no longer matches.

`INDEX.csv` lists every recording: meeting date, body, YouTube title, video ID, watch URL, the department's redirect URL where one exists, upload date, duration in seconds, whether the captions are manual or automatic, caption language, the text file, and notes. `MISSING.md` lists the one department link that resolves to no video and the five recordings found on the channel but not on the department's page.

## Bodies

`board` is the Advisory Board. `tae` is the Training and Education Committee. `eolc` is the End of Life Care Committee. `pqs` is the Patient Qualification and Safety Committee. `dacp` is the Dosage, Administration and Clinical Practice Committee. `raci` is the Research and Continuous Improvement Committee. `eacc` is the Equity, Access and Cultural Considerations Committee. `prop` is the Propagation Committee. `hearing` is a rule hearing. `other` is a listening session.

## What these transcripts are, and are not

The text is YouTube's caption track, saved exactly as served. Sixty-one of the eighty are automatic captions, and automatic captions misspell names and drop words. No transcript here has been corrected. They carry no speaker labels. A speaker is named from one of these transcripts only where the surrounding text fixes it, and the basis is stated, as `CLAUDE.md` requires for the July 17, 2026 transcripts. Verbatim quotation from these files means the caption text, including its errors.

The recording itself is the public record. These files are a searchable copy of it. Where a transcript and the recording disagree, the recording governs.

## Provenance

Pulled from YouTube on October 1, 2026 with yt-dlp, captions only, no video or audio. The department's page and channel were read the same day. The yt-dlp metadata files were not kept; `INDEX.csv` carries the dates and durations taken from them. `tools/sync-recordings.py` pulls recordings published after that date.

A file is named by the date of its meeting. One title carries the wrong date: the Training and Education Committee recording titled May 26, 2026 is the meeting of May 22, 2026, and its index row states the basis.

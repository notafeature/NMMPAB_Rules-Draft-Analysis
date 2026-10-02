#!/usr/bin/env python3
"""Pull the caption transcripts of the department's public meeting recordings.

source-text/recordings/ holds one .vtt and one .txt per recording the New Mexico
Department of Health has published of the Medical Psilocybin Advisory Board, its
committees, its listening sessions, and its rule hearings, with INDEX.csv listing
them. The department publishes a recording weeks after the meeting, so the folder
goes stale unless something looks for new ones. This tool looks.

Three sources are read, all public:

    the department's meeting records page, whose recording links each redirect
        to a YouTube video
    a search of the department's YouTube channel for "psilocybin"
    the channel's Medical Psilocybin playlist

A recording found in any of them and absent from INDEX.csv is pulled: the caption
file as YouTube serves it becomes the .vtt, the .txt is made from it, and a row is
added to the index. Captions only; no video or audio is downloaded.

The .txt is the .vtt with the timing removed and nothing else changed. A manual
caption track, and an automatic one served as plain cues, become one line per cue.
An automatic track served as rolling captions repeats each line: a cue shows the
line just completed above the line being spoken. There the line being spoken is
kept and the repeated line above it is dropped, on an exact match only. No word is
compared loosely and none is removed for resembling its neighbour, so a speaker
who repeats a word keeps both.

The meeting date and the body come from the YouTube title. Where a title carries
the wrong date, CORRECTIONS below holds the date the record supports and the
basis for it, and the basis is written into the index row.

Usage:
    python3 tools/sync-recordings.py            # pull what is new, update the index
    python3 tools/sync-recordings.py --list     # report what is new, write nothing
    python3 tools/sync-recordings.py --check    # no network: the folder agrees with itself
    python3 tools/sync-recordings.py --rebuild-txt   # remake every .txt from its .vtt

yt-dlp does the fetching. It is found on PATH, or at the path in the YT_DLP
environment variable.
"""

import csv
import html
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FOLDER = ROOT / "source-text" / "recordings"
INDEX = FOLDER / "INDEX.csv"

RECORDS_PAGE = "https://www.nmhealth.org/about/mcpp/mpp/mpab/mr/"
CHANNEL_SEARCH = "https://www.youtube.com/@NMHEALTH/search?query=psilocybin"
PLAYLIST = "https://www.youtube.com/playlist?list=PLYOwoMAmeJV4i2xIJrYgZW-EeEVwmrNSi"

FIELDS = ["meeting_date", "body", "youtube_title", "video_id", "watch_url",
          "department_resource_url", "upload_date", "duration_seconds", "caption_type",
          "caption_language", "txt_file", "notes"]

CHANNEL_ONLY = "Found on NMDOH channel; not listed on the department Meeting Records page."

# The body is read from the title, first match wins. The Advisory Board is last
# because committee titles can carry its name.
BODIES = [
    ("other", r"listening session"),
    ("hearing", r"hearing"),
    ("tae", r"training"),
    ("eolc", r"end[ -]of[ -]life"),
    ("pqs", r"patient qualification"),
    ("dacp", r"dosage"),
    ("raci", r"research"),
    ("eacc", r"equity"),
    ("prop", r"propagation"),
    ("board", r"advisory board"),
]

# A recording whose title carries the wrong date. The key is the video ID; the
# value is the meeting date and the basis for it, which becomes the row's note.
CORRECTIONS = {
    "gZJS4sPuacg": (
        "2026-05-22",
        "The YouTube title says May 26, 2026 and the department link is labeled May 29. "
        "Filed under May 22: the May 8 committee recording sets the next meeting for "
        "\"Friday the 22nd\" (1:54:00), the May 15 board recording says \"training and "
        "education is coming up on the 22nd\" (1:48:49), and this recording cites a list "
        "\"collected by us uh on May 21st\" (0:03:55). No statement in the recording gives "
        "its own date. The recording runs 13 minutes and ends mid-sentence."),
}

MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], 1)}

TIMING = re.compile(r"^(\d\d):(\d\d):(\d\d)\.\d{3} --> \d\d:\d\d:\d\d\.\d{3}")
TAG = re.compile(r"<[^>]*>")
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")


# ---------------------------------------------------------------- the .txt

def cues(vtt):
    """Yield (stamp, lines) for every cue, tags removed, entities decoded.

    A cue's text runs to the next empty line. Rolling captions carry lines that
    hold a single space; those are caption lines, not separators, and come back
    as empty strings.
    """
    lines = vtt.replace("\r\n", "\n").split("\n")
    i, n = 0, len(lines)
    while i < n:
        m = TIMING.match(lines[i])
        if not m:
            i += 1
            continue
        stamp = "[%s:%s:%s]" % m.groups()
        i += 1
        body = []
        while i < n and lines[i] != "" and not TIMING.match(lines[i]):
            body.append(html.unescape(TAG.sub("", lines[i])).strip())
            i += 1
        yield stamp, body


def vtt_to_txt(vtt):
    """One line per caption line, as `[HH:MM:SS] text`, stamped with its cue's start."""
    rolling = "<c>" in vtt
    out, shown = [], []
    for stamp, body in cues(vtt):
        text = [line for line in body if line]
        if rolling:
            new = text[1:] if text and shown and text[0] == shown[-1] else text
            out.extend(f"{stamp} {line}" for line in new)
            shown = text
        elif text:
            out.append(f"{stamp} {' '.join(text)}")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- the index

def read_index():
    with open(INDEX, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def index_text(rows):
    rows = sorted(rows, key=lambda r: (r["meeting_date"], r["body"], r["video_id"]))
    out = io.StringIO(newline="")
    w = csv.DictWriter(out, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(rows)
    return out.getvalue()


def write_index(rows):
    with open(INDEX, "w", encoding="utf-8", newline="") as f:
        f.write(index_text(rows))


def stem(row):
    return f'{row["meeting_date"]}-{row["body"]}-{row["video_id"]}'


def body_of(title):
    low = title.lower()
    for body, pattern in BODIES:
        if re.search(pattern, low):
            return body
    return None


def date_of(title):
    """The meeting date a title states, as YYYY-MM-DD, or None."""
    for m in re.finditer(r"(?<![A-Za-z])([A-Za-z]{3,9})\.?,? (\d{1,2}),? ?(\d{4})\b", title):
        month = [n for name, n in MONTHS.items() if name.startswith(m.group(1).lower())]
        if len(month) == 1:
            return "%04d-%02d-%02d" % (int(m.group(3)), month[0], int(m.group(2)))
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{2}|\d{4})\b", title)
    if m:
        year = int(m.group(3))
        year += 2000 if year < 100 else 0
        return "%04d-%02d-%02d" % (year, int(m.group(1)), int(m.group(2)))
    return None


# ---------------------------------------------------------------- the check

def check():
    """The folder agrees with itself. No network."""
    problems = []
    rows = read_index()
    seen = set()
    for row in rows:
        s = stem(row)
        if row["video_id"] in seen:
            problems.append(f"{row['video_id']} is indexed twice")
        seen.add(row["video_id"])
        if row["txt_file"] != s + ".txt":
            problems.append(f"{s}: the index names {row['txt_file']}")
        vtt, txt = FOLDER / (s + ".vtt"), FOLDER / (s + ".txt")
        if not vtt.exists() or not txt.exists():
            problems.append(f"{s}: the .vtt or the .txt is absent")
            continue
        if vtt_to_txt(vtt.read_text(encoding="utf-8")) != txt.read_text(encoding="utf-8"):
            problems.append(f"{s}: the .txt is not what its .vtt produces; run --rebuild-txt")
        want = CORRECTIONS.get(row["video_id"], (date_of(row["youtube_title"]),))[0]
        if want and want != row["meeting_date"]:
            problems.append(f"{s}: the title or the correction gives {want}")
    indexed = {stem(r) for r in rows}
    for path in sorted(FOLDER.glob("*.vtt")) + sorted(FOLDER.glob("*.txt")):
        if path.stem not in indexed:
            problems.append(f"{path.name} has no index row")
    for name in ("INDEX.csv", "MISSING.md", "README.md"):
        if chr(8212) in (FOLDER / name).read_text(encoding="utf-8"):
            problems.append(f"{name} carries an em dash")
    if index_text(rows) != open(INDEX, encoding="utf-8", newline="").read():
        problems.append("INDEX.csv is not as the tool writes it: date order, then body")
    return problems


def rebuild_txt():
    changed = 0
    for row in read_index():
        s = stem(row)
        new = vtt_to_txt((FOLDER / (s + ".vtt")).read_text(encoding="utf-8"))
        txt = FOLDER / (s + ".txt")
        if not txt.exists() or txt.read_text(encoding="utf-8") != new:
            txt.write_text(new, encoding="utf-8")
            changed += 1
    return changed


# ---------------------------------------------------------------- the network

def yt_dlp():
    path = os.environ.get("YT_DLP") or shutil.which("yt-dlp")
    if not path:
        sys.exit("yt-dlp is not on PATH and YT_DLP is not set. Install it, for example with "
                 "`pipx install yt-dlp`.")
    return path


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8", "replace")


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


def redirect_of(url):
    """Where a department resource link points, without following it."""
    opener = urllib.request.build_opener(NoRedirect)
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
    try:
        opener.open(request, timeout=60)
    except urllib.error.HTTPError as error:
        return error.headers.get("Location", "")
    return ""


def video_id_in(location):
    m = re.search(r"(?:[?&]v=|youtu\.be/)([^&#/]+)", location)
    return m.group(1) if m else ""


def department_links():
    """{resource URL: (link text, redirect target)} for every link on the records page."""
    page = fetch(RECORDS_PAGE)
    links = {}
    for href, text in re.findall(r'<a[^>]+href="([^"]*/resource/view/\d+/)"[^>]*>(.*?)</a>',
                                 page, flags=re.S):
        url = href if href.startswith("http") else "https://www.nmhealth.org" + href
        links.setdefault(url, html.unescape(TAG.sub("", text)).strip())
    return links


def flat_list(url):
    """[(video id, title)] for a channel search or a playlist."""
    result = subprocess.run(
        [yt_dlp(), "--flat-playlist", "--no-warnings", "--print", "%(id)s\t%(title)s", url],
        capture_output=True, text=True)
    found = []
    for line in result.stdout.splitlines():
        vid, _, title = line.partition("\t")
        if VIDEO_ID.match(vid):
            found.append((vid, title))
    return found


def discover(rows):
    """What the three sources hold that the index does not.

    Returns (new, dead): new is {video id: resource URL or ""}; dead is the
    department links that redirect to YouTube without a valid video ID.
    """
    have = {r["video_id"] for r in rows}
    known_links = {r["department_resource_url"] for r in rows if r["department_resource_url"]}
    new, dead = {}, []
    for url, text in department_links().items():
        if url in known_links:
            continue
        location = redirect_of(url)
        if "youtu" not in location:
            continue
        vid = video_id_in(location)
        if not VIDEO_ID.match(vid):
            dead.append((text, url, location))
        elif vid not in have:
            new[vid] = url
    for source in (CHANNEL_SEARCH, PLAYLIST):
        for vid, title in flat_list(source):
            if vid not in have and vid not in new and "psilocybin" in title.lower():
                new[vid] = ""
    return new, dead


def pull(vid, resource_url):
    """Fetch one recording's captions. Returns (row, vtt text), or (None, reason)."""
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(
            [yt_dlp(), "--skip-download", "--no-warnings", "--write-subs", "--write-auto-subs",
             "--sub-langs", "en.*,en", "--sub-format", "vtt", "--write-info-json",
             "-o", "%(id)s", f"https://www.youtube.com/watch?v={vid}"],
            cwd=tmp, capture_output=True, text=True)
        info_path = Path(tmp) / f"{vid}.info.json"
        if not info_path.exists():
            return None, "yt-dlp returned no metadata"
        info = json.loads(info_path.read_text(encoding="utf-8"))
        manual = any(k.startswith("en") for k in (info.get("subtitles") or {}))
        if manual:
            choices = [("manual", "en")]
        else:
            choices = [("auto", "en-orig"), ("auto", "en")]
        for kind, language in choices:
            vtt_path = Path(tmp) / f"{vid}.{language}.vtt"
            if vtt_path.exists():
                vtt = vtt_path.read_text(encoding="utf-8")
                break
        else:
            return None, "no English caption track is published yet"
    title = info.get("title", "")
    body = body_of(title)
    date = CORRECTIONS.get(vid, (date_of(title),))[0]
    if not body or not date:
        return None, f"the title gives no {'body' if not body else 'date'}: {title!r}"
    upload = info.get("upload_date") or ""
    notes = []
    if vid in CORRECTIONS:
        notes.append(CORRECTIONS[vid][1])
    if not resource_url:
        notes.append(CHANNEL_ONLY)
    row = {
        "meeting_date": date, "body": body, "youtube_title": title, "video_id": vid,
        "watch_url": f"https://www.youtube.com/watch?v={vid}",
        "department_resource_url": resource_url,
        "upload_date": f"{upload[:4]}-{upload[4:6]}-{upload[6:8]}" if len(upload) == 8 else "",
        "duration_seconds": str(info.get("duration") or ""),
        "caption_type": kind, "caption_language": language, "txt_file": "", "notes": " ".join(notes),
    }
    row["txt_file"] = stem(row) + ".txt"
    return row, vtt


def main(argv):
    if "--check" in argv:
        problems = check()
        for p in problems:
            print("recordings:", p)
        print(f"recordings: {len(read_index())} indexed, "
              f"{'clean' if not problems else str(len(problems)) + ' problem(s)'}")
        return 1 if problems else 0
    if "--rebuild-txt" in argv:
        print(f"recordings: {rebuild_txt()} .txt file(s) rewritten")
        return 0

    rows = read_index()
    new, dead = discover(rows)
    for text, url, location in dead:
        print(f"recordings: department link with no video: {text} | {url} | {location}")
    if not new:
        print(f"recordings: nothing new; {len(rows)} indexed")
        return 0
    if "--list" in argv:
        for vid, url in new.items():
            print(f"recordings: new: https://www.youtube.com/watch?v={vid} {url}")
        return 0
    added = 0
    for vid, url in new.items():
        row, vtt = pull(vid, url)
        if row is None:
            print(f"recordings: not pulled: {vid}: {vtt}")
            continue
        s = stem(row)
        (FOLDER / (s + ".vtt")).write_text(vtt, encoding="utf-8")
        (FOLDER / (s + ".txt")).write_text(vtt_to_txt(vtt), encoding="utf-8")
        rows.append(row)
        added += 1
        print(f"recordings: pulled {s} ({row['caption_type']} captions)")
    if added:
        write_index(rows)
    print(f"recordings: {added} added; {len(rows)} indexed. MISSING.md is written by hand: "
          "update it for any channel-only recording or dead link reported above.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

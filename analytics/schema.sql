-- Schema for the nmmpab-count D1 database.
--
-- One row per recorded event. There is no session table, no user table, and no
-- column that holds an IP address, a cookie value, or anything else that
-- survives the day it was written.
--
-- Apply with:
--   wrangler d1 execute nmmpab-count --remote --file=analytics/schema.sql

CREATE TABLE IF NOT EXISTS hits (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,

  -- When. ts is UTC to the second, day is the UTC date the row belongs to.
  ts       TEXT NOT NULL,
  day      TEXT NOT NULL,

  -- What. kind is 'pv' for a page view and 'dl' for a document download.
  -- path is normalised to a bare file name: 'hours.html', 'documents/x.pdf'.
  kind     TEXT NOT NULL,
  path     TEXT NOT NULL,

  -- Who, as coarsely as the question allows. visitor is a hash of the
  -- requesting address and browser string salted with the UTC date, so it
  -- distinguishes two readers on the same day and cannot connect one reader
  -- across two days. Nothing that went into the hash is stored.
  visitor  TEXT NOT NULL,

  -- Where from. ref_host is the host part of document.referrer and nothing
  -- else: no path, no query string. Empty means the reader arrived directly.
  ref_host TEXT,

  -- Coarse network context, from Cloudflare's view of the connection.
  -- country is a two-letter code. No city, no region, no coordinates.
  -- as_org names the network that carried the request, which is the internet
  -- provider, not the reader's employer. See the note in the dashboard.
  country  TEXT,
  asn      INTEGER,
  as_org   TEXT,
  net_kind TEXT,

  -- 1 if the row arrived through the beacon's image fallback rather than
  -- through sendBeacon or fetch.
  nojs     INTEGER NOT NULL DEFAULT 0,

  -- Which address the reader was on. The site is served at
  -- rules.medical-psilocybin.org, and notafeature.github.io redirects there,
  -- so nearly every row says the former. A github.io row is somebody arriving
  -- from a stale bookmark or an old emailed link.
  --
  -- What this cannot show is a reader who is blocked: they never load the
  -- page, so nothing is recorded, which is indistinguishable from nobody
  -- reading.
  site_host TEXT
);

CREATE INDEX IF NOT EXISTS hits_day      ON hits(day);
CREATE INDEX IF NOT EXISTS hits_path_day ON hits(path, day);
CREATE INDEX IF NOT EXISTS hits_kind_day ON hits(kind, day);

-- Bookkeeping for the retention sweep, so it runs once a day rather than on
-- every request. One row, key 'purged_on'.
CREATE TABLE IF NOT EXISTS meta (
  k TEXT PRIMARY KEY,
  v TEXT NOT NULL
);

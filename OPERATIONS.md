# Operations

The infrastructure behind the site, as it stands, and the runbooks for changing it. This file
exists so that no session has to rediscover how the site is served. Read it before touching
DNS, hosting, the counter, or anything outside the content of `docs/`.

Every fact in Part 1 was read from the live systems on September 7, 2026. Part 6 says how to
read them again.

---

## Part 1: Inventory

### 1.1 Domain and DNS

The zone `medical-psilocybin.org` is on Cloudflare DNS, in the personal Cloudflare account
(account ID `2418db2ff3f95726c374a86551d2436e`, zone ID `ff942843527ffd5e5cc100101df756ad`),
on the Free plan. It is deliberately not in the Santa Fe Psychedelic Society account. Name
servers: `greg.ns.cloudflare.com`, `rose.ns.cloudflare.com`.

| Record | Type | Content | Proxied | Purpose |
|---|---|---|---|---|
| `medical-psilocybin.org` | A | `192.0.2.0` | yes | Placeholder; the hub Worker's zone route `medical-psilocybin.org/*` answers every request on it, and the redirect rule below fires first while it is enabled |
| `www.medical-psilocybin.org` | A | `192.0.2.0` | yes | Same, route `www.medical-psilocybin.org/*` |
| `rules.medical-psilocybin.org` | CNAME | `notafeature.github.io` | **no** | The site. DNS-only on purpose; see 1.3 |
| `count.medical-psilocybin.org` | AAAA | `100::` | yes | The counter Worker's custom domain, created by Wrangler |
| `research.medical-psilocybin.org` | (created by Wrangler) | Worker custom domain | yes | The research Worker's custom domain, created by the September 11, 2026 deploy (1.4c) |

Zone settings: SSL/TLS mode **Full**; Always Use HTTPS **off**. `192.0.2.0` and `100::` are
reserved placeholder addresses; the proxied records exist so Cloudflare handles the request.

**Redirect rule** (Cloudflare, Rules, Redirect Rules), named "Redirect to rules subdomain",
enabled: if the host is `medical-psilocybin.org` or `www.medical-psilocybin.org`, 301 to
`https://rules.medical-psilocybin.org` plus the request path, query string preserved. Rule id
`f608fd6122b34aa1b0d08739d5d969e7` in ruleset `948e2cb12d104a84a4a8f71d507bc4d9`. **Until this
rule is disabled, the apex redirects and the hub Worker routed behind it never answers.** Neither
the session's Cloudflare API token nor Wrangler's login may edit zone rulesets or delete DNS
records; the switch is one action in the dashboard: Rules, Redirect Rules, disable "Redirect to
rules subdomain" (Part 4.3).

No page rules, no bulk redirect lists, no rate-limit rule enabled.

### 1.2 The site: GitHub Pages

| Item | Value |
|---|---|
| Repository | `github.com/notafeature/NMMPAB_Rules-Draft-Analysis`, public, default branch `main` |
| Pages source | branch `main`, folder `/docs`. The parts index and the redirect stubs sit at the root; each Part's pages sit in their own folder, `docs/7.35.3/` today; `style.css` and `documents/` are shared and linked by root-absolute path |
| Build type | legacy (GitHub runs Jekyll over `docs/`; no `_config.yml` is present, so it publishes the folder as-is) |
| Custom domain | `rules.medical-psilocybin.org`, set by the file `docs/CNAME` |
| HTTPS | enforced; certificate issued by GitHub, renewed by GitHub, current one expires 2026-10-23 |
| Old address | `notafeature.github.io/NMMPAB_Rules-Draft-Analysis/` redirects to the custom domain |
| Deploy | merge to `main`. Nothing else. A few minutes to appear; GitHub caches each file for ten minutes |

GitHub Pages serves a private repository only on a paid plan. The account is not on one. If
the repository goes private, the site moves to Cloudflare first (Part 4.4).

### 1.3 Why the `rules` record is not proxied

Proxying `rules` would put Cloudflare in front of GitHub Pages. That works only with SSL mode
Full, and a mismatch produces a redirect loop that takes the live site down. Nothing today
needs the proxy on that host. Turn it on only as a deliberate step in Part 4.4, after
confirming the SSL mode, and never in the week before a rule hearing.

### 1.4 The counter: the `nmmpab-count` Worker

| Item | Value |
|---|---|
| Code and config | `analytics/worker.js`, `analytics/wrangler.toml`, `analytics/schema.sql`, `analytics/setup.sh` |
| Account | the personal account, `2418db2ff3f95726c374a86551d2436e` |
| Host | `count.medical-psilocybin.org`, a Workers custom domain; `workers.dev` and preview URLs off |
| Database | D1, `nmmpab-count`, id `6b4b8f4f-38be-4315-9cd1-75a08d10acb6`, created 2026-07-26, schema applied |
| Bindings on the deployed Worker | `DB` (d1), `ALLOWED_ORIGINS` (text), `DASH_USER` (text), `SALT` (secret), `DASH_PASS` (secret) |
| Allowed origins | `https://notafeature.github.io`, `https://rules.medical-psilocybin.org` |
| Dashboard | `https://count.medical-psilocybin.org/`, HTTP Basic auth, user `owner`, password is the `DASH_PASS` secret |
| Beacon in the pages | written by `tools/sync-count.py`; endpoint is the `ENDPOINT` constant there and nowhere else |
| Deploy | `./analytics/setup.sh`, or `npx wrangler@4 deploy --config ./analytics/wrangler.toml` from the repository root |

What it records, what it drops, and what the organisation column can and cannot tell you are
in `analytics/README.md`. The beacon reports `location.pathname`; the Worker keeps the Part
folder and the file name (`7.35.3/index.html`), so two Parts' index pages are two rows. The
page-view filter `PV_PATH` in `analytics/worker.js` accepts a file at the root or one folder
down; a deeper folder would need that pattern widened and the Worker redeployed. Two facts from it that come up: datacenter networks are dropped, so
scanners sweeping the domain mostly do not appear, and a mobile carrier row is a phone on
that carrier's network, wherever the reader is.

### 1.4a The hub: the `medical-psilocybin-hub` Worker

| Item | Value |
|---|---|
| Repository | `github.com/notafeature/medical-psilocybin.org`, public; local clone `~/MPAB/medical-psilocybin.org/` |
| Code and config | `public/index.html`, `public/404.html`, `public/style.css` (a copy of the rules site's), `wrangler.jsonc` |
| Account | the personal account, `2418db2ff3f95726c374a86551d2436e` |
| Hosting | a Worker with static assets and no code, name `medical-psilocybin-hub`, bound by zone routes `medical-psilocybin.org/*` and `www.medical-psilocybin.org/*` over the placeholder A records; deployed September 7, 2026 |
| Deploy | `npx wrangler@4 deploy --config ./wrangler.jsonc` from that repository |
| Counter | carries the beacon; both hosts are in the counter's `ALLOWED_ORIGINS` |

The hub answers only once the apex redirect rule (1.1) is disabled.

### 1.4b Pathways: the `medical-psilocybin-pathways` Worker

| Item | Value |
|---|---|
| Repository | `github.com/notafeature/pathways.medical-psilocybin.org`, public; local clone `~/MPAB/pathways.medical-psilocybin.org/` |
| Hosting | a Worker with static assets, name `medical-psilocybin-pathways`, custom domain `pathways.medical-psilocybin.org` created by Wrangler; deployed September 7, 2026 |
| Content | one folder per role under `public/` (`producers/` with six guide pages and the drafter; `testing/`, `clinicians/`, `practitioners/`, `facilitators/`, `healing-centers/`, `educational-programs/`, `patients/` with one page each); `public/_redirects` carries the first day's addresses; `tools/build.py` stamps the shared chrome, a folder's `_subnav.html`, and the counter beacon, refuses an em dash, and fails on a root-absolute link that resolves to no file |
| Deploy | `python3 tools/build.py && npx wrangler@4 deploy --config ./wrangler.jsonc` from that repository |
| Counter | in `ALLOWED_ORIGINS` |

### 1.4c Research: the `medical-psilocybin-research` Worker

| Item | Value |
|---|---|
| Repository | `github.com/notafeature/research.medical-psilocybin.org`, public, created September 11, 2026; local clone `~/Projects/Medical-Psilocybin/research.medical-psilocybin.org/` |
| Hosting | a Worker with static assets, name `medical-psilocybin-research`, custom domain `research.medical-psilocybin.org` created by Wrangler; deployed September 11, 2026 |
| Content | one page at the root and the files beside it at fixed addresses (Summary and Schema PDFs, workbook, JSON Schema, CSV, and three diagrams in PNG and SVG); `public/_redirects` sends the first day's `/2026-09-11/` addresses to the root; `tools/build.py` stamps the shared chrome and the files table (size, SHA-256), refuses an em dash, fails on a root-absolute link that resolves to no file, on the provenance address appearing in a page, on a Measures file, or on a file the table does not name |
| Signed | the only signed host: every page carries "Work product of the Research and Continuous Improvement Committee workgroup, New Mexico Medical Psilocybin Advisory Board. Published by Gregory Evans. Not a department publication." The published files are CC BY 4.0. Its README records the decisions of September 11, 2026 |
| Deploy | `python3 tools/build.py && npx wrangler@4 deploy --config ./wrangler.jsonc` from that repository |
| Counter | **not counted**, decided September 11, 2026 and recorded in that repository's README (4.1 step 3, the written alternative); no beacon, not in `ALLOWED_ORIGINS` |

### 1.5 The input form

`docs/7.35.3/comment.html` posts to Formspree form `mjgqnkvv`. Submissions land in the Formspree
inbox of the account that owns the form. No other service receives reader input.

### 1.6 Local preview

`.claude/launch.json` (ignored by git) starts `python3 -m http.server 4599 --directory docs`.
Any static server over `docs/` is equivalent. There is no build step for the site.

### 1.7 Credentials, where each one lives

No credential is in the repository. The Worker's `wrangler.toml` holds only identifiers.

| Credential | Lives in | Needed for |
|---|---|---|
| GitHub account | the owner's browser and `gh auth` (scopes `repo`, `workflow`, `read:org`, `gist`) | merging, Pages settings, making the repository private |
| Cloudflare account | the owner's browser and `wrangler login` | DNS, rules, the Worker, any new project |
| `SALT`, `DASH_PASS` | Worker secrets, set by `setup.sh` | the counter; regenerate with `wrangler secret put` |
| Formspree account | the owner's browser | the input form |

---

## Part 2: How a change reaches the public

1. Branch from `main`. Never push to `main`.
2. Edit. Content that a tool owns is edited in the tool and the tool is run (`UPDATING.md`,
   Part 3).
3. `python3 tools/check-all.py` must print `clean` for every Part (`check-site.py --part N` runs one). It checks every page parses, carries the
   menu, the counter, the versioned stylesheet, no em dashes, no broken links, and that every
   tool-owned region matches its tool.
4. Open a pull request. The owner merges.
5. GitHub Pages publishes `docs/` from `main` within minutes. Nothing to deploy.

The Worker is the one thing with a deploy step, and merging does not deploy it. Run
`analytics/setup.sh` only when `analytics/` changed.

**Rollback:** revert the merge commit on `main` through a pull request. Pages republishes.

---

## Part 3: Runbooks for the site

### 3.1 Add a page

1. Create the file in the Part's folder, `docs/7.35.3/`.
2. Add its slug and name to `NAMES` and its place to `GROUPS` in `tools/sync-nav.py`.
3. Run, in this order: `sync-nav.py`, `sync-css-version.py`, `sync-count.py`,
   `sync-provenance.py` (with a `REVISIONS` entry for the new page).
4. `check-site.py`. It fails until the page is in the menu, reachable, titled from `NAMES`,
   and carrying every shared block.

### 3.2 Retire a page

Replace its content with a redirect stub (copy one at the root of `docs/`) pointing at the
page that now owns the content by root-absolute path, with the anchor. Remove it from `sync-nav.py`. `check-site.py` verifies the
stub's target and anchor exist.

### 3.3 Add a document

Follow `UPDATING.md`, Event A or C: the PDF into `docs/documents/` with a dated name, the
extraction into `source-text/`, the register row in `tools/sync-record.py`, the dropdown in
`tools/sync-nav.py` if it is a document of the latest filing, and the tools run.

### 3.3a Add a site-wide page outside any Part

A folder under `docs/` with one `index.html` carrying the root's chrome (brand link to `/`,
no Part menu), its name added to `SITE_DIRS` in `tools/partlib.py`, and a link from the
parts index, which `check-site.py` requires. `sync-css-version.py` and `sync-count.py` cover
it; the Part tools do not touch it. `docs/statute/` and `docs/about/` are the two that exist.

### 3.4 Add a part

1. `docs/7.35.N/`, an entry for the Part in `PARTS` in `tools/partlib.py` (title suffix and
   brand), and a data file per tool in `tools/parts/7.35.N/`: `sync-nav.py`, `sync-status.py`,
   `sync-record.py`, `sync-provenance.py`, `build-rule-page.py`, and `sync-pathways.py` only
   if the Part has routes. Copy Part 2's as the smaller template.
2. The official text: the Register issue's PDF and the compiled NMAC file into
   `docs/documents/`, extracted into `parts/7.35.N/source-text/`.
3. `tools/build-rule-page.py --part 7.35.N` with `SOURCE` pointed at the extraction. Every
   tool takes `--part`; `check-site.py --part 7.35.N` runs the Part's checks.
4. A row on `docs/index.html` (the parts and their states) and on `docs/statute/` for each
   statute section the part implements.
5. The title suffix for the part in its `site.py`.
6. The tools and `check-site.py` run for the new part. The counter needs nothing: same host.

### 3.5 Change a status or a date

`tools/sync-status.py` and `tools/sync-record.py`, then `UPDATING.md` Event D for the
copies in hand-maintained prose.

---

## Part 4: Runbooks for hosts and hosting

### 4.1 Add a host for a new application

1. Create the application in its own repository with its own deploy config. Never add a
   second Cloudflare config to this repository (Part 5).
2. Host it as a Cloudflare Worker with static assets (or Pages, which Cloudflare is
   folding into Workers), in the personal account, with a **distinct Worker name**. Its
   custom domain is created by its own Wrangler deploy, which also creates the DNS record.
3. Add its origin (`https://NAME.medical-psilocybin.org`) to `ALLOWED_ORIGINS` in
   `analytics/wrangler.toml` and redeploy the counter; copy the beacon from
   `tools/sync-count.py` into the application's pages so it reports to the same endpoint.
   Or decide, in writing, that the application is not counted.
4. Link it from the hub, and from any rules page that hands the reader to it, by absolute
   URL.
5. Disclose it on the rules site's about page if it receives anything from a reader.

### 4.2 Rename or move a host

The addresses are in exactly these places: `docs/CNAME`; the GitHub Pages custom-domain
setting (which reads `CNAME`); the DNS record; `ALLOWED_ORIGINS` in `analytics/wrangler.toml`;
`ENDPOINT` in `tools/sync-count.py`; the redirect rule at the apex; the dashboard text in
`analytics/worker.js`; `analytics/setup.sh` (`SITE`); and any absolute link on another host.
Change all of them in one pass.

### 4.3 Put the hub at the apex

Done September 7, 2026 except the last switch. The hub is its own project (1.4a), bound by
zone routes over the placeholder A records rather than custom domains, because deleting the
records needs a DNS permission the deploy credentials lack. Both hosts are in the counter's
`ALLOWED_ORIGINS`. `rules.` is untouched.

**To switch the apex to the hub:** in the Cloudflare dashboard, zone `medical-psilocybin.org`,
Rules, Redirect Rules, disable "Redirect to rules subdomain". The Worker answers at once; to
verify, `curl -sI https://medical-psilocybin.org/` returns `200` with the hub, and
`https://www.medical-psilocybin.org/` the same. To revert, enable the rule again.

If custom domains are ever wanted instead of routes: delete the two placeholder A records,
change `routes` in the hub's `wrangler.jsonc` back to `custom_domain: true`, and deploy.

### 4.4 Move `rules.` from GitHub Pages to Cloudflare

Do this when the repository goes private, and not in the fortnight before a hearing.

1. Create the Worker with static assets for `docs/` in the personal account, distinct name,
   config **outside this repository's root** (a separate deploy repository, or a subfolder
   with every wrangler call passing `--config`). Deploy to a temporary hostname and check
   every page, the stubs, and the counter beacon.
2. Confirm the zone SSL mode is Full.
3. Change the `rules` DNS record to the Worker's custom domain (Wrangler does this) and set
   it proxied. Remove the custom domain from the GitHub Pages settings and delete
   `docs/CNAME` in the same change, so GitHub stops answering for the host.
4. `ALLOWED_ORIGINS` and `ENDPOINT` are unchanged: the host name did not move.
5. Keep GitHub Pages disabled afterwards, or the `github.io` address serves a stale copy.

### 4.5 Make the repository private

Only after Part 4.4. Flipping a public repository to private while GitHub Pages serves it
takes the site down on the Free plan. Making it private does not unpublish what was public
before; it stops further reading.

---

## Part 5: What must never be done

- Push to `main`.
- Delete or overwrite `docs/CNAME` while GitHub Pages serves the site.
- Add a `wrangler.json`, `wrangler.jsonc`, or `wrangler.toml` anywhere but `analytics/`. The
  Cloudflare GitHub integration offers a root config named `nmmpab-count` that serves
  `docs/` as static assets; accepting it replaces the counter with a copy of the website. It
  has happened twice. Keep the Cloudflare build connection for this repository disconnected.
- Proxy the `rules` record as a side effect of anything. It is a step in Part 4.4 only.
- Commit a secret, a private-workspace link, or the name of the person who compiles the site.
- Run `wrangler` without `--config ./analytics/wrangler.toml`. Wrangler prefers a JSON config
  found above the working directory over a TOML beside it.

---

## Part 6: Checking the live state

The counter is the counter, not a mirror of the site:

```
GET https://api.cloudflare.com/client/v4/accounts/2418db2ff3f95726c374a86551d2436e/workers/scripts/nmmpab-count/settings
```

`bindings` must include one of type `d1`. An empty list means the mirror is deployed
(Part 5).

GitHub Pages configuration:

```bash
gh api repos/notafeature/NMMPAB_Rules-Draft-Analysis/pages
```

Cloudflare zone: DNS records at `/zones/ff942843527ffd5e5cc100101df756ad/dns_records`, SSL
mode at `/settings/ssl`, the redirect rule at
`/rulesets/phases/http_request_dynamic_redirect/entrypoint`, Worker custom domains at
`/accounts/<account>/workers/domains`.

DNS from anywhere:

```bash
dig +short rules.medical-psilocybin.org CNAME
```

Refresh Part 1 of this file from those reads whenever any of it changes, and date the
refresh here: last read September 7, 2026.

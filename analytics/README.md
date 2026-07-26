# The visit counter

GitHub Pages keeps no access logs and exposes none, so the site had no way of knowing whether anyone opened it. This directory holds a Cloudflare Worker that answers four questions and no more than four: is anyone reading this, roughly how many, which pages, and is there any signal that the Department of Health is among them.

Identifying an individual reader is not the goal, and the schema is built so that it is not possible: there is no cookie, no stored address, and no identifier that survives the day it was written.

| File | What it is |
|---|---|
| `worker.js` | The whole service: the collector, the dashboard, and the query layer |
| `schema.sql` | The D1 schema, with a comment on every column saying why it exists |
| `wrangler.toml` | Deploy config. No credentials, by design; the repository is public |
| `setup.sh` | One command that does the whole deployment |

The beacon that every page carries is not here. It is written into `docs/*.html` by `tools/sync-count.py`, in the same way the nav and the provenance block are written by their own tools.

## The options, and why this one

Five real options were considered. Only one of them can answer the fourth question at all.

**Cloudflare in front of Pages.** Point a custom domain at GitHub Pages, proxy it through Cloudflare, and count at the edge with nothing in the page. This is the most robust collection method available: no JavaScript, no cross-origin request, nothing a content blocker can refuse. The price is the site's URL. `notafeature.github.io/NMMPAB_Rules-Draft-Analysis` is printed in `UPDATING.md`, in the README, and in whatever board members have already bookmarked or been emailed, and moving it to a custom domain to gain a counter is a large change made for a small reason. Free-plan zone analytics is also thinner than it looks: request counts and countries, no per-reader uniqueness, and no network operator.

**Self-hosted Plausible or Umami.** The best dashboards of the five, and no code to maintain. Plausible Community Edition wants ClickHouse and Postgres and about 2 GB of memory, which is a real server at real monthly cost. Umami is much lighter and will sit on a free Vercel plus a free Postgres, but free Postgres tiers sleep, expire, or vanish, and the failure mode is losing exactly the record you were trying to keep. Both are disqualified on substance rather than cost: neither records the network the request came from, so neither can say anything about the fourth question.

**GoatCounter.** Free for non-commercial use, genuinely privacy-minded, one script tag, and the fastest thing here to set up. Two problems. It records no network information either. And the data would live on a third party's server, which on a site read by state officials is another party to disclose on the about page and another party to trust. Self-hosting it is a single Go binary over SQLite and is genuinely cheap, but that is a server again.

**A Worker with KV.** KV is a key-value store with no query language, so you count what you decided in advance to count: one key per page per day, incremented. That is fast, cheap, and sufficient for questions one to three. It cannot answer a question you did not anticipate, and unique-ish counts need a key per reader per day, at which point you are storing the same rows as D1 with none of the ability to ask anything of them. KV would be the right answer at ten million hits a day, where D1 write costs would start to matter. At a few dozen readers the flexibility is free.

**A Worker with D1. This is what is deployed.** You define the schema, so you can record `request.cf.asOrganization`, the network that carried the request, which is the only field in any of these options that bears on the Department of Health question. SQL over the raw rows means a question that was not anticipated can still be asked. There is no server to patch, nothing to back up, and no third party. Free-tier limits are not close: a few dozen readers produce a few hundred rows a month against a five-gigabyte allowance.

**The deciding argument.** Three of the five options cannot answer the fourth question at any price, because they do not collect the field. Between the two that remain, the edge-proxy option collects better but costs the site's URL, and the Worker costs about four hundred lines that are already written. The real, honest cost of the choice made is that the dashboard is bespoke, and that a cross-origin beacon is blockable in a way that edge collection is not.

## What is recorded

One row per event. Every column is in `schema.sql` with its reason.

Kept: the UTC timestamp and date, whether it was a page view or a document click, the file name, a daily reader hash, the referring host with no path or query string, a two-letter country code, and the autonomous system number and name.

Never kept: IP addresses, cookies, any identifier lasting beyond one UTC day, city or coordinates, referrer paths, query strings, and anything a reader typed.

The reader hash is `SHA-256(day + secret + IP + user-agent)`, truncated. Two visits from one person on one day collide, which is what makes a daily unique count possible. The same person tomorrow gets a different hash, which is what makes a per-person history impossible. None of the inputs are stored.

Global Privacy Control and Do Not Track are honoured in the page script, so those readers are never counted. Every number in the dashboard is a floor rather than a total, and the dashboard says so in its footer.

Records older than 400 days are deleted by a sweep that runs at most once per UTC day.

## Deploy

```
./analytics/setup.sh
```

That is the whole thing. It logs into Cloudflare, deploys the Worker, generates the hashing secret, asks for a dashboard password, writes the resulting address into all thirteen pages, and prints the dashboard URL. Then commit and push, and numbers start arriving once someone loads a page.

The D1 database already exists and its schema is already applied. It was created on July 26, 2026 in the personal Cloudflare account, not the Santa Fe Psychedelic Society one, and both IDs are in `wrangler.toml`.

Until the address is set the beacon is present, valid, identical on every page, and inert: it returns before sending anything. That is deliberate, because a guessed hostname would record nothing while looking like it worked.

### On the choice of hostname

The Worker deploys to `nmmpab-count.<subdomain>.workers.dev`, a free address Cloudflare hands out with no DNS to configure and no domain to buy. It names neither this site nor any organisation, which matters: the address appears in the page source of every page, on a site whose about page states that it is unaffiliated with the Department of Health or the Advisory Board and whose `UPDATING.md` states that it is not an advocacy site.

The one real drawback is that `workers.dev` is a shared domain that some corporate and government networks category-block outright, and those are precisely the networks whose readers this is meant to detect. If the state-network row never appears and you suspect that is why, move to a subdomain of a domain you own: set `workers_dev = false` in `wrangler.toml`, add

```toml
[[routes]]
pattern = "count.example.org"
custom_domain = true
```

redeploy, and run `python3 tools/sync-count.py --endpoint https://count.example.org`. Wrangler creates the DNS record and the certificate itself, provided the domain is on Cloudflare DNS in the same account.

If the site itself ever moves to a custom domain, add that origin to `ALLOWED_ORIGINS` in `wrangler.toml` and redeploy, and the counter follows.

### Who can see what

The numbers are yours alone. The dashboard and the data API are the only routes that read anything, both are behind a password, and both send `X-Robots-Tag: noindex`. Nobody else can reach them, and there is no public or shareable view.

One thing is public, unavoidably: the address itself. It sits in the page source of a public site in a public repository, so anyone who views source can see that a counter exists and what it is called. That is why the address should not carry a name you would rather not attach to this, and it is why `about.html` says plainly what is collected instead of leaving it to be discovered.

## The dashboard

`https://<worker-host>/`, HTTP Basic auth, user `owner` and the `DASH_PASS` secret. It is the only route that reads data, it sends `X-Robots-Tag: noindex`, and it is served with `Cache-Control: no-store`.

It shows visits per day with readers overlaid, totals for the selected range, views and reader-days per page, referring hosts, documents opened, countries, and the network table described below. Ranges are 7, 30 and 90 days, one year, and everything.

Two words used throughout:

- **Reader-days.** One person, on one day, counts once. A page reread all afternoon is one reader-day. Summed across a month, one person reading on five days is five reader-days.
- **Unique readers over a range** is not available and cannot be recovered, because the hash rotates daily. That is the deliberate trade for not being able to follow anyone. The dashboard reports daily readers and reader-days and does not pretend to more.

To harden access further, put Cloudflare Access in front of the Worker hostname in Zero Trust and require a Google login. The Basic auth check stays as a second gate.

### How reliable the organisation signal is

Not very, and the dashboard says so above the table rather than in a footnote.

`request.cf.asOrganization` is the name of the autonomous system that carried the request. That is an internet provider, not an employer. A person reading from a Department of Health office may appear as the state network. The same person reading at home appears as Comcast or Lumen, on a phone as T-Mobile or Verizon, and on a VPN as the VPN company, none of which is distinguishable from any other reader in New Mexico.

So a state-network row is weak positive evidence that somebody at the department opened the page, and the absence of one is no evidence either way. It is a signal worth having because there is no other, not a signal worth relying on.

The `net_kind` column is a guess made by regular expression in `worker.js`. The patterns for a New Mexico state network are a guess at a registration string, not a lookup. When a plausible row appears in the dashboard, put its exact name into `NET_RULES` and redeploy, and it will classify correctly from then on.

## Cost

Zero at this volume. Workers and D1 both have free tiers measured in millions of operations, and a few dozen readers produce a few hundred rows a month. There is no monthly bill to forget about and no server to keep alive.

## Operating notes

**Rotating the salt.** Changing `SALT` makes every hash after the change unrelated to every hash before it. Nothing breaks; daily counts on either side of the change stay correct, because the hash is only ever compared within a single day. Rotating occasionally is good hygiene.

**Querying by hand.** `npx wrangler d1 execute nmmpab-count --remote --command "SELECT path, COUNT(*) FROM hits GROUP BY path"`.

**Deleting everything.** `npx wrangler d1 execute nmmpab-count --remote --command "DELETE FROM hits"`, or delete the database in the Cloudflare dashboard. Then run `python3 tools/sync-count.py --endpoint ""` to make the beacon inert again, and remove the Measurement section from `docs/about.html`.

**Abuse.** The collector is unauthenticated, because it has to be. It is kept narrow: the request must carry an allowed `Origin`, the path must match a file this site actually has, and obvious robot user-agents are dropped. Someone determined could still post junk rows. The blast radius is a wrong number on a private dashboard, which `DELETE FROM hits WHERE ...` fixes.

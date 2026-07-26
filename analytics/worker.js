/**
 * nmmpab-count: a visit counter for the NMMPAB rules-draft site.
 *
 * The site is static HTML on GitHub Pages, served at
 * rules.medical-psilocybin.org, and GitHub keeps no access logs and exposes
 * none. This Worker is the only place a visit is recorded, and it stores the
 * least it can while still answering the four questions that were asked:
 * is anyone reading this, roughly how many, which pages, and is there any
 * sign the Department of Health is among them.
 *
 * It runs at count.medical-psilocybin.org, a sibling of the site's own
 * hostname rather than a third-party tracking service. That matters for the
 * question being asked: a network filter blocks a registrable domain, so any
 * filter that can reach medical-psilocybin.org to read the site can reach it
 * to record the visit. The Worker is deliberately NOT in front of the site,
 * so it cannot take the site down.
 *
 * Routes:
 *   POST /e         record an event, sent by the beacon in every page
 *   GET  /px        image fallback when sendBeacon and fetch are blocked
 *   GET  /          the dashboard, HTTP Basic auth, owner only
 *   GET  /api/summary?days=N   the dashboard's data, same auth
 *   GET  /health    liveness, no auth, reveals no data
 *
 * What is never stored: IP addresses, cookies, any identifier that survives
 * the UTC day, city or coordinates, referrer paths or query strings, and any
 * value a reader typed. See docs/about.html, which says the same thing to the
 * people being counted.
 */

const RETENTION_DAYS = 400;

// Applied to every authenticated response. The dashboard is a private page
// that reads a database, so it should not be framed, sniffed, cached by
// anything in between, indexed, or allowed to load or reach anything off its
// own origin. The page is entirely self-contained, so the policy can be
// absolute rather than a list of exceptions.
const SECURITY_HEADERS = {
  "Cache-Control": "no-store, no-cache, must-revalidate, private",
  "Content-Security-Policy":
    "default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; " +
    "connect-src 'self'; img-src 'self' data:; form-action 'none'; " +
    "frame-ancestors 'none'; base-uri 'none'",
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "Referrer-Policy": "no-referrer",
  "X-Robots-Tag": "noindex, nofollow, noarchive",
  "Permissions-Policy": "geolocation=(), camera=(), microphone=(), interest-cohort=()",
  "Cross-Origin-Opener-Policy": "same-origin",
  "Cross-Origin-Resource-Policy": "same-origin",
};


const PV_PATH = /^[a-z0-9-]+\.html$/;
const DL_PATH = /^documents\/[A-Za-z0-9._%-]+\.(pdf|txt)$/;

const BOT_UA = /bot|crawl|spider|slurp|headless|lighthouse|monitor|curl|wget|python-requests|axios|scrapy|facebookexternalhit|whatsapp|telegram|slackbot|discord|embedly|pingdom|uptime|preview|feedfetcher|archive\.org/i;

// Networks worth naming when they appear. This is a guess at a string, not a
// lookup: Cloudflare reports the name of the autonomous system that carried
// the request, and state agencies are not consistent about how theirs is
// registered. Add the exact string here once one is observed in the dashboard.
const NET_RULES = [
  ["state-nm", /state of new ?mexico|new ?mexico (department|dept|state)|nm ?doit|state of nm|doh\.nm\.gov/i],
  ["gov", /\bgov(ernment)?\b|county of|city of|municipal|federal|\bstate of\b/i],
  ["edu", /universit|college|\bschool|academic|\bedu\b|research and education/i],
  // "verizon" alone is wrong here: Verizon Business is a wireline network.
  ["mobile", /wireless|cellular|\bmobile\b|t-?mobile|verizon wireless|at&?t mobility|us ?cellular/i],
  ["hosting", /amazon|aws|google (cloud|llc)|microsoft|azure|cloudflare|digitalocean|linode|akamai|fastly|ovh|hetzner|oracle|vpn|warp|proxy|hosting|datacenter|data ?center|colo/i],
];

function classifyNetwork(org) {
  if (!org) return "unknown";
  for (const [kind, re] of NET_RULES) if (re.test(org)) return kind;
  return "consumer";
}

function allowedOrigins(env) {
  return (env.ALLOWED_ORIGINS || "https://notafeature.github.io")
    .split(",").map((s) => s.trim()).filter(Boolean);
}

function corsHeaders(request, env) {
  const origin = request.headers.get("Origin") || "";
  const ok = allowedOrigins(env).includes(origin);
  return {
    "Access-Control-Allow-Origin": ok ? origin : allowedOrigins(env)[0],
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
  };
}

function utcDay(d) {
  return d.toISOString().slice(0, 10);
}

function daysAgo(n) {
  return utcDay(new Date(Date.now() - n * 86400000));
}

async function sha256hex(s) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

/**
 * A reader identifier that lasts one UTC day and then is gone.
 *
 * The inputs are the connecting address, the browser string and a secret, all
 * mixed with the date. None of the inputs are stored. Two visits from the same
 * person on the same day share a hash; the same person tomorrow does not. That
 * is what makes a daily unique count possible and a per-person history not.
 */
async function visitorHash(request, env, day) {
  const ip = request.headers.get("CF-Connecting-IP") || "0.0.0.0";
  const ua = request.headers.get("User-Agent") || "";
  const salt = env.SALT || "nmmpab-count-unsalted";
  return (await sha256hex(day + "|" + salt + "|" + ip + "|" + ua)).slice(0, 16);
}

function normalisePath(raw) {
  let p = String(raw || "").trim().split("#")[0].split("?")[0];
  p = p.replace(/^https?:\/\/[^/]+/i, "").replace(/^\/+/, "");
  p = p.replace(/^NMMPAB_Rules-Draft-Analysis\//i, "");
  p = p.replace(/^\.\//, "");
  if (p === "" || p.endsWith("/")) p += "index.html";
  return p.length > 120 ? "" : p;
}

function refHost(raw) {
  try {
    const h = new URL(String(raw)).hostname.toLowerCase().replace(/^www\./, "");
    return h.length > 100 ? "" : h;
  } catch (e) {
    return "";
  }
}

/** Delete rows past the retention window, at most once per UTC day. */
async function sweep(env, today) {
  const row = await env.DB.prepare("SELECT v FROM meta WHERE k='purged_on'").first();
  if (row && row.v === today) return;
  await env.DB.batch([
    env.DB.prepare("DELETE FROM hits WHERE day < ?1").bind(daysAgo(RETENTION_DAYS)),
    env.DB.prepare("INSERT INTO meta (k,v) VALUES ('purged_on',?1) ON CONFLICT(k) DO UPDATE SET v=?1").bind(today),
  ]);
}

async function record(request, env, ctx, { kind, path, ref, nojs, siteHost }) {
  const ua = request.headers.get("User-Agent") || "";
  if (!ua || BOT_UA.test(ua)) return;

  const p = normalisePath(path);
  const isPv = PV_PATH.test(p);
  const isDl = DL_PATH.test(p);
  if (kind === "dl" ? !isDl : !isPv) return;

  const now = new Date();
  const day = utcDay(now);
  const cf = request.cf || {};
  const org = String(cf.asOrganization || "").slice(0, 120);
  const net = classifyNetwork(org);

  // Drop datacenter traffic. A newly registered domain gets swept by
  // vulnerability scanners within minutes, and the ones that render pages run
  // the counter script and arrive looking like readers. The first two rows
  // this counter ever recorded were exactly that, from AWS, alongside probes
  // for /.ssh/id_rsa and /backup.zip in the same minute.
  //
  // The cost is that a reader behind a commercial VPN is not counted either.
  // That is the right trade here: the readers this exists to detect are on
  // office and home networks, and an uncounted reader is better than a
  // scanner counted as one.
  if (net === "hosting") return;

  await env.DB.prepare(
    "INSERT INTO hits (ts,day,kind,path,visitor,ref_host,country,asn,as_org,net_kind,nojs,site_host) " +
    "VALUES (?1,?2,?3,?4,?5,?6,?7,?8,?9,?10,?11,?12)"
  ).bind(
    now.toISOString().slice(0, 19) + "Z",
    day,
    kind === "dl" ? "dl" : "pv",
    p,
    await visitorHash(request, env, day),
    refHost(ref),
    String(cf.country || "").slice(0, 2),
    Number(cf.asn) || 0,
    org,
    net,
    nojs ? 1 : 0,
    refHost(siteHost) || ""
  ).run();

  ctx.waitUntil(sweep(env, day).catch(() => {}));
}

/* ------------------------------------------------------------------ auth */

function timingSafeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return diff === 0;
}

function authed(request, env) {
  const pass = env.DASH_PASS;
  if (!pass) return false;
  const header = request.headers.get("Authorization") || "";
  if (!header.startsWith("Basic ")) return false;
  let decoded;
  try {
    decoded = atob(header.slice(6));
  } catch (e) {
    return false;
  }
  const i = decoded.indexOf(":");
  if (i < 0) return false;
  return timingSafeEqual(decoded.slice(0, i), env.DASH_USER || "owner") &&
         timingSafeEqual(decoded.slice(i + 1), pass);
}

function challenge() {
  return new Response("Authentication required.", {
    status: 401,
    headers: {
      "WWW-Authenticate": 'Basic realm="nmmpab-count", charset="UTF-8"',
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
}

/* ------------------------------------------------------------------ query */

async function summary(env, days) {
  const from = daysAgo(days);
  const q = (sql) => env.DB.prepare(sql).bind(from).all();

  const [totals, daily, pages, refs, orgs, dls, countries, hosts] = await Promise.all([
    q("SELECT COUNT(*) views, COUNT(DISTINCT visitor||day) visitor_days, " +
      "COUNT(DISTINCT day) active_days, MIN(day) first_day, " +
      "SUM(nojs) nojs FROM hits WHERE day >= ?1 AND kind='pv'"),
    q("SELECT day, COUNT(*) views, COUNT(DISTINCT visitor) readers " +
      "FROM hits WHERE day >= ?1 AND kind='pv' GROUP BY day ORDER BY day"),
    q("SELECT path, COUNT(*) views, COUNT(DISTINCT visitor||day) visitor_days, MAX(day) last_day " +
      "FROM hits WHERE day >= ?1 AND kind='pv' GROUP BY path ORDER BY views DESC"),
    q("SELECT COALESCE(NULLIF(ref_host,''),'(none)') host, COUNT(*) n, " +
      "COUNT(DISTINCT visitor||day) visitor_days FROM hits WHERE day >= ?1 " +
      "GROUP BY COALESCE(NULLIF(ref_host,''),'(none)') ORDER BY n DESC LIMIT 25"),
    // Group by the expressions, not by the output aliases. SQLite resolves a
    // GROUP BY name against the real columns first, and `hits` has a column
    // called `kind`, so `GROUP BY kind` would silently split every network
    // into a page-view row and a document-click row.
    q("SELECT COALESCE(NULLIF(as_org,''),'(unknown)') org, net_kind, asn, COUNT(*) n, " +
      "COUNT(DISTINCT visitor||day) visitor_days, MIN(day) first_day, MAX(day) last_day " +
      "FROM hits WHERE day >= ?1 " +
      "GROUP BY COALESCE(NULLIF(as_org,''),'(unknown)'), net_kind, asn " +
      "ORDER BY visitor_days DESC, n DESC LIMIT 40"),
    q("SELECT path, COUNT(*) n, COUNT(DISTINCT visitor||day) visitor_days, MAX(day) last_day " +
      "FROM hits WHERE day >= ?1 AND kind='dl' GROUP BY path ORDER BY n DESC LIMIT 30"),
    q("SELECT COALESCE(NULLIF(country,''),'??') code, COUNT(*) n FROM hits " +
      "WHERE day >= ?1 GROUP BY COALESCE(NULLIF(country,''),'??') ORDER BY n DESC LIMIT 20"),
    q("SELECT COALESCE(NULLIF(site_host,''),'(before this was recorded)') host, COUNT(*) n, " +
      "COUNT(DISTINCT visitor||day) visitor_days, MAX(day) last_day FROM hits WHERE day >= ?1 " +
      "GROUP BY COALESCE(NULLIF(site_host,''),'(before this was recorded)') ORDER BY n DESC LIMIT 10"),
  ]);

  const t = totals.results[0] || {};
  return {
    range: { days, from, to: utcDay(new Date()) },
    totals: {
      views: t.views || 0,
      visitorDays: t.visitor_days || 0,
      activeDays: t.active_days || 0,
      firstDay: t.first_day || null,
      nojs: t.nojs || 0,
      downloads: dls.results.reduce((a, r) => a + r.n, 0),
    },
    daily: daily.results,
    pages: pages.results,
    referrers: refs.results,
    orgs: orgs.results,
    downloads: dls.results,
    countries: countries.results,
    hosts: hosts.results,
    retentionDays: RETENTION_DAYS,
  };
}

/* --------------------------------------------------------------- handler */

const GIF = Uint8Array.from([
  0x47, 0x49, 0x46, 0x38, 0x39, 0x61, 1, 0, 1, 0, 0x80, 0, 0, 0, 0, 0, 0, 0, 0,
  0x21, 0xf9, 4, 1, 0, 0, 0, 0, 0x2c, 0, 0, 0, 0, 1, 0, 1, 0, 0, 2, 2, 0x44,
  1, 0, 0x3b,
]);

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Answered here rather than passed upstream, since the browser asks for it
    // on every dashboard load and GitHub Pages has nothing to give it.
    if (url.pathname === "/favicon.ico") {
      return new Response(null, { status: 204, headers: { "Cache-Control": "max-age=86400" } });
    }

    const path = url.pathname.replace(/\/+$/, "") || "/";

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: corsHeaders(request, env) });
    }

    if (path === "/health") {
      return new Response("ok", { headers: { "Content-Type": "text/plain" } });
    }

    // Ingest. Deliberately unauthenticated, so it is kept narrow: the request
    // must come from an allowed origin, carry a path this site actually has,
    // and not look like a robot.
    if (path === "/e" && request.method === "POST") {
      const cors = corsHeaders(request, env);
      const origin = request.headers.get("Origin") || "";
      if (!allowedOrigins(env).includes(origin)) {
        return new Response(null, { status: 204, headers: cors });
      }
      let body = {};
      try {
        const text = (await request.text()).slice(0, 2000);
        body = JSON.parse(text);
      } catch (e) {
        return new Response(null, { status: 204, headers: cors });
      }
      ctx.waitUntil(
        record(request, env, ctx, {
          kind: body.k === "dl" ? "dl" : "pv",
          path: body.p,
          ref: body.r,
          nojs: false,
          siteHost: origin,
        }).catch(() => {})
      );
      return new Response(null, { status: 204, headers: cors });
    }

    // Last-resort fallback for the beacon. A managed desktop can have
    // sendBeacon and fetch unavailable or blocked by policy while still
    // loading images, and those readers are exactly the ones worth counting.
    if (path === "/px") {
      const ref = request.headers.get("Referer") || "";
      const host = refHost(ref);
      const ok = !host || allowedOrigins(env).some((o) => refHost(o) === host);
      if (ok) {
        ctx.waitUntil(
          record(request, env, ctx, {
            kind: "pv",
            path: url.searchParams.get("p"),
            ref: url.searchParams.get("r") || "",
            nojs: true,
            siteHost: ref,
          }).catch(() => {})
        );
      }
      return new Response(GIF, {
        headers: {
          "Content-Type": "image/gif",
          "Cache-Control": "no-store, no-cache, must-revalidate",
          "Content-Length": String(GIF.length),
        },
      });
    }

    if (path === "/api/summary") {
      if (!authed(request, env)) return challenge();
      const raw = parseInt(url.searchParams.get("days") || "30", 10);
      const days = [7, 30, 90, 365, 3650].includes(raw) ? raw : 30;
      const data = await summary(env, days);
      return new Response(JSON.stringify(data), { headers: { ...SECURITY_HEADERS, "Content-Type": "application/json; charset=utf-8" } });
    }

    if (path === "/") {
      if (!authed(request, env)) return challenge();
      return new Response(DASHBOARD, { headers: { ...SECURITY_HEADERS, "Content-Type": "text/html; charset=utf-8" } });
    }

    return new Response("Not found", { status: 404 });
  },
};

/* ------------------------------------------------------------- dashboard */

const DASHBOARD = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Readers of the NMMPAB rules site</title>
<style>
  :root{
    color-scheme: light dark;
    --bg:#FBFAFC; --surface:#FFFFFF; --surface-2:#F4F1F8;
    --text:#1A1621; --text-muted:#645E71; --text-faint:#8A8397;
    --border:#E4E0EB; --border-strong:#D2CCDF;
    --accent:#5A4A88;
    --grid:#EEEBF3; --axis:#D2CCDF;
    --s1:#4a3aa7;  /* page views */
    --s2:#eb6834;  /* readers */
    --sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
    --mono:ui-monospace,"SF Mono","SFMono-Regular",Menlo,Consolas,monospace;
  }
  @media (prefers-color-scheme: dark){
    :root:where(:not([data-theme="light"])){
      --bg:#0F0D13; --surface:#17141D; --surface-2:#1E1A28;
      --text:#F3F1F7; --text-muted:#A9A2B8; --text-faint:#7E7791;
      --border:#2A2536; --border-strong:#3A3348;
      --accent:#9C8BD0;
      --grid:#221E2E; --axis:#3A3348;
      --s1:#9085e9; --s2:#d95926;
    }
  }
  :root[data-theme="dark"]{
    --bg:#0F0D13; --surface:#17141D; --surface-2:#1E1A28;
    --text:#F3F1F7; --text-muted:#A9A2B8; --text-faint:#7E7791;
    --border:#2A2536; --border-strong:#3A3348;
    --accent:#9C8BD0;
    --grid:#221E2E; --axis:#3A3348;
    --s1:#9085e9; --s2:#d95926;
  }
  *{box-sizing:border-box;}
  body{margin:0; background:var(--bg); color:var(--text); font-family:var(--sans);
       font-size:15px; line-height:1.55; -webkit-font-smoothing:antialiased;}
  .col{max-width:1000px; margin:0 auto; padding:26px 20px 70px;}
  h1{font-size:21px; margin:0 0 4px; font-weight:650; letter-spacing:-.01em;}
  h2{font-size:15px; margin:0 0 3px; font-weight:650;}
  .sub{color:var(--text-muted); font-size:13.5px; margin:0;}
  .card{background:var(--surface); border:1px solid var(--border); border-radius:12px;
        padding:16px 18px; margin-top:16px;}
  .cardhead{margin-bottom:14px;}

  .ranges{display:flex; gap:6px; flex-wrap:wrap; margin-top:14px;}
  .ranges button{font:inherit; font-size:13px; padding:5px 12px; border-radius:999px;
    border:1px solid var(--border-strong); background:var(--surface); color:var(--text-muted); cursor:pointer;}
  .ranges button:hover{color:var(--text); background:var(--surface-2);}
  .ranges button[aria-pressed="true"]{background:var(--accent); border-color:var(--accent); color:#fff;}

  .kpis{display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; margin-top:16px;}
  .kpi{background:var(--surface); border:1px solid var(--border); border-radius:12px; padding:13px 15px;}
  .kpi .k{font-size:11px; font-weight:700; letter-spacing:.08em; text-transform:uppercase;
          color:var(--text-faint); margin:0 0 6px;}
  .kpi .v{font-size:30px; font-weight:600; line-height:1.05; margin:0; letter-spacing:-.02em;}
  .kpi .n{font-size:12.5px; color:var(--text-muted); margin:5px 0 0;}

  .legend{display:flex; gap:16px; align-items:center; font-size:12.5px; color:var(--text-muted); margin:0 0 8px;}
  .legend span{display:flex; align-items:center; gap:6px;}
  .swatch{width:10px; height:10px; border-radius:3px; display:inline-block;}
  .chartwrap{position:relative; overflow-x:auto;}
  svg{display:block; max-width:100%;}
  .tip{position:absolute; pointer-events:none; opacity:0; transition:opacity .1s;
       background:var(--text); color:var(--bg); font-size:12px; line-height:1.45;
       padding:6px 9px; border-radius:7px; white-space:nowrap; z-index:5;}
  .tip b{font-weight:650;}

  table{width:100%; border-collapse:collapse; font-size:13.5px;}
  th{text-align:left; font-size:11px; font-weight:700; letter-spacing:.07em; text-transform:uppercase;
     color:var(--text-faint); padding:0 10px 7px 0; border-bottom:1px solid var(--border);}
  td{padding:7px 10px 7px 0; border-bottom:1px solid var(--border); vertical-align:top;}
  tr:last-child td{border-bottom:none;}
  td.num, th.num{text-align:right; font-variant-numeric:tabular-nums; padding-right:20px;}
  td:last-child, th:last-child{padding-right:0;}
  .barcell{position:relative; min-width:110px;}
  .bar{height:9px; border-radius:0 4px 4px 0; background:var(--s1); display:block;}
  .mono{font-family:var(--mono); font-size:12.5px;}
  .tag{display:inline-block; font-size:10.5px; font-weight:700; text-transform:uppercase;
       letter-spacing:.05em; border-radius:999px; padding:1px 7px; border:1px solid var(--border-strong);
       color:var(--text-muted);}
  .tag.state-nm{color:#fff; background:#2C7A57; border-color:#2C7A57;}
  .tag.gov{color:#fff; background:#4a3aa7; border-color:#4a3aa7;}
  .tag.edu{color:#fff; background:#8A5A12; border-color:#8A5A12;}

  .note{font-size:13px; color:var(--text-muted); line-height:1.6; margin:0 0 14px;
        border-left:2px solid var(--border-strong); padding-left:13px;}
  .note b{color:var(--text); font-weight:650;}
  details.tbl{margin-top:12px;}
  details.tbl summary{font-size:12.5px; color:var(--text-muted); cursor:pointer;}
  .empty{color:var(--text-faint); font-size:13.5px; padding:8px 0;}
  footer{margin-top:26px; font-size:12.5px; color:var(--text-faint); line-height:1.6;}
</style>
</head>
<body>
<div class="col">
  <h1>Readers of the NMMPAB rules site</h1>
  <p class="sub">rules.medical-psilocybin.org. No cookies, no reader identified.</p>

  <div class="ranges" id="ranges" role="group" aria-label="Time range">
    <button data-days="7">7 days</button>
    <button data-days="30" aria-pressed="true">30 days</button>
    <button data-days="90">90 days</button>
    <button data-days="365">1 year</button>
    <button data-days="3650">All</button>
  </div>

  <div class="kpis" id="kpis"></div>

  <div class="card">
    <div class="cardhead">
      <h2>Visits per day</h2>
      <p class="sub">Bars are page views. The line is readers, counted once each per day.</p>
    </div>
    <p class="legend">
      <span><i class="swatch" style="background:var(--s1)"></i> Page views</span>
      <span><i class="swatch" style="background:var(--s2)"></i> Readers that day</span>
    </p>
    <div class="chartwrap" id="dailywrap"></div>
    <details class="tbl"><summary>Show the daily numbers as a table</summary>
      <div id="dailytable"></div>
    </details>
  </div>

  <div class="card">
    <div class="cardhead">
      <h2>Which pages</h2>
      <p class="sub">Reader-days counts one person once per day per page, so a page reread all afternoon counts once.</p>
    </div>
    <div id="pages"></div>
  </div>

  <div class="card">
    <div class="cardhead">
      <h2>Which network the reader came from</h2>
    </div>
    <p class="note"><b>Read this before reading the table.</b> The name below is the network that carried the
      request, as Cloudflare sees it. It is an internet provider, not an employer. Somebody reading from a
      Department of Health office may show as the state network; the same person reading at home or on a phone
      shows as Comcast, Lumen, T-Mobile or Verizon, which is indistinguishable from any other reader in New
      Mexico. A VPN shows the VPN company. So a state-network row is <b>weak positive evidence</b> that
      somebody at the department opened the page, and the absence of one is <b>no evidence either way</b>.
      Nothing here identifies a person, and it should not be used to try.</p>
    <div id="orgs"></div>
  </div>

  <div class="card">
    <div class="cardhead">
      <h2>Which address readers used</h2>
    </div>
    <p class="note">The site is served at <span class="mono">rules.medical-psilocybin.org</span>, and the older
      <span class="mono">notafeature.github.io</span> address now redirects there, so nearly every row should
      show the new domain. A github.io row is somebody who reached the old address from a stale bookmark or an
      emailed link and was redirected. <b>What this table cannot tell you is whether the new domain is blocked
      for somebody.</b> A reader whose network filters
      <span class="mono">medical-psilocybin.org</span> never loads the page, so the beacon never fires and
      nothing appears here at all, which looks exactly like nobody reading. If you suspect that, the test is
      to ask one person at the department to open the link and say whether it loaded.</p>
    <div id="hosts"></div>
  </div>

  <div class="card">
    <div class="cardhead">
      <h2>Where readers arrived from</h2>
      <p class="sub">Host only. No path, no search terms. "(none)" is a direct visit, a bookmark, or a link from an email or document.</p>
    </div>
    <div id="refs"></div>
  </div>

  <div class="card">
    <div class="cardhead">
      <h2>Documents opened</h2>
      <p class="sub">Clicks on a PDF link. A file opened from a bookmark or a saved copy is not counted.</p>
    </div>
    <div id="dls"></div>
  </div>

  <div class="card">
    <div class="cardhead">
      <h2>Country</h2>
      <p class="sub">Country only. City and coordinates are never stored.</p>
    </div>
    <div id="countries"></div>
  </div>

  <footer id="foot"></footer>
</div>

<script>
(function(){
  var state = { days: 30, data: null };
  var $ = function(id){ return document.getElementById(id); };
  var esc = function(s){ return String(s == null ? "" : s).replace(/[&<>"]/g, function(c){
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); };
  var n = function(v){ return (v == null ? 0 : v).toLocaleString("en-US"); };

  function shortDay(d){
    var p = String(d).split("-");
    return p[1].replace(/^0/,"") + "/" + p[2];
  }

  function empty(msg){ return '<p class="empty">' + esc(msg) + '</p>'; }

  /* ---- KPI row ---- */
  function kpis(d){
    var t = d.totals;
    var peak = d.daily.reduce(function(a,r){ return r.readers > (a ? a.readers : -1) ? r : a; }, null);
    var tiles = [
      ["Page views", n(t.views), t.views ? "since " + (t.firstDay || d.range.from) : "nothing recorded yet"],
      ["Reader-days", n(t.visitorDays), "one person on one day counts once"],
      ["Most in a day", peak ? n(peak.readers) : "0",
        peak ? "readers, on " + peak.day + ", " + n(peak.views) + " views" : "no activity in range"],
      ["Active days", n(t.activeDays), "days with at least one reader, of " +
        (d.range.days > 999 ? "all time" : n(d.range.days))],
      ["Documents opened", n(t.downloads), "PDF links clicked"]
    ];
    $("kpis").innerHTML = tiles.map(function(k){
      return '<div class="kpi"><p class="k">' + esc(k[0]) + '</p><p class="v">' + esc(k[1]) +
             '</p><p class="n">' + esc(k[2]) + '</p></div>';
    }).join("");
  }

  /* ---- daily chart: columns for views, line for readers ---- */
  function daily(d){
    var wrap = $("dailywrap");
    var rows = d.daily;
    if (!rows.length){ wrap.innerHTML = empty("No visits recorded in this range."); $("dailytable").innerHTML = ""; return; }

    // Fill in the days with no visits, so a gap reads as a gap.
    var byDay = {}, i;
    for (i = 0; i < rows.length; i++) byDay[rows[i].day] = rows[i];
    var start = new Date(d.range.from + "T00:00:00Z");
    var end = new Date(d.range.to + "T00:00:00Z");
    var firstSeen = new Date((d.totals.firstDay || d.range.to) + "T00:00:00Z");
    if (firstSeen > start) start = firstSeen;
    var series = [];
    for (var t = start.getTime(); t <= end.getTime(); t += 86400000){
      var key = new Date(t).toISOString().slice(0,10);
      series.push(byDay[key] || { day: key, views: 0, readers: 0 });
    }
    if (series.length > 190) series = series.slice(series.length - 190);

    var W = Math.max(560, series.length * 13), H = 210;
    var padL = 34, padR = 12, padT = 12, padB = 26;
    var iw = W - padL - padR, ih = H - padT - padB;
    var max = Math.max(1, series.reduce(function(a,r){ return Math.max(a, r.views); }, 0));
    var ticks = max <= 4 ? max : 4;
    var step = Math.ceil(max / ticks);
    var top = step * ticks;
    var bw = Math.max(3, Math.min(22, iw / series.length - 2));
    var x = function(i){ return padL + (i + 0.5) * (iw / series.length); };
    var y = function(v){ return padT + ih - (v / top) * ih; };

    var svg = ['<svg viewBox="0 0 ' + W + ' ' + H + '" width="' + W + '" height="' + H +
               '" role="img" aria-label="Page views and readers per day">'];
    for (i = 0; i <= ticks; i++){
      var gv = step * i;
      svg.push('<line x1="' + padL + '" x2="' + (W - padR) + '" y1="' + y(gv) + '" y2="' + y(gv) +
               '" stroke="var(--grid)" stroke-width="1"/>');
      svg.push('<text x="' + (padL - 7) + '" y="' + (y(gv) + 4) + '" text-anchor="end" font-size="10.5" ' +
               'fill="var(--text-faint)" font-family="var(--sans)">' + gv + '</text>');
    }
    for (i = 0; i < series.length; i++){
      var r = series[i];
      if (r.views > 0){
        var h = Math.max(2, ih - (y(r.views) - padT));
        svg.push('<rect x="' + (x(i) - bw/2).toFixed(1) + '" y="' + y(r.views).toFixed(1) + '" width="' + bw.toFixed(1) +
                 '" height="' + h.toFixed(1) + '" rx="' + Math.min(4, bw/2).toFixed(1) + '" fill="var(--s1)"/>');
      }
    }
    var pts = series.map(function(r,i){ return x(i).toFixed(1) + "," + y(r.readers).toFixed(1); });
    svg.push('<polyline points="' + pts.join(" ") + '" fill="none" stroke="var(--s2)" stroke-width="2" ' +
             'stroke-linejoin="round" stroke-linecap="round"/>');
    for (i = 0; i < series.length; i++){
      if (series[i].readers > 0 && series.length <= 60){
        svg.push('<circle cx="' + x(i).toFixed(1) + '" cy="' + y(series[i].readers).toFixed(1) +
                 '" r="3.2" fill="var(--s2)" stroke="var(--surface)" stroke-width="2"/>');
      }
    }
    // Date labels: first, last, and a few in between, so they never collide.
    var every = Math.max(1, Math.ceil(series.length / 10));
    for (i = 0; i < series.length; i++){
      if (i % every === 0 || i === series.length - 1){
        svg.push('<text x="' + x(i).toFixed(1) + '" y="' + (H - 8) + '" text-anchor="middle" font-size="10.5" ' +
                 'fill="var(--text-faint)" font-family="var(--sans)">' + shortDay(series[i].day) + '</text>');
      }
    }
    for (i = 0; i < series.length; i++){
      svg.push('<rect class="hit" data-i="' + i + '" x="' + (x(i) - (iw/series.length)/2).toFixed(1) + '" y="' + padT +
               '" width="' + (iw/series.length).toFixed(1) + '" height="' + ih + '" fill="transparent"/>');
    }
    svg.push('<line x1="' + padL + '" x2="' + (W - padR) + '" y1="' + y(0) + '" y2="' + y(0) +
             '" stroke="var(--axis)" stroke-width="1"/>');
    svg.push("</svg>");
    wrap.innerHTML = svg.join("") + '<div class="tip" id="tip"></div>';

    var tip = $("tip");
    wrap.querySelectorAll(".hit").forEach(function(el){
      el.addEventListener("mouseenter", function(){
        var r = series[+el.dataset.i];
        tip.innerHTML = "<b>" + r.day + "</b><br>" + n(r.views) + " views, " + n(r.readers) + " readers";
        tip.style.opacity = 1;
        var box = el.getBoundingClientRect(), pw = wrap.getBoundingClientRect();
        tip.style.left = Math.min(Math.max(0, box.left - pw.left + wrap.scrollLeft - 40), wrap.scrollWidth - 150) + "px";
        tip.style.top = "6px";
      });
      el.addEventListener("mouseleave", function(){ tip.style.opacity = 0; });
    });

    $("dailytable").innerHTML = table(
      ["Day", "Views", "Readers"],
      series.slice().reverse().map(function(r){
        return ['<span class="mono">' + r.day + "</span>", n(r.views), n(r.readers)];
      }), [false, true, true]);
  }

  function table(head, rows, nums){
    if (!rows.length) return empty("Nothing recorded in this range.");
    var h = head.map(function(c,i){ return '<th' + (nums[i] ? ' class="num"' : '') + '>' + esc(c) + "</th>"; }).join("");
    var b = rows.map(function(r){
      return "<tr>" + r.map(function(c,i){ return "<td" + (nums[i] ? ' class="num"' : '') + ">" + c + "</td>"; }).join("") + "</tr>";
    }).join("");
    return "<table><thead><tr>" + h + "</tr></thead><tbody>" + b + "</tbody></table>";
  }

  function pages(d){
    var max = d.pages.reduce(function(a,r){ return Math.max(a, r.views); }, 0) || 1;
    $("pages").innerHTML = table(
      ["Page", "", "Views", "Reader-days", "Last seen"],
      d.pages.map(function(r){
        var w = Math.max(3, Math.round((r.views / max) * 100));
        return [
          '<span class="mono">' + esc(r.path) + "</span>",
          '<span class="bar" style="width:' + w + '%"></span>',
          n(r.views), n(r.visitor_days), '<span class="mono">' + esc(r.last_day) + "</span>"
        ];
      }), [false, false, true, true, false]);
    var cells = document.querySelectorAll("#pages td:nth-child(2)");
    for (var i = 0; i < cells.length; i++) cells[i].className = "barcell";
  }

  function orgs(d){
    $("orgs").innerHTML = table(
      ["Network", "AS", "Kind", "Reader-days", "Requests", "First seen", "Last seen"],
      d.orgs.map(function(r){
        return [
          esc(r.org),
          '<span class="mono">' + (r.asn ? "AS" + r.asn : "") + "</span>",
          '<span class="tag ' + esc(r.net_kind) + '">' + esc(r.net_kind) + "</span>",
          n(r.visitor_days), n(r.n),
          '<span class="mono">' + esc(r.first_day) + "</span>",
          '<span class="mono">' + esc(r.last_day) + "</span>"
        ];
      }), [false, false, false, true, true, false, false]);
  }

  function simple(id, head, rows, nums){ $(id).innerHTML = table(head, rows, nums); }

  function render(d){
    state.data = d;
    kpis(d); daily(d); pages(d); orgs(d);
    simple("hosts", ["Address", "Requests", "Reader-days", "Last seen"],
      d.hosts.map(function(r){ return ['<span class="mono">' + esc(r.host) + "</span>", n(r.n), n(r.visitor_days),
        '<span class="mono">' + esc(r.last_day) + "</span>"]; }), [false, true, true, false]);
    simple("refs", ["Came from", "Requests", "Reader-days"],
      d.referrers.map(function(r){ return [esc(r.host), n(r.n), n(r.visitor_days)]; }), [false, true, true]);
    simple("dls", ["Document", "Clicks", "Reader-days", "Last seen"],
      d.downloads.map(function(r){ return ['<span class="mono">' + esc(r.path) + "</span>", n(r.n), n(r.visitor_days),
        '<span class="mono">' + esc(r.last_day) + "</span>"]; }), [false, true, true, false]);
    simple("countries", ["Country", "Requests"],
      d.countries.map(function(r){ return ['<span class="mono">' + esc(r.code) + "</span>", n(r.n)]; }), [false, true]);
    $("foot").innerHTML = "Range " + esc(d.range.from) + " to " + esc(d.range.to) + ". " +
      "Rows are deleted after " + n(d.retentionDays) + " days. " +
      n(d.totals.nojs) + " view(s) arrived through the image fallback. " +
      "Readers whose browser sends Global Privacy Control or Do Not Track are not counted at all, " +
      "so every number here is a floor rather than a total.";
  }

  function load(){
    $("kpis").innerHTML = '<p class="empty">Loading.</p>';
    fetch("/api/summary?days=" + state.days, { credentials: "same-origin" })
      .then(function(r){ if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(render)
      .catch(function(e){ $("kpis").innerHTML = '<p class="empty">Could not load: ' + esc(e.message) + "</p>"; });
  }

  $("ranges").addEventListener("click", function(e){
    var b = e.target.closest("button[data-days]");
    if (!b) return;
    state.days = +b.dataset.days;
    $("ranges").querySelectorAll("button").forEach(function(x){ x.removeAttribute("aria-pressed"); });
    b.setAttribute("aria-pressed", "true");
    load();
  });

  load();
})();
</script>
</body>
</html>`;

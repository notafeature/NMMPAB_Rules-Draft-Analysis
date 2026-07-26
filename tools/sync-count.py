#!/usr/bin/env python3
"""Keep the visit-counter beacon byte-identical across every page in docs/.

GitHub Pages keeps no logs and exposes none, so the only way to know whether
anyone is reading this site is to have each page say so. That is this block:
about twenty lines of JavaScript that report the file name of the page and the
host a reader arrived from, to a Cloudflare Worker in analytics/.

Same house rule as the nav: the block is physically duplicated in every page and
must be identical everywhere. Edit ENDPOINT or BEACON below, run this, and every
page gets the same block. Never hand-edit it in a page.

The endpoint lives here and nowhere else, so moving the counter to a different
hostname is one edit and one run.

Usage:
    python3 tools/sync-count.py                      # rewrite every page
    python3 tools/sync-count.py --check              # exit 1 if any page differs
    python3 tools/sync-count.py --endpoint https://h # set the host, then rewrite

Until an endpoint is set the block is inert: it is present, valid and identical
on every page, and it returns before sending anything. That is deliberate. A
guessed hostname would record nothing and look like it was working.
"""
import glob
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
SELF = os.path.abspath(__file__)

# The Worker's origin, no trailing slash. Printed by `npx wrangler deploy`.
ENDPOINT = "https://rules.medical-psilocybin.org/_count"

# What this sends, and nothing else:
#   k  "pv" for a page view, "dl" for a click on a document link
#   p  location.pathname, which the Worker reduces to a bare file name
#   r  document.referrer, which the Worker reduces to a bare host name
#
# Global Privacy Control and Do Not Track are honoured, which means the counts
# are a floor rather than a total. The dashboard says so.
BEACON = """<script id="countjs">
(function(){
  var E="__ENDPOINT__";
  if(!E) return;
  var nav=navigator;
  if(nav.globalPrivacyControl===true||nav.doNotTrack==="1"||window.doNotTrack==="1") return;
  if(location.protocol==="file:"||location.hostname==="localhost"||location.hostname==="127.0.0.1") return;

  function send(k,p){
    var body=JSON.stringify({k:k,p:p,r:document.referrer||""});
    try{
      if(nav.sendBeacon&&nav.sendBeacon(E+"/e",new Blob([body],{type:"text/plain;charset=UTF-8"}))) return;
    }catch(e){}
    try{
      if(window.fetch){
        fetch(E+"/e",{method:"POST",body:body,mode:"cors",keepalive:true,
                      headers:{"Content-Type":"text/plain;charset=UTF-8"}}).catch(function(){});
        return;
      }
    }catch(e){}
    new Image().src=E+"/px?p="+encodeURIComponent(p)+"&r="+encodeURIComponent(document.referrer||"");
  }

  send("pv",location.pathname);

  // Which documents actually get opened is half the question, and a PDF link
  // leaves the site without ever loading a page that could report it.
  document.addEventListener("click",function(e){
    var a=e.target&&e.target.closest&&e.target.closest('a[href$=".pdf"]');
    if(a) send("dl",a.getAttribute("href"));
  },true);
})();
</script>"""

PATTERN = re.compile(r'<script id="countjs">.*?</script>', re.S)
ANCHOR = "\n</body>"


def block():
    return BEACON.replace("__ENDPOINT__", ENDPOINT.rstrip("/"))


def set_endpoint(url):
    """Rewrite the ENDPOINT constant in this file, so the value has one home."""
    url = url.strip().rstrip("/")
    # A path rather than an origin means the counter is served from the site's
    # own hostname, which is the best case: no cross-origin request at all, and
    # nothing for a content blocker or a network filter to recognise.
    if url and not (url.startswith("https://") or url.startswith("/")):
        print("Endpoint must be an https:// origin, or a same-origin path such as /_count.")
        return 1
    src = open(SELF).read()
    new = re.sub(r'^ENDPOINT = ".*"$', 'ENDPOINT = "%s"' % url, src, count=1, flags=re.M)
    if new == src:
        print("Could not find the ENDPOINT line to rewrite.")
        return 1
    open(SELF, "w").write(new)
    print("endpoint    " + (url or "(cleared, beacon is inert)"))
    return 0


def main():
    argv = sys.argv[1:]
    global ENDPOINT

    if "--endpoint" in argv:
        i = argv.index("--endpoint")
        if i + 1 >= len(argv):
            print("--endpoint needs a URL, or \"\" to clear it.")
            return 1
        rc = set_endpoint(argv[i + 1])
        if rc:
            return rc
        ENDPOINT = argv[i + 1].strip().rstrip("/")

    check = "--check" in argv
    changed, ok = [], []
    want = block()

    for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        name = os.path.basename(path)
        src = open(path).read()
        if PATTERN.search(src):
            new = PATTERN.sub(lambda _: want, src, count=1)
        elif ANCHOR in src:
            new = src.replace(ANCHOR, "\n" + want + ANCHOR, 1)
        else:
            print("NO ANCHOR   " + name)
            return 1

        if new == src:
            ok.append(name)
        elif check:
            changed.append(name)
        else:
            open(path, "w").write(new)
            changed.append(name)

    for name in changed:
        print(("OUT OF SYNC " if check else "updated     ") + name)
    for name in ok:
        print("in sync     " + name)

    if check and changed:
        print("\n%d page(s) out of sync. Run without --check to fix." % len(changed))
        return 1

    total = len(changed) + len(ok)
    if ENDPOINT:
        print("\n%d page(s), counting to %s." % (total, ENDPOINT))
    else:
        print("\n%d page(s), beacon present and inert. No endpoint set: run\n"
              "    python3 tools/sync-count.py --endpoint https://YOUR-WORKER-HOST" % total)
    return 0


if __name__ == "__main__":
    sys.exit(main())

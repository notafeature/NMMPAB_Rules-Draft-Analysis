#!/usr/bin/env bash
#
# Turn the visit counter on. Run this once:
#
#     ./analytics/setup.sh
#
# It logs you into Cloudflare if you are not already, deploys the Worker to
# your personal account, generates the hashing secret, sets the dashboard
# password, wires the resulting address into all thirteen pages, and tells you
# the dashboard URL. Nothing here needs the Santa Fe Psychedelic Society.
#
# Safe to run again. Re-running redeploys and leaves the data alone.

set -euo pipefail
cd "$(dirname "$0")"
REPO=".."

say() { printf '\n\033[1m%s\033[0m\n' "$1"; }

# ---------------------------------------------------------------- 1. login
say "1/5  Cloudflare login"
if npx --yes wrangler@4 whoami >/dev/null 2>&1; then
  echo "Already logged in."
else
  echo "A browser window will open. Approve the login, then come back here."
  npx --yes wrangler@4 login
fi

# --------------------------------------------------------------- 2. deploy
say "2/5  Deploying the Worker"
DEPLOY_LOG="$(mktemp)"
npx --yes wrangler@4 deploy 2>&1 | tee "$DEPLOY_LOG"
URL="$(grep -oE 'https://[A-Za-z0-9._-]+\.workers\.dev' "$DEPLOY_LOG" | head -1)"
rm -f "$DEPLOY_LOG"

if [ -z "$URL" ]; then
  echo
  echo "Could not read the address out of the deploy output."
  read -r -p "Paste the https://...workers.dev address it printed: " URL
fi
URL="${URL%/}"

# -------------------------------------------------------------- 3. secrets
say "3/5  Secrets"

# The salt is what makes a reader hash unguessable. It is generated here and
# never needs to be seen or remembered by anyone.
head -c 32 /dev/urandom | base64 | tr -d '\n' \
  | npx --yes wrangler@4 secret put SALT >/dev/null
echo "Hashing secret: generated."

echo
echo "Pick a password for the dashboard. Press Enter to have one generated."
read -r -s -p "Password: " PASS; echo
if [ -z "$PASS" ]; then
  PASS="$(head -c 18 /dev/urandom | base64 | tr -d '/+=\n')"
  PASS_NOTE="$PASS        <-- generated, save it now"
else
  PASS_NOTE="the one you just typed"
fi
printf '%s' "$PASS" | npx --yes wrangler@4 secret put DASH_PASS >/dev/null
echo "Dashboard password: set."

# ---------------------------------------------------------------- 4. pages
say "4/5  Pointing the pages at it"
python3 "$REPO/tools/sync-count.py" --endpoint "$URL"

# ----------------------------------------------------------------- 5. done
say "5/5  Done"
cat <<EOF

  Dashboard   $URL/
  Username    owner
  Password    $PASS_NOTE

The pages are wired but not yet published. Commit and push:

    git add -A && git commit -m "Point the visit counter at $URL" && git push

Numbers start appearing a few minutes after that, once GitHub Pages rebuilds
and somebody loads a page. Until then the dashboard will be empty, which is
correct rather than broken.
EOF

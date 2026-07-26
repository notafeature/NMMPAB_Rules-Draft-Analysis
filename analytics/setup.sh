#!/usr/bin/env bash
#
# Turn the visit counter on. Run this once:
#
#     ./analytics/setup.sh
#
# It logs you into Cloudflare, deploys the Worker to your personal account,
# creates the DNS record and certificate for count.medical-psilocybin.org,
# generates the hashing secret, and sets the dashboard password.
#
# It does not touch the site. GitHub Pages serves rules.medical-psilocybin.org
# directly, and nothing here sits in front of that.
#
# Safe to run again. Re-running redeploys and leaves the data alone.

set -euo pipefail
cd "$(dirname "$0")"

# Every wrangler call pins its config explicitly. Changing directory is NOT
# enough: wrangler searches upwards from the working directory and prefers a
# JSON config it finds above one it was standing next to, so a wrangler.jsonc
# at the repository root silently wins over this directory's wrangler.toml.
# That is not hypothetical. The Cloudflare GitHub integration puts exactly
# such a file at the root, naming the same Worker and pointing it at docs/ as
# static assets, and without this flag setup.sh deploys that mirror over the
# counter and reports success.
CFG="--config ./wrangler.toml"

COUNTER="https://count.medical-psilocybin.org"
SITE="https://rules.medical-psilocybin.org"
say() { printf '\n\033[1m%s\033[0m\n' "$1"; }

# ---------------------------------------------------------------- 1. login
say "1/4  Cloudflare login"
if npx --yes wrangler@4 whoami >/dev/null 2>&1; then
  echo "Already logged in."
else
  echo "A browser window will open. Approve the login, then come back here."
  npx --yes wrangler@4 login
fi

# --------------------------------------------------------------- 2. deploy
say "2/4  Deploying"
echo "This claims count.medical-psilocybin.org and creates its DNS record."
echo
if ! npx --yes wrangler@4 deploy $CFG; then
  cat <<'EOF'

Deploy failed. The usual cause is that a DNS record for "count" already
exists, which blocks Wrangler from creating the one it needs.

Fix: Cloudflare dashboard, medical-psilocybin.org, DNS, delete the existing
"count" record, then run this script again. Wrangler will recreate it.

Do not delete the "rules" record. That one is the site.
EOF
  exit 1
fi

# -------------------------------------------------------------- 3. secrets
say "3/4  Secrets"

# The salt is what makes a reader hash unguessable. It is generated here and
# never needs to be seen or remembered by anyone.
head -c 32 /dev/urandom | base64 | tr -d '\n' \
  | npx --yes wrangler@4 secret put SALT $CFG >/dev/null
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
printf '%s' "$PASS" | npx --yes wrangler@4 secret put DASH_PASS $CFG >/dev/null
echo "Dashboard password: set."

# ----------------------------------------------------------------- 4. done
say "4/4  Verifying"
if npx --yes wrangler@4 deploy $CFG --dry-run 2>&1 | grep -q "env.DB"; then
  echo "D1 binding present. The counter is what is deployed."
else
  echo "WARNING: no D1 binding. Something other than analytics/wrangler.toml was used."
  echo "Check for a wrangler.json or wrangler.jsonc at the repository root and delete it."
  exit 1
fi

say "Done"
cat <<EOF

  Dashboard   $COUNTER/
  Username    owner
  Password    $PASS_NOTE

The site itself is untouched and still served by GitHub Pages at
  $SITE/

Numbers appear once somebody loads a page. Until then the dashboard is empty,
which is correct rather than broken.
EOF

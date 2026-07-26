#!/usr/bin/env bash
#
# Put the site on rules.medical-psilocybin.org and turn the visit counter on.
# Run this once:
#
#     ./analytics/setup.sh
#
# It logs you into Cloudflare, deploys the Worker to your personal account,
# creates the DNS record and certificate for rules.medical-psilocybin.org,
# generates the hashing secret, and sets the dashboard password.
#
# After this the site answers on BOTH addresses, independently:
#   https://rules.medical-psilocybin.org/            served by this Worker
#   https://notafeature.github.io/NMMPAB_Rules-Draft-Analysis/   served by GitHub
# That is deliberate. If a network filter blocks one, the other still works.
#
# Safe to run again. Re-running redeploys and leaves the data alone.

set -euo pipefail
cd "$(dirname "$0")"

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
echo "This claims rules.medical-psilocybin.org and creates its DNS record."
echo
if ! npx --yes wrangler@4 deploy; then
  cat <<'EOF'

Deploy failed. The usual cause is that a DNS record for "rules" already
exists, which blocks Wrangler from creating the one it needs.

Fix: Cloudflare dashboard, medical-psilocybin.org, DNS, delete the existing
"rules" record, then run this script again. Wrangler will recreate it.
EOF
  exit 1
fi

# -------------------------------------------------------------- 3. secrets
say "3/4  Secrets"

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

# ----------------------------------------------------------------- 4. done
say "4/4  Done"
cat <<EOF

  Site        $SITE/
  Dashboard   $SITE/_count/
  Username    owner
  Password    $PASS_NOTE

The old address keeps working and is not redirected:
  https://notafeature.github.io/NMMPAB_Rules-Draft-Analysis/

Check both open before you hand the new one to anybody. Readers on either
address are counted, and the dashboard has a "Which address readers used"
table, which is how you find out if a filter is blocking the new domain.

Numbers appear once somebody loads a page. Until then the dashboard is empty,
which is correct rather than broken.
EOF

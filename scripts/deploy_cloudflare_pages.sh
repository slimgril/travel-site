#!/usr/bin/env bash
# Cloudflare Pages — travel-site Production deploy（Cutover 2026-07-30）
# Knowledge: .ai-kos/DEPLOY_MIGRATION.md
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUNDLE="${ROOT}/dist-surge-upload"
PROJECT="${CF_PAGES_PROJECT:-travel-site-quarter}"
BRANCH="${CF_PAGES_BRANCH:-main}"
WRANGLER_VER="${WRANGLER_VER:-4}"

# Prefer local wrangler if present (avoids npx hang); else npx
if [[ -x /Users/mac/.npm/_npx/c943b712072b77c4/node_modules/.bin/wrangler ]]; then
  WRANGLER=(/Users/mac/.npm/_npx/c943b712072b77c4/node_modules/.bin/wrangler)
else
  WRANGLER=(npx --yes "wrangler@${WRANGLER_VER}")
fi

if [[ ! -d "${BUNDLE}" ]]; then
  echo "ERROR: missing bundle: ${BUNDLE}"
  echo "Run package_preview_deploy / sips outside sandbox first."
  exit 1
fi

if [[ ! -f "${BUNDLE}/index.html" ]]; then
  echo "ERROR: ${BUNDLE}/index.html not found — refuse empty/partial upload"
  exit 1
fi

case "${BUNDLE}" in
  */dist|*/photos|*/photos/*)
    echo "ERROR: refusing forbidden upload root: ${BUNDLE}"
    exit 1
    ;;
esac

echo "Deploying ${BUNDLE} → Cloudflare Pages project=${PROJECT} branch=${BRANCH}"
echo "Production URL: https://${PROJECT}.pages.dev/"
cd "${ROOT}"
"${WRANGLER[@]}" pages deploy "${BUNDLE}" \
  --project-name="${PROJECT}" \
  --branch="${BRANCH}" \
  --commit-dirty=true

echo "Done."
echo "Production: https://${PROJECT}.pages.dev/"
echo "Surge fallback (if needed): npx surge@0.23.1 dist-surge-upload cluttered-breath.surge.sh"

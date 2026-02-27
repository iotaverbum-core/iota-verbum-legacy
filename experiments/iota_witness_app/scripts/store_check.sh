#!/usr/bin/env bash
set -euo pipefail

fail() {
  echo "[store-check] $1" >&2
  exit 1
}

echo "[store-check] checking privacy manifest file"
[ -f apps/mobile/ios/PrivacyInfo.xcprivacy ] || fail "PrivacyInfo.xcprivacy missing"

echo "[store-check] checking consent modal"
grep -q "AI Sharing Consent" apps/mobile/app/_layout.tsx || fail "First-run consent modal not found"

echo "[store-check] checking policy and terms wiring"
if ! grep -q "privacyPolicyUrl" apps/mobile/app.config.ts && ! grep -q "/v1/privacy" services/api/app/main.py; then
  fail "Neither privacy URL config nor /v1/privacy endpoint found"
fi
if ! grep -q "termsUrl" apps/mobile/app.config.ts && ! grep -q "/v1/terms" services/api/app/main.py; then
  fail "Neither terms URL config nor /v1/terms endpoint found"
fi

echo "[store-check] checking retention defaults"
grep -q "data_retention_days: int = 0" services/api/app/settings.py || fail "DATA_RETENTION_DAYS default must be 0"
grep -q "store_eden_text: bool = False" services/api/app/settings.py || fail "STORE_EDEN_TEXT default must be false"

echo "[store-check] checking backend request logs avoid raw text"
if rg -n "logger\.(info|warning|error).*text" services/api/app/main.py services/api/app/llm/openai_client.py >/dev/null; then
  fail "Potential raw text logging found in backend logger calls"
fi

echo "[store-check] checking mobile for key leakage"
if rg -n "OPENAI_API_KEY|IOTA_OPENAI_API_KEY|sk-[A-Za-z0-9]{10,}" apps/mobile/app apps/mobile/src apps/mobile/app.config.ts apps/mobile/package.json >/dev/null; then
  fail "Potential key leakage pattern found in mobile code"
fi

echo "[store-check] all checks passed"

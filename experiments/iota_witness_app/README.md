# EDEN - Witness Companion

EDEN is a minimalist spiritual companion app (`□ ◇ → Δ`) with deterministic safeguards around generated responses.

## Core guardrails

- EDEN voice is male, steady, sparse, and non-escalating.
- Companion posture only: not therapy, not medical care, not crisis care, not prophecy.
- No false divine authority statements.
- DVL is deterministic: generation is validated and repaired with hard rules.

## Compliance-ready behavior

- First-run explicit AI-sharing consent modal.
- "Not now" keeps app functional in **Local mode** (deterministic templates, no OpenAI call).
- Settings screen includes:
  - AI sharing toggle (revoke any time)
  - Privacy Policy link
  - Terms link
  - Delete my data
  - Contact link
  - About disclaimer
- Crisis/self-harm language triggers deterministic safety response and bypasses OpenAI.

## Privacy-first backend defaults

- `IOTA_DATA_RETENTION_DAYS=0`
- `IOTA_STORE_EDEN_TEXT=false`
- Raw user text is not persisted.
- Stored fields: text hash, modal scores, hinge action, attestation hashes, timestamps.

## Run locally

### Backend

```bash
cd services/api
python -m pip install -e .[dev]
uvicorn app.main:app --reload --port 8000
```

### Mobile

```bash
cd apps/mobile
npm install
set EXPO_PUBLIC_API_BASE_URL=http://localhost:8000
set EXPO_PUBLIC_PRIVACY_POLICY_URL=http://localhost:8000/v1/privacy
set EXPO_PUBLIC_TERMS_URL=http://localhost:8000/v1/terms
set EXPO_PUBLIC_LOCAL_CRISIS_HELP_URL=http://localhost:8000/v1/help/local-crisis
set EXPO_PUBLIC_CONTACT_EMAIL=support@example.com
npm run start
```

## API endpoints

- `POST /v1/season_entries` body `{ device_id, text, ai_consent, local_only }`
- `POST /v1/moments` body `{ device_id, text, ai_consent, local_only }`
- `GET /v1/trace?device_id=...`
- `DELETE /v1/user_data/{device_id}`
- `GET /v1/privacy`
- `GET /v1/terms`
- `GET /v1/help/local-crisis`
- `GET /health`

## Quality gates

Backend:

```bash
cd services/api
python -m ruff check app tests --no-cache
python -m mypy app
python -m pytest -q -p no:cacheprovider
```

Mobile:

```bash
cd apps/mobile
npm run typecheck
npm run lint
```

Store checks:

```bash
node scripts/store_check.js
```

## EAS commands

From `apps/mobile`:

```bash
npm run eas:configure
npm run eas:build:ios
npm run eas:build:android
npm run eas:submit:ios
npm run eas:submit:android
```

## Store submission files

- `store/APP_STORE_METADATA.md`
- `store/APP_REVIEW_NOTES.md`
- `store/PRIVACY_LABEL_GUIDE.md`
- `store/PLAY_STORE_DATA_SAFETY.md`
- `docs/STORE_SUBMISSION.md`

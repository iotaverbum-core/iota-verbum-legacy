# App Privacy Label Guide (Apple)

## Data processing
- User-entered reflection text is processed to produce a response.
- Anonymous `device_id` is used for retrieval/deletion control.

## Stored data by default
- SHA256 hash of text
- derived modal/posture fields
- deterministic hinge action
- attestation hashes
- timestamps

Defaults:
- `DATA_RETENTION_DAYS=0`
- `STORE_EDEN_TEXT=false`

This means raw text is not stored, and final EDEN text is not stored unless explicitly enabled server-side.

## User controls
- AI sharing opt-in/opt-out in Settings.
- Delete all device data in Settings (`DELETE /v1/user_data/{device_id}`).

## Third-party processing
- OpenAI is used only when user has explicitly consented.
- If consent is off or local-only is enabled, OpenAI is bypassed.
- Crisis/self-harm flag forces bypass of OpenAI.

## Claims to avoid in store copy
- Do not claim therapy or medical treatment.
- Do not claim prophetic certainty.
- Do not claim guaranteed outcomes.

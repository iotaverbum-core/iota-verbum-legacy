# Play Store Data Safety Guide

## Collected/processed data
- User-entered text for response generation.
- Anonymous `device_id` for deletion and trace retrieval.

## Data stored
- By default: text hash, modal fields, hinge action, attestation hashes, timestamps.
- Raw text is not stored.
- Final EDEN response text is not stored by default (`STORE_EDEN_TEXT=false`).

## Retention and defaults
- `DATA_RETENTION_DAYS=0` (privacy-first default).
- Storage remains minimal until user deletes data.

## Sharing with third parties
- OpenAI processing happens only after explicit in-app consent.
- Local-only mode works without AI sharing.
- Crisis flag always bypasses OpenAI.

## User controls
- Revoke AI sharing consent in Settings.
- Delete all backend data tied to device ID in Settings.

## Positioning guardrails
- Not therapy.
- Not medical care.
- Not crisis care.
- Not prophecy.

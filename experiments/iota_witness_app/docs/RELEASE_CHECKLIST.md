# Release Checklist

## Pre-release QA

1. Launch app and confirm header symbols `? ? ? ?` appear.
2. Confirm first-run consent modal appears with `I agree` and `Not now`.
3. Choose `Not now` and submit Season and Moment entries.
4. Confirm responses show `Local mode` label.
5. Enable AI sharing in Settings and submit another Season and Moment entry.
6. Confirm normal response path works and output remains concise.
7. Submit crisis sample text and verify safety response path and local-help link.
8. Open Privacy Policy, Terms, and Contact links from Settings.
9. Tap `Delete my data` and confirm no errors.

## Automated gates

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

Store gate:

```bash
cd ..
node scripts/store_check.js
```

## Build and submit commands

```bash
cd apps/mobile
npm run eas:configure
npm run eas:build:ios
npm run eas:build:android
npm run eas:submit:ios
npm run eas:submit:android
```

## Store docs to paste

- `store/APP_STORE_METADATA.md`
- `store/APP_REVIEW_NOTES.md`
- `store/PRIVACY_LABEL_GUIDE.md`
- `store/PLAY_STORE_DATA_SAFETY.md`

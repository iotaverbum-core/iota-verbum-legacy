# Store Submission

## iOS Privacy Manifest

Manifest file location:
- `apps/mobile/ios/PrivacyInfo.xcprivacy`

Runtime config wiring:
- `apps/mobile/app.config.ts` -> `ios.privacyManifests`

Build aggregation setting:
- `apps/mobile/app.config.ts` plugin `expo-build-properties`
- `privacyManifestAggregationEnabled: true`

This prevents duplicate manifest generation issues (for example "multiple commands produce PrivacyInfo.xcprivacy").

## How the manifest is bundled

1. Keep `apps/mobile/ios/PrivacyInfo.xcprivacy` in source control.
2. Keep `ios.privacyManifests` populated in `app.config.ts`.
3. Run `npm run eas:build:ios`.
4. Verify the archive contains exactly one `PrivacyInfo.xcprivacy`.

## Required-reason updates

1. Update `NSPrivacyAccessedAPITypes` in `apps/mobile/ios/PrivacyInfo.xcprivacy`.
2. Mirror the same changes in `app.config.ts` under `ios.privacyManifests`.
3. Rebuild iOS and re-verify archive contents.

## Reviewer notes source

Use `store/APP_REVIEW_NOTES.md` directly in App Store Connect.

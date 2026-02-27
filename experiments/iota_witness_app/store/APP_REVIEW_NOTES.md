# App Review Notes

## Reviewer summary
- App type: Christian companion app for reflection and abiding in Christ.
- Not therapy, not medical care, not crisis care, not prophecy.
- No account and no sign-in required.

## Core test flow
1. Launch app.
2. Confirm first-run consent modal appears with `I agree` and `Not now`.
3. Tap `Not now`.
4. Open `Season (?)` or `Moment (?)` and submit sample text.
5. Confirm response appears with `Local mode` label.
6. Open `Settings (?)` and enable `AI sharing`.
7. Submit a new Season or Moment entry and confirm standard response flow.
8. In `Settings (?)`, open Privacy Policy and Terms.
9. In `Settings (?)`, tap `Delete my data`.

## Sample inputs
- Season: `I feel defensive this week and I keep hiding.`
- Moment: `I reacted quickly and now I feel exposed.`
- Crisis safety test: `I want to hurt myself.`

Expected crisis result:
- AI generation is bypassed.
- User receives brief safety guidance and local-help direction.

## Consent and privacy behavior
- AI sharing is explicit opt-in only.
- `Not now` keeps app usable in Local mode (deterministic templates only).
- Consent can be revoked in Settings.
- Delete-my-data removes stored records for that device ID.

## Compliance notes
- No analytics SDK by default.
- No ATT prompt.
- App is not marketed for kids.

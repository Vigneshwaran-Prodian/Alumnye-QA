# Triage — run-20261003-185504

alumnye | android | module `auth`

| Metric | Count |
|---|---|
| total | 1 |
| passed | 0 |
| passed zero ai | 0 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 1 |
| error | 0 |
| blocked | 0 |
| skipped | 0 |
| ai calls | 0 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | AUTH-004 | Positive | New user registers with yopmail email + OTP | none | element-not-found: button 'Create account' not found | reports/results/alumnye/run-20261003-185504/AUTH-004_FAILED.png |

## Entry paths the runner navigated (Splash -> ... -> target)

- AUTH-004: Splash -> Skip -> Create account -> Email tab -> Terms checkbox: ticked

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- AUTH-004: email_tab -> ViewGroup at x64,y318 477x100 | primary_button -> ViewGroup at x53,y771 975x127 | terms_checkbox -> ViewGroup at x105,y907 53x54 | verify_button -> ViewGroup at x53,y1266 975x139

# Triage — run-20261003-173842

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
| FAILED | AUTH-004 | Positive | New user registers with yopmail email + OTP | none | element-disabled: 'verify_button' ('Verify & join Alumnye →') is on screen but DISABLED - an earlier input is probably empty/invalid (step: verify the OTP and join) | reports/results/alumnye/run-20261003-173842/AUTH-004_FAILED.png |

## Entry paths the runner navigated (Splash -> ... -> target)

- AUTH-004: Splash -> Skip -> Create account -> Email tab

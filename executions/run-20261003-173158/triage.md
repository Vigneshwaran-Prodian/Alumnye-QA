# Triage — run-20261003-173158

alumnye | android | module `auth`

> **RUN STOPPED:** Stopped by user (Ctrl+C).

| Metric | Count |
|---|---|
| total | 4 |
| passed | 2 |
| passed zero ai | 2 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 1 |
| error | 0 |
| blocked | 0 |
| skipped | 1 |
| ai calls | 1 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | AUTH-004 | Positive | New user registers with yopmail email + OTP | none | likely-bug: 'otp_input' (One-time-code input) is missing from the screen — likely functionality break. Qwen: The OTP input field 'otp_input' is not present in the visible elements list, indicating a missing UI element. | reports/results/alumnye/run-20261003-173158/AUTH-004_FAILED.png |
| SKIPPED | AUTH-003 | Positive | New user registers with mobile number + SMS OTP | none | out-of-scope: Mobile-number scenarios are out of scope for now (owner decision 2026-10-03); email scenarios only | reports/results/alumnye/run-20261003-173158/AUTH-003_SKIPPED.png |
| PASSED | AUTH-001 | Positive | Fresh launch routes from Splash to the landing screen (Sign in / Google / Create account) | none |  | reports/results/alumnye/run-20261003-173158/AUTH-001_PASSED.png |
| PASSED | AUTH-002 | Positive | Landing layout: Sign in above Google, divider reads 'or' (v1.3.2) | none |  | reports/results/alumnye/run-20261003-173158/AUTH-002_PASSED.png |

## Entry paths the runner navigated (Splash -> ... -> target)

- AUTH-001: Splash -> Next -> Skip
- AUTH-002: Splash -> Next -> Skip
- AUTH-004: Splash -> Skip -> Create account -> Email tab

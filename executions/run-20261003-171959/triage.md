# Triage — run-20261003-171959

alumnye | android | module `auth`

> **RUN STOPPED:** Stopped by user (Ctrl+C).

| Metric | Count |
|---|---|
| total | 8 |
| passed | 2 |
| passed zero ai | 2 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 2 |
| error | 0 |
| blocked | 3 |
| skipped | 1 |
| ai calls | 2 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | AUTH-004 | Positive | New user registers with yopmail email + OTP | none | needs-human: 'primary_button' (Identifier screen: submit button (screen not yet seen)) not found; Qwen could not resolve it. The 'Continue' button is visible at index 35 with label 'Continue' matching the expected label list. | reports/results/alumnye/run-20261003-171959/AUTH-004_FAILED.png |
| FAILED | AUTH-005 | Positive | Sign in with Google using the account already on the device | none | likely-bug: 'home_marker' (Home reached (Anchor Home or Member Home)) is missing from the screen — likely functionality break. Qwen: The screen shows Google sign-in errors and no 'home_marker' element exists among visible elements. | reports/results/alumnye/run-20261003-171959/AUTH-005_FAILED.png |
| BLOCKED | AUTH-006 | Positive | Returning user signs in with OTP and skips Complete Profile | none | prerequisite: no registered test user yet - run AUTH-004 first | reports/results/alumnye/run-20261003-171959/AUTH-006_BLOCKED.png |
| BLOCKED | AUTH-007 | Positive | Logged-in session survives an app restart (Splash -> Home) | none | prerequisite: no registered test user yet — run AUTH-004 (email registration) first | reports/results/alumnye/run-20261003-171959/AUTH-007_BLOCKED.png |
| BLOCKED | AUTH-008 | Positive | Sign out returns to Sign In and ends the session | none | prerequisite: no registered test user yet — run AUTH-004 (email registration) first | reports/results/alumnye/run-20261003-171959/AUTH-008_BLOCKED.png |
| SKIPPED | AUTH-003 | Positive | New user registers with mobile number + SMS OTP | none | out-of-scope: Mobile-number scenarios are out of scope for now (owner decision 2026-10-03); email scenarios only | reports/results/alumnye/run-20261003-171959/AUTH-003_SKIPPED.png |
| PASSED | AUTH-001 | Positive | Fresh launch routes from Splash to the landing screen (Sign in / Google / Create account) | none |  | reports/results/alumnye/run-20261003-171959/AUTH-001_PASSED.png |
| PASSED | AUTH-002 | Positive | Landing layout: Sign in above Google, divider reads 'or' (v1.3.2) | none |  | reports/results/alumnye/run-20261003-171959/AUTH-002_PASSED.png |

## Entry paths the runner navigated (Splash -> ... -> target)

- AUTH-001: Splash -> Skip
- AUTH-002: Splash -> Skip
- AUTH-004: Splash -> Skip -> Create account
- AUTH-005: Splash -> Next -> Skip -> Sign in with Google

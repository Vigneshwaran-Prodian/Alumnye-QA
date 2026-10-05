# Triage — run-20261004-001220

alumnye | android | module `auth`

| Metric | Count |
|---|---|
| total | 5 |
| passed | 4 |
| passed zero ai | 4 |
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
| FAILED | AUTH-005 | Positive | Sign in with Google using the account already on the device | none | product-defect: Google sign-in is blocked by Google: 'Access blocked: Authorization Error'. Page text: Access blocked: Authorization Error; Custom scheme URIs are not allowed for 'WEB' client type.; error details; Error 400: invalid_request. The OAuth client is misconfigured (wrong client type / redirect URI) - product/config defect, not a script issue. | reports/results/alumnye/run-20261004-001220/AUTH-005_FAILED.png |
| PASSED | AUTH-006 | Positive | Returning user signs in with OTP and skips Complete Profile | none |  | reports/results/alumnye/run-20261004-001220/AUTH-006_PASSED.png |
| PASSED | AUTH-008 | Positive | Sign out returns to Sign In and ends the session | none |  | reports/results/alumnye/run-20261004-001220/AUTH-008_PASSED.png |
| PASSED | AUTH-009 | Positive | Member ID (code) on Complete Your Profile follows the typed name: <FirstInitial><LastInitial><n> | none |  | reports/results/alumnye/run-20261004-001220/AUTH-009_PASSED.png |
| PASSED | AUTH-013 | Negative | Complete Profile blocks empty / spaces-only names | none |  | reports/results/alumnye/run-20261004-001220/AUTH-013_PASSED.png |

## Entry paths the runner navigated (Splash -> ... -> target)

- AUTH-005: Splash -> Skip -> Sign in with Google
- AUTH-006: Splash -> Skip -> Sign in -> Email tab -> Terms checkbox: ticked
- AUTH-009: Splash -> Skip -> Create account -> Email tab -> Terms checkbox: ticked
- AUTH-013: Splash -> Skip -> Create account -> Email tab -> Terms checkbox: ticked

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- AUTH-005: google_button -> ViewGroup at x53,y1867 975x119

## Flow variants the runner detected

- AUTH-008: 'sign_out' found by exploring: nav_profile (scrolled as needed)

## Messages observed (review wording — also in message-catalog.md)

- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Access blocked: Authorization Error" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Custom scheme URIs are not allowed for 'WEB' client type." (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "error details" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Error 400: invalid_request" (on-screen)
- AUTH-009 | after: Member ID before typing | "(empty)" (state)
- AUTH-009 | after: after first name 'Meera' | "(empty)" (state)
- AUTH-009 | after: after last name 'Sharma' | "MS1" (state)
- AUTH-013 | after: empty first/last name | "(Continue button stays disabled)" (state)
- AUTH-013 | after: spaces-only first/last name | "(Continue button stays disabled)" (state)

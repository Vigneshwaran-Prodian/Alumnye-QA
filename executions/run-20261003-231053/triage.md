# Triage — run-20261003-231053

alumnye | android | module `auth`

> **RUN STOPPED:** Stopped by user (Ctrl+C).

| Metric | Count |
|---|---|
| total | 7 |
| passed | 3 |
| passed zero ai | 3 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 3 |
| error | 0 |
| blocked | 0 |
| skipped | 1 |
| ai calls | 1 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | AUTH-005 | Positive | Sign in with Google using the account already on the device | none | product-defect: Google sign-in is blocked by Google: 'Access blocked: Authorization Error'. Page text: Web View; Close tab; Minimize tab; Your connection to this site is not secure; accounts.google.com; Share. The OAuth client is misconfigured (wrong client type / redirect URI) - product/config defect, not a script issue. | reports/results/alumnye/run-20261003-231053/AUTH-005_FAILED.png |
| FAILED | AUTH-006 | Positive | Returning user signs in with OTP and skips Complete Profile | none | element-disabled: 'verify_button' ('Verify & join Alumnye →') is on screen but DISABLED - an earlier input is probably empty/invalid (step: verify OTP) | reports/results/alumnye/run-20261003-231053/AUTH-006_FAILED.png |
| FAILED | AUTH-007 | Positive | Logged-in session survives an app restart (Splash -> Home) | qwen | element-disabled: 'verify_button' ('Verify & join Alumnye →') is on screen but DISABLED - an earlier input is probably empty/invalid (step: verify OTP) | reports/results/alumnye/run-20261003-231053/AUTH-007_FAILED.png |
| SKIPPED | AUTH-003 | Positive | New user registers with mobile number + SMS OTP | none | out-of-scope: Mobile-number scenarios are out of scope for now (owner decision 2026-10-03); email scenarios only | reports/results/alumnye/run-20261003-231053/AUTH-003_SKIPPED.png |
| PASSED | AUTH-001 | Positive | Fresh launch routes from Splash to the landing screen (Sign in / Google / Create account) | none |  | reports/results/alumnye/run-20261003-231053/AUTH-001_PASSED.png |
| PASSED | AUTH-002 | Positive | Landing layout: Sign in above Google, divider reads 'or' (v1.3.2) | none |  | reports/results/alumnye/run-20261003-231053/AUTH-002_PASSED.png |
| PASSED | AUTH-004 | Positive | New user registers with yopmail email + OTP | none |  | reports/results/alumnye/run-20261003-231053/AUTH-004_PASSED.png |

## UI adaptations to confirm (never silent)

- AUTH-007: `landing_sign_in` -> `btnx:` via qwen — The 'Sign in' button is likely the 'ViewGroup' with icon U+F127 at index 17, which is commonly used for sign-in buttons in mobile UIs.

## Entry paths the runner navigated (Splash -> ... -> target)

- AUTH-001: Splash -> Skip
- AUTH-002: Splash -> Skip
- AUTH-004: Splash -> Skip -> Create account -> Email tab -> Terms checkbox: ticked
- AUTH-005: Splash -> Skip -> Sign in with Google
- AUTH-006: Splash -> Skip -> Sign in -> Email tab
- AUTH-007: Splash -> Sign in -> Email tab

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- AUTH-005: google_button -> ViewGroup at x53,y1867 975x119
- AUTH-006: landing_sign_in -> ViewGroup at x53,y1732 975x114 | email_tab -> ViewGroup at x64,y318 477x100 | primary_button -> ViewGroup at x53,y771 975x127
- AUTH-007: landing_sign_in -> ViewGroup at x42,y144 95x94 | email_tab -> ViewGroup at x64,y318 477x100 | primary_button -> ViewGroup at x53,y771 975x127

## Flow variants the runner detected

- AUTH-004: Profile form filled automatically: screen 1: Enter your first name = Vivek; screen 1: Enter your last name = Verma; screen 1: Enter your mobile number = 9602660531; screen 1: tapped 'Continue'

## Messages observed (review wording — also in message-catalog.md)

- AUTH-004 | after: profile screen 1: tapped 'Continue' | "SET DEFAULT PREFERENCES, Just now, Complete Your Profile Defaults, Fill your default food, room and travel choices to auto-fill event RSVPs." (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "SET DEFAULT PREFERENCES" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "Just now" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "Complete Your Profile Defaults" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "Fill your default food, room and travel choices to auto-fill event RSVPs." (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "Set Preferences →" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Web View" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Close tab" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Minimize tab" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Your connection to this site is not secure" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "accounts.google.com" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Share" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Customize and control Google Chrome" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Connection is secure" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Access blocked: Authorization Error" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "vignesh94.prodian@gmail.com" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Custom scheme URIs are not allowed for 'WEB' client type." (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "If you are a developer of alumnye, see" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "error details" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Error 400: invalid_request" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Open Google Account Help Center (external, opens in a new window)" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Privacy Policy (external, opens in a new window)" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Google Terms of Service (external, opens in a new window)" (on-screen)

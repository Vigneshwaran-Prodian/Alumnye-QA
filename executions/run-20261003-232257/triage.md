# Triage — run-20261003-232257

alumnye | android | module `auth`

| Metric | Count |
|---|---|
| total | 16 |
| passed | 10 |
| passed zero ai | 10 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 3 |
| error | 2 |
| blocked | 0 |
| skipped | 1 |
| ai calls | 3 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | AUTH-005 | Positive | Sign in with Google using the account already on the device | none | product-defect: Google sign-in is blocked by Google: 'Access blocked: Authorization Error'. Page text: Web View; Close tab; Minimize tab; Connection is secure; accounts.google.com; Share. The OAuth client is misconfigured (wrong client type / redirect URI) - product/config defect, not a script issue. | reports/results/alumnye/run-20261003-232257/AUTH-005_FAILED.png |
| FAILED | AUTH-006 | Positive | Returning user signs in with OTP and skips Complete Profile | none | assertion: Expected 'complete_profile_marker' to be absent: returning user must not see Complete Profile again | reports/results/alumnye/run-20261003-232257/AUTH-006_FAILED.png |
| FAILED | AUTH-008 | Positive | Sign out returns to Sign In and ends the session | qwen | assertion: Expected 'home_marker' to be absent: no Home after sign-out + restart | reports/results/alumnye/run-20261003-232257/AUTH-008_FAILED.png |
| ERROR | AUTH-009 | Positive | Complete Profile shows live member-code preview (<FirstInitial><LastInitial><n>) | none | driver: Message: A session is either terminated or not started; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#invalidsessionidexception | reports/results/alumnye/run-20261003-232257/AUTH-009_ERROR.png |
| ERROR | AUTH-013 | Negative | Complete Profile blocks empty / spaces-only names | none | driver: Message: Cannot set the element to '   '. Did you interact with the correct element? | reports/results/alumnye/run-20261003-232257/AUTH-013_ERROR.png |
| SKIPPED | AUTH-003 | Positive | New user registers with mobile number + SMS OTP | none | out-of-scope: Mobile-number scenarios are out of scope for now (owner decision 2026-10-03); email scenarios only | reports/results/alumnye/run-20261003-232257/AUTH-003_SKIPPED.png |
| PASSED | AUTH-001 | Positive | Fresh launch routes from Splash to the landing screen (Sign in / Google / Create account) | none |  | reports/results/alumnye/run-20261003-232257/AUTH-001_PASSED.png |
| PASSED | AUTH-002 | Positive | Landing layout: Sign in above Google, divider reads 'or' (v1.3.2) | none |  | reports/results/alumnye/run-20261003-232257/AUTH-002_PASSED.png |
| PASSED | AUTH-004 | Positive | New user registers with yopmail email + OTP | none |  | reports/results/alumnye/run-20261003-232257/AUTH-004_PASSED.png |
| PASSED | AUTH-007 | Positive | Logged-in session survives an app restart (Splash -> Home) | none |  | reports/results/alumnye/run-20261003-232257/AUTH-007_PASSED.png |
| PASSED | AUTH-010 | Negative | Invalid email / mobile format is rejected on Sign In | none |  | reports/results/alumnye/run-20261003-232257/AUTH-010_PASSED.png |
| PASSED | AUTH-011 | Negative | Incorrect OTP shows an error and does not sign in | none |  | reports/results/alumnye/run-20261003-232257/AUTH-011_PASSED.png |
| PASSED | AUTH-012 | Negative | Verify is blocked until Terms & Conditions are accepted | none |  | reports/results/alumnye/run-20261003-232257/AUTH-012_PASSED.png |
| PASSED | AUTH-014 | Edge | 'Wrong email? Go back' returns to the identifier step without creating an account | none |  | reports/results/alumnye/run-20261003-232257/AUTH-014_PASSED.png |
| PASSED | AUTH-015 | Edge | Resend is disabled during the countdown and works after it ends | none |  | reports/results/alumnye/run-20261003-232257/AUTH-015_PASSED.png |
| PASSED | AUTH-017 | Positive | Welcome / Create account screens have no Google/Apple options (v1.3.2) | none |  | reports/results/alumnye/run-20261003-232257/AUTH-017_PASSED.png |

## UI adaptations to confirm (never silent)

- AUTH-008: `sign_out` -> `btnx:, My Account` via qwen — The 'My Account' button with index 67 matches the expected 'Sign Out' intent as it's the only button with a clear label and context for profile screen.
- AUTH-008: `landing_sign_in` -> `btnx:Sign Out` via qwen — The 'Sign Out' button is present at index 12 with label 'Sign Out' and tap capability.
- AUTH-008: `landing_sign_in` -> `btnx:, Home` via qwen — The 'Sign in' button is represented by the 'Home' button with label '' at index 49, which is the closest match for the landing screen sign-in action.

## Entry paths the runner navigated (Splash -> ... -> target)

- AUTH-001: Splash -> Skip
- AUTH-002: Splash -> Skip
- AUTH-004: Splash -> Skip -> Create account -> Email tab -> Terms checkbox: ticked
- AUTH-005: Splash -> Skip -> Sign in with Google
- AUTH-006: Splash -> Skip -> Sign in -> Email tab -> Terms checkbox: ticked
- AUTH-009: Splash -> Skip -> Create account -> Email tab
- AUTH-010: Splash -> Skip -> Sign in -> Email tab
- AUTH-011: Splash -> Skip -> Create account -> Email tab -> Terms checkbox: ticked
- AUTH-012: Splash -> Skip -> Create account -> Email tab
- AUTH-013: Splash -> Skip -> Create account -> Email tab -> Terms checkbox: ticked
- AUTH-014: Splash -> Skip -> Create account -> Email tab
- AUTH-015: Splash -> Skip -> Create account -> Email tab
- AUTH-017: Splash -> Skip -> Create account

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- AUTH-005: google_button -> ViewGroup at x53,y1867 975x119
- AUTH-006: email_tab -> ViewGroup at x64,y318 477x100 | primary_button -> ViewGroup at x53,y771 975x127 | terms_checkbox -> ViewGroup at x105,y896 53x54 | verify_button -> ViewGroup at x53,y1255 975x139
- AUTH-008: nav_profile -> ViewGroup at x111,y541 849x273 | sign_out -> Button at x720,y2189 360x149 | confirm_sign_out -> ViewGroup at x830,y175 208x79
- AUTH-009: landing_create_account -> ViewGroup at x53,y2113 975x114 | email_tab -> ViewGroup at x64,y318 477x100 | primary_button -> ViewGroup at x53,y771 975x127
- AUTH-013: email_tab -> ViewGroup at x64,y318 477x100 | primary_button -> ViewGroup at x53,y771 975x127 | terms_checkbox -> ViewGroup at x105,y907 53x54 | verify_button -> ViewGroup at x53,y1266 975x139

## Flow variants the runner detected

- AUTH-004: Profile form filled automatically: screen 1: Enter your first name = Vivek; screen 1: Enter your last name = Reddy; screen 1: Enter your mobile number = 9330917835; screen 1: tapped 'Continue'

## Messages observed (review wording — also in message-catalog.md)

- AUTH-004 | after: profile screen 1: tapped 'Continue' | "MEMBER" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "ANCHOR" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "Welcome, Vivek" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "Welcome to Alumnye!" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "You don't have any events yet. When you're invited to a group, events will appear here so you can stay connected with your community." (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | ", Home" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "Home" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | ", My Group" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "My Group" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | ", My Account" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "My Account" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "SET DEFAULT PREFERENCES, Just now, Complete Your Profile Defaults, Fill your default food, room and travel choices to auto-fill event RSVPs." (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "SET DEFAULT PREFERENCES" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "Just now" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "Complete Your Profile Defaults" (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "Fill your default food, room and travel choices to auto-fill event RSVPs." (on-screen)
- AUTH-004 | after: profile screen 1: tapped 'Continue' | "Set Preferences →" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Web View" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Close tab" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Minimize tab" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Connection is secure" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "accounts.google.com" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Share" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Customize and control Google Chrome" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Access blocked: Authorization Error" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "vignesh94.prodian@gmail.com" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Custom scheme URIs are not allowed for 'WEB' client type." (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "If you are a developer of alumnye, see" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "error details" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Error 400: invalid_request" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Open Google Account Help Center (external, opens in a new window)" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Privacy Policy (external, opens in a new window)" (on-screen)
- AUTH-005 | after: tapped Sign in with Google and chose the device account | "Google Terms of Service (external, opens in a new window)" (on-screen)
- AUTH-010 | after: entered invalid identifier 'abc@' | "(Continue button stays disabled)" (state)
- AUTH-010 | after: entered invalid identifier '12345' | "(Continue button stays disabled)" (state)
- AUTH-010 | after: entered invalid identifier 'no spaces@yopmail.com' | "(Continue button stays disabled)" (state)
- AUTH-011 | after: entered wrong OTP 000000 and tapped Verify | "Invalid OTP" (on-screen)
- AUTH-011 | after: entered wrong OTP 000000 and tapped Verify | "Resend code (1:50)" (on-screen)
- AUTH-011 | after: entered wrong OTP 000000 and tapped Verify | "Resend code (1:49)" (on-screen)
- AUTH-011 | after: entered wrong OTP 000000 and tapped Verify | "Resend code (1:48)" (on-screen)
- AUTH-011 | after: entered wrong OTP 000000 and tapped Verify | "Resend code (1:47)" (on-screen)
- AUTH-012 | after: entered a valid OTP but did not tick the Terms checkbox | "(Verify & join Alumnye stays disabled)" (state)
- AUTH-013 | after: empty first/last name | "(Continue button stays disabled)" (state)
- AUTH-015 | after: arrived on the Verify identity screen | "Resend code (2:00)" (state)
- AUTH-015 | after: tapped Resend code after the countdown ended | "Resend code (2:00)" (on-screen)
- AUTH-015 | after: tapped Resend code after the countdown ended | "Success, A new code has been sent" (on-screen)
- AUTH-015 | after: tapped Resend code after the countdown ended | "Success" (on-screen)
- AUTH-015 | after: tapped Resend code after the countdown ended | "A new code has been sent" (on-screen)
- AUTH-015 | after: tapped Resend code after the countdown ended | "Resend code (1:59)" (on-screen)
- AUTH-015 | after: tapped Resend code after the countdown ended | "Resend code (1:58)" (on-screen)

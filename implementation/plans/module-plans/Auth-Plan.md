# Auth Plan

Reusable decisions and standing checks for BF1 (Auth & onboarding).

## Standing checks
- Every Auth screen: no "welcome back" copy on a first-time path (v1.5 item — do NOT assert yet).
- Sign In layout must keep Sign In button above social options and divider "or" (v1.3.2) — strict check, no self-heal.
- Terms & Conditions acceptance is mandatory at first login (DR-088).

## Real screens seen on device (2026-10-03, from the first run's evidence)
- Landing screen: buttons "Sign in" (top), "Sign in with Google", divider "OR", "Create account". No input field here.
- Intro slides with a "Skip" button come before it. New users use "Create account"; existing users "Sign in". The screens AFTER these two buttons have not been seen yet — their locators are still docs-draft.
- The app's text is Sentence case ("Sign in", "Create account") and "OR" upper case; all locator matching is case-insensitive and button matches are exact (`btnx:`) so "Sign in" never hits "Sign in with Google".

## Known product defects (found by runs)
- 2026-10-03 AUTH-005: Google sign-in ends on Google's "Access blocked: Authorization Error / Custom scheme URIs are not allowed for 'WEB' client type / Error 400: invalid_request". OAuth client misconfigured (confirmed by owner). Scenario stays in the suite and is reported as FAILED (product-defect) until fixed.

## More real screens seen on device (2026-10-03)
- Create Account: header "Create Account", "Step 1", tabs Email | Mobile (opens on Mobile), field labelled MOBILE NUMBER with country flag, Continue (disabled until valid; reports clickable=false, enabled=false).
- Disabled Continue is detected by the runner and reported as "element-disabled" (an earlier input is empty/invalid) instead of a vague "not found".
- Email scenarios must tap the Email tab first (`choose_identifier_tab`).
- Cascade rule: AUTH-006/007/008 depend on AUTH-004's registered user; if AUTH-004 fails they report BLOCKED, not FAILED.

## Terms & Conditions (owner decision 2026-10-03)
After the OTP is entered the runner ticks the icon-only "I accept ..." checkbox directly and confirms it is ticked (pixel check - the hierarchy does not expose the state). The Terms / Privacy links are NOT clicked and no Terms-reading scenario exists.

## Smart form filling (`alumnye_qa/formfill.py`)
After "Verify & join" the runner does not need a script per screen: it reads the inputs (hint / label above / input type), maps them by name (first name, last name, email, phone, company, city, ...) to valid test values, leaves pre-filled and auto-generated fields alone, skips optional screens (Skip / Maybe later), taps the forward button, and loops until Home. A disabled forward button is reported with the visible hints. Unknown fields get a neutral value. No AI on the normal path. Dropdown / date-picker / photo fields are not handled yet and will surface as a clear failure when first met.

## Locator lesson
The checkbox locator must be unambiguous: Appium's XPath engine returns the FIRST match in document order, not the nearest sibling, so a bare preceding-sibling lookup hit OTP box 1. It is now restricted to android.view.ViewGroup.

## Smart entry navigation
`app.reach_landing()` walks Splash -> intro slides by tapping pass-through buttons (Skip, Get Started, Next, Allow...). `reach_sign_in()` / `reach_create_account()` then tap the landing choice that the scenario needs (existing vs new user). The path is printed and added to the triage report.

## Decisions
- 2026-10-02 — Release under test is v1.4; v1.5 login redesign excluded. Source: owner decision 2026-10-01.
- 2026-10-02 — Test data: yopmail emails, OTP typed by tester at CLI prompt, Google account pre-signed-in on device.
- 2026-10-02 — Scenarios that create state (AUTH-004) feed later ones via `data/test_users.json`; later ones report BLOCKED (not failed) if it is empty.
- 2026-10-02 — Error wording is unspecified in docs; negative checks assert "blocked + some error shown", not exact text.

## Resolved by owner (2026-10-03)
- "Sign in with Apple" is NOT shown on Android (iOS only).
- OTP timer is ~2 minutes (AUTH-015 waits up to 150 s).
- Entry path: app opens on Splash, then screens before Sign In are not documented — the runner discovers the path itself (see "Smart entry navigation") and reports it.

## Open questions (flag, don't guess)
- Exact wording of error messages — logged in `message-catalog.md` from real runs for the team to review against expectations.

## Logged UI adaptations (relocated/relabeled elements)
- (none yet — runs append to locator-maps/Auth-Elements.md "Adaptation log")

- 2026-10-03 — Mobile-number scenarios are out of scope for now; email scenarios only. AUTH-003 is marked SKIPPED (META skip) and reports as SKIPPED, not failed. Remove the `skip=` line in its script to re-enable.

## Auto-recovery of disabled buttons (2026-10-03)
A required button that is on screen but disabled is no longer a dead end: the runner ticks an unticked consent checkbox, fills empty required fields, then asks Qwen (bounded). Negative scenarios use `unblock=False` / `is_disabled()` so a disabled guard is still verified rather than "fixed".

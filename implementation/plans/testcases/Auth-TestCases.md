# Auth — Test Cases (BF1: Sign-up, Sign-in & Onboarding)

**Release under test:** Alumnye v1.4 (includes v1.3, v1.3.2). v1.5 login redesign is OUT of scope.
**Criticality: CRITICAL** — identity gate; every other module depends on it.
**Sources:** FSD Member §3, FRD FR-UM-04/07/09/15/16, Walkthrough v1.3 §6, Release v1.3.2 §1, Quick Start Guide v1.2.
**Platforms:** Android + iOS (AUTH-005 Google is Android-only; Apple button exists on iOS only — confirmed by owner).
**Test data:** yopmail emails + valid names; OTP typed by the tester at the CLI prompt; Google account pre-signed-in on the device.
**Run order matters:** AUTH-004 registers a user that AUTH-006/007/008 reuse (`data/test_users.json`).

> **Draft notice:** steps are grounded in the requirement docs only. Locators are cached in `locator-maps/Auth-Elements.md` as *docs-draft* and will be verified/healed on first run.

### TC-AUTH-001 — Fresh launch routes from Splash to the landing screen
- Priority: High
- Type: Positive
- Preconditions: App installed; app data cleared (no stored session).
- Test Data: none
- Steps:
  1. Launch the app.
  2. Wait for Splash to finish.
- Expected Result: Landing screen is shown with three options — "Sign in", "Sign in with Google", "Create account" (seen on device); Home is not shown.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_001_splash_routes_to_sign_in.py
- Notes: Walkthrough §6.1 auto-route. Any intro slides (Skip / Next) on the way are passed through and reported.

### TC-AUTH-002 — Landing layout: Sign in above Google, divider reads "or" (v1.3.2)
- Priority: Medium
- Type: Positive
- Preconditions: Fresh launch, landing screen visible.
- Test Data: none
- Steps:
  1. Locate the Sign In button, the divider label and "Sign in with Google" (and "Sign in with Apple" on iOS).
  2. Compare their vertical positions.
- Expected Result: Sign In button is ABOVE the social options; divider label is exactly "or" (not "or use email") and sits between them.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_002_sign_in_screen_layout_v132.py
- Notes: Release 1.3.2 §1. Strict check — no self-heal, because a changed label is the defect. Owner confirmed: no Apple button on Android; Apple asserted on iOS only. OBSERVATION: the app shows the divider as "OR" (upper case) while v1.3.2 says "or" — matching is case-insensitive; confirm with the owner whether upper case is intended styling.

### TC-AUTH-003 — New user registers with mobile number + SMS OTP  *(SKIPPED for now — email scenarios only)*
- Priority: High
- Type: Positive
- Preconditions: Fresh launch; mobile number able to receive SMS (entered at prompt or `ALUMNYE_TEST_MOBILE`).
- Test Data: valid 10-digit mobile; generated valid first/last name.
- Steps:
  1. Enter the mobile number on Sign In and submit.
  2. On Verify screen, accept Terms & Conditions.
  3. Enter the OTP (tester types it at the CLI prompt) and Verify.
  4. On Complete Profile, enter first and last name; Save & Finish.
- Expected Result: Home is reached; user is registered.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_003_register_with_mobile_otp.py
- Notes: FR-UM-09 (mobile primary identifier), FR-UM-16 (consent at first login). Depends on Karix SMS delivery — failures may be vendor-side (DR-020).

### TC-AUTH-004 — New user registers with yopmail email + OTP
- Priority: High
- Type: Positive
- Preconditions: Fresh launch.
- Test Data: `<first>.<last>.<timestamp>@yopmail.com`; generated valid names.
- Steps:
  1. Landing -> Create account -> switch to the Email tab (the screen opens on Mobile) -> enter the yopmail address -> Continue.
  2. Read the OTP from the yopmail inbox (URL printed by the CLI) and type it at the prompt.
  3. Terms & Conditions: tick the "I accept the Terms & Conditions and Privacy Policy" checkbox and confirm it is ticked (the Terms / Privacy links are not used).
  4. Confirm "Verify & join Alumnye" is enabled; tap it.
  5. Profile screen (step 3 of 3: First name*, Last name*, Member ID auto, Mobile number*, Email pre-filled, Continue) and any that follow: the runner reads each screen, works out what every field is, fills valid test values (names, company, city, etc.; pre-filled and auto-generated fields such as member code are left alone), skips optional screens such as nominee, taps Save & Finish / Continue / Next, and repeats until Home. What it filled is listed in the triage report.
- Expected Result: Home is reached; the user is saved to `data/test_users.json` for later scenarios.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_004_register_with_email_otp.py
- Notes: FR-UM-15 (email login for overseas members). FR-UM-16 / DR-088 for Terms. Soft checks: a failed check is recorded and the run continues, so every problem on the flow is reported together. Seen on device: Create Account screen, "Step 1", Email | Mobile tabs, Continue is disabled until the entry is valid.

### TC-AUTH-005 — Sign in with Google using the account already on the device
- Priority: High
- Type: Positive
- Preconditions: Fresh launch; Google account already added on the Android emulator.
- Test Data: device Google account.
- Steps:
  1. Tap "Sign in with Google".
  2. If the account chooser appears, pick the first account.
  3. If Complete Profile appears (new account), fill generated names and save.
- Expected Result: Home is reached.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_005_google_sign_in.py
- Notes: **KNOWN PRODUCT DEFECT (owner confirmed 2026-10-03): Google OAuth is misconfigured.** Run 2026-10-03 showed Google's page "Access blocked: Authorization Error - Custom scheme URIs are not allowed for 'WEB' client type. Error 400: invalid_request". The script reports this as a product-defect failure with that text; it will pass once the OAuth client (client type / redirect URI) is fixed. Android only. Apple sign-in is not scripted (needs a real Apple ID on iOS). v1.5 "mobile blank on Complete Profile" is out of scope.

### TC-AUTH-006 — Returning user signs in with OTP and skips Complete Profile
- Priority: High
- Type: Positive
- Preconditions: A user registered by AUTH-004 exists; app data cleared (signed out).
- Test Data: last registered yopmail user.
- Steps:
  1. Enter the registered email on Sign In; submit.
  2. Enter the OTP at the prompt; Verify.
- Expected Result: Home is reached directly; Complete Profile is not shown again.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_006_returning_user_sign_in.py
- Notes: BLOCKED (not failed) if no registered user exists.

### TC-AUTH-007 — Logged-in session survives an app restart
- Priority: High
- Type: Positive
- Preconditions: User is signed in (script signs in if needed).
- Test Data: last registered user.
- Steps:
  1. Terminate and relaunch the app.
- Expected Result: Splash routes straight to Home; Sign In is not shown.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_007_session_persists_after_restart.py
- Notes: Walkthrough §6.1; no forced auto-logout (MoM 04-Sep decision, sessions persist until sign-out).

### TC-AUTH-008 — Sign out returns to Sign In and ends the session
- Priority: High
- Type: Positive
- Preconditions: User is signed in.
- Test Data: none
- Steps:
  1. Open profile; tap Sign Out (confirm if asked).
  2. Observe screen; terminate and relaunch the app.
- Expected Result: Sign In shown after sign-out and again after relaunch; Home is never shown.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_008_sign_out_returns_to_sign_in.py
- Notes: Walkthrough §7.1 (Sign Out label consistent).

### TC-AUTH-009 — Complete Profile shows live member-code preview
- Priority: Medium
- Type: Positive
- Preconditions: Reached Complete Profile via fresh email registration (registration is not completed).
- Test Data: generated names, e.g. "Meera Iyer".
- Steps:
  1. Reach Complete Profile (identifier, Terms, OTP, Verify).
  2. Type first and last name.
- Expected Result: Preview shows `<FirstInitial><LastInitial><n>` (e.g. `MI1`), no zero-padding.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_009_member_code_live_preview.py
- Notes: FR-UM-07. Initials are user-overridable and duplicate-checked (override not covered here).

### TC-AUTH-010 — Invalid email / mobile format is rejected
- Priority: High
- Type: Negative
- Preconditions: Sign In screen.
- Test Data: `abc@`, `12345`, `no spaces@yopmail.com`.
- Steps:
  1. For each value: type it, tap Sign In.
- Expected Result: Never reaches the OTP screen; user stays on the identifier screen. On device the Continue button stays disabled for an invalid entry (logged as observed behaviour); any message shown is logged.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_010_invalid_identifier_rejected.py
- Notes: Walkthrough §6.2 (format-validated). Exact error text is unspecified — blocking is asserted and every message shown is LOGGED to `message-catalog.md` for wording review.

### TC-AUTH-011 — Incorrect OTP shows an error and does not sign in
- Priority: High
- Type: Negative
- Preconditions: On the OTP screen for a new yopmail user.
- Test Data: OTP `000000` (entered by the script — no tester input).
- Steps:
  1. Accept Terms; enter `000000`; tap Verify.
- Expected Result: Error is surfaced; user remains on the OTP screen; no Home, no Complete Profile.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_011_wrong_otp_rejected.py
- Notes: Walkthrough §6.3 "Incorrect OTP surfaced inline". Error wording unspecified, so matched on invalid/incorrect/wrong/expired. (A 000000 OTP could coincidentally be valid — 1 in a million.)

### TC-AUTH-012 — Verify is blocked until Terms & Conditions are accepted
- Priority: High
- Type: Negative
- Preconditions: On the OTP screen for a new yopmail user.
- Test Data: real OTP typed by tester.
- Steps:
  1. Do NOT tick the Terms checkbox.
  2. Enter the real OTP; tap Verify.
- Expected Result: User does not proceed; a prompt to accept Terms is visible.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_012_terms_not_accepted_blocks_verify.py
- Notes: FR-UM-16 / DR-088 mandatory consent. Consumes one OTP.

### TC-AUTH-013 — Complete Profile blocks empty / spaces-only names
- Priority: Medium
- Type: Negative
- Preconditions: On Complete Profile (fresh email user).
- Test Data: empty, then `"   "` in both name fields.
- Steps:
  1. Tap Save & Finish with empty names.
  2. Enter spaces-only names; tap Save & Finish.
- Expected Result: Onboarding does not complete; inline errors; stays on Complete Profile.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_013_blank_name_blocked.py
- Notes: Walkthrough §6.4 validation. Consumes one OTP.

### TC-AUTH-014 — "Wrong number? Go back" returns to the previous step
- Priority: Medium
- Type: Edge
- Preconditions: On the OTP screen.
- Test Data: generated yopmail address.
- Steps:
  1. Tap "Wrong number? Go back".
- Expected Result: Returns to the identifier step; OTP screen closed; no session created.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_014_wrong_number_go_back.py
- Notes: Walkthrough §6.3. MoM 04-Sep (#16) calls this edge case ambiguous (possible 4xx / duplicate account) — flagged; "correct prior screen by context" is v1.5.

### TC-AUTH-015 — OTP can be resent once the timer expires
- Priority: Medium
- Type: Edge
- Preconditions: On the OTP screen.
- Test Data: generated yopmail address.
- Steps:
  1. Wait for the Resend control to appear (OTP timer is ~2 minutes; script waits up to 150 s).
  2. Tap Resend.
- Expected Result: Resend becomes available; tapping it keeps the user on the OTP screen.
- Automation script path: source/mobile/alumnye/specs/auth/AUTH_015_otp_resend_after_expiry.py
- Notes: Timer ~2 min per owner. Slow scenario (up to 2.5 min). Messages shown after Resend are logged in message-catalog.md.

---
### Intro slides (Splash) - first launch, fresh install state. The runner is adaptive: it reads the live screen after the Splash and uses whichever control is offered (Skip / Next / Get Started); no OTP is needed.
**The runner is adaptive:** it looks at the live screen after the Splash and decides: intro slide with which controls (Skip / Next / Get Started), or straight to the landing screen. It never assumes a fixed number of slides.

### TC-AUTH-018 - Skip goes straight to the landing screen
- Priority: High - Type: Positive
- Steps: 1. Launch the app fresh. 2. Wait through the Splash. 3. On the first intro slide tap "Skip".
- Expected: "Skip" is offered; Skip leads directly to the landing screen (Sign in / Sign in with Google / Create account); no slide control remains.
- Script: source/mobile/alumnye/specs/auth/AUTH_018_intro_skip_goes_to_landing.py
- Notes: BLOCKED (not failed) if the app opens directly on the landing screen (no intro on this launch).

### TC-AUTH-019 - Get Started / Next, Next ... lead to the landing screen
- Priority: High - Type: Positive
- Steps: 1. Launch fresh. 2. On every slide press whichever of "Get Started" / "Next" is offered, until the landing screen appears (maximum 10 presses).
- Expected: the sequence of presses ends on the landing screen; every slide shows different content (a button that did nothing would repeat a slide). The sequence actually pressed is written to the report.
- Script: source/mobile/alumnye/specs/auth/AUTH_019_intro_next_until_landing.py

### TC-AUTH-020 - UI and wording of the intro slides and the landing screen (v1.3.2)
- Priority: Medium - Type: Positive
- Steps: 1. Launch fresh. 2. On each slide record the wording and controls and take a screenshot. 3. Reach the landing screen.
- Expected: every slide has wording and at least one control; wording equals the approved wording (first run records it in data/splash-wordings.json for the owner to approve, then set "approved": true); landing: "Sign in" above "Sign in with Google", divider reads "or" (any letter case), the old "or use email" is gone, no Apple option on Android.
- Script: source/mobile/alumnye/specs/auth/AUTH_020_intro_ui_and_wording.py
- Sources: Release 1.3.2 section 1 (button order, divider label). The slide wording itself is not in any document, so the first run's wording becomes the reference after the owner approves it.

### Precondition for every later module (Groups etc.)
A user must be signed in before GRP-001. `flows.precondition_signed_in` reuses the open session or signs in with the registered test user (OTP typed by the tester), registers one if none exists, and writes the route taken into the report ("precondition: signed in as ...").

## Message logging (all negative / edge scenarios)
Messages shown after a failed action (toast, inline error, validation) are captured automatically and written to `implementation/plans/message-catalog.md` with the scenario and trigger, so wording can be reviewed. Scenarios that log: AUTH-010, 011, 012, 013, 015.

---
## Not covered (deliberately) — see coverage-model.md
Apple sign-in on iOS (needs real Apple ID), v1.5 login redesign, biometric, duplicate-account mobile/email rule (undecided), forced-update gate (only exists on pre-1.4 builds).

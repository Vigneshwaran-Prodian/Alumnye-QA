# Triage — run-20261004-234648

alumnye | android | module `journeys`

> **RUN STOPPED:** Stopped by user (Ctrl+C).

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
| ai calls | 5 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | JNY-001 | Positive | Anchor invites, member accepts: the Anchor's Members count goes up and the member's name is listed | qwen | likely-bug: member: 'home_marker' (Home reached: 'Welcome, <name>', bottom nav Home / My Group / My Account, MEMBER / ANCHOR toggle) is missing from the screen — likely functionality break. AI: App is stuck on registration completion screen instead of navigating to home screen; phone number validation error prevents progression to expected home_marker element. / profile screen 3: could not move forward (tried: 'Continue' is disabled (a required field is probably empty or invalid); Qwen could not unblock it; visible hints: none) / anchor: the other device stopped before 'member_ready': member: 'home_marker' (Home reached: 'Welcome, <name>', bottom nav Home / My Group / My Account, MEMBER / ANCHOR toggle) is miss | reports/results/alumnye/run-20261004-234648/JNY-001_anchor_FAILED.png (+ _member_) |

## UI adaptations to confirm (never silent)

- JNY-001: `anchor_home_marker` -> `text:New Group` via heal — label 'New Group' ~ ['New Group', "You don't have any groups"] (score 1.00)
- JNY-001: `group_details_marker` -> `text:MEMBER` via heal — label 'MEMBER' ~ ['Add Event', 'Add Member'] (score 0.81)
- JNY-001: `finish this profile screen (fill every required field marked * with a valid value) and move forward until the Home screen` -> `type 35` via qwen — Mobile number field is empty; entering valid Indian 10-digit number.
- JNY-001: `finish this profile screen (fill every required field marked * with a valid value) and move forward until the Home screen` -> `type 35` via qwen — Current mobile number is already registered; replace with different valid number.
- JNY-001: `finish this profile screen (fill every required field marked * with a valid value) and move forward until the Home screen` -> `type 35` via qwen — Phone number registered to another user; try different number.
- JNY-001: `finish this profile screen (fill every required field marked * with a valid value) and move forward until the Home screen` -> `type 35` via qwen — Phone number is registered to another user; try a different number.

## Entry paths the runner navigated (Splash -> ... -> target)

- JNY-001: Splash -> anchor: dialog 'Success / Group created successfully!' -> OK -> anchor: dialog 'Success / Group created successfully!' -> OK -> member: Skip -> member: Create account -> member: Email tab -> member: Terms checkbox: ticked

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- JNY-001: anchor: role_anchor -> ViewGroup at x857,y186 173x58 | anchor: new_group_button -> ViewGroup at x696,y447 321x99 | anchor: save_group_button -> ViewGroup at x63,y1446 954x116 | member: terms_checkbox -> ViewGroup at x105,y911 53x54 | member: verify_button -> ViewGroup at x53,y1270 975x139 | member: 'Continue' -> ViewGroup at x53,y1664

## Flow variants the runner detected

- JNY-001: anchor: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- JNY-001: anchor: self-heal for 'anchor_home_marker' used text:New Group for this run only (not saved: it also describes 'new_group_button')
- JNY-001: anchor: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- JNY-001: anchor: self-heal for 'group_details_marker' used text:MEMBER for this run only (not saved: it also describes 'role_member')
- JNY-001: member: Profile form filled automatically: screen 1: Enter your first name = Meera; screen 1: Enter your last name = Nair; screen 1: Qwen-assisted (progressed); screen 2: tapped 'Continue'; screen 3: Qwen-assisted (could not progress)

## Messages observed (review wording — also in message-catalog.md)

- JNY-001 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- JNY-001 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- JNY-001 | after: profile screen 2: tapped 'Continue' | "Phone number is already registered to another user" (on-screen)

## Controls found on screen that no document or locator map mentions (review - new features?)

- JNY-001 [anchor] on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- JNY-001 [anchor] on 'group form is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- JNY-001 [anchor] on 'Group Details opens after saving': **, Home** - listed only (could change data) - test manually or add a scenario
- JNY-001 [member] on 'Create account screen asks for the email / mobile': **🇮🇳** - listed only (could change data) - test manually or add a scenario
- JNY-001 [member] on 'OTP verification screen is shown': **Terms & Conditions** - listed only (could change data) - test manually or add a scenario
- JNY-001 [member] on 'OTP verification screen is shown': **Privacy Policy** - listed only (could change data) - test manually or add a scenario

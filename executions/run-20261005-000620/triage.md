# Triage — run-20261005-000620

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
| ai calls | 2 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | JNY-001 | Positive | Anchor invites, member accepts: the Anchor's Members count goes up and the member's name is listed | qwen | likely-bug: anchor: 'group_details_marker' (Group Details is open) is missing from the screen — likely functionality break. AI: The Group Details marker and expected action labels (Add Event, Add Member) are completely absent; instead an error state (Alumnye isn't responding) with recovery buttons is shown, indicating the Group Details screen failed to open. / member: the other device stopped before 'invite_sent': anchor: 'group_details_marker' (Group Details is open) is missing from the screen — likely functionality break. AI: The Group De | reports/results/alumnye/run-20261005-000620/JNY-001_anchor_FAILED.png (+ _member_) |

## UI adaptations to confirm (never silent)

- JNY-001: `finish this profile screen (fill every required field marked * with a valid value) and move forward until the Home screen` -> `type 35` via qwen — Mobile number field is empty; filling with valid 10-digit Indian number
- JNY-001: `Enter your mobile number` -> `retyped Enter your mobile number` via validation — Phone number is already registered to another user -> the phone number is already used by someone else, so a different number is needed

## Entry paths the runner navigated (Splash -> ... -> target)

- JNY-001: Splash -> anchor: dialog 'Success / Group created successfully!' -> OK -> anchor: dialog 'Success / Group created successfully!' -> OK -> member: Skip -> member: Create account -> member: Email tab -> member: Terms checkbox: ticked

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- JNY-001: anchor: role_anchor -> ViewGroup at x857,y186 173x58 | anchor: new_group_button -> ViewGroup at x696,y447 321x99 | anchor: save_group_button -> ViewGroup at x63,y1446 954x116 | member: verify_button -> ViewGroup at x53,y1270 975x139 | member: 'Continue' -> ViewGroup at x53,y1664 | member: 'Continue' -> ViewGroup at x53,y1664

## Flow variants the runner detected

- JNY-001: anchor: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- JNY-001: anchor: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- JNY-001: member: form filler: field 'Enter your last name' was not on the screen on attempt 1
- JNY-001: member: form filler: field 'Enter your mobile number' was not on the screen on attempt 1
- JNY-001: member: form filler: field 'Enter your mobile number' was not on the screen on attempt 2
- JNY-001: member: validation 'Phone number is already registered to another user' on 'Enter your mobile number': the phone number is already used by someone else, so a different number is needed; entered a new value 9597024921 (known rule)
- JNY-001: member: Profile form filled automatically: screen 1: Enter your first name = Rohan; screen 1: Enter your last name = Pillai; screen 1: Qwen-assisted (progressed); screen 2: tapped 'Continue'; validation 'Phone number is already registered to another user' -> new Enter your mobile number 9597024921 (known rule); screen 3: tapped 'Continue' after correcting a rejected value
- JNY-001: member account registered: rohan.pillai.1005000700@yopmail.com

## Messages observed (review wording — also in message-catalog.md)

- JNY-001 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- JNY-001 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- JNY-001 | after: profile screen 2: tapped 'Continue' | "Phone number is already registered to another user" (on-screen)

## Controls found on screen that no document or locator map mentions (review - new features?)

- JNY-001 [anchor] on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- JNY-001 [anchor] on 'group form is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- JNY-001 [member] on 'Create account screen asks for the email / mobile': **🇮🇳** - listed only (could change data) - test manually or add a scenario
- JNY-001 [member] on 'OTP verification screen is shown': **Terms & Conditions** - listed only (could change data) - test manually or add a scenario
- JNY-001 [member] on 'OTP verification screen is shown': **Privacy Policy** - listed only (could change data) - test manually or add a scenario
- JNY-001 [member] on 'Home screen after registration': **Set Preferences →** - listed only (could change data) - test manually or add a scenario
- JNY-001 [member] on 'Home screen after registration': **, Home** - listed only (could change data) - test manually or add a scenario

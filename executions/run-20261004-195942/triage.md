# Triage — run-20261004-195942

alumnye | android | module `groups`

> **RUN STOPPED:** Stopped by user (Ctrl+C).

| Metric | Count |
|---|---|
| total | 7 |
| passed | 5 |
| passed zero ai | 5 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 1 |
| error | 1 |
| blocked | 0 |
| skipped | 0 |
| ai calls | 3 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | GRP-005 | Positive | Anchor invites a member by email and gets a success confirmation | qwen | likely-bug: 'invite_email_field' (Invite: email entry) is missing from the screen — likely functionality break. AI: No email input field is visible on the screen; all listed elements are ViewGroups, TextViews, or Buttons with no input field matching 'invite_email_field'. | reports/results/alumnye/run-20261004-195942/GRP-005_FAILED.png |
| ERROR | GRP-007 | Negative | Anchor cannot invite their own email address | none | driver: Message: Cached elements 'By.xpath: //*[contains(translate(normalize-space(@text),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'qa group 1004195958') or contains(translate(normalize-space(@content-desc),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'qa group 1004195958')]' do not exist in DOM anymore; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#staleelementreferenceexception | reports/results/alumnye/run-20261004-195942/GRP-007_ERROR.png |
| PASSED | GRP-001 | Positive | Anchor creates a group and lands on its Group Details | none |  | reports/results/alumnye/run-20261004-195942/GRP-001_PASSED.png |
| PASSED | GRP-002 | Positive | Anchor Home offers + New Group and shows the right state (welcome message or the group list) | none |  | reports/results/alumnye/run-20261004-195942/GRP-002_PASSED.png |
| PASSED | GRP-003 | Positive | Group Details shows the group, Add Member / Add Event, the Members count tab, Events tab and Notice Board | none |  | reports/results/alumnye/run-20261004-195942/GRP-003_PASSED.png |
| PASSED | GRP-004 | Positive | Add Members shows the four invitation tabs and the Invite form (email OR mobile, Send Invitation) | none |  | reports/results/alumnye/run-20261004-195942/GRP-004_PASSED.png |
| PASSED | GRP-006 | Negative | Invite rejects an invalid email format with 'Please enter a valid email format' | none |  | reports/results/alumnye/run-20261004-195942/GRP-006_PASSED.png |

## UI adaptations to confirm (never silent)

- GRP-005: `something (a dialog, pop-up or overlay) may be covering the screen; clear it so that 'Invite: email entry' becomes reachable` -> `back` via qwen — Close potential modal dialog covering the Invite email entry field.
- GRP-005: `something (a dialog, pop-up or overlay) may be covering the screen; clear it so that 'Invite: email entry' becomes reachable` -> `tap 25` via qwen — Switch from MEMBER to ANCHOR tab; invite likely accessible there.

## Entry paths the runner navigated (Splash -> ... -> target)

- GRP-001: Splash -> dialog 'Success / Group created successfully!' -> OK

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- GRP-005: role_anchor -> ViewGroup at x857,y186 173x58 | add_member_entry -> ViewGroup at x540,y800 540x130
- GRP-007: nav_profile -> Button at x720,y2189 360x149 | role_anchor -> ViewGroup at x857,y186 173x58

## Flow variants the runner detected

- GRP-002: user already has groups: group list shown (the empty state applies only to a user with no groups)
- GRP-003: Members tab: 'Members, 1' (count 1); the docs' 'About' section does not exist in v1.4.0
- GRP-004: tabs seen: Invite | Upload | Add Members | 'Add Contact' (singular; the release note says 'Add Contacts')
- GRP-007: signed-in user: vivek.reddy.1004001541@yopmail.com

## Messages observed (review wording — also in message-catalog.md)

- GRP-001 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- GRP-006 | after: sent invitation to 'abc@' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to 'plainaddress' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to 'no spaces@yopmail.com' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to 'a@b' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to '@yopmail.com' | "Please enter a valid email format" (on-screen)

## Where the time went (seconds / calls; the rest is waiting, typing and sleeps)

| Scenario | Total s | element lookups | page reads | adb |
|---|---|---|---|---|
| GRP-005 | 120.3 | 17.5 (46) | 2.4 (7) | 0.8 (5) |
| GRP-006 | 70.4 | 12.5 (28) | 14.7 (29) | 8.2 (32) |
| GRP-001 | 54.8 | 28.9 (109) | 2.8 (7) | 4.9 (12) |
| GRP-004 | 17.8 | 9.8 (18) | 1.2 (5) | 0.4 (3) |
| GRP-003 | 11.9 | 6.0 (14) | 3.3 (7) | 0.1 (1) |
| GRP-007 | 10.7 | 4.9 (11) | 0.7 (2) | 0.4 (2) |
| GRP-002 | 9.5 | 4.8 (12) | 1.2 (2) | 0.2 (1) |

## Controls found on screen that no document or locator map mentions (review - new features?)

- GRP-001 on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'group form is shown': **Cancel** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'group form is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'Group Details opens after saving': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-003 on 'Group Details is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-004 on 'Add Members screen': **, Home** - listed only (could change data) - test manually or add a scenario

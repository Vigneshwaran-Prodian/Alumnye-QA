# Triage — run-20261004-200934

alumnye | android | module `groups`

> **RUN STOPPED:** Stopped by user (Ctrl+C).

| Metric | Count |
|---|---|
| total | 14 |
| passed | 10 |
| passed zero ai | 8 |
| passed after self heal | 2 |
| passed after qwen | 0 |
| failed | 3 |
| error | 1 |
| blocked | 0 |
| skipped | 0 |
| ai calls | 2 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | GRP-012 | Positive | Download the template, upload the 200-member sheet, Bulk Preview, import | self-heal | likely-bug: 'confirm_import' (Bulk Preview: confirm import (not the 'Add Members' tab)) is missing from the screen — likely functionality break. AI: No visible element contains 'Confirm' or 'Import' labels; the confirm_import button is absent from this screen. | reports/results/alumnye/run-20261004-200934/GRP-012_FAILED.png |
| FAILED | GRP-013 | Negative | Bulk upload flags invalid rows with validation errors | self-heal | assertion: could not select 'members_invalid.csv' in the device file picker / invalid rows must be reported with a validation error | reports/results/alumnye/run-20261004-200934/GRP-013_FAILED.png |
| FAILED | GRP-014 | Positive | Member count opens the cohort members list showing the Anchor with their member code | none | likely-bug: 'landing_sign_in' (Landing screen: 'Sign in' (existing user)) is missing from the screen — likely functionality break. AI: The expected 'Sign in' button for a landing screen is absent; the visible screen shows a logged-in group management interface (QA Group, Invite, Upload, Add Members actions) rather than the expected landing/login screen with Sign in, Google, and Create account options. | reports/results/alumnye/run-20261004-200934/GRP-014_FAILED.png |
| ERROR | GRP-011 | Edge | Group description is limited to 200 characters with a live counter | none | driver: Message: Cached elements 'By.xpath: //*[@clickable='true'][contains(translate(normalize-space(@content-desc),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'new group') or .//*[contains(translate(normalize-space(@text),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'new group')] or contains(translate(normalize-space(@text),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'new group')]' do not exist in DOM anymore; For documentation on this error, please visit: https://www.selenium.dev/documentation/webdriver/troubleshooting/errors#staleelementreferenceexception | reports/results/alumnye/run-20261004-200934/GRP-011_ERROR.png |
| PASSED | GRP-001 | Positive | Anchor creates a group and lands on its Group Details | self-heal |  | reports/results/alumnye/run-20261004-200934/GRP-001_PASSED.png |
| PASSED | GRP-002 | Positive | Anchor Home offers + New Group and shows the right state (welcome message or the group list) | none |  | reports/results/alumnye/run-20261004-200934/GRP-002_PASSED.png |
| PASSED | GRP-003 | Positive | Group Details shows the group, Add Member / Add Event, the Members count tab, Events tab and Notice Board | none |  | reports/results/alumnye/run-20261004-200934/GRP-003_PASSED.png |
| PASSED | GRP-004 | Positive | Add Members shows the four invitation tabs and the Invite form (email OR mobile, Send Invitation) | none |  | reports/results/alumnye/run-20261004-200934/GRP-004_PASSED.png |
| PASSED | GRP-005 | Positive | Anchor invites a member by email and gets a success confirmation | none |  | reports/results/alumnye/run-20261004-200934/GRP-005_PASSED.png |
| PASSED | GRP-006 | Negative | Invite rejects an invalid email format with 'Please enter a valid email format' | none |  | reports/results/alumnye/run-20261004-200934/GRP-006_PASSED.png |
| PASSED | GRP-007 | Negative | Anchor cannot invite their own email address | none |  | reports/results/alumnye/run-20261004-200934/GRP-007_PASSED.png |
| PASSED | GRP-008 | Negative | Inviting the same email twice is blocked | none |  | reports/results/alumnye/run-20261004-200934/GRP-008_PASSED.png |
| PASSED | GRP-009 | Negative | Create Group is blocked when the name is empty | none |  | reports/results/alumnye/run-20261004-200934/GRP-009_PASSED.png |
| PASSED | GRP-010 | Negative | A duplicate group name is rejected with the full message | self-heal |  | reports/results/alumnye/run-20261004-200934/GRP-010_PASSED.png |

## UI adaptations to confirm (never silent)

- GRP-001: `group_details_marker` -> `text:MEMBER` via heal — label 'MEMBER' ~ ['Add Event', 'Add Member'] (score 0.81)
- GRP-010: `group_details_marker` -> `text:MEMBER` via heal — label 'MEMBER' ~ ['Add Event', 'Add Member'] (score 0.81)
- GRP-012: `choose_file_button` -> `btnx:Upload` via heal — label 'Upload' ~ ['Choose File', 'Select File', 'Upload File', 'Browse'] (score 0.79)
- GRP-013: `choose_file_button` -> `btnx:Upload` via heal — label 'Upload' ~ ['Choose File', 'Select File', 'Upload File', 'Browse'] (score 0.79)

## Entry paths the runner navigated (Splash -> ... -> target)

- GRP-001: Splash -> dialog 'Success / Group created successfully!' -> OK
- GRP-010: Splash -> dialog 'Success / Group created successfully!' -> OK

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- GRP-011: role_anchor -> ViewGroup at x857,y186 173x58
- GRP-012: add_member_entry -> ViewGroup at x53,y648 479x97 | tab_upload -> ViewGroup at x270,y474 270x111 | download_template -> ViewGroup at x97,y766 886x172 | choose_file_button -> ViewGroup at x270,y474 270x111
- GRP-013: role_anchor -> ViewGroup at x857,y186 173x58 | add_member_entry -> ViewGroup at x53,y648 479x97 | tab_upload -> ViewGroup at x270,y474 270x111 | choose_file_button -> ViewGroup at x270,y474 270x111

## Flow variants the runner detected

- GRP-001: self-heal for 'group_details_marker' used text:MEMBER for this run only (not saved: it also describes 'role_member')
- GRP-002: user already has groups: group list shown (the empty state applies only to a user with no groups)
- GRP-003: Members tab: 'Members, 1' (count 1); the docs' 'About' section does not exist in v1.4.0
- GRP-004: tabs seen: Invite | Upload | Add Members | 'Add Contact' (singular; the release note says 'Add Contacts')
- GRP-005: invited meera.nair.1004201045@yopmail.com; pending invites before: 
- GRP-007: signed-in user: vivek.reddy.1004001541@yopmail.com
- GRP-010: self-heal for 'group_details_marker' used text:MEMBER for this run only (not saved: it also describes 'role_member')
- GRP-012: the app was left for 'com.android.chrome' (after 'Download template'); the runner brought Alumnye back to the front
- GRP-012: template download: no new file seen (the app was left and recovered)
- GRP-012: sample sheet for upload: C:\Projects\Alumnye QA\source\mobile\alumnye\data\members_200.xlsx (200 members, qa.member001..200@yopmail.com)
- GRP-012: self-heal for 'choose_file_button' used btnx:Upload for this run only (not saved: it also describes 'tab_upload')
- GRP-012: the app was left for 'com.android.chrome' (looking for 'confirm_import'); the runner brought Alumnye back to the front
- GRP-013: self-heal for 'choose_file_button' used btnx:Upload for this run only (not saved: it also describes 'tab_upload')
- GRP-014: the app was left for 'com.android.chrome' (looking for 'landing_sign_in'); the runner brought Alumnye back to the front

## Messages observed (review wording — also in message-catalog.md)

- GRP-001 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- GRP-005 | after: sent invitation to 'meera.nair.1004201045@yopmail.com' | "Enter email address..." (on-screen)
- GRP-005 | after: sent invitation to 'meera.nair.1004201045@yopmail.com' | "Invite sent successfully!" (on-screen)
- GRP-006 | after: sent invitation to 'abc@' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to 'plainaddress' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to 'no spaces@yopmail.com' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to 'a@b' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to '@yopmail.com' | "Please enter a valid email format" (on-screen)
- GRP-007 | after: sent invitation to 'vivek.reddy.1004001541@yopmail.com' | "You are already an anchor" (on-screen)
- GRP-008 | after: sent invitation to 'divya.kapoor.1004201216@yopmail.com' | "Enter email address..." (on-screen)
- GRP-008 | after: sent invitation to 'divya.kapoor.1004201216@yopmail.com' | "Invite sent successfully!" (on-screen)
- GRP-008 | after: sent invitation to 'divya.kapoor.1004201216@yopmail.com' | "0.0" (on-screen)
- GRP-008 | after: sent invitation to 'divya.kapoor.1004201216@yopmail.com' | "User already invited to this group" (on-screen)
- GRP-009 | after: tried to save a group with an empty name | "(button stays disabled)" (state)
- GRP-009 | after: tried to save a group with a spaces-only name | "(button stays disabled)" (state)
- GRP-010 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- GRP-010 | after: tried to create a second group with an existing name | "A group with this name already exists. Please choose a different name." (on-screen)

## Where the time went (seconds / calls; the rest is waiting, typing and sleeps)

| Scenario | Total s | element lookups | page reads | adb |
|---|---|---|---|---|
| GRP-012 | 127.8 | 41.6 (325) | 1.3 (22) | 7.1 (33) |
| GRP-014 | 86.8 | 17.8 (293) | 1.3 (40) | 0.7 (3) |
| GRP-013 | 67.1 | 32.0 (141) | 1.8 (38) | 2.9 (12) |
| GRP-010 | 53.3 | 21.8 (121) | 4.2 (18) | 5.2 (19) |
| GRP-006 | 51.7 | 8.9 (34) | 10.6 (32) | 5.6 (32) |
| GRP-001 | 37.9 | 18.2 (81) | 2.8 (16) | 2.3 (12) |
| GRP-008 | 28.3 | 6.5 (21) | 5.1 (14) | 1.9 (14) |
| GRP-007 | 21.4 | 6.1 (21) | 3.2 (8) | 1.1 (9) |
| GRP-005 | 18.2 | 4.7 (19) | 2.5 (9) | 1.9 (8) |
| GRP-009 | 18.0 | 7.0 (43) | 0.7 (6) | 2.6 (7) |
| GRP-004 | 11.2 | 5.3 (21) | 0.8 (5) | 0.2 (3) |
| GRP-003 | 7.1 | 3.7 (18) | 1.0 (8) | 0.1 (1) |
| GRP-011 | 6.8 | 3.1 (11) | 0.2 (1) | 0.2 (2) |
| GRP-002 | 4.9 | 2.6 (16) | 0.2 (2) | 0.1 (1) |

## Controls found on screen that no document or locator map mentions (review - new features?)

- GRP-001 on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'group form is shown': **Cancel** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'group form is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'Group Details opens after saving': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-003 on 'Group Details is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-004 on 'Add Members screen': **, Home** - listed only (could change data) - test manually or add a scenario

# Triage — run-20261004-231812

alumnye | android | module `groups`

| Metric | Count |
|---|---|
| total | 15 |
| passed | 12 |
| passed zero ai | 10 |
| passed after self heal | 2 |
| passed after qwen | 0 |
| failed | 3 |
| error | 0 |
| blocked | 0 |
| skipped | 0 |
| ai calls | 0 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | GRP-012 | Positive | Bulk upload: valid .xlsx and .csv files (new data each run, picked from local storage) reach the preview, are confirmed and imported | self-heal | assertion: 'Member Template Download' must save a template file to the device Downloads folder / valid_200_members_1004232627.xlsx: the app must confirm the import (shown: nothing) | reports/results/alumnye/run-20261004-231812/GRP-012_FAILED.png |
| FAILED | GRP-013 | Negative | Bulk upload flags invalid files and rows (new data each run): bad e-mail, missing data, duplicates, wrong columns, empty, wrong format | none | assertion: missing_first_name_1004232808.csv (a row without a first name) must be flagged with a validation message in the preview or at the top of the app (shown: (nothing flagged)) / duplicate_emails_1004232808.csv (the same e-mail twice in one file) must be flagged with a validation message in the preview or at the top of the app (shown: (nothing flagged)) / wrong_columns_1004232808.csv (columns that do not match the template) must be flagged with a validation message in the preview or at the top of the app (shown: (nothing flagged)) | reports/results/alumnye/run-20261004-231812/GRP-013_FAILED.png |
| FAILED | GRP-015 | Positive | Pending Acceptance members each have a Remind button; accepted members do not | none | assertion: the 'PENDING ACCEPTANCE' section must list the invitees who have not accepted (run GRP-005 / GRP-012 first) | reports/results/alumnye/run-20261004-231812/GRP-015_FAILED.png |
| PASSED | GRP-001 | Positive | Anchor creates a group and lands on its Group Details | self-heal |  | reports/results/alumnye/run-20261004-231812/GRP-001_PASSED.png |
| PASSED | GRP-002 | Positive | Anchor Home offers + New Group and shows the right state (welcome message or the group list) | none |  | reports/results/alumnye/run-20261004-231812/GRP-002_PASSED.png |
| PASSED | GRP-003 | Positive | Group Details shows the group, Add Member / Add Event, the Members count tab, Events tab and Notice Board | none |  | reports/results/alumnye/run-20261004-231812/GRP-003_PASSED.png |
| PASSED | GRP-004 | Positive | Add Members shows the four invitation tabs and the Invite form (email OR mobile, Send Invitation) | none |  | reports/results/alumnye/run-20261004-231812/GRP-004_PASSED.png |
| PASSED | GRP-005 | Positive | Anchor invites a member by email and gets a success confirmation | none |  | reports/results/alumnye/run-20261004-231812/GRP-005_PASSED.png |
| PASSED | GRP-006 | Negative | Invite rejects an invalid email format with 'Please enter a valid email format' | none |  | reports/results/alumnye/run-20261004-231812/GRP-006_PASSED.png |
| PASSED | GRP-007 | Negative | Anchor cannot invite their own email address | none |  | reports/results/alumnye/run-20261004-231812/GRP-007_PASSED.png |
| PASSED | GRP-008 | Negative | Inviting the same email twice is blocked | none |  | reports/results/alumnye/run-20261004-231812/GRP-008_PASSED.png |
| PASSED | GRP-009 | Negative | Create Group is blocked when the name is empty | none |  | reports/results/alumnye/run-20261004-231812/GRP-009_PASSED.png |
| PASSED | GRP-010 | Negative | A duplicate group name is rejected with the full message | self-heal |  | reports/results/alumnye/run-20261004-231812/GRP-010_PASSED.png |
| PASSED | GRP-011 | Edge | Group description is limited to 200 characters with a live counter | none |  | reports/results/alumnye/run-20261004-231812/GRP-011_PASSED.png |
| PASSED | GRP-014 | Positive | Members tab: the count equals the accepted-members name list; invitees sit under Pending Acceptance, not in the count | none |  | reports/results/alumnye/run-20261004-231812/GRP-014_PASSED.png |

## UI adaptations to confirm (never silent)

- GRP-001: `group_details_marker` -> `text:MEMBER` via heal — label 'MEMBER' ~ ['Add Event', 'Add Member'] (score 0.81)
- GRP-010: `group_details_marker` -> `text:MEMBER` via heal — label 'MEMBER' ~ ['Add Event', 'Add Member'] (score 0.81)
- GRP-012: `group_details_marker` -> `text:MEMBER` via heal — label 'MEMBER' ~ ['Add Event', 'Add Member'] (score 0.81)

## Entry paths the runner navigated (Splash -> ... -> target)

- GRP-001: Splash -> Sign in -> Email tab -> Terms checkbox: ticked -> dialog 'Success / Group created successfully!' -> OK
- GRP-010: Splash -> dialog 'Success / Group created successfully!' -> OK
- GRP-012: Splash -> dialog 'Success / Group created successfully!' -> OK

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- GRP-012: choose_file_button -> ViewGroup at x97,y1117 886x420 | confirm_import -> ViewGroup at x475,y1733 491x126 | choose_file_button -> ViewGroup at x97,y1117 886x420 | confirm_import -> ViewGroup at x475,y1475 491x126
- GRP-013: confirm_import -> ViewGroup at x475,y1647 491x126 | choose_file_button -> ViewGroup at x97,y1117 886x420 | choose_file_button -> ViewGroup at x97,y1117 886x420 | choose_file_button -> ViewGroup at x97,y1117 886x420
- GRP-015: role_anchor -> ViewGroup at x857,y186 173x58 | members_tab -> ViewGroup at x540,y800 540x130

## Flow variants the runner detected

- GRP-001: precondition: signed in as arjun.sharma.1004223213@yopmail.com (signed in by the runner before the scenario)
- GRP-001: self-heal for 'group_details_marker' used text:MEMBER for this run only (not saved: it also describes 'role_member')
- GRP-002: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-002: user already has groups: group list shown (the empty state applies only to a user with no groups)
- GRP-003: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-003: Members tab: 'Members, 1' (count 1); the docs' 'About' section does not exist in v1.4.0
- GRP-004: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-004: tabs seen: Invite | Upload | Add Members | 'Add Contact' (singular; the release note says 'Add Contacts')
- GRP-005: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-005: invited karthik.iyer.1004232044@yopmail.com; pending invites before: 
- GRP-006: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-007: signed-in user: arjun.sharma.1004223213@yopmail.com
- GRP-007: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-008: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-009: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-010: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-010: self-heal for 'group_details_marker' used text:MEMBER for this run only (not saved: it also describes 'role_member')
- GRP-010: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-011: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-012: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-012: self-heal for 'group_details_marker' used text:MEMBER for this run only (not saved: it also describes 'role_member')
- GRP-012: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-012: the app was left for 'com.android.chrome' (after 'Member Template Download'); the runner brought Alumnye back to the front
- GRP-012: template download: no fresh file (the app was left for the browser and recovered)
- GRP-012: valid_200_members_1004232627.xlsx (template format (.xlsx), 200 valid members): preview=True errors=none
- GRP-012: valid_5_members_1004232627.csv (.csv format, 5 valid members): preview=True errors=none
- GRP-012: valid_email_or_phone_only_1004232627.csv (one row with only an e-mail and one with only a phone (either is enough)): preview=True errors=none
- GRP-013: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-013: invalid_email_format_1004232808.xlsx (rows with malformed e-mail addresses): preview=True confirmed=True flagged: Validation Errors (2): / Invalid email format "not-an-email" / Invalid email format "abc@"
- GRP-013: missing_first_name_1004232808.csv (a row without a first name): preview=True confirmed=True flagged: (nothing flagged)
- GRP-013: missing_email_and_phone_1004232808.csv (a row with neither e-mail nor phone (the app requires at least one)): preview=True confirmed=True flagged: Validation Errors (1): / At least one of Email or Phone is required
- GRP-013: bad_phone_number_1004232808.csv (a row with a malformed phone number): preview=True confirmed=True flagged: Validation Errors (1): / Invalid phone number "12ab"
- GRP-013: duplicate_emails_1004232808.csv (the same e-mail twice in one file): preview=True confirmed=True flagged: (nothing flagged)
- GRP-013: the picker stayed open after choosing 'wrong_columns_1004232808.csv'
- GRP-013: file picker: switched from Google Drive to the device's Downloads (local storage) for 'wrong_columns_1004232808.csv'
- GRP-013: wrong_columns_1004232808.csv (columns that do not match the template): preview=False confirmed=False flagged: (nothing flagged)
- GRP-013: the app was left for 'com.google.android.documentsui' (after an upload); the runner brought Alumnye back to the front
- GRP-013: headers_only_empty_1004232808.csv (a file with headers and no members): preview=False confirmed=False flagged: No records found in spreadsheet.
- GRP-013: the app was left for 'com.google.android.documentsui' (closing the file picker); the runner brought Alumnye back to the front
- GRP-013: 'unsupported_format_1004232808.txt' could not be chosen in the file picker (the picker does not offer it)
- GRP-013: unsupported_format_1004232808.txt (a .txt file (only .xlsx / .csv are allowed)): the picker does not accept it - rejected at the picker (correct)
- GRP-014: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-014: Members tab count 1; accepted list (1): Arjun Sharma (Anchor); pending rows read: 40
- GRP-015: precondition: signed in as arjun.sharma.1004223213@yopmail.com (session already open)
- GRP-015: pending rows read: 43; accepted members: 
- GRP-015: Remind feedback: Invitation email resent successfully!

## Messages observed (review wording — also in message-catalog.md)

- GRP-001 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- GRP-005 | after: sent invitation to 'karthik.iyer.1004232044@yopmail.com' | "0.0" (on-screen)
- GRP-005 | after: sent invitation to 'karthik.iyer.1004232044@yopmail.com' | "Enter email address..." (on-screen)
- GRP-005 | after: sent invitation to 'karthik.iyer.1004232044@yopmail.com' | "Invite sent successfully!" (on-screen)
- GRP-006 | after: sent invitation to 'abc@' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to 'plainaddress' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to 'no spaces@yopmail.com' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to 'a@b' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to '@yopmail.com' | "Please enter a valid email format" (on-screen)
- GRP-007 | after: sent invitation to 'arjun.sharma.1004223213@yopmail.com' | "You are already an anchor" (on-screen)
- GRP-008 | after: sent invitation to 'arjun.iyer.1004232240@yopmail.com' | "Enter email address..." (on-screen)
- GRP-008 | after: sent invitation to 'arjun.iyer.1004232240@yopmail.com' | "Invite sent successfully!" (on-screen)
- GRP-008 | after: sent invitation to 'arjun.iyer.1004232240@yopmail.com' | "User already invited to this group" (on-screen)
- GRP-009 | after: tried to save a group with an empty name | "(button stays disabled)" (state)
- GRP-009 | after: tried to save a group with a spaces-only name | "(button stays disabled)" (state)
- GRP-010 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- GRP-010 | after: tried to create a second group with an existing name | "0.0" (on-screen)
- GRP-010 | after: tried to create a second group with an existing name | "A group with this name already exists. Please choose a different name." (on-screen)
- GRP-012 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- GRP-012 | after: confirmed the import of valid_5_members_1004232627.csv | "Invite" (banner)
- GRP-012 | after: confirmed the import of valid_5_members_1004232627.csv | "0 members uploaded successfully!, 5 members already in the group." (banner)
- GRP-012 | after: confirmed the import of valid_5_members_1004232627.csv | "0 members uploaded successfully!" (banner)
- GRP-012 | after: confirmed the import of valid_5_members_1004232627.csv | "5 members already in the group." (banner)
- GRP-012 | after: confirmed the import of valid_email_or_phone_only_1004232627.csv | "Invite" (banner)
- GRP-012 | after: confirmed the import of valid_email_or_phone_only_1004232627.csv | "2 members uploaded successfully!" (banner)
- GRP-013 | after: uploaded invalid_email_format_1004232808.xlsx | "Validation Errors (2):" (on-screen)
- GRP-013 | after: uploaded invalid_email_format_1004232808.xlsx | "Invalid email format "not-an-email"" (on-screen)
- GRP-013 | after: uploaded invalid_email_format_1004232808.xlsx | "Invalid email format "abc@"" (on-screen)
- GRP-013 | after: confirmed the import of invalid_email_format_1004232808.xlsx | "Validation Errors (2):" (banner)
- GRP-013 | after: confirmed the import of invalid_email_format_1004232808.xlsx | "Invalid email format "not-an-email"" (banner)
- GRP-013 | after: confirmed the import of invalid_email_format_1004232808.xlsx | "Invalid email format "abc@"" (banner)
- GRP-013 | after: confirmed the import of invalid_email_format_1004232808.xlsx | "Invite" (banner)
- GRP-013 | after: confirmed the import of invalid_email_format_1004232808.xlsx | "2 members uploaded successfully!" (banner)
- GRP-013 | after: confirmed the import of missing_first_name_1004232808.csv | "Invite" (banner)
- GRP-013 | after: confirmed the import of missing_first_name_1004232808.csv | "1 member uploaded successfully!, 2 members already in the group." (banner)
- GRP-013 | after: confirmed the import of missing_first_name_1004232808.csv | "1 member uploaded successfully!" (banner)
- GRP-013 | after: confirmed the import of missing_first_name_1004232808.csv | "2 members already in the group." (banner)
- GRP-013 | after: uploaded missing_email_and_phone_1004232808.csv | "Validation Errors (1):" (on-screen)
- GRP-013 | after: uploaded missing_email_and_phone_1004232808.csv | "At least one of Email or Phone is required" (on-screen)
- GRP-013 | after: confirmed the import of missing_email_and_phone_1004232808.csv | "Validation Errors (1):" (banner)
- GRP-013 | after: confirmed the import of missing_email_and_phone_1004232808.csv | "Invite" (banner)
- GRP-013 | after: confirmed the import of missing_email_and_phone_1004232808.csv | "0 members uploaded successfully!, 2 members already in the group." (banner)
- GRP-013 | after: confirmed the import of missing_email_and_phone_1004232808.csv | "0 members uploaded successfully!" (banner)
- GRP-013 | after: confirmed the import of missing_email_and_phone_1004232808.csv | "2 members already in the group." (banner)
- GRP-013 | after: uploaded bad_phone_number_1004232808.csv | "Validation Errors (1):" (on-screen)
- GRP-013 | after: uploaded bad_phone_number_1004232808.csv | "Invalid phone number "12ab"" (on-screen)
- GRP-013 | after: confirmed the import of bad_phone_number_1004232808.csv | "Validation Errors (1):" (banner)
- GRP-013 | after: confirmed the import of bad_phone_number_1004232808.csv | "Invalid phone number "12ab"" (banner)
- GRP-013 | after: confirmed the import of bad_phone_number_1004232808.csv | "Invite" (banner)
- GRP-013 | after: confirmed the import of bad_phone_number_1004232808.csv | "0 members uploaded successfully!, 2 members already in the group." (banner)
- GRP-013 | after: confirmed the import of bad_phone_number_1004232808.csv | "0 members uploaded successfully!" (banner)
- GRP-013 | after: confirmed the import of bad_phone_number_1004232808.csv | "2 members already in the group." (banner)
- GRP-013 | after: confirmed the import of duplicate_emails_1004232808.csv | "Invite" (banner)
- GRP-013 | after: confirmed the import of duplicate_emails_1004232808.csv | "1 member uploaded successfully!, 3 members already in the group." (banner)
- GRP-013 | after: confirmed the import of duplicate_emails_1004232808.csv | "1 member uploaded successfully!" (banner)
- GRP-013 | after: confirmed the import of duplicate_emails_1004232808.csv | "3 members already in the group." (banner)
- GRP-013 | after: uploaded headers_only_empty_1004232808.csv | "No records found in spreadsheet." (on-screen)
- GRP-015 | after: tapped Remind for a member under Pending Acceptance | "Invitation email resent successfully!" (on-screen)

## REGRESSIONS - passed before, failing now (investigate first)

- **GRP-015** passed in run-20261004-220152; since then: nothing recorded changed - suspect the app build, device state or data

## Where the time went (seconds / calls; the rest is waiting, typing and sleeps)

| Scenario | Total s | element lookups | page reads | adb |
|---|---|---|---|---|
| GRP-013 | 239.6 | 108.3 (210) | 7.8 (14) | 28.7 (104) |
| GRP-012 | 180.2 | 89.9 (160) | 3.8 (12) | 19.4 (66) |
| GRP-001 | 102.8 | 44.5 (135) | 3.8 (20) | 7.6 (26) |
| GRP-006 | 64.2 | 13.9 (41) | 12.3 (30) | 6.1 (32) |
| GRP-015 | 62.7 | 16.3 (21) | 27.6 (15) | 0.7 (2) |
| GRP-010 | 60.5 | 28.1 (94) | 4.9 (14) | 4.6 (19) |
| GRP-014 | 43.9 | 7.8 (21) | 15.4 (10) | 0.5 (2) |
| GRP-008 | 30.9 | 9.1 (31) | 5.2 (11) | 2.6 (14) |
| GRP-007 | 29.4 | 11.2 (29) | 5.4 (9) | 1.6 (9) |
| GRP-009 | 23.2 | 11.1 (43) | 0.9 (6) | 3.4 (7) |
| GRP-005 | 22.5 | 7.3 (24) | 4.1 (10) | 1.2 (8) |
| GRP-011 | 17.8 | 7.1 (24) | 0.6 (2) | 1.7 (6) |
| GRP-004 | 14.8 | 8.2 (27) | 0.9 (5) | 0.4 (3) |
| GRP-003 | 12.9 | 7.2 (20) | 2.0 (7) | 0.1 (1) |
| GRP-002 | 8.3 | 5.6 (15) | 0.2 (2) | 0.2 (1) |

## Controls found on screen that no document or locator map mentions (review - new features?)

- GRP-001 on 'Sign in screen asks for the email / mobile': **🇮🇳** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'OTP screen is shown': **Terms & Conditions** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'OTP screen is shown': **Privacy Policy** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'Home screen after sign-in': **Set Preferences →** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'Home screen after sign-in': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'group form is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'Group Details opens after saving': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-003 on 'Group Details is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-004 on 'Add Members screen': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-014 on 'Members list': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-015 on 'Members list (pending invitees)': **, Home** - listed only (could change data) - test manually or add a scenario

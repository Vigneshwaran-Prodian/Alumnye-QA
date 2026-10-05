# Triage — run-20261004-202705

alumnye | android | module `groups`

> **RUN STOPPED:** Stopped by user (Ctrl+C).

| Metric | Count |
|---|---|
| total | 3 |
| passed | 0 |
| passed zero ai | 0 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 3 |
| error | 0 |
| blocked | 0 |
| skipped | 0 |
| ai calls | 0 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | GRP-012 | Positive | Bulk upload: the Upload area takes valid .xlsx and .csv files and the members are imported | none | assertion: 'Download template' must put a template file in the device Downloads folder / valid_200_members.xlsx: a preview or success confirmation must be shown (shown: (no message)) | reports/results/alumnye/run-20261004-202705/GRP-012_FAILED.png |
| FAILED | GRP-013 | Negative | Bulk upload rejects invalid files and rows (bad e-mail, missing data, duplicates, wrong columns, empty, wrong format) | none | assertion: missing_email.csv (a row without an e-mail) must be rejected or flagged with a validation message (shown: (no message)) / duplicate_emails.csv (the same e-mail twice in one file) must be rejected or flagged with a validation message (shown: (no message)) / could not select 'unsupported_format.txt' in the device file picker | reports/results/alumnye/run-20261004-202705/GRP-013_FAILED.png |
| FAILED | GRP-014 | Positive | Members tab of an existing group lists the members, including the Anchor with their member code | none | assertion: the Members list must show member codes (e.g. AN1) / the Members tab says 1 member(s); the list shows 0 member code(s) | reports/results/alumnye/run-20261004-202705/GRP-014_FAILED.png |

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- GRP-012: choose_file_button -> ViewGroup at x97,y1117 886x420 | confirm_import -> ViewGroup at x475,y1987 491x126 | choose_file_button -> ViewGroup at x97,y1117 886x420 | confirm_import -> ViewGroup at x475,y1733 491x126
- GRP-013: choose_file_button -> ViewGroup at x97,y1117 886x420 | choose_file_button -> ViewGroup at x97,y1117 886x420 | choose_file_button -> ViewGroup at x97,y1117 886x420 | choose_file_button -> ViewGroup at x97,y1117 886x420
- GRP-014: role_anchor -> ViewGroup at x857,y186 173x58 | members_tab -> ViewGroup at x540,y800 540x130

## Flow variants the runner detected

- GRP-012: the app was left for 'com.android.chrome' (after 'Download template'); the runner brought Alumnye back to the front
- GRP-012: template download: no new file seen (the app was left and recovered)
- GRP-012: valid_200_members.xlsx (template format (.xlsx), 200 valid members): (no message)
- GRP-012: valid_5_members.csv (.csv format, 5 valid members): (no message)
- GRP-013: invalid_email_format.xlsx (rows with malformed e-mail addresses): Validation Errors (2): / Invalid email format "not-an-email" / Invalid email format "abc@"
- GRP-013: the app was left for 'com.google.android.documentsui' (after picking the file); the runner brought Alumnye back to the front
- GRP-013: missing_first_name.csv (a row without a first name): (no message)
- GRP-013: missing_email.csv (a row without an e-mail): (no message)
- GRP-013: bad_phone_number.csv (a row with a malformed phone number): Validation Errors (1): / Invalid phone number "12ab"
- GRP-013: duplicate_emails.csv (the same e-mail twice in one file): (no message)
- GRP-013: wrong_columns.csv (columns that do not match the template): List of Members / Validation Errors (1): / Row 2: / At least one of Email or Phone is required / Cancel / Confirm Import
- GRP-013: headers_only_empty.csv (a file with headers and no members): No records found in spreadsheet.
- GRP-013: unsupported_format.txt (a .txt file (only .xlsx / .csv are allowed)): (no message)
- GRP-013: the app was left for 'com.google.android.documentsui' (after an upload); the runner brought Alumnye back to the front
- GRP-014: Members tab count: 1; codes seen: none

## Messages observed (review wording — also in message-catalog.md)

- GRP-012 | after: confirmed the import of valid_5_members.csv | "5 members uploaded successfully!" (on-screen)
- GRP-013 | after: uploaded invalid_email_format.xlsx | "Validation Errors (2):" (on-screen)
- GRP-013 | after: uploaded invalid_email_format.xlsx | "Invalid email format "not-an-email"" (on-screen)
- GRP-013 | after: uploaded invalid_email_format.xlsx | "Invalid email format "abc@"" (on-screen)
- GRP-013 | after: uploaded bad_phone_number.csv | "Validation Errors (1):" (on-screen)
- GRP-013 | after: uploaded bad_phone_number.csv | "Invalid phone number "12ab"" (on-screen)
- GRP-013 | after: uploaded wrong_columns.csv | "List of Members" (on-screen)
- GRP-013 | after: uploaded wrong_columns.csv | "Validation Errors (1):" (on-screen)
- GRP-013 | after: uploaded wrong_columns.csv | "Row 2:" (on-screen)
- GRP-013 | after: uploaded wrong_columns.csv | "At least one of Email or Phone is required" (on-screen)
- GRP-013 | after: uploaded wrong_columns.csv | "Cancel" (on-screen)
- GRP-013 | after: uploaded wrong_columns.csv | "Confirm Import" (on-screen)
- GRP-013 | after: uploaded headers_only_empty.csv | "No records found in spreadsheet." (on-screen)

## Regression guard - things that changed under scenarios that had PASSED

- shared runner code changed since the last baseline: flows.py, testdata.py (every passed scenario that uses it must be re-verified)

## Where the time went (seconds / calls; the rest is waiting, typing and sleeps)

| Scenario | Total s | element lookups | page reads | adb |
|---|---|---|---|---|
| GRP-013 | 161.1 | 62.0 (166) | 14.7 (74) | 14.3 (51) |
| GRP-012 | 79.0 | 19.6 (40) | 17.0 (36) | 7.1 (32) |
| GRP-014 | 18.1 | 4.0 (15) | 5.1 (7) | 0.4 (2) |

## Controls found on screen that no document or locator map mentions (review - new features?)

- GRP-012 on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-012 on 'Group Details is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-012 on 'Upload tab': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-014 on 'Members list': **, Home** - listed only (could change data) - test manually or add a scenario

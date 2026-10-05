# Triage — run-20261004-220152

alumnye | android | module `groups`

| Metric | Count |
|---|---|
| total | 4 |
| passed | 2 |
| passed zero ai | 2 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 2 |
| error | 0 |
| blocked | 0 |
| skipped | 0 |
| ai calls | 0 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | GRP-012 | Positive | Bulk upload: valid .xlsx and .csv files (picked from local storage) reach the preview without errors and import | none | assertion: 'Member Template Download' must save a template file to the device Downloads folder / valid_200_members.xlsx: the 'List of Members' preview with 'Confirm Import' must be shown / valid_200_members.xlsx: the preview must list the rows of THIS file (expected to see qa.member001@yopmail.com) | reports/results/alumnye/run-20261004-220152/GRP-012_FAILED.png |
| FAILED | GRP-013 | Negative | Bulk upload flags invalid files and rows (picked from local storage): bad e-mail, missing data, duplicates, wrong columns, empty, wrong format | none | assertion: missing_first_name.csv (a row without a first name) must be flagged with a validation message (shown: (nothing flagged)) / duplicate_emails.csv (the same e-mail twice in one file) must be flagged with a validation message (shown: (nothing flagged)) | reports/results/alumnye/run-20261004-220152/GRP-013_FAILED.png |
| PASSED | GRP-014 | Positive | Members tab: the count equals the accepted-members name list; invitees sit under Pending Acceptance, not in the count | none |  | reports/results/alumnye/run-20261004-220152/GRP-014_PASSED.png |
| PASSED | GRP-015 | Positive | Pending Acceptance members each have a Remind button; accepted members do not | none |  | reports/results/alumnye/run-20261004-220152/GRP-015_PASSED.png |

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- GRP-012: choose_file_button -> ViewGroup at x97,y1117 886x420 | confirm_import -> ViewGroup at x475,y1733 491x126 | choose_file_button -> ViewGroup at x97,y1117 886x420 | confirm_import -> ViewGroup at x475,y1475 491x126
- GRP-013: choose_file_button -> ViewGroup at x97,y1117 886x420 | upload_cancel -> ViewGroup at x116,y1356 327x126 | choose_file_button -> ViewGroup at x97,y1117 886x420 | choose_file_button -> ViewGroup at x97,y1117 886x420

## Flow variants the runner detected

- GRP-012: the app was left for 'com.android.chrome' (after 'Member Template Download'); the runner brought Alumnye back to the front
- GRP-012: template download: no fresh file (the app was left for the browser and recovered)
- GRP-012: the picker stayed open after choosing 'valid_200_members.xlsx'
- GRP-012: valid_200_members.xlsx (template format (.xlsx), 200 valid members): preview=False errors=none
- GRP-012: the app was left for 'com.google.android.documentsui' (after an upload); the runner brought Alumnye back to the front
- GRP-012: valid_5_members.csv (.csv format, 5 valid members): preview=True errors=none
- GRP-012: valid_email_or_phone_only.csv (one row with only an e-mail and one with only a phone (either is enough)): preview=True errors=none
- GRP-013: invalid_email_format.xlsx (rows with malformed e-mail addresses): preview=True flagged: Validation Errors (2): / Invalid email format "not-an-email" / Invalid email format "abc@"
- GRP-013: missing_first_name.csv (a row without a first name): preview=True flagged: (nothing flagged)
- GRP-013: missing_email_and_phone.csv (a row with neither e-mail nor phone (the app requires at least one)): preview=True flagged: Validation Errors (1): / At least one of Email or Phone is required
- GRP-013: bad_phone_number.csv (a row with a malformed phone number): preview=True flagged: Validation Errors (1): / Invalid phone number "12ab"
- GRP-013: duplicate_emails.csv (the same e-mail twice in one file): preview=True flagged: (nothing flagged)
- GRP-013: wrong_columns.csv (columns that do not match the template): preview=True flagged: Validation Errors (1): / At least one of Email or Phone is required
- GRP-013: headers_only_empty.csv (a file with headers and no members): preview=False flagged: No records found in spreadsheet.
- GRP-013: the app was left for 'com.google.android.documentsui' (closing the file picker); the runner brought Alumnye back to the front
- GRP-013: 'unsupported_format.txt' could not be chosen in the file picker (the picker does not offer it)
- GRP-013: unsupported_format.txt (a .txt file (only .xlsx / .csv are allowed)): the picker does not accept it - rejected at the picker (correct)
- GRP-014: Members tab count 1; accepted list (1): Vivek Reddy (Anchor); pending rows read: 41
- GRP-015: pending rows read: 51; accepted members: Vivek Reddy
- GRP-015: Remind feedback: 0.0 / Invitation email resent successfully!

## Messages observed (review wording — also in message-catalog.md)

- GRP-012 | after: confirmed the import of valid_5_members.csv | "0 members uploaded successfully!, 5 members already in the group." (on-screen)
- GRP-012 | after: confirmed the import of valid_5_members.csv | "0 members uploaded successfully!" (on-screen)
- GRP-012 | after: confirmed the import of valid_email_or_phone_only.csv | "2 members uploaded successfully!" (on-screen)
- GRP-013 | after: uploaded invalid_email_format.xlsx | "Validation Errors (2):" (on-screen)
- GRP-013 | after: uploaded invalid_email_format.xlsx | "Invalid email format "not-an-email"" (on-screen)
- GRP-013 | after: uploaded invalid_email_format.xlsx | "Invalid email format "abc@"" (on-screen)
- GRP-013 | after: uploaded missing_email_and_phone.csv | "Validation Errors (1):" (on-screen)
- GRP-013 | after: uploaded missing_email_and_phone.csv | "At least one of Email or Phone is required" (on-screen)
- GRP-013 | after: uploaded bad_phone_number.csv | "Validation Errors (1):" (on-screen)
- GRP-013 | after: uploaded bad_phone_number.csv | "Invalid phone number "12ab"" (on-screen)
- GRP-013 | after: uploaded wrong_columns.csv | "Validation Errors (1):" (on-screen)
- GRP-013 | after: uploaded wrong_columns.csv | "At least one of Email or Phone is required" (on-screen)
- GRP-013 | after: uploaded headers_only_empty.csv | "No records found in spreadsheet." (on-screen)
- GRP-015 | after: tapped Remind for a member under Pending Acceptance | "0.0" (on-screen)
- GRP-015 | after: tapped Remind for a member under Pending Acceptance | "Invitation email resent successfully!" (on-screen)

## Regression guard - things that changed under scenarios that had PASSED

- shared runner code changed since the last baseline: app.py, flows.py, testdata.py (every passed scenario that uses it must be re-verified)

## Where the time went (seconds / calls; the rest is waiting, typing and sleeps)

| Scenario | Total s | element lookups | page reads | adb |
|---|---|---|---|---|
| GRP-012 | 183.3 | 65.9 (231) | 5.8 (20) | 11.4 (79) |
| GRP-013 | 106.5 | 36.5 (154) | 12.0 (13) | 9.5 (66) |
| GRP-015 | 40.8 | 8.6 (15) | 18.5 (15) | 0.1 (2) |
| GRP-014 | 35.3 | 6.6 (29) | 12.5 (10) | 0.1 (2) |

## Controls found on screen that no document or locator map mentions (review - new features?)

- GRP-012 on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-012 on 'Group Details is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-014 on 'Members list': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-015 on 'Members list (pending invitees)': **, Home** - listed only (could change data) - test manually or add a scenario

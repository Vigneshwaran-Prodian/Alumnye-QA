# Triage — run-20261004-221135

alumnye | android | module `groups`

| Metric | Count |
|---|---|
| total | 2 |
| passed | 0 |
| passed zero ai | 0 |
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
| FAILED | GRP-012 | Positive | Bulk upload: valid .xlsx and .csv files (new data each run, picked from local storage) reach the preview, are confirmed and imported | none | assertion: 'Member Template Download' must save a template file to the device Downloads folder / valid_200_members_1004221225.xlsx: the app must confirm the import (shown: nothing) | reports/results/alumnye/run-20261004-221135/GRP-012_FAILED.png |
| FAILED | GRP-013 | Negative | Bulk upload flags invalid files and rows (new data each run): bad e-mail, missing data, duplicates, wrong columns, empty, wrong format | none | assertion: missing_first_name_1004221352.csv (a row without a first name) must be flagged with a validation message in the preview or at the top of the app (shown: (nothing flagged)) / duplicate_emails_1004221352.csv (the same e-mail twice in one file) must be flagged with a validation message in the preview or at the top of the app (shown: (nothing flagged)) | reports/results/alumnye/run-20261004-221135/GRP-013_FAILED.png |

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- GRP-012: choose_file_button -> ViewGroup at x97,y1117 886x420 | confirm_import -> ViewGroup at x475,y1733 491x126 | choose_file_button -> ViewGroup at x97,y1117 886x420 | confirm_import -> ViewGroup at x475,y1475 491x126
- GRP-013: choose_file_button -> ViewGroup at x97,y1117 886x420 | upload_cancel -> ViewGroup at x116,y1356 327x126 | choose_file_button -> ViewGroup at x97,y1117 886x420 | choose_file_button -> ViewGroup at x97,y1117 886x420

## Flow variants the runner detected

- GRP-012: the app was left for 'com.android.chrome' (after 'Member Template Download'); the runner brought Alumnye back to the front
- GRP-012: template download: no fresh file (the app was left for the browser and recovered)
- GRP-012: valid_200_members_1004221225.xlsx (template format (.xlsx), 200 valid members): preview=True errors=none
- GRP-012: valid_5_members_1004221225.csv (.csv format, 5 valid members): preview=True errors=none
- GRP-012: valid_email_or_phone_only_1004221225.csv (one row with only an e-mail and one with only a phone (either is enough)): preview=True errors=none
- GRP-013: invalid_email_format_1004221352.xlsx (rows with malformed e-mail addresses): preview=True confirmed=True flagged: Validation Errors (2): / Invalid email format "not-an-email" / Invalid email format "abc@"
- GRP-013: missing_first_name_1004221352.csv (a row without a first name): preview=True confirmed=True flagged: (nothing flagged)
- GRP-013: missing_email_and_phone_1004221352.csv (a row with neither e-mail nor phone (the app requires at least one)): preview=True confirmed=True flagged: Validation Errors (1): / At least one of Email or Phone is required
- GRP-013: bad_phone_number_1004221352.csv (a row with a malformed phone number): preview=True confirmed=True flagged: Validation Errors (1): / Invalid phone number "12ab"
- GRP-013: duplicate_emails_1004221352.csv (the same e-mail twice in one file): preview=True confirmed=True flagged: (nothing flagged)
- GRP-013: wrong_columns_1004221352.csv (columns that do not match the template): preview=True confirmed=False flagged: Validation Errors (1): / At least one of Email or Phone is required
- GRP-013: headers_only_empty_1004221352.csv (a file with headers and no members): preview=False confirmed=False flagged: No records found in spreadsheet.
- GRP-013: the app was left for 'com.google.android.documentsui' (closing the file picker); the runner brought Alumnye back to the front
- GRP-013: 'unsupported_format_1004221352.txt' could not be chosen in the file picker (the picker does not offer it)
- GRP-013: unsupported_format_1004221352.txt (a .txt file (only .xlsx / .csv are allowed)): the picker does not accept it - rejected at the picker (correct)

## Messages observed (review wording — also in message-catalog.md)

- GRP-012 | after: confirmed the import of valid_5_members_1004221225.csv | "0 members uploaded successfully!, 5 members already in the group." (on-screen)
- GRP-012 | after: confirmed the import of valid_5_members_1004221225.csv | "0 members uploaded successfully!" (on-screen)
- GRP-012 | after: confirmed the import of valid_email_or_phone_only_1004221225.csv | "2 members uploaded successfully!" (on-screen)
- GRP-013 | after: uploaded invalid_email_format_1004221352.xlsx | "Validation Errors (2):" (on-screen)
- GRP-013 | after: uploaded invalid_email_format_1004221352.xlsx | "Invalid email format "not-an-email"" (on-screen)
- GRP-013 | after: uploaded invalid_email_format_1004221352.xlsx | "Invalid email format "abc@"" (on-screen)
- GRP-013 | after: confirmed the import of invalid_email_format_1004221352.xlsx | "Validation Errors (2):" (on-screen)
- GRP-013 | after: confirmed the import of invalid_email_format_1004221352.xlsx | "2 members uploaded successfully!" (on-screen)
- GRP-013 | after: confirmed the import of missing_first_name_1004221352.csv | "1 member uploaded successfully!, 2 members already in the group." (on-screen)
- GRP-013 | after: confirmed the import of missing_first_name_1004221352.csv | "1 member uploaded successfully!" (on-screen)
- GRP-013 | after: uploaded missing_email_and_phone_1004221352.csv | "Validation Errors (1):" (on-screen)
- GRP-013 | after: uploaded missing_email_and_phone_1004221352.csv | "At least one of Email or Phone is required" (on-screen)
- GRP-013 | after: confirmed the import of missing_email_and_phone_1004221352.csv | "0 members uploaded successfully!, 2 members already in the group." (on-screen)
- GRP-013 | after: confirmed the import of missing_email_and_phone_1004221352.csv | "0 members uploaded successfully!" (on-screen)
- GRP-013 | after: uploaded bad_phone_number_1004221352.csv | "Validation Errors (1):" (on-screen)
- GRP-013 | after: uploaded bad_phone_number_1004221352.csv | "Invalid phone number "12ab"" (on-screen)
- GRP-013 | after: confirmed the import of bad_phone_number_1004221352.csv | "0 members uploaded successfully!, 2 members already in the group." (on-screen)
- GRP-013 | after: confirmed the import of bad_phone_number_1004221352.csv | "0 members uploaded successfully!" (on-screen)
- GRP-013 | after: confirmed the import of duplicate_emails_1004221352.csv | "1 member uploaded successfully!, 3 members already in the group." (on-screen)
- GRP-013 | after: confirmed the import of duplicate_emails_1004221352.csv | "1 member uploaded successfully!" (on-screen)
- GRP-013 | after: uploaded wrong_columns_1004221352.csv | "Validation Errors (1):" (on-screen)
- GRP-013 | after: uploaded wrong_columns_1004221352.csv | "At least one of Email or Phone is required" (on-screen)
- GRP-013 | after: uploaded headers_only_empty_1004221352.csv | "No records found in spreadsheet." (on-screen)

## Regression guard - things that changed under scenarios that had PASSED

- shared runner code changed since the last baseline: flows.py, testdata.py (every passed scenario that uses it must be re-verified)

## Where the time went (seconds / calls; the rest is waiting, typing and sleeps)

| Scenario | Total s | element lookups | page reads | adb |
|---|---|---|---|---|
| GRP-013 | 128.5 | 52.2 (200) | 13.7 (39) | 9.9 (66) |
| GRP-012 | 113.3 | 46.4 (125) | 8.9 (19) | 7.0 (53) |

## Controls found on screen that no document or locator map mentions (review - new features?)

- GRP-012 on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-012 on 'Group Details is shown': **, Home** - listed only (could change data) - test manually or add a scenario

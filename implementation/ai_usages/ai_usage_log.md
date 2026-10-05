# AI Usage Log

One entry per real AI invocation (failure diagnosis, screen-mismatch adaptation, CLI-halt recovery).

| Date | Run ID | Scenario ID | Trigger (failure / mismatch / halt) | Outcome (fixed / adapted+logged / real bug / escalated) |
|---|---|---|---|---|
| 2026-10-03 | run-20261003-171412 | AUTH-001 | element 'identifier_field' not found | escalated to human |
| 2026-10-03 | run-20261003-171959 | AUTH-004 | element 'primary_button' not found | escalated to human |
| 2026-10-03 | run-20261003-171959 | AUTH-005 | element 'home_marker' not found | likely real bug |
| 2026-10-03 | run-20261003-173158 | AUTH-004 | element 'otp_input' not found | likely real bug |
| 2026-10-03 | run-20261003-181342 | AUTH-004 | stuck: tick the 'I accept the Terms & Conditions and Privacy Policy' checkbox (icon left of that text) | Qwen advised tap 34 - The checkbox is likely the first element with the icon (index 34) and tapping it directly should accept the terms. |
| 2026-10-03 | run-20261003-183744 | AUTH-004 | stuck: tick the 'I accept the Terms & Conditions and Privacy Policy' checkbox (icon left of that text) | Qwen advised back  - Keyboard visible; close to unblock taps |
| 2026-10-03 | run-20261003-183744 | AUTH-004 | stuck: tick the 'I accept the Terms & Conditions and Privacy Policy' checkbox (icon left of that text) | Qwen advised tap 34 - Checkbox is at index 34 with visible tap target |
| 2026-10-03 | run-20261003-231053 | AUTH-007 | element 'landing_sign_in' not found | adapted + logged -> btnx: |
| 2026-10-03 | run-20261003-232257 | AUTH-008 | element 'sign_out' not found | adapted + logged -> btnx:, My Account |
| 2026-10-03 | run-20261003-232257 | AUTH-008 | element 'landing_sign_in' not found | adapted + logged -> btnx:Sign Out |
| 2026-10-03 | run-20261003-232257 | AUTH-008 | element 'landing_sign_in' not found | adapted + logged -> btnx:, Home |
| 2026-10-04 | run-20261004-191224 | GRP-002 | element 'group_details_marker' not found | likely real bug |
| 2026-10-04 | run-20261004-191224 | GRP-003 | element 'landing_sign_in' not found | likely real bug |
| 2026-10-04 | run-20261004-191826 | GRP-012 | element 'confirm_import' not found | likely real bug |
| 2026-10-04 | run-20261004-191826 | GRP-012 | stuck: something (a dialog, pop-up or overlay) may be covering the screen; clear it so that 'Bulk Preview: confirm import' becomes reachable | Qwen advised tap 50 - Upload file to trigger 'Bulk Preview: confirm import' dialog |
| 2026-10-04 | run-20261004-195942 | GRP-005 | element 'invite_email_field' not found | likely real bug |
| 2026-10-04 | run-20261004-195942 | GRP-005 | stuck: something (a dialog, pop-up or overlay) may be covering the screen; clear it so that 'Invite: email entry' becomes reachable | Qwen advised back  - Close potential modal dialog covering the Invite email entry field. |
| 2026-10-04 | run-20261004-195942 | GRP-005 | stuck: something (a dialog, pop-up or overlay) may be covering the screen; clear it so that 'Invite: email entry' becomes reachable | Qwen advised tap 25 - Switch from MEMBER to ANCHOR tab; invite likely accessible there. |
| 2026-10-04 | run-20261004-200934 | GRP-012 | element 'confirm_import' not found | likely real bug |
| 2026-10-04 | run-20261004-200934 | GRP-014 | element 'landing_sign_in' not found | likely real bug |
| 2026-10-04 | run-20261004-213711 | GRP-012 | element 'anchor_home_marker' not found | likely real bug |
| 2026-10-04 | run-20261004-213711 | GRP-013 | element 'landing_sign_in' not found | likely real bug |
| 2026-10-04 | run-20261004-213711 | GRP-014 | element 'landing_sign_in' not found | likely real bug |
| 2026-10-04 | run-20261004-213711 | GRP-015 | element 'landing_sign_in' not found | likely real bug |
| 2026-10-04 | run-20261004-223035 | GRP-001 | element 'landing_sign_in' not found | likely real bug |
| 2026-10-04 | run-20261004-234648 | JNY-001 | stuck: finish this profile screen (fill every required field marked * with a valid value) and move forward until the Home screen | Qwen advised type 35 - Mobile number field is empty; entering valid Indian 10-digit number. |
| 2026-10-04 | run-20261004-234648 | JNY-001 | stuck: finish this profile screen (fill every required field marked * with a valid value) and move forward until the Home screen | Qwen advised type 35 - Current mobile number is already registered; replace with different valid number. |
| 2026-10-04 | run-20261004-234648 | JNY-001 | stuck: finish this profile screen (fill every required field marked * with a valid value) and move forward until the Home screen | Qwen advised type 35 - Phone number registered to another user; try different number. |
| 2026-10-04 | run-20261004-234648 | JNY-001 | stuck: finish this profile screen (fill every required field marked * with a valid value) and move forward until the Home screen | Qwen advised type 35 - Phone number is registered to another user; try a different number. |
| 2026-10-04 | run-20261004-234648 | JNY-001 | element 'home_marker' not found | likely real bug |
| 2026-10-04 | run-20261004-234648 | JNY-002 | stuck: finish this profile screen (fill every required field marked * with a valid value) and move forward until the Home screen | Qwen advised type 35 - Mobile number field is empty, which is a required field. |
| 2026-10-04 | run-20261004-234648 | JNY-002 | element 'group_description_field' not found | likely real bug |
| 2026-10-05 | run-20261005-000048 | JNY-001 | element 'group_details_marker' not found | AI call failed: no JSON in AI reply: 'Execution errorTerminate batch job (Y/N)? \n' |
| 2026-10-05 | run-20261005-000048 | JNY-001 | element 'otp_screen_marker' not found | AI call failed: no JSON in AI reply: 'Execution errorTerminate batch job (Y/N)? \n' |
| 2026-10-05 | run-20261005-000620 | JNY-001 | stuck: finish this profile screen (fill every required field marked * with a valid value) and move forward until the Home screen | Qwen advised type 35 - Mobile number field is empty; filling with valid 10-digit Indian number |
| 2026-10-05 | run-20261005-000620 | JNY-001 | element 'group_details_marker' not found | likely real bug |

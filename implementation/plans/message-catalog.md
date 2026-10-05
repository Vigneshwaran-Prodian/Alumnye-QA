# Message Catalog (observed in real runs)

Every toast / inline error / validation text the app showed after a scripted action, with the scenario and
trigger that caused it. Filled automatically by `alumnye-qa run`; review the wording and fill the last two columns.
Note: "on-screen" rows include any new text after the action — ignore rows that are just the next screen's content.

| Module | Scenario | Trigger (what the user did) | Observed message | Where | Expected wording (fill in) | Wording OK? | First seen |
|---|---|---|---|---|---|---|---|
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | MEMBER | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | ANCHOR | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | Welcome, Anita | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | SET DEFAULT PREFERENCES, Just now, Complete Your Profile Defaults, Fill your default food, room and travel choices to auto-fill event RSVPs. | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | SET DEFAULT PREFERENCES | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | Just now | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | Complete Your Profile Defaults | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | Fill your default food, room and travel choices to auto-fill event RSVPs. | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | Set Preferences → | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | Welcome to Alumnye! | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | You don't have any events yet. When you're invited to a group, events will appear here so you can stay connected with your community. | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | , Home | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | Home | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | , My Group | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | My Group | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | , My Account | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | My Account | on-screen |  |  | run-20261003-190235 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Web View | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Close tab | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Minimize tab | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Your connection to this site is not secure | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | accounts.google.com | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Share | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Customize and control Google Chrome | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Connection is secure | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Access blocked: Authorization Error | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | vignesh94.prodian@gmail.com | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Custom scheme URIs are not allowed for 'WEB' client type. | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | If you are a developer of alumnye, see | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | error details | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Error 400: invalid_request | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Open Google Account Help Center (external, opens in a new window) | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Privacy Policy (external, opens in a new window) | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-005 | tapped Sign in with Google and chose the device account | Google Terms of Service (external, opens in a new window) | on-screen |  |  | run-20261003-231053 |
| auth | AUTH-004 | profile screen 1: tapped 'Continue' | Welcome, Vivek | on-screen |  |  | run-20261003-232257 |
| auth | AUTH-010 | entered invalid identifier 'abc@' | (Continue button stays disabled) | state |  |  | run-20261003-232257 |
| auth | AUTH-010 | entered invalid identifier '12345' | (Continue button stays disabled) | state |  |  | run-20261003-232257 |
| auth | AUTH-010 | entered invalid identifier 'no spaces@yopmail.com' | (Continue button stays disabled) | state |  |  | run-20261003-232257 |
| auth | AUTH-011 | entered wrong OTP 000000 and tapped Verify | Invalid OTP | on-screen |  |  | run-20261003-232257 |
| auth | AUTH-011 | entered wrong OTP 000000 and tapped Verify | Resend code (1:50) | on-screen |  |  | run-20261003-232257 |
| auth | AUTH-011 | entered wrong OTP 000000 and tapped Verify | Resend code (1:49) | on-screen |  |  | run-20261003-232257 |
| auth | AUTH-011 | entered wrong OTP 000000 and tapped Verify | Resend code (1:48) | on-screen |  |  | run-20261003-232257 |
| auth | AUTH-011 | entered wrong OTP 000000 and tapped Verify | Resend code (1:47) | on-screen |  |  | run-20261003-232257 |
| auth | AUTH-012 | entered a valid OTP but did not tick the Terms checkbox | (Verify & join Alumnye stays disabled) | state |  |  | run-20261003-232257 |
| auth | AUTH-013 | empty first/last name | (Continue button stays disabled) | state |  |  | run-20261003-232257 |
| auth | AUTH-015 | arrived on the Verify identity screen | Resend code (2:00) | state |  |  | run-20261003-232257 |
| auth | AUTH-015 | tapped Resend code after the countdown ended | Resend code (2:00) | on-screen |  |  | run-20261003-232257 |
| auth | AUTH-015 | tapped Resend code after the countdown ended | Success, A new code has been sent | on-screen |  |  | run-20261003-232257 |
| auth | AUTH-015 | tapped Resend code after the countdown ended | Success | on-screen |  |  | run-20261003-232257 |
| auth | AUTH-015 | tapped Resend code after the countdown ended | A new code has been sent | on-screen |  |  | run-20261003-232257 |
| auth | AUTH-015 | tapped Resend code after the countdown ended | Resend code (1:59) | on-screen |  |  | run-20261003-232257 |
| auth | AUTH-015 | tapped Resend code after the countdown ended | Resend code (1:58) | on-screen |  |  | run-20261003-232257 |
| auth | AUTH-009 | Member ID before typing | (empty) | state |  |  | run-20261004-001220 |
| auth | AUTH-009 | after first name 'Meera' | (empty) | state |  |  | run-20261004-001220 |
| auth | AUTH-009 | after last name 'Sharma' | MS1 | state |  |  | run-20261004-001220 |
| auth | AUTH-013 | spaces-only first/last name | (Continue button stays disabled) | state |  |  | run-20261004-001220 |
| groups | GRP-001 | a pop-up appeared | Success / Group created successfully! | dialog |  |  | run-20261004-191826 |
| groups | GRP-005 | sent invitation to 'karthik.nair.1004192002@yopmail.com' | Enter email address... | on-screen |  |  | run-20261004-191826 |
| groups | GRP-005 | sent invitation to 'karthik.nair.1004192002@yopmail.com' | Invite sent successfully! | on-screen |  |  | run-20261004-191826 |
| groups | GRP-006 | sent invitation to 'abc@' | Please enter a valid email format | on-screen |  |  | run-20261004-191826 |
| groups | GRP-006 | sent invitation to 'plainaddress' | Please enter a valid email format | on-screen |  |  | run-20261004-191826 |
| groups | GRP-006 | sent invitation to 'no spaces@yopmail.com' | Please enter a valid email format | on-screen |  |  | run-20261004-191826 |
| groups | GRP-007 | sent invitation to 'vivek.reddy.1003232340@yopmail.com' | Enter email address... | on-screen |  |  | run-20261004-191826 |
| groups | GRP-007 | sent invitation to 'vivek.reddy.1003232340@yopmail.com' | Invite sent successfully! | on-screen |  |  | run-20261004-191826 |
| groups | GRP-008 | sent invitation to 'arjun.sharma.1004192121@yopmail.com' | Enter email address... | on-screen |  |  | run-20261004-191826 |
| groups | GRP-008 | sent invitation to 'arjun.sharma.1004192121@yopmail.com' | Invite sent successfully! | on-screen |  |  | run-20261004-191826 |
| groups | GRP-008 | sent invitation to 'arjun.sharma.1004192121@yopmail.com' | User already invited to this group | on-screen |  |  | run-20261004-191826 |
| groups | GRP-009 | tried to save a group with an empty name | (button stays disabled) | state |  |  | run-20261004-191826 |
| groups | GRP-009 | tried to save a group with a spaces-only name | (button stays disabled) | state |  |  | run-20261004-191826 |
| groups | GRP-010 | a pop-up appeared | Success / Group created successfully! | dialog |  |  | run-20261004-191826 |
| groups | GRP-010 | tried to create a second group with an existing name | A group with this name already exists. Please choose a different name. | on-screen |  |  | run-20261004-191826 |
| groups | GRP-005 | sent invitation to 'divya.reddy.1004195243@yopmail.com' | Enter email address... | on-screen |  |  | run-20261004-194847 |
| groups | GRP-006 | sent invitation to 'a@b' | Please enter a valid email format | on-screen |  |  | run-20261004-195942 |
| groups | GRP-006 | sent invitation to '@yopmail.com' | Please enter a valid email format | on-screen |  |  | run-20261004-195942 |
| groups | GRP-005 | sent invitation to 'meera.nair.1004201045@yopmail.com' | Enter email address... | on-screen |  |  | run-20261004-200934 |
| groups | GRP-005 | sent invitation to 'meera.nair.1004201045@yopmail.com' | Invite sent successfully! | on-screen |  |  | run-20261004-200934 |
| groups | GRP-007 | sent invitation to 'vivek.reddy.1004001541@yopmail.com' | You are already an anchor | on-screen |  |  | run-20261004-200934 |
| groups | GRP-008 | sent invitation to 'divya.kapoor.1004201216@yopmail.com' | Enter email address... | on-screen |  |  | run-20261004-200934 |
| groups | GRP-008 | sent invitation to 'divya.kapoor.1004201216@yopmail.com' | Invite sent successfully! | on-screen |  |  | run-20261004-200934 |
| groups | GRP-008 | sent invitation to 'divya.kapoor.1004201216@yopmail.com' | 0.0 | on-screen |  |  | run-20261004-200934 |
| groups | GRP-008 | sent invitation to 'divya.kapoor.1004201216@yopmail.com' | User already invited to this group | on-screen |  |  | run-20261004-200934 |
| groups | GRP-012 | confirmed the import of valid_5_members.csv | 5 members uploaded successfully! | on-screen |  |  | run-20261004-202705 |
| groups | GRP-013 | uploaded invalid_email_format.xlsx | Validation Errors (2): | on-screen |  |  | run-20261004-202705 |
| groups | GRP-013 | uploaded invalid_email_format.xlsx | Invalid email format "not-an-email" | on-screen |  |  | run-20261004-202705 |
| groups | GRP-013 | uploaded invalid_email_format.xlsx | Invalid email format "abc@" | on-screen |  |  | run-20261004-202705 |
| groups | GRP-013 | uploaded bad_phone_number.csv | Validation Errors (1): | on-screen |  |  | run-20261004-202705 |
| groups | GRP-013 | uploaded bad_phone_number.csv | Invalid phone number "12ab" | on-screen |  |  | run-20261004-202705 |
| groups | GRP-013 | uploaded wrong_columns.csv | List of Members | on-screen |  |  | run-20261004-202705 |
| groups | GRP-013 | uploaded wrong_columns.csv | Validation Errors (1): | on-screen |  |  | run-20261004-202705 |
| groups | GRP-013 | uploaded wrong_columns.csv | Row 2: | on-screen |  |  | run-20261004-202705 |
| groups | GRP-013 | uploaded wrong_columns.csv | At least one of Email or Phone is required | on-screen |  |  | run-20261004-202705 |
| groups | GRP-013 | uploaded wrong_columns.csv | Cancel | on-screen |  |  | run-20261004-202705 |
| groups | GRP-013 | uploaded wrong_columns.csv | Confirm Import | on-screen |  |  | run-20261004-202705 |
| groups | GRP-013 | uploaded headers_only_empty.csv | No records found in spreadsheet. | on-screen |  |  | run-20261004-202705 |
| groups | GRP-012 | confirmed the import of valid_5_members.csv | 0 members uploaded successfully!, 5 members already in the group. | on-screen |  |  | run-20261004-220152 |
| groups | GRP-012 | confirmed the import of valid_5_members.csv | 0 members uploaded successfully! | on-screen |  |  | run-20261004-220152 |
| groups | GRP-012 | confirmed the import of valid_email_or_phone_only.csv | 2 members uploaded successfully! | on-screen |  |  | run-20261004-220152 |
| groups | GRP-013 | uploaded missing_email_and_phone.csv | Validation Errors (1): | on-screen |  |  | run-20261004-220152 |
| groups | GRP-013 | uploaded missing_email_and_phone.csv | At least one of Email or Phone is required | on-screen |  |  | run-20261004-220152 |
| groups | GRP-015 | tapped Remind for a member under Pending Acceptance | 0.0 | on-screen |  |  | run-20261004-220152 |
| groups | GRP-015 | tapped Remind for a member under Pending Acceptance | Invitation email resent successfully! | on-screen |  |  | run-20261004-220152 |
| groups | GRP-012 | confirmed the import of valid_5_members_1004221225.csv | 0 members uploaded successfully!, 5 members already in the group. | on-screen |  |  | run-20261004-221135 |
| groups | GRP-012 | confirmed the import of valid_5_members_1004221225.csv | 0 members uploaded successfully! | on-screen |  |  | run-20261004-221135 |
| groups | GRP-012 | confirmed the import of valid_email_or_phone_only_1004221225.csv | 2 members uploaded successfully! | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | uploaded invalid_email_format_1004221352.xlsx | Validation Errors (2): | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | uploaded invalid_email_format_1004221352.xlsx | Invalid email format "not-an-email" | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | uploaded invalid_email_format_1004221352.xlsx | Invalid email format "abc@" | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | confirmed the import of invalid_email_format_1004221352.xlsx | Validation Errors (2): | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | confirmed the import of invalid_email_format_1004221352.xlsx | 2 members uploaded successfully! | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | confirmed the import of missing_first_name_1004221352.csv | 1 member uploaded successfully!, 2 members already in the group. | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | confirmed the import of missing_first_name_1004221352.csv | 1 member uploaded successfully! | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | uploaded missing_email_and_phone_1004221352.csv | Validation Errors (1): | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | uploaded missing_email_and_phone_1004221352.csv | At least one of Email or Phone is required | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | confirmed the import of missing_email_and_phone_1004221352.csv | 0 members uploaded successfully!, 2 members already in the group. | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | confirmed the import of missing_email_and_phone_1004221352.csv | 0 members uploaded successfully! | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | uploaded bad_phone_number_1004221352.csv | Validation Errors (1): | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | uploaded bad_phone_number_1004221352.csv | Invalid phone number "12ab" | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | confirmed the import of bad_phone_number_1004221352.csv | 0 members uploaded successfully!, 2 members already in the group. | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | confirmed the import of bad_phone_number_1004221352.csv | 0 members uploaded successfully! | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | confirmed the import of duplicate_emails_1004221352.csv | 1 member uploaded successfully!, 3 members already in the group. | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | confirmed the import of duplicate_emails_1004221352.csv | 1 member uploaded successfully! | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | uploaded wrong_columns_1004221352.csv | Validation Errors (1): | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | uploaded wrong_columns_1004221352.csv | At least one of Email or Phone is required | on-screen |  |  | run-20261004-221135 |
| groups | GRP-013 | uploaded headers_only_empty_1004221352.csv | No records found in spreadsheet. | on-screen |  |  | run-20261004-221135 |
| auth+groups | AUTH-009 | after first name 'Karthik' | (empty) | state |  |  | run-20261004-223035 |
| auth+groups | AUTH-009 | after last name 'Reddy' | KR2 | state |  |  | run-20261004-223035 |
| groups | GRP-005 | sent invitation to 'karthik.iyer.1004232044@yopmail.com' | 0.0 | on-screen |  |  | run-20261004-231812 |
| groups | GRP-005 | sent invitation to 'karthik.iyer.1004232044@yopmail.com' | Enter email address... | on-screen |  |  | run-20261004-231812 |
| groups | GRP-005 | sent invitation to 'karthik.iyer.1004232044@yopmail.com' | Invite sent successfully! | on-screen |  |  | run-20261004-231812 |
| groups | GRP-007 | sent invitation to 'arjun.sharma.1004223213@yopmail.com' | You are already an anchor | on-screen |  |  | run-20261004-231812 |
| groups | GRP-008 | sent invitation to 'arjun.iyer.1004232240@yopmail.com' | Enter email address... | on-screen |  |  | run-20261004-231812 |
| groups | GRP-008 | sent invitation to 'arjun.iyer.1004232240@yopmail.com' | Invite sent successfully! | on-screen |  |  | run-20261004-231812 |
| groups | GRP-008 | sent invitation to 'arjun.iyer.1004232240@yopmail.com' | User already invited to this group | on-screen |  |  | run-20261004-231812 |
| groups | GRP-010 | tried to create a second group with an existing name | 0.0 | on-screen |  |  | run-20261004-231812 |
| groups | GRP-012 | a pop-up appeared | Success / Group created successfully! | dialog |  |  | run-20261004-231812 |
| groups | GRP-012 | confirmed the import of valid_5_members_1004232627.csv | Invite | banner |  |  | run-20261004-231812 |
| groups | GRP-012 | confirmed the import of valid_5_members_1004232627.csv | 0 members uploaded successfully!, 5 members already in the group. | banner |  |  | run-20261004-231812 |
| groups | GRP-012 | confirmed the import of valid_5_members_1004232627.csv | 0 members uploaded successfully! | banner |  |  | run-20261004-231812 |
| groups | GRP-012 | confirmed the import of valid_5_members_1004232627.csv | 5 members already in the group. | banner |  |  | run-20261004-231812 |
| groups | GRP-012 | confirmed the import of valid_email_or_phone_only_1004232627.csv | Invite | banner |  |  | run-20261004-231812 |
| groups | GRP-012 | confirmed the import of valid_email_or_phone_only_1004232627.csv | 2 members uploaded successfully! | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | uploaded invalid_email_format_1004232808.xlsx | Validation Errors (2): | on-screen |  |  | run-20261004-231812 |
| groups | GRP-013 | uploaded invalid_email_format_1004232808.xlsx | Invalid email format "not-an-email" | on-screen |  |  | run-20261004-231812 |
| groups | GRP-013 | uploaded invalid_email_format_1004232808.xlsx | Invalid email format "abc@" | on-screen |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of invalid_email_format_1004232808.xlsx | Validation Errors (2): | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of invalid_email_format_1004232808.xlsx | Invalid email format "not-an-email" | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of invalid_email_format_1004232808.xlsx | Invalid email format "abc@" | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of invalid_email_format_1004232808.xlsx | Invite | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of invalid_email_format_1004232808.xlsx | 2 members uploaded successfully! | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of missing_first_name_1004232808.csv | Invite | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of missing_first_name_1004232808.csv | 1 member uploaded successfully!, 2 members already in the group. | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of missing_first_name_1004232808.csv | 1 member uploaded successfully! | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of missing_first_name_1004232808.csv | 2 members already in the group. | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | uploaded missing_email_and_phone_1004232808.csv | Validation Errors (1): | on-screen |  |  | run-20261004-231812 |
| groups | GRP-013 | uploaded missing_email_and_phone_1004232808.csv | At least one of Email or Phone is required | on-screen |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of missing_email_and_phone_1004232808.csv | Validation Errors (1): | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of missing_email_and_phone_1004232808.csv | Invite | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of missing_email_and_phone_1004232808.csv | 0 members uploaded successfully!, 2 members already in the group. | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of missing_email_and_phone_1004232808.csv | 0 members uploaded successfully! | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of missing_email_and_phone_1004232808.csv | 2 members already in the group. | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | uploaded bad_phone_number_1004232808.csv | Validation Errors (1): | on-screen |  |  | run-20261004-231812 |
| groups | GRP-013 | uploaded bad_phone_number_1004232808.csv | Invalid phone number "12ab" | on-screen |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of bad_phone_number_1004232808.csv | Validation Errors (1): | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of bad_phone_number_1004232808.csv | Invalid phone number "12ab" | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of bad_phone_number_1004232808.csv | Invite | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of bad_phone_number_1004232808.csv | 0 members uploaded successfully!, 2 members already in the group. | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of bad_phone_number_1004232808.csv | 0 members uploaded successfully! | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of bad_phone_number_1004232808.csv | 2 members already in the group. | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of duplicate_emails_1004232808.csv | Invite | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of duplicate_emails_1004232808.csv | 1 member uploaded successfully!, 3 members already in the group. | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of duplicate_emails_1004232808.csv | 1 member uploaded successfully! | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | confirmed the import of duplicate_emails_1004232808.csv | 3 members already in the group. | banner |  |  | run-20261004-231812 |
| groups | GRP-013 | uploaded headers_only_empty_1004232808.csv | No records found in spreadsheet. | on-screen |  |  | run-20261004-231812 |
| journeys | JNY-001 | a pop-up appeared | Success / Group created successfully! | dialog |  |  | run-20261004-234648 |
| journeys | JNY-001 | profile screen 2: tapped 'Continue' | Phone number is already registered to another user | on-screen |  |  | run-20261004-234648 |

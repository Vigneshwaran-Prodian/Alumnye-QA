# Triage — run-20261004-191826

alumnye | android | module `groups`

> **RUN STOPPED:** Stopped by user (Ctrl+C).

| Metric | Count |
|---|---|
| total | 12 |
| passed | 6 |
| passed zero ai | 5 |
| passed after self heal | 1 |
| passed after qwen | 0 |
| failed | 6 |
| error | 0 |
| blocked | 0 |
| skipped | 0 |
| ai calls | 2 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | GRP-003 | Positive | Group Details shows About, member count and the Add Event button | none | assertion: Group Details must show an About section | reports/results/alumnye/run-20261004-191826/GRP-003_FAILED.png |
| FAILED | GRP-004 | Positive | Add Members offers the invitation methods (Invite, Upload, Add Members, Add Contacts) | none | assertion: the 'Add Contacts' option must be available in the add-member screen (v1.3 invitation methods) | reports/results/alumnye/run-20261004-191826/GRP-004_FAILED.png |
| FAILED | GRP-006 | Negative | Invite rejects an invalid email format | none | assertion: 'abc@' must not be accepted as an invitation email (result: unknown) / 'plainaddress' must not be accepted as an invitation email (result: unknown) / 'no spaces@yopmail.com' must not be accepted as an invitation email (result: unknown) | reports/results/alumnye/run-20261004-191826/GRP-006_FAILED.png |
| FAILED | GRP-007 | Negative | Anchor cannot invite their own email address | none | assertion: the Anchor must not be able to invite their own email (result: sent) | reports/results/alumnye/run-20261004-191826/GRP-007_FAILED.png |
| FAILED | GRP-010 | Negative | A duplicate group name is rejected | none | assertion: a message about the duplicate name must be shown | reports/results/alumnye/run-20261004-191826/GRP-010_FAILED.png |
| FAILED | GRP-012 | Positive | Bulk upload of a valid file goes through Bulk Preview and imports the members | qwen | assertion: could not select 'members_valid.csv' in the device file picker / Bulk Preview must show the parsed rows / a success confirmation must be shown after the import | reports/results/alumnye/run-20261004-191826/GRP-012_FAILED.png |
| PASSED | GRP-001 | Positive | Anchor creates a group and lands on its Group Details | self-heal |  | reports/results/alumnye/run-20261004-191826/GRP-001_PASSED.png |
| PASSED | GRP-002 | Positive | Anchor Home offers + New Group and shows the right state (welcome message or the group list) | none |  | reports/results/alumnye/run-20261004-191826/GRP-002_PASSED.png |
| PASSED | GRP-005 | Positive | Anchor invites a member by email and gets a success confirmation | none |  | reports/results/alumnye/run-20261004-191826/GRP-005_PASSED.png |
| PASSED | GRP-008 | Negative | Inviting the same email twice is blocked | none |  | reports/results/alumnye/run-20261004-191826/GRP-008_PASSED.png |
| PASSED | GRP-009 | Negative | Create Group is blocked when the name is empty | none |  | reports/results/alumnye/run-20261004-191826/GRP-009_PASSED.png |
| PASSED | GRP-011 | Edge | Group description is limited to 200 characters with a live counter | none |  | reports/results/alumnye/run-20261004-191826/GRP-011_PASSED.png |

## UI adaptations to confirm (never silent)

- GRP-001: `group_details_marker` -> `text:MEMBER` via heal — label 'MEMBER' ~ ['Add Event', 'Add Member'] (score 0.81)
- GRP-012: `something (a dialog, pop-up or overlay) may be covering the screen; clear it so that 'Bulk Preview: confirm import' becomes reachable` -> `tap 50` via qwen — Upload file to trigger 'Bulk Preview: confirm import' dialog

## Entry paths the runner navigated (Splash -> ... -> target)

- GRP-001: Splash -> dialog 'Success / Group created successfully!' -> OK
- GRP-010: Splash -> dialog 'Success / Group created successfully!' -> OK

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- GRP-003: role_anchor -> ViewGroup at x857,y186 173x58
- GRP-004: role_anchor -> ViewGroup at x857,y186 173x58 | add_member_entry -> ViewGroup at x53,y648 479x97
- GRP-006: tab_invite -> ViewGroup at x0,y474 270x111 | send_invite_button -> ViewGroup at x97,y1483 886x115 | tab_invite -> ViewGroup at x0,y474 270x111 | send_invite_button -> ViewGroup at x97,y1483 886x115
- GRP-007: role_anchor -> ViewGroup at x857,y186 173x58 | add_member_entry -> ViewGroup at x53,y648 479x97 | tab_invite -> ViewGroup at x0,y474 270x111 | send_invite_button -> ViewGroup at x97,y1483 886x115
- GRP-010: save_group_button -> ViewGroup at x63,y1446 954x116 | role_anchor -> ViewGroup at x857,y186 173x58 | new_group_button -> ViewGroup at x696,y447 321x99 | save_group_button -> ViewGroup at x63,y1446 954x116
- GRP-012: add_member_entry -> ViewGroup at x53,y648 479x97 | tab_upload -> ViewGroup at x270,y474 270x111 | choose_file_button -> ViewGroup at x270,y474 270x111 | confirm_import -> ViewGroup at x540,y474 270x111

## Flow variants the runner detected

- GRP-002: user already has groups: group list shown (the empty state applies only to a user with no groups)
- GRP-005: invited karthik.nair.1004192002@yopmail.com; pending invites before: 

## Messages observed (review wording — also in message-catalog.md)

- GRP-001 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- GRP-005 | after: sent invitation to 'karthik.nair.1004192002@yopmail.com' | "Enter email address..." (on-screen)
- GRP-005 | after: sent invitation to 'karthik.nair.1004192002@yopmail.com' | "Invite sent successfully!" (on-screen)
- GRP-006 | after: sent invitation to 'abc@' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to 'plainaddress' | "Please enter a valid email format" (on-screen)
- GRP-006 | after: sent invitation to 'no spaces@yopmail.com' | "Please enter a valid email format" (on-screen)
- GRP-007 | after: sent invitation to 'vivek.reddy.1003232340@yopmail.com' | "Enter email address..." (on-screen)
- GRP-007 | after: sent invitation to 'vivek.reddy.1003232340@yopmail.com' | "Invite sent successfully!" (on-screen)
- GRP-008 | after: sent invitation to 'arjun.sharma.1004192121@yopmail.com' | "Enter email address..." (on-screen)
- GRP-008 | after: sent invitation to 'arjun.sharma.1004192121@yopmail.com' | "Invite sent successfully!" (on-screen)
- GRP-008 | after: sent invitation to 'arjun.sharma.1004192121@yopmail.com' | "User already invited to this group" (on-screen)
- GRP-009 | after: tried to save a group with an empty name | "(button stays disabled)" (state)
- GRP-009 | after: tried to save a group with a spaces-only name | "(button stays disabled)" (state)
- GRP-010 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- GRP-010 | after: tried to create a second group with an existing name | "A group with this name already exists. Please choose a different name." (on-screen)

## Controls found on screen that no document or locator map mentions (review - new features?)

- GRP-001 on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'group form is shown': **Cancel** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'group form is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'Group Details opens after saving': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-003 on 'Group Details is shown': **Edit** - listed only (could change data) - test manually or add a scenario
- GRP-003 on 'Group Details is shown': **Events** - listed only (could change data) - test manually or add a scenario
- GRP-003 on 'Group Details is shown': **, Notice Board, 0 notices, ** - listed only (could change data) - test manually or add a scenario
- GRP-003 on 'Group Details is shown': **, Home** - listed only (could change data) - test manually or add a scenario

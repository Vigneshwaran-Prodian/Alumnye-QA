# Triage — run-20261004-194847

alumnye | android | module `groups`

> **RUN STOPPED:** Stopped by user (Ctrl+C).

| Metric | Count |
|---|---|
| total | 6 |
| passed | 4 |
| passed zero ai | 4 |
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
| FAILED | GRP-005 | Positive | Anchor invites a member by email and gets a success confirmation | none | assertion: inviting divya.reddy.1004195243@yopmail.com must succeed (result: unknown) / a success confirmation must be shown after the invitation is sent | reports/results/alumnye/run-20261004-194847/GRP-005_FAILED.png |
| FAILED | GRP-006 | Negative | Invite rejects an invalid email format with 'Please enter a valid email format' | none | assertion: 'abc@' must not be accepted as an invitation email (result: unknown; message: (no message)) / 'plainaddress' must not be accepted as an invitation email (result: unknown; message: (no message)) / 'no spaces@yopmail.com' must not be accepted as an invitation email (result: unknown; message: (no message)) / 'a@b' must not be accepted as an invitation email (result: unknown; message: (no message)) / '@yopmail.com' must not be accepted as an invitation email (result: unknown; message: (no message)) | reports/results/alumnye/run-20261004-194847/GRP-006_FAILED.png |
| PASSED | GRP-001 | Positive | Anchor creates a group and lands on its Group Details | none |  | reports/results/alumnye/run-20261004-194847/GRP-001_PASSED.png |
| PASSED | GRP-002 | Positive | Anchor Home offers + New Group and shows the right state (welcome message or the group list) | none |  | reports/results/alumnye/run-20261004-194847/GRP-002_PASSED.png |
| PASSED | GRP-003 | Positive | Group Details shows the group, Add Member / Add Event, the Members count tab, Events tab and Notice Board | none |  | reports/results/alumnye/run-20261004-194847/GRP-003_PASSED.png |
| PASSED | GRP-004 | Positive | Add Members shows the four invitation tabs and the Invite form (email OR mobile, Send Invitation) | none |  | reports/results/alumnye/run-20261004-194847/GRP-004_PASSED.png |

## Entry paths the runner navigated (Splash -> ... -> target)

- GRP-001: Splash -> dialog 'Success / Group created successfully!' -> OK

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- GRP-005: role_anchor -> ViewGroup at x857,y186 173x58 | add_member_entry -> ViewGroup at x53,y648 479x97 | tab_invite -> ViewGroup at x0,y474 270x111 | send_invite_button -> ViewGroup at x97,y1483 886x115
- GRP-006: tab_invite -> ViewGroup at x0,y474 270x111 | send_invite_button -> ViewGroup at x97,y1483 886x115 | tab_invite -> ViewGroup at x0,y474 270x111 | send_invite_button -> ViewGroup at x97,y1483 886x115

## Flow variants the runner detected

- GRP-002: user already has groups: group list shown (the empty state applies only to a user with no groups)
- GRP-003: Members tab: 'Members, 1' (count 1); the docs' 'About' section does not exist in v1.4.0
- GRP-004: tabs seen: Invite | Upload | Add Members | 'Add Contact' (singular; the release note says 'Add Contacts')
- GRP-005: invited divya.reddy.1004195243@yopmail.com; pending invites before: 

## Messages observed (review wording — also in message-catalog.md)

- GRP-001 | after: a pop-up appeared | "Success / Group created successfully!" (dialog)
- GRP-005 | after: sent invitation to 'divya.reddy.1004195243@yopmail.com' | "Enter email address..." (on-screen)

## Controls found on screen that no document or locator map mentions (review - new features?)

- GRP-001 on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'group form is shown': **Cancel** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'group form is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-001 on 'Group Details opens after saving': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-003 on 'Group Details is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-004 on 'Add Members screen': **, Home** - listed only (could change data) - test manually or add a scenario

# Triage — run-20261004-213711

alumnye | android | module `groups`

| Metric | Count |
|---|---|
| total | 4 |
| passed | 0 |
| passed zero ai | 0 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 4 |
| error | 0 |
| blocked | 0 |
| skipped | 0 |
| ai calls | 4 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | GRP-012 | Positive | Bulk upload: valid .xlsx and .csv files (picked from local storage) reach the preview without errors and import | self-heal | likely-bug: 'anchor_home_marker' (Anchor Home is open) is missing from the screen — likely functionality break. AI: Current screen shows an 'Exit App' confirmation dialog; expected 'Anchor Home' screen with 'New Group' or 'You don't have any groups' elements is completely absent. | reports/results/alumnye/run-20261004-213711/GRP-012_FAILED.png |
| FAILED | GRP-013 | Negative | Bulk upload flags invalid files and rows (picked from local storage): bad e-mail, missing data, duplicates, wrong columns, empty, wrong format | none | likely-bug: 'landing_sign_in' (Landing screen: 'Sign in' (existing user)) is missing from the screen — likely functionality break. AI: An exit confirmation dialog is displayed instead of the landing screen; the 'Sign in' button is not present on the current screen. | reports/results/alumnye/run-20261004-213711/GRP-013_FAILED.png |
| FAILED | GRP-014 | Positive | Members tab: the count equals the accepted-members name list; invitees sit under Pending Acceptance, not in the count | none | likely-bug: 'landing_sign_in' (Landing screen: 'Sign in' (existing user)) is missing from the screen — likely functionality break. AI: The landing screen sign-in button is absent; an exit confirmation dialog is shown instead, indicating either a navigation defect or premature dialog appearance. | reports/results/alumnye/run-20261004-213711/GRP-014_FAILED.png |
| FAILED | GRP-015 | Positive | Pending Acceptance members each have a Remind button; accepted members do not | none | likely-bug: 'landing_sign_in' (Landing screen: 'Sign in' (existing user)) is missing from the screen — likely functionality break. AI: Landing screen not displayed; an exit confirmation dialog is shown instead of Sign in/Google/Create account options. | reports/results/alumnye/run-20261004-213711/GRP-015_FAILED.png |

## UI adaptations to confirm (never silent)

- GRP-012: `anchor_home_marker` -> `text:New Group` via heal — label 'New Group' ~ ['New Group', "You don't have any groups"] (score 1.00)

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- GRP-012: role_anchor -> ViewGroup at x857,y186 173x58 | add_member_entry -> ViewGroup at x53,y648 479x97

## Flow variants the runner detected

- GRP-012: self-heal for 'anchor_home_marker' used text:New Group for this run only (not saved: it also describes 'new_group_button')

## Regression guard - things that changed under scenarios that had PASSED

- shared runner code changed since the last baseline: app.py, flows.py, testdata.py (every passed scenario that uses it must be re-verified)

## Where the time went (seconds / calls; the rest is waiting, typing and sleeps)

| Scenario | Total s | element lookups | page reads | adb |
|---|---|---|---|---|
| GRP-012 | 470.8 | 208.7 (108) | 178.1 (18) | 20.5 (5) |
| GRP-015 | 74.7 | 28.8 (50) | 17.0 (15) | 1.9 (1) |
| GRP-014 | 74.3 | 37.8 (41) | 14.7 (14) | 1.3 (1) |
| GRP-013 | 70.1 | 27.9 (94) | 10.2 (20) | 1.0 (1) |

## Controls found on screen that no document or locator map mentions (review - new features?)

- GRP-012 on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-012 on 'Group Details is shown': **, Home** - listed only (could change data) - test manually or add a scenario

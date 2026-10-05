# Triage — run-20261004-191224

alumnye | android | module `groups`

> **RUN STOPPED:** Stopped by user (Ctrl+C).

| Metric | Count |
|---|---|
| total | 3 |
| passed | 1 |
| passed zero ai | 1 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 2 |
| error | 0 |
| blocked | 0 |
| skipped | 0 |
| ai calls | 2 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| FAILED | GRP-002 | Positive | Anchor creates a group and lands on its Group Details | none | likely-bug: 'group_details_marker' (Group Details is open) is missing from the screen — likely functionality break. AI: Group Details screen with expected labels 'Add Event' and 'Add Member' is not present; a success confirmation dialog is shown instead, indicating the app did not navigate to the expected screen after saving. | reports/results/alumnye/run-20261004-191224/GRP-002_FAILED.png |
| FAILED | GRP-003 | Positive | Group Details shows About, member count and the Add Event button | none | likely-bug: 'landing_sign_in' (Landing screen: 'Sign in' (existing user)) is missing from the screen — likely functionality break. AI: The landing screen with Sign in/Google/Create account is absent; instead, a success confirmation dialog for group creation is displayed, indicating the app is in an unexpected state. | reports/results/alumnye/run-20261004-191224/GRP-003_FAILED.png |
| PASSED | GRP-001 | Positive | Anchor Home shows the welcome empty state when the user has no groups | none |  | reports/results/alumnye/run-20261004-191224/GRP-001_PASSED.png |

## What the failed scenarios actually tapped (last taps) - a wrong element shows up here

- GRP-002: role_anchor -> ViewGroup at x857,y186 173x58 | new_group_button -> ViewGroup at x696,y447 321x99 | save_group_button -> ViewGroup at x63,y1446 954x116

## Controls found on screen that no document or locator map mentions (review - new features?)

- GRP-001 on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario
- GRP-002 on 'group form is shown': **Cancel** - listed only (could change data) - test manually or add a scenario
- GRP-002 on 'group form is shown': **, Home** - listed only (could change data) - test manually or add a scenario

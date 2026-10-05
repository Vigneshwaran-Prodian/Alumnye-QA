# Triage — run-20261004-191613

alumnye | android | module `groups`

> **RUN STOPPED:** Stopped by user (Ctrl+C).

| Metric | Count |
|---|---|
| total | 1 |
| passed | 0 |
| passed zero ai | 0 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 0 |
| error | 0 |
| blocked | 1 |
| skipped | 0 |
| ai calls | 0 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| BLOCKED | GRP-001 | Positive | Anchor Home shows the welcome empty state when the user has no groups | none | prerequisite: this user already has groups - the empty state needs a fresh user | reports/results/alumnye/run-20261004-191613/GRP-001_BLOCKED.png |

## Controls found on screen that no document or locator map mentions (review - new features?)

- GRP-001 on 'Anchor Home is shown': **, Home** - listed only (could change data) - test manually or add a scenario

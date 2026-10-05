# Triage — run-20261004-190500

alumnye | android | module `groups`

| Metric | Count |
|---|---|
| total | 15 |
| passed | 0 |
| passed zero ai | 0 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 0 |
| error | 15 |
| blocked | 0 |
| skipped | 0 |
| ai calls | 0 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| ERROR | GRP-001 | Positive | Anchor Home shows the welcome empty state when the user has no groups | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-001_ERROR.png |
| ERROR | GRP-002 | Positive | Anchor creates a group and lands on its Group Details | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-002_ERROR.png |
| ERROR | GRP-003 | Positive | Group Details shows About, member count and the Add Event button | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-003_ERROR.png |
| ERROR | GRP-004 | Positive | Add Members offers the invitation methods (Invite, Upload, Add Members, Add Contacts) | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-004_ERROR.png |
| ERROR | GRP-005 | Positive | Anchor invites a member by email and gets a success confirmation | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-005_ERROR.png |
| ERROR | GRP-006 | Negative | Invite rejects an invalid email format | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-006_ERROR.png |
| ERROR | GRP-007 | Negative | Anchor cannot invite their own email address | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-007_ERROR.png |
| ERROR | GRP-008 | Negative | Inviting the same email twice is blocked | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-008_ERROR.png |
| ERROR | GRP-009 | Negative | Create Group is blocked when the name is empty | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-009_ERROR.png |
| ERROR | GRP-010 | Negative | A duplicate group name is rejected | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-010_ERROR.png |
| ERROR | GRP-011 | Edge | Group description is limited to 200 characters with a live counter | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-011_ERROR.png |
| ERROR | GRP-012 | Positive | Bulk upload of a valid file goes through Bulk Preview and imports the members | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-012_ERROR.png |
| ERROR | GRP-013 | Negative | Bulk upload flags invalid rows with validation errors | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-013_ERROR.png |
| ERROR | GRP-014 | Positive | Member count opens the cohort members list showing the Anchor with their member code | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-014_ERROR.png |
| ERROR | GRP-015 | Positive | Pending invitation offers a Remind option that responds | none | script: KeyError: "locator key 'home_marker' not in Group-Elements.md" | reports/results/alumnye/run-20261004-190500/GRP-015_ERROR.png |

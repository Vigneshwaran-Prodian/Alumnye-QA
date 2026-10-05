# Triage — run-20261003-182335

alumnye | android | module `auth`

| Metric | Count |
|---|---|
| total | 1 |
| passed | 0 |
| passed zero ai | 0 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 0 |
| error | 1 |
| blocked | 0 |
| skipped | 0 |
| ai calls | 0 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| ERROR | AUTH-004 | Positive | New user registers with yopmail email + OTP (Terms handled adaptively) | none | script: TypeError: argument of type 'NoneType' is not iterable | reports/results/alumnye/run-20261003-182335/AUTH-004_ERROR.png |

## Entry paths the runner navigated (Splash -> ... -> target)

- AUTH-004: Splash -> Skip

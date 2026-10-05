# Test Case Generation Template

Tag this file at the start of every module's test-case generation (person or AI). Before starting, read `summary.md`, `task_log.md`, and the module's Plan file.

## Module header (state at top of every `<Module>-TestCases.md`)
- Module:
- Criticality: critical / normal / light — and why (blocks core flow, touches money, touches identity?)

## Process
1. Check `scenario-catalog.md` — reuse before create. Never invent an ID without checking.
2. Ground every step in the live screen (screenshot / accessibility tree / DOM). Reference screenshots in `knowledge/doc/` are an optional cross-check.
   2b. Read `locator-maps/<Module>-Elements.md` first; only inspect screens not yet mapped. Record new elements there (name, how to find it, what it does).
3. Fill the 11-dimension check in `coverage-model.md` per scenario.
4. Write `testcases/<Module>-TestCases.md` in the fixed format below.
5. One script per scenario ID at `source/<platform>/<product>/specs/<module>/`. Never bundle.
6. Write `testcases/<Module>-UserScenarios.md` — plain-language "Approach 1, 2, 3..." journeys for non-technical reviewers.
7. Update `scenario-catalog.md`, `<Module>-Plan.md`, `summary.md`, `task_log.md`.

## Fixed test-case format
```
### TC-<ID> — <title>
- Priority:
- Type: Positive | Negative | Edge
- Preconditions:
- Test Data:
- Steps:
  1. ...
- Expected Result:
- Automation script path:
- Notes:
```

## Hard rules
- No large speculative batches; scope strictly to what the catalog / CR delta calls for.
- Every scenario type (Positive/Negative/Edge) gets a report entry and evidence.

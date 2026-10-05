# Project Summary

_Read this first, every session. Update at the end of every session._

**Last updated:** 2026-10-04 (module 2 generated; journeys + discovery added)
**Target release:** Alumnye v1.4.0 (final). v1.5 items (4-Sep-26 MoM: login redesign, biometric, dual-identifier rule) are out of scope.
**Platform:** Mobile (Appium + Python), Android (emulator-5554, app `app.alumnye.com` v1.4.0 installed). iOS scripts exist but need a Mac / device farm (`config.json` udid + bundle_id).

## AI backend
Recovery AI is **Claude** (Claude Code CLI headless, logged-in account, model `haiku`, no API key) — set in `config.json` `ai.backend` (`claude` | `qwen`). Verified: a test call picked 'Log out' for a 'Sign out' step in ~9 s. Used only when deterministic recovery cannot proceed; passing runs use none. `--model` overrides the active backend's model.

## Module 2 — BF2 Groups, members & invitations (generated, NOT yet run)
14 scenarios GRP-001..014 (create group, group details, add-member options, invite by email + 3 negatives, create-group negatives, 200-char description, bulk upload valid/invalid, members list). Assets: `Group-TestCases.md`, `Group-UserScenarios.md`, `locator-maps/Group-Elements.md` (docs-draft), `module-plans/Group-Plan.md`, scripts `specs/groups/`, flows in `flows.py`, CSV/group test data in `testdata.py`. Deferred to the end-to-end journey layer: accepting an invite (2nd user), invite-link routing, multi-anchor, import from another group. Run: `.lumnye-qa run --product=alumnye --platform=android --module=groups`.

## Module 3 — BF3 Events (generated, NOT yet run)
30 scenarios EVT-001..030: empty state, form layout, category list (7), exact tile sets per category (Reunion 8 / Sports 5 / shared 4 - one script per category), listing/grouping/ordering, tile navigation, Poll tile -> list-first, negative (empty/space title, no category, cancel), edge (length limits, special characters, duplicate title), form reset, edit title/category, restart persistence (RULE-007), reachability from Home/My Group. Assets: `Event-TestCases.md` (concrete, with the tile tables), `Event-UserScenarios.md`, `locator-maps/Event-Elements.md` (docs-draft), `module-plans/Event-Plan.md`, scripts `specs/events/`, flows in `flows.py` (create_event, read_tiles, check_tiles, edit_event, read_listing ...), `data/test_events.json`. Chain Auth -> Group -> Members -> Event is enforced by `flows.group_ready` / `new_group_ready` (signs in, finds or creates the group, invites 2 test members if it has none). Owner decisions 2026-10-04: v1.4 shared tile set confirmed, category MANDATORY (EVT-021 expects a refusal), no title limit and duplicate titles allowed (owner's belief - EVT-023/025 expect acceptance and report otherwise). Member-side checks are queued in `journey-catalog.md`. Run: `.\alumnye-qa run --product=alumnye --platform=android --module=events` (depends on auth + groups: signs in first); everything in one go: `--module=auth,groups,events`.

## Intro slides (AUTH-018..020) + sign-in precondition — built, NOT yet run
- Part of the Auth module (`specs/auth/`): AUTH-018 Skip -> landing; AUTH-019 Next / Get Started presses until landing (adaptive: `App.intro_state` reads the live screen and picks the control); AUTH-020 UI + wording per slide (screenshot per slide, wording recorded in `data/splash-wordings.json`, owner approves with `"approved": true`) + v1.3.2 landing checks. Test cases: TC-AUTH-018..020 in `Auth-TestCases.md`; locators `splash_*` in `Auth-Elements.md`.
- Precondition: every module after Auth starts with `flows.precondition_signed_in` (reuse session, else sign in with the registered user, else register); the route is written to the report. These scenarios clear app data (fresh intro), so the next module signs in again (one OTP).
- Full flow: `--module=auth,groups`.

## Journeys (2 emulators, parallel) + feature discovery — built, NOT yet run
- `specs/journeys/` JNY-001..008 (positive, negative, edge; list in `implementation/plans/journey-catalog.md`; rule: RULES.md section 7 - journeys span ALL modules/products, built up as modules are generated); plus GRP-015 (Remind on a pending invite, an option the docs do not mention). Run: `.lumnye-qa run --product=alumnye --platform=android --module=journeys`.
- Anchor = emulator-5554 (Pixel 6), Member = emulator-5556 (Pixel 8, v1.4.0 freshly installed 2026-10-04); set in `config.json` `android.devices`. Each device runs in its own thread (`journey.py`), hand-over via named checkpoints (`Sync`), log lines prefixed [anchor]/[member]. Member account is registered once (`data/journey_accounts.json`), then the session is reused. OTP prompts are serialised (one question at a time).
- Member finds the invitation by exploring (Home, My Group, other tabs); if it is not in the app the tester is asked for the e-mail invitation link (opened on the member device via adb). Locators in `Journey-Elements.md` are docs-draft.
- Discovery: every screen the runner reaches is scanned for tappable controls no locator map mentions; harmless ones (Remind, Resend, View, Filter ...) are tapped via `probe_safe` and the result recorded, destructive ones (delete, remove, cancel, sign out ...) are only listed. Output: triage section + `implementation/plans/discovered-features.md`.

## Current state — BF1 Auth is built and run on a real v1.4.0 build
Latest results (full run `run-20261003-232257`, then re-run of the fixed ones `run-20261004-001220`):

| Status | Scenarios |
|---|---|
| PASSED (14) | AUTH-001, 002, 004, 006, 007, 008, 009, 010, 011, 012, 013, 014, 015, 017 |
| FAILED — product defect (1) | AUTH-005 Google sign-in: Google shows "Access blocked: Authorization Error / Custom scheme URIs are not allowed for 'WEB' client type / Error 400: invalid_request" — OAuth client misconfigured (owner confirmed). Stays in the suite until fixed. |
| SKIPPED — out of scope (1) | AUTH-003 mobile-number registration (owner: email scenarios only for now) |

Passing runs used **zero AI calls**. Message wording observed in real runs is in `implementation/plans/message-catalog.md` (e.g. "Invalid OTP", "A new code has been sent").

## How to run (project root, PowerShell)
```
.\alumnye-qa doctor
.\alumnye-qa list --module=auth
.\alumnye-qa run --product=alumnye --platform=android --module=auth
.\alumnye-qa run --product=alumnye --platform=android --module=auth --scenario=AUTH-006,AUTH-008
.\alumnye-qa run --product=alumnye --platform=android --module=groups        # module 2 (not yet run)
```
Flags: `--no-ai` (turn the AI step off), `--model=<model>` (for the active AI backend), `--type=negative`. OTP is typed at the prompt (yopmail inbox URL is printed; ~2 min timer); a common OTP can be set via `ALUMNYE_OTP` / `config.json common_otp` if the backend ever accepts one (not needed now). Output: `executions/<run>/triage.md` (failures first), `reports/results/alumnye/<run>/` (screenshot + hierarchy per scenario).

## What is built
- **Docs/test assets (BF1 Auth):** `implementation/plans/testcases/Auth-TestCases.md` (16 TCs), `Auth-UserScenarios.md`, `scenario-catalog.md`, `coverage-model.md`, `module-plans/Auth-Plan.md`, `locator-maps/Auth-Elements.md` (now mostly *seen on device*; sign-out screen still docs-draft), `message-catalog.md`.
- **Scripts:** `source/mobile/alumnye/specs/auth/` — one file per scenario ID.
- **Runner** `source/mobile/alumnye/alumnye_qa/`: `app.py` (element API, recovery, navigation), `locators.py` (case-insensitive strategies, `btnx` exact buttons), `healer.py` (deterministic self-heal), `ai.py` (AI backends: Claude CLI default, Qwen optional) + `qwen.py` (recovery prompts), `formfill.py` (smart profile form filling), `terms.py` (tick Terms checkbox, pixel-verified), `flows.py`, `testdata.py`, `session.py` (Appium session with retries/cleanup), `runner.py` (run loop, reports), `cli.py`.

## How the runner behaves (tiers)
1. Cached locators (no AI). 2. Deterministic self-heal on the live screen (moved/renamed). 3. The AI (Claude by default; Qwen optional) only when stuck; its answers are validated (label must resemble the wanted element; disabled/filled targets rejected). 4. Stop with a plain reason. A failed scenario never stops the run; a dead session is reopened; session start retries 3x with stale-server cleanup.
Built-in behaviours: smart entry navigation (Splash → Skip → landing, `reach_landing/sign_in/create_account`); keyboard handled centrally (adb `mInputShown`, closed before taps); disabled buttons auto-recovered (`_unblock`: tick consent checkbox → fill required fields → bounded Qwen); `explore_for` finds items by exploring (this screen → My Account → scroll → other tabs → heal → Qwen); soft checks (a scenario verifies several things and still continues); every tap records what it really hit; triage lists adaptations, entry paths, notes and last taps.

## Real screens seen on device (v1.4.0)
Landing (Sign in / Sign in with Google / OR / Create account; intro slide with Skip before it) → Create Account step 1 (Email | Mobile tabs, Continue disabled until valid) → Verify identity step 2 of 3 (six OTP boxes, icon-only Terms checkbox, "Verify & join Alumnye" disabled until OTP + checkbox, "Resend code (m:ss)" ~2:00 countdown, "Wrong email? Go back") → Complete Your Profile step 3 of 3 (First/Last name*, Member ID auto e.g. AN1 below last name, Mobile*, Email pre-filled/disabled, Continue) → Home ("Welcome, <name>", MEMBER/ANCHOR toggle, card "Complete Your Profile Defaults", bottom nav Home / My Group / My Account). Sign out lives under **My Account**.

## Decisions (owner)
v1.4 final; v1.5 out; email scenarios only (mobile skipped); yopmail test emails; OTP typed by tester; Google account pre-signed on emulator; no Terms/Privacy link clicking or Terms scenarios; Apple button is iOS-only; minimal human/AI intervention is the core product idea; AI = Claude (logged-in Claude Code account; changed from local Qwen on 2026-10-04), used on failure only, execution never done by AI; document-generator idea on hold. Details: `knowledge/discussions/2026-10-01-scope-and-test-approach-decisions.md`.

## Regression rules - problems we hit once and must never hit again (product-grade consistency)
A scenario that has PASSED is a baseline. Changing it, its locators or the shared runner code needs a recorded reason; the runner now enforces this (`baseline.py`, `implementation/plans/passed-baseline.json`, `alumnye-qa baseline`). Each run prints a **REGRESSION GUARD** block and the triage lists **REGRESSIONS** (passed before, fails now) with what changed.

| # | What went wrong (date) | Root cause | Permanent rule / safeguard |
|---|---|---|---|
| 1 | GRP-005 (passed) failed after later work; it tapped the Members tab and never reached the invite form (2026-10-04) | A self-heal run while the "Group created successfully" pop-up covered the screen saved `text:MEMBER` as the first locator of `group_details_marker`. That label is the MEMBER role toggle, so the marker matched on any screen. A sloppy fallback `btn:Members` in `add_member_entry` then hit the Members count tab | (a) A healed / AI-learned locator is NOT saved if its label already belongs to another key (`conflicts`); it is used for that run only and reported. (b) Fallback strategies must be specific (`btn:Add Member`), never a word that is also another control. (c) Poisoned map rows were repaired from device evidence |
| 2 | Shared code changed and passed scenarios silently broke | No record of what a passed scenario depended on | Baseline fingerprints: script hash, locators used, shared runner files. Drift is announced before the run; regressions are called out after it. Approve an intended change with `alumnye-qa baseline --accept=ID --reason="CR/defect"` |
| 3 | "Group created successfully!" OK was tapped late (about 8 s) or not at all | The pop-up was only handled after the full element wait, and heal/AI acted on the screen under the pop-up | The element wait now runs in 1.5 s slices and dismisses an acknowledgement pop-up in between. Decision buttons (Yes/Confirm/Delete/Accept/Reject) are never auto-tapped |
| 4 | An AI "clear the overlay" last resort tapped the MEMBER toggle and Back | AI guessed on a screen it did not understand | Removed. Unknown pop-ups stop the step with a plain reason; AI is used only to locate a missing element, answers are label-validated |
| 5 | Validation message "not captured" (GRP-006) | Banner appears at the top, may already be up before the action, same text each time | Message-like text counts even if already visible; the previous banner is waited out before the next action; checks use the captured text (`app.last_msgs`) |
| 6 | Template download left the app and the run lost focus (GRP-012) | Nothing checked which app was in front | `return_to_app` after the download and whenever an element is missing |
| 7 | Locators matched TABS instead of the buttons (Upload / Add Members tabs) | Over-broad `btn:` strategies in the map | Strategies are reviewed against the real hierarchy; Group map rows now marked "seen on device" |
| 8 | Stale-element crash when tapping the group card (GRP-007) | The card re-rendered between find and click | Re-find and retry the click |

| 9 | Upload scenarios "kept navigating here and there" (GRP-012/013, 2026-10-04) | After a file was picked the runner pressed BACK while the picker was still closing (cancelling the upload); reset loops pressed BACK again; the template download goes to Chrome and the "new file" test missed an older copy | Wait for the app to return (`wait_foreground`), leave a preview with its own Cancel button, use file timestamps for downloads. BACK is used only to leave a picker with nothing to choose |
| 10 | GRP-014 only checked for member codes that do not exist (2026-10-04) | The Members list shows names and roles under a count, with a PENDING ACCEPTANCE section | The count is verified against the accepted-names list and the invitees against the Pending section (RULES 7c) |
| 11 | Expectations from drafts disagreed with the app (missing e-mail) | The app only requires Email OR Phone | Expectations follow the enforced rule; differences recorded (RULES 7c.4) |
| 12 | Upload picked files from Google Drive instead of the device (GRP-012/013) | The Android picker opens on whichever root it used last (here Drive) | The runner pushes files to the device's own Downloads, opens the roots drawer and chooses Downloads when the picker shows Drive; picker screens are saved as evidence when a file cannot be found; the preview is checked to list THIS file's rows (RULES 7c) |
| 13 | GRP-015 wandered to My Account (2026-10-04) | The old script used explore_for, which also opens the other bottom tabs, to find Remind | Remind lives on the Members tab (same screen as GRP-014); scripts open it directly, never explore other tabs; probe_safe removed from GRP-014/015 (discovery only lists) |
| 14 | A count of 1 proved nothing about the count (GRP-014) | The Anchor is also a member; the count only changes when someone accepts | Single-device test verifies count == accepted-names list; the CHANGE is verified in journeys (JNY-001/002/003/005: Anchor reads count + names + Pending before, member decides, Anchor reads again) |
| 15 | 'Exit App' dialog took the whole run down (run-20261004-213711: GRP-012 470 s, GRP-013..015 failed at 'landing_sign_in') | A BACK press on Home opens 'Exit App'; the dialog hides the bottom bar, so the runner decided it was signed out and went looking for the landing screen. The AI then called it a 'likely bug' | back() never presses BACK on Home (new key home_welcome: the Home greeting, unlike home_marker which also matches the bottom bar on every screen); an 'Exit App' dialog is always answered with Cancel, never Exit; ensure_logged_in cancels it first. Rule: a 'likely-bug' verdict from the AI is only trusted after known pop-ups were cleared |
| 16 | Upload scenario took 470 s (2026-10-04) | Full-screen reads (page source) take ~10 s each on the 200-row preview; 18 reads + 108 lookups | Upload/preview checks use a few targeted lookups, never full reads (RULES 7c: heavy screens are read with targeted queries) |
| 17 | Re-imported test members collided with earlier runs (GRP-012/013) | Fixed file names / e-mails were reused every run | A NEW set of files is generated for every run (e-mails and phones carry a run stamp) under data/upload-files/<scenario>/<stamp>/ and kept on disk; the emails of each imported file are recorded for the Members-list checks. Uploads always end with 'Confirm Import'; validations are read in the preview popup AND the banner at the top |
| 18 | AUTH-019 saw no Next button and AUTH-020 'passed' after reading 1 slide (2026-10-04) | The button's label is 'Next, →' (icon in the label); my check compared the whole label with 'next'. The wording baseline was recorded from 1 slide | Controls are matched on the words before the comma and symbol-only text is ignored; the wrongly recorded baseline was deleted. Rule: a screen-reading helper is tested on a saved real hierarchy of EVERY control variant before it is trusted |
| 19 | Member registration stuck on 'Phone number is already registered to another user' (journey run 20261004-234648); the AI then wasted 3 turns on an already-filled field | The filler typed a random number that was already taken and had no way to read the validation message | Validation repair (formfill.repair_validation): read the error under the field, map it to the nearest ENABLED input, and enter a new value - a taken phone number is handled directly with a fresh 10-digit mobile; any other rejected value is interpreted by the AI (qwen.ask_fix) which suggests a new one; bounded (5 values per field); every correction is written to the report. Also: an acknowledgement dialog is now waited out until it is really gone (the 'Group created' OK was tapped twice) |
| 20 | Pixel 8 profile step 3 of 3: first/last name filled, mobile left empty, then the AI was asked every time (journeys 20261004-234648) | NOT a missing script: the Auth form filler (formfill) is the code that runs. Its fill loop made ONE pass and swallowed any error, so when the mobile tap failed once (timing on the second device) the field was silently skipped | fill_inputs now makes up to 4 passes, retries a field that is still empty after the keyboard is closed and the screen re-read, and writes every failure to the report; the typed mobile is kept on the person record. Rule: shared helpers never swallow an error silently - they retry and report |
| 21 | Machine overloaded (two emulators + Appium + AI + IDE): Pixel 6 showed "Alumnye isn't responding", element lookups timed out, the form filler could not find the mobile field, and the AI called the Group Details failure a 'likely bug' (run-20261005-000620) | Position-based lookup `(//EditText)[n]` timed out after 1.5 s on a slow device; the ANR dialog covered the app | Fields are found by what they are (hint / visible text) with a 2.5 s window, and if no element comes back the field is tapped by its on-screen position and typed with adb; the Android ANR dialog is always answered with Wait (never Close) before any 'not found' verdict; load advice written in the README |

**Working agreement:** do not edit a PASSED scenario or its locator rows without a reason logged here / in task_log.md (a defect, CR, or a confirmed app change). Fix shared code only with the guard output reviewed, and re-run every passed scenario that depends on it.

## Lessons / honest limits
- Most failures so far were **my locator/logic mistakes** found by reading the evidence the runner saved (ambiguous locators, wrong element matched, XPath engine returning first-in-document-order, keyboard swallowing taps). They were fixed between runs, not auto-fixed at runtime. Runtime self-heal handles moved/renamed elements only.
- The small local model (`qwen3:4b`) was too weak to find new locators (it once wrote wrong ones into the map — reverted, now guarded); that is why Claude is now the default AI. Claude calls use the logged-in account's plan usage (no API bill) and take several seconds, so they stay failure-only. Consider an approval step before AI-learned locators are saved.
- Locator descriptions in the map must not contain `|`.

## Open items / next
- Re-run the full Auth module once more to confirm a clean 14/15 (+1 known defect, 1 skipped); capture the My Account / Sign out screen into the locator map.
- Optional: approval step for AI-learned locators; iOS execution environment.
- BF2 Groups: run it, then fix/learn locators from the evidence; journey layer (E2E: sign in → create group → add member → accept invite) planned after BF2; open decisions: invite link pasted by tester vs API mailbox; one emulator vs two.
- Baseline: BF3 Event & category tiles → BF4 Poll (+CostGPT) → BF5 RSVP & payment → BF6 Itinerary/travel/library → BF7 Profile (manual + AI) → BF8 Golf.

## Product vision (owner) and status
Core idea: a simple, intelligent product that understands a project / new CR by itself, creates scripts and executes them, and brings AI in only on failure; minimal human and AI intervention. **Today** the product executes, self-heals moved/renamed items, navigates/fills forms, and calls AI on failure; the understanding + script generation was done by Claude in the session. **Document/CR-to-scenario generator: ON HOLD (owner, 2026-10-04)** — planned design when resumed: declarative YAML scenarios + generic interpreter, `--discover` app crawler building locator maps, CR delta against scenario-catalog, AI backend = Claude CLI.

## Open doc questions (flag, don't guess)
- Member AI profile enablement; poll-answer visibility after submission; exact error-message wording (see message-catalog.md); OTP timer observed ~2:00 (docs silent); divider shows "OR" upper-case vs "or" in v1.3.2 notes (matching is case-insensitive — confirm intent).

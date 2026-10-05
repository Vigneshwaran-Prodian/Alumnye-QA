# Alumnye mobile automation (Appium, Python)

One CLI for everything (from the project root):

```
alumnye-qa doctor                                              # check emulator, app, Appium, Qwen
alumnye-qa list --module=auth                                  # list scenarios
alumnye-qa run --product=alumnye --platform=android --module=auth            # whole module
alumnye-qa run --product=alumnye --platform=android --module=auth --scenario=AUTH-004   # one script
alumnye-qa run --product=alumnye --platform=android --module=auth --scenario=AUTH-010,AUTH-011
alumnye-qa run --product=alumnye --platform=android --module=auth --type=negative
```
Flags: `--no-ai` (disable Qwen fallback), `--model=qwen3:8b` (use a bigger local Qwen).
iOS: set `udid` + `bundle_id` in `config.json` and run Appium on a Mac / device farm, then `--platform=ios`.

## How a run behaves
1. Script runs with cached locators (`implementation/plans/locator-maps/<Module>-Elements.md`) — zero AI.
2. Element missing -> deterministic self-heal on the live page source (moved / renamed) -> continue, logged.
3. Still missing -> local Qwen (Ollama) is asked once; it can point at the element or call it a likely bug.
4. A failed scenario never stops the run. Appium crash -> session reopened. Unrecoverable -> stops with a plain reason.

Outputs: `executions/<run>/triage.md` (failures first), `execution_runs.json`, evidence in `reports/results/alumnye/<run>/`.
Manual input: OTP is typed at the prompt; or set a common OTP (`set ALUMNYE_OTP=123456` or `common_otp` in config.json) if the backend accepts one for test emails; mobile number via prompt or `set ALUMNYE_TEST_MOBILE=...`.

## Running two emulators (journeys) on one machine
Two Android emulators + Appium + the AI CLI + an IDE is heavy. If an emulator shows "app isn't responding", lookups time out and scenarios fail for reasons that are not product bugs. Before a journey run:
- Close other heavy applications (browsers with many tabs, the IDE's extra windows); keep only the terminal.
- Give each emulator 2 GB RAM / 2 cores (AVD Manager -> Edit -> Advanced), enable hardware graphics, and cold boot both once.
- Start both emulators and wait until Home is shown on each before running; run a few journeys at a time (`--scenario=JNY-001,JNY-002`) instead of all eight.
- The runner answers the Android "isn't responding" dialog with Wait automatically, but sustained overload will still slow every step.

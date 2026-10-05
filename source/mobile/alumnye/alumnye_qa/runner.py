"""Loads scenario scripts, runs them one by one, keeps going after a failure, and writes the
execution record + failures-first triage report + evidence for EVERY scenario (RULES §6)."""
import datetime
import importlib.util
import json
import time
import traceback

from selenium.common.exceptions import WebDriverException

from . import baseline, config
from .app import App, StepFailed
from .locators import MultiMap
from .session import Blocked, Halt, Skipped, ensure_server, open_driver


def load_scenarios(module, wanted=None, types=None, platform="android"):
    folder = config.SPECS_DIR / module
    if not folder.is_dir():
        raise Halt(f"No such module '{module}'. Available: {', '.join(p.name for p in config.SPECS_DIR.iterdir() if p.is_dir() and not p.name.startswith('_'))}")
    found = []
    for f in sorted(folder.glob("*.py")):
        if f.name.startswith("_"):
            continue
        spec = importlib.util.spec_from_file_location(f"specs_{module}_{f.stem}", f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        meta = dict(mod.META, script=str(f.relative_to(config.ROOT)).replace("\\", "/"))
        if wanted and meta["id"] not in wanted:
            continue
        if types and meta["type"].lower() not in types:
            continue
        if platform not in meta.get("platforms", ["android", "ios"]):
            continue
        found.append((meta, mod.run if hasattr(mod, "run") else (mod.anchor, mod.member)))
    if wanted:
        missing = set(wanted) - {m["id"] for m, _ in found}
        if missing:
            raise Halt(f"Scenario id(s) not found for module '{module}' / {platform}: {', '.join(sorted(missing))}")
    return found


def _ai_mode(app):
    tiers = {e["tier"] for e in app.events}
    return "qwen" if "qwen" in tiers else "self-heal" if "heal" in tiers else "none"


def run(args):
    cfg = config.load()
    cfg["ai"]["enabled"] = cfg["ai"]["enabled"] and not args.no_ai
    if args.model:
        cfg["ai"]["claude_model" if cfg["ai"].get("backend", "claude") == "claude" else "model"] = args.model
    modules = [m.strip() for m in args.module.split(",") if m.strip()]
    scenarios = []
    for m in modules:                                           # several modules = one full flow, in the order given, one device session
        scenarios += load_scenarios(m, args.scenario if len(modules) == 1 else None, args.type, args.platform)
    if not scenarios:
        raise Halt("No scenarios matched the filters.")
    if len(modules) > 1:
        if any(m in config.LOCATOR_MULTI for m in modules):
            raise Halt("Journeys use two devices and run on their own: run them as --module=journeys.")
        order = list(config.MODULE_DEPENDS)
        if modules != sorted(modules, key=lambda m: order.index(m) if m in order else 99):
            raise Halt(f"Modules must be listed in dependency order (earlier modules first): {','.join(sorted(modules, key=lambda m: order.index(m) if m in order else 99))}")
        print(f"[run] full flow: {' -> '.join(modules)} ({len(scenarios)} scenarios in one session)")
    args.module = "+".join(modules)
    run_id = datetime.datetime.now().strftime("run-%Y%m%d-%H%M%S")
    ev_dir = config.RESULTS_DIR / run_id
    ev_dir.mkdir(parents=True, exist_ok=True)
    needs = config.MODULE_DEPENDS.get(args.module, [])
    if needs:
        print(f"[run] module '{args.module}' depends on: {', '.join(needs)} (a successful login comes first; it is done automatically if the device is not signed in)")
    if args.module in config.LOCATOR_MULTI:                  # two-device journeys run in parallel
        print(f"[run] {run_id} | {args.product} | {args.platform} | module={args.module} | {len(scenarios)} journey(ies)")
        from . import ai as _ai0
        print(f"[run] AI fallback: {_ai0.label(cfg) if cfg['ai']['enabled'] else 'OFF'}")
        from .journey import run_journeys

        def _reports(rid, a, c, res, halted):
            _write_reports(rid, a, c, res, halted)
            _update_message_catalog(rid, a.module, res)
        return run_journeys(args, cfg, scenarios, run_id, ev_dir, _reports)
    files = []
    for m in modules:
        files += [f for f in config.locator_files(m) if f not in files]
    locmap = MultiMap([config.LOCATOR_DIR / f for f in files])
    drift, fw = baseline.check(scenarios, locmap, args.platform)
    _announce_drift(drift, fw)
    print(f"[run] {run_id} | {args.product} | {args.platform} | module={args.module} | {len(scenarios)} scenario(s)")
    from . import ai as _ai
    print(f"[run] AI fallback: {_ai.label(cfg) if cfg['ai']['enabled'] else 'OFF'}")

    server = ensure_server(cfg["appium_url"])
    results, halted = [], None
    driver = app = None
    try:
        driver = open_driver(cfg, args.platform)
        if cfg["ai"]["enabled"]:
            from . import qwen
            qwen.warm_up(cfg)                       # after the session is up, so it cannot slow the server start
        app = App(driver, args.platform, cfg, locmap, run_id)
        app.launch()
        for meta, fn in scenarios:
            sid = meta["id"]
            print(f"\n=== {sid} — {meta['title']} [{meta['type']}]")
            app.scenario, app.events, app.ai_calls, app.path, app.messages = sid, [], 0, [], []
            app.soft_failures, app.notes, app.taps = [], [], []
            app.timing.clear()
            app.keys_used.clear()
            t0, status, category, message = time.time(), "PASSED", "", ""
            try:
                if meta.get("skip"):
                    raise Skipped(meta["skip"])
                if meta.get("fresh"):
                    app.reset()
                fn(app)
                if app.soft_failures:
                    status, category, message = "FAILED", "assertion", " | ".join(app.soft_failures)
            except Skipped as e:
                status, category, message = "SKIPPED", "out-of-scope", str(e)
            except Blocked as e:
                status, category, message = "BLOCKED", "prerequisite", str(e)
            except StepFailed as e:
                status, category, message = "FAILED", e.category, str(e)
            except WebDriverException as e:
                status, category, message = "ERROR", "driver", str(e).splitlines()[0]
            except Exception as e:
                status, category, message = "ERROR", "script", f"{type(e).__name__}: {e}"
                traceback.print_exc()
            app.capture(str(ev_dir / f"{sid}_{status}"))
            rec = {**{k: meta[k] for k in ("id", "title", "type", "script")}, "status": status, "category": category,
                   "message": message, "seconds": round(time.time() - t0, 1), "ai_mode": _ai_mode(app),
                   "ai_calls": app.ai_calls, "adaptations": app.events, "entry_path": list(app.path), "notes": list(app.notes), "last_taps": app.taps[-4:],
                   "messages": list(app.messages),
                   "discovered": [d for d in app.discovered if d["scenario"] == sid],
                   "timing": {k: [c, round(v, 1)] for k, (c, v) in app.timing.items()},
                   "keys": baseline.strategies_of(locmap, app.keys_used, args.platform),
                   "evidence": f"reports/results/alumnye/{run_id}/{sid}_{status}.png"}
            results.append(rec)
            print(f"    -> {status}{(' (' + category + ')') if category else ''} {message}")
            if status == "ERROR" and category == "driver":  # recover only if the session is really gone
                try:
                    driver.get_window_size()
                    alive = True
                except Exception:
                    alive = False
                if not alive:
                    try:
                        driver.quit()
                    except Exception:
                        pass
                    print("    [recover] driver session lost — reopening")
                    driver = open_driver(cfg, args.platform)
                    app = App(driver, args.platform, cfg, locmap, run_id)
                    app.launch()
    except Halt as e:
        halted = str(e)
    except KeyboardInterrupt:
        halted = "Stopped by user (Ctrl+C)."
    finally:
        try:
            if driver:
                driver.quit()
        except Exception:
            pass
        if server:
            server.terminate()
    guard = (drift, fw)
    _write_reports(run_id, args, cfg, results, halted, guard)
    baseline.record(results, scenarios, None, args.platform, run_id)
    _update_message_catalog(run_id, args.module, results)
    return 1 if halted or any(r["status"] in ("FAILED", "ERROR") for r in results) else 0


def _write_reports(run_id, args, cfg, results, halted, guard=None):
    out = config.EXEC_DIR / run_id
    out.mkdir(parents=True, exist_ok=True)
    count = lambda s: sum(r["status"] == s for r in results)
    passed = [r for r in results if r["status"] == "PASSED"]
    summary = {
        "run_id": run_id, "product": args.product, "platform": args.platform, "module": args.module,
        "total": len(results), "passed": len(passed),
        "passed_zero_ai": sum(r["ai_mode"] == "none" for r in passed),
        "passed_after_self_heal": sum(r["ai_mode"] == "self-heal" for r in passed),
        "passed_after_qwen": sum(r["ai_mode"] == "qwen" for r in passed),
        "failed": count("FAILED"), "error": count("ERROR"), "blocked": count("BLOCKED"), "skipped": count("SKIPPED"),
        "ai_calls": sum(r["ai_calls"] for r in results), "stopped_reason": halted,
    }
    (out / "execution_runs.json").write_text(json.dumps({"summary": summary, "results": results}, indent=2), encoding="utf-8")

    order = {"FAILED": 0, "ERROR": 1, "BLOCKED": 2, "SKIPPED": 3, "PASSED": 4}
    rows = sorted(results, key=lambda r: (order[r["status"]], r["id"]))
    md = [f"# Triage — {run_id}", "",
          f"{args.product} | {args.platform} | module `{args.module}`", ""]
    if halted:
        md += [f"> **RUN STOPPED:** {halted}", ""]
    md += ["| Metric | Count |", "|---|---|"] + [f"| {k.replace('_', ' ')} | {v} |" for k, v in summary.items()
                                                  if k not in ("run_id", "product", "platform", "module", "stopped_reason")]
    md += ["", "## Scenarios (failures first)", "",
           "| Status | ID | Type | Title | AI | Category / message | Evidence |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        msg = f"{r['category']}: {r['message']}".strip(": ").replace("|", "/")
        md.append(f"| {r['status']} | {r['id']} | {r['type']} | {r['title']} | {r['ai_mode']} | {msg} | {r['evidence']} |")
    adapt = [(r["id"], a) for r in results for a in r["adaptations"]]
    if adapt:
        md += ["", "## UI adaptations to confirm (never silent)", ""]
        md += [f"- {i}: `{a['key']}` -> `{a['strategy']}` via {a['tier']} — {a['reason']}" for i, a in adapt]
    paths = [(r["id"], r["entry_path"]) for r in results if r["entry_path"]]
    if paths:
        md += ["", "## Entry paths the runner navigated (Splash -> ... -> target)", ""]
        md += [f"- {i}: " + " -> ".join(["Splash"] + p_) for i, p_ in paths]
    taps = [(r["id"], r["last_taps"]) for r in results if r["last_taps"] and r["status"] in ("FAILED", "ERROR")]
    if taps:
        md += ["", "## What the failed scenarios actually tapped (last taps) - a wrong element shows up here", ""]
        md += [f"- {i}: " + " | ".join(t_) for i, t_ in taps]
    notes = [(r["id"], n) for r in results for n in r["notes"]]
    if notes:
        md += ["", "## Flow variants the runner detected", ""] + [f"- {i}: {n}" for i, n in notes]
    msgs = [(r["id"], m) for r in results for m in r["messages"]]
    if msgs:
        md += ["", "## Messages observed (review wording — also in message-catalog.md)", ""]
        md += [f"- {i} | after: {m['trigger']} | \"{m['text']}\" ({m['where']})" for i, m in msgs]
    if guard:
        drift, fw = guard
        regs = baseline.regressions(results, drift, fw)
        if regs:
            md += ["", "## REGRESSIONS - passed before, failing now (investigate first)", ""]
            md += [f"- **{i}** passed in {run}; since then: " + "; ".join(why) for i, run, why in regs]
        if drift or fw:
            md += ["", "## Regression guard - things that changed under scenarios that had PASSED", ""]
            md += [f"- {i}: " + "; ".join(w) for i, w in drift.items()]
            if fw:
                md.append(f"- shared runner code changed since the last baseline: {', '.join(fw)} (every passed scenario that uses it must be re-verified)")
    slow = [r for r in results if r.get("timing")]
    if slow:
        md += ["", "## Where the time went (seconds / calls; the rest is waiting, typing and sleeps)", "",
               "| Scenario | Total s | element lookups | page reads | adb |", "|---|---|---|---|---|"]
        cell = lambda t, k: f"{t.get(k, [0, 0])[1]} ({t.get(k, [0, 0])[0]})"
        for r in sorted(slow, key=lambda r: -r["seconds"]):
            t = r["timing"]
            md.append(f"| {r['id']} | {r['seconds']} | {round(t.get('find_elements', [0, 0])[1] + t.get('find_element', [0, 0])[1], 1)} ({t.get('find_elements', [0, 0])[0] + t.get('find_element', [0, 0])[0]}) | {cell(t, 'page_source')} | {cell(t, 'adb')} |")
    found = [(r["id"], d) for r in results for d in r.get("discovered", [])]
    if found:
        md += ["", "## Controls found on screen that no document or locator map mentions (review - new features?)", ""]
        md += [f"- {i}{' [' + d['device'] + ']' if d['device'] else ''} on '{d['where']}': **{d['label']}** - "
               + (f"explored: {d['result']}" if d["result"] else ("safe to explore, not yet tapped" if d["safe"] else "listed only (could change data) - test manually or add a scenario"))
               for i, d in found]
        _update_discovered(run_id, found)
    (out / "triage.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print("\n" + "=" * 60)
    print(f"RESULT: {summary['passed']}/{summary['total']} passed "
          f"({summary['passed_zero_ai']} zero-AI, {summary['passed_after_self_heal']} self-healed, "
          f"{summary['passed_after_qwen']} Qwen) | failed {summary['failed']} | error {summary['error']} | blocked {summary['blocked']} | skipped {summary['skipped']}")
    if halted:
        print(f"RUN STOPPED: {halted}")
    print(f"Triage : executions/{run_id}/triage.md")
    print(f"Evidence: reports/results/alumnye/{run_id}/")


CATALOG = config.ROOT / "implementation" / "plans" / "message-catalog.md"
CATALOG_HEAD = """# Message Catalog (observed in real runs)

Every toast / inline error / validation text the app showed after a scripted action, with the scenario and
trigger that caused it. Filled automatically by `alumnye-qa run`; review the wording and fill the last two columns.
Note: "on-screen" rows include any new text after the action — ignore rows that are just the next screen's content.

| Module | Scenario | Trigger (what the user did) | Observed message | Where | Expected wording (fill in) | Wording OK? | First seen |
|---|---|---|---|---|---|---|---|
"""


def _update_message_catalog(run_id, module, results):
    rows = [(r["id"], m) for r in results for m in r["messages"]]
    if not rows:
        return
    text = CATALOG.read_text(encoding="utf-8") if CATALOG.exists() else CATALOG_HEAD
    added = 0
    for sid, m in rows:
        msg = m["text"].replace("|", "/")
        if f"| {sid} | {m['trigger']} | {msg} |" in text:
            continue
        text = text.rstrip("\n") + f"\n| {module} | {sid} | {m['trigger']} | {msg} | {m['where']} |  |  | {run_id} |\n"
        added += 1
    CATALOG.write_text(text, encoding="utf-8")
    print(f"Messages: {added} new observed message(s) -> implementation/plans/message-catalog.md")


DISCOVERED = config.ROOT / "implementation" / "plans" / "discovered-features.md"
DISCOVERED_HEAD = """# Discovered features (seen in the app, absent from the documents / locator maps)

Filled automatically by `alumnye-qa run`. Each row is a control the runner met while executing. "Explored" means the runner
tapped it (harmless controls only) and recorded the result; the rest need a scenario. Turn confirmed ones into test cases
(Group-TestCases.md etc.), then add their locators to the module map so they stop being listed here.

| Screen | Control | Explored result | Scenario that met it | First seen |
|---|---|---|---|---|
"""


def _update_discovered(run_id, found):
    text = DISCOVERED.read_text(encoding="utf-8") if DISCOVERED.exists() else DISCOVERED_HEAD
    for sid, d in found:
        row = f"| {d['where']} | {d['label']} |"
        if row in text:
            continue
        res = (d["result"] or ("not tapped (could change data)" if not d["safe"] else "not yet tapped")).replace("|", "/")
        text = text.rstrip("\n") + f"\n{row} {res} | {sid} | {run_id} |\n"
    DISCOVERED.write_text(text, encoding="utf-8")


def _announce_drift(drift, fw):
    if drift or fw:
        print("[guard] REGRESSION GUARD - changes under scenarios that had PASSED:")
        for sid, w in drift.items():
            for x in w:
                print(f"        {sid}: {x}")
        if fw:
            print(f"        shared runner code changed since the last baseline: {', '.join(fw)}")
        print("        (approve an intended change with: alumnye-qa baseline --accept=<ID> --reason=\"...\")")

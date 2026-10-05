"""Regression guard. A scenario that has PASSED is a baseline: its script, the locators it used and the shared runner code are
fingerprinted. Every later run compares against it and says so plainly when something under a passed scenario changed, and flags
a REGRESSION when a scenario that passed before now fails. Nothing is silently re-baselined by a human edit:
    alumnye-qa baseline --accept=GRP-005 --reason="CR-123 invite screen redesigned"
records an approved change; a passing run re-verifies and refreshes the baseline."""
import datetime
import hashlib
import json

from . import config

FILE = config.ROOT / "implementation" / "plans" / "passed-baseline.json"
SHARED = ("app.py", "flows.py", "locators.py", "healer.py", "terms.py", "formfill.py", "testdata.py")


def _h(path):
    try:
        return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:12]
    except OSError:
        return ""


def framework_fingerprint():
    base = config.PRODUCT_DIR / "alumnye_qa"
    return {f: _h(base / f) for f in SHARED}


def load():
    if FILE.exists():
        return json.loads(FILE.read_text(encoding="utf-8") or "{}")
    return {"scenarios": {}, "framework": {}, "changes": []}


def save(data):
    FILE.parent.mkdir(parents=True, exist_ok=True)
    FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def script_hash(meta):
    return _h(config.ROOT / meta["script"])


def strategies_of(locmap, keys, platform):
    out = {}
    for k in sorted(keys):
        try:
            out[k] = locmap.strategies(k, platform)
        except Exception:
            pass
    return out


def check(scenarios, locmap, platform):
    """Compare the scenarios about to run with their baselines. Returns {scenario_id: [what changed]} and a framework note."""
    data, drift = load(), {}
    for meta, _ in scenarios:
        b = data["scenarios"].get(meta["id"])
        if not b:
            continue
        found = []
        if b.get("script") and script_hash(meta) != b["script"]:
            found.append("SCRIPT changed since it passed")
        for k, strat in b.get("locators", {}).items():
            try:
                now = locmap.strategies(k, platform)
            except Exception:
                found.append(f"locator '{k}' no longer exists")
                continue
            if now != strat:
                found.append(f"LOCATOR '{k}' changed: {' ;; '.join(strat)}  ->  {' ;; '.join(now)}")
        if found:
            drift[meta["id"]] = found
    now_fw = framework_fingerprint()
    old_fw = data.get("framework", {})
    fw = [f for f in SHARED if old_fw.get(f) and old_fw.get(f) != now_fw.get(f)]
    return drift, fw


def record(results, scenarios, locmaps_by_id, platform, run_id):
    """After a run: refresh the baseline of every scenario that PASSED; first-time passes create it."""
    data = load()
    metas = {m["id"]: m for m, _ in scenarios}
    for r in results:
        if r["status"] == "PASSED" and r["id"] in metas and r.get("keys"):
            data["scenarios"][r["id"]] = {"script": script_hash(metas[r["id"]]), "locators": r["keys"],
                                          "passed_run": run_id, "passed_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
    if any(r["status"] == "PASSED" for r in results):
        data["framework"] = framework_fingerprint()
    save(data)


def regressions(results, drift, fw):
    """Scenarios that passed before and fail now, with the likely reason (what changed since the pass)."""
    data, out = load(), []
    for r in results:
        b = data["scenarios"].get(r["id"])
        if b and r["status"] in ("FAILED", "ERROR"):
            why = drift.get(r["id"], []) + ([f"shared runner code changed: {', '.join(fw)}"] if fw else [])
            out.append((r["id"], b["passed_run"], why or ["nothing recorded changed - suspect the app build, device state or data"]))
    return out


def accept(ids, reason):
    """Record an approved change for scenarios and re-fingerprint their scripts (locator/framework drift is re-checked on the next pass)."""
    data = load()
    for sid in ids:
        b = data["scenarios"].get(sid)
        if b:
            b["script"] = ""                 # re-learned on the next passing run
            b["locators"] = {}
        data["changes"].append({"id": sid, "reason": reason, "at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")})
    save(data)

"""Two-device journeys: an Anchor emulator and a Member emulator run their halves of a scenario IN PARALLEL
(one thread each) and hand over at named checkpoints, e.g. the member signs in while the anchor creates the group,
then the anchor invites and the member accepts. Each journey script defines anchor(app, sync) and member(app, sync)."""
import subprocess
import sys
import threading
import time
import traceback

from selenium.common.exceptions import WebDriverException

from . import config
from .app import App, StepFailed
from .locators import MultiMap
from .session import Blocked, Halt, ensure_server, open_driver

WAIT_LIMIT = 1500       # seconds a side waits for the other (covers a human typing an OTP)


class Sync:
    """Checkpoints shared by the two devices. If one side fails, the other stops waiting instead of hanging."""

    def __init__(self):
        self._ev, self.data, self.aborted = {}, {}, None
        self._lock = threading.Lock()

    def _event(self, name):
        with self._lock:
            return self._ev.setdefault(name, threading.Event())

    def set(self, name):
        self._event(name).set()

    def wait(self, name, timeout=WAIT_LIMIT):
        ev, end = self._event(name), time.time() + timeout
        while not ev.wait(1):
            if self.aborted:
                raise Blocked(f"the other device stopped before '{name}': {self.aborted}")
            if time.time() > end:
                raise Blocked(f"timed out waiting for '{name}' from the other device")

    def abort(self, why):
        self.aborted = self.aborted or why


class _TaggedOut:
    """Prefixes every printed line with the device role of the thread that printed it."""

    def __init__(self, real):
        self.real, self.local, self._lock = real, threading.local(), threading.Lock()

    def tag(self, name):
        self.local.name = name

    def write(self, text):
        name = getattr(self.local, "name", "")
        with self._lock:
            if name and text.strip():
                text = "".join(f"[{name:6}] {l}" if l.strip() else l for l in text.splitlines(True))
            self.real.write(text)

    def flush(self):
        self.real.flush()

    def __getattr__(self, a):
        return getattr(self.real, a)


def _devices(cfg):
    named = cfg["android"].get("devices") or {}
    if named.get("anchor") and named.get("member"):
        return named["anchor"], named["member"]
    out = subprocess.run(["adb", "devices"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.splitlines()[1:]
    devs = [l.split()[0] for l in out if l.strip().endswith("device")]
    if len(devs) < 2:
        raise Halt(f"Journeys need two emulators ('adb devices' shows {len(devs)}). Start both, or set android.devices in config.json.")
    return devs[0], devs[1]


def _side(name, fn, app, sync, out, tagger):
    tagger.tag(name)
    try:
        fn(app, sync)
        out[name] = ("PASSED", "", "")
    except Blocked as e:
        out[name] = ("BLOCKED", "prerequisite", str(e))
    except StepFailed as e:
        out[name] = ("FAILED", e.category, str(e))
    except WebDriverException as e:
        out[name] = ("ERROR", "driver", str(e).splitlines()[0])
    except Exception as e:
        traceback.print_exc()
        out[name] = ("ERROR", "script", f"{type(e).__name__}: {e}")
    if out[name][0] != "PASSED":
        sync.abort(f"{name}: {out[name][2][:120]}")


def run_journeys(args, cfg, scenarios, run_id, ev_dir, write_reports):
    from .runner import _ai_mode
    udids = _devices(cfg)
    new_map = lambda: MultiMap([config.LOCATOR_DIR / f for f in config.locator_files(args.module)])
    print(f"[run] two-device journeys: anchor={udids[0]}  member={udids[1]}  (running in parallel)")
    server, results, halted, drivers = ensure_server(cfg["appium_url"]), [], None, []
    tagger = _TaggedOut(sys.stdout)
    sys.stdout = tagger
    try:
        apps = {}
        for slot, (role, udid) in enumerate(zip(("anchor", "member"), udids)):
            tagger.tag(role)
            drv = open_driver(cfg, args.platform, udid=udid, slot=slot)
            drivers.append(drv)
            app = App(drv, args.platform, cfg, new_map(), run_id)
            app.tag = role
            apps[role] = app
        tagger.tag("")
        if cfg["ai"]["enabled"]:
            from . import qwen
            qwen.warm_up(cfg)
        for a in apps.values():
            a.launch()
        for meta, (anchor_fn, member_fn) in scenarios:
            sid = meta["id"]
            print(f"\n=== {sid} — {meta['title']} [{meta['type']}]")
            for a in apps.values():
                a.scenario, a.events, a.ai_calls, a.path, a.messages = sid, [], 0, [], []
                a.soft_failures, a.notes, a.taps = [], [], []
                a.timing.clear()
                a.keys_used.clear()
            sync, out, t0 = Sync(), {}, time.time()
            threads = [threading.Thread(target=_side, args=(role, fn, apps[role], sync, out, tagger), daemon=True)
                       for role, fn in (("anchor", anchor_fn), ("member", member_fn))]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            for role, a in apps.items():
                for sf in a.soft_failures:
                    st, cat, msg = out[role]
                    out[role] = ("FAILED" if st == "PASSED" else st, cat or "assertion", (msg + " | " if msg else "") + sf)
            order = {"ERROR": 0, "FAILED": 1, "BLOCKED": 2, "PASSED": 3}
            status = min((o[0] for o in out.values()), key=lambda s: order[s])
            category = next((o[1] for o in out.values() if o[0] == status and o[1]), "")
            message = " | ".join(f"{r}: {o[2]}" for r, o in out.items() if o[2])
            for role, a in apps.items():
                a.capture(str(ev_dir / f"{sid}_{role}_{status}"))
            modes = {_ai_mode(a) for a in apps.values()}
            rec = {**{k: meta[k] for k in ("id", "title", "type", "script")}, "status": status, "category": category,
                   "message": message, "seconds": round(time.time() - t0, 1),
                   "ai_mode": "qwen" if "qwen" in modes else "self-heal" if "self-heal" in modes else "none",
                   "ai_calls": sum(a.ai_calls for a in apps.values()),
                   "adaptations": [e for a in apps.values() for e in a.events],
                   "entry_path": [f"{r}: {p}" for r, a in apps.items() for p in a.path],
                   "notes": [n if n.startswith(r) else f"{r}: {n}" for r, a in apps.items() for n in a.notes],
                   "last_taps": [f"{r}: {t}" for r, a in apps.items() for t in a.taps[-3:]],
                   "messages": [m for a in apps.values() for m in a.messages],
                   "discovered": [d for a in apps.values() for d in a.discovered if d["scenario"] == sid],
                   "evidence": f"reports/results/alumnye/{run_id}/{sid}_anchor_{status}.png (+ _member_)"}
            results.append(rec)
            print(f"    -> {status}{(' (' + category + ')') if category else ''} {message}")
            for role, a in apps.items():
                try:
                    a.d.get_window_size()
                except Exception:
                    halted = f"the {role} device session was lost during {sid}"
            if halted:
                break
    except Halt as e:
        halted = str(e)
    except KeyboardInterrupt:
        halted = "Stopped by user (Ctrl+C)."
    finally:
        sys.stdout = tagger.real
        for d in drivers:
            try:
                d.quit()
            except Exception:
                pass
        if server:
            server.terminate()
    write_reports(run_id, args, cfg, results, halted)
    return 1 if halted or any(r["status"] in ("FAILED", "ERROR") for r in results) else 0

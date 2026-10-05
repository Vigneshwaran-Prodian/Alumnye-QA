"""alumnye-qa run --product=alumnye --platform=android --module=auth [--scenario=AUTH-003,AUTH-004]"""
import argparse
import shutil
import subprocess
import sys

from . import config, qwen
from .session import Halt


def _list(args):
    from .runner import load_scenarios
    for meta, _ in load_scenarios(args.module, None, None, args.platform):
        print(f"{meta['id']:10} {meta['type']:9} {meta['title']}")
    return 0


def _doctor(args):
    cfg = config.load()
    ok = True

    def line(name, good, detail=""):
        nonlocal ok
        ok &= bool(good)
        print(f"[{'OK ' if good else 'FAIL'}] {name} {detail}")
    line("appium on PATH", shutil.which("appium") or shutil.which("appium.cmd"))
    adb = shutil.which("adb")
    line("adb on PATH", adb)
    if adb:
        devs = [l.split()[0] for l in subprocess.run([adb, "devices"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.splitlines()[1:] if l.strip().endswith("device")]
        line("Android device/emulator", devs, str(devs))
        if devs:
            pk = cfg["android"]["app_package"]
            inst = subprocess.run([adb, "-s", devs[0], "shell", "pm", "list", "packages", pk], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
            line(f"app installed ({pk})", pk in inst, "" if pk in inst else "- install the v1.4.0 build first")
            ver = subprocess.run([adb, "-s", devs[0], "shell", "dumpsys", "package", pk], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
            v = [l.strip() for l in ver.splitlines() if "versionName" in l]
            print(f"       installed version: {v[0] if v else 'unknown'}  (target: 1.4.0)")
    from . import ai as _ai
    line(f"AI backend {_ai.label(cfg)}", qwen.available(cfg), "- needed only for the AI fallback (claude: Claude Code CLI on PATH and logged in)")
    return 0 if ok else 1


def main(argv=None):
    p = argparse.ArgumentParser(prog="alumnye-qa")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="run scenarios")
    r.add_argument("--product", default="alumnye")
    r.add_argument("--platform", choices=["android", "ios"], default="android")
    r.add_argument("--module", required=True, help="e.g. auth")
    r.add_argument("--scenario", type=lambda s: [x.strip().upper() for x in s.split(",")], help="one or more IDs, e.g. AUTH-003,AUTH-004")
    r.add_argument("--type", type=lambda s: [x.strip().lower() for x in s.split(",")], help="Positive,Negative,Edge")
    r.add_argument("--no-ai", action="store_true", help="disable the Qwen fallback")
    r.add_argument("--model", help="override the Qwen model, e.g. qwen3:8b")
    l = sub.add_parser("list", help="list scenarios")
    l.add_argument("--module", required=True)
    l.add_argument("--platform", default="android")
    sub.add_parser("doctor", help="check environment")
    b = sub.add_parser("baseline", help="show the passed-scenario baseline or approve a change")
    b.add_argument("--accept", type=lambda s: [x.strip().upper() for x in s.split(",")], help="scenario id(s) whose change is approved")
    b.add_argument("--reason", help="why the change was made (a CR / defect reference)")
    args = p.parse_args(argv)
    try:
        if args.cmd == "run":
            if args.product != "alumnye":
                raise Halt("Only product 'alumnye' exists in this project.")
            from .runner import run
            return run(args)
        if args.cmd == "baseline":
            from . import baseline
            if args.accept:
                if not args.reason:
                    raise Halt("--reason is required to approve a change (say which CR / defect it is).")
                baseline.accept(args.accept, args.reason)
                print(f"Change approved for {', '.join(args.accept)}: {args.reason}. They are re-baselined on their next passing run.")
            else:
                d = baseline.load()
                print(f"{len(d['scenarios'])} passed scenario(s) under guard; {len(d.get('changes', []))} approved change(s)")
                for sid, b_ in sorted(d["scenarios"].items()):
                    print(f"  {sid}  passed in {b_['passed_run']} ({b_['passed_at']}), {len(b_.get('locators', {}))} locator(s) pinned")
            return 0
        return {"list": _list, "doctor": _doctor}[args.cmd](args)
    except Halt as e:
        print(f"\nRUN STOPPED: {e}")
        return 2


if __name__ == "__main__":
    sys.exit(main())

"""Appium server + device session. Never hangs silently: every failure raises Halt with a plain reason."""
import shutil
import subprocess
import time

import requests
from appium import webdriver


class Halt(Exception):
    """The run cannot continue; message tells a human exactly what is blocking."""


class Skipped(Exception):
    """Scenario deliberately not run (out of the current scope); META['skip'] holds the reason."""


class Blocked(Exception):
    """A scenario cannot run because a prerequisite is missing (not a product failure)."""


def ensure_server(url: str):
    status = url.rstrip("/") + "/status"
    try:
        if requests.get(status, timeout=2).ok:
            return None
    except Exception:
        pass
    exe = shutil.which("appium") or shutil.which("appium.cmd")
    if not exe:
        raise Halt("Appium is not installed or not on PATH. Install with: npm i -g appium && appium driver install uiautomator2")
    print("[run] Appium server not running — starting it ...")
    proc = subprocess.Popen([exe], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(40):
        time.sleep(1)
        try:
            if requests.get(status, timeout=2).ok:
                return proc
        except Exception:
            continue
    proc.terminate()
    raise Halt(f"Appium did not start at {url} within 40s. Start it manually with: appium")


def _adb_udid() -> str:
    adb = shutil.which("adb")
    if not adb:
        raise Halt("adb not found on PATH (Android SDK platform-tools).")
    out = subprocess.run([adb, "devices"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.splitlines()[1:]
    devs = [l.split()[0] for l in out if l.strip().endswith("device")]
    if not devs:
        raise Halt("No Android device/emulator detected. Start the emulator, then check 'adb devices'.")
    return devs[0]


def _adb(udid, *args, timeout=20):
    try:
        out = subprocess.run(["adb", "-s", udid, *args], capture_output=True, timeout=timeout).stdout
        return (out or b"").decode("utf-8", errors="replace")
    except Exception:
        return ""


def _device_ready(udid, wait=90) -> bool:
    """Booted and Android's package service answering (it can be missing right after an emulator restart)."""
    end = time.time() + wait
    while time.time() < end:
        if _adb(udid, "shell", "getprop", "sys.boot_completed").strip() == "1" and "package:" in _adb(udid, "shell", "pm", "path", "android"):
            return True
        time.sleep(3)
    return False


def _cleanup_uiautomator(udid):
    """Remove leftovers of an earlier (e.g. Ctrl+C'd) run that stop a new UiAutomator2 server from starting."""
    for pkg in ("io.appium.uiautomator2.server", "io.appium.uiautomator2.server.test"):
        _adb(udid, "shell", "am", "force-stop", pkg)
    _adb(udid, "forward", "--remove-all")


def _open_android(cfg, url, udid=None, slot=0):
    from appium.options.android import UiAutomator2Options
    c = cfg["android"]
    udid = udid or c["udid"] or _adb_udid()
    last = ""
    for attempt in range(1, 4):
        if not _device_ready(udid):
            raise Halt("The emulator is not ready (not booted, or Android's package service is not answering). "
                       "Cold-boot it (Device Manager > Cold Boot Now) and run again.")
        o = UiAutomator2Options()
        o.udid = udid
        o.set_capability("appium:systemPort", 8200 + slot)       # one UiAutomator2 port per device so two sessions can run side by side
        o.no_reset = True
        o.new_command_timeout = 3600
        o.auto_grant_permissions = True
        o.set_capability("appium:uiautomator2ServerLaunchTimeout", 120000)   # default 30s is too tight on a busy emulator
        o.set_capability("appium:uiautomator2ServerInstallTimeout", 120000)
        o.set_capability("appium:adbExecTimeout", 60000)
        o.set_capability("appium:disableWindowAnimation", True)
        if c["app_path"]:
            o.app = c["app_path"]
        try:
            drv = webdriver.Remote(url, options=o)
            try:    # React Native apps never go 'idle': stop UiAutomator2 waiting 10s for it on every call
                drv.update_settings({"waitForIdleTimeout": 100, "waitForSelectorTimeout": 500,
                                     "actionAcknowledgmentTimeout": 500, "scrollAcknowledgmentTimeout": 100})
            except Exception:
                pass
            return drv
        except Exception as e:
            last = str(e).splitlines()[0]
            print(f"[run] could not start the Android automation session (attempt {attempt}/3): {last[:120]}")
            _cleanup_uiautomator(udid)
            time.sleep(4)
    raise Halt(f"Could not start the Android automation session after 3 attempts: {last}. "
               "Close other Appium/adb users, check the emulator is responsive, and run again.")


def open_driver(cfg: dict, platform: str, udid=None, slot=0):
    url = cfg["appium_url"]
    try:
        if platform == "android":
            return _open_android(cfg, url, udid, slot)
        from appium.options.ios import XCUITestOptions
        c = cfg["ios"]
        if not (c["udid"] and c["bundle_id"]):
            raise Halt("iOS needs 'udid' and 'bundle_id' in source/mobile/alumnye/config.json (and a Mac/device farm running Appium).")
        o = XCUITestOptions()
        o.udid, o.bundle_id, o.no_reset = c["udid"], c["bundle_id"], True
        if c["platform_version"]:
            o.platform_version = c["platform_version"]
        if c["device_name"]:
            o.device_name = c["device_name"]
        if c["app_path"]:
            o.app = c["app_path"]
        return webdriver.Remote(url, options=o)
    except Halt:
        raise
    except Exception as e:
        raise Halt(f"Could not open a {platform} session: {str(e).splitlines()[0]}")

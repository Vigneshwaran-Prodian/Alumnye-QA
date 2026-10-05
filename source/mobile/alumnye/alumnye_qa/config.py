"""Paths and settings. Everything resolves relative to the project root (RULES.md §1 layout)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PRODUCT_DIR = Path(__file__).resolve().parents[1]
SPECS_DIR = PRODUCT_DIR / "specs"
DATA_DIR = PRODUCT_DIR / "data"
LOCATOR_DIR = ROOT / "implementation" / "plans" / "locator-maps"
AI_LOG = ROOT / "implementation" / "ai_usages" / "ai_usage_log.md"
EXEC_DIR = ROOT / "executions"
RESULTS_DIR = ROOT / "reports" / "results" / "alumnye"

# module name -> locator map file
LOCATOR_FILES = {"auth": "Auth-Elements.md", "groups": "Group-Elements.md", "events": "Event-Elements.md"}
# a module needs the ones before it to work: Groups needs a successful login (Auth), journeys need both
MODULE_DEPENDS = {"auth": [], "groups": ["auth"], "events": ["auth", "groups"], "journeys": ["auth", "groups", "events"]}

# modules that drive several screens/roles at once use several maps (first match wins)
LOCATOR_MULTI = {"journeys": ["Journey-Elements.md", "Group-Elements.md", "Auth-Elements.md"]}

DEFAULTS = {
    "appium_url": "http://127.0.0.1:4723",
    "android": {"udid": "", "app_package": "app.alumnye.com", "app_path": "", "devices": {}},
    "ios": {"udid": "", "bundle_id": "", "platform_version": "", "device_name": "", "app_path": ""},
    "ai": {"enabled": True, "backend": "claude", "claude_model": "haiku", "model": "qwen3:4b", "url": "http://127.0.0.1:11434"},
    "timeouts": {"find": 8, "screen": 20},
    "test_mobile": "",
}


def load() -> dict:
    cfg = json.loads(json.dumps(DEFAULTS))
    path = PRODUCT_DIR / "config.json"
    if path.exists():
        user = json.loads(path.read_text(encoding="utf-8"))
        for k, v in user.items():
            if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                cfg[k].update(v)
            else:
                cfg[k] = v
    return cfg


def locator_files(module: str) -> list:
    """A module's own locator map first, then those of every module it depends on (Groups needs Auth's Home/sign-in keys)."""
    own = LOCATOR_MULTI.get(module) or [LOCATOR_FILES[module]]
    out = list(own)
    for dep in MODULE_DEPENDS.get(module, []):
        for f in locator_files(dep):
            if f not in out:
                out.append(f)
    return out

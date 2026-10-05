"""Locator map: reads/writes implementation/plans/locator-maps/<Module>-Elements.md.

Table columns: Key | Kind | Android strategies | iOS strategies | What it does | Last verified
Strategies are separated by ' ;; ' and tried in order. Forms:
  text:X   exact visible text / accessibility label
  textc:X  contains
  btn:X    a tappable control whose label contains X
  btnx:X   a tappable control whose label equals X exactly
  id:X     resource-id (Android) / accessibility id (iOS)
  xpath:Y  raw XPath (must not contain '|')
"""
import datetime
from pathlib import Path

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

SEP = " ;; "


def _lit(s: str) -> str:
    if "'" not in s:
        return f"'{s}'"
    if '"' not in s:
        return f'"{s}"'
    return "concat(" + ", \"'\", ".join(f"'{p}'" for p in s.split("'")) + ")"


_UP, _LOW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"


def _lc(expr: str) -> str:
    return f"translate(normalize-space({expr}),'{_UP}','{_LOW}')"


def to_locator(strategy: str, platform: str):
    """All text matching is case-insensitive (the app writes 'Sign in', docs write 'Sign In')."""
    kind, _, val = strategy.partition(":")
    android = platform == "android"
    if kind == "id":
        return (AppiumBy.ID, val) if android else (AppiumBy.ACCESSIBILITY_ID, val)
    if kind == "xpath":
        return By.XPATH, val
    v = _lit(val.strip().lower())
    if android:
        t, d = _lc("@text"), _lc("@content-desc")
        if kind == "text":
            return By.XPATH, f"//*[{t}={v} or {d}={v}]"
        if kind == "textc":
            return By.XPATH, f"//*[contains({t},{v}) or contains({d},{v})]"
        if kind == "btn":    # tappable control whose label CONTAINS the text
            return By.XPATH, f"//*[@clickable='true'][contains({d},{v}) or .//*[contains({t},{v})] or contains({t},{v})]"
        if kind == "btnx":   # tappable control whose label EQUALS the text (e.g. 'Sign in' but not 'Sign in with Google')
            return By.XPATH, f"//*[@clickable='true'][{d}={v} or .//*[{t}={v}] or {t}={v}]"
    else:
        lb, nm, vl = _lc("@label"), _lc("@name"), _lc("@value")
        if kind == "text":
            return By.XPATH, f"//*[{lb}={v} or {nm}={v} or {vl}={v}]"
        if kind == "textc":
            return By.XPATH, f"//*[contains({lb},{v}) or contains({nm},{v}) or contains({vl},{v})]"
        if kind == "btn":
            return By.XPATH, f"//XCUIElementTypeButton[contains({lb},{v}) or contains({nm},{v})]"
        if kind == "btnx":
            return By.XPATH, f"//XCUIElementTypeButton[{lb}={v} or {nm}={v}]"
    raise ValueError(f"unknown strategy '{strategy}'")


def literal_labels(strategies: list) -> list:
    """Human-readable labels an element is expected to carry (used by self-heal)."""
    out = []
    for s in strategies:
        kind, _, val = s.partition(":")
        if kind in ("text", "textc", "btn", "btnx") and val:
            out.append(val)
    return out


class LocatorMap:
    HEADER = "| Key | Kind | Android strategies | iOS strategies | What it does | Last verified |"

    def __init__(self, path: Path):
        self.path = Path(path)
        self.lines = self.path.read_text(encoding="utf-8").splitlines()
        self.rows = {}  # key -> line index
        self._parse()

    def _cells(self, line):
        return [c.strip() for c in line.strip().strip("|").split("|")]

    def _parse(self):
        in_table = False
        for i, line in enumerate(self.lines):
            if line.startswith("| Key |"):
                in_table = True
                continue
            if in_table and line.startswith("|---"):
                continue
            if in_table and line.startswith("|"):
                cells = self._cells(line)
                if len(cells) >= 6 and cells[0]:
                    self.rows[cells[0]] = i
            elif in_table:
                in_table = False

    def _row(self, key):
        if key not in self.rows:
            raise KeyError(f"locator key '{key}' not in {self.path.name}")
        return self._cells(self.lines[self.rows[key]])

    def strategies(self, key, platform):
        c = self._row(key)
        raw = c[2] if platform == "android" else c[3]
        return [s.strip() for s in raw.split(";;") if s.strip()]

    def kind(self, key):
        return self._row(key)[1]

    def describe(self, key):
        return self._row(key)[4]

    def conflicts(self, key, strategy, platform):
        """Another key whose own locators already describe the same label (so a healed strategy for `key` would be ambiguous)."""
        kind, _, val = strategy.partition(":")
        v = val.strip().lower()
        if not v:
            return None
        for other in self.rows:
            if other != key:
                if any(l.lower() == v for l in literal_labels(self.strategies(other, platform))):
                    return other
        return None

    def all_labels(self, platform):
        out = set()
        for k in self.rows:
            out.update(l.lower() for l in literal_labels(self.strategies(k, platform)))
        return out

    def promote(self, key, platform, strategy, why):
        """Put a healed strategy first and log it (never silent — RULES §2)."""
        c = self._row(key)
        idx = 2 if platform == "android" else 3
        cur = [s.strip() for s in c[idx].split(";;") if s.strip()]
        if strategy in cur:
            cur.remove(strategy)
        c[idx] = SEP.join([strategy] + cur)
        c[5] = datetime.date.today().isoformat()
        self.lines[self.rows[key]] = "| " + " | ".join(c) + " |"
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if "## Adaptation log" not in self.lines:
            self.lines += ["", "## Adaptation log"]
        self.lines.append(f"- {stamp} [{platform}] `{key}` -> `{strategy}` ({why})")
        self.path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")


class MultiMap:
    """Several locator-map files behind one LocatorMap interface (journeys use the Journey, Group and Auth maps together).
    The first file that has a key wins; a learned locator is saved back into the file the key came from."""

    def __init__(self, paths):
        self.maps = [LocatorMap(p) for p in paths]

    def _of(self, key):
        for m in self.maps:
            if key in m.rows:
                return m
        raise KeyError(f"locator key '{key}' not in any of: {', '.join(m.path.name for m in self.maps)}")

    def strategies(self, key, platform):
        return self._of(key).strategies(key, platform)

    def kind(self, key):
        return self._of(key).kind(key)

    def describe(self, key):
        return self._of(key).describe(key)

    def promote(self, key, platform, strategy, why):
        return self._of(key).promote(key, platform, strategy, why)

    def conflicts(self, key, strategy, platform):
        for m in self.maps:
            c = m.conflicts(key, strategy, platform)
            if c:
                return c
        return None

    def all_labels(self, platform):
        out = set()
        for m in self.maps:
            for k in m.rows:
                out.update(l.lower() for l in literal_labels(m.strategies(k, platform)))
        return out

"""The object every scenario script drives. Tier 1: cached locators. Tier 2: deterministic self-heal.
Tier 3: local Qwen (only when tiers 1-2 cannot find a required element). Tier 4: stop with a reason."""
import re
import subprocess
import time

from selenium.common.exceptions import WebDriverException

from . import healer, qwen, testdata
from .locators import literal_labels, to_locator


class _Timed:
    """Wraps the Appium driver and adds up where the time goes (element lookups, page reads, adb) for the triage report."""

    def __init__(self, drv, bucket):
        object.__setattr__(self, "_d", drv)
        object.__setattr__(self, "_b", bucket)

    def _t(self, name, fn, *a, **k):
        t0 = time.time()
        try:
            return fn(*a, **k)
        finally:
            c, sec = self._b.get(name, (0, 0.0))
            self._b[name] = (c + 1, sec + time.time() - t0)

    def find_elements(self, *a, **k):
        return self._t("find_elements", self._d.find_elements, *a, **k)

    def find_element(self, *a, **k):
        return self._t("find_element", self._d.find_element, *a, **k)

    @property
    def page_source(self):
        return self._t("page_source", lambda: self._d.page_source)

    def __getattr__(self, n):
        return getattr(self._d, n)


class StepFailed(Exception):
    def __init__(self, msg, category="assertion"):
        super().__init__(msg)
        self.category = category


# Pass-through buttons the app may show between Splash and Sign In (intro slides, Welcome, permission
# prompts). Order = preference. Create Account / Sign Up are never tapped here.
ENTRY_STEPS = ["Skip", "Get Started", "Next", "Allow", "While using the app", "Got it"]


class App:
    def __init__(self, driver, platform, cfg, locmap, run_id):
        self.timing = {}        # name -> (calls, seconds) for the current scenario
        self.d, self.platform, self.cfg, self.loc, self.run_id = _Timed(driver, self.timing), platform, cfg, locmap, run_id
        self._seen_where = set()
        self.scenario = ""
        self.events = []        # self-heal / Qwen adaptations in the current scenario
        self.ai_calls = 0
        self._ai_ok = None
        self.path = []          # screens/buttons passed through on the way to a target screen
        self.messages = []      # error / toast / validation messages observed in the current scenario
        self.taps = []          # what each tap actually hit (key, class, rectangle) - shown in the triage report
        self.soft_failures = []  # failed checks that do not stop the scenario (several flows can be verified in one run)
        self.notes = []         # which variant of an adaptive flow the app used (e.g. Terms handling)
        self.keys_used = set()  # locator keys this scenario touched (for the pass baseline)
        self.last_msgs = []     # texts seen by the latest watch_messages() (toast / banner / inline error)
        self.tag = ""           # device role shown in the log when two devices run in parallel ('anchor' / 'member')
        self.account = None     # e-mail this device signs in with (None = the last registered test user)
        self.discovered = []    # controls seen on screen that no scenario or locator map knows about (shown in the triage)
        self.pkg = cfg["android"]["app_package"] if platform == "android" else cfg["ios"]["bundle_id"]

    # ---------- low-level -------------------------------------------------
    def _is_input(self, el) -> bool:
        try:
            cls = el.get_attribute("class") or ""
        except Exception:
            return False
        return cls.endswith(("EditText", "TextField", "SecureTextField"))

    def _try(self, strategies, timeout, accept=None):
        end = time.time() + timeout
        while True:
            for s in strategies:
                try:
                    els = self.d.find_elements(*to_locator(s, self.platform))
                except WebDriverException:
                    raise
                except Exception:
                    els = []
                if accept:
                    els = [e for e in els if accept(e)]
                if els:
                    return els[0]
            if time.time() >= end:
                return None
            time.sleep(0.2)

    def _disabled_match(self, key, nodes=None):
        """The wanted control IS on screen but disabled (e.g. Continue before a valid entry)."""
        labels = literal_labels(self.loc.strategies(key, self.platform))
        nodes = nodes or healer.snapshot(self.d.page_source, self.platform)
        for n in nodes:
            if not n.enabled and n.label and any(l.lower() in n.label.lower() or healer._sim(l, n.label) >= 0.9 for l in labels):
                return n
        return None

    def is_disabled(self, key) -> bool:
        return self._disabled_match(key) is not None

    def _unblock(self, key, dis) -> bool:
        """A required button is on screen but DISABLED: find out what it is waiting for and satisfy it.
        1) an unticked consent checkbox  2) empty required fields  3) ask Qwen. Returns True once it is enabled."""
        from . import formfill, terms, testdata
        steps = []
        if terms._checkbox(self, 1) is not None and not terms.is_ticked(self):
            steps.append(f"ticked the Terms checkbox ({terms.tick_terms(self, required=False)})")
        filled = formfill.fill_inputs(self, testdata.new_person())
        if filled:
            steps.append("filled " + ", ".join(l for l, _ in filled))
        time.sleep(0.4)
        if not self._disabled_match(key):
            self.events.append({"tier": "unblock", "key": key, "strategy": "; ".join(steps), "reason": f"'{dis.label}' was disabled"})
            self.notes.append(f"'{dis.label}' was disabled - recovered automatically: " + "; ".join(steps))
            print(f"    [unblock] '{dis.label}' enabled after: {'; '.join(steps)}")
            return True
        ok = self.unstick(f"make the '{dis.label}' button enabled: satisfy whatever this screen still requires",
                          lambda: not self._disabled_match(key), steps, turns=2)
        if ok:
            self.notes.append(f"'{dis.label}' was disabled - recovered with the AI's help")
        return ok

    def _heal_ladder(self, key, intent, unblock=True):
        strategies = self.loc.strategies(key, self.platform)
        kind, desc = self.loc.kind(key), self.loc.describe(key)
        labels = literal_labels(strategies)
        nodes = healer.snapshot(self.d.page_source, self.platform)
        dis = self._disabled_match(key, nodes)
        if dis is not None and unblock and self._unblock(key, dis):
            el = self._try(strategies, 3)
            if el:
                return el
        if dis is not None:
            raise StepFailed(f"'{key}' ('{dis.label}') is on screen but DISABLED - an earlier input is probably "
                             f"empty/invalid (step: {intent})", "element-disabled")

        res = healer.heal(nodes, labels, kind, self.platform)
        if res:
            strat, why = res
            el = self._try([strat], 3)
            if el:
                clash = self.loc.conflicts(key, strat, self.platform)
                if clash:                       # e.g. 'text:MEMBER' is the role toggle, not Group Details: use it now, never save it
                    self.notes.append(f"self-heal for '{key}' used {strat} for this run only (not saved: it also describes '{clash}')")
                else:
                    self.loc.promote(key, self.platform, strat, f"self-heal: {why}")
                self.events.append({"tier": "heal", "key": key, "strategy": strat, "reason": why})
                print(f"    [heal] {key} -> {strat}")
                return el

        if self.cfg["ai"]["enabled"]:
            if self._ai_ok is None:
                self._ai_ok = qwen.available(self.cfg)
                if not self._ai_ok:
                    print("    [ai] the AI backend is not available (is the 'claude' CLI installed and logged in?) - skipping AI step")
            if self._ai_ok:
                print(f"    [ai] asking the AI about '{key}' ...")
                self.ai_calls += 1
                try:
                    ans = qwen.ask(self.cfg, intent, key, kind, desc, labels, healer.ui_summary(nodes))
                except Exception as e:
                    qwen.log_usage(self.run_id, self.scenario, f"element '{key}' not found", f"AI call failed: {e}")
                    raise StepFailed(f"'{key}' not found and AI call failed: {e}", "needs-human")
                idx = ans.get("node_index")
                if ans["verdict"] == "found" and isinstance(idx, int) and 0 <= idx < len(nodes) and kind != "input" and labels \
                        and max(healer._sim(l, nodes[idx].label.lstrip(", ")) for l in labels) < 0.5:
                    why = f"label '{nodes[idx].label}' does not resemble {labels}"     # a locator must never be learned from a guess
                    print(f"    [ai] rejected the AI's answer for '{key}': {why}")
                    qwen.log_usage(self.run_id, self.scenario, f"element '{key}' not found", f"answer rejected: {why}")
                    ans = {"verdict": "human", "node_index": None, "reason": f"rejected: {why}"}
                    idx = None
                if ans["verdict"] == "found" and isinstance(idx, int) and 0 <= idx < len(nodes):
                    strat = healer.strategy_for(nodes[idx], kind, self.platform)
                    el = self._try([strat], 3)
                    if el:
                        clash = self.loc.conflicts(key, strat, self.platform)
                        if clash:
                            self.notes.append(f"AI answer for '{key}' used {strat} for this run only (not saved: it also describes '{clash}')")
                        else:
                            self.loc.promote(key, self.platform, strat, f"qwen: {ans.get('reason', '')}")
                        self.events.append({"tier": "qwen", "key": key, "strategy": strat, "reason": ans.get("reason", "")})
                        qwen.log_usage(self.run_id, self.scenario, f"element '{key}' not found", f"adapted + logged -> {strat}")
                        return el
                if ans["verdict"] == "bug":
                    qwen.log_usage(self.run_id, self.scenario, f"element '{key}' not found", "likely real bug")
                    raise StepFailed(f"'{key}' ({desc}) is missing from the screen — likely functionality break. AI: {ans.get('reason')}", "likely-bug")
                qwen.log_usage(self.run_id, self.scenario, f"element '{key}' not found", "escalated to human")
                raise StepFailed(f"'{key}' ({desc}) not found; the AI could not resolve it. {ans.get('reason', '')}", "needs-human")
        raise StepFailed(f"'{key}' ({desc}) not found on screen", "element-not-found")

    # ---------- element API ----------------------------------------------
    def find(self, key, intent="", strict=False, timeout=None, unblock=True):
        timeout = timeout or self.cfg["timeouts"]["find"]
        kind = self.loc.kind(key)
        accept = (lambda e: not self._is_input(e)) if kind in ("button", "text") else (self._is_input if kind == "input" else None)
        self.keys_used.add(key)
        strategies, end, sliced = self.loc.strategies(key, self.platform), time.time() + timeout, 0
        while True:                                             # wait in short slices; a Success pop-up is dismissed within ~1.5 s, not after the full wait
            el = self._try(strategies, min(1.5, max(0.2, end - time.time())), accept)
            if el:
                return el
            sliced += 1
            if sliced >= 1 and not strict and self.handle_blocking_dialog():
                continue
            if time.time() >= end:
                break
        if strict:
            raise StepFailed(f"'{key}' ({self.loc.describe(key)}) not found", "assertion")
        if self.return_to_app(f"looking for '{key}'"):         # a download / picker / browser screen took us out of the app
            el = self._try(strategies, timeout, accept)
            if el:
                return el
        return self._heal_ladder(key, intent or f"use {key}", unblock)

    def foreground_package(self) -> str:
        if self.platform != "android":
            return self.pkg
        out = self._adb("shell", "dumpsys", "window")
        m = re.search(r"mCurrentFocus=Window\{[^ ]+ [^ ]+ ([\w.]+)/", out) or re.search(r"mFocusedApp=.*? ([\w.]+)/", out)
        return m.group(1) if m else self.pkg

    def wait_foreground(self, timeout=8) -> bool:
        """Wait (never press BACK) until Alumnye is in front again, e.g. while a file picker closes after a file was chosen."""
        end = time.time() + timeout
        while time.time() < end:
            if self.foreground_package() == self.pkg:
                return True
            time.sleep(0.5)
        return False

    def return_to_app(self, why="") -> bool:
        """If the screen in front is not Alumnye (a download screen, file picker, browser, Drive ...), bring the app back:
        BACK a few times, then re-activate the app. Reports where it had gone. Returns True if it had left the app."""
        fg = self.foreground_package()
        if fg == self.pkg or not fg:
            return False
        where = fg
        for _ in range(3):
            self.back()
            time.sleep(0.7)
            if self.foreground_package() == self.pkg:
                break
        else:
            self.d.activate_app(self.pkg)
            time.sleep(1.2)
        self.notes.append(f"the app was left for '{where}' ({why}); the runner brought Alumnye back to the front")
        print(f"    [focus] left the app for {where} - returned to Alumnye")
        return True

    # Buttons that only acknowledge a message. Decisions (Yes / Confirm / Delete / Accept / Reject) are never tapped here.
    ACK_BUTTONS = ("ok", "okay", "got it", "dismiss", "close", "done", "continue", "understood")

    def dismiss_anr(self) -> bool:
        """Android's '<app> isn't responding  [Close app] [Wait]' dialog appears when the machine is overloaded. Always Wait, never Close."""
        if self._try(["xpath://*[contains(@text,'responding')]"], 0.3) is None:
            return False
        wait = self._try(["btnx:Wait"], 1)
        if wait is None:
            return False
        wait.click()
        self.notes.append("Android 'app isn't responding' dialog (machine under load) - tapped Wait")
        print("    [dialog] 'isn't responding' -> Wait")
        time.sleep(1.5)
        return True

    def handle_blocking_dialog(self) -> bool:
        """If an acknowledgement dialog (e.g. 'Success - Group created successfully!  [OK]') is on screen, record its
        message for the message catalog and tap its OK button. Deterministic, no AI. Returns True if one was dismissed."""
        if self.dismiss_anr() or self.cancel_exit_dialog():
            return True
        nodes = healer.snapshot(self.d.page_source, self.platform)
        size = self.d.get_window_size()
        for n in nodes:
            lab = n.label.strip().lstrip(",").strip().lower()
            if n.clickable and n.enabled and not n.is_input and lab in self.ACK_BUTTONS and size["height"] * 0.2 < n.cy < size["height"] * 0.8:
                texts = [m.label for m in nodes if m is not n and m.label and not m.is_input and abs(m.cy - n.cy) <= 260
                         and abs(m.cx - n.cx) <= size["width"] * 0.45 and m.label.strip().lower() not in self.ACK_BUTTONS]
                near = [t for t in texts if not t.strip().isdigit()][:3]
                if near:
                    self.messages.append({"trigger": "a pop-up appeared", "text": " / ".join(near), "where": "dialog"})
                try:
                    n_el = self._try([f"btnx:{n.label.strip()}"], 1)
                    (n_el.click() if n_el else self.tap_xy(n.cx, n.cy))
                except Exception:
                    self.tap_xy(n.cx, n.cy)
                self.path.append(f"dialog '{' / '.join(near)}' -> {n.label.strip()}")
                print(f"    [dialog] dismissed '{' / '.join(near)}' with '{n.label.strip()}'")
                end = time.time() + 3
                while time.time() < end and self._try([f"btnx:{n.label.strip()}"], 0.2):      # wait until the dialog is really gone
                    time.sleep(0.2)
                time.sleep(0.4)
                return True
        return False

    def scroll_find(self, key, max_swipes=6):
        """Find an element that may be below the fold: look, swipe up, look again until the screen stops changing."""
        strategies = self.loc.strategies(key, self.platform)
        kind = self.loc.kind(key)
        accept = (lambda e: not self._is_input(e)) if kind in ("button", "text") else None
        last = None
        for _ in range(max_swipes + 1):
            el = self._try(strategies, 1.2, accept)
            if el:
                return el
            sig = hash(tuple(self.labels()))
            if sig == last:
                break
            last = sig
            self.swipe_up()
            time.sleep(0.4)
        return None

    def explore_for(self, key, intent="", via=()):
        """Find `key` wherever it lives instead of failing: this screen (scrolling) -> each `via` entry key (e.g. the
        My Account tab) with scrolling -> every other bottom-navigation tab -> self-heal -> Qwen. The route is reported."""
        el = self.scroll_find(key, max_swipes=1)
        if el:
            return el
        tried = []
        for entry in via:
            if self.visible(entry, 1):
                self.tap(entry, f"open {entry} to look for {key}")
                tried.append(entry)
                el = self.scroll_find(key)
                if el:
                    self.notes.append(f"'{key}' found by exploring: {' -> '.join(tried)} (scrolled as needed)")
                    return el
        size = self.d.get_window_size()
        nodes = healer.snapshot(self.d.page_source, self.platform)
        tabs = [n for n in nodes if n.clickable and n.label and n.cy > size["height"] * 0.85 and n.label.lstrip(", ") not in tried]
        for n in tabs[:5]:
            self.tap_xy(n.cx, n.cy)
            tried.append(n.label.lstrip(", "))
            time.sleep(0.6)
            el = self.scroll_find(key)
            if el:
                self.notes.append(f"'{key}' found by exploring: {' -> '.join(tried)} (scrolled as needed)")
                return el
        self.notes.append(f"'{key}' not found by exploring ({' -> '.join(tried) or 'this screen only'}); trying self-heal / Qwen")
        return self.find(key, intent or f"find {key}")

    def value_next_to(self, label):
        """Text shown beside a label on the same row (e.g. the code chip next to 'Member ID')."""
        nodes = healer.snapshot(self.d.page_source, self.platform)
        anchor = next((n for n in nodes if n.label.strip().lower() == label.lower()), None)
        if anchor is None:
            return ""
        cand = [n for n in nodes if n is not anchor and n.label and not n.is_input and abs(n.cy - anchor.cy) <= 40 and n.cx > anchor.cx]
        return min(cand, key=lambda n: n.cx - anchor.cx).label if cand else ""

    def visible(self, key, timeout=3) -> bool:
        """Check only — never heals, never calls AI. For negative / branching checks."""
        self.keys_used.add(key)
        return self._try(self.loc.strategies(key, self.platform), timeout) is not None

    def wait_screen(self, key, why, timeout=None):
        """Wait for a screen marker (healing allowed once the normal wait fails)."""
        el = self.find(key, why, timeout=timeout or self.cfg["timeouts"]["screen"])
        self.discover(why)
        return el

    # ---------- features the documents did not mention ---------------------
    # Never tapped by the explorer: anything that destroys, leaves or signs out.
    UNSAFE = re.compile(r"delete|remove|cancel|revoke|log ?out|sign ?out|leave|reject|decline|block|clear|reset|deactivate|close", re.I)
    # Safe to tap when exploring (read-only or harmless notifications).
    SAFE = re.compile(r"remind|resend|reminder|view|detail|filter|search|refresh|share|copy|history|status|pending|more", re.I)
    NOISE = re.compile(r"^(home|my group|my account|back|skip|next|ok|done|member|anchor|\d+)$", re.I)

    def _known_labels(self):
        try:
            return self.loc.all_labels(self.platform)
        except Exception:
            return set()

    def unmapped_controls(self):
        """Tappable controls on this screen whose label no locator-map entry mentions."""
        known = self._known_labels()
        out = []
        for n in healer.snapshot(self.d.page_source, self.platform):
            lab = n.label.strip()
            if not (n.clickable and n.enabled and 2 <= len(lab) <= 40) or n.is_input or self.NOISE.match(lab):
                continue
            low = lab.lower()
            if any(low in k or k in low for k in known if len(k) > 2):
                continue
            out.append(lab)
        return out

    def discover(self, where):
        """Record controls that nothing in the documents/locator maps covers (e.g. a 'Remind' option) so they
        get tested; the run report lists them and implementation/plans/discovered-features.md keeps them."""
        if where in self._seen_where:
            return
        self._seen_where.add(where)
        try:
            for lab in self.unmapped_controls():
                if not any(d["label"] == lab and d["where"] == where for d in self.discovered):
                    self.discovered.append({"where": where, "label": lab, "device": self.tag, "scenario": self.scenario,
                                            "safe": bool(self.SAFE.search(lab)) and not self.UNSAFE.search(lab), "result": ""})
        except Exception:
            pass

    def probe_safe(self, where, settle=1.5):
        """Exercise the harmless unmapped controls on this screen (Remind, Resend, View ...): tap, record what the app
        says or shows, come back. Destructive ones are only listed, never tapped. Returns the labels tapped."""
        self.discover(where)
        done = []
        for d in [d for d in self.discovered if d["where"] == where and d["safe"] and not d["result"]]:
            el = self._try([f"btn:{d['label']}", f"textc:{d['label']}"], 1.5)
            if el is None:
                continue
            before, screen_before = self.mark(), self.labels()
            try:
                el.click()
            except Exception:
                continue
            new = self.watch_messages(f"explored '{d['label']}' ({where})", before, seconds=settle + 1.5)
            changed = set(self.labels()) != set(screen_before)
            d["result"] = ("; ".join(new)[:160] if new else "no visible message") + (" (screen changed)" if changed else "")
            self.notes.append(f"{self.tag + ': ' if self.tag else ''}explored unlisted control '{d['label']}' on {where} -> {d['result']}")
            done.append(d["label"])
            if changed:
                self.back()
                time.sleep(0.6)
        return done

    def reach(self, key, why, on_screen=None):
        """Navigate to the screen holding `key` from wherever the app currently is (Splash, intro slides,
        Welcome ...) by tapping pass-through buttons. Deterministic; the path taken is reported.
        It acts on what is on screen right now and only waits while the screen is still loading."""
        strategies = self.loc.strategies(key, self.platform)
        end = time.time() + self.cfg["timeouts"]["screen"]
        taps = 0
        while time.time() < end and taps < 8:
            if self._try(strategies, 0.3):
                return
            present = {l.strip().lower() for l in self.labels()}      # one snapshot
            label = next((l for l in ENTRY_STEPS if l.lower() in present), None)
            if label is None:
                time.sleep(0.4)                                        # still on Splash / loading
                continue
            if on_screen:
                on_screen(self)
            el = self._try([f"btnx:{label}"], 0.5)
            if el:
                el.click()
                taps += 1
                self.path.append(label)
                print(f"    [nav] tapped '{label}' on the way to {key}")
                time.sleep(0.6)
        self.find(key, why, timeout=self.cfg["timeouts"]["screen"])

    INTRO_CONTROLS = ("skip", "next", "get started")

    def intro_state(self, wait=20, settle=0.0):
        """Look at the screen the app shows after launch and say what it is: the Splash still loading, an intro slide (with which
        controls: Skip / Next / Get Started) or the landing screen. Waits through the Splash. Returns
        {'kind': 'landing'|'slide'|'loading', 'skip','next','start': bool, 'texts': [slide wording], 'controls': [labels]}."""
        end = time.time() + wait
        state = {"kind": "loading", "skip": False, "next": False, "start": False, "texts": [], "controls": []}
        while time.time() < end:
            nodes = healer.snapshot(self.d.page_source, self.platform)
            # a button's label can carry its icon ("Next, →"), so controls are matched on the words before the comma
            norm = lambda l: l.strip().lstrip(",").strip().split(",")[0].strip().lower()
            clickable = {norm(n.label): n for n in nodes if n.clickable and n.label.strip()}
            labels = [n.label.strip().lstrip(",").strip() for n in nodes if n.label.strip()]
            state.update(skip="skip" in clickable, next="next" in clickable, start="get started" in clickable)
            state["controls"] = [c for c in ("Skip", "Next", "Get Started") if c.lower() in clickable]
            state["texts"] = list(dict.fromkeys(l for l in labels if norm(l) not in self.INTRO_CONTROLS and not re.match(r"^[\d:]{3,5}$", l) and len(l) > 1
                                                and not re.fullmatch(r"[\W_]+", l)))
            if "sign in" in clickable and "create account" in clickable:
                state["kind"] = "landing"
                return state
            if state["controls"]:
                state["kind"] = "slide"
                time.sleep(settle)
                return state
            time.sleep(0.4)
        return state

    def reach_landing(self, on_screen=None):
        """Splash -> (intro slides) -> landing screen with Sign in / Sign in with Google / Create account."""
        self.reach("landing_sign_in", "landing screen with Sign in / Google / Create account is shown", on_screen)

    def choose_identifier_tab(self, via="email"):
        """The identifier screens open on the Mobile tab (seen on device); switch to Email when needed."""
        key = "email_tab" if via == "email" else "mobile_tab"
        if self.visible(key, 2):
            self.tap(key, f"switch to the {via} tab")
            self.path.append(f"{via.title()} tab")

    def reach_sign_in(self, via="email"):
        """Existing user: landing -> 'Sign in' -> identifier screen (Email tab by default)."""
        self.reach_landing()
        self.tap("landing_sign_in", "open Sign in")
        self.path.append("Sign in")
        self.wait_screen("identifier_field", "Sign in screen asks for the email / mobile")
        self.choose_identifier_tab(via)

    def reach_create_account(self, via="email"):
        """New user: landing -> 'Create account' -> identifier screen (Email tab by default)."""
        self.reach_landing()
        self.tap("landing_create_account", "open Create account")
        self.path.append("Create account")
        self.wait_screen("identifier_field", "Create account screen asks for the email / mobile")
        self.choose_identifier_tab(via)

    def mark(self) -> set:
        """Labels currently on screen — call before an action, then watch_messages() after it."""
        return set(self.labels())

    def watch_messages(self, trigger, before=None, seconds=4):
        """Record every NEW piece of text (toast / inline error / validation) that appears after an action,
        so the team can review wording. Returns the list of texts."""
        before, seen = before or set(), {}
        end = time.time() + seconds
        msg_like = re.compile(r"invalid|error|required|failed|success|sent|incorrect|expired|must|please|blocked|denied|not allowed|try again|already|exist", re.I)
        last_new = None
        while time.time() < end:
            fresh = 0
            for n in healer.snapshot(self.d.page_source, self.platform):
                # a validation banner can already be up when 'before' was taken (the field validates on blur), so message-like text counts even then
                if n.label and (n.label not in before or msg_like.search(n.label)) and n.label not in seen and 3 <= len(n.label) <= 220:
                    seen[n.label] = "toast" if n.cls.endswith("Toast") else "on-screen"
                    fresh += 1
            if fresh:
                last_new = time.time()
            # leave early once the message (or the next screen) has appeared and stopped changing
            if last_new and (time.time() - last_new) >= (0.7 if any(msg_like.search(t) for t in seen) else 1.2) and len(seen) >= 1 and not fresh:
                break
            time.sleep(0.15)
        if len(seen) > 8:                       # the screen changed (navigation) - keep only message-like text
            seen = {t: k for t, k in seen.items() if k == "toast" or re.search(
                r"invalid|error|required|failed|success|sent|incorrect|expired|must|please|blocked|denied|not allowed|try again", t, re.I)}
        for text, kind in seen.items():
            self.messages.append({"trigger": trigger, "text": text, "where": kind})
        self._stale = set(seen)                # banners that may still be fading when the next action starts
        self.last_msgs = list(seen)            # the banner at the top of the app disappears quickly: checks use this, not a later screen read
        return list(seen)

    _BANNER_XPATH = ("//*[@text or @content-desc][" + " or ".join(f"contains(translate(@text,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{w}') or "
                     f"contains(translate(@content-desc,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'{w}')"
                     for w in ("success", "imported", "added", "invite", "sent", "invalid", "error", "failed", "required", "already", "duplicate", "must", "please", "created", "saved", "successful", "valid", "cannot", "exceed", "maximum", "too long")) + "]")

    def watch_banner(self, trigger, seconds=12, settle=1.0):
        """Catch the banner at the top of the app with targeted lookups (a few ms each) instead of whole-screen reads - on a heavy
        screen a full read takes ~10 s and the banner is gone before it finishes. Stops `settle` s after the last new text."""
        seen, end, last = [], time.time() + seconds, None
        while time.time() < end:
            try:
                els = self.d.find_elements("xpath", self._BANNER_XPATH)
            except Exception:
                els = []
            for e in els[:10]:
                try:
                    t = (e.text or e.get_attribute("content-desc") or "").strip()
                except Exception:
                    continue
                if 3 <= len(t) <= 220 and t not in seen:
                    seen.append(t)
                    last = time.time()
            if last and time.time() - last >= settle:
                break
            time.sleep(0.15)
        for t in seen:
            self.messages.append({"trigger": trigger, "text": t, "where": "banner"})
        self._stale, self.last_msgs = set(seen), list(seen)
        return seen

    def wait_banner_clear(self, limit=4.0):
        """Wait until the banner shown by the previous action is gone, so the next action's banner cannot be mistaken for it
        (the same text, e.g. 'Please enter a valid email format', appears once per bad input)."""
        stale = getattr(self, "_stale", set())
        end = time.time() + limit
        while stale and time.time() < end:
            if not (stale & set(self.labels())):
                break
            time.sleep(0.25)
        self._stale = set()

    def tap(self, key, intent="", strict=False, unblock=True):
        if self.loc.kind(key) != "input":
            self.dismiss_keyboard()
        el = self.find(key, intent or f"tap {key}", strict, unblock=unblock)
        try:
            r = el.rect
            self.taps.append(f"{key} -> {(el.get_attribute('class') or '').split('.')[-1]} at x{int(r['x'])},y{int(r['y'])} {int(r['width'])}x{int(r['height'])}")
        except Exception:
            pass
        el.click()

    def type(self, key, text, intent=""):
        el = self.find(key, intent or f"type into {key}")
        el.click()
        try:
            if (el.text or "").strip():
                el.clear()
        except Exception:
            pass
        self.enter_text(el, text)
        self.hide_keyboard()

    def enter_text(self, el, text):
        """Put text into a focused field: clipboard paste for long text (fast), otherwise normal typing."""
        if self.platform == "android" and text and not text.strip():
            self._adb("shell", "input", "text", "%s" * len(text))           # Appium refuses whitespace-only values
            return
        if self.platform == "android" and len(text or "") > 8 and self._paste(el, text):
            return
        el.send_keys(text)

    def _recover_label(self, label):
        """A button looked up by its label is missing: same ladder as a locator key - self-heal, then Qwen."""
        nodes = healer.snapshot(self.d.page_source, self.platform)
        res = healer.heal(nodes, [label], "button", self.platform)
        if res:
            el = self._try([res[0]], 3)
            if el:
                self.events.append({"tier": "heal", "key": f"button '{label}'", "strategy": res[0], "reason": res[1]})
                print(f"    [heal] button '{label}' -> {res[0]}")
                return el
        if self.cfg["ai"]["enabled"] and (self._ai_ok if self._ai_ok is not None else qwen.available(self.cfg)):
            self._ai_ok = True
            self.ai_calls += 1
            print(f"    [ai] asking the AI about button '{label}' ...")
            try:
                ans = qwen.ask(self.cfg, f"tap the '{label}' button", f"button '{label}'", "button", f"button labelled {label}",
                               [label], healer.ui_summary(nodes))
            except Exception as e:
                qwen.log_usage(self.run_id, self.scenario, f"button '{label}' not found", f"AI call failed: {e}")
                raise StepFailed(f"button '{label}' not found and AI call failed: {e}", "needs-human")
            idx = ans.get("node_index")
            if ans["verdict"] == "found" and isinstance(idx, int) and 0 <= idx < len(nodes):
                strat = healer.strategy_for(nodes[idx], "button", self.platform)
                el = self._try([strat], 3)
                if el:
                    qwen.log_usage(self.run_id, self.scenario, f"button '{label}' not found", f"adapted -> {strat}")
                    self.events.append({"tier": "qwen", "key": f"button '{label}'", "strategy": strat, "reason": ans.get("reason", "")})
                    return el
            qwen.log_usage(self.run_id, self.scenario, f"button '{label}' not found", f"{ans['verdict']}: {ans.get('reason', '')}")
        raise StepFailed(f"button '{label}' not found on screen", "element-not-found")

    def tap_label(self, label):
        """Tap the tappable control whose label equals / contains `label` (case-insensitive)."""
        self.dismiss_keyboard()
        el = self._try([f"btnx:{label}", f"btn:{label}"], 3)
        if el is None:
            el = self._recover_label(label)
        try:
            r = el.rect
            self.taps.append(f"'{label}' -> {(el.get_attribute('class') or '').split('.')[-1]} at x{int(r['x'])},y{int(r['y'])}")
        except Exception:
            pass
        el.click()

    def _paste(self, el, text) -> bool:
        """Clipboard + PASTE key: far faster than typing char by char. Verified; the caller falls back to send_keys."""
        import base64
        try:
            self.d.set_clipboard_base64(base64.b64encode(text.encode("utf-8")).decode())
            self.d.press_keycode(279)                              # KEYCODE_PASTE
            time.sleep(0.3)
            return (el.text or "").strip() == text.strip()
        except Exception:
            return False

    def text_of(self, key) -> str:
        el = self.find(key)
        attr = "content-desc" if self.platform == "android" else "label"
        try:
            alt = el.get_attribute(attr)
        except Exception:
            alt = ""
        return (el.text or alt or "").strip()

    def expect(self, key, why, strict=False):
        self.find(key, why, strict)

    def expect_absent(self, key, why, timeout=3):
        if self.visible(key, timeout):
            raise StepFailed(f"Expected '{key}' to be absent: {why}")

    def check(self, cond, msg):
        if not cond:
            raise StepFailed(msg)

    def soft_check(self, cond, msg):
        """Like check(), but records the failure and lets the scenario continue; the scenario still ends FAILED."""
        if not cond:
            self.soft_failures.append(msg)
            print(f"    [check failed] {msg}")
        return bool(cond)

    def tap_xy(self, x, y):
        if self.platform == "android":
            self.d.execute_script("mobile: clickGesture", {"x": int(x), "y": int(y)})
        else:
            self.d.execute_script("mobile: tap", {"x": int(x), "y": int(y)})

    def tap_center(self, el):
        r = el.rect
        self.tap_xy(r["x"] + r["width"] / 2, r["y"] + r["height"] / 2)

    def swipe_down(self):
        size = self.d.get_window_size()
        w, h = size["width"], size["height"]
        if self.platform == "android":
            self.d.execute_script("mobile: swipeGesture", {"left": int(w * 0.1), "top": int(h * 0.25), "width": int(w * 0.8),
                                                           "height": int(h * 0.5), "direction": "down", "percent": 0.75})
        else:
            self.d.execute_script("mobile: swipe", {"direction": "down"})

    def unstick(self, goal, done, tried, turns=2, focus=None) -> bool:
        """Tier 3 for 'the action had no effect': ask local Qwen for the next single action (tap / scroll / wait /
        back / give_up), perform it, and re-check `done()`. Every call is logged to ai_usage_log.md."""
        if not self.cfg["ai"]["enabled"]:
            return False
        if self._ai_ok is None:
            self._ai_ok = qwen.available(self.cfg)
        if not self._ai_ok:
            print("    [ai] the AI backend is not available - cannot ask for help")
            return False
        tried = list(tried)
        for turn in range(turns):
            nodes = healer.snapshot(self.d.page_source, self.platform)
            print(f"    [ai] stuck on '{goal}' - asking the AI (turn {turn + 1}) ...")
            self.ai_calls += 1
            try:
                ans = qwen.ask_action(self.cfg, goal, tried, healer.ui_summary(nodes, near_text=focus),
                                      extra=f"On-screen keyboard visible: {'YES' if self.keyboard_shown() else 'no'}")
            except Exception as e:
                qwen.log_usage(self.run_id, self.scenario, f"stuck: {goal}", f"AI call failed: {e}")
                return False
            act, idx, why = ans["action"], ans.get("node_index"), ans.get("reason", "")
            qwen.log_usage(self.run_id, self.scenario, f"stuck: {goal}", f"Qwen advised {act} {idx if idx is not None else ''} - {why}")
            self.events.append({"tier": "qwen", "key": goal, "strategy": f"{act} {idx if idx is not None else ''}".strip(), "reason": why})
            if act == "give_up":
                return False
            tgt_node = nodes[idx] if isinstance(idx, int) and 0 <= idx < len(nodes) else None
            invalid = None
            if tgt_node is not None and act in ("tap", "type"):
                if not tgt_node.enabled:
                    invalid = f"element {idx} is disabled"
                elif act == "type" and tgt_node.label.strip() and tgt_node.label.strip() != tgt_node.hint:
                    invalid = f"field {idx} already has a value"
            if invalid:                                   # the model's advice is checked, never trusted blindly
                tried.append(f"Qwen advised {act} {idx} but {invalid}")
                print(f"    [ai] rejected advice: {invalid}")
                continue
            if act == "tap" and isinstance(idx, int) and 0 <= idx < len(nodes):
                self.tap_xy(nodes[idx].cx, nodes[idx].cy)
            elif act == "type" and isinstance(idx, int) and 0 <= idx < len(nodes) and ans.get("text"):
                tgt = self._try([f"xpath:(//{nodes[idx].cls})[{nodes[idx].ordinal}]"], 1)
                if tgt is not None:
                    tgt.click()
                    self.enter_text(tgt, str(ans["text"]))
                    self.dismiss_keyboard()
            elif act == "scroll_down":
                self.swipe_up()
            elif act == "scroll_up":
                self.swipe_down()
            elif act == "back":
                self.back()
            else:
                time.sleep(2)
            tried.append(f"Qwen: {act} {idx if idx is not None else ''}")
            time.sleep(1)
            if done():
                return True
        return False

    def swipe_up(self):
        size = self.d.get_window_size()
        w, h = size["width"], size["height"]
        if self.platform == "android":
            self.d.execute_script("mobile: swipeGesture", {"left": int(w * 0.1), "top": int(h * 0.25), "width": int(w * 0.8),
                                                           "height": int(h * 0.5), "direction": "up", "percent": 0.75})
        else:
            self.d.execute_script("mobile: swipe", {"direction": "up"})

    # ---------- screen text ----------------------------------------------
    def labels(self) -> list:
        return [n.label for n in healer.snapshot(self.d.page_source, self.platform) if n.label]

    def screen_has(self, *patterns, timeout=4) -> str:
        """Return the first label matching any regex pattern (case-insensitive) or ''."""
        end = time.time() + timeout
        while True:
            for lab in self.labels():
                if any(re.search(p, lab, re.I) for p in patterns):
                    return lab
            if time.time() >= end:
                return ""
            time.sleep(0.5)

    def inputs(self) -> list:
        return [n for n in healer.snapshot(self.d.page_source, self.platform) if n.is_input]

    # ---------- device / app ---------------------------------------------
    def _adb(self, *args) -> str:
        udid = self.d.capabilities.get("udid") or self.d.capabilities.get("deviceUDID") or ""
        try:
            return self.d._t("adb", lambda: (subprocess.run(["adb", *(["-s", udid] if udid else []), *args], capture_output=True, timeout=10).stdout or b"")
                             .decode("utf-8", errors="replace"))      # never let a stray byte break the run
        except Exception:
            return ""

    def keyboard_shown(self) -> bool:
        """Appium's is_keyboard_shown() reports False on some emulators while the keyboard is on screen,
        so on Android the Android input-method service itself is asked."""
        if self.platform == "android":
            out = self._adb("shell", "dumpsys input_method | grep -m1 mInputShown")   # filtered on the device: the full dump is ~900 KB
            if "mInputShown=" in out:
                return "mInputShown=true" in out
        try:
            return bool(self.d.is_keyboard_shown())
        except Exception:
            return False

    def dismiss_keyboard(self) -> bool:
        """React Native apps swallow the first tap while the keyboard is up (that tap only dismisses it).
        Close it for real - hide key, then a tap on a neutral spot - and confirm, before tapping anything else."""
        for attempt in range(3):
            if not self.keyboard_shown():
                return True
            if self.platform == "android":
                self._adb("shell", "input", "keyevent", "4")       # BACK: closes the keyboard (only sent when it is shown)
            else:
                try:
                    self.d.hide_keyboard()
                except Exception:
                    pass
            time.sleep(0.3)
            if self.keyboard_shown():
                size = self.d.get_window_size()
                self.tap_xy(size["width"] / 2, size["height"] * 0.10)      # blank area in the header
                time.sleep(0.6)
        return not self.keyboard_shown()

    def hide_keyboard(self):
        self.dismiss_keyboard()

    def at_home_screen(self, timeout=0.3) -> bool:
        try:
            return self.visible("home_welcome", timeout)
        except KeyError:
            return False

    def back(self):
        """BACK, except on Home: there it only opens the app's 'Exit App' dialog. If that dialog is ever up, Cancel is tapped."""
        if self.platform == "android":
            if self.at_home_screen():
                self.notes.append("BACK skipped on Home (it would open the 'Exit App' dialog)")
                return
            self.d.back()
            time.sleep(0.3)
            self.cancel_exit_dialog()
        else:
            self.d.execute_script("mobile: tap", {"x": 20, "y": 60})

    def cancel_exit_dialog(self) -> bool:
        """'Exit App - Do you want to exit the app? [Cancel] [Exit]': always Cancel (never Exit)."""
        if self._try(["text:Exit App"], 0.4) is None:
            return False
        cancel = self._try(["btnx:Cancel"], 1)
        if cancel is None:
            return False
        cancel.click()
        self.notes.append("the 'Exit App' dialog was open - Cancel tapped")
        print("    [dialog] 'Exit App' dialog dismissed with Cancel")
        time.sleep(0.5)
        return True

    def has_text(self, text, timeout=2) -> bool:
        """One targeted lookup (no full screen read) - use on heavy screens such as a 200-row preview."""
        return self._try([f"textc:{text}"], timeout) is not None

    def dismiss_permissions(self):
        if self.platform != "android":
            return
        for _ in range(3):
            btn = None
            for rid in ("permission_allow_foreground_only_button", "permission_allow_button"):
                els = self.d.find_elements("id", f"com.android.permissioncontroller:id/{rid}")
                if els:
                    btn = els[0]
                    break
            if not btn:
                return
            btn.click()
            time.sleep(1)

    def launch(self):
        self.d.activate_app(self.pkg)
        time.sleep(1.2)
        self.dismiss_permissions()

    def restart(self):
        self.d.terminate_app(self.pkg)
        self.launch()

    def reset(self):
        """Fresh-install state: clear app data (Android) / relaunch (iOS) and open the app."""
        self.d.terminate_app(self.pkg)
        if self.platform == "android":
            try:
                self.d.execute_script("mobile: clearApp", {"appId": self.pkg})
            except Exception:
                udid = self.d.capabilities.get("udid", "")
                subprocess.run(["adb", *(["-s", udid] if udid else []), "shell", "pm", "clear", self.pkg], capture_output=True)
        self.launch()

    # ---------- evidence --------------------------------------------------
    def capture(self, prefix):
        try:
            self.d.save_screenshot(f"{prefix}.png")
            with open(f"{prefix}_hierarchy.xml", "w", encoding="utf-8") as f:
                f.write(self.d.page_source)
        except Exception:
            pass

    # ---------- shared journeys ------------------------------------------
    def _otp_boxes(self):
        cls = "android.widget.EditText" if self.platform == "android" else "XCUIElementTypeTextField"
        return self.d.find_elements("xpath", f"//{cls}")

    def enter_otp(self, label, code=None):
        """Works for one OTP field or for one box per digit (the app uses six boxes)."""
        if not code:
            import threading
            stop = threading.Event()

            def _keepalive():                                  # the session must not time out while a human is typing
                while not stop.wait(20):
                    try:
                        self.d.get_window_size()
                    except Exception:
                        pass
            threading.Thread(target=_keepalive, daemon=True).start()
            try:
                code = testdata.otp(label)
            finally:
                stop.set()
        self.find("otp_input", "focus the first OTP box").click()
        boxes = self._otp_boxes()
        if self.platform == "android" and len(boxes) >= len(code) > 1:
            self._adb("shell", "input", "text", code)                  # one call; focus auto-advances between boxes
            time.sleep(0.3)
            filled = sum(1 for n in healer.snapshot(self.d.page_source, "android") if n.is_input and n.label.strip())
            if filled < len(code):                                     # no auto-advance: fill box by box
                for b, ch in zip(self._otp_boxes(), code):
                    b.click()
                    b.send_keys(ch)
        elif len(boxes) >= len(code) > 1:
            for b, ch in zip(boxes, code):
                b.send_keys(ch)
        elif self.platform == "android":
            self._adb("shell", "input", "text", code)
        else:
            self.find("otp_input").send_keys(code)
        self.dismiss_keyboard()

    def at_home(self, timeout=3) -> bool:
        return self.visible("home_marker", timeout)

    def sign_in_with_email_otp(self, email):
        """Existing-user sign-in by email OTP; lands on Home."""
        self.reach_sign_in()
        self.type("identifier_field", email)
        self.tap("primary_button", "submit identifier")
        self.wait_screen("otp_screen_marker", "OTP screen is shown")
        self.enter_otp(f"Sign in OTP for {email} (check https://yopmail.com/?{email.split('@')[0]})")
        from .flows import accept_terms
        accept_terms(self, required=False)                       # the Verify screen may ask for Terms again
        self.tap("verify_button", "verify OTP")
        if not self.at_home(6):
            self.finish_pending_profile()                       # the account never finished its profile
        self.wait_screen("home_marker", "Home screen after sign-in")

    def finish_pending_profile(self) -> bool:
        """The app remembers a half-finished registration (step 3 of 3, Complete Your Profile) and reopens on it.
        Finish it with valid data so the session can move on to Home."""
        if not self.visible("complete_profile_marker", 2):
            return False
        from .flows import complete_profile
        print("    [prerequisite] the app reopened on 'Complete Your Profile' (unfinished registration) - completing it")
        complete_profile(self, testdata.new_person())
        self.notes.append("prerequisite: finished an unfinished registration (Complete Your Profile) before continuing")
        return self.at_home(15)

    def ensure_logged_in(self):
        """Reuse the current session if on Home; otherwise sign in with the last registered test user."""
        self.cancel_exit_dialog()                                         # an 'Exit App' dialog hides the screen: never mistake it for 'signed out'
        if self.visible("nav_profile", 1.5) or self.at_home(0.5):      # the bottom bar exists on every signed-in screen
            return
        if self.at_home(3):
            return
        if self.finish_pending_profile():
            return
        users = testdata.load_users()
        if not users and not self.account:      # module dependency: Groups etc. need a successful login, so the Auth flow runs first
            from .flows import register_new_user
            person = testdata.new_person()
            print("    [prerequisite] no signed-in user - running the Auth registration flow first")
            self.reset()
            register_new_user(self, person["email"], person)
            testdata.save_user(person)
            self.notes.append(f"prerequisite: registered {person['email']} (Auth) before this module")
            return
        self.sign_in_with_email_otp(self.account or users[-1]["email"])

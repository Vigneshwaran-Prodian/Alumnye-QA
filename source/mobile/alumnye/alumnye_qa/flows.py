"""Reusable journeys shared by scenario scripts (scripts stay one-per-scenario; flows are not scenarios)."""


def to_otp_screen(app, identifier, new_user=True):
    """New user -> landing 'Create account'; existing user -> landing 'Sign in'."""
    app.reach_create_account() if new_user else app.reach_sign_in()
    app.type("identifier_field", identifier, "enter the mobile/email")
    app.tap("primary_button", "submit the identifier")
    app.wait_screen("otp_screen_marker", "OTP verification screen is shown")


def enter_otp_for(app, identifier, code=None):
    hint = f" (inbox: https://yopmail.com/?{identifier.split('@')[0]})" if "@" in identifier else ""
    app.enter_otp(f"OTP sent to {identifier}{hint}", code=code)


def accept_terms(app, required=True):
    """After the OTP is entered: tick the 'I accept the Terms & Conditions and Privacy Policy' checkbox (if the screen has one)."""
    from .terms import tick_terms
    result = tick_terms(app, required)
    app.path.append(f"Terms checkbox: {result}")
    return result


def verify_otp(app, identifier, accept=True):
    """Verify identity screen: enter the 6-digit OTP, tick the checkbox, tap 'Verify & join Alumnye'."""
    enter_otp_for(app, identifier)
    if accept:
        accept_terms(app)
    app.tap("verify_button", "verify the OTP and join")


def fill_profile(app, person):
    """Fill every empty field on the profile screen (names, and anything else the screen asks for) - no submit."""
    from .formfill import fill_inputs
    app.wait_screen("complete_profile_marker", "Complete Profile screen is shown")
    return fill_inputs(app, person)


def complete_profile(app, person):
    """After 'Verify & join': read each screen, fill all fields with valid values, continue until Home."""
    from .formfill import complete_profile as run
    return run(app, person)


def register_new_user(app, identifier, person):
    to_otp_screen(app, identifier)
    verify_otp(app, identifier)
    complete_profile(app, person)
    app.wait_screen("home_marker", "Home screen after registration")


# ------------------------------------------------------------------ groups
import re
import time

from selenium.common.exceptions import WebDriverException


def precondition_signed_in(app):
    """PRECONDITION for every module after Auth (Groups, events ...): a user must be signed in. Reuses the live session; otherwise
    signs in with the registered test user (OTP typed by the tester) and, if none exists yet, registers one. The route taken is
    written to the report so it is visible how the scenario got its signed-in user."""
    was_home = app.at_home(2)
    app.ensure_logged_in()
    who = app.account or (testdata.load_users() or [{}])[-1].get("email", "?")
    app.notes.append(f"precondition: signed in as {who} ({'session already open' if was_home else 'signed in by the runner before the scenario'})")


def to_anchor_home(app):
    """Signed in (reusing the session) and on the Anchor view of Home."""
    precondition_signed_in(app)
    for _ in range(4):                                  # leave any group / form screen left open by a previous scenario
        if app.visible("role_anchor", 1):
            break
        app.back()
        time.sleep(0.5)
    else:
        app.restart()
    if app.visible("role_anchor", 2):
        app.tap("role_anchor", "switch to the ANCHOR view")
    app.wait_screen("anchor_home_marker", "Anchor Home is shown")


def back_to_anchor_home(app):
    for _ in range(4):
        if app.visible("anchor_home_marker", 1):
            return
        app.back()
        time.sleep(0.5)
    to_anchor_home(app)


def open_group_form(app):
    to_anchor_home(app)
    app.tap("new_group_button", "open the New Group form")
    app.wait_screen("group_name_field", "group form is shown")


def create_group(app, group):
    open_group_form(app)
    app.type("group_name_field", group["name"], "enter the group name")
    if group.get("desc"):
        app.type("group_description_field", group["desc"], "enter the group description")
    app.tap("save_group_button", "save the group")
    app.wait_screen("group_details_marker", "Group Details opens after saving")
    from . import testdata
    testdata.save_group(group)
    return group


def open_group(app, name=None):
    """Open a group from Anchor Home (the last one the tests created; one is created if none exists yet)."""
    from . import testdata
    groups = testdata.load_groups()
    if not groups and not name:
        create_group(app, testdata.new_group())
        return
    name = name or groups[-1]["name"]
    to_anchor_home(app)
    for attempt in range(3):                                   # the card can re-render between finding and tapping it
        el = app._try([f"textc:{name}"], 5)
        if el is None:
            app.soft_check(False, f"group '{name}' is not listed on Anchor Home")
            return
        try:
            el.click()
            break
        except WebDriverException:
            time.sleep(0.5)
    app.wait_screen("group_details_marker", "Group Details is shown")


def open_add_members(app):
    open_group(app)
    app.tap("add_member_entry", "open the add-member screen")
    time.sleep(0.8)


def pending_invites(app):
    return app.screen_has(r"\d+\s*(pending|invite)", timeout=1) or ""


def submit_or_guard(app, key, trigger):
    """A disabled submit button IS the guard (logged); otherwise tap it without auto-recovery and log any message."""
    app.wait_banner_clear()
    before = app.mark()
    if app.is_disabled(key):
        app.messages.append({"trigger": trigger, "text": "(button stays disabled)", "where": "state"})
        return "blocked"
    app.tap(key, trigger, unblock=False)
    app.watch_messages(trigger, before, seconds=3)      # full text kept in app.last_msgs
    return "tapped"


ERROR_WORDS = r"invalid|valid email|valid format|please enter|already|cannot|can't|own|exist|duplicate|error|not allowed|self|failed|required"


def send_invite(app, email):
    """Invite one email. Returns 'sent', 'blocked' (button disabled), 'error' (a rejection message) or 'unknown'.
    The banner text is kept in app.last_msgs (it disappears after a few seconds, so checks must use it)."""
    if app.visible("tab_invite", 1):
        app.tap("tab_invite", "open the Invite tab")
    app.type("invite_email_field", email, f"enter {email}")
    app.wait_banner_clear()
    before = app.mark()
    app.last_msgs = []
    if app.is_disabled("send_invite_button"):
        app.messages.append({"trigger": f"entered '{email}' on Invite", "text": "(send button stays disabled)", "where": "state"})
        return "blocked"
    app.tap("send_invite_button", f"send the invitation to {email}", unblock=False)
    texts = [t for t in app.watch_messages(f"sent invitation to '{email}'", before, seconds=3) if not t.lower().startswith("enter ")]
    app.last_msgs = texts
    text = " ".join(texts).lower()
    if re.search(ERROR_WORDS, text):
        return "error"
    if re.search(r"success|sent|invited", text):
        groups = testdata.load_groups()
        if groups and "@" in email:
            testdata.save_invite(groups[-1]["name"], email)
        return "sent"
    return "unknown"


def current_user_email(app):
    """The e-mail of the signed-in user, read from My Account (so 'invite yourself' uses the REAL logged-in user)."""
    app.ensure_logged_in()
    app.tap("nav_profile", "open My Account to read the signed-in e-mail")
    time.sleep(0.8)
    found = app.screen_has(r"[\w.+-]+@[\w-]+\.[\w.]+", timeout=4)
    back_to_anchor_home(app)
    m = re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", found or "")
    return m.group(0) if m else None


DRIVE_MARKERS = r"my drive|shared with me|starred|files from drive|google drive"


def _picker_evidence(app, why):
    """Save the picker screen next to the run's evidence so a picker that behaves differently can be read afterwards."""
    from . import config
    try:
        app.capture(str(config.RESULTS_DIR / app.run_id / f"{app.scenario}_picker_{why}"))
    except Exception:
        pass


def choose_file(app, filename, local_path, required=True):
    """Push the file to the device's own Downloads folder (local storage), tap the Upload area and pick the file in the Android
    picker FROM LOCAL STORAGE - the picker may open on Google Drive, so the runner opens the roots drawer and chooses 'Downloads'.
    Returns True once picked and the app is back in front; False when the picker offers the file greyed out / not at all."""
    app._adb("push", local_path, f"/sdcard/Download/{filename}")
    app._adb("shell", "am", "broadcast", "-a", "android.intent.action.MEDIA_SCANNER_SCAN_FILE", "-d", f"file:///sdcard/Download/{filename}")
    app.tap("choose_file_button", "open the file picker")
    end = time.time() + 10
    while app.foreground_package() == app.pkg and time.time() < end:      # wait for the picker; no BACK, no extra taps
        time.sleep(0.4)
    if app.foreground_package() == app.pkg:
        app.soft_check(False, f"the file picker did not open after tapping the Upload area ('{filename}')")
        return False
    went_local = False
    for attempt in range(4):
        on_drive = any(re.search(DRIVE_MARKERS, l, re.I) for l in app.labels())
        el = None if on_drive else app._try([f"textc:{filename}"], 2.5)
        if el:
            if el.get_attribute("enabled") == "false":
                app.notes.append(f"the file picker shows '{filename}' greyed out (not selectable)")
                break
            el.click()
            if not app.wait_foreground(10):
                app.notes.append(f"the picker stayed open after choosing '{filename}'")
            if went_local:
                app.notes.append(f"file picker: switched from Google Drive to the device's Downloads (local storage) for '{filename}'")
            return True
        roots = app._try(["xpath://*[@content-desc='Show roots']"], 1)         # open the roots drawer and pick the LOCAL Downloads
        if roots:
            roots.click()
            time.sleep(0.8)
        dl = app._try(["xpath://*[@text='Downloads']"], 1.5)
        if dl:
            dl.click()
            went_local = True
            time.sleep(1.0)
        else:
            app.swipe_up()
    _picker_evidence(app, "not_found")
    app.return_to_app("closing the file picker")                         # BACK is used only to leave a picker that has nothing to choose
    if required:
        app.soft_check(False, f"could not select '{filename}' from the device's local Downloads in the file picker")
    else:
        app.notes.append(f"'{filename}' could not be chosen in the file picker (the picker does not offer it)")
    return False


# ------------------------------------------------------------------ journeys (two devices)
from . import testdata
from .session import Blocked


def member_ready(app, sync):
    """Member device: signed in as the journey's member account (registered once, then the session is reused)."""
    acc = testdata.journey_account("member")
    if acc:
        app.account = acc["email"]
        app.ensure_logged_in()
    else:
        person = testdata.new_person()
        app.account = person["email"]
        app.reset()
        register_new_user(app, person["email"], person)
        testdata.save_journey_account("member", person)
        app.notes.append(f"member account registered: {person['email']}")
    sync.data["member_email"] = app.account
    who = testdata.journey_account("member") or {}
    if who.get("first"):
        sync.data["member_name"] = f"{who['first']} {who.get('last', '')}".strip()
    sync.set("member_ready")


def anchor_creates_group_and_invites(app, sync):
    """Anchor device: create a group, wait until the member device is ready, invite the member. Returns the group name."""
    group = testdata.new_group()
    create_group(app, group)
    sync.data["group"] = group["name"]
    sync.wait("member_ready")
    open_add_members(app)
    result = send_invite(app, sync.data["member_email"])
    app.soft_check(result == "sent", f"inviting the member must succeed (result: {result})")
    sync.data["invite_result"] = result
    snap = anchor_members_snapshot(app, sync)                    # numbers before the member answers: the member is Pending, not counted
    sync.data["before"] = snap
    app.soft_check(_pending_has(snap, sync.data["member_email"]), "after the invitation the member must be listed under PENDING ACCEPTANCE with a Remind button")
    sync.set("invite_sent")
    return group["name"]


def member_open_invitation(app, sync):
    """Member device: find the pending invitation. The app is explored (Home, My Group, other tabs); if it is not
    in the app, the tester is asked for the invitation link from the e-mail and it is opened on this device."""
    sync.wait("invite_sent")
    app.restart()                                           # pick up the invitation on a fresh start
    app.wait_screen("home_marker", "member Home")
    if app.visible("role_member", 2):
        app.tap("role_member", "switch to the MEMBER view")
    group = sync.data.get("group", "")
    for _ in range(2):
        if app.screen_has(re.escape(group), r"invited you|invitation", timeout=3):
            app.notes.append("member: invitation visible in the app")
            return True
        if app.visible("nav_my_group", 1):
            app.tap("nav_my_group", "look for the invitation under My Group")
            time.sleep(0.8)
        elif not app.visible("accept_invite_button", 1):
            break
    if app.visible("accept_invite_button", 2):
        return True
    link = testdata.ask(f"[member] the invitation is not visible in the app. Open https://yopmail.com/?{app.account.split('@')[0]}, "
                        f"copy the group-invitation link from the e-mail for '{group}'", "invitation link (blank = give up)")
    if not link:
        app.soft_check(False, "the invitation reached neither the app screens nor an e-mail link the tester could supply")
        return False
    app._adb("shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", link, app.pkg)
    time.sleep(3)
    app.notes.append("member: invitation opened from the e-mail link")
    return True


def member_decide(app, accept=True):
    """Tap Accept or Reject (finding the control by exploring), confirm a dialog if one appears."""
    key = "accept_invite_button" if accept else "reject_invite_button"
    app.explore_for(key, f"{'accept' if accept else 'reject'} the group invitation", via=("nav_my_group",))
    before = app.mark()
    app.tap(key, "accept the invitation" if accept else "reject the invitation", unblock=False)
    if app.visible("confirm_dialog_yes", 1.5):
        app.tap("confirm_dialog_yes", "confirm the decision")
    app.watch_messages("accepted the invitation" if accept else "rejected the invitation", before, seconds=3)


def anchor_invite_again(app, sync, email=None):
    """Anchor device: invite an e-mail to the journey's group (default: the member). Returns send_invite's result."""
    open_add_members(app)
    return send_invite(app, email or sync.data["member_email"])


def member_sees_invitation(app, sync, timeout=4) -> bool:
    """Member device, check only: is an invitation for the journey's group offered right now?"""
    app.restart()
    app.wait_screen("home_marker", "member Home")
    if app.visible("role_member", 2):
        app.tap("role_member", "switch to the MEMBER view")
    if app.visible("nav_my_group", 1):
        app.tap("nav_my_group", "look for the invitation under My Group")
    return bool(app.visible("accept_invite_button", timeout))


def _downloads(app):
    """{file name: modified-time (epoch seconds)} of the device Downloads folder."""
    out = {}
    for line in app._adb("shell", "stat", "-c", "%Y %n", "/sdcard/Download/*").splitlines():
        m = re.match(r"(\d+) (.+)$", line.strip())
        if m:
            out[m.group(2).rsplit("/", 1)[-1]] = int(m.group(1))
    return out


def download_template(app):
    """Tap 'Member Template Download'. The app hands the file to Chrome, so the runner waits for a template file that is NEWER
    than the tap, brings Alumnye back, and pulls the file. Returns the local path of the template or None."""
    from . import testdata
    try:
        t0 = int((app._adb("shell", "date", "+%s") or "0").strip() or 0)
    except ValueError:
        t0 = 0
    app.tap("download_template", "download the member template")
    fresh, end = {}, time.time() + 20
    while time.time() < end and not fresh:
        time.sleep(1.5)
        fresh = {n: t for n, t in _downloads(app).items() if "template" in n.lower() and t >= t0 - 2 and not n.endswith((".crdownload", ".pending"))}
    left = app.return_to_app("after 'Member Template Download'")
    present = {n for n in _downloads(app) if "template" in n.lower()}
    app.soft_check(bool(fresh), "'Member Template Download' must save a template file to the device Downloads folder"
                   + (" (an older copy is there, nothing new arrived)" if present else ""))
    app.notes.append(f"template download: {', '.join(sorted(fresh)) or 'no fresh file'}{' (the app was left for the browser and recovered)' if left else ''}")
    name = max(fresh, key=fresh.get) if fresh else (sorted(present)[-1] if present else None)
    if not name:
        return None
    local = testdata.TEMPLATE_DIR / name
    local.parent.mkdir(parents=True, exist_ok=True)
    app._adb("pull", f"/sdcard/Download/{name}", str(local))
    return str(local) if local.exists() else None


# ------------------------------------------------------------------ bulk upload / members list (GRP-012..015)
ERR_TEXT = r"invalid|error|missing|required|failed|skipped|not allowed|unsupported|format|duplicate|no members|empty|incorrect|must"


def open_upload_tab(app):
    """Add Members screen of the latest group, on the Upload tab (never taps the tab twice if it is already open)."""
    app.return_to_app("before the upload step")
    if not app.visible("tab_upload", 1.5):
        open_add_members(app)
    app.tap("tab_upload", "open the Upload tab")
    time.sleep(0.5)


_SIGNALS = ("//*[contains(@text,'List of Members') or contains(@text,'Confirm Import') or contains(@text,'Validation Errors') or contains(@text,'No records') "
            "or contains(@text,'not supported') or contains(@text,'Invalid') or contains(@text,'required') "
            "or contains(@content-desc,'List of Members') or contains(@content-desc,'Confirm Import')]")
_ERRORISH = re.compile(r"validation errors|^invalid |at least one|no records|is required|not supported|unsupported|duplicate|failed|row \d+", re.I)


def upload_file(app, path, required=True):
    """Tap the Upload area, pick `path` from local storage and read what the app shows - with a few targeted lookups, not full screen
    reads (a 200-row preview makes a full read take ~10 s). Returns None if the picker would not take the file, else
    {'preview': bool, 'errors': [texts]}."""
    name = path.replace("\\", "/").rsplit("/", 1)[-1]
    if not choose_file(app, name, path, required):
        return None
    end, els = time.time() + 12, []
    while time.time() < end and not els:
        els = app.d.find_elements("xpath", _SIGNALS)
        if not els:
            time.sleep(0.5)
    errors = []
    for e in els[:12]:
        try:
            t = (e.text or e.get_attribute("content-desc") or "").strip()
        except Exception:
            continue
        if t and _ERRORISH.search(t) and t not in errors:
            errors.append(t)
    preview = app.has_text("List of Members", 1) or app.has_text("Confirm Import", 1)
    for t in errors:
        app.messages.append({"trigger": f"uploaded {name}", "text": t, "where": "on-screen"})
    return {"preview": preview, "errors": errors}


def reset_after_upload(app):
    """Leave a preview / error screen the straight way (its own Cancel button) and be on the Upload tab for the next file."""
    if not app.wait_foreground(8):
        app.return_to_app("after an upload")
    if app.visible("upload_cancel", 1.5) and app.has_text("Confirm Import", 0.5):
        app.tap("upload_cancel", "cancel the import preview")
        time.sleep(0.6)
    if not app.visible("choose_file_button", 1.5):
        open_upload_tab(app)


def read_members(app, max_swipes=6):
    """The Members tab as data: member count from the tab, accepted members (name, role) and pending invitees (text, has-Remind),
    scrolling to the end. Used to verify numbers against lists."""
    from . import healer
    out = {"count": None, "accepted": [], "pending": [], "pending_header": False}
    seen_sig, swipes = None, 0
    size = app.d.get_window_size()
    for _ in range(max_swipes + 1):
        nodes = healer.snapshot(app.d.page_source, app.platform)
        for n in nodes:
            m = re.match(r"^members,\s*(\d+)$", n.label.strip(), re.I)
            if m and out["count"] is None:
                out["count"] = int(m.group(1))
        header = next((n for n in nodes if n.label.strip() == "PENDING ACCEPTANCE"), None)
        out["pending_header"] = out["pending_header"] or header is not None
        for n in nodes:
            lab = n.label.strip()
            m = re.match(r"^([^,\uf000-\uf8ff]+), ([A-Za-z][A-Za-z \-]*)$", lab)
            if n.clickable and m and 850 < n.cy < size["height"] * 0.9 and m.group(1).lower() not in ("members", "events", "home", "new group", "my account"):
                if (header is None or n.cy < header.cy) and (m.group(1), m.group(2)) not in out["accepted"]:
                    out["accepted"].append((m.group(1), m.group(2)))
        for r in [n for n in nodes if n.clickable and n.label.strip().lower() == "remind"]:
            near = [x.label.strip() for x in nodes if x is not r and x.label and abs(x.cy - r.cy) < 150 and x.cx < r.cx and not x.clickable and x.cy < size["height"] * 0.9
                    and not re.search(r"^pending acceptance$|[\uf000-\uf8ff]", x.label.strip(), re.I)]
            text = " | ".join(near)
            if text and not any(p["text"] == text for p in out["pending"]):
                out["pending"].append({"text": text, "remind": True})
        sig = hash(tuple(n.label for n in nodes))
        if sig == seen_sig:
            break
        seen_sig = sig
        app.swipe_up()
        swipes += 1
        time.sleep(0.4)
    for _ in range(swipes):                                           # leave the list scrolled back to the top
        app.swipe_down()
    return out


def open_members_list(app, group=None):
    """Open a group (the latest the tests created, or `group`) and tap its Members tab. Returns the count shown on the tab."""
    open_group(app, group)
    tab = app.screen_has(r"^members,?\s*\d+", timeout=3)
    count = int(re.search(r"\d+", tab).group()) if tab else None
    app.tap("members_tab", "open the Members list")
    time.sleep(1.0)
    return count


def anchor_members_snapshot(app, sync):
    """Anchor device: open the journey's group, tap Members, and read count / accepted names / pending invitees."""
    open_members_list(app, sync.data["group"])
    return read_members(app)


def _pending_has(data, email):
    return any(email.lower() in p["text"].lower() for p in data["pending"])


def anchor_verify_members(app, sync, before, joined, label):
    """Anchor device, after the member decided: the Members count must equal the accepted-names list; if the member joined the
    count is +1 and their name is in the list and they have left Pending (no Remind); if not, nothing may have changed."""
    now = anchor_members_snapshot(app, sync)
    email, name = sync.data["member_email"], sync.data.get("member_name")
    names = [n for n, _ in now["accepted"]]
    app.notes.append(f"{label}: count {before['count']} -> {now['count']}; accepted names {names}; pending has member: {_pending_has(now, email)}")
    app.soft_check(now["count"] == len(now["accepted"]), f"{label}: the Members count ({now['count']}) must equal the accepted names list ({len(now['accepted'])}: {', '.join(names)})")
    if joined:
        app.soft_check(before["count"] is not None and now["count"] == before["count"] + 1, f"{label}: the member count must go up by one after acceptance ({before['count']} -> {now['count']})")
        if name:
            app.soft_check(any(name.lower() == n.lower() for n in names), f"{label}: '{name}' must be in the accepted names list (list: {', '.join(names)})")
        app.soft_check(not _pending_has(now, email), f"{label}: an accepted member must no longer be under PENDING ACCEPTANCE (no Remind button)")
    else:
        app.soft_check(now["count"] == before["count"], f"{label}: the member count must not change when the invitation is not accepted ({before['count']} -> {now['count']})")
        if name:
            app.soft_check(not any(name.lower() == n.lower() for n in names), f"{label}: '{name}' must not be in the accepted names list")
    return now


def remind_member(app, email):
    """On the open Members list: tap Remind on the row of the pending member with this e-mail. Returns the messages shown."""
    from . import healer
    nodes = healer.snapshot(app.d.page_source, app.platform)
    row = next((n for n in nodes if email.lower() in n.label.lower() and not n.clickable), None)
    if row is None:
        app.soft_check(False, f"{email} must be listed under PENDING ACCEPTANCE before it can be reminded")
        return []
    remind = min((n for n in nodes if n.clickable and n.label.strip().lower() == "remind"), key=lambda n: abs(n.cy - row.cy), default=None)
    if remind is None or abs(remind.cy - row.cy) > 160:
        app.soft_check(False, f"the pending member {email} must have a Remind button")
        return []
    before = app.mark()
    app.wait_banner_clear()
    app.tap_xy(remind.cx, remind.cy)
    return app.watch_messages(f"tapped Remind for {email}", before, seconds=4)


def confirm_import(app, name):
    """Click 'Confirm Import' on the preview (if the file reached one) and catch the banner at the top of the app.
    Returns (clicked, [texts shown after the click])."""
    if not app.visible("confirm_import", 2):
        return False, []
    app.tap("confirm_import", f"confirm the import of {name}")
    return True, app.watch_banner(f"confirmed the import of {name}", seconds=15)


# ------------------------------------------------------------------ events (BF3: event creation, categories, tiles)
# Source: Release v1.4 "Event Category-based Tiles & List" (the three tile sets), Walkthrough 9.1-9.4, FSD Anchor 5.2.
CATEGORIES = ["Reunion", "Sports", "Networking", "Professional", "Social", "Cultural", "Other"]
COMMON_CATEGORIES = ["Networking", "Professional", "Social", "Cultural", "Other"]
REUNION_TILES = ["Poll", "CostGPT", "Itinerary", "Launch RSVP", "Travel", "Preference", "Library", "Payment"]
SPORTS_TILES = ["Poll", "Launch RSVP", "Golf", "Library", "Payment"]
COMMON_TILES = ["Poll", "Launch RSVP", "Library", "Payment"]
ALL_TILES = ["Poll", "CostGPT", "Itinerary", "Launch RSVP", "Travel", "Preference", "Library", "Payment", "Golf"]
TILE_PATTERNS = {                       # tile name -> label patterns (whole label, lower case) the app may use for it
    "Poll": r"polls?", "CostGPT": r"cost ?gpt|cost estimat(or|ion)", "Itinerary": r"itinerary",
    "Launch RSVP": r"launch rsvp|rsvp( launch)?", "Travel": r"travel", "Preference": r"(travel )?preferences?",
    "Library": r"(media )?library", "Payment": r"payments?", "Golf": r"golf",
}
STATUS_WORDS = r"draft|planning|upcoming|poll active|decision finalized|cost estimation|rsvp open|payment tracking open|executed"


def tiles_for(category):
    return REUNION_TILES if category == "Reunion" else SPORTS_TILES if category == "Sports" else COMMON_TILES


def _glyphless(text):
    return re.sub(r"[-]", "", text).strip()


def canon_tile(label):
    """The tile a label stands for ('Cost GPT' -> 'CostGPT'), or None. Only short labels count, so a sentence never matches."""
    if not label or len(label) > 40:
        return None
    for part in [p.strip().lower() for p in _glyphless(label).split(",") if p.strip()]:
        for name, pat in TILE_PATTERNS.items():
            if re.fullmatch(pat, part):
                return name
    return None


def read_tiles(app, max_swipes=4):
    """The tiles shown on the open Event Home, as an ordered list of canonical names (scrolls to the end, then back to the top)."""
    from . import healer
    found, last, swipes = [], None, 0
    for _ in range(max_swipes + 1):
        for n in healer.snapshot(app.d.page_source, app.platform):
            t = canon_tile(n.label)
            if t and t not in found:
                found.append(t)
        sig = hash(tuple(n.label for n in healer.snapshot(app.d.page_source, app.platform)))
        if sig == last:
            break
        last = sig
        app.swipe_up()
        swipes += 1
        time.sleep(0.3)
    for _ in range(swipes):
        app.swipe_down()
    return found


def check_tiles(app, category, found, label=""):
    """Exact comparison with the category's documented tile set: nothing missing, nothing extra, no tile of another category."""
    want = tiles_for(category)
    missing = [t for t in want if t not in found]
    extra = [t for t in found if t not in want]
    app.notes.append(f"{label or category}: tiles shown = {', '.join(found) or 'none'}")
    app.soft_check(not missing, f"{label or category} event must show the tile(s) {', '.join(missing)} (shown: {', '.join(found) or 'none'})")
    app.soft_check(not extra, f"{label or category} event must NOT show {', '.join(extra)} (allowed: {', '.join(want)})")
    app.soft_check(len(found) == len(want), f"{label or category} event must show exactly {len(want)} tiles (shown {len(found)}: {', '.join(found)})")
    return not missing and not extra


def new_event(category, title=None, desc="Automated test event for the category tile check."):
    stamp = time.strftime("%m%d%H%M%S")
    # the category name is deliberately NOT in the title, so a label match on the category can never be satisfied by the title
    return {"title": title or f"QA Evt {stamp} {category[:3].upper()}", "category": category, "desc": desc}


def group_ready(app, members=2):
    """PRECONDITION of the Events module (the chain Auth -> Group -> Members -> Event): a user is signed in, owns a group that is
    listed on Anchor Home, and that group already has members added (invited) - an event is only raised for a group with people in it.
    Reuses the latest test group when it is still there and has members; otherwise creates a group and invites `members` people."""
    precondition_signed_in(app)
    ready = app.__dict__.setdefault("ready_groups", set())
    groups = testdata.load_groups()
    name = groups[-1]["name"] if groups else None
    if name and name in ready:
        return name
    listed = False
    if name:
        to_anchor_home(app)
        listed = app._try([f"textc:{name}"], 4) is not None
    if not listed:                                                # no group of this user yet: step 2 of the chain
        group = create_group(app, testdata.new_group())
        name = group["name"]
        app.notes.append(f"precondition: created group '{name}'")
    if not testdata.load_invites().get(name):                    # step 3: add members
        open_add_members(app)
        added = []
        for _ in range(members):
            email = testdata.new_person()["email"]
            if send_invite(app, email) == "sent":
                added.append(email)
            time.sleep(1.1)                                       # new_person() stamps seconds: keep the e-mails unique
        app.notes.append(f"precondition: added {len(added)} member(s) to '{name}': {', '.join(added)}")
        app.soft_check(len(added) >= 1, "precondition failed: no member could be added to the group, so no event can be raised")
        back_to_anchor_home(app)
    ready.add(name)
    return name


def new_group_ready(app, members=2):
    """A brand-new group that already has members (for scenarios that need a group without earlier events)."""
    precondition_signed_in(app)
    group = create_group(app, testdata.new_group())
    app.__dict__.setdefault("ready_groups", set())
    open_add_members(app)
    for _ in range(members):
        send_invite(app, testdata.new_person()["email"])
        time.sleep(1.1)
    back_to_anchor_home(app)
    app.ready_groups.add(group["name"])
    app.notes.append(f"precondition: new group '{group['name']}' with {members} member(s) added")
    return group


def open_event_form(app, group=None):
    """Latest group -> Add Event -> the Event form. The group must exist and have members (group_ready)."""
    if group is None:
        group_ready(app)
    open_group(app, group)
    app.tap("add_event_button", "open the Event form")
    app.wait_screen("event_title_field", "the Event form is shown")


def choose_category(app, category):
    """Open the category dropdown (bottom sheet) and pick `category`. Returns True if the option existed."""
    app.tap("event_category_dropdown", "open the category list")
    opt = app._try([f"btnx:{category}", f"textc:{category}"], 4)
    if opt is None:
        app.soft_check(False, f"the category list must offer '{category}'")
        app.back()
        return False
    opt.click()
    time.sleep(0.5)
    return True


def category_options(app):
    """The options the category dropdown offers (names only), read from the open bottom sheet; the sheet is closed again."""
    before = {l.lower() for l in app.labels()}
    app.tap("event_category_dropdown", "open the category list")
    time.sleep(0.8)
    opts = [l for l in app.labels() if l.lower() not in before and 2 <= len(_glyphless(l)) <= 25]
    app.back()
    time.sleep(0.4)
    return list(dict.fromkeys(_glyphless(o) for o in opts))


def fill_event(app, ev, category=True, desc=True):
    app.type("event_title_field", ev["title"], "enter the event title")
    if desc and ev.get("desc") and app.visible("event_description_field", 1):
        app.type("event_description_field", ev["desc"], "enter the event description")
    if category and ev.get("category"):
        choose_category(app, ev["category"])


def save_event(app, trigger="saved the event", unblock=True):
    """Tap Save; required fields the form still wants (for example the dates) are filled by the runner. Returns the banner texts."""
    app.wait_banner_clear()
    app.tap("event_save_button", trigger, unblock=unblock)
    return app.watch_banner(trigger, seconds=4, settle=0.8)


def create_event(app, ev, group=None):
    """The full user path: Add Event -> fill -> Save -> back on Group Details. The event is recorded for later checks."""
    open_event_form(app, group)
    fill_event(app, ev)
    save_event(app, f"saved the {ev['category']} event '{ev['title']}'")
    app.wait_screen("group_details_marker", "Save returns to Group Details")
    testdata.save_event(testdata.load_groups()[-1]["name"] if testdata.load_groups() else "", ev)
    return ev


def show_events_tab(app):
    if app.visible("events_tab", 1.5):
        app.tap("events_tab", "open the Events tab")
        time.sleep(0.5)


def event_on_list(app, title, timeout=4):
    show_events_tab(app)
    return app._try([f"textc:{title[:30]}"], timeout) is not None


def open_event(app, title):
    """Group Details -> Events tab -> the event card -> Event Home."""
    show_events_tab(app)
    for _ in range(3):
        el = app._try([f"textc:{title[:30]}"], 5)
        if el is None:
            app.soft_check(False, f"the event '{title}' must be listed on the group's Events tab")
            return False
        try:
            el.click()
            break
        except WebDriverException:
            time.sleep(0.5)
    app.wait_screen("event_home_marker", "Event Home is shown")
    return True


def to_group_details(app):
    """Back out of an event / form to the Group Details of the latest group."""
    for _ in range(4):
        if app.visible("add_event_button", 1):
            return
        app.back()
        time.sleep(0.5)
    open_group(app)


def status_badge(app):
    """The lifecycle status text on the open Event Home / event card ('' if none shown)."""
    return app.screen_has(rf"^({STATUS_WORDS})$", timeout=2)


def open_tile(app, tile):
    """Tap the Event Home tile `tile`; returns (screen_changed, error_text, heading). Navigation only - nothing is saved."""
    from . import healer
    before = set(app.labels())
    node = next((n for n in healer.snapshot(app.d.page_source, app.platform) if canon_tile(n.label) == tile and n.clickable), None) \
        or next((n for n in healer.snapshot(app.d.page_source, app.platform) if canon_tile(n.label) == tile), None)
    if node is None:
        app.swipe_up()
        node = next((n for n in healer.snapshot(app.d.page_source, app.platform) if canon_tile(n.label) == tile), None)
    if node is None:
        return False, f"the '{tile}' tile could not be found", ""
    app.tap_xy(node.cx, node.cy)
    time.sleep(1.5)
    app.return_to_app(f"after opening the {tile} tile")
    labels = app.labels()
    err = next((l for l in labels if re.search(r"something went wrong|error|failed|unable to|try again|not found|crash", l, re.I)), "")
    heading = next((l for l in labels if l not in before and 2 < len(l) < 40), "")
    return set(labels) != before, err, heading


def back_to_event_home(app):
    for _ in range(3):
        if app.visible("event_home_marker", 1):
            return True
        app.back()
        time.sleep(0.6)
    return app.visible("event_home_marker", 2)


def filled_inputs(app):
    """Text fields on the open form that hold something other than their placeholder."""
    return [n.label for n in app.inputs() if n.label.strip() and n.label.strip() != (n.hint or "").strip()]


def y_of(app, text):
    """Vertical position of the first on-screen label containing `text` (None if not shown)."""
    from . import healer
    for n in sorted(healer.snapshot(app.d.page_source, app.platform), key=lambda n: n.cy):
        if text.lower() in n.label.lower():
            return n.cy
    return None


def edit_event(app, title, new_title=None, category=None):
    """Event Home -> Edit -> change the title and/or category -> Save -> back on Group Details."""
    if not open_event(app, title):
        return False
    app.tap("event_edit_button", "open the event for editing")
    app.wait_screen("event_title_field", "the Event form opens for editing")
    if new_title:
        app.type("event_title_field", new_title, "replace the event title")
    if category:
        choose_category(app, category)
    save_event(app, f"saved the edited event ({new_title or title})")
    app.wait_screen("group_details_marker", "Save returns to Group Details after an edit")
    return True


def read_listing(app, titles, max_swipes=8):
    """Which category each event title is listed under on the Events tab, read top to bottom while scrolling.
    A category heading (or a category label on the card) that PRECEDES the title - or sits within 90 px of it - is its category.
    Returns {title: [candidate categories]}."""
    from . import healer
    cats = {c.lower(): c for c in CATEGORIES}
    result = {t: [] for t in titles}
    carry, last = None, None
    for _ in range(max_swipes + 1):
        nodes = sorted([n for n in healer.snapshot(app.d.page_source, app.platform) if n.label], key=lambda n: (n.cy, n.cx))
        labels_sig = hash(tuple(n.label for n in nodes))
        for n in nodes:
            low = _glyphless(n.label).lower().strip(", ")
            if low in cats:
                carry = (cats[low], n.cy)
                continue
            for t in titles:
                if t[:30].lower() in n.label.lower() and carry is not None:
                    prev_cat, prev_y = carry
                    near = [cats[_glyphless(m.label).lower().strip(", ")] for m in nodes
                            if _glyphless(m.label).lower().strip(", ") in cats and abs(m.cy - n.cy) <= 90]
                    for c in [prev_cat] + near:
                        if c not in result[t]:
                            result[t].append(c)
        if labels_sig == last:
            break
        last = labels_sig
        app.swipe_up()
        time.sleep(0.3)
    return result

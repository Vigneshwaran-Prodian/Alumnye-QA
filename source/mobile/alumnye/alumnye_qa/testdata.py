"""Valid, realistic test data. Emails are yopmail; OTPs are typed by the tester when prompted."""
import json
import os
import random
import threading
import time

from . import config

FIRST = ["Arjun", "Meera", "Karthik", "Divya", "Rohan", "Anita", "Vivek", "Sneha"]
LAST = ["Sharma", "Iyer", "Nair", "Reddy", "Menon", "Kapoor", "Verma", "Pillai"]
USERS_FILE = config.DATA_DIR / "test_users.json"


def new_person() -> dict:
    f, l = random.choice(FIRST), random.choice(LAST)
    stamp = time.strftime("%m%d%H%M%S")
    return {"first": f, "last": l, "email": f"{f}.{l}.{stamp}@yopmail.com".lower()}


def mobile(cfg: dict) -> str:
    m = os.environ.get("ALUMNYE_TEST_MOBILE") or cfg.get("test_mobile")
    if not m:
        m = input("\n[input needed] Enter a 10-digit mobile number that can receive the OTP SMS: ").strip()
    return m


def common_otp() -> str:
    """Fixed OTP for test accounts (backend must accept it): env ALUMNYE_OTP, else config.json 'common_otp'."""
    return os.environ.get("ALUMNYE_OTP") or config.load().get("common_otp", "")


def wrong_otp() -> str:
    """A deliberately wrong code that can never equal the common OTP."""
    return "000000" if common_otp() != "000000" else "999999"


def otp(label: str) -> str:
    code = common_otp()
    if code:
        print(f"    [otp] using the configured common OTP (no prompt)")
        return code
    return input(f"\n[input needed] {label}\n  Enter the OTP you received (then press Enter): ").strip()


def save_user(user: dict):
    users = load_users()
    users.append(user)
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    USERS_FILE.write_text(json.dumps(users, indent=2), encoding="utf-8")


def load_users() -> list:
    if USERS_FILE.exists():
        return json.loads(USERS_FILE.read_text(encoding="utf-8") or "[]")
    return []


GROUPS_FILE = config.DATA_DIR / "test_groups.json"


def new_group() -> dict:
    return {"name": f"QA Group {time.strftime('%m%d%H%M%S')}", "desc": "Automated test group for the Alumni 2026 batch."}


def save_group(group: dict):
    groups = load_groups()
    groups.append(group)
    GROUPS_FILE.parent.mkdir(parents=True, exist_ok=True)
    GROUPS_FILE.write_text(json.dumps(groups, indent=2), encoding="utf-8")


def load_groups() -> list:
    if GROUPS_FILE.exists():
        return json.loads(GROUPS_FILE.read_text(encoding="utf-8") or "[]")
    return []


def make_members_csv(name: str, valid: bool = True) -> str:
    """Bulk-upload test file (columns follow the docs: names, email, mobile). Returns the local path."""
    people = [new_person() for _ in range(3)]
    mob = lambda: "9" + "".join(random.choice("0123456789") for _ in range(9))
    rows = [["First Name", "Last Name", "Email", "Mobile"]]
    if valid:
        rows += [[p["first"], p["last"], p["email"], mob()] for p in people]
    else:
        rows += [[people[0]["first"], people[0]["last"], people[0]["email"], mob()],
                 [people[1]["first"], people[1]["last"], "not-an-email", mob()],
                 ["", people[2]["last"], people[2]["email"], mob()]]
    path = config.DATA_DIR / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(",".join(r) for r in rows) + "\n", encoding="utf-8")
    return str(path)


ACCOUNTS_FILE = config.DATA_DIR / "journey_accounts.json"


def journey_account(role: str):
    """The e-mail registered for a journey role ('member'), or None until it has been registered."""
    if ACCOUNTS_FILE.exists():
        return json.loads(ACCOUNTS_FILE.read_text(encoding="utf-8") or "{}").get(role)
    return None


def save_journey_account(role: str, person: dict):
    data = json.loads(ACCOUNTS_FILE.read_text(encoding="utf-8") or "{}") if ACCOUNTS_FILE.exists() else {}
    data[role] = person
    ACCOUNTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    ACCOUNTS_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


TEMPLATE_DIR = config.DATA_DIR / "templates"
MEMBERS_SHEET_STEM = "members_200"           # fixed name: later scenarios reuse the same sheet
SHEET_EMAIL = "qa.member{n:03d}@yopmail.com"


def _member_row(headers, n):
    """One valid row for the template's own columns (matched by header words)."""
    row = []
    for h in headers:
        k = (h or "").lower()
        if "email" in k or "e-mail" in k:
            row.append(SHEET_EMAIL.format(n=n))
        elif "first" in k:
            row.append(f"Test{n:03d}")
        elif "last" in k or "surname" in k:
            row.append("Member")
        elif "name" in k:
            row.append(f"Test{n:03d} Member")
        elif "mobile" in k or "phone" in k or "contact" in k:
            row.append(f"9{8000000 + n:09d}"[:10])
        else:
            row.append("")
    return row


def build_members_sheet(template_path=None, count=200):
    """Sample bulk-upload sheet: the downloaded template's own headers, `count` valid members with yopmail test addresses
    (qa.member001@yopmail.com ...). Same file name every time so every scenario can reuse it. Returns the local path."""
    import csv
    DATA_DIR = config.DATA_DIR
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ext = (os.path.splitext(template_path)[1].lower() if template_path else ".csv")
    if ext in (".xlsx", ".xlsm"):
        import openpyxl
        wb = openpyxl.load_workbook(template_path)
        ws = wb.active
        header_row = next((r for r in range(1, 6) if sum(1 for c in ws[r] if c.value) >= 2), 1)
        headers = [str(c.value or "") for c in ws[header_row]]
        for r in range(header_row + 1, ws.max_row + 1):          # drop the template's sample rows
            for c in ws[r]:
                c.value = None
        for n in range(1, count + 1):
            for col, v in enumerate(_member_row(headers, n), start=1):
                ws.cell(row=header_row + n, column=col, value=v)
        out = DATA_DIR / f"{MEMBERS_SHEET_STEM}.xlsx"
        wb.save(out)
        return str(out)
    headers = ["First Name", "Last Name", "Email", "Mobile"]
    if template_path and ext == ".csv":
        with open(template_path, encoding="utf-8-sig", newline="") as f:
            first = next(csv.reader(f), None)
            headers = first or headers
    out = DATA_DIR / f"{MEMBERS_SHEET_STEM}.csv"
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        for n in range(1, count + 1):
            w.writerow(_member_row(headers, n))
    return str(out)


def members_sheet(count=200):
    """The shared 200-member sheet, built from the downloaded template on first use."""
    for ext in (".xlsx", ".csv"):
        p = config.DATA_DIR / f"{MEMBERS_SHEET_STEM}{ext}"
        if p.exists():
            return str(p)
    tpl = sorted(TEMPLATE_DIR.glob("*")) if TEMPLATE_DIR.exists() else []
    return build_members_sheet(str(tpl[-1]) if tpl else None, count)


# ---------------------------------------------------------------- bulk-upload file sets (one folder per scenario)
UPLOAD_DIR = config.DATA_DIR / "upload-files"
HEADERS = ["First Name", "Last Name", "Email", "Phone Number"]       # the app's own template (Group_Member_Upload_Template.xlsx)


def _template_headers():
    tpl = sorted(TEMPLATE_DIR.glob("*.xlsx")) if TEMPLATE_DIR.exists() else []
    if tpl:
        try:
            import openpyxl
            ws = openpyxl.load_workbook(tpl[-1]).active
            row = [str(c.value) for c in ws[1] if c.value]
            if len(row) >= 3:
                return row
        except Exception:
            pass
    return HEADERS


def _write(path, headers, rows):
    import csv
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".xlsx":
        import openpyxl
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(headers)
        for r in rows:
            ws.append(r)
        wb.save(path)
    else:
        with open(path, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(headers)
            w.writerows(rows)
    return str(path)


def _stamp():
    return time.strftime("%m%d%H%M%S")


def _rows(prefix, stamp, n):
    """n valid members whose e-mail AND phone are unique to this run (so a re-import never collides with an earlier one)."""
    base = int(stamp) % 10000
    return [[f"{prefix}{i:03d}", "Member", f"qa.{prefix.lower()}{stamp}.{i:03d}@yopmail.com", f"9{base:04d}{i:05d}"] for i in range(1, n + 1)]


def _xlsx_from_template(rows, headers, out):
    """The app's own template, emptied and filled with `rows` (keeps its formatting); plain workbook if no template is on disk."""
    import openpyxl
    tpl = sorted(TEMPLATE_DIR.glob("*.xlsx")) if TEMPLATE_DIR.exists() else []
    wb = openpyxl.load_workbook(tpl[-1]) if tpl else openpyxl.Workbook()
    ws = wb.active
    for r in range(2, ws.max_row + 1):
        for c in ws[r]:
            c.value = None
    if not tpl:
        ws.append(headers)
    for n, row in enumerate(rows, start=2):
        for col, v in enumerate(row, start=1):
            ws.cell(row=n, column=col, value=v)
    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return str(out)


def upload_files(scenario_id, stamp=None):
    """A NEW set of files for the scenario on every run, as [(path, expectation, why, token)] - `token` is text the app must show
    for that file. Written to data/upload-files/<scenario>/<run stamp>/ and kept there so a person can open them; e-mails and phones
    carry the stamp, so no two runs share a member."""
    stamp = stamp or _stamp()
    h = _template_headers()
    d = UPLOAD_DIR / scenario_id / stamp
    out = []
    if scenario_id == "GRP-012":
        big = _rows("Mem", stamp, 200)
        out.append((_xlsx_from_template(big, h, d / f"valid_200_members_{stamp}.xlsx"), "accepted",
                    "template format (.xlsx), 200 valid members", big[0][2]))
        small = _rows("Csv", stamp, 5)
        out.append((_write(d / f"valid_5_members_{stamp}.csv", h, small), "accepted", ".csv format, 5 valid members", small[0][2]))
        one = f"qa.onlyemail{stamp}@yopmail.com"
        out.append((_write(d / f"valid_email_or_phone_only_{stamp}.csv", h, [["Only", "Email", one, ""], ["Only", "Phone", "", f"9{int(stamp) % 10000:04d}99999"]]),
                    "accepted", "one row with only an e-mail and one with only a phone (either is enough)", one))
    elif scenario_id == "GRP-013":
        good = _rows("Mix", stamp, 2)
        dup = f"qa.dup{stamp}@yopmail.com"
        out += [
            (_xlsx_from_template(good + [["Bad", "Email", "not-an-email", "9000000001"], ["Bad", "Email2", "abc@", "9000000002"]], h, d / f"invalid_email_format_{stamp}.xlsx"),
             "rejected", "rows with malformed e-mail addresses", "not-an-email"),
            (_write(d / f"missing_first_name_{stamp}.csv", h, good + [["", "Member", f"qa.nofirst{stamp}@yopmail.com", "9000000003"]]), "rejected", "a row without a first name", None),
            (_write(d / f"missing_email_and_phone_{stamp}.csv", h, good + [["No", "Contact", "", ""]]), "rejected", "a row with neither e-mail nor phone (the app requires at least one)", "Email or Phone"),
            (_write(d / f"bad_phone_number_{stamp}.csv", h, good + [["Bad", "Phone", f"qa.badphone{stamp}@yopmail.com", "12ab"]]), "rejected", "a row with a malformed phone number", "12ab"),
            (_write(d / f"duplicate_emails_{stamp}.csv", h, good + [["Dup", "One", dup, "9000000005"], ["Dup", "Two", dup, "9000000006"]]), "rejected", "the same e-mail twice in one file", None),
            (_write(d / f"wrong_columns_{stamp}.csv", ["Name", "Mail", "Number"], [["Wrong Columns", f"qa.wrong{stamp}@yopmail.com", "9000000007"]]), "rejected", "columns that do not match the template", "Email or Phone"),
            (_write(d / f"headers_only_empty_{stamp}.csv", h, []), "rejected", "a file with headers and no members", "No records"),
        ]
        txt = d / f"unsupported_format_{stamp}.txt"
        d.mkdir(parents=True, exist_ok=True)
        txt.write_text("First Name,Last Name,Email,Phone Number\nTxt,Member,qa.txt" + stamp + "@yopmail.com,9000000008\n", encoding="utf-8")
        out.append((str(txt), "rejected", "a .txt file (only .xlsx / .csv are allowed)", None))
    return out


def emails_in(path):
    """E-mail addresses inside an uploaded .csv / .xlsx (so the Members list can be verified against what was imported)."""
    import csv
    found = []
    if str(path).lower().endswith(".xlsx"):
        import openpyxl
        for row in openpyxl.load_workbook(path).active.iter_rows(min_row=2, values_only=True):
            found += [str(v) for v in row if v and "@" in str(v)]
    else:
        with open(path, encoding="utf-8", newline="") as f:
            for row in csv.reader(f):
                found += [v for v in row if "@" in v]
    return found


INVITES_FILE = config.DATA_DIR / "test_invites.json"


def save_invite(group_name, email):
    """Remember every e-mail the tests invited into a group, so the Members list can be verified against it."""
    data = load_invites()
    data.setdefault(group_name, [])
    if email not in data[group_name]:
        data[group_name].append(email)
    INVITES_FILE.parent.mkdir(parents=True, exist_ok=True)
    INVITES_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_invites():
    if INVITES_FILE.exists():
        return json.loads(INVITES_FILE.read_text(encoding="utf-8") or "{}")
    return {}


WORDINGS_FILE = config.DATA_DIR / "splash-wordings.json"


def load_wordings():
    if WORDINGS_FILE.exists():
        return json.loads(WORDINGS_FILE.read_text(encoding="utf-8") or "{}")
    return {}


def save_wordings(data):
    WORDINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    WORDINGS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


EVENTS_FILE = config.DATA_DIR / "test_events.json"


def save_event(group_name, ev):
    """Remember every event the tests created, per group, so lists and counts can be verified against it."""
    data = load_events()
    data.setdefault(group_name, [])
    if ev["title"] not in [e["title"] for e in data[group_name]]:
        data[group_name].append(dict(ev, created=time.strftime("%Y-%m-%d %H:%M:%S")))
    EVENTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    EVENTS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_events():
    if EVENTS_FILE.exists():
        return json.loads(EVENTS_FILE.read_text(encoding="utf-8") or "{}")
    return {}

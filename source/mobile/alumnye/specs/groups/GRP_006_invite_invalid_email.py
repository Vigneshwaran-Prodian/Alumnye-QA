import re

from alumnye_qa import flows, testdata

META = dict(id="GRP-006", title="Invite rejects an invalid email format with 'Please enter a valid email format'", type="Negative", fresh=False)

BAD = ["abc@", "plainaddress", "no spaces@yopmail.com", "a@b", "@yopmail.com"]
EXPECTED = r"valid email format"


def run(app):
    flows.open_add_members(app)
    for bad in BAD:
        result = flows.send_invite(app, bad)
        shown = " / ".join(app.last_msgs) or "(no message)"
        app.soft_check(result in ("blocked", "error"), f"'{bad}' must not be accepted as an invitation email (result: {result}; message: {shown})")
        if result == "error":
            app.soft_check(any(re.search(EXPECTED, m, re.I) for m in app.last_msgs),
                           f"'{bad}': the message must say 'Please enter a valid email format' (shown: {shown})")

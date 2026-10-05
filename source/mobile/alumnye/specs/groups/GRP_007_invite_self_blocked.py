from alumnye_qa import flows, testdata
from alumnye_qa.session import Blocked

META = dict(id="GRP-007", title="Anchor cannot invite their own email address", type="Negative", fresh=False)


def run(app):
    mine = flows.current_user_email(app)                        # read from My Account: the account really signed in on the device
    if not mine:
        raise Blocked("could not read the signed-in user's e-mail from My Account")
    app.notes.append(f"signed-in user: {mine}")
    flows.open_add_members(app)
    result = flows.send_invite(app, mine)
    shown = " / ".join(app.last_msgs) or "(no message)"
    app.soft_check(result in ("blocked", "error"), f"the Anchor must not be able to invite their own email {mine} (result: {result}; message: {shown})")

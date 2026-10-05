"""Anchor withdraws a pending invitation before the member answers: the member must not be able to join with it."""
from alumnye_qa import flows
from alumnye_qa.session import Blocked

META = dict(id="JNY-007", title="A withdrawn invitation can no longer be accepted", type="Negative", devices=2)


def anchor(app, sync):
    flows.to_anchor_home(app)
    flows.anchor_creates_group_and_invites(app, sync)
    flows.open_add_members(app)
    el = app.scroll_find("withdraw_invite_button", max_swipes=3)
    if el is None:
        sync.data["withdrawn"] = False
        sync.set("withdraw_done")
        raise Blocked("the app offers no way to withdraw / cancel a pending invitation that the runner could find - confirm whether the feature exists")
    app.tap("withdraw_invite_button", "withdraw the pending invitation", unblock=False)
    if app.visible("confirm_dialog_yes", 1.5):
        app.tap("confirm_dialog_yes", "confirm the withdrawal")
    sync.data["withdrawn"] = True
    sync.set("withdraw_done")


def member(app, sync):
    flows.member_ready(app, sync)
    sync.wait("invite_sent")
    sync.wait("withdraw_done")
    if not sync.data.get("withdrawn"):
        raise Blocked("nothing was withdrawn, so there is nothing to check on the member side")
    app.soft_check(not flows.member_sees_invitation(app, sync, timeout=4), "a withdrawn invitation must not be offered to the member")

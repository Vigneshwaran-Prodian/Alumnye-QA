"""Member rejects; the anchor invites again; the member gets a fresh invitation and accepts (state edge case)."""
from alumnye_qa import flows

META = dict(id="JNY-005", title="After a rejection the anchor can invite again and the member can then accept", type="Edge", devices=2)


def anchor(app, sync):
    flows.to_anchor_home(app)
    flows.anchor_creates_group_and_invites(app, sync)
    sync.wait("rejected")
    result = flows.anchor_invite_again(app, sync)
    app.soft_check(result == "sent", f"a member who rejected must be invitable again (result: {result})")
    sync.set("reinvited")
    sync.wait("member_decided")
    flows.anchor_verify_members(app, sync, sync.data["before"], joined=True, label="after reject, re-invite and acceptance")


def member(app, sync):
    flows.member_ready(app, sync)
    flows.member_open_invitation(app, sync)
    flows.member_decide(app, accept=False)
    sync.set("rejected")
    sync.wait("reinvited")
    app.soft_check(flows.member_sees_invitation(app, sync, timeout=6), "after a new invite the member must be offered the invitation again")
    flows.member_decide(app, accept=True)
    sync.set("member_decided")

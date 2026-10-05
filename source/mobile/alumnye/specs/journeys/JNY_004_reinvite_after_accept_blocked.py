"""Member accepts; the anchor then invites the same person again - must be refused (already a member)."""
from alumnye_qa import flows

META = dict(id="JNY-004", title="Re-inviting a member who already joined is refused", type="Negative", devices=2)


def anchor(app, sync):
    flows.to_anchor_home(app)
    flows.anchor_creates_group_and_invites(app, sync)
    sync.wait("member_decided")
    result = flows.anchor_invite_again(app, sync)
    app.soft_check(result in ("error", "blocked"), f"inviting a member who already joined must be refused (result: {result})")


def member(app, sync):
    flows.member_ready(app, sync)
    flows.member_open_invitation(app, sync)
    flows.member_decide(app, accept=True)
    sync.set("member_decided")

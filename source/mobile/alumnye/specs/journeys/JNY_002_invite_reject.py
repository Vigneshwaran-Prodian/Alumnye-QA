from alumnye_qa import flows

META = dict(id="JNY-002", title="Anchor invites, member rejects: the Anchor's Members count does not change", type="Positive", devices=2)


def anchor(app, sync):
    flows.to_anchor_home(app)
    flows.anchor_creates_group_and_invites(app, sync)
    sync.wait("member_decided")
    flows.anchor_verify_members(app, sync, sync.data["before"], joined=False, label="after rejection")


def member(app, sync):
    flows.member_ready(app, sync)
    flows.member_open_invitation(app, sync)
    flows.member_decide(app, accept=False)
    sync.data["decision"] = "rejected"
    app.restart()
    app.soft_check(not flows.member_sees_invitation(app, sync, timeout=3), "after rejecting, the invitation must no longer be offered to the member")
    sync.set("member_decided")

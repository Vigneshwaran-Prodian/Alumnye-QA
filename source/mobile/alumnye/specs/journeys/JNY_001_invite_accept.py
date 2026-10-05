from alumnye_qa import flows

META = dict(id="JNY-001", title="Anchor invites, member accepts: the Anchor's Members count goes up and the member's name is listed", type="Positive", devices=2)


def anchor(app, sync):
    flows.to_anchor_home(app)
    flows.anchor_creates_group_and_invites(app, sync)             # also records the Members numbers while the member is still Pending
    sync.wait("member_decided")
    flows.anchor_verify_members(app, sync, sync.data["before"], joined=True, label="after acceptance")


def member(app, sync):
    flows.member_ready(app, sync)
    flows.member_open_invitation(app, sync)
    flows.member_decide(app, accept=True)
    sync.data["decision"] = "accepted"
    app.soft_check(bool(app.screen_has(sync.data["group"], r"joined|welcome|group", timeout=5)), "after accepting, the group must be shown to the member")
    sync.set("member_decided")

"""Anchor invites the same pending person twice: second attempt refused (or merged); the member sees ONE invitation."""
from alumnye_qa import flows

META = dict(id="JNY-006", title="Inviting the same pending person twice never creates two invitations", type="Negative", devices=2)


def anchor(app, sync):
    flows.to_anchor_home(app)
    flows.anchor_creates_group_and_invites(app, sync)
    result = flows.anchor_invite_again(app, sync)
    app.soft_check(result in ("error", "blocked"), f"a second invite to a pending invitee must be refused (result: {result})")
    sync.set("second_invite_done")
    sync.wait("member_decided")


def member(app, sync):
    flows.member_ready(app, sync)
    sync.wait("invite_sent")
    sync.wait("second_invite_done")
    flows.member_open_invitation(app, sync)
    entries = [l for l in app.labels() if sync.data["group"].lower() in l.lower()]
    app.soft_check(len(entries) <= 2, f"the member must see one invitation, not one per attempt (saw {len(entries)} entries)")
    flows.member_decide(app, accept=True)
    sync.set("member_decided")

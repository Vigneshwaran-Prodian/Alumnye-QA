from alumnye_qa import flows

META = dict(id="JNY-003", title="Anchor reminds a Pending member from the Members list, the member sees one invitation and accepts; Remind then disappears", type="Positive", devices=2)


def anchor(app, sync):
    flows.to_anchor_home(app)
    flows.anchor_creates_group_and_invites(app, sync)
    flows.open_members_list(app, sync.data["group"])               # the Members tab: Remind exists only on PENDING ACCEPTANCE rows
    texts = flows.remind_member(app, sync.data["member_email"])
    app.soft_check(bool(texts), "tapping Remind must give visible feedback (message / status change)")
    app.notes.append("Remind feedback: " + (" / ".join(texts) or "none"))
    sync.set("reminded")
    sync.wait("member_decided")
    flows.anchor_verify_members(app, sync, sync.data["before"], joined=True, label="after remind + acceptance")


def member(app, sync):
    flows.member_ready(app, sync)
    sync.wait("reminded")
    flows.member_open_invitation(app, sync)
    entries = [l for l in app.labels() if sync.data["group"].lower() in l.lower()]
    app.soft_check(len(entries) <= 2, f"the reminder must not create duplicate invitations (saw {len(entries)} entries)")
    flows.member_decide(app, accept=True)
    sync.set("member_decided")

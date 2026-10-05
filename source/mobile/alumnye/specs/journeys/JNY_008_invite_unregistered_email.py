"""Release 1.3 flow 'user is not registered': the invitee has no account, registers with the invited e-mail, and lands on the invitation.
The newly registered person becomes the standing journey member afterwards."""
from alumnye_qa import flows, testdata

META = dict(id="JNY-008", title="Invited person without an account registers and then sees the invitation", type="Edge", devices=2)


def anchor(app, sync):
    flows.to_anchor_home(app)
    person = testdata.new_person()
    sync.data["person"] = person
    sync.data["member_email"] = person["email"]
    sync.set("member_ready")                                # no existing account to wait for
    group = testdata.new_group()
    flows.create_group(app, group)
    sync.data["group"] = group["name"]
    flows.open_add_members(app)
    result = flows.send_invite(app, person["email"])
    app.soft_check(result == "sent", f"inviting an unregistered e-mail must succeed (result: {result})")
    sync.set("invite_sent")
    sync.wait("member_decided")


def member(app, sync):
    sync.wait("member_ready")
    person = sync.data["person"]
    app.account = person["email"]
    app.reset()
    sync.wait("invite_sent")
    flows.register_new_user(app, person["email"], person)
    testdata.save_journey_account("member", person)
    app.notes.append(f"registered the invited person {person['email']}; now the standing journey member")
    flows.member_open_invitation(app, sync)
    flows.member_decide(app, accept=True)
    sync.set("member_decided")

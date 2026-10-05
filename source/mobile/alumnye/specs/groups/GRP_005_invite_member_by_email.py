from alumnye_qa import flows, testdata

META = dict(id="GRP-005", title="Anchor invites a member by email and gets a success confirmation", type="Positive", fresh=False)


def run(app):
    email = testdata.new_person()["email"]
    flows.open_add_members(app)
    count_before = flows.pending_invites(app)
    result = flows.send_invite(app, email)
    app.soft_check(result == "sent", f"inviting {email} must succeed (result: {result})")
    app.soft_check(bool(app.screen_has(r"invitation.*sent|sent successfully|invited", timeout=3)), "a success confirmation must be shown after the invitation is sent")
    app.notes.append(f"invited {email}; pending invites before: {count_before}")

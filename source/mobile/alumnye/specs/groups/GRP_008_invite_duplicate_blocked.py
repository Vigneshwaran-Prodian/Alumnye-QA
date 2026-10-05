from alumnye_qa import flows, testdata

META = dict(id="GRP-008", title="Inviting the same email twice is blocked", type="Negative", fresh=False)


def run(app):
    email = testdata.new_person()["email"]
    flows.open_add_members(app)
    app.soft_check(flows.send_invite(app, email) == "sent", "the first invitation must succeed")
    second = flows.send_invite(app, email)
    app.soft_check(second in ("blocked", "error"), f"inviting the same email twice must be rejected (result: {second})")

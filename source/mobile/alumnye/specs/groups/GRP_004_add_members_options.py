from alumnye_qa import flows, testdata

META = dict(id="GRP-004", title="Add Members shows the four invitation tabs and the Invite form (email OR mobile, Send Invitation)", type="Positive", fresh=False)


def run(app):
    flows.open_add_members(app)
    for key, name in (("tab_invite", "Invite"), ("tab_upload", "Upload"), ("tab_add_members", "Add Members"), ("tab_add_contacts", "Add Contact")):
        app.soft_check(app.visible(key, 2), f"the '{name}' tab must be shown in the add-member screen")
    app.notes.append("tabs seen: Invite | Upload | Add Members | 'Add Contact' (singular; the release note says 'Add Contacts')")
    app.tap("tab_invite", "open the Invite tab")
    app.soft_check(bool(app.screen_has(r"^email address$", timeout=2)), "the Invite tab must have an 'Email Address' field")
    app.soft_check(bool(app.screen_has(r"^mobile number$", timeout=2)), "the Invite tab must have a 'Mobile Number' field")
    app.soft_check(bool(app.screen_has(r"^or$", timeout=2)), "the Invite tab must offer email OR mobile (an 'OR' divider)")
    app.soft_check(app.visible("send_invite_button", 2), "the Invite tab must have a 'Send Invitation' button")
    app.soft_check(app.visible("invite_mobile_field", 2), "the Invite tab must have a 10-digit mobile number input")
    app.probe_safe("Add Members screen")

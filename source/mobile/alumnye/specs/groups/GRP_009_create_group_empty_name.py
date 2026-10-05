from alumnye_qa import flows, testdata

META = dict(id="GRP-009", title="Create Group is blocked when the name is empty", type="Negative", fresh=False)


def run(app):
    flows.open_group_form(app)
    for value, label in (("", "an empty name"), ("   ", "a spaces-only name")):
        if value:
            app.type("group_name_field", value)
        result = flows.submit_or_guard(app, "save_group_button", f"tried to save a group with {label}")
        app.soft_check(not app.visible("group_details_marker", 2), f"a group must not be created with {label}")
        app.soft_check(app.visible("group_name_field", 2), f"the form must stay open after {label}")

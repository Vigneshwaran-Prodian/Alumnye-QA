from alumnye_qa import flows, testdata

META = dict(id="GRP-001", title="Anchor creates a group and lands on its Group Details", type="Positive", fresh=False)


def run(app):
    """Always creates a NEW group for the logged-in user (a user can own many groups); later scenarios reuse it."""
    group = testdata.new_group()
    flows.create_group(app, group)
    app.soft_check(app.visible("group_name_title", 3) or bool(app.screen_has(group["name"], timeout=2)), f"Group Details must show the group name '{group['name']}'")
    flows.back_to_anchor_home(app)
    app.soft_check(bool(app.screen_has(group["name"], timeout=3)), "the new group must appear on Anchor Home")
    app.soft_check(bool(app.screen_has(r"since", timeout=1)), "the group card should show 'Since <date>'")

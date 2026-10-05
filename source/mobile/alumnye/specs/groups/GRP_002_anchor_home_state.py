from alumnye_qa import flows

META = dict(id="GRP-002", title="Anchor Home offers + New Group and shows the right state (welcome message or the group list)", type="Positive", fresh=False)


def run(app):
    flows.to_anchor_home(app)
    app.expect("new_group_button", "+ New Group button is shown")
    if app.visible("empty_state_text", 2):
        app.notes.append("user has no groups: welcome empty state shown")
    else:
        app.soft_check(bool(app.screen_has(r"since", timeout=2)), "a user who has groups must see them listed (group cards show 'Since <date>')")
        app.notes.append("user already has groups: group list shown (the empty state applies only to a user with no groups)")

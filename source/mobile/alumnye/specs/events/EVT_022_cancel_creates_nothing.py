from alumnye_qa import flows

META = dict(id="EVT-022", title="Leaving the Event form without saving creates no event and keeps nothing in the next form", type="Negative", fresh=False)


def run(app):
    ev = flows.new_event("Cultural")
    flows.open_event_form(app)
    flows.fill_event(app, ev)                                                  # title, description and category entered, not saved
    if app.visible("event_cancel_button", 1):
        app.tap("event_cancel_button", "cancel the Event form")
    else:
        app.back()
    app.notes.append("left the form with " + ("Cancel" if app.visible("add_event_button", 2) else "Back"))
    app.wait_screen("add_event_button", "leaving the form returns to Group Details")
    app.soft_check(not flows.event_on_list(app, ev["title"], timeout=2), f"the cancelled event '{ev['title']}' must not be listed")
    flows.open_event_form(app)
    app.soft_check(not flows.filled_inputs(app), f"the next Create form must be empty, not show the cancelled entries (found: {flows.filled_inputs(app)})")
    flows.to_group_details(app)

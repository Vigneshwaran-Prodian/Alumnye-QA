from alumnye_qa import flows

META = dict(id="EVT-026", title="After saving an event the next Add Event form opens empty, with no category preselected", type="Positive", fresh=False)


def run(app):
    ev = flows.create_event(app, flows.new_event("Sports"))
    flows.open_event_form(app)
    app.soft_check(not flows.filled_inputs(app), f"the Create form must be empty after a save (found: {flows.filled_inputs(app)})")
    app.soft_check(not app.screen_has(r"^sports$", timeout=1), "the category chosen for the previous event must not stay selected")
    flows.to_group_details(app)

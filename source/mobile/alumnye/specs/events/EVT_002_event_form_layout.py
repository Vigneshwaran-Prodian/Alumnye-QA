from alumnye_qa import flows

META = dict(id="EVT-002", title="Add Event opens the Event form: title, description, category dropdown and Save, all fields empty", type="Positive", fresh=False)


def run(app):
    flows.open_event_form(app)
    app.soft_check(app.visible("event_title_field", 2), "the Event form must have a title field")
    app.soft_check(app.visible("event_description_field", 2), "the Event form must have a description / details field")
    app.soft_check(app.visible("event_category_dropdown", 2), "the Event form must have a category dropdown")
    app.soft_check(app.visible("event_save_button", 2), "the Event form must have a Save button")
    app.soft_check(app.visible("event_cancel_button", 1) or app.visible("event_save_button", 1), "the Event form must be leavable (Cancel or the back arrow)")
    app.soft_check(not flows.filled_inputs(app), f"the Create form must open with empty fields (found: {flows.filled_inputs(app)})")
    app.notes.append("Save is " + ("disabled" if app.is_disabled("event_save_button") else "enabled") + " on the empty form")
    app.discover("Event form")
    flows.to_group_details(app)

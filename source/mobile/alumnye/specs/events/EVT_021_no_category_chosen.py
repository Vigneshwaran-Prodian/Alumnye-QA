import re

from alumnye_qa import flows

META = dict(id="EVT-021", title="An event cannot be saved without a category (category is mandatory)", type="Negative", fresh=False)


def run(app):
    ev = flows.new_event("Reunion")
    flows.open_event_form(app)
    flows.fill_event(app, ev, category=False)                                  # title and description only
    result = flows.submit_or_guard(app, "event_save_button", "tried to save an event without choosing a category")
    shown = " / ".join(app.last_msgs) or "(no message)"
    app.soft_check(result == "blocked" or any(re.search(r"categor|select|choose|required", m, re.I) for m in app.last_msgs),
                   f"saving without a category must be refused: a disabled Save or a message about the category (result: {result}; message: {shown})")
    app.soft_check(app.visible("event_title_field", 2) and not app.visible("add_event_button", 1),
                   "the form must stay open: an event without a category must not be created")
    flows.to_group_details(app)
    app.soft_check(not flows.event_on_list(app, ev["title"], timeout=2), f"'{ev['title']}' must not be listed: it has no category")

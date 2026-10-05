import re

from alumnye_qa import flows

META = dict(id="EVT-019", title="An event cannot be saved without a title", type="Negative", fresh=False)


def run(app):
    flows.open_event_form(app)
    flows.choose_category(app, "Reunion")                                      # everything filled except the title
    result = flows.submit_or_guard(app, "event_save_button", "tried to save an event with an empty title")
    shown = " / ".join(app.last_msgs) or "(no message)"
    app.soft_check(result == "blocked" or any(re.search(r"title|name|required|enter|fill", m, re.I) for m in app.last_msgs),
                   f"saving without a title must be blocked: a disabled Save or a message about the title (result: {result}; message: {shown})")
    app.soft_check(app.visible("event_title_field", 2) and not app.visible("add_event_button", 1), "the form must stay open: no event may be created without a title")
    flows.to_group_details(app)

import re

from alumnye_qa import flows

META = dict(id="EVT-020", title="A title made only of spaces is not accepted", type="Negative", fresh=False)


def run(app):
    flows.open_event_form(app)
    app.type("event_title_field", "     ", "type a title made of 5 spaces")
    flows.choose_category(app, "Reunion")
    result = flows.submit_or_guard(app, "event_save_button", "tried to save an event whose title is only spaces")
    shown = " / ".join(app.last_msgs) or "(no message)"
    app.soft_check(result == "blocked" or any(re.search(r"title|name|required|enter|valid|fill", m, re.I) for m in app.last_msgs),
                   f"a spaces-only title must be refused (result: {result}; message: {shown})")
    app.soft_check(app.visible("event_title_field", 2) and not app.visible("add_event_button", 1), "the form must stay open: no event may be created from a blank title")
    flows.to_group_details(app)

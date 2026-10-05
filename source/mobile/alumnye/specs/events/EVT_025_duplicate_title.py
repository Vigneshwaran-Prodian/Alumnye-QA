import time

from alumnye_qa import flows

META = dict(id="EVT-025", title="The same event title can be added twice to a group and is listed twice", type="Edge", fresh=False)


def run(app):
    flows.new_group_ready(app)
    ev = flows.new_event("Social", title=f"QA Same Title {time.strftime('%m%d%H%M%S')}")
    flows.create_event(app, ev)
    flows.open_event_form(app)
    flows.fill_event(app, ev)
    flows.save_event(app, "saved a second event with the same title")
    shown = " / ".join(app.last_msgs) or "(no message)"
    if app.visible("event_title_field", 2):                                    # refused
        app.notes.append(f"duplicate title REFUSED; message: {shown}")
        app.soft_check(False, f"the owner expects the same event to be addable twice, but the app refused it (message: {shown}) - confirm the rule")
        flows.to_group_details(app)
        return
    flows.show_events_tab(app)
    count = sum(1 for l in app.labels() if ev["title"][:30].lower() in l.lower())
    app.notes.append(f"duplicate title accepted; labels showing it: {count}")
    app.soft_check(count >= 2, f"the second event with the same title must be listed as its own event (labels showing it: {count})")

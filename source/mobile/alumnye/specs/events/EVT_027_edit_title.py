import time

from alumnye_qa import flows

META = dict(id="EVT-027", title="Editing the title updates the Events tab and Event Home; the old title disappears", type="Positive", fresh=False)


def run(app):
    ev = flows.create_event(app, flows.new_event("Professional"))
    new_title = f"QA Renamed {time.strftime('%m%d%H%M%S')}"
    app.soft_check(flows.edit_event(app, ev["title"], new_title=new_title), "the event must be editable from Event Home")
    app.soft_check(flows.event_on_list(app, new_title), f"the new title '{new_title}' must be listed")
    app.soft_check(not flows.event_on_list(app, ev["title"], timeout=1), f"the old title '{ev['title']}' must be gone")
    app.soft_check(flows.open_event(app, new_title) and app.has_text(new_title, 3), "Event Home must show the new title")

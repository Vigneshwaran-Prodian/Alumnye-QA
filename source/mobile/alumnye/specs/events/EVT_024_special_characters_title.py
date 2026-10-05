import time

from alumnye_qa import flows

META = dict(id="EVT-024", title="A title with symbols, quotes and accents is saved and shown exactly as typed", type="Edge", fresh=False)


def run(app):
    stamp = time.strftime("%m%d%H%M%S")
    title = f"QA & Co's \"Meet\" 100% #{stamp} Caf\u00e9"
    ev = flows.new_event("Social", title=title)
    flows.create_event(app, ev)
    app.soft_check(flows.event_on_list(app, title), "the event with special characters must be listed")
    app.soft_check(flows.open_event(app, title), "the event must open")
    app.soft_check(app.has_text(title, 3), f"Event Home must show the title exactly as typed: {title}")

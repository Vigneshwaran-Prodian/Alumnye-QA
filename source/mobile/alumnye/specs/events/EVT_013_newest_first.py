import time

from alumnye_qa import flows, testdata

META = dict(id="EVT-013", title="Two events in one group are listed newest first", type="Positive", fresh=False)


def run(app):
    flows.new_group_ready(app)
    stamp = time.strftime("%m%d%H%M%S")
    older = flows.new_event("Social", title=f"QA Older {stamp}")
    newer = flows.new_event("Social", title=f"QA Newer {stamp}")
    flows.create_event(app, older)
    flows.create_event(app, newer)                                             # created later, same group
    flows.show_events_tab(app)
    y_old, y_new = flows.y_of(app, older["title"]), flows.y_of(app, newer["title"])
    app.soft_check(y_old is not None and y_new is not None, "both events must be listed on the Events tab")
    if y_old is not None and y_new is not None:
        app.soft_check(y_new < y_old, f"the most recently created event must be listed first (newer at y={y_new}, older at y={y_old})")

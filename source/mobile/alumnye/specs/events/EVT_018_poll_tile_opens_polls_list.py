import re

from alumnye_qa import flows

META = dict(id="EVT-018", title="The Poll tile opens the Event Polls List (list first), not the poll creation form", type="Positive", fresh=False)


def run(app):
    ev = flows.create_event(app, flows.new_event("Social"))
    flows.open_event(app, ev["title"])
    changed, err, heading = flows.open_tile(app, "Poll")
    app.notes.append(f"Poll tile opened '{heading}'")
    app.soft_check(changed, "the Poll tile must open a new screen")
    app.soft_check(not err, f"the Polls screen must not show an error ('{err}')")
    app.soft_check(bool(app.screen_has(r"poll", timeout=2)), "the opened screen must be about polls")
    app.soft_check(not app.inputs(), "list-first UX: the first screen must not be a creation form with input fields")
    app.soft_check(not app.screen_has(r"d4 poll wizard|choose a poll type|select poll type", timeout=1), "list-first UX: the poll-type chooser must not open before the list")
    app.soft_check(bool(app.screen_has(r"no polls|create|new poll|add poll|\+", timeout=2)), "the list must offer a way to create a poll or show its empty state")
    flows.back_to_event_home(app)

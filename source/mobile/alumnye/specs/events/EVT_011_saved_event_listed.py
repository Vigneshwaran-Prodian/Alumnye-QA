from alumnye_qa import flows

META = dict(id="EVT-011", title="Save returns to Group Details and the event is listed with its category and a status badge", type="Positive", fresh=False)


def run(app):
    ev = flows.create_event(app, flows.new_event("Networking"))
    app.soft_check(app.visible("group_details_marker", 3), "Save must return to Group Details")
    app.soft_check(flows.event_on_list(app, ev["title"]), f"the event '{ev['title']}' must be listed on the Events tab")
    app.soft_check(not app.visible("no_events_text", 1), "'No events yet' must be gone once an event exists")
    app.soft_check(bool(app.screen_has(r"^networking$", timeout=2)), "the listing must show the event's category 'Networking'")
    app.soft_check(bool(flows.status_badge(app)), "the event must show a status badge")

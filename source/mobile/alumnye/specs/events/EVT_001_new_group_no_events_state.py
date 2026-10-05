from alumnye_qa import flows, testdata

META = dict(id="EVT-001", title="A brand-new group shows 'No events yet' with Add Event available", type="Positive", fresh=False)


def run(app):
    flows.new_group_ready(app)                                                 # brand-new group WITH members (the chain Auth -> Group -> Members), but no events
    flows.show_events_tab(app)
    app.soft_check(app.visible("no_events_text", 3), "a group without events must show 'No events yet'")
    app.soft_check(bool(app.screen_has(r"tap add event above to plan one", timeout=2)), "the empty state must say 'Tap Add Event above to plan one.'")
    app.soft_check(app.visible("add_event_button", 2), "'Add Event' must be available")
    app.soft_check(not flows.status_badge(app), "no event card (status badge) may be listed in a group without events")

from alumnye_qa import flows

META = dict(id="EVT-012", title="Event Home shows the title and description that were entered and a status badge", type="Positive", fresh=False)


def run(app):
    ev = flows.new_event("Social", desc="Annual alumni get-together at the club house.")
    flows.create_event(app, ev)
    app.soft_check(flows.open_event(app, ev["title"]), "the event must open its Event Home")
    app.soft_check(app.has_text(ev["title"], 3), f"Event Home must show the title '{ev['title']}'")
    app.soft_check(app.has_text("get-together", 2), "Event Home must show the description that was entered")
    badge = flows.status_badge(app)
    app.soft_check(bool(badge), "Event Home must show the event's lifecycle status badge")
    app.notes.append(f"initial status badge: '{badge}'")

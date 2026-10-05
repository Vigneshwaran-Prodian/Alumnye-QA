from alumnye_qa import flows

META = dict(id="EVT-030", title="A created event is also visible from the main navigation (Home / My Group) with its status badge", type="Positive", fresh=False)


def run(app):
    ev = flows.create_event(app, flows.new_event("Social"))
    route = ""
    for label in ("Home", "My Group"):
        tab = app._try([f"btnx:{label}"], 2)
        if tab is None:
            continue
        tab.click()
        app.wait_banner_clear()
        if app.has_text(ev["title"][:30], 4):
            route = label
            break
    app.notes.append(f"event found via: {route or 'nowhere'}")
    app.soft_check(bool(route), f"the event '{ev['title']}' must be reachable from Home or My Group")
    if route:
        app.soft_check(bool(flows.status_badge(app)), "the event must show a status badge in that list")

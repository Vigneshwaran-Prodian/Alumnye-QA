from alumnye_qa import flows, testdata

META = dict(id="EVT-014", title="One event per category: the listing shows each event under its own category", type="Positive", fresh=False)


def run(app):
    flows.new_group_ready(app)
    made = [flows.create_event(app, flows.new_event(c)) for c in flows.CATEGORIES]      # 7 events, one per category
    flows.show_events_tab(app)
    seen = flows.read_listing(app, [e["title"] for e in made])
    for ev in made:
        got = seen.get(ev["title"], [])
        app.notes.append(f"{ev['category']}: '{ev['title']}' listed under {got or 'no category label found'}")
        app.soft_check(bool(got), f"'{ev['title']}' must be listed under a category (no category heading or label found near it)")
        app.soft_check(not got or ev["category"] in got, f"'{ev['title']}' must be listed under {ev['category']} (found under: {', '.join(got)})")
    app.soft_check(all(flows.event_on_list(app, e["title"], timeout=1) for e in made), "all 7 events must be listed")

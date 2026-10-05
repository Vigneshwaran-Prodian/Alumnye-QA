from alumnye_qa import flows

META = dict(id="EVT-029", title="After the app is restarted the event, its category tiles and its status are unchanged (no auto-advance)", type="Edge", fresh=False)


def run(app):
    ev = flows.create_event(app, flows.new_event("Sports"))
    flows.open_event(app, ev["title"])
    status_before, tiles_before = flows.status_badge(app), flows.read_tiles(app)
    app.restart()                                                              # kill and reopen the app
    flows.open_group(app)
    app.soft_check(flows.open_event(app, ev["title"]), "the event must still be listed after the restart")
    status_after, tiles_after = flows.status_badge(app), flows.read_tiles(app)
    app.notes.append(f"status before/after restart: '{status_before}' / '{status_after}'")
    app.soft_check(status_before == status_after, f"no phase advances by itself (RULE-007): '{status_before}' became '{status_after}'")
    app.soft_check(sorted(tiles_before) == sorted(tiles_after), f"the tile set must not change on restart ({tiles_before} -> {tiles_after})")
    flows.check_tiles(app, "Sports", tiles_after, label="after restart")

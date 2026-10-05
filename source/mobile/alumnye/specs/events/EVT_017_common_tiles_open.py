from alumnye_qa import flows

META = dict(id="EVT-017", title="Every tile of the shared set opens its own screen and Back returns to Event Home", type="Positive", fresh=False)

CATEGORY = "Social"


def run(app):
    ev = flows.create_event(app, flows.new_event(CATEGORY))
    app.soft_check(flows.open_event(app, ev["title"]), "the new event must open its Event Home")
    for tile in flows.tiles_for(CATEGORY):                                      # navigation only: nothing is created or changed
        changed, err, heading = flows.open_tile(app, tile)
        app.notes.append(f"{tile} tile opened '{heading or 'unknown screen'}'")
        app.soft_check(changed, f"the {tile} tile must open its own screen")
        app.soft_check(not err, f"the {tile} screen must not show an error ('{err}')")
        if not flows.back_to_event_home(app):
            app.soft_check(False, f"Back from the {tile} screen must return to Event Home")
            break

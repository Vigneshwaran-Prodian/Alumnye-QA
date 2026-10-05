from alumnye_qa import flows

META = dict(id="EVT-028", title="Changing the category Reunion -> Sports -> Reunion switches the tile set each time", type="Positive", fresh=False)


def run(app):
    ev = flows.create_event(app, flows.new_event("Reunion"))
    flows.open_event(app, ev["title"])
    flows.check_tiles(app, "Reunion", flows.read_tiles(app), label="before the change (Reunion)")
    flows.back_to_event_home(app)
    app.soft_check(flows.edit_event(app, ev["title"], category="Sports"), "the category must be editable")
    flows.open_event(app, ev["title"])
    flows.check_tiles(app, "Sports", flows.read_tiles(app), label="after changing to Sports")
    flows.back_to_event_home(app)
    app.soft_check(flows.edit_event(app, ev["title"], category="Reunion"), "the category must be editable back")
    flows.open_event(app, ev["title"])
    flows.check_tiles(app, "Reunion", flows.read_tiles(app), label="after changing back to Reunion")

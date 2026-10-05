from alumnye_qa import flows

META = dict(id="EVT-005", title="Sports event shows exactly Poll, Launch RSVP, Golf, Library and Payment", type="Positive", fresh=False)

CATEGORY = "Sports"


def run(app):
    ev = flows.create_event(app, flows.new_event(CATEGORY))                   # Add Event -> Sports -> Save
    app.soft_check(flows.open_event(app, ev["title"]), "the new event must open its Event Home")
    flows.check_tiles(app, CATEGORY, flows.read_tiles(app))
    app.soft_check(bool(flows.status_badge(app)), "Event Home must show the event's status badge")
    app.soft_check("Golf" in flows.read_tiles(app), "the Golf tile belongs to the Sports category")

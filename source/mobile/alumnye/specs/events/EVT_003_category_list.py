from alumnye_qa import flows

META = dict(id="EVT-003", title="The category dropdown offers exactly Reunion, Sports, Networking, Professional, Social, Cultural and Other", type="Positive", fresh=False)


def run(app):
    flows.open_event_form(app)
    options = flows.category_options(app)
    app.notes.append("category options shown, in order: " + " | ".join(options))
    shown = [o.lower() for o in options]
    want = [c.lower() for c in flows.CATEGORIES]
    app.soft_check(not [c for c in want if c not in shown], f"the dropdown must offer {', '.join(c for c in flows.CATEGORIES if c.lower() not in shown)} (offered: {', '.join(options) or 'nothing'})")
    app.soft_check(not [o for o in shown if o not in want], f"the dropdown must not offer extra categories (extra: {', '.join(o for o in options if o.lower() not in want)})")
    app.soft_check(len(shown) == len(set(shown)), "no category may be listed twice")
    app.soft_check(len(shown) == 7, f"the dropdown must offer exactly 7 categories (offered {len(shown)})")
    flows.to_group_details(app)

import time

from alumnye_qa import flows, testdata

META = dict(id="EVT-023", title="Title length limits: 1, 100, 255 and 256 characters are handled consistently", type="Edge", fresh=False)

LENGTHS = [1, 100, 255, 256]


def run(app):
    flows.new_group_ready(app)                                                 # fresh group with members: no earlier title can clash
    outcomes = {}
    for n in LENGTHS:
        title = chr(64 + LENGTHS.index(n) + 1) + "x" * (n - 1)               # A, Bxxx..., Cxxx..., Dxxx... : exactly n characters, unique per length
        flows.open_event_form(app)
        flows.fill_event(app, {"title": title, "category": "Social", "desc": ""})
        flows.save_event(app, f"saved an event with a {n}-character title")
        saved = app.visible("group_details_marker", 3) or app.visible("add_event_button", 1)
        shown = " / ".join(app.last_msgs) or "(no message)"
        outcomes[n] = saved
        app.notes.append(f"{n} characters: {'accepted' if saved else 'refused'}; message: {shown}")
        if saved:
            app.soft_check(flows.event_on_list(app, title[:20]), f"the {n}-character event must be listed (first 20 characters shown)")
        else:
            flows.to_group_details(app)
    app.soft_check(outcomes[1], "a 1-character title is valid and must be accepted")
    app.soft_check(outcomes[100], "a 100-character title must be accepted")
    app.soft_check(outcomes[255] and outcomes[256], "the owner expects NO title limit: 255 and 256 characters should be accepted - a refusal means a limit exists (to be confirmed with the owner)")
    accepted = [n for n in LENGTHS if outcomes[n]]
    refused = [n for n in LENGTHS if not outcomes[n]]
    app.soft_check(not accepted or not refused or max(accepted) < min(refused), f"the limit must be one clear boundary: accepted {accepted}, refused {refused}")
    app.soft_check(app.visible("add_event_button", 3), "the app must still be responsive after the longest title")

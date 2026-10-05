import re

from alumnye_qa import flows, testdata

META = dict(id="GRP-010", title="A duplicate group name is rejected with the full message", type="Negative", fresh=False)

FULL = r"a group with this name already exists\.?\s*please choose a different name"


def run(app):
    group = testdata.new_group()
    flows.create_group(app, group)
    flows.back_to_anchor_home(app)
    flows.open_group_form(app)
    app.type("group_name_field", group["name"], "re-use the same group name")
    flows.submit_or_guard(app, "save_group_button", "tried to create a second group with an existing name")
    shown = " / ".join(app.last_msgs) or "(no message)"
    app.soft_check(not app.visible("group_details_marker", 2), "a duplicate group name must be rejected")
    app.soft_check(any(re.search(FULL, m, re.I) for m in app.last_msgs),
                   f"the message must read 'A group with this name already exists. Please choose a different name.' in full (shown: {shown})")

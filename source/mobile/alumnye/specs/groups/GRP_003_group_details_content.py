import re

from alumnye_qa import flows, testdata

META = dict(id="GRP-003", title="Group Details shows the group, Add Member / Add Event, the Members count tab, Events tab and Notice Board", type="Positive", fresh=False)


def run(app):
    flows.open_group(app)
    group = testdata.load_groups()[-1]
    app.soft_check(bool(app.screen_has(re.escape(group["name"]), timeout=3)), f"Group Details must show the group name '{group['name']}'")
    app.soft_check(app.visible("edit_group_button", 2), "Group Details must offer 'Edit'")
    app.soft_check(bool(app.screen_has(re.escape(group.get("desc", "Automated test group")[:25]), timeout=2)), "the group description must be shown under the name")
    app.soft_check(app.visible("add_member_entry", 3), "Group Details must have 'Add Member'")
    app.soft_check(app.visible("add_event_button", 3), "Group Details must have 'Add Event' (renamed from 'New Event')")
    app.soft_check(not app.visible("old_new_event_button", 1), "the old 'New Event' label must be gone")
    app.soft_check(app.visible("events_tab", 2), "Group Details must have an 'Events' tab")
    tab = app.screen_has(r"^members,?\s*\d+", timeout=3)           # the number on the Members tab IS the member count
    count = int(re.search(r"\d+", tab).group()) if tab else None
    app.soft_check(tab != "", "Group Details must have a 'Members' tab showing the member count")
    app.soft_check(count is not None and count >= 1, f"a new group has at least its creator as a member (Members tab shows: {tab or 'nothing'})")
    app.soft_check(bool(app.screen_has(r"notice board", timeout=2)), "Group Details must show the Notice Board card")
    app.soft_check(bool(app.screen_has(r"no events yet", timeout=2)), "a group without events must show 'No events yet' (with 'Tap Add Event above to plan one.')")
    app.notes.append(f"Members tab: '{tab}' (count {count}); the docs' 'About' section does not exist in v1.4.0")

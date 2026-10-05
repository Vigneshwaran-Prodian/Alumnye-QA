import re

from alumnye_qa import flows, healer

META = dict(id="GRP-015", title="Pending Acceptance members each have a Remind button; accepted members do not", type="Positive", fresh=False)


def run(app):
    flows.open_members_list(app)                                      # same screen as GRP-014: the group's Members tab
    data = flows.read_members(app)
    pending, accepted = data["pending"], data["accepted"]
    app.notes.append(f"pending rows read: {len(pending)}; accepted members: {', '.join(n for n, _ in accepted)}")
    app.soft_check(data["pending_header"] and len(pending) >= 1, "the 'PENDING ACCEPTANCE' section must list the invitees who have not accepted (run GRP-005 / GRP-012 first)")
    app.soft_check(all(p["remind"] for p in pending), "every member under PENDING ACCEPTANCE must have a 'Remind' button")
    # accepted members (e.g. the Anchor) must not offer Remind: no Remind sits on an accepted card's row
    nodes = healer.snapshot(app.d.page_source, app.platform)
    reminds = [n for n in nodes if n.clickable and n.label.strip().lower() == "remind"]
    accepted_cards = [n for n in nodes if n.clickable and any(re.match(rf"^{re.escape(name)}, ", n.label.strip()) for name, _ in accepted)]
    for card in accepted_cards:
        app.soft_check(not any(abs(r.cy - card.cy) < 110 for r in reminds), f"an accepted member ('{card.label}') must not have a Remind button")
    if reminds:
        before = app.mark()
        app.wait_banner_clear()
        app.tap_xy(reminds[0].cx, reminds[0].cy)
        texts = app.watch_messages("tapped Remind for a member under Pending Acceptance", before, seconds=4)
        app.soft_check(bool(texts), "tapping Remind must give visible feedback (message / status change)")
        app.notes.append("Remind feedback: " + (" / ".join(texts) or "none"))
    app.discover("Members list (pending invitees)")

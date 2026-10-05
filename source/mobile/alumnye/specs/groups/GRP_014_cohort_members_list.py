from alumnye_qa import flows, testdata

META = dict(id="GRP-014", title="Members tab: the count equals the accepted-members name list; invitees sit under Pending Acceptance, not in the count", type="Positive", fresh=False)


def run(app):
    flows.open_members_list(app)                                      # open an existing group, tap its 'Members, N' tab
    data = flows.read_members(app)
    count, accepted, pending = data["count"], data["accepted"], data["pending"]
    names = [n for n, _ in accepted]
    app.notes.append(f"Members tab count {count}; accepted list ({len(accepted)}): {', '.join(f'{n} ({r})' for n, r in accepted) or 'none'}; pending rows read: {len(pending)}")
    app.soft_check(count is not None, "the group page must show a 'Members, N' tab with the member count")
    app.soft_check(count == len(accepted), f"the member count ({count}) must equal the number of names in the accepted-members list ({len(accepted)}: {', '.join(names)})")
    app.soft_check(any(r.lower() == "anchor" for _, r in accepted), "the group's creator must be listed with the role 'Anchor'")
    app.soft_check(len(set(names)) == len(names), "no member may be listed twice")
    group = testdata.load_groups()[-1]["name"]
    invited = testdata.load_invites().get(group, [])
    shown = " ".join(p["text"] for p in pending).lower()
    if invited:
        first = [e for e in invited if e.lower() in shown]
        app.soft_check(bool(first), f"invitees sent for '{group}' must appear under PENDING ACCEPTANCE (none of {len(invited)} recorded invites found)")
        app.soft_check(not any(e.split("@")[0].lower() in " ".join(n.lower() for n in names) for e in invited),
                       "a member who only has a pending invitation must not be in the accepted names list / count")
    app.soft_check(bool(pending) == data["pending_header"], "the 'PENDING ACCEPTANCE' section must exist exactly when there are pending invitees")
    app.discover("Members list")                                      # only listed in the report: this screen is never wandered around

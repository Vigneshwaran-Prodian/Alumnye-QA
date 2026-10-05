from alumnye_qa import flows, testdata

META = dict(id="GRP-011", title="Group description is limited to 200 characters with a live counter", type="Edge", fresh=False)


def run(app):
    flows.open_group_form(app)
    app.type("group_description_field", "x" * 230, "type 230 characters")
    typed = app.find("group_description_field").text or ""
    app.soft_check(len(typed) == 200, f"Description must accept at most 200 characters (it holds {len(typed)})")
    app.soft_check(bool(app.screen_has(r"200\s*/\s*200|200/200", timeout=2)), "the live counter must show 200 / 200")

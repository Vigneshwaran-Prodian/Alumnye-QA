import re

from alumnye_qa import flows, testdata

META = dict(id="GRP-013", title="Bulk upload flags invalid files and rows (new data each run): bad e-mail, missing data, duplicates, wrong columns, empty, wrong format", type="Negative", fresh=False)


def run(app):
    flows.open_add_members(app)
    flows.open_upload_tab(app)
    for path, expect, why, token in testdata.upload_files("GRP-013"):    # NEW files every run: data/upload-files/GRP-013/<stamp>/
        name = path.replace("\\", "/").rsplit("/", 1)[-1]
        unsupported = name.endswith(".txt")
        res = flows.upload_file(app, path, required=not unsupported)
        if res is None:
            if unsupported:
                app.notes.append(f"{name} ({why}): the picker does not accept it - rejected at the picker (correct)")
            continue
        errors = list(res["errors"])                                      # validations in the preview popup ...
        confirmed, shown = flows.confirm_import(app, name)                # ... click 'Confirm Import' ...
        errors += [t for t in shown if re.search(flows.ERR_TEXT, t, re.I) and t not in errors]   # ... or in the banner at the top of the app
        text = " / ".join(errors) or "(nothing flagged)"
        app.notes.append(f"{name} ({why}): preview={res['preview']} confirmed={confirmed} flagged: {text}")
        app.soft_check(bool(errors), f"{name} ({why}) must be flagged with a validation message in the preview or at the top of the app (shown: {text})")
        if token and errors:
            app.soft_check(any(token.lower() in e.lower() for e in errors) or app.has_text(token, 1),
                           f"{name}: the message must point at the problem ('{token}'); shown: {text}")
        flows.reset_after_upload(app)

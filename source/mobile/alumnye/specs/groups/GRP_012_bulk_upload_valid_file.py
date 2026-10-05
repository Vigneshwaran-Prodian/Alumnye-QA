from alumnye_qa import flows, testdata

META = dict(id="GRP-012", title="Bulk upload: valid .xlsx and .csv files (new data each run, picked from local storage) reach the preview, are confirmed and imported", type="Positive", fresh=False)


def run(app):
    flows.create_group(app, testdata.new_group())                      # fresh data: a NEW group, so no member from an earlier run is in it
    flows.open_add_members(app)
    flows.open_upload_tab(app)
    app.soft_check(app.visible("download_template", 3), "the Upload tab must offer 'Member Template Download' (.xlsx format file)")
    app.soft_check(app.visible("choose_file_button", 3), "the Upload tab must have the dashed Upload area (.xlsx, .csv)")
    flows.download_template(app)                                     # the app hands the file to Chrome: the runner waits for it and comes back
    if not app.visible("choose_file_button", 3):
        flows.open_upload_tab(app)
    groups = testdata.load_groups()
    for path, expect, why, token in testdata.upload_files("GRP-012"):    # NEW files every run: data/upload-files/GRP-012/<stamp>/
        name = path.replace("\\", "/").rsplit("/", 1)[-1]
        res = flows.upload_file(app, path)                               # picked from the device's local Downloads, not Google Drive
        if res is None:
            continue
        app.notes.append(f"{name} ({why}): preview={res['preview']} errors={res['errors'] or 'none'}")
        app.soft_check(res["preview"], f"{name}: the 'List of Members' preview with 'Confirm Import' must be shown")
        app.soft_check(not res["errors"], f"{name} is valid and must show no validation errors (shown: {' / '.join(res['errors'])})")
        app.soft_check(app.has_text(token, 3), f"{name}: the preview must list the rows of THIS file (expected to see {token})")
        confirmed, shown = flows.confirm_import(app, name)               # click 'Confirm Import'
        app.soft_check(confirmed, f"{name}: the preview must have a 'Confirm Import' button")
        if confirmed:
            app.soft_check(any(__import__("re").search(r"success|imported|added|invited|sent", t, __import__("re").I) for t in shown),
                           f"{name}: the app must confirm the import (shown: {' / '.join(shown) or 'nothing'})")
            if groups:
                for mail in testdata.emails_in(path):
                    testdata.save_invite(groups[-1]["name"], mail)
        flows.reset_after_upload(app)

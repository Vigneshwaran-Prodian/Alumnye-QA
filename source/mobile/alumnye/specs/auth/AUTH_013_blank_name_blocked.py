from alumnye_qa import flows, testdata

META = dict(id="AUTH-013", title="Complete Profile blocks empty / spaces-only names", type="Negative", fresh=True)


def _try_continue(app, trigger):
    """Continue stays disabled while the form is invalid (the guard); if it is enabled, tapping must still not get past the screen."""
    before = app.mark()
    if app.is_disabled("save_finish_button"):
        app.messages.append({"trigger": trigger, "text": "(Continue button stays disabled)", "where": "state"})
    else:
        app.tap("save_finish_button", trigger, unblock=False)
        app.watch_messages(trigger, before)
    app.check(not app.at_home(2), f"{trigger}: onboarding must not complete")
    app.check(app.visible("complete_profile_marker", 2), f"{trigger}: user must stay on Complete Profile")


def run(app):
    person = testdata.new_person()
    flows.to_otp_screen(app, person["email"])
    flows.verify_otp(app, person["email"])
    app.wait_screen("complete_profile_marker", "Complete Profile screen")
    _try_continue(app, "empty first/last name")
    app.type("first_name_field", "   ")
    app.type("last_name_field", "   ")
    _try_continue(app, "spaces-only first/last name")

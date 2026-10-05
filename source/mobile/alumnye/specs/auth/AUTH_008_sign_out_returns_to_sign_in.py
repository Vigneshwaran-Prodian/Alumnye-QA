META = dict(id="AUTH-008", title="Sign out returns to Sign In and ends the session", type="Positive", fresh=False)


def run(app):
    app.ensure_logged_in()
    # Sign out lives under the My Account tab (owner). The runner finds it by exploring: My Account -> scroll -> other tabs -> heal/Qwen
    el = app.explore_for("sign_out", "find the Sign out / Log out option", via=["nav_profile"])
    app.dismiss_keyboard()
    el.click()
    if app.screen_has(r"are you sure|do you want|confirm|sign out\?|log out\?", timeout=1.5):      # only if a dialog is shown
        app.tap("confirm_sign_out", "confirm sign out")
    app.wait_screen("landing_sign_in", "landing screen after sign-out")
    app.restart()
    app.wait_screen("landing_sign_in", "session is really gone after restart (landing screen again)")
    app.expect_absent("home_marker", "no Home after sign-out + restart")

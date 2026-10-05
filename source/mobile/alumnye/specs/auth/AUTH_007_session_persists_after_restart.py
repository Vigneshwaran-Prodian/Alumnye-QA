META = dict(id="AUTH-007", title="Logged-in session survives an app restart (Splash -> Home)", type="Positive", fresh=False)


def run(app):
    app.ensure_logged_in()
    app.restart()
    app.wait_screen("home_marker", "Splash routes straight to Home with a valid session")
    app.expect_absent("landing_sign_in", "landing / Sign in must not be shown again")

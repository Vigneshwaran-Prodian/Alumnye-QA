META = dict(id="AUTH-001", title="Fresh launch routes from Splash to the landing screen (Sign in / Google / Create account)", type="Positive", fresh=True)


def run(app):
    # Splash (and any intro slides) auto-route to the landing screen when there is no stored session
    app.reach_landing()
    app.expect("landing_sign_in", "Sign in option is present", strict=True)
    app.expect("google_button", "Sign in with Google option is present", strict=True)
    app.expect("landing_create_account", "Create account option is present", strict=True)
    app.expect_absent("home_marker", "no Home without a session")

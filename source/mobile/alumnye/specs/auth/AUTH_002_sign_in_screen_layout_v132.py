META = dict(id="AUTH-002", title="Landing layout: Sign in above Google, divider reads 'or' (v1.3.2)", type="Positive", fresh=True)


def run(app):
    app.reach_landing()
    # strict=True: a missing/renamed label here IS the defect, so no self-heal / AI
    app.expect("landing_sign_in", "Sign in button present", strict=True)
    app.expect("google_button", "Google option present", strict=True)
    app.expect("or_divider", "divider label reads 'or' (any letter case)", strict=True)
    app.expect_absent("old_divider_text", "old 'or use email' label removed")

    def y(key):
        return app.find(key, strict=True).location["y"]

    app.check(y("landing_sign_in") < y("google_button"), "Sign in button must be ABOVE 'Sign in with Google'")
    app.check(y("google_button") < y("or_divider"), "divider sits below the Sign in / Google options")
    if app.platform == "ios":
        app.expect("apple_button", "Sign in with Apple present (iOS only)", strict=True)
        app.check(y("landing_sign_in") < y("apple_button"), "Sign in button must be ABOVE 'Sign in with Apple'")
    else:
        app.expect_absent("apple_button", "no Apple option on Android (owner confirmed)")

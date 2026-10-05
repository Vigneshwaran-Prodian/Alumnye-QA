META = dict(id="AUTH-017", title="Welcome / Create account screens have no Google/Apple options (v1.3.2)", type="Positive", fresh=True)


def _no_social(app):
    app.check(not app.visible("google_button", 1), f"'Continue with Google' must not appear here (path so far: {app.path})")
    app.check(not app.visible("apple_button", 1), f"'Continue with Apple' must not appear here (path so far: {app.path})")


def run(app):
    # intro slides / welcome screens before the landing screen: no social sign-up options
    app.reach_landing(on_screen=lambda a: None if a.visible("landing_sign_in", 1) else _no_social(a))
    # the Create account screen itself must not offer them either
    app.tap("landing_create_account", "open Create account")
    app.path.append("Create account")
    app.wait_screen("identifier_field", "Create account screen is shown")
    _no_social(app)

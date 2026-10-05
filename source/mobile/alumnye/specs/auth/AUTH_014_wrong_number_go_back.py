from alumnye_qa import flows, testdata

META = dict(id="AUTH-014", title="'Wrong email? Go back' returns to the identifier step without creating an account", type="Edge", fresh=True)


def run(app):
    person = testdata.new_person()
    flows.to_otp_screen(app, person["email"])
    app.tap("wrong_number_link", "tap 'Wrong email? Go back'")
    app.wait_screen("identifier_field", "back on the identifier step")
    app.expect_absent("otp_screen_marker", "OTP screen is closed")
    app.expect_absent("home_marker", "no session was created")

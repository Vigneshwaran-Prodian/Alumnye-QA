from alumnye_qa import flows, testdata

META = dict(id="AUTH-011", title="Incorrect OTP shows an error and does not sign in", type="Negative", fresh=True)


def run(app):
    person = testdata.new_person()
    flows.to_otp_screen(app, person["email"])
    flows.enter_otp_for(app, person["email"], code=testdata.wrong_otp())    # no tester input needed
    flows.accept_terms(app)
    before = app.mark()
    app.tap("verify_button", "verify the wrong OTP")
    app.watch_messages(f"entered wrong OTP {testdata.wrong_otp()} and tapped Verify", before)
    msg = app.screen_has(r"invalid|incorrect|wrong|expired|try again", timeout=6)
    app.check(msg, "an inline/toast error for an incorrect OTP must be shown")
    app.expect_absent("home_marker", "wrong OTP must not sign the user in")
    app.expect_absent("complete_profile_marker", "wrong OTP must not reach Complete Profile")

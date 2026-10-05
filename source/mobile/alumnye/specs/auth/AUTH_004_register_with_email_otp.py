from alumnye_qa import flows, testdata

META = dict(id="AUTH-004", title="New user registers with yopmail email + OTP", type="Positive", fresh=True)


def run(app):
    person = testdata.new_person()
    print(f"    test user: {person['first']} {person['last']} <{person['email']}>")
    flows.to_otp_screen(app, person["email"])                       # landing -> Create account -> Email tab -> Continue
    flows.enter_otp_for(app, person["email"])                       # tester types the OTP
    result = flows.accept_terms(app)                                # tick the Terms checkbox and confirm it is ticked
    app.soft_check(result in ("ticked", "already-ticked"), f"Terms & Conditions could not be accepted (result: {result})")
    app.soft_check(not app.is_disabled("verify_button"), "'Verify & join Alumnye' must be enabled once the OTP is entered and Terms are accepted")
    app.tap("verify_button", "verify the OTP and join")
    flows.complete_profile(app, person)                             # step 3 of 3: every field filled automatically
    app.wait_screen("home_marker", "Home screen after registration")
    testdata.save_user({**person, "via": "email"})

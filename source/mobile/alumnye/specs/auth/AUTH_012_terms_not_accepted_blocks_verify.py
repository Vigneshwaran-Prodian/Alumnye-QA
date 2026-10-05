from alumnye_qa import flows, testdata

META = dict(id="AUTH-012", title="Verify is blocked until Terms & Conditions are accepted", type="Negative", fresh=True)


def run(app):
    person = testdata.new_person()
    flows.to_otp_screen(app, person["email"])
    flows.enter_otp_for(app, person["email"])                     # real OTP entered, checkbox NOT ticked
    before = app.mark()
    if app.is_disabled("verify_button"):
        # 'Verify & join Alumnye' stays disabled without the checkbox: the guard works - logged as observed behaviour
        app.messages.append({"trigger": "entered a valid OTP but did not tick the Terms checkbox", "text": "(Verify & join Alumnye stays disabled)", "where": "state"})
    else:
        app.tap("verify_button", "verify without accepting Terms")
        app.watch_messages("tapped Verify without accepting Terms & Conditions", before)
        app.check(not app.visible("complete_profile_marker", 4) and not app.at_home(1),
                  "user must not proceed without accepting Terms & Conditions")
    app.expect("otp_screen_marker", "user is still on the Verify identity screen")

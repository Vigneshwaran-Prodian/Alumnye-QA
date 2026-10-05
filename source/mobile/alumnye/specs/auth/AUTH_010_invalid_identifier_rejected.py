META = dict(id="AUTH-010", title="Invalid email / mobile format is rejected on Sign In", type="Negative", fresh=True)

BAD = ["abc@", "12345", "no spaces@yopmail.com"]


def run(app):
    app.reach_sign_in()
    for bad in BAD:
        app.type("identifier_field", bad, f"enter invalid identifier '{bad}'")
        before = app.mark()
        if app.is_disabled("primary_button"):
            # Continue stays disabled for an invalid entry: that is the guard working - logged as an observed behaviour
            app.messages.append({"trigger": f"entered invalid identifier '{bad}'", "text": "(Continue button stays disabled)", "where": "state"})
        else:
            app.tap("primary_button", "submit")
            app.watch_messages(f"entered invalid identifier '{bad}' and tapped Continue", before)
        app.check(not app.visible("otp_screen_marker", 3), f"'{bad}' must not advance to the OTP screen")
        app.check(app.visible("identifier_field", 2), f"user stays on Sign In after '{bad}'")

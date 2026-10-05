import time

from alumnye_qa import flows, testdata

META = dict(id="AUTH-015", title="Resend is disabled during the countdown and works after it ends", type="Edge", fresh=True)


def run(app):
    person = testdata.new_person()
    flows.to_otp_screen(app, person["email"])
    # during the countdown the control reads 'Resend code (m:ss)' and is disabled (observed on device)
    timer = app.screen_has(r"resend code \(\d+:\d+\)", timeout=3)
    app.check(timer, "a 'Resend code (m:ss)' countdown must be shown on the Verify identity screen")
    app.check(app.is_disabled("resend_link"), f"Resend must be disabled while the countdown runs ({timer})")
    app.messages.append({"trigger": "arrived on the Verify identity screen", "text": timer, "where": "state"})
    end = time.time() + 150          # owner estimated ~2 min; the screen showed ~1 min - wait up to 150s
    while time.time() < end and not app.visible("resend_link", 2):
        pass
    app.check(app.visible("resend_link", 1), "Resend must become tappable after the countdown ends (waited 150s)")
    before = app.mark()
    app.tap("resend_link", "resend the OTP")
    app.watch_messages("tapped Resend code after the countdown ended", before)
    app.expect("otp_screen_marker", "still on the Verify identity screen after resend")

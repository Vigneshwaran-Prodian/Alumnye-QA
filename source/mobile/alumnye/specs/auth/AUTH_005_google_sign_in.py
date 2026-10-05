import time

from alumnye_qa import testdata
from alumnye_qa.app import StepFailed
from alumnye_qa.flows import complete_profile

META = dict(id="AUTH-005", title="Sign in with Google using the account already on the device", type="Positive", fresh=True, platforms=["android"])

GOOGLE_ERROR = r"access blocked|authorization error|invalid_request|error 400|something went wrong|couldn.t sign you in"


def run(app):
    app.reach_landing()
    before = app.mark()
    app.tap("google_button", "start Google sign-in")
    app.path.append("Sign in with Google")
    time.sleep(2)
    # account chooser (Google Play services): pick the first signed-in account if it is shown
    chooser = app.d.find_elements("id", "com.google.android.gms:id/container")
    if chooser:
        chooser[0].click()
    app.watch_messages("tapped Sign in with Google and chose the device account", before, seconds=6)
    err = app.screen_has(GOOGLE_ERROR, timeout=3)
    if err:
        detail = "; ".join(m["text"] for m in app.messages[:6])
        try:
            app.back()                      # close the Google custom tab so later scenarios start clean
        except Exception:
            pass
        raise StepFailed(f"Google sign-in is blocked by Google: '{err}'. Page text: {detail}. "
                         "The OAuth client is misconfigured (wrong client type / redirect URI) - product/config defect, not a script issue.",
                         "product-defect")
    # first-time Google users go through Complete Profile; returning users go straight Home
    end = time.time() + app.cfg["timeouts"]["screen"]
    while time.time() < end:
        if app.visible("complete_profile_marker", 1):
            complete_profile(app, testdata.new_person())
            break
        if app.at_home(1):
            break
    app.wait_screen("home_marker", "Home after Google sign-in")

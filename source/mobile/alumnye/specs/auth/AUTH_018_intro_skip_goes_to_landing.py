from alumnye_qa.session import Blocked

META = dict(id="AUTH-018", title="Intro slides offer Skip and Skip goes straight to the landing screen", type="Positive", fresh=True)


def run(app):
    st = app.intro_state(wait=25)
    if st["kind"] == "landing":
        raise Blocked("the app opened directly on the landing screen: no intro slides are shown on this launch")
    app.notes.append(f"first screen: {st['kind']}; controls: {', '.join(st['controls']) or 'none'}; wording: {' | '.join(st['texts'][:4])}")
    app.soft_check(st["kind"] == "slide", "after the Splash the app must show the intro slides")
    app.soft_check(st["skip"], f"the intro slide must offer 'Skip' (controls found: {', '.join(st['controls']) or 'none'})")
    if not st["skip"]:
        return
    app.tap("splash_skip", "skip the intro slides")
    app.wait_screen("landing_sign_in", "Skip leads to the landing screen")
    app.soft_check(app.visible("landing_create_account", 2), "the landing screen must offer 'Create account'")
    app.soft_check(not app.visible("splash_skip", 1), "no intro slide control may remain after Skip")

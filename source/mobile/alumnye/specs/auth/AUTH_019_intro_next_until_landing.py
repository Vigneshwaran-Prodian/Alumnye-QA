from alumnye_qa.session import Blocked

META = dict(id="AUTH-019", title="Intro slides: Get Started / Next, Next ... lead to the landing screen", type="Positive", fresh=True)

MAX_SLIDES = 10


def run(app):
    st = app.intro_state(wait=25)
    if st["kind"] == "landing":
        raise Blocked("the app opened directly on the landing screen: no intro slides are shown on this launch")
    sequence, seen = [], []
    for n in range(1, MAX_SLIDES + 1):
        if st["kind"] == "landing":
            break
        press = "Get Started" if st["start"] else "Next" if st["next"] else None      # decided from what the live screen offers
        if press is None:
            app.soft_check(False, f"slide {n} has neither 'Next' nor 'Get Started' (controls: {', '.join(st['controls']) or 'none'}), so the runner cannot move on")
            break
        sequence.append(press)
        seen.append(" | ".join(st["texts"][:3]))
        app.tap("splash_get_started" if press == "Get Started" else "splash_next", f"press {press} on slide {n}")
        st = app.intro_state(wait=8, settle=0.4)
    app.notes.append(f"pressed: {' -> '.join(sequence) or 'nothing'}; slides seen: {len(seen)}")
    app.soft_check(len(sequence) >= 1, "the intro must have at least one 'Next' / 'Get Started' step")
    app.soft_check(st["kind"] == "landing", f"pressing {' / '.join(sequence)} must end on the landing screen (ended on: {st['kind']})")
    if st["kind"] == "landing":
        app.expect("landing_sign_in", "landing screen reached", strict=True)
        app.expect("landing_create_account", "landing screen reached", strict=True)
    app.soft_check(len(set(seen)) == len(seen), "every slide must show different content (a repeated slide means a button did nothing)")

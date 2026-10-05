from alumnye_qa import config, testdata

META = dict(id="AUTH-020", title="Splash / intro UI and wording: every slide has its text and controls; landing follows the v1.3.2 wording and order", type="Positive", fresh=True)

MAX_SLIDES = 10


def run(app):
    st = app.intro_state(wait=25)
    slides = []
    ev = config.RESULTS_DIR / app.run_id
    for n in range(1, MAX_SLIDES + 1):
        if st["kind"] != "slide":
            break
        slides.append({"slide": n, "controls": st["controls"], "texts": st["texts"]})
        app.capture(str(ev / f"AUTH-020_slide{n}"))                       # a screenshot per slide, for the visual review
        app.soft_check(bool(st["texts"]), f"slide {n} must show wording (it is blank)")
        app.soft_check(bool(st["controls"]), f"slide {n} must offer a control (Skip / Next / Get Started)")
        press = "Get Started" if st["start"] else "Next" if st["next"] else None
        if press is None:
            break
        app.tap("splash_get_started" if press == "Get Started" else "splash_next", f"press {press} on slide {n}")
        st = app.intro_state(wait=8, settle=0.4)
    app.notes.append(f"{len(slides)} slide(s) read; screenshots AUTH-020_slide<n>.png are in the run evidence")

    # wording: compared with the approved wording; the first run records it and asks for approval (never silently trusted)
    data = testdata.load_wordings()
    if not data.get("slides"):
        testdata.save_wordings({"approved": False, "slides": slides})
        app.notes.append("slide wording recorded for the first time in data/splash-wordings.json - review it, then set approved to true to lock it")
    elif data.get("approved"):
        old = {s["slide"]: s for s in data["slides"]}
        app.soft_check(len(slides) == len(old), f"the intro must have {len(old)} slide(s) (found {len(slides)})")
        for s in slides:
            o = old.get(s["slide"])
            if o:
                app.soft_check(s["texts"] == o["texts"], f"slide {s['slide']} wording changed: expected {' | '.join(o['texts'])}; found {' | '.join(s['texts'])}")
                app.soft_check(s["controls"] == o["controls"], f"slide {s['slide']} controls changed: expected {o['controls']}; found {s['controls']}")
    else:
        old = {s["slide"]: s for s in data["slides"]}
        same = len(old) == len(slides) and all(old.get(s["slide"], {}).get("texts") == s["texts"] for s in slides)
        app.notes.append("slide wording " + ("matches the recorded (not yet approved) wording" if same else "DIFFERS from the recorded wording, which is not approved yet") + " - approve it in data/splash-wordings.json")

    # landing (v1.3.2): Sign in above Google, divider reads 'or', old label gone
    if st["kind"] != "landing":
        app.reach_landing()
    app.expect("landing_sign_in", "Sign in present", strict=True)
    app.expect("google_button", "Sign in with Google present", strict=True)
    app.expect("landing_create_account", "Create account present", strict=True)
    app.soft_check(app.visible("or_divider", 2), "the divider must read 'or' (v1.3.2)")
    app.soft_check(not app.visible("old_divider_text", 1), "the old divider 'or use email' must be gone (v1.3.2)")
    y = lambda key: app.find(key, strict=True).location["y"]
    app.soft_check(y("landing_sign_in") < y("google_button"), "Sign in must sit ABOVE 'Sign in with Google' (v1.3.2)")
    app.soft_check(app.platform == "ios" or not app.visible("apple_button", 1), "no Apple sign-in on Android")

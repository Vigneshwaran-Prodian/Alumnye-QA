"""Terms & Conditions: once the OTP is entered, tick the 'I accept ...' checkbox and confirm it is ticked.
(The Terms / Privacy links are deliberately NOT used - owner decision 2026-10-03.)"""
import io
import time


def _checkbox(app, timeout=1):
    el = app._try(app.loc.strategies("terms_checkbox", app.platform), timeout)
    if el is not None and app.platform == "android" and (el.get_attribute("class") or "").endswith("EditText"):
        return None          # sanity: a checkbox is never a text input (an XPath engine can mis-order hits)
    return el


def _ticked_fraction(app, el):
    """Share of 'ticked' (teal) pixels inside the checkbox. The hierarchy does not expose the checked state."""
    try:
        from PIL import Image
        r = el.rect
        img = Image.open(io.BytesIO(app.d.get_screenshot_as_png())).convert("RGB")
        crop = img.crop((int(r["x"]), int(r["y"]), int(r["x"] + r["width"]), int(r["y"] + r["height"])))
        px = list(crop.getdata())
        return sum(1 for (R, G, B) in px if G > 120 and R < 90 and B > 100) / max(len(px), 1)
    except Exception:
        return None


def is_ticked(app) -> bool:
    el = _checkbox(app)
    if el is None:
        return False
    if "true" in ((el.get_attribute("checked") or ""), (el.get_attribute("selected") or "")):
        return True
    frac = _ticked_fraction(app, el)
    return frac is not None and frac >= 0.35           # unticked ~0.20 (teal border), ticked ~0.47 (filled)


def tick_terms(app, required=True) -> str:
    """Tick the checkbox if it is not ticked yet. Returns 'ticked', 'already-ticked' or 'missing'."""
    app.dismiss_keyboard()                               # a first tap with the keyboard up can be swallowed
    el = _checkbox(app, 2)
    if el is None:
        if required:
            app.soft_check(False, "no 'I accept the Terms & Conditions and Privacy Policy' checkbox found on the Verify identity screen (FR-UM-16)")
        return "missing"
    if is_ticked(app):
        return "already-ticked"
    try:
        r = el.rect
        app.taps.append(f"terms_checkbox -> {(el.get_attribute('class') or '').split('.')[-1]} at x{int(r['x'])},y{int(r['y'])} {int(r['width'])}x{int(r['height'])}")
    except Exception:
        pass
    el.click()
    time.sleep(0.3)
    ticked = is_ticked(app)
    if not ticked:                                       # one retry; only taps again because we verified it is still unticked
        app.dismiss_keyboard()
        (_checkbox(app) or el).click()
        time.sleep(0.3)
        ticked = is_ticked(app)
    app.soft_check(ticked, "the Terms checkbox did not become ticked after tapping it")
    return "ticked" if ticked else "failed"

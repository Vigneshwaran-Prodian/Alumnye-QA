from alumnye_qa import testdata
from alumnye_qa.session import Blocked

META = dict(id="AUTH-006", title="Returning user signs in with OTP and skips Complete Profile", type="Positive", fresh=True)


def run(app):
    users = testdata.load_users()
    if not users:
        raise Blocked("no registered test user yet - run AUTH-004 first")
    app.sign_in_with_email_otp(users[-1]["email"])
    app.expect_absent("complete_profile_marker", "returning user must not see Complete Profile again")

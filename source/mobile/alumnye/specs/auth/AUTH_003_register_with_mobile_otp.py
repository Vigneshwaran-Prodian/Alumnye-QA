from alumnye_qa import flows, testdata

META = dict(id="AUTH-003", title="New user registers with mobile number + SMS OTP", type="Positive", fresh=True,
            skip="Mobile-number scenarios are out of scope for now (owner decision 2026-10-03); email scenarios only")


def run(app):
    person, mobile = testdata.new_person(), testdata.mobile(app.cfg)
    flows.register_new_user(app, mobile, person)
    app.expect("home_marker", "user lands on Home after Complete Profile")
    testdata.save_user({**person, "mobile": mobile, "via": "mobile"})

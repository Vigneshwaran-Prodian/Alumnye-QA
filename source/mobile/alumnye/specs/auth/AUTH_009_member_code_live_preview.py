import re

from alumnye_qa import flows, testdata

META = dict(id="AUTH-009", title="Member ID (code) on Complete Your Profile follows the typed name: <FirstInitial><LastInitial><n>", type="Positive", fresh=True)


def run(app):
    person = testdata.new_person()
    flows.to_otp_screen(app, person["email"])
    flows.verify_otp(app, person["email"])
    app.wait_screen("complete_profile_marker", "Complete Your Profile screen (step 3 of 3)")
    # The Member ID row sits below Last name: label 'Member ID' with the code chip beside it
    start = app.value_next_to("Member ID")
    app.type("first_name_field", person["first"], "type the first name")
    after_first = app.value_next_to("Member ID")
    app.type("last_name_field", person["last"], "type the last name")
    final = app.value_next_to("Member ID")
    expected = (person["first"][0] + person["last"][0]).upper()
    app.messages += [{"trigger": "Member ID before typing", "text": start or "(empty)", "where": "state"},
                     {"trigger": f"after first name '{person['first']}'", "text": after_first or "(empty)", "where": "state"},
                     {"trigger": f"after last name '{person['last']}'", "text": final or "(empty)", "where": "state"}]
    app.check(bool(final), "the Member ID row shows no code on the Complete Your Profile screen")
    app.soft_check(re.fullmatch(rf"{expected}\d+", final or ""), f"Member ID must be {expected}<n> (e.g. {expected}1) for {person['first']} {person['last']}, got '{final}'")
    app.soft_check(not re.fullmatch(rf"{expected}0\d+", final or ""), f"Member ID '{final}' must have no zero-padding (FR-UM-07)")

# Events - Test Cases (BF3: event creation, categories and category tiles)

**Module:** Events. **Release under test:** Alumnye v1.4 (final). **Criticality: CRITICAL** - every poll, RSVP, payment, itinerary and library item hangs off an event, and v1.4's headline change (category-based tile sets) lives here.
**Depends on (the chain, confirmed by the owner 2026-10-04):** Auth (a signed-in user) -> Group (created by that user) -> Members (people added/invited to the group) -> Event. The runner establishes all three first (`flows.group_ready`): it signs in, makes sure the user owns a group listed on Anchor Home, and makes sure that group already has members (it invites two yopmail test members if it has none). An event is only raised for a group with people in it.
**Sources:** Release v1.4 "Event Category-based Tiles & List" (the three tile sets), Walkthrough 9.1-9.4 and 8.3, FSD Anchor 5.2 (event creation, state machine, RULE-007), MoM 11-Aug-26 (category refactor), Walkthrough RULE-007.
**Platforms:** Android + iOS. **Test data:** group `QA Group <timestamp>`; event titles `QA Evt <timestamp> <REU|SPO|NET|PRO|SOC|CUL|OTH>` (the category name is deliberately NOT in the title so a category check can never be satisfied by the title); description "Automated test event for the category tile check."

## The reference tables every tile scenario is checked against (Release v1.4)
| Category | Tiles shown (exact set, nothing else) | Count |
|---|---|---|
| Reunion | Poll, CostGPT, Itinerary, Launch RSVP, Travel, Preference, Library, Payment | 8 |
| Sports | Poll, Launch RSVP, Golf, Library, Payment | 5 |
| Networking, Professional, Social, Cultural, Other | Poll, Launch RSVP, Library, Payment | 4 |

A tile scenario fails if a tile is missing, if ANY tile outside the table is shown (for example Itinerary on a Social event, or Golf on a Reunion event) or if the count differs.

> **Draft notice:** the Event form and Event Home have not been seen on a device yet; steps follow the documents and the runner reads the live screen. Locators are docs-draft in `locator-maps/Event-Elements.md` and are learned on the first runs. Where the documents are silent (title length limit, duplicate titles, default category) the scenario states the exact accepted outcomes and records what the app does - it never passes on silence.

### TC-EVT-001 - A brand-new group shows "No events yet" with Add Event available
- Priority: High - Type: Positive
- Preconditions: Signed in; a brand-new group WITH members added (but no events).
- Test Data: group `QA Group <timestamp>`
- Steps:
  1. Create a group and land on its Group Details.
  2. Open the Events tab.
- Expected Result: the text "No events yet" and "Tap Add Event above to plan one." are shown; the "Add Event" button is available; no event card (no status badge) is listed.
- Automation script path: source/mobile/alumnye/specs/events/EVT_001_new_group_no_events_state.py
- Notes: Walkthrough 9.4 empty state. Seen on device 2026-10-04 (Group Details).

### TC-EVT-002 - Add Event opens the Event form with every field empty
- Priority: High - Type: Positive
- Preconditions: Group Details of a group that has members.
- Steps: 1. Tap "Add Event". 2. Inspect the form.
- Expected Result: the form shows a title field, a description/details field, a category dropdown and Save; it can be left (Cancel or back arrow); no field contains text. The state of Save (enabled/disabled) on the empty form is written to the report.
- Automation script path: source/mobile/alumnye/specs/events/EVT_002_event_form_layout.py
- Notes: Walkthrough 9.1 "Fields cleared/reset on the Create flow". Unknown extra controls are listed in the discovered-features report.

### TC-EVT-003 - The category dropdown offers exactly the seven categories
- Priority: High - Type: Positive
- Preconditions: Event form open.
- Steps: 1. Tap the category dropdown (a bottom sheet opens). 2. Read every option. 3. Close the sheet.
- Expected Result: exactly 7 options - Reunion, Sports, Networking, Professional, Social, Cultural, Other - none missing, none extra, none repeated. The order shown is recorded.
- Automation script path: source/mobile/alumnye/specs/events/EVT_003_category_list.py
- Notes: Release v1.4 flow step 3; Walkthrough 9.1 "Category dropdown - bottom-sheet".

### TC-EVT-004 - Reunion event shows exactly the 8 Reunion tiles
- Priority: Critical - Type: Positive
- Preconditions: Group Details of the latest group.
- Test Data: category Reunion
- Steps: 1. Add Event, enter the title and description, choose Reunion, Save. 2. Open the event from the Events tab. 3. Read all tiles (scrolling to the end).
- Expected Result: exactly Poll, CostGPT, Itinerary, Launch RSVP, Travel, Preference, Library, Payment (8). Golf is NOT shown. A status badge is shown.
- Automation script path: source/mobile/alumnye/specs/events/EVT_004_reunion_tiles.py
- Notes: Release v1.4 step 5.

### TC-EVT-005 - Sports event shows exactly the 5 Sports tiles
- Priority: Critical - Type: Positive
- Steps: as TC-EVT-004 with category Sports.
- Expected Result: exactly Poll, Launch RSVP, Golf, Library, Payment (5). CostGPT, Itinerary, Travel and Preference are NOT shown. Golf IS shown.
- Automation script path: source/mobile/alumnye/specs/events/EVT_005_sports_tiles.py
- Notes: Release v1.4 step 6.

### TC-EVT-006 .. TC-EVT-010 - Networking, Professional, Social, Cultural, Other each show exactly the 4 shared tiles
- Priority: Critical - Type: Positive (one test case and one script per category)
- Steps: as TC-EVT-004 with the category: 006 Networking, 007 Professional, 008 Social, 009 Cultural, 010 Other.
- Expected Result: exactly Poll, Launch RSVP, Library, Payment (4). Itinerary, CostGPT, Travel, Preference and Golf are NOT shown.
- Automation script paths: source/mobile/alumnye/specs/events/EVT_006_networking_tiles.py, EVT_007_professional_tiles.py, EVT_008_social_tiles.py, EVT_009_cultural_tiles.py, EVT_010_other_tiles.py
- Notes: Release v1.4 step 7. The v1.3 notes/MoM say Itinerary is a "generic tile always available"; v1.4 (final target) lists only 4 shared tiles - see Open Questions.

### TC-EVT-011 - Save returns to Group Details and the event is listed with its category and status
- Priority: High - Type: Positive
- Test Data: category Networking
- Steps: 1. Create a Networking event. 2. Observe the screen after Save. 3. Look at the Events tab.
- Expected Result: Group Details is shown (Walkthrough 9.1 "redirects to Group Details"); the event title is listed; the category "Networking" is shown with it; a status badge is shown; "No events yet" is gone.
- Automation script path: source/mobile/alumnye/specs/events/EVT_011_saved_event_listed.py

### TC-EVT-012 - Event Home shows the entered title and description and a status badge
- Priority: High - Type: Positive
- Test Data: title `QA Evt <timestamp> SOC`, description "Annual alumni get-together at the club house."
- Steps: 1. Create a Social event with that description. 2. Open it.
- Expected Result: Event Home shows the title and the description text; a lifecycle status badge is shown; its initial value is written to the report.
- Automation script path: source/mobile/alumnye/specs/events/EVT_012_event_home_header.py
- Notes: Walkthrough 9.2 status badge.

### TC-EVT-013 - Two events in one group are listed newest first
- Priority: Medium - Type: Positive
- Preconditions: a brand-new group.
- Steps: 1. Create `QA Older <timestamp>`. 2. Create `QA Newer <timestamp>`. 3. Open the Events tab.
- Expected Result: both are listed; "QA Newer" appears above "QA Older".
- Automation script path: source/mobile/alumnye/specs/events/EVT_013_newest_first.py
- Notes: Walkthrough 9.4 "most recent first". If the app orders by event date and both default to the same date the result is reported, not guessed.

### TC-EVT-014 - One event per category: each is listed under its own category
- Priority: Critical - Type: Positive
- Preconditions: a brand-new group.
- Steps: 1. Create seven events, one for each of Reunion, Sports, Networking, Professional, Social, Cultural, Other. 2. Open the Events tab and scroll through the whole list.
- Expected Result: all seven are listed; each is shown under (or carries the label of) its own category - never under another one.
- Automation script path: source/mobile/alumnye/specs/events/EVT_014_grouped_by_category.py
- Notes: Release v1.4 step 8 "displayed as a tile under its selected category". The grouping layout is unseen; the first run records it in the Observed-Behaviour notes.

### TC-EVT-015 / 016 / 017 - Every tile of a category opens its own screen and Back returns
- Priority: High - Type: Positive
- Test Data: 015 Reunion (8 tiles), 016 Sports (5 tiles including Golf), 017 Social (the 4 shared tiles)
- Steps: 1. Create an event of the category and open it. 2. For each tile in its set: tap it, note the screen heading, press Back.
- Expected Result: every tap opens a different screen without an error message; Back returns to Event Home each time. Navigation only - nothing is created.
- Automation script paths: EVT_015_reunion_tiles_open.py, EVT_016_sports_tiles_open.py, EVT_017_common_tiles_open.py (all in specs/events/)

### TC-EVT-018 - The Poll tile opens the Event Polls List (list first)
- Priority: High - Type: Positive
- Steps: 1. Create a Social event and open it. 2. Tap Poll.
- Expected Result: a screen about polls opens that is a list (or its empty state) with a way to create a poll; it is NOT a form with input fields and NOT the poll-type chooser.
- Automation script path: source/mobile/alumnye/specs/events/EVT_018_poll_tile_opens_polls_list.py
- Notes: Walkthrough 9.2 "'Poll' routes to the Event Polls List (list-first UX)". Poll creation itself belongs to BF4.

### TC-EVT-019 - An event cannot be saved without a title
- Priority: High - Type: Negative
- Test Data: title empty, category Reunion
- Steps: 1. Open the form. 2. Choose Reunion only. 3. Try to Save.
- Expected Result: either Save is disabled or a message naming the title/name/required is shown; the form stays open; no event is created. The message wording is logged to the message catalog.
- Automation script path: source/mobile/alumnye/specs/events/EVT_019_empty_title_blocked.py

### TC-EVT-020 - A title of only spaces is not accepted
- Priority: High - Type: Negative
- Test Data: title = 5 spaces, category Reunion
- Steps: as TC-EVT-019 after typing five spaces in the title.
- Expected Result: same as TC-EVT-019 - blocked or refused with a message; the form stays open.
- Automation script path: source/mobile/alumnye/specs/events/EVT_020_spaces_only_title_blocked.py

### TC-EVT-021 - An event cannot be saved without a category
- Priority: High - Type: Negative
- Test Data: valid title and description, no category chosen
- Steps: 1. Fill title and description only. 2. Try to Save. 3. Return to Group Details and look at the Events tab.
- Expected Result: the category is MANDATORY (owner, 2026-10-04): Save is disabled or a message about the category is shown; the form stays open; no event is created and nothing is listed under that title. The message wording is logged to the message catalog.
- Automation script path: source/mobile/alumnye/specs/events/EVT_021_no_category_chosen.py
- Notes: if the app saves the event anyway the scenario fails and reports it as a defect against the owner's rule.

### TC-EVT-022 - Leaving the form without saving creates nothing and keeps nothing
- Priority: Medium - Type: Negative
- Test Data: title, description and category Cultural entered, then Cancel (or Back)
- Steps: 1. Fill the form completely. 2. Leave it with Cancel (or Back). 3. Open the Events tab. 4. Open Add Event again.
- Expected Result: the cancelled event is not listed; the new form is empty.
- Automation script path: source/mobile/alumnye/specs/events/EVT_022_cancel_creates_nothing.py

### TC-EVT-023 - Title length: 1, 100, 255 and 256 characters
- Priority: Medium - Type: Edge
- Preconditions: brand-new group with members (so no earlier title can clash).
- Test Data: titles of exactly 1, 100, 255 and 256 characters, category Social
- Steps: for each length: Add Event, enter the title, Save, note accepted/refused and the message, return to Group Details.
- Expected Result: ALL four are accepted and listed (the owner believes there is no title limit - to be confirmed); a refusal at 255 or 256 means a limit exists and is reported with the message and the length found; the app stays responsive.
- Automation script path: source/mobile/alumnye/specs/events/EVT_023_title_length_boundaries.py
- Notes: no limit is documented. The owner's belief is the expectation until the product owner confirms.

### TC-EVT-024 - A title with symbols, quotes and accents is shown exactly as typed
- Priority: Medium - Type: Edge
- Test Data: `QA & Co's "Meet" 100% #<timestamp> Café`
- Steps: 1. Create a Social event with that title. 2. Find it on the Events tab. 3. Open it.
- Expected Result: listed and shown on Event Home character-for-character as typed.
- Automation script path: source/mobile/alumnye/specs/events/EVT_024_special_characters_title.py

### TC-EVT-025 - The same title can be added twice
- Priority: Medium - Type: Edge
- Preconditions: brand-new group with members.
- Steps: 1. Create `QA Same Title <timestamp>`. 2. Create another event with the identical title.
- Expected Result: the second event is accepted and the Events tab lists the title twice (the owner believes duplicates are allowed - to be confirmed). A refusal fails the scenario and reports the message, so the rule gets confirmed.
- Automation script path: source/mobile/alumnye/specs/events/EVT_025_duplicate_title.py
- Notes: group names reject duplicates; events are expected to differ.

### TC-EVT-026 - The next Add Event form opens empty after a save
- Priority: Medium - Type: Positive
- Steps: 1. Create a Sports event. 2. Tap Add Event again.
- Expected Result: title and description are empty and "Sports" is not preselected.
- Automation script path: source/mobile/alumnye/specs/events/EVT_026_form_resets_between_creates.py
- Notes: Walkthrough 9.1 "Fields cleared/reset on the Create flow".

### TC-EVT-027 - Editing the title updates everywhere
- Priority: High - Type: Positive
- Test Data: Professional event renamed to `QA Renamed <timestamp>`
- Steps: 1. Create the event. 2. Open it, tap Edit, replace the title, Save. 3. Look at the Events tab. 4. Open the event.
- Expected Result: the new title is listed and shown on Event Home; the old title is gone.
- Automation script path: source/mobile/alumnye/specs/events/EVT_027_edit_title.py
- Notes: Walkthrough 9.1 "Event Form (Create / Edit)".

### TC-EVT-028 - Changing the category switches the tile set both ways
- Priority: Critical - Type: Positive
- Steps: 1. Create a Reunion event; check 8 Reunion tiles. 2. Edit: change to Sports, Save; open; check 5 Sports tiles. 3. Edit: change back to Reunion, Save; open; check 8 Reunion tiles.
- Expected Result: each state shows exactly its own table row; no tile from the previous category remains.
- Automation script path: source/mobile/alumnye/specs/events/EVT_028_edit_category_switches_tiles.py

### TC-EVT-029 - After a restart the event, its tiles and its status are unchanged
- Priority: High - Type: Edge
- Steps: 1. Create a Sports event, open it, note the status badge and the tiles. 2. Kill and reopen the app. 3. Open the same event.
- Expected Result: the event is still listed; the tiles are the 5 Sports tiles; the status badge is identical (no phase advances by itself - RULE-007).
- Automation script path: source/mobile/alumnye/specs/events/EVT_029_survives_restart_status_unchanged.py

### TC-EVT-030 - A created event is reachable from the main navigation
- Priority: Medium - Type: Positive
- Steps: 1. Create a Social event. 2. From the bottom navigation open Home, then My Group.
- Expected Result: the event is found in one of them and shows a status badge. The route that worked is written to the report.
- Automation script path: source/mobile/alumnye/specs/events/EVT_030_event_visible_from_home.py
- Notes: Walkthrough 9.4 (Events Home / All Events). The exact screen is unseen; the runner explores Home and My Group.

## Decisions and open questions
1. **Shared tile set - CONFIRMED (owner, 2026-10-04):** Release v1.4 governs. Networking, Professional, Social, Cultural and Other show Poll, Launch RSVP, Library, Payment (no Itinerary).
2. **Category is mandatory - CONFIRMED (owner):** TC-EVT-021 expects a refusal.
3. **No title limit and duplicate titles allowed - owner's belief, not yet confirmed by the product owner:** TC-EVT-023 and TC-EVT-025 expect "accepted"; a different result is reported with the exact message so the rule can be settled.
4. The "tile under its category" layout in the event listing is unseen (TC-EVT-014).
5. Preference tile name: MoM calls it "Travel Preferences"; v1.4 says "Preference". Both are accepted as the same tile.

## Not covered here (deliberately)
- Member-side views of events (events list for a member, empty state "Welcome to Alumnye! You don't have any events yet...", no Add Event button, read-only tiles): need a second user - end-to-end journeys (see journey-catalog.md).
- Promoted (multi-anchor) Anchor creating events: journey layer.
- What each tile does inside (Poll BF4, RSVP/Payment BF5, Itinerary/Travel/Library BF6, Golf BF8) - their own modules. Here only that the tile exists for the right category and opens.
- Event notification SMS (MoM 04-Sep item 22): outside the app UI.

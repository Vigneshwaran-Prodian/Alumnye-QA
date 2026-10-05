# Events - End-to-End User Scenarios (plain language)

Release under test: Alumnye v1.4. For reviewers who do not read scripts.

**Approach 1 - "My group has no events yet"**
Priya has just created a group. Its Events tab says "No events yet - Tap Add Event above to plan one." She taps Add Event and sees an empty form: a title, a description and a category list.
*Covers: EVT-001, EVT-002, EVT-003*

**Approach 2 - "I plan a reunion"**
Priya names the event, picks **Reunion** and saves. She lands back on the group page where the event is listed with its category and a status. She opens it and finds exactly eight tiles: Poll, CostGPT, Itinerary, Launch RSVP, Travel, Preference, Library and Payment - and no Golf.
*Covers: EVT-004, EVT-011, EVT-012*

**Approach 3 - "I plan a golf day"**
Rohan creates an event in the **Sports** category. His event shows five tiles: Poll, Launch RSVP, Golf, Library, Payment. The reunion-only tiles (CostGPT, Itinerary, Travel, Preference) are not there.
*Covers: EVT-005*

**Approach 4 - "A networking mixer, a talk, a get-together, a festival, anything else"**
For Networking, Professional, Social, Cultural and Other events the app offers the same four tiles: Poll, Launch RSVP, Library, Payment. Nothing more.
*Covers: EVT-006, EVT-007, EVT-008, EVT-009, EVT-010*

**Approach 5 - "A busy year"**
Priya adds one event of every category to the same group. The list shows each one under its own category and the newest is at the top.
*Covers: EVT-013, EVT-014, EVT-030*

**Approach 6 - "I tap through everything"**
For a Reunion, a Sports and a Social event, Priya taps every tile in turn; each opens its own page and the back button always returns her to the event. The Poll tile shows the list of polls first, not a form.
*Covers: EVT-015, EVT-016, EVT-017, EVT-018*

**Approach 7 - "I change my mind"**
Priya renames an event and sees the new name everywhere and the old one nowhere. She switches an event from Reunion to Sports and the tiles change to the sports set; switching back restores the reunion set.
*Covers: EVT-027, EVT-028*

**Approach 8 - "Mistakes and odd input"**
She tries to save without a title, with only spaces, and without a category: the app refuses (or applies a clear default) and no half-made event appears. She backs out of a filled form and nothing is created; the next form is empty. Very long titles, titles with quotes and accents, and the same title twice are all handled in a predictable way.
*Covers: EVT-019, EVT-020, EVT-021, EVT-022, EVT-023, EVT-024, EVT-025, EVT-026*

**Approach 9 - "I close the app and come back"**
After a restart the event, its tiles and its status are exactly as she left them; the status never moves on by itself.
*Covers: EVT-029*

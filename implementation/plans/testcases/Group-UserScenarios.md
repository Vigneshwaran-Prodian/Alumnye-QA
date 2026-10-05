# Groups - End-to-End User Scenarios (plain language)

Release under test: Alumnye v1.4. For reviewers who do not read scripts.

**Approach 1 - "I am new and want to start a group"**
Priya has just joined and switches to the Anchor view. The app shows "+ New Group" (with a welcome message if she has no groups yet; a user can create as many groups as they like). She gives her group a name and a short description, saves, and lands on the group's page. Back on her home screen the new group is listed with the date it started.
*Covers: GRP-002, GRP-001*

**Approach 2 - "I check my group page"**
On the group page Priya sees the group's About text, how many members there are (tappable), and an "Add Event" button. Tapping the member count opens the list of members, where she sees herself with her member code.
*Covers: GRP-003, GRP-014*

**Approach 3 - "I invite people"**
Priya opens "Add Members" and finds the ways to invite - Invite, Upload and (from v1.3) Add Members and Add Contacts. She invites a friend by email and sees "The invitation was sent successfully"; the friend now shows as pending.
*Covers: GRP-004, GRP-005*

**Approach 4 - "I bring in a whole batch"**
Priya downloads the template, fills in her list and uploads the file. The app shows a preview of what it understood, she confirms, and the invitations go out. When some rows are wrong (bad email, missing name) the app tells her which rows and still lets the good ones through.
*Covers: GRP-012, GRP-013*

**Approach 5 - "I slip up"**
She tries to invite "abc@" - refused. She tries to invite herself - refused. She invites the same friend twice - refused. She tries to save a group with no name or with a name that already exists - refused. She pastes a very long description - it stops at 200 characters while the counter counts up.
*Covers: GRP-006, GRP-007, GRP-008, GRP-009, GRP-010, GRP-011*

**Not covered here (end-to-end journey):** the invited friend opening the link, registering and accepting; making a member a second Anchor.

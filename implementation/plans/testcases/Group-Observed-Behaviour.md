# Groups - what the live v1.4.0 app really does (device evidence, 2026-10-04)

Corrections to the docs-draft test cases in Group-TestCases.md. The scripts follow THIS file where the two differ.

| Scenario | Docs said | App actually does | Script now checks |
|---|---|---|---|
| GRP-001 | (was: empty state) | A user can own many groups; "Create Group" shows a pop-up "Success / Group created successfully!" with OK | Always creates a new group; the pop-up is acknowledged by the runner |
| GRP-003 | An "About" section, clickable member count | No About section. Under the name: description, Edit, Add Member, Add Event, tabs **Events** and **Members, N** (N = member count), Notice Board card ("0 notices"), empty state "No events yet / Tap Add Event above to plan one." | Each of those; the count is read from the Members tab |
| GRP-004 | Tabs Invite, Upload, Add Members, Add Contacts | Tabs **Invite, Upload, Add Members, Add Contact** (singular). Invite form: Email Address, OR, Mobile Number (10 digits), button **Send Invitation** | All four tabs and the form fields |
| GRP-005 | success message | Banner at the TOP of the app: "Invite sent successfully!" (disappears in a few seconds) | Message read while it is visible |
| GRP-006 | validation on bad email | Banner at the top: "Please enter a valid email format" | Every bad address must give that message (the message is verified, not just the outcome) |
| GRP-007 | own e-mail refused | Earlier run invited a stored test user, not the signed-in one, and the invite was sent | Reads the signed-in e-mail from My Account first; must be refused. **Open question:** if the app really sends an invite to the user's own address, that is a product defect |
| GRP-008 | duplicate invite refused | "User already invited to this group" | unchanged (passed) |
| GRP-010 | duplicate name refused | "A group with this name already exists. Please choose a different name." (shown briefly) | The full sentence must be seen |
| GRP-012 | download template, upload | "Download template" takes the user OUT of the app (Downloads / Drive). The template is **Group_Member_Upload_Template.xlsx** with columns First Name, Last Name, Email, Phone Number | Runner returns to the app (focus guard), pulls the template, builds the 200-member sheet, uploads it |

## Shared test sheet
`data/members_200.xlsx` - built from the downloaded template (same headers), 200 members: First Name `Test001`..`Test200`, Last Name `Member`, Email `qa.member001@yopmail.com`..`qa.member200@yopmail.com`, Phone `9008000001`..`9008000200`. The file name is fixed so later scenarios (bulk-upload variants, journeys, member lists) reuse it.

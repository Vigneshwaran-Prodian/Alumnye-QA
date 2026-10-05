# Groups - Elements (locator map)

**Status: DRAFT from requirement docs (Walkthrough 8.1-8.7, Release 1.3). Group screens not yet seen on a device.** The AI resolves and records what differs; every learned locator is listed under the Adaptation log. Do not put the pipe character in descriptions.

| Key | Kind | Android strategies | iOS strategies | What it does | Last verified |
|---|---|---|---|---|---|
| role_anchor | button | btnx:ANCHOR | btnx:ANCHOR | Home: ANCHOR side of the MEMBER / ANCHOR toggle (seen on device) | seen on device 2026-10-03 |
| role_member | button | btnx:MEMBER | btnx:MEMBER | Home: MEMBER side of the toggle (seen on device) | seen on device 2026-10-03 |
| new_group_button | button | btn:New Group | btn:New Group | Anchor Home: '+ New Group' | docs-draft |
| anchor_home_marker | text | btn:New Group ;; textc:You don't have any groups | btn:New Group ;; textc:You don't have any groups | Anchor Home is open | docs-draft |
| empty_state_text | text | textc:don't have any groups ;; textc:no active groups | textc:don't have any groups ;; textc:no active groups | Anchor Home empty state message | docs-draft |
| group_name_field | input | xpath://android.widget.EditText[contains(@hint,'roup name')] ;; xpath:(//android.widget.EditText)[1] | xpath://android.widget.EditText[contains(@hint,'roup name')] ;; xpath:(//android.widget.EditText)[1] | Group form: name | docs-draft |
| group_description_field | input | xpath://android.widget.EditText[contains(@hint,'escription')] ;; xpath:(//android.widget.EditText)[2] | xpath://android.widget.EditText[contains(@hint,'escription')] ;; xpath:(//android.widget.EditText)[2] | Group form: description (200 chars) | docs-draft |
| save_group_button | button | btnx:Save ;; btnx:Create Group ;; btnx:Create ;; btn:Save | btnx:Save ;; btnx:Create Group ;; btnx:Create ;; btn:Save | Group form: save | docs-draft |
| group_details_marker | text | btn:Add Event ;; btn:Add Member | btn:Add Event ;; btn:Add Member | Group Details is open | seen on device 2026-10-04 (poisoned heal text:MEMBER removed) |
| group_name_title | text | textc:QA Group | textc:QA Group | Group name shown on Group Details | docs-draft |
| about_section | text | textc:About ;; textc:See More | textc:About ;; textc:See More | Group Details: About section - NOT present in v1.4.0 (only the description text under the name) | seen absent 2026-10-04 |
| member_count | button | btn:Members | btn:Members | Group Details: 'Members, N' tab - the number is the member count (seen on device) | seen on device 2026-10-04 |
| add_event_button | button | btn:Add Event | btn:Add Event | Group Details: 'Add Event' (renamed from 'New Event') | docs-draft |
| old_new_event_button | button | btnx:New Event | btnx:New Event | Old label that must be gone | docs-draft |
| add_member_entry | button | btn:Add Member | btn:Add Member | Group Details: entry to add members | seen on device 2026-10-04 (btn:Invite / btn:Members removed: Members is the count TAB) |
| tab_invite | button | btnx:Invite | btnx:Invite | Add Members: Invite tab/option | docs-draft |
| tab_upload | button | btnx:Upload | btnx:Upload | Add Members: Upload tab/option | docs-draft |
| tab_add_members | button | btnx:Add Members | btnx:Add Members | Add Members: add from existing members | docs-draft |
| tab_add_contacts | button | btnx:Add Contact ;; btnx:Add Contacts ;; btnx:Contacts | btnx:Add Contact ;; btnx:Add Contacts ;; btnx:Contacts | Add Members tab labelled 'Add Contact' (docs say 'Add Contacts') | seen on device 2026-10-04 |
| invite_email_field | input | xpath://android.widget.EditText[contains(@hint,'mail')] ;; xpath:(//android.widget.EditText)[1] | xpath://android.widget.EditText[contains(@hint,'mail')] ;; xpath:(//android.widget.EditText)[1] | Invite: email entry | docs-draft |
| send_invite_button | button | btn:Send Invitation ;; btn:Send Invite | btn:Send Invitation ;; btn:Send Invite | Invite: 'Send Invitation' button | seen on device 2026-10-04 |
| pending_invites_text | text | textc:pending ;; textc:invite | textc:pending ;; textc:invite | Group Details / Members: pending invitation count | docs-draft |
| download_template | button | btn:Member Template Download ;; btn:Template Download ;; btn:Download Template | btn:Member Template Download ;; btn:Template Download ;; btn:Download Template | Upload tab: 'Member Template Download' card (.xlsx format file) | seen on device 2026-10-04 |
| choose_file_button | button | btn:.xlsx, .csv ;; btn:.csv ;; btn:Choose File ;; btn:Select File | btn:.xlsx, .csv ;; btn:.csv ;; btn:Choose File ;; btn:Select File | Upload tab: the dashed 'Upload (.xlsx, .csv)' area that opens the file picker (NOT the Upload tab) | seen on device 2026-10-04 |
| bulk_preview_marker | text | textc:Preview ;; textc:Bulk | textc:Preview ;; textc:Bulk | Bulk Preview screen | docs-draft |
| confirm_import | button | btn:Confirm Import ;; btn:Import | btn:Confirm Import ;; btn:Import | Bulk preview: 'Confirm Import' (preview also has Cancel) | seen on device 2026-10-04 |
| members_list_marker | text | textc:Cohort Members ;; textc:Members | textc:Cohort Members ;; textc:Members | Cohort members list | docs-draft |
| remind_button | button | btn:Remind ;; btn:Send Reminder ;; btn:Resend | btn:Remind ;; btn:Send Reminder ;; btn:Resend | Pending invitee: Remind option (seen by the owner in the live app, not in the docs; also in Journey-Elements.md) | docs-draft |
| members_tab | button | btn:Members | btn:Members | Group Details: Members tab with the count (content-desc 'Members, N') | seen on device 2026-10-04 |
| events_tab | button | btnx:Events | btnx:Events | Group Details: Events tab | seen on device 2026-10-04 |
| edit_group_button | button | btnx:Edit | btnx:Edit | Group Details: Edit (group details) | seen on device 2026-10-04 |
| notice_board | button | btn:Notice Board | btn:Notice Board | Group Details: Notice Board card ('0 notices') | seen on device 2026-10-04 |
| no_events_text | button | textc:No events yet | textc:No events yet | Group Details: empty events state ('No events yet' / 'Tap Add Event above to plan one.') | seen on device 2026-10-04 |
| invite_mobile_field | button | xpath://android.widget.EditText[contains(@hint,'mobile')] | xpath://android.widget.EditText[contains(@hint,'mobile')] | Invite: mobile number field (10 digits; OR the email field) | seen on device 2026-10-04 |
| upload_cancel | button | btnx:Cancel | btnx:Cancel | Bulk preview / validation screen: Cancel (leaves the preview) | seen on device 2026-10-04 |

## Adaptation log
- 2026-10-04 19:19 [android] `group_details_marker` -> `text:MEMBER` (self-heal: label 'MEMBER' ~ ['Add Event', 'Add Member'] (score 0.81))

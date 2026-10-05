# Journeys - Elements (locator map, member side + invitation actions)

**Status: DRAFT from requirement docs (Release 1.3 Invitation Flow: the invited user can accept or reject the group invitation; FSD Member). Not yet seen on a device.** Journey scripts also use Group-Elements.md and Auth-Elements.md. The runner explores My Group / other tabs to find these, the AI fills gaps, and every learned locator is listed under the Adaptation log. Do not put the pipe character in descriptions.

| Key | Kind | Android strategies | iOS strategies | What it does | Last verified |
|---|---|---|---|---|---|
| nav_my_group | button | btnx:My Group ;; btn:My Group | btnx:My Group ;; btn:My Group | Bottom nav 'My Group' tab (seen on Home) | seen on device 2026-10-03 |
| invitation_banner | text | textc:invited you ;; textc:invitation ;; textc:invited | textc:invited you ;; textc:invitation ;; textc:invited | Member side: a pending group invitation is shown | docs-draft |
| accept_invite_button | button | btnx:Accept ;; btn:Accept ;; btn:Join | btnx:Accept ;; btn:Accept ;; btn:Join | Member side: accept the group invitation | docs-draft |
| reject_invite_button | button | btnx:Reject ;; btn:Reject ;; btnx:Decline ;; btn:Decline | btnx:Reject ;; btn:Reject ;; btnx:Decline ;; btn:Decline | Member side: reject the group invitation | docs-draft |
| confirm_dialog_yes | button | btnx:Yes ;; btnx:Confirm ;; btnx:OK | btnx:Yes ;; btnx:Confirm ;; btnx:OK | Confirmation dialog after Accept or Reject, if the app asks | docs-draft |
| remind_button | button | btn:Remind ;; btn:Send Reminder ;; btn:Resend | btn:Remind ;; btn:Send Reminder ;; btn:Resend | Anchor side: remind a member whose invitation is still pending | docs-draft |
| pending_member_row | text | textc:Pending ;; textc:Invited | textc:Pending ;; textc:Invited | Anchor side: member row marked pending | docs-draft |
| withdraw_invite_button | button | btn:Withdraw ;; btn:Revoke ;; btn:Cancel Invite ;; btn:Cancel Invitation | btn:Withdraw ;; btn:Revoke ;; btn:Cancel Invite ;; btn:Cancel Invitation | Anchor side: withdraw a pending invitation (existence not confirmed in docs) | docs-draft |

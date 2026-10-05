# Journey Catalog (end-to-end, product-wide)

Rule: RULES.md section 7. Status: **Scripted** = file exists, not yet run on devices. **Planned** = waits for its modules.
Types: Positive / Negative / Edge. Devices: A = Anchor emulator, M = Member emulator.

## Built now (Auth + Groups + invitations)
| ID | Journey | Type | Devices | Status |
|---|---|---|---|---|
| JNY-001 | Anchor invites, member accepts: Anchor's Members count +1, name listed, member leaves Pending (no Remind) | Positive | A+M | Scripted |
| JNY-002 | Anchor invites, member rejects: Members count unchanged, name not listed | Positive | A+M | Scripted |
| JNY-003 | Anchor taps Remind on the member's Pending row, one invitation, member accepts, count +1, Remind gone | Positive | A+M | Scripted |
| JNY-004 | Re-inviting a member who already joined is refused | Negative | A+M | Scripted |
| JNY-005 | Reject, anchor re-invites, member accepts | Edge | A+M | Scripted |
| JNY-006 | Same pending person invited twice: no duplicate invitation | Negative | A+M | Scripted |
| JNY-007 | Withdrawn invitation can no longer be accepted (Blocked if the app has no withdraw option) | Negative | A+M | Scripted |
| JNY-008 | Invitee without an account registers, then sees the invitation | Edge | A+M | Scripted |

## Planned next within invitations (need confirmation of app behaviour)
- Invitee opens an invitation link while signed in as a different account (wrong-account guard) - Negative.
- Invitation link opened with the app not installed (web route) - Edge, needs web/browser step.
- Bulk-upload invite (CSV): every row's member receives an invitation; invalid rows never do - Negative/Edge.
- Anchor adds an existing member from another group: in-app invitation is mandatory, never silent (FRD) - Edge.
- Invitation expiry, if the product has one.

## Planned next from the Events module (BF3) - need the member device
- Member sees the Anchor's event in the events list under its category, with its status badge, after joining (Positive).
- Member sees exactly the same tile set as the Anchor for each category (Reunion 8 / Sports 5 / shared 4) and cannot see or use Add Event / Edit (Role, Negative).
- Member with no events sees "Welcome to Alumnye! You don't have any events yet..." with the calendar icon (Edge).
- Event created while the invitation is still pending: the pending member does not see it; after accepting, the member does (State).
- Promoted (multi-anchor) Anchor creates and edits an event; both Anchors see it (Role).
- Anchor changes the category after the member joined: the member's tiles switch on refresh (State).

## Planned when the modules are generated (BF4-BF8)
Event creation + category tiles; poll (anchor creates, member answers, invalid/duplicate/late answer, reminder); RSVP yes/no/thinking
and payment gating (payment only after RSVP yes - RULE-PAY-003, negative); payment record + reminder; itinerary/travel/library;
profile (member edits, AI profile accept/reject, privacy); golf scoring (two players, cross-scoring). Then full-product
journeys chaining them: sign-up -> group -> invite -> accept -> event -> poll -> RSVP -> payment -> itinerary -> profile,
each with its negative and edge variants.

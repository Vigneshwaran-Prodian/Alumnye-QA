# Coverage Model

Why each scenario earns its place — or deliberately wasn't created.
Dimensions: Functional, Negative, Boundary/Edge, State, Role, Data, Integration, Recovery, UI/Visual, API, Regression impact.

| Scenario ID | Func | Neg | Edge | State | Role | Data | Integ | Recov | UI | API | Regr | Rationale |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

| Item | Reason |
|---|---|
| AUTH-001 | x |  |  |  |  |  | x |  |  |  | x | Gate to everything; session-less launch |
| AUTH-002 |  |  |  |  |  | x |  |  | x |  |  | Explicit v1.3.2 change — easy to regress |
| AUTH-003 | x |  |  | x |  | x | x |  |  |  | x | Primary identifier per FR-UM-09 |
| AUTH-004 | x |  |  | x |  | x | x |  |  |  | x | Overseas/email path FR-UM-15; also feeds later scenarios |
| AUTH-005 | x |  |  | x |  |  | x |  |  |  | x | Third auth method in Delta |
| AUTH-006 | x |  |  | x |  | x |  |  |  |  | x | Returning-user path differs from first-time |
| AUTH-007 | x |  |  | x |  |  | x |  |  | x |  | Golfers on course need persistent sessions |
| AUTH-008 | x |  |  | x |  |  |  |  |  |  | x | Security: session must truly end |
| AUTH-009 | x |  |  |  |  | x |  |  | x |  |  | Unique identifier format rule |
| AUTH-010 |  | x |  |  |  |  |  |  |  |  |  | Input guard |
| AUTH-011 |  | x |  |  |  | x |  |  |  |  |  | OTP security guard |
| AUTH-012 |  | x |  | x |  |  |  |  |  |  |  | Mandatory consent (legal) |
| AUTH-013 |  | x | x |  |  |  |  |  |  |  |  | Data integrity guard |
| AUTH-014 |  |  | x | x |  |  | x |  | x |  |  | Known ambiguous edge (MoM #16) |
| AUTH-015 |  |  | x |  |  | x |  | x |  |  |  | OTP recovery path |
| AUTH-017 |  |  |  |  |  |  |  |  | x |  | x | Explicit v1.3.2 removal; Welcome/Create Account not documented in detail |
| GRP-001 | x |  |  |  |  |  | x |  |  |  | x | Anchor Home state (welcome or group list) |
| GRP-002 | x |  |  | x |  |  | x |  |  | x | x | Core flow: nothing else works without a group |
| GRP-003 | x |  |  |  |  |  | x |  | x |  | x | Group hub screen; renamed button easy to regress |
| GRP-004 | x |  |  |  |  |  | x |  | x |  | x | v1.3 invitation methods; verifies each exists |
| GRP-005 | x |  |  | x |  |  | x | x |  |  | x | Core invitation path |
| GRP-006 |  | x |  |  |  |  |  |  |  |  |  | Input guard |
| GRP-007 |  | x |  |  |  | x |  |  |  |  |  | Explicit documented guard |
| GRP-008 |  | x |  | x |  | x |  |  |  |  |  | Prevents duplicate invitations |
| GRP-009 |  | x | x |  |  |  |  |  |  |  |  | Input guard on the core flow |
| GRP-010 |  | x |  | x |  | x |  |  |  |  |  | Documented validation |
| GRP-011 |  |  | x |  |  |  |  |  |  |  |  | Boundary from the docs |
| GRP-012 | x |  |  | x |  |  | x |  |  |  | x | Bulk onboarding is the main path for large cohorts |
| GRP-013 |  | x | x |  |  | x |  |  |  |  |  | Data-quality guard on bulk import |
| GRP-014 | x |  |  |  |  |  | x |  |  |  | x | Member visibility after group creation |
| EVT-001 | x |  |  | x |  |  |  |  | x |  | x | Empty state guides the first event |
| EVT-002 | x |  |  |  |  |  |  |  | x |  | x | Form is the entry to every event |
| EVT-003 | x |  | x |  |  | x |  |  | x |  | x | Category set drives the tile sets |
| EVT-004 | x |  |  | x |  | x | x |  | x |  | x | Reunion: 8 tiles exact - v1.4 headline |
| EVT-005 | x |  |  | x |  | x | x |  | x |  | x | Sports: 5 tiles incl. Golf - v1.4 headline |
| EVT-006 | x |  |  | x |  | x | x |  | x |  | x | Shared set of 4 |
| EVT-007 | x |  |  | x |  | x | x |  | x |  | x | Shared set of 4 |
| EVT-008 | x |  |  | x |  | x | x |  | x |  | x | Shared set of 4 |
| EVT-009 | x |  |  | x |  | x | x |  | x |  | x | Shared set of 4 |
| EVT-010 | x |  |  | x |  | x | x |  | x |  | x | Shared set of 4 |
| EVT-011 | x |  |  | x |  |  |  |  | x |  | x | Save outcome and listing |
| EVT-012 | x |  |  |  |  | x |  |  | x |  |  | Event Home header and status |
| EVT-013 | x |  |  | x |  |  |  |  |  |  |  | Ordering rule (most recent first) |
| EVT-014 | x |  |  | x |  | x | x |  | x |  | x | Listing grouped by category - v1.4 headline |
| EVT-015 | x |  |  |  |  |  | x |  |  |  | x | Reunion tiles navigate |
| EVT-016 | x |  |  |  |  |  | x |  |  |  | x | Sports tiles navigate incl. Golf |
| EVT-017 | x |  |  |  |  |  | x |  |  |  | x | Shared tiles navigate |
| EVT-018 | x |  |  |  |  |  | x |  | x |  |  | List-first routing into Poll (BF4 boundary) |
| EVT-019 |  | x |  |  |  | x |  |  |  |  |  | Required title |
| EVT-020 |  | x | x |  |  | x |  |  |  |  |  | Whitespace title |
| EVT-021 |  | x |  | x |  | x |  |  |  |  | x | Category rule undocumented - outcomes pinned |
| EVT-022 |  | x |  | x |  |  |  | x |  |  |  | No partial event, no leftover input |
| EVT-023 |  |  | x |  |  | x |  | x |  |  |  | Title boundary found and recorded |
| EVT-024 |  |  | x |  |  | x |  |  | x |  |  | Special characters round trip |
| EVT-025 |  |  | x | x |  | x |  |  |  |  |  | Duplicate behaviour pinned |
| EVT-026 | x |  |  | x |  |  |  |  |  |  |  | Form reset (Walkthrough 9.1) |
| EVT-027 | x |  |  | x |  | x |  |  |  |  | x | Edit propagates |
| EVT-028 | x |  |  | x |  |  | x |  | x |  | x | Category change switches tiles both ways |
| EVT-029 |  |  | x | x |  |  |  | x |  |  | x | Persistence and RULE-007 no auto-advance |
| EVT-030 | x |  |  |  |  |  | x |  |  |  |  | Event reachable from main navigation |

## Deliberately not covered
| Item | Reason |
|---|---|
| Apple sign-in (iOS) | Needs a real Apple ID; only button placement checked (AUTH-002) |
| v1.5 login redesign, biometric, device-persisted identifier | Out of scope (v1.5) |
| Mobile/email duplicate-account rule | Rule not finalised in docs (MoM 04-Sep D5) |
| Forced-update screen | Exists only on pre-1.4 builds |
| Accepting an invite, invite-link routing, multi-anchor, import from another group | Need two users / devices - end-to-end journey layer |
| Add Contacts (beyond presence) | Needs device contacts + SMS; mobile out of scope |
| Edit group / remove member | Not in the minimum set; add if the CR touches them |
| Member-side event views, promoted-Anchor event creation | Need a second user - journey layer |
| Tile contents (Poll, RSVP, Payment, Itinerary, Travel, Library, Golf) | Their own modules BF4-BF8; here only existence per category and navigation |
| Event SMS on creation (MoM 04-Sep item 22) | Outside the app UI |

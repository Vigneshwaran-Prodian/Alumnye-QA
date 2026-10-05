# Scope & Test Approach Decisions — 2026-10-01

Confirmed by project owner:

1. **Target release: v1.4 (final).** Baseline = v1.3 + v1.3.2 (shipped) + v1.4.0 (categories, multi-anchor, D4 poll merge, member AI profile, 12 golf defects ALM-1.3-086..113).
2. **Out of scope: v1.5** items from MoM 04-Sep-26 (sign-in/sign-up redesign, new invite landing screen, biometric, device login persistence, dual-identifier account model, post-sign-out flow).
3. **Doc layout:** baseline docs (BRD, FRD, FSDs, Walkthrough v1.3, Decision Records, QuickStart, golf rules) live in `knowledge/doc/`; CR docs (v1.3, v1.3.2, v1.4.0, MoMs) stay in `knowledge/doc/change-requests/`.
4. **Round Robin PDF** (image-only) was read visually: Green Buddies league rulebook — 4 teams x 11 players, 9-hole 2x2 four-ball match play, 60 matches, Mon/Thu; match win=2 / draw=1 / loss=0; 3/4 handicap allowance, dynamic handicap (downward only, max 2 per game), caps Men 24 / Ladies 28; rainout rule (<5 holes = nullified); captain lineup/forfeit/penalty rules. Largely offline league rules — only test what the app implements (see Golf Plan).
5. **Platforms:** Android + iOS; Android emulator ready.
6. **Test-data / environment approach**
   - Emails: yopmail addresses; valid, realistic person names.
   - OTP: entered **manually** by the tester during CLI execution (script pauses and prompts). No OTP mocking.
   - Google sign-in: tester's Google account is already signed in on the emulator.
   - SMS/email invite links: delivered to yopmail inbox; link opened on device as part of the run.

## Open questions in docs — flag, do not guess expected results
- Member AI profile enablement (Walkthrough §7.6 question vs. v1.4.0 item 4 "Member Profile").
- Poll-answer visibility to members after submission (FR-POLL-12, TBD).

# Events Plan

## Scope (2026-10-04)
BF3 Events: creation, category dropdown, category-based tile sets (the v1.4 headline), listing, edit, persistence. Critical module (polls, RSVP, payments, itinerary, library, golf all hang off an event). 30 scenarios EVT-001..030 (Positive 21, Negative 4, Edge 5).

## Standing checks
- The three tile tables in Event-TestCases.md are the single reference: Reunion 8, Sports 5, shared 4. A tile outside its table fails, even if nothing is missing.
- The category name is never in a generated title, so a category label check cannot be satisfied by the title.
- Where the documents are silent (category mandatory? title limit? duplicate titles?) the scenario pins the ALLOWED outcomes and records which one the app chose - it never passes on silence.
- Tiles are recognised by name (flows.TILE_PATTERNS), not by saved locators: a renamed tile is a visible failure, not a silent heal.

## Decisions
- **Chain (owner, 2026-10-04):** Auth -> Group -> Members -> Event. `flows.group_ready` guarantees a signed-in user, a listed group and members in it before any event is raised; scenarios that need a fresh group use `flows.new_group_ready` (group + 2 invited members).
- Category mandatory (confirmed); title limit none and duplicates allowed (owner's belief, to be confirmed).
- Anchor-side only. Member views, promoted-Anchor creation and the member empty state go to the journey layer (journey-catalog.md).
- Tile contents belong to their own modules; here a tile must exist for the right category and open.
- Event dates: the form's date control is unseen; the runner fills required fields it meets (formfill, AI on failure) and the first run documents the real form.
- Each tile scenario creates its own event through the full user path (Add Event -> Save), then opens it from the Events tab.

## Open questions (flag, don't guess)
See "Decisions and open questions" in Event-TestCases.md: shared tile set and mandatory category are confirmed; title limit and duplicates await product-owner confirmation; listing layout and Preference tile name open.

## Logged UI adaptations
- (none yet - runs append to locator-maps/Event-Elements.md)

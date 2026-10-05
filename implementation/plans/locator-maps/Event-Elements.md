# Events - Elements (locator map)

**Status: DRAFT from requirement docs (Release v1.4 "Event Category-based Tiles & List", Walkthrough 9.1-9.4, FSD Anchor 5.2). The Event form and Event Home have not been seen on a device yet; "Add Event", the Events tab and the "No events yet" empty state are already mapped in Group-Elements.md (seen on device).** Tiles are not mapped one by one: the runner recognises them by name (flows.TILE_PATTERNS), so a renamed tile is reported by the scenario, not silently healed. The first runs may resolve some of these by AI; every learned locator is listed under the Adaptation log. Do not put the pipe character in descriptions.

| Key | Kind | Android strategies | iOS strategies | What it does | Last verified |
|---|---|---|---|---|---|
| event_title_field | input | xpath://android.widget.EditText[contains(@hint,'itle')] ;; xpath://android.widget.EditText[contains(@hint,'ame')] ;; xpath:(//android.widget.EditText)[1] | xpath://XCUIElementTypeTextField[contains(@placeholderValue,'itle')] ;; xpath:(//XCUIElementTypeTextField)[1] | Event form: title | docs-draft |
| event_description_field | input | xpath://android.widget.EditText[contains(@hint,'escription')] ;; xpath://android.widget.EditText[contains(@hint,'etail')] ;; xpath:(//android.widget.EditText)[2] | xpath://XCUIElementTypeTextField[contains(@placeholderValue,'escription')] ;; xpath:(//XCUIElementTypeTextField)[2] | Event form: description / details | docs-draft |
| event_category_dropdown | button | btn:Category ;; textc:Select category ;; textc:Category | btn:Category ;; textc:Select category ;; textc:Category | Event form: category dropdown (bottom sheet) | docs-draft |
| event_save_button | button | btnx:Save ;; btnx:Create Event ;; btnx:Create ;; btnx:Save Event ;; btnx:Update | btnx:Save ;; btnx:Create Event ;; btnx:Create ;; btnx:Save Event ;; btnx:Update | Event form: Save (creates or updates; returns to Group Details) | docs-draft |
| event_cancel_button | button | btnx:Cancel ;; btn:Cancel | btnx:Cancel ;; btn:Cancel | Event form: Cancel | docs-draft |
| event_home_marker | text | btn:Poll ;; btn:Library ;; btn:Payment | btn:Poll ;; btn:Library ;; btn:Payment | Event Home is open (the tile area; Group Details has none of these) | docs-draft |
| event_edit_button | button | btnx:Edit ;; btn:Edit Event | btnx:Edit ;; btn:Edit Event | Event Home: edit the event (opens the same Event form) | docs-draft |

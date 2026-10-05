# Triage — run-20261003-175346

alumnye | android | module `auth`

| Metric | Count |
|---|---|
| total | 1 |
| passed | 0 |
| passed zero ai | 0 |
| passed after self heal | 0 |
| passed after qwen | 0 |
| failed | 0 |
| error | 1 |
| blocked | 0 |
| skipped | 0 |
| ai calls | 0 |

## Scenarios (failures first)

| Status | ID | Type | Title | AI | Category / message | Evidence |
|---|---|---|---|---|---|---|
| ERROR | AUTH-004 | Positive | New user registers with yopmail email + OTP (Terms handled adaptively) | none | driver: Message: 'value' attribute is unknown for the element. Only the following attributes are supported: [checkable, checked, {class,className}, clickable, {content-desc,contentDescription}, enabled, focusable, focused, {long-clickable,longClickable}, package, password, {resource-id,resourceId}, scrollable, selection-start, selection-end, selected, {text,name}, hint, extras, bounds, displayed, contentSize, {a11y-important,importantForAccessibility}, {screen-reader-focusable,screenReaderFocusable}, {input-type,inputType}, {drawing-order,drawingOrder}, {showing-hint,showingHintText}, {text-entry-key,textEntryKey}, {multiline,multiLine}, dismissable, {a11y-focused,accessibilityFocused}, heading, {live-region,liveRegion}, {context-clickable,contextClickable}, {max-text-length,maxTextLength}, {content-invalid,contentInvalid}, {error,errorText}, {pane-title,paneTitle}, {tooltip-text,tooltipText}, {text-has-clickable-span,textHasClickableSpan}, actions, {window-id,windowId}, {text-size,textSize}, {text-unit,textUnit}, {is-collection,isCollection}, {is-collection-item,isCollectionItem}, {collection-info,collectionInfo}, {collection-item-info,collectionItemInfo}] | reports/results/alumnye/run-20261003-175346/AUTH-004_ERROR.png |

## Entry paths the runner navigated (Splash -> ... -> target)

- AUTH-004: Splash -> Skip -> Create account -> Email tab

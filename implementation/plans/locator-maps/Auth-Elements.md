# Auth — Elements (locator map)

**Status: DRAFT from requirement docs — NOT yet verified on a live v1.4 build.** Labels come from FSD Member §3, Walkthrough v1.3 §6, Release v1.3.2. First runs may self-heal; healed locators are written back into this table and listed under "Adaptation log". Strategy forms: `text:` exact, `textc:` contains, `btn:` tappable control containing label, `id:`, `xpath:`. Separator between strategies is ` ;; `.

| Key | Kind | Android strategies | iOS strategies | What it does | Last verified |
|---|---|---|---|---|---|
| identifier_field | input | xpath:(//android.widget.EditText)[1] | xpath:(//XCUIElementTypeTextField)[1] | Create account / Sign in: email or mobile entry (label MOBILE NUMBER on the Mobile tab) | seen on device 2026-10-03 |
| landing_sign_in | button | btnx:Sign in | btnx:Sign in | Landing screen: 'Sign in' (existing user) | seen on device 2026-10-03 |
| landing_create_account | button | btnx:Create account | btnx:Create account | Landing screen: 'Create account' (new user) | seen on device 2026-10-03 |
| primary_button | button | btnx:Continue ;; btn:Continue ;; btn:Sign in ;; btn:Next | btnx:Continue ;; btn:Continue ;; btn:Sign in ;; btn:Next | Create account / Sign in: Continue (DISABLED until the entry is valid) | seen on device 2026-10-03 |
| email_tab | button | btn:Email | btn:Email | Create account / Sign in: Email tab (screen opens on Mobile tab) | seen on device 2026-10-03 |
| mobile_tab | button | btn:Mobile | btn:Mobile | Create account / Sign in: Mobile tab | seen on device 2026-10-03 |
| google_button | button | btnx:Sign in with Google ;; btn:Google | btnx:Sign in with Google ;; btn:Google | Landing: 'Sign in with Google' (below Sign in) | seen on device 2026-10-03 |
| apple_button | button | btn:Apple | btn:Apple | "Sign in with Apple" (v1.3.2: placed BELOW Sign In) | docs-draft |
| or_divider | text | text:or | text:or | Landing divider; app shows 'OR' (matching is case-insensitive) | seen on device 2026-10-03 |
| old_divider_text | text | textc:or use email | textc:or use email | Old divider label that must NOT appear in v1.3.2+ | docs-draft |
| otp_screen_marker | text | textc:Enter verification code ;; textc:Verify identity | textc:Enter verification code ;; textc:Verify identity | Verify identity screen (step 2 of 3) is open | seen on device 2026-10-03 |
| otp_input | input | xpath:(//android.widget.EditText)[1] | xpath:(//XCUIElementTypeTextField)[1] | OTP: SIX separate one-digit boxes (this is the first box; App.enter_otp fills all six) | seen on device 2026-10-03 |
| terms_checkbox | button | xpath://*[contains(@text,'I accept')]/preceding-sibling::android.view.ViewGroup[@clickable='true'][1] | xpath://*[contains(@label,'I accept')]/preceding-sibling::*[1] | Icon-only checkbox LEFT of 'I accept the Terms & Conditions and Privacy Policy' (not the links) | seen on device 2026-10-03 |
| verify_button | button | btn:Verify | btn:Verify | 'Verify & join Alumnye ->' (DISABLED until OTP entered and Terms accepted) | seen on device 2026-10-03 |
| resend_link | button | btn:Resend | btn:Resend | 'Resend code (m:ss)' — disabled while the countdown runs, tappable after it ends | seen on device 2026-10-03 |
| wrong_number_link | button | btn:Wrong | btn:Wrong | '<- Wrong email? Go back' returns to the identifier step | seen on device 2026-10-03 |
| first_name_field | input | xpath://android.widget.EditText[contains(@hint,'irst name')] ;; xpath:(//android.widget.EditText)[1] | xpath:(//XCUIElementTypeTextField)[1] | Complete Your Profile: first name input (hint 'Enter your first name') | seen on device 2026-10-04 |
| last_name_field | input | xpath://android.widget.EditText[contains(@hint,'ast name')] ;; xpath:(//android.widget.EditText)[2] | xpath:(//XCUIElementTypeTextField)[2] | Complete Your Profile: last name input (hint 'Enter your last name') | seen on device 2026-10-04 |
| save_finish_button | button | btnx:Continue ;; btn:Save & Finish ;; btn:Save ;; btn:Finish | btnx:Continue ;; btn:Save & Finish ;; btn:Save ;; btn:Finish | Persists name and completes onboarding | docs-draft |
| skip_nominee | button | btn:Skip | btn:Skip | Skip optional nominee details | docs-draft |
| complete_profile_marker | text | text:Complete Your Profile ;; text:3 of 3 | text:Complete Your Profile ;; text:3 of 3 | Profile step (3 of 3). Exact match: Home has a card 'Complete Your Profile Defaults' that must NOT match | seen on device 2026-10-03 |
| home_marker | text | textc:Welcome, ;; textc:Welcome to Alumnye ;; btnx:My Account ;; textc:My Group | textc:Welcome, ;; textc:Welcome to Alumnye ;; textc:My Group | Home reached: 'Welcome, <name>', bottom nav Home / My Group / My Account, MEMBER / ANCHOR toggle | seen on device 2026-10-03 |
| nav_profile | button | btnx:My Account ;; btn:My Account | btnx:My Account ;; btn:My Account | Bottom nav 'My Account' tab (Home / My Group / My Account); account/sign-out lives here | seen on device 2026-10-03 |
| sign_out | button | btnx:Sign Out ;; btnx:Log out ;; btnx:Logout ;; btn:Sign out | btnx:Sign Out ;; btnx:Log out ;; btnx:Logout | Sign out on the My Account screen (screen not yet seen) | docs-draft |
| confirm_sign_out | button | btnx:Yes ;; btnx:Confirm ;; btnx:Sign Out ;; btnx:Log out | btnx:Yes ;; btnx:Confirm ;; btnx:Sign Out | Optional confirmation dialog on sign-out (only tapped if a dialog is shown) | docs-draft |
| home_welcome | text | textc:Welcome, ;; textc:Welcome to Alumnye | textc:Welcome, ;; textc:Welcome to Alumnye | The Home screen itself (the greeting) - unlike home_marker it is NOT on other screens | seen on device 2026-10-04 |
| splash_skip | button | btnx:Skip | btnx:Skip | Intro slide: Skip (jumps to the landing screen) | seen on device 2026-10-03 |
| splash_next | button | btnx:Next | btnx:Next | Intro slide: Next, a full-width teal button labelled 'Next, ->' (3 slides, page dots above it) | seen on device 2026-10-04 |
| splash_get_started | button | btnx:Get Started | btnx:Get Started | Intro slide: Get Started (leaves the slides) | docs-draft |

## Adaptation log
- 2026-10-03 REVERTED: four Qwen 'adaptations' from run-20261003-232257 pointed landing_sign_in / sign_out at unrelated buttons (Home, Sign Out, My Account). They were wrong and have been removed; the runner now rejects AI answers whose label does not resemble the wanted one.

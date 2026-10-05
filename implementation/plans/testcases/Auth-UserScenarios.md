# Auth — End-to-End User Scenarios (plain language)

For reviewers who do not read scripts. Each "Approach" is a real journey a person takes. Release under test: Alumnye v1.4.

**Approach 1 — "I just installed the app" (first-time user, email)**
Priya installs Alumnye and opens it. After the logo (and any intro slides) she sees three choices: "Sign in" on top, "Sign in with Google" below it, then the word "or" and a "Create account" button. As a new user she taps Create account and types her email. A verification screen asks for a code; she ticks the Terms & Conditions box, types the code she received and taps Verify. The app asks for her first and last name and shows her member code live as she types (for "Priya Nair" it shows PN followed by a number). She taps Save & Finish and lands on her Home screen.
*Covers: AUTH-001, 002, 004, 009, 017 (the app may show intro slides or a Welcome screen first; the test walks through them and checks none offers Google/Apple sign-up)*

**Approach 2 — "I'd rather use my phone number"**
Rahul registers the same way but with his mobile number; the code arrives by SMS. Everything after that is identical.
*Covers: AUTH-003*

**Approach 3 — "I use Google"**
Meera taps "Sign in with Google", picks the account already on her phone, and arrives on Home (filling in her name first if she is brand new).
*Covers: AUTH-005*

**Approach 4 — "I come back every day"**
Priya closes and reopens the app: she goes straight to Home, no login. A week later she signs out from her profile, and the app shows Sign In again. When she signs back in with her email and a fresh code she goes straight to Home and is not asked for her name again.
*Covers: AUTH-006, 007, 008*

**Approach 5 — "I make mistakes"**
Arun types "abc@" as his email — the app refuses to continue. Later he types the wrong code — he sees an error and stays on the screen. Another time he forgets to tick the Terms box — he cannot continue. On the name screen he leaves the names empty or types only spaces — the app will not let him finish.
*Covers: AUTH-010, 011, 012, 013*

**Approach 6 — "Wait, wrong number!"**
Divya notices she typed the wrong number. She taps "Wrong number? Go back", fixes it and carries on. In another try she waits for the code to expire, and the Resend option appears so she can ask for a new one. 
*Covers: AUTH-014, 015*

**Open questions:** What exact wording should the error messages use? (Every message shown during the mistake scenarios is logged to `message-catalog.md` for the team to review.)

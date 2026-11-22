# Beginner guide (SMS + URL version)

## 1. Input (Python, `app.py`)
The user types an SMS and/or URLs (one per line) and presses **Scan**. `scanner.scan()` cleans the text, adds `https://` to domains such as `example.com`, and skips lines that are not URLs.

## 2. Finding warning signs (C++, `cpp/Scanner.cpp`)
- `MessageScanner` looks for OTP/PIN/password requests, urgency, threats, prize/refund lures and payment requests.
- `URLScanner` looks for `@`, punycode, shorteners, login/verify words, long URLs, many subdomains and IP addresses.
- Both inherit from `Scanner` and override `scan()`. `main.cpp` calls them through a `Scanner*` pointer.
- Output lines look like `FINDING=shortener|Uses a shortened URL|15`.

## 3. Removing repeats (C, `dsa/evidence_list.c`)
Python sends the findings to `scamshield_dsa.exe`. For each one, `evidenceInsertEnd()` first calls `evidenceSearch()`; a name already in the list is skipped. The unique list is printed, then `evidenceClear()` frees the memory.

## 4. Score (C++, `cpp/RiskCalculator.cpp`)
`calculate()` adds the points and caps at 100. `label()` gives Safe (0–29), Suspicious (30–59) or Scam (60–100). `reasons()` joins the reasons.

## 5. Display (Python, `app.py`)
Shows the score, label, reasons and a bar chart of points per finding. The Accuracy tab shows the saved ML model results and graphs.

## Example dry run
SMS: "URGENT! Your account is blocked. Send your OTP." URL: `bit.ly/login`
- credentials 20 + urgency 10 + threat 15 + shortener 15 + phishing_word 15 = **75 → Scam**

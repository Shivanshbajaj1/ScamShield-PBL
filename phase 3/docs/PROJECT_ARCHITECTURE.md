# Combined scanning architecture

```text
Streamlit combined form
  ├─ Any selected pair: SMS/message, URL list, QR image, screenshot
  ├─ Any three selected sources
  └─ All four selected sources
          │
          ▼
Python collects and extracts the selected inputs
  ├─ QR URL → URL list
  ├─ QR plain text → message text
  ├─ Screenshot OCR text → message text
  └─ URLs found in SMS/QR/OCR text → URL list
          │
          ▼
Python starts scamshield.exe (C++ SCAN_MULTI)
          │
          ▼
C++ MessageScanner + URLScanner
          │ prints raw FINDING records
          ▼
Python starts scamshield_dsa.exe (C EVIDENCE)
          │
          ▼
C evidence linked list removes duplicate finding names
          │ prints unique FINDING records
          ▼
Python starts scamshield.exe again (C++ CALCULATE)
          │
          ▼
C++ RiskCalculator calculates one score, label and reasons
          │
          ▼
Python starts scamshield_dsa.exe (C ADD)
  ├─ C history linked list saves one combined scan
  └─ C stack stores the scan ID for Undo
```

## Combined score

C++ scanners produce named findings with fixed rule points. The C evidence linked list stores each finding name once. Python passes the unique records to the C++ `RiskCalculator`, which sums the distinct points and caps the result at 100. `label()` applies Safe (0–29), Suspicious (30–59) and Scam (60–100). This is a heuristic score, not a probability.

## Process commands

- **C++ `SCAN_MULTI`:** accepts combined text and URLs; outputs raw finding records.
- **C `EVIDENCE`:** accepts findings; stores each finding name once in a linked list; outputs unique records.
- **C++ `CALCULATE`:** accepts unique findings; outputs score, label and reasons.
- **C `ADD`, `LIST`, `SEARCH`, `UNDO`, `CLEAR`:** manages the persistent history linked list and Undo stack.

Python starts the correct executable with `subprocess`, sends newline-separated input and reads the output. C and C++ remain separate compiled languages. There are no `extern` declarations, DLLs or `ctypes` calls.

## Language responsibilities

- **Python:** interface, QR/OCR extraction, input routing and process coordination.
- **C++:** OOP message/URL scanners and final risk calculation.
- **C:** evidence linked list, history linked list and Undo stack.
- **Optional ML models:** displayed separately; they do not change the rule-based risk score.

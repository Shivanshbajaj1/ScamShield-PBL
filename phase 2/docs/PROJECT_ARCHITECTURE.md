# Architecture (SMS + URL version)

```text
Streamlit page: SMS box + URL box (one URL per line)
        │
        ▼
Python scanner.scan()
  - cleans text, adds https:// to plain domains, skips invalid URLs
        │
        ▼
scamshield.exe  (C++ SCAN)
  MessageScanner + URLScanner through a Scanner* base pointer
  prints FINDING=name|reason|points
        │
        ▼
scamshield_dsa.exe  (C EVIDENCE)
  evidence linked list: evidenceSearch() then evidenceInsertEnd()
  prints only unique findings
        │
        ▼
scamshield.exe  (C++ CALCULATE)
  RiskCalculator: sum points, cap at 100, label, reasons
        │
        ▼
Streamlit shows score, label, reasons and a points bar chart
```

## Commands

- **C++ `SCAN`:** lines = SMS text, number of URLs, then each URL. Output: raw findings.
- **C `EVIDENCE`:** lines = count, then name/reason/points for each finding. Output: unique findings.
- **C++ `CALCULATE`:** same input format as EVIDENCE. Output: `SCORE`, `LABEL`, `REASONS`.

## Why the linked list is needed

If two URLs are both shorteners (e.g. `bit.ly/login` and `tinyurl.com/verify`), C++ reports `shortener` twice. The C list keeps it once, so the score is 30, not 60.

## Language responsibilities

- **Python:** interface, input cleaning, running the programs, graphs.
- **C++:** OOP scanners and risk calculation.
- **C:** evidence linked list.
- **ML models:** shown for information only; they do not change the score.

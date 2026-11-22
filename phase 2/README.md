# Phase 2 — SMS and URL prototype

This is the Phase II ScamShield implementation snapshot. It scans SMS/message text and one or more URLs, then returns a rule-based risk score, classification and reasons.

## Architecture

- **Python / Streamlit:** interface, URL normalization, optional ML outputs and dashboard (`app.py`, `scanner.py`).
- **C++ OOP:** message and URL scanners plus the risk calculator (`cpp/`).
- **C DSA:** singly linked list for deduplicating evidence (`dsa/`).

Python invokes the native programs with `subprocess`. The model output is informational only and does not change the rule-based score.

## Run on Windows

Follow [WINDOWS_SETUP.md](WINDOWS_SETUP.md), then from this folder run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\build.bat
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Install GCC/G++ as described in the setup guide before building. This phase does not include QR/OCR, saved scan history or Undo; those are in Phase III.

## Shared supporting material

The common research notes, papers, training scripts and datasets are stored once at the repository root in [`research_and_datasets/`](../research_and_datasets/). The Phase II model files and `models/metrics.json` remain in this phase folder.

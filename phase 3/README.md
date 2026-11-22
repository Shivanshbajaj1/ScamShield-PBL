# Phase 3 — Combined-input implementation

This is the later integrated ScamShield snapshot. A user can submit one input or combine SMS/message text, one or more URLs, a QR-code image and a screenshot in one scan session.

## Features

- Combined 0–100 rule-based risk score with Safe / Suspicious / Scam labels and reasons.
- QR decoding with OpenCV; optional screenshot OCR with local Tesseract.
- URLs found in messages, QR content or screenshot text are also sent to URL checks.
- C evidence linked list deduplicates repeated finding types.
- C history linked list stores a combined scan record; C stack supports Undo.
- Streamlit dashboard, JSON export and optional SMS/URL ML outputs.

The rule score is not a probability or a guarantee. The model outputs are supplementary and do not change the C++ rule-based score.

## Run on Windows

Follow [WINDOWS_SETUP.md](WINDOWS_SETUP.md), then from this folder run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\build.bat
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m streamlit run app.py
```

GCC/G++ is required for native compilation. QR decoding uses OpenCV. Screenshot OCR is optional and requires Tesseract installed separately and available on PATH. Both native executables must be built before scanning/history features are available.

## Code map

- `app.py`: Streamlit input form, combined result display, dashboard and history UI.
- `scanner.py`: input preprocessing, QR/OCR helpers, subprocess calls, optional models and history orchestration.
- `cpp/`: C++ message/URL scanners and risk calculator.
- `dsa/`: C evidence list, history list and Undo stack.
- `tests/`: single-input and combined-input tests.
- `docs/`: architecture, syllabus mapping, beginner guide, test results and viva questions.
- `models/`: optional SMS/URL model files and saved evaluation metrics.

Shared research notes, papers, scripts and datasets are stored at the repository root in [`research_and_datasets/`](../research_and_datasets/).

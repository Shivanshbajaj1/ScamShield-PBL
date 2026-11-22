# ScamShield — Explainable Multimodal Scam Screening

ScamShield is a three-phase student Project-Based Learning (PBL) project for screening suspicious messages and URLs, with the Phase III version adding QR-code and screenshot text extraction. It presents explainable warning signs and a rule-based risk score to help users pause and verify suspicious content.

> **Educational tool only:** a Safe result is not proof that content is harmless. ScamShield does not open submitted URLs, contact threat-intelligence services, or replace security software or official reporting channels.

## Project at a glance

| Phase | Purpose | Main contents |
|---|---|---|
| [Phase 1](phase%201/) | Project proposal and initial design | Proposal source, presentation, report and assets |
| [Phase 2](phase%202/) | SMS and URL prototype | Streamlit UI, Python coordinator, C++ scanners, C evidence list, model metrics, tests and research |
| [Phase 3](phase%203/) | Combined-input version | SMS, URL, QR and screenshot inputs; C/C++ components; scan history and Undo; tests and documentation |
| [Shared research](research_and_datasets/) | Common supporting material | Research notes, datasets, papers and optional training scripts |

Phase 2 and Phase 3 are preserved as separate snapshots. Phase 3 is the later integrated version; the Phase 2 files are retained for project history and comparison.

## Phase III features

- Scan any one input or a combination of message text, URLs, QR-code image and screenshot.
- Route URLs found in message, QR or screenshot text to URL checks.
- Show one combined 0–100 score, Safe / Suspicious / Scam label and reasons.
- Deduplicate repeated finding types before scoring.
- Save a local scan-history record and support Undo of the latest record.
- Show optional SMS/URL model outputs and saved evaluation metrics separately from the rule-based score.
- Export a combined scan result as JSON.

### Risk score bands

| Score | Label |
|---:|---|
| 0–29 | Safe |
| 30–59 | Suspicious |
| 60–100 | Scam |

The score is a configured rule-based indicator, not a probability of fraud or a guarantee of safety. Existing ML outputs are supporting information and do not change the C++ rule score.

## Architecture (Phase III)

1. **Streamlit (`app.py`)** provides the user interface and dashboard.
2. **Python (`scanner.py`)** extracts QR text, optionally uses local Tesseract for screenshot OCR, normalizes URLs and coordinates the scan workflow.
3. **C++ (`cpp/`)** implements the message/URL scanners and risk calculation.
4. **C (`dsa/`)** implements evidence deduplication, a linked list for scan history and a stack for Undo.
5. Python starts the native C/C++ executables through `subprocess`; the project does not use DLL/`ctypes` integration or a cloud database.

## Run Phase III on Windows

See [Phase 3 setup instructions](phase%203/WINDOWS_SETUP.md). In PowerShell, from the `phase 3` folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\build.bat
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The native build requires GCC/G++ (the documented Windows setup uses MSYS2 UCRT64). QR decoding uses OpenCV. Screenshot OCR is optional and requires Tesseract installed separately and available on PATH.

## Run Phase II

See [Phase 2 setup instructions](phase%202/WINDOWS_SETUP.md). Phase 2 is the earlier SMS/URL-only application.

## Tests and verification

During the repository preparation review on 23 November 2026, the Phase 2 and Phase 3 C/C++ sources were compiled with GCC/G++ in the Linux review environment and the supplied Python unit tests were executed against the resulting native executables:

| Check | Phase 2 | Phase 3 |
|---|---:|---:|
| Native C/C++ compilation | Passed | Passed |
| Python unit tests | 10/10 passed | 21/21 passed |

This does not claim that the Windows build, interactive Streamlit walkthrough or Tesseract OCR on another computer has been verified. See each phase's `docs/TEST_RESULTS.md` for scope and limitations.

## Models, metrics and datasets

The supplied SMS and URL model files, `metrics.json`, and dataset/research materials are included with the phase archives and shared research directory. The models are optional at scan time; the saved metrics describe the stated holdout experiments, not the accuracy of QR/OCR processing or of the full combined rule engine. Dataset and paper reuse must follow the source's terms and citations.

The PhiUSIIL URL CSV is a large file. GitHub may show a size warning for it, but it remains below GitHub's 100 MB single-file limit. For teams wishing to keep clones smaller, Git LFS can be used instead.

## Team

| Member | Project responsibility |
|---|---|
| Shivansh Bajaj | Team lead, system architecture, Streamlit/Python workflow and integration |
| Ashrey Goel | C++ OOP scanner/risk engine and C DSA integration |
| Kangana Agarwal | Research/dataset work, ML support, testing, validation and documentation |

See [`CONTRIBUTION_MAP.md`](CONTRIBUTION_MAP.md) and [`team member contributions/`](team%20member%20contributions/) for the responsibility-based file map. The map describes the team's assigned work areas; it does not rewrite Git commit authorship or claim that every file was individually authored by one person.

## Repository structure

```text
ScamShield-PBL/
├── README.md
├── CONTRIBUTION_MAP.md
├── phase 1/
├── phase 2/                 # SMS + URL prototype
├── phase 3/                 # Combined-input implementation
├── research_and_datasets/   # Shared research/dataset source material
└── team member contributions/
```

## Responsible use

Do not submit real passwords, OTPs, payment details or private messages. Keep local history private. Verify suspicious claims through a separately obtained official channel. Never rely on a Safe label alone.

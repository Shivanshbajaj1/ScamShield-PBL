# Phase 3 upload status

This folder is the Phase 3 integrated snapshot area.

## Committed to this repository

The following Phase 3 code files have been committed as complete files in the source-module commit:

### C++ OOP
- `cpp/Scanner.cpp`
- `cpp/Scanner.h`
- `cpp/RiskCalculator.cpp`
- `cpp/RiskCalculator.h`
- `cpp/main.cpp`

### C DSA
- `dsa/evidence_list.c`
- `dsa/evidence_list.h`
- `dsa/main.c`
- `dsa/history_list.c`
- `dsa/history_list.h`
- `dsa/undo_stack.c`
- `dsa/undo_stack.h`

## Not yet transferred from the Phase 3 ZIP

The supplied Phase 3 archive also contains the Streamlit UI and Python integration (`app.py`, `scanner.py`), README and Windows setup/build files, tests, documentation, model metrics and joblib models, research papers/scripts, and datasets (including a large URL CSV).

Those files have not been included in the source-module commit. Do not treat this folder as a fully runnable, end-to-end Phase 3 checkout until the remaining runtime files and assets are added.

## Team repositories

The current connected GitHub App has not been able to write to Ashrey's and Kangana's repositories: GitHub returns HTTP 403 from the blob/contents write APIs, despite repository metadata displaying push access. The per-member repositories therefore have not been updated by this operation.

The contribution mapping in the central repository is based on the supplied Phase-II progress report and project archive. It does not rewrite commit authorship or assert that every mapped file was individually authored by a specific member.

## Source integrity check

The 12 C/C++ files listed above were compared with the extracted Phase 3 ZIP using Git blob SHA-1 values. All 12 blob IDs match exactly, so those files are byte-for-byte copies of the supplied Phase 3 source files. The history-list source was re-uploaded from the archive and re-verified.

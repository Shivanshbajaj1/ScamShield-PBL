# ScamShield contribution map

This page records the team's responsibility areas and links them to relevant parts of the project. It is a project-role map, not an assertion that Git commit authorship can be reassigned or that every file in a mapped folder was solely written by one person.

## Shivansh Bajaj — team lead, architecture and integration

- Overall project architecture and integration of the phase-wise implementations.
- Streamlit user interface and Python orchestration (`phase 2/app.py`, `phase 2/scanner.py`, `phase 3/app.py`, `phase 3/scanner.py`).
- Coordination between Python, the C++ scanning/risk modules and C DSA processes.
- Integration of the combined-input workflow and project-level documentation.

See [individual contribution notes](team%20member%20contributions/Shivansh%20Bajaj/README.md).

## Ashrey Goel — C++ OOP and DSA integration

- C++ scanner classes and risk calculation (`phase 2/cpp/`, `phase 3/cpp/`).
- C data-structure components (`phase 2/dsa/`, `phase 3/dsa/`), including evidence handling and Phase III history/Undo structures.
- Native build integration with the Python coordinator.

See [individual contribution notes](team%20member%20contributions/Ashrey%20Goel/README.md).

## Kangana Agarwal — research, ML support and validation

- Research and dataset planning, source review and literature notes (`research_and_datasets/`).
- Training/evaluation support scripts and supplied evaluation metrics/model resources.
- Test cases, validation notes, beginner/viva material and project documentation.

See [individual contribution notes](team%20member%20contributions/Kangana%20Agarwal/README.md).

## Phase responsibilities

| Phase | Project emphasis |
|---|---|
| Phase 1 | Proposal, initial problem framing and presentation material |
| Phase 2 | SMS/URL prototype and first C/C++/Python integration |
| Phase 3 | Combined input scanning, QR/OCR, evidence deduplication, history and Undo |

For an accurate record of personal Git contributions, use GitHub's commit history and pull-request history. The responsibility map above is based on the team's supplied project-role description.

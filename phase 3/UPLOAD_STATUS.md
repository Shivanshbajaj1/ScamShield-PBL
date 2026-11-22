# Phase 3 source and verification status

This folder now contains the complete supplied Phase III source archive: Streamlit application, Python coordinator, C++ scanner/risk engine, C evidence/history/Undo structures, model artifacts/metrics, tests, Windows setup/build scripts and phase-specific documentation.

Common research notes, papers, training scripts and datasets are stored once at repository root in `research_and_datasets/` because these files are identical in the Phase II and Phase III archives.

## Review verification (23 November 2026)

- C DSA sources compiled as C11 with GCC in the Linux review environment.
- C++ scanner and risk calculator compiled as C++17 with G++ in the Linux review environment.
- Python unit tests: **21/21 passed** after both native executables were built.

The tests cover the implemented unit/process paths but do not replace a Windows build and interactive UI walkthrough. Tesseract OCR on the target Windows computer remains an environment-specific check.

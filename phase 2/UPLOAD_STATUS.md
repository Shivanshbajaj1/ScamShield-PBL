# Phase 2 source and verification status

This folder now contains the complete Phase II archive contents: the Streamlit application, Python coordinator, C++ scanner and risk calculator, C evidence-list implementation, model artifacts/metrics, tests, setup/build scripts and phase-specific documentation.

Common research notes, papers, training scripts and datasets are stored once at repository root in `research_and_datasets/` because these files are identical in the Phase II and Phase III archives.

## Review verification (23 November 2026)

- C DSA sources compiled with GCC in the Linux review environment.
- C++ scanner and risk calculator compiled with G++ in the Linux review environment.
- Python unit tests: **10/10 passed** after the native executables were built.

Windows `build.bat`, interactive Streamlit browser use and Tesseract are not claimed as independently re-tested in this review.

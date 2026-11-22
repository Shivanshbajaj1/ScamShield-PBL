# Phase 2 upload status

This folder preserves the earlier SMS/URL implementation snapshot.

## Committed source modules

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

The source modules were copied from the supplied Phase 2 ZIP. The scanner and risk-calculator modules are byte-for-byte identical to the matching Phase 3 files in the supplied archives.

## Not yet transferred from the Phase 2 ZIP

The archive also contains the Streamlit/Python app and scanner coordinator, Windows setup/build scripts, requirements, documentation, tests, model metrics and model files, research notes/papers, and training/evaluation scripts and datasets. They are not included in this Phase 2 source-module commit.

The Phase 2 presentation PDF is stored in this folder as `ScamshieldPhase2ppt.pdf`.

## Source integrity check

The eight C/C++ source files listed above were compared with the extracted Phase 2 ZIP using Git blob SHA-1 values. All eight blob IDs match exactly, so they are byte-for-byte copies of the supplied Phase 2 source files.

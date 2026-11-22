# Test results — Phase 2 (SMS + URL)

Reviewed on 23 November 2026 in a Linux environment. The C DSA executable and C++ scanner executable were compiled from the supplied source with GCC/G++ first; then the Python unit test suite was run against those executables.

| Check | Result |
|---|---|
| C DSA compile (`gcc -std=c11 -Wall -Wextra`) | PASS |
| C++ scanner/risk calculator compile (`g++ -std=c++17 -Wall -Wextra`) | PASS |
| Python unit tests | PASS — 10/10 |
| Safe SMS and shipping false-positive check | PASS |
| Scam SMS and suspicious URL checks | PASS |
| SMS + URL combined result | PASS |
| Evidence linked-list deduplication | PASS |
| Domain without scheme accepted | PASS |
| Invalid URL skipped while valid SMS is scanned | PASS |
| Empty input and missing executable errors | PASS |

## Not verified in this review

- Windows `build.bat` execution on the target laptop.
- Interactive Streamlit browser walkthrough.
- OCR/QR input, which is not part of the Phase II implementation.

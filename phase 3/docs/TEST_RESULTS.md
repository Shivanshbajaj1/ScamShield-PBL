# Test results — Phase 3 (combined inputs)

Reviewed on 23 November 2026 in a Linux environment. C sources were compiled as C11 with GCC and C++ sources as C++17 with G++; the Python test suite was then executed against both native executables.

| Check | Result |
|---|---|
| C DSA compile (`gcc -std=c11 -Wall -Wextra`) | PASS |
| C++ scanner/risk calculator compile (`g++ -std=c++17 -Wall -Wextra`) | PASS |
| Python unit tests | PASS — 21/21 |
| SMS and URL rules and validation | PASS |
| Combined QR text + screenshot text scoring path | PASS |
| All four source types in one combined scan | PASS |
| Deduplication of repeated evidence | PASS |
| Scan history add/list/search and C stack Undo | PASS |
| Every two-source pair (6 combinations) | PASS |
| Every three-source combination (4 combinations) | PASS |

## Not verified in this review

- Windows `build.bat` execution on the target laptop.
- Interactive Streamlit browser walkthrough on Windows.
- Tesseract OCR installed and working on the target laptop.
- Real camera/phone QR images and screenshot OCR on the target laptop.

The automated tests confirm the paths covered by the test suite; they do not establish production detection performance or guarantee that every real scam will be detected.

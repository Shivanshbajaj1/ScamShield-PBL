# Beginner guide: explain the combined ScamShield implementation

This project is designed for a second-year B.Tech CSE (AI & ML) student, III Semester. It demonstrates syllabus-level C, DSA, C++ OOP and basic Python integration.

## 1. Combined input form

- **What:** The user can submit any combination of SMS text, URL(s), a QR image and a screenshot.
- **How:** Streamlit collects optional fields in one form. QR URLs and URLs extracted from SMS/OCR text join the URL list. QR plain text and screenshot OCR text join message text.
- **Concept:** Python functions, dictionaries, lists, conditions, file upload and exception handling.

## 2. C++ message and URL scanners

- **Files:** `cpp/Scanner.h`, `cpp/Scanner.cpp`, `cpp/main.cpp`.
- **What:** `MessageScanner` checks combined text; `URLScanner` checks every collected URL.
- **How:** Each class uses straightforward `if` statements. The base `Scanner` class has a virtual `scan()` function. A base-class pointer calls each derived scanner.
- **Concept:** classes, objects, constructors, inheritance, overriding, virtual functions and runtime polymorphism.
- **Output:** C++ prints `FINDING=name|reason|points` lines. The Python integration passes those findings to the C evidence linked list.

## 3. C evidence linked list

- **Files:** `dsa/evidence_list.h`, `dsa/evidence_list.c`, `dsa/main.c`.
- **What:** Stores unique warning findings from the current combined scan temporarily.
- **How:** Python sends the finding records to `scamshield_dsa.exe` with the `EVIDENCE` command. `evidenceInsertEnd()` adds a node unless `evidenceSearch()` finds the same finding name. The C program prints the unique findings and clears the list before exiting.
- **Concept:** C structures, pointers, singly linked list, insert-at-end, linear search, traversal and dynamic memory.
- **Important:** Duplicate removal is performed by the C linked list, not by a global C++ variable.

## 4. C++ RiskCalculator

- **Files:** `cpp/RiskCalculator.h`, `cpp/RiskCalculator.cpp`, `cpp/main.cpp`.
- **What:** Calculates one final score for the whole combined scan.
- **How:** Python sends the unique findings returned by C to the C++ executable using the `CALCULATE` command. `calculate()` adds the distinct finding points and caps the score at 100. `label()` applies 0–29 Safe, 30–59 Suspicious and 60–100 Scam.
- **Concept:** constructors, private data members, public member functions, vector traversal and simple arithmetic.
- **Important:** The score is a rule-based indicator, not a mathematically verified probability.

## 5. C linked-list history

- **Files:** `dsa/history_list.h`, `dsa/history_list.c`, `dsa/main.c`.
- **What:** Stores one record per combined scan: ID, date/time, input type, score, label, reasons and preview.
- **How:** Python sends `ADD`, `LIST` or `SEARCH` commands to the C DSA executable. `history_add()` creates a node; `history_print()` traverses; `history_search()` searches; `history_delete()` removes a record. Data is saved in `history.txt`.
- **Concept:** C structures, pointers, `calloc`, `free`, singly linked list, traversal, linear search and file handling.

## 6. C stack and Undo

- **Files:** `dsa/undo_stack.h`, `dsa/undo_stack.c`, `dsa/main.c`.
- **What:** Removes the latest combined scan.
- **How:** The saved history IDs are loaded oldest-to-newest and pushed onto the stack. The `UNDO` command pops the latest ID and deletes that record from the history linked list.
- **Concept:** stack, push, pop, LIFO and dynamic memory.

## 7. Python and subprocess integration

- **File:** `scanner.py`.
- **What:** Python coordinates the Streamlit interface, C++ scanner/calculator and C DSA program.
- **How:** `run_cpp_engine()` sends `SCAN_MULTI` or `CALCULATE` commands to `scamshield.exe`. `run_dsa_engine()` sends evidence/history/undo commands to `scamshield_dsa.exe`. Both use standard input and read standard output.
- **Concept:** functions, lists, dictionaries, paths, exception handling and process input/output.
- **Why separate executables:** C source is compiled as C and C++ source is compiled as C++. This avoids direct mixed-language function linkage and avoids `extern` declarations, DLLs or `ctypes`.

## 8. QR and screenshot processing

QR URLs go into the URL list; QR plain text goes into message scanning. Screenshot OCR text goes into message scanning, while URLs found in OCR are also URL-scanned. OCR requires a separate Tesseract installation.

## 9. Existing ML models and charts

Optional SMS and URL model outputs and evaluation charts are supporting information only. They do not alter the combined C++ risk score. Saved metrics are test-set results, not live-scan accuracy.

## DSA scope

The implemented structures are two singly linked lists and one stack. The project does not claim queue, BST, graph, BFS or DFS functionality.

## Namespace style and build

All DSA implementation files are genuine `.c` files compiled by `gcc -std=c11`. C++ files use `using namespace std;` and do not use `std::` prefixes. No `extern` declarations are used. Run `build.bat` to create both `scamshield_dsa.exe` and `scamshield.exe`.

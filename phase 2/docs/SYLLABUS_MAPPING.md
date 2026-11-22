# Syllabus mapping

| Concept | File → function | Use |
|---|---|---|
| Structures and pointers | `dsa/evidence_list.c` → `EvidenceNode` | Each node holds one finding and a `next` pointer. |
| Dynamic memory | `evidenceInsertEnd`, `evidenceClear` | `malloc` creates nodes; `free` releases them. |
| Singly linked list (insert at end, traversal) | `evidenceInsertEnd`, `evidenceCount`, `evidenceGet` | Stores unique findings of the current scan. |
| Linear search | `evidenceSearch` | Checks if a finding name already exists before inserting. |
| Classes, objects, constructors | `cpp/Scanner.h`, `RiskCalculator.h` | Scanner classes and RiskCalculator. |
| Encapsulation | `Scanner::scanner_name`, `RiskCalculator::maximum_score` | Private data used through public functions. |
| Inheritance and overriding | `MessageScanner::scan`, `URLScanner::scan` | Both override the pure virtual `Scanner::scan`. |
| Runtime polymorphism | `cpp/main.cpp` → `Scanner *scanner` | Base pointer calls the correct derived `scan`. |
| Process integration | `scanner.py` → `run_program` | Python sends lines to the C/C++ programs and reads output. |

## DSA scope

Only one data structure is used: the evidence singly linked list. The history linked list, Undo stack and file handling were removed together with the history feature. No queue, BST or graph is claimed.

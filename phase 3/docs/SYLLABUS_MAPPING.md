# Syllabus mapping

| Course concept | Actual file and function | How it is used |
|---|---|---|
| Structures and pointers | `dsa/history_list.h` → `HistoryNode`; `dsa/evidence_list.c` → `EvidenceNode` | The C linked lists use `next` pointers to connect records. |
| Dynamic memory | `dsa/history_list.c` → `history_add`, `history_load`; `dsa/evidence_list.c` → `evidenceInsertEnd` | `calloc`/`malloc` create nodes and `free` releases them. |
| Singly linked list | `dsa/history_list.c` → `insert_beginning`, `insert_end`, `history_print`, `history_delete` | New scans are inserted at the beginning; file records reload at the end; traversal and delete support history and Undo. |
| Stack | `dsa/undo_stack.c` → `stack_push`, `stack_pop` | Stores record IDs; Undo removes the newest saved scan (LIFO). |
| Array and linear traversal | `dsa/history_list.c` → `save_file`, `history_last_id`, `history_print` | A small pointer array writes history oldest-to-newest; traversal walks from `head` to `NULL`. |
| Linear search | `dsa/history_list.c` → `history_search`; `dsa/evidence_list.c` → `evidenceSearch` | Searches saved history or checks whether a finding name already exists. |
| Evidence linked list | `dsa/evidence_list.c` → `evidenceInsertEnd`, `evidenceSearch`, `evidenceGet`, `evidenceClear` | Stores unique findings from the current scan before the C++ risk calculation. |
| File operations | `dsa/history_list.c` → `save_file`, `history_load` | Saves and reloads `history.txt`. |
| Classes/objects and constructors | `cpp/Scanner.h`, `Scanner.cpp`, `RiskCalculator.cpp` | Scanner classes and RiskCalculator use constructors and member functions. |
| Encapsulation | `cpp/Scanner.h`, `cpp/RiskCalculator.h` | Private fields are accessed through public member functions. |
| Inheritance/overriding | `Scanner`, `MessageScanner::scan`, `URLScanner::scan` | Both derived classes implement the base `scan` function. |
| Runtime polymorphism | `cpp/main.cpp` → `Scanner *scanner` | A base-class pointer calls the correct derived scan method. |
| C/C++ process integration | `scanner.py` → `run_cpp_engine`, `run_dsa_engine` | Python sends simple line-based input and reads output from separate C and C++ executables. |

## Intentional DSA choices

The implemented structures have direct roles: the evidence linked list stores unique findings, the history linked list stores saved scans, and the stack implements Undo. No queue, BST, graph, BFS or DFS is claimed in this version. These are not required by the present one-session scan workflow, so they are not added just for decoration.

## C and C++ build note

The DSA source files use the `.c` extension and are compiled by `gcc` in C11 mode. The scanner classes and risk calculator use `.cpp` files and are compiled by `g++` in C++17 mode. Python coordinates the two executables with `subprocess`; there are no `extern` declarations or mixed-language direct function calls. The C++ source files use `using namespace std;` and do not use `std::` prefixes.

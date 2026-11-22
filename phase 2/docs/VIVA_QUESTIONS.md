# Viva questions

1. **What does ScamShield check?** One SMS and/or up to 10 URLs, giving one 0–100 score.
2. **Why C, C++ and Python?** C for the linked list, C++ for OOP scanners and scoring, Python for the interface and joining the programs.
3. **How does Python call C/C++?** With `subprocess`: it writes lines to the program's standard input and reads its standard output.
4. **Why two executables?** C and C++ are compiled separately (`gcc` and `g++`), so no `extern` or DLL is needed.
5. **Where is the score calculated?** `RiskCalculator::calculate()` in `cpp/RiskCalculator.cpp`.
6. **What is runtime polymorphism here?** `main.cpp` uses `Scanner *scanner`, pointing first to `MessageScanner`, then to `URLScanner`; the virtual `scan()` runs the right version.
7. **What does the linked list do?** Keeps each finding name only once so the same sign from two URLs is not counted twice.
8. **How does it avoid duplicates?** `evidenceSearch()` is called inside `evidenceInsertEnd()`; if the name exists, the node is not added.
9. **Time complexity of insert-at-end?** O(n): we walk to the last node.
10. **Time complexity of evidenceSearch?** O(n): linear search.
11. **Why `malloc` and `free`?** Nodes are created while the program runs; `evidenceClear()` frees all of them before exit.
12. **How was the "shipping"/"pin" false positive avoided?** `has_word()` checks word boundaries.
13. **Does Safe mean the link is safe?** No, only that no configured rule matched.
14. **Does the app open URLs?** No, URLs are only text.
15. **Do ML models change the score?** No, they are shown for information only.
16. **What do the Accuracy graphs show?** Saved test-set accuracy, precision, recall and F1 of the ML models, their confusion matrices, and CrossPhire's cross-dataset results as a research reference.
17. **Why is CrossPhire's 40% result important?** It shows a model can do very well on its own dataset but poorly on a new one, so our test accuracy is not real-world accuracy.
18. **Why was history/QR/screenshot removed?** To keep the project focused on SMS and URL and easier to explain.
19. **Main limitation?** Fixed keyword rules; new scam wording can be missed and normal messages can be flagged.

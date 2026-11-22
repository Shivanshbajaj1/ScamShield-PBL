# Viva questions

1. **Why C, C++ and Python?** C implements linked lists and stack; C++ implements OOP scanners and risk calculation; Python provides the dashboard, QR/OCR extraction and integration.
2. **How does Python call C/C++?** It runs `scamshield.exe` for scanning/scoring and `scamshield_dsa.exe` for C data-structure operations using `subprocess`.
3. **Why are there two executables?** C and C++ are compiled separately. Python coordinates them using standard input and output, avoiding direct mixed-language linking.
4. **Where is the score calculated?** `cpp/RiskCalculator.cpp`.
5. **What is a linked list here?** Each `HistoryNode` stores one saved scan and points to the next record. New scans use insert-at-beginning; saved records reload with insert-at-end.
6. **Why use a stack?** The newest ID is on top, so Undo removes the latest scan.
7. **What is runtime polymorphism?** `main.cpp` uses a `Scanner*` base pointer for message/URL child scanners.
8. **Does Safe mean a link is safe?** No; it only means configured rules found no strong warning.
9. **Does the app visit URLs?** No. URLs are plain text input.
10. **Do ML probabilities set the score?** No. They are optional display information; C++ calculates the score.
11. **Why is OCR optional?** It needs external Tesseract software.
12. **Why no batch scan?** One explainable scan at a time is the project scope.
13. **Why are there two linked lists?** The history list stores saved scans; the evidence list temporarily stores unique warning findings before risk calculation.
14. **What does `malloc` do?** It allocates memory while the program runs. `free` releases that memory when an evidence or history node is no longer needed.
15. **What is the time complexity of list insertion at the beginning?** O(1), because the new node immediately points to `head`.
16. **What is the time complexity of insert-at-end?** O(n), because the list is traversed to find the last node.
17. **What is the time complexity of history search?** O(n), because each record may need to be checked.
18. **What is the time complexity of stack push and pop?** O(1), because they only change the top node.
19. **Why does Undo use a stack rather than a queue?** Undo must remove the newest scan first, which is LIFO behavior.
20. **Why is no queue used?** The application accepts only one scan at a time. A queue would not improve its actual work.
21. **Why is no BST used?** The project has a small local history; a simple linked-list search is easier to understand and sufficient.
22. **Why is no graph/BFS/DFS used?** Scam inputs do not contain a meaningful network or graph relationship in this offline project.
23. **How are duplicate indicators controlled?** Python sends raw C++ findings to the C evidence executable. `evidenceSearch()` checks the C linked list before `evidenceInsertEnd()` adds a node.
24. **How was the shipping false positive avoided?** C++ uses `has_word`, which checks word boundaries, so `pin` inside `shipping` is not treated as a PIN request.
25. **How is QR content routed?** A decoded full URL goes to URL scanning; normal decoded text goes to message scanning; payment/phone URI values show an unsupported-content message.
26. **How is screenshot content routed?** OCR text goes to message scanning and the first visible URL goes to URL scanning in the same screenshot scan.
27. **What happens if OCR cannot read text?** The app shows an error rather than returning Safe.
28. **Where is persistent history stored?** Locally in `history.txt`, written and reloaded by the DSA history functions.
29. **Why are model charts shown?** They display real saved Phase-II evaluation results from `metrics.json`, clearly separated from the current scan score.
30. **What is the main limitation?** It is an explainable offline rule-based prototype; it cannot visit websites or guarantee that content is harmless or malicious.
31. **Where is linear search used?** `history_search` traverses nodes and matches the scan type, label or reasons.
32. **Why is there an array in the DSA module?** `save_file()` uses an array of node pointers to write the newest-first linked list back to the file in oldest-first order.

33. **Why are DSA files `.c`?** The linked-list and stack implementations are written and compiled as C11 using GCC. Python calls the separate C DSA executable, so the C++ program does not need direct C function declarations or `extern "C"`.
34. **How does the C evidence list work with C++ risk scoring?** C++ prints the detected findings. Python sends them to the C executable. The C linked list removes duplicate finding names and returns unique findings to Python. Python sends those to C++ `RiskCalculator` for the final score.

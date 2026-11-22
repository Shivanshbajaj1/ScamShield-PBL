# Windows setup

1. Install Python 3.10 or later.
2. Install MSYS2 UCRT64 and in its UCRT64 terminal run: `pacman -S --needed mingw-w64-ucrt-x86_64-gcc`.
3. Optional: install Tesseract OCR for screenshot text extraction.
4. Open PowerShell in this project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\build.bat
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m streamlit run app.py
```

`build.bat` builds two separate executables:

- `scamshield_dsa.exe`: compiled by `gcc -std=c11` from `dsa/main.c`, `history_list.c`, `undo_stack.c` and `evidence_list.c`. These are genuine C source files.
- `scamshield.exe`: compiled by `g++ -std=c++17` from the scanner classes and risk calculator.

Python uses `subprocess` to send commands to the appropriate executable. The C and C++ programs communicate through standard input and output, so no `extern`, DLL or `ctypes` setup is required. Both executables must be present before the application can scan or access history. Run `build.bat` again after changing any C or C++ source file.

The combined form accepts any combination of SMS, URL(s), QR image and screenshot. QR decoding needs OpenCV. Screenshot OCR needs Tesseract installed separately. If OCR is unavailable, the app reports it and still analyses other valid inputs in that submission.

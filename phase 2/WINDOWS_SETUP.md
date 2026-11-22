# Windows setup

1. Install Python 3.10 or later.
2. Install MSYS2 UCRT64 and in its UCRT64 terminal run: `pacman -S --needed mingw-w64-ucrt-x86_64-gcc`.
3. In PowerShell, inside the project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\build.bat
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m streamlit run app.py
```

`build.bat` creates two programs:

- `scamshield_dsa.exe` — `gcc -std=c11` from `dsa/main.c` and `dsa/evidence_list.c`.
- `scamshield.exe` — `g++ -std=c++17` from the C++ scanner and risk calculator files.

Run `build.bat` again after changing any `.c` or `.cpp` file. Tesseract and OpenCV are no longer needed.

@echo off
setlocal
set ROOT=%~dp0
set MSYS=C:\msys64\ucrt64\bin
if exist "%MSYS%\gcc.exe" set PATH=%MSYS%;%PATH%

echo Building C DSA executable...
gcc -std=c11 -Wall -Wextra -static -static-libgcc "%ROOT%dsa\main.c" "%ROOT%dsa\evidence_list.c" -I "%ROOT%dsa" -o "%ROOT%scamshield_dsa.exe"
if errorlevel 1 goto failed

echo Building C++ scanning executable...
g++ -std=c++17 -Wall -Wextra -static -static-libgcc -static-libstdc++ "%ROOT%cpp\main.cpp" "%ROOT%cpp\Scanner.cpp" "%ROOT%cpp\RiskCalculator.cpp" -I "%ROOT%cpp" -o "%ROOT%scamshield.exe"
if errorlevel 1 goto failed

echo Build complete: scamshield.exe and scamshield_dsa.exe
exit /b 0

:failed
echo Build failed. Install MSYS2 UCRT64 GCC and G++, then run build.bat again.
exit /b 1

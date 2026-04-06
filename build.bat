@echo off
setlocal

echo ============================================================
echo  kmon build
echo ============================================================

echo.
echo [1/4] Krypton to C (kmon)...
..\krypton\kcc.exe --headers ..\krypton\headers run.k > kmon_tmp.c
if errorlevel 1 (
    echo ERROR: kmon Krypton compilation failed.
    del /Q kmon_tmp.c 2>nul
    exit /b 1
)

echo [2/4] C to exe (kmon.exe)...
gcc kmon_tmp.c -I. -I"C:/npcap-sdk/Include" -L"C:/npcap-sdk/Lib/x64" -o kmon.exe -lwpcap -lws2_32 -lshell32 -lpsapi -lpdh -lm -w
if errorlevel 1 (
    echo ERROR: kmon gcc failed.
    del /Q kmon_tmp.c 2>nul
    exit /b 1
)
del /Q kmon_tmp.c
echo OK: kmon.exe

echo.
echo [3/4] Krypton to C (scanner)...
..\krypton\kcc.exe --headers ..\krypton\headers kmon_scanner.k > scanner_tmp.c
if errorlevel 1 (
    echo ERROR: scanner Krypton compilation failed.
    del /Q scanner_tmp.c 2>nul
    exit /b 1
)

echo [4/4] C to exe (kmon_scanner.exe)...
gcc scanner_tmp.c -I. -o kmon_scanner.exe -lws2_32 -lm -w
if errorlevel 1 (
    echo ERROR: scanner gcc failed.
    del /Q scanner_tmp.c 2>nul
    exit /b 1
)
del /Q scanner_tmp.c
echo OK: kmon_scanner.exe

echo.
echo ============================================================
echo  Done!
echo.
echo  Usage: kmon.exe ^<interface^>
echo.
echo  To list interfaces:
echo    kmon_scanner.exe
echo.
echo  The UI opens automatically in your browser at:
echo    http://127.0.0.1:8080
echo ============================================================

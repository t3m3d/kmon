@echo off
setlocal

echo [1/2] Krypton to C...
..\krypton\kcc.exe --headers ..\krypton\headers run.k > kmon_tmp.c
if errorlevel 1 (
    echo ERROR: Krypton compilation failed.
    del /Q kmon_tmp.c 2>nul
    exit /b 1
)

echo [2/2] C to exe...
gcc kmon_tmp.c -I. -o kmon_backend.exe -lwpcap -lws2_32 -lm -w
if errorlevel 1 (
    echo ERROR: gcc failed.
    del /Q kmon_tmp.c 2>nul
    exit /b 1
)
del /Q kmon_tmp.c

echo Done! Run: kmon_backend.exe ^<interface^>

@echo off
setlocal
set "KICAD_MAJOR=9"
if /I "%~1"=="-v" (
    set "KICAD_MAJOR=%~2"
    shift
    shift
)
REM SHIFT does not change %%*, so forward the remaining arguments explicitly.
py -3 "%~dp0run_kibot.py" --container --major %KICAD_MAJOR% %1 %2 %3 %4 %5 %6 %7 %8 %9
exit /b %errorlevel%

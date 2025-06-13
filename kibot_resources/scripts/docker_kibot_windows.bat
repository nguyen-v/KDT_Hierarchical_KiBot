@echo off
REM Set variables for display and user name
set DISPLAY=host.docker.internal:0.0
set USER_NAME=%USERNAME%

REM Set default image
set "IMAGE=ghcr.io/inti-cmnb/kicad8_auto_full:dev"

REM Check for optional -v flag and version number
if /I "%~1"=="-v" (
    if "%~2"=="9" (
        set "IMAGE=ghcr.io/inti-cmnb/kicad9_auto_full:dev"
    ) else (
        echo Unsupported version: %~2
        goto :eof
    )
)

REM Run the Docker container with mounted volumes
docker run --rm -it ^
    --env NO_AT_BRIDGE=1 ^
    --env DISPLAY=%DISPLAY% ^
    --workdir="/home/%USER_NAME%" ^
    --volume=C:\Users\%USER_NAME%:/home/%USER_NAME%:rw ^
    --volume=/tmp/.X11-unix:/tmp/.X11-unix ^
    --entrypoint /bin/bash ^
    -p 8000:8000 ^
    %IMAGE%

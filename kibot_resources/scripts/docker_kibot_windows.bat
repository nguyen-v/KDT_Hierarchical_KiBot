@echo off
REM Set variables for user ID, group ID, and display
set DISPLAY=host.docker.internal:0.0
set USER_NAME=%USERNAME%

REM Run the Docker container with mounted volumes
docker run --rm -it ^
    --env NO_AT_BRIDGE=1 ^
    --env DISPLAY=%DISPLAY% ^
    --workdir="/home/%USER_NAME%" ^
    --volume=C:\Users\%USER_NAME%:/home/%USER_NAME%:rw ^
    --volume=/tmp/.X11-unix:/tmp/.X11-unix ^
    --entrypoint /bin/bash ^
    ghcr.io/inti-cmnb/kicad8_auto_full:dev

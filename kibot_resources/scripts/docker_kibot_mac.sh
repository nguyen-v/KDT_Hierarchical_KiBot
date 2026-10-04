#!/bin/sh

# Default image version
IMAGE="ghcr.io/inti-cmnb/kicad8_auto_full:dev"

# Parse the optional -v flag
while getopts "v:" opt; do
    case "$opt" in
        v)
            if [ "$OPTARG" = "9" ]; then
                IMAGE="ghcr.io/inti-cmnb/kicad9_auto_full:dev"
            else
                echo "Unsupported version: $OPTARG" >&2
                exit 1
            fi
            ;;
        *)
            echo "Usage: $0 [-v 9]" >&2
            exit 1
            ;;
    esac
done

docker run --rm -it \
    --platform linux/amd64 \
    --hostname "kibot" \
    --name "kibot" \
    --user "$USER_ID:$GROUP_ID" \
    --env NO_AT_BRIDGE=1 \
    --env DISPLAY="$DISPLAY" \
    --workdir "$HOME" \
    --volume "$HOME:$HOME:rw" \
    -p 8000:8000 \
    --entrypoint /bin/bash \
    "$IMAGE"
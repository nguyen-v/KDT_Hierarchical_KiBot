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

export USER_ID=$(id -u)
export GROUP_ID=$(id -g)
export USER_NAME=$(whoami)

docker run --rm -it \
    --user "$USER_ID:$GROUP_ID" \
    --env NO_AT_BRIDGE=1 \
    --env DISPLAY="$DISPLAY" \
    --workdir="/home/$USER_NAME" \
    --volume=/tmp/.X11-unix:/tmp/.X11-unix \
    --volume="/etc/group:/etc/group:ro" \
    --volume="/etc/passwd:/etc/passwd:ro" \
    --volume="/etc/shadow:/etc/shadow:ro" \
    --volume="/home/$USER_NAME:/home/$USER_NAME:rw" \
    -p 8000:8000 \
    --entrypoint /bin/bash \
    "$IMAGE" -c "
    if ! id $USER_NAME &>/dev/null; then
        echo \"Creating user $USER_NAME ($USER_ID:$GROUP_ID)...\"
        useradd -u $USER_ID -g $GROUP_ID -d /home/$USER_NAME -m $USER_NAME
        chown -R $USER_ID:$GROUP_ID /home/$USER_NAME
    fi
    exec su - $USER_NAME"

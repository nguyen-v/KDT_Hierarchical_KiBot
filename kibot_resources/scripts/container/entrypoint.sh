#!/bin/sh
set -eu
for major in 9 10; do
    mkdir -p "$HOME/.cache/kicad/$major.0/embed" "${XDG_CACHE_HOME:-$HOME/.cache}/kicad/$major.0/embed"
done
if [ -d /opt/kicad/share/kicad/template ]; then
    # The base image's older stock table points to packed symbols. 10.0.7's
    # official libraries are unpacked directories; use its matching table.
    version="$(kicad-cli version | cut -d. -f1)"
    config="${KICAD_CONFIG_HOME:-${XDG_CONFIG_HOME:-$HOME/.config}/kicad}/$version.0"
    mkdir -p "$config"
    for table in sym-lib-table fp-lib-table; do
        if [ ! -f "$config/$table" ]; then
            cp "/opt/kicad/share/kicad/template/$table" "$config/$table"
        fi
    done
fi
if [ -z "${DISPLAY:-}" ]; then
    Xvfb :99 -screen 0 2200x2200x24 -ac -nolisten tcp > /tmp/xvfb.log 2>&1 &
    export DISPLAY=:99
    sleep 1
fi
exec "$@"

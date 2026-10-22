#!/usr/bin/env bash
# Run from the PCB project folder. Only this project is mounted into the container.
set -euo pipefail
major=9
if [[ "${1:-}" == -v ]]; then
    major="${2:?Usage: docker_kibot_linux.sh [-v 9|10] [runner options]}"
    shift 2
fi
exec python3 "$(dirname -- "${BASH_SOURCE[0]}")/run_kibot.py" --container --major "$major" "$@"

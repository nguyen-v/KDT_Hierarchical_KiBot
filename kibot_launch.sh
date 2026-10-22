#!/bin/bash

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default options
variant="CHECKED"
revision=""
costs_flag=false
server_flag=false
server_port=8000
pid_file="/tmp/kibot_server.pid"

# Display help
function display_help() {
    echo -e "USAGE"
    echo -e "  ./kibot_launch.sh [OPTIONS]"
    echo
    echo -e "OPTIONS"
    echo -e "  -v, --variant VARIANT       Specify a variant name. Supported variants:"
    echo -e "                              RELEASED, DRAFT, PRELIMINARY, CHECKED, or others."
    echo -e "  --version VERSION           Specify a version to use in the command."
    echo -e "  --costs                     Replace draft_group or all_group with xlsx_bom, and enforce specific skip-pre options."
    echo -e "  --server [PORT]             Start an HTTP server on the specified port (default: 8000)."
    echo -e "  --stop-server               Stop the running HTTP server."
    echo -e "  -h, --help                  Display this help message."
    echo
    echo -e "EXAMPLES"
    echo -e "  ./kibot_launch.sh                        Run with default options."
    echo -e "  ./kibot_launch.sh -v RELEASED            Run with RELEASED variant."
    echo -e "  ./kibot_launch.sh --costs                Compute XLSX costs spreadsheet. Results in Manufacturing/Assembly folder"
    echo -e "  ./kibot_launch.sh -v DRAFT               Run with DRAFT variant."
    echo -e "  ./kibot_launch.sh -v PRELIMINARY         Run with PRELIMINARY variant."
    echo -e "  ./kibot_launch.sh -v CUSTOM_VARIANT      Run with a custom variant, saved in the Variants folder."
    echo -e "  ./kibot_launch.sh --server               Start an HTTP server on port 8000."
    echo -e "  ./kibot_launch.sh --server 8080          Start an HTTP server on port 8080."
    echo -e "  ./kibot_launch.sh --stop-server          Stop the running HTTP server."
    echo
    echo -e "VARIANT DESCRIPTIONS"
    echo -e "  DRAFT: only schematic in progress, will only generate schematic PDF, netlist and BoM"
    echo -e "  PRELIMINARY: will generate both schematic and PCB documents, but no ERC/DRC"
    echo -e "  CHECKED: will generate both schematic and PCB documents, with ERC/DRC"
    echo -e "  RELEASED: similar to CHECKED but should only be used for releases"
    echo -e "  Other variants: will be saved in the Variants folder"
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --variant|-v)
            if [[ -n $2 && $2 != -* ]]; then
                variant="$2"
                shift
            else
                echo -e "${YELLOW}Warning: --variant|-v requires a value.${NC}"
                exit 1
            fi
            ;;
        --version)
            if [[ -n $2 && $2 != -* ]]; then
                revision="$2"
                shift
            else
                echo -e "${YELLOW}Warning: --version requires a value.${NC}"
                exit 1
            fi
            ;;
        --costs)
            costs_flag=true
            ;;
        --server)
            server_flag=true
            if [[ -n $2 && $2 != -* ]]; then
                server_port="$2"
                shift
            fi
            if [[ -f $pid_file ]]; then
                pid=$(cat $pid_file)
                if kill -0 $pid 2>/dev/null; then
                    echo -e "${YELLOW}A server is already running on PID $pid. Please stop it first with --stop-server.${NC}"
                    exit 1
                else
                    echo -e "${YELLOW}Stale PID file detected. Removing it.${NC}"
                    rm -f $pid_file
                fi
            fi
            ;;
        --stop-server)
            if [[ -f $pid_file ]]; then
                pid=$(cat $pid_file)
                if kill -0 $pid 2>/dev/null; then
                    echo -e "${GREEN}Stopping HTTP server with PID $pid...${NC}"
                    kill $pid
                    rm -f $pid_file
                    echo -e "${GREEN}Server stopped.${NC}"
                    exit 0
                else
                    echo -e "${YELLOW}No running server found. Removing stale PID file.${NC}"
                    rm -f $pid_file
                    exit 1
                fi
            else
                echo -e "${YELLOW}No server is running.${NC}"
                exit 1
            fi
            ;;
        -h|--help)
            display_help
            ;;
        *)
            echo -e "${YELLOW}Warning: Unrecognized argument: $1${NC}"
            display_help
            ;;
    esac
    shift
done

# Server controls above remain available; generation uses the shared argument-safe runner.
if [[ "$server_flag" == true ]]; then
    python3 -m http.server "$server_port" &
    echo $! > "$pid_file"
    exit 0
fi
runner_args=(--variant "$variant")
[[ -z "$revision" ]] || runner_args+=(--version "$revision")
[[ "$costs_flag" == false ]] || runner_args+=(--costs)
exec python3 "$(dirname -- "${BASH_SOURCE[0]}")/kibot_resources/scripts/run_kibot.py" "${runner_args[@]}"

#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
FW_DIR="${PROJECT_ROOT}/firmware/esp32_ptt_streamer"
BUILD_DIR="${FW_DIR}/build"

BOOT_BIN="${BUILD_DIR}/bootloader/bootloader.bin"
PART_BIN="${BUILD_DIR}/partition_table/partition-table.bin"
APP_BIN="${BUILD_DIR}/esp32_ptt_streamer.bin"

usage() {
    cat <<'EOF'
Usage:
  flash_esp32.sh --prebuilt [PORT] [--yes]
  flash_esp32.sh --idf [PORT] [--yes]

Options:
  --prebuilt [PORT]   Flash pre-built ESP-IDF binaries at 460800 baud.
                      Auto-detects /dev/ttyUSB* or /dev/ttyACM* if PORT is omitted.
  --idf [PORT]        Run idf.py -p PORT build flash monitor in firmware/esp32_ptt_streamer.
  --yes, -y           Acknowledge J1 disconnection safety check non-interactively.
  --help, -h          Show this help message.
EOF
}

detect_port() {
    local found=""
    local count=0
    local dev
    for dev in /dev/ttyUSB* /dev/ttyACM*; do
        if [ -e "${dev}" ]; then
            found="${dev}"
            count=$((count + 1))
        fi
    done
    if [ "${count}" -eq 0 ]; then
        echo "ERROR: No serial port found at /dev/ttyUSB* or /dev/ttyACM*. Pass PORT explicitly." >&2
        return 1
    fi
    if [ "${count}" -gt 1 ]; then
        echo "ERROR: Multiple serial ports found. Pass PORT explicitly." >&2
        return 1
    fi
    printf '%s\n' "${found}"
}

confirm_j1_disconnected() {
    echo "SAFETY CHECK: Confirm J1 electrode cable is DISCONNECTED and NO HUMAN CONNECTION exists before USB connection."
    if [ "${AUTO_YES}" -eq 1 ]; then
        echo "SAFETY CHECK CONFIRMED (--yes): J1 electrode cable disconnected."
        return 0
    fi
    if [ -t 0 ]; then
        printf "Confirm J1 electrode cable is disconnected [y/N]: "
        read -r reply
        case "${reply}" in
            y|Y|yes|YES)
                return 0
                ;;
            *)
                echo "Aborted: confirm J1 electrode cable disconnection before flashing." >&2
                return 1
                ;;
        esac
    fi
    echo "SAFETY CHECK NOTICE: non-interactive mode; ensure J1 electrode cable is disconnected."
}

resolve_esptool() {
    if command -v esptool.py >/dev/null 2>&1; then
        ESPTOOL_CMD=("esptool.py")
        return 0
    fi
    if command -v esptool >/dev/null 2>&1; then
        ESPTOOL_CMD=("esptool")
        return 0
    fi
    if command -v python3 >/dev/null 2>&1 && python3 -c "import esptool" >/dev/null 2>&1; then
        ESPTOOL_CMD=("python3" "-m" "esptool")
        return 0
    fi
    return 1
}

MODE=""
PORT=""
AUTO_YES=0

while [ -n "${1+x}" ]; do
    case "$1" in
        --prebuilt)
            if [ -n "${MODE}" ]; then
                echo "ERROR: Specify only one of --prebuilt or --idf." >&2
                exit 2
            fi
            MODE="prebuilt"
            if [ -n "${2+x}" ]; then
                case "$2" in
                    -*) ;;
                    *)
                        PORT="$2"
                        shift
                        ;;
                esac
            fi
            ;;
        --idf)
            if [ -n "${MODE}" ]; then
                echo "ERROR: Specify only one of --prebuilt or --idf." >&2
                exit 2
            fi
            MODE="idf"
            if [ -n "${2+x}" ]; then
                case "$2" in
                    -*) ;;
                    *)
                        PORT="$2"
                        shift
                        ;;
                esac
            fi
            ;;
        --yes|-y)
            AUTO_YES=1
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo "ERROR: Unknown argument: $1" >&2
            usage >&2
            exit 2
            ;;
    esac
    shift
done

if [ -z "${MODE}" ]; then
    usage >&2
    exit 2
fi

if [ -z "${PORT}" ]; then
    PORT="$(detect_port)"
fi

if [ "${MODE}" = "prebuilt" ]; then
    for bin_file in "${BOOT_BIN}" "${PART_BIN}" "${APP_BIN}"; do
        if [ ! -f "${bin_file}" ]; then
            echo "ERROR: Missing firmware binary: ${bin_file}" >&2
            exit 1
        fi
    done
    if ! resolve_esptool; then
        echo "ERROR: Neither esptool.py nor 'python3 -m esptool' was found. Install esptool or source ESP-IDF export.sh." >&2
        exit 1
    fi
    confirm_j1_disconnected
    exec "${ESPTOOL_CMD[@]}" \
        --chip esp32 \
        --port "${PORT}" \
        --baud 460800 \
        --before default_reset \
        --after hard_reset \
        write_flash -z \
        --flash_mode dio \
        --flash_freq 40m \
        --flash_size 2MB \
        0x1000 "${BOOT_BIN}" \
        0x8000 "${PART_BIN}" \
        0x10000 "${APP_BIN}"
fi

if [ "${MODE}" = "idf" ]; then
    if ! command -v idf.py >/dev/null 2>&1; then
        echo "ERROR: idf.py not found. Source your ESP-IDF export.sh environment first." >&2
        exit 1
    fi
    confirm_j1_disconnected
    cd "${FW_DIR}"
    exec idf.py -p "${PORT}" build flash monitor
fi

#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(pwd)
GATEWAY_DIR="${ROOT_DIR}/gateway"
ZIP_URL="https://download2.interactivebrokers.com/portal/clientportal.gw.zip"
ZIP_FILE="${GATEWAY_DIR}/clientportal.gw.zip"

usage() {
  cat <<USAGE
Usage: ${0##*/} <command>

Commands:
  download   Download and extract the Client Portal Gateway
  run        Ensure the gateway is installed and start it with conf.yaml
  clean      Remove the downloaded gateway files
USAGE
}

download_gateway() {
  mkdir -p "${GATEWAY_DIR}"

  if [ ! -f "${ZIP_FILE}" ]; then
    echo "Downloading Client Portal Gateway…"
    curl -# -L "${ZIP_URL}" -o "${ZIP_FILE}"
  else
    echo "Using cached gateway archive at ${ZIP_FILE}"
  fi

  if [ ! -d "${GATEWAY_DIR}/bin" ]; then
    echo "Extracting gateway archive…"
    unzip -q -o "${ZIP_FILE}" -d "${GATEWAY_DIR}"
  fi

  if [ -f "${ROOT_DIR}/conf.yaml" ]; then
    mkdir -p "${GATEWAY_DIR}/root"
    cp "${ROOT_DIR}/conf.yaml" "${GATEWAY_DIR}/root/conf.yaml"
  fi

  echo "Gateway ready in ${GATEWAY_DIR}"
}

run_gateway() {
  download_gateway
  echo "Starting Client Portal Gateway…"
  echo "Press Ctrl+C to stop."
  (cd "${GATEWAY_DIR}" && sh bin/run.sh root/conf.yaml)
}

clean_gateway() {
  if [ -d "${GATEWAY_DIR}" ]; then
    rm -rf "${GATEWAY_DIR}"
    echo "Removed ${GATEWAY_DIR}"
  else
    echo "Gateway directory not found; nothing to clean."
  fi
}

command=${1:-run}
case "${command}" in
  download)
    download_gateway
    ;;
  run)
    run_gateway
    ;;
  clean)
    clean_gateway
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    echo "Unknown command: ${command}" >&2
    usage
    exit 1
    ;;
esac

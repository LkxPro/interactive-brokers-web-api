#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(cd "$(dirname "$0")" && pwd)
GATEWAY_DIR="${ROOT_DIR}/gateway"
VENV_DIR="${ROOT_DIR}/.venv"

if [ -d "${GATEWAY_DIR}" ]; then
  (cd "${GATEWAY_DIR}" && sh bin/run.sh root/conf.yaml &)
  GATEWAY_PID=$!
  trap 'kill ${GATEWAY_PID} >/dev/null 2>&1 || true' EXIT
fi

if [ ! -d "${VENV_DIR}" ]; then
  uv venv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
. "${VENV_DIR}/bin/activate"
uv pip install -e "${ROOT_DIR}"

export FLASK_APP="ibkr_web.app:create_app"
flask run --debug -p 5056 -h 0.0.0.0

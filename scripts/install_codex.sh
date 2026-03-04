#!/usr/bin/env bash
set -euo pipefail

# Install local Codex runtime for webnovel-writer.
# - Creates a dedicated virtualenv and installs dependencies
# - Links runtime to ~/.codex/webnovel-writer/runtime
# - Creates ~/.local/bin/webnovel launcher

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SOURCE_RUNTIME_DIR="${REPO_ROOT}/webnovel-writer"

RUNTIME_ROOT_DEFAULT="${HOME}/.codex/webnovel-writer/runtime"
RUNTIME_ROOT="${WEBNOVEL_RUNTIME_ROOT:-${RUNTIME_ROOT_DEFAULT}}"
VENV_DIR="${HOME}/.codex/webnovel-writer/venv"
VENV_PYTHON="${VENV_DIR}/bin/python"
BIN_DIR="${HOME}/.local/bin"
LAUNCHER_PATH="${BIN_DIR}/webnovel"

if [ ! -d "${SOURCE_RUNTIME_DIR}" ]; then
  echo "ERROR: missing runtime source directory: ${SOURCE_RUNTIME_DIR}" >&2
  exit 1
fi

echo "[1/5] Prepare virtual environment"
if [ ! -x "${VENV_PYTHON}" ]; then
  python3 -m venv "${VENV_DIR}"
fi

echo "[2/5] Install Python dependencies"
"${VENV_PYTHON}" -m pip install --upgrade pip
"${VENV_PYTHON}" -m pip install -r "${REPO_ROOT}/requirements.txt"

echo "[3/5] Prepare runtime link"
mkdir -p "$(dirname "${RUNTIME_ROOT}")"
if [ -e "${RUNTIME_ROOT}" ] && [ ! -L "${RUNTIME_ROOT}" ]; then
  echo "ERROR: runtime path exists and is not a symlink: ${RUNTIME_ROOT}" >&2
  echo "Please move it or set WEBNOVEL_RUNTIME_ROOT to another path." >&2
  exit 1
fi
ln -sfn "${SOURCE_RUNTIME_DIR}" "${RUNTIME_ROOT}"

echo "[4/5] Create launcher at ${LAUNCHER_PATH}"
mkdir -p "${BIN_DIR}"
cat > "${LAUNCHER_PATH}" <<LAUNCHER
#!/usr/bin/env bash
set -euo pipefail

WEBNOVEL_VENV_PYTHON="\${WEBNOVEL_VENV_PYTHON:-${VENV_PYTHON}}"
WEBNOVEL_RUNTIME_ROOT="\${WEBNOVEL_RUNTIME_ROOT:-${RUNTIME_ROOT}}"
if [ ! -x "\${WEBNOVEL_VENV_PYTHON}" ]; then
  WEBNOVEL_VENV_PYTHON="python3"
fi
exec "\${WEBNOVEL_VENV_PYTHON}" "\${WEBNOVEL_RUNTIME_ROOT}/scripts/webnovel.py" "\$@"
LAUNCHER
chmod +x "${LAUNCHER_PATH}"

echo "[5/5] Done"
echo
echo "Runtime root : ${RUNTIME_ROOT}"
echo "Venv python  : ${VENV_PYTHON}"
echo "Launcher     : ${LAUNCHER_PATH}"
echo ""
echo "If 'webnovel' is not found, add this to your shell profile:"
echo "  export PATH=\"${BIN_DIR}:\$PATH\""

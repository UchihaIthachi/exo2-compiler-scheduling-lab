#!/usr/bin/env bash
set -euo pipefail

# Usage: ./generate_targets.sh /path/to/your/cloned/exo
# Produces ./target/quiz{1,2,3}/ with generated C/H from exocc.

EXO_REPO="${1:-}"
if [[ -z "${EXO_REPO}" ]]; then
  echo "ERROR: Provide path to your cloned exo repo, e.g. ./generate_targets.sh ~/exo"
  exit 1
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${ROOT}/target"
mkdir -p "${TARGET_DIR}"

echo "[1/3] Copying solutions into your exo repo..."
cp -f "${ROOT}/solutions/quiz1_solution.py" "${EXO_REPO}/examples/quiz1/quiz1_solution.py"
cp -f "${ROOT}/solutions/quiz2_solution.py" "${EXO_REPO}/examples/quiz2/quiz2_solution.py"
cp -f "${ROOT}/solutions/quiz3_solution.py" "${EXO_REPO}/examples/quiz3/quiz3_solution.py"

echo "[2/3] Generating target C/H with exocc..."
pushd "${EXO_REPO}/examples/quiz1" >/dev/null
exocc quiz1_solution.py -o "${TARGET_DIR}/quiz1"
popd >/dev/null

pushd "${EXO_REPO}/examples/quiz2" >/dev/null
exocc quiz2_solution.py -o "${TARGET_DIR}/quiz2"
popd >/dev/null

pushd "${EXO_REPO}/examples/quiz3" >/dev/null
exocc quiz3_solution.py -o "${TARGET_DIR}/quiz3"
popd >/dev/null

echo "[3/3] Done. Targets are in: ${TARGET_DIR}/quiz{1,2,3}/"

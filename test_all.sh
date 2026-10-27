#!/usr/bin/env bash
set -e

PYTHON_VERSIONS=("3.10" "3.11" "3.12" "3.13")

echo "========================================================"
echo " Running tests across Python versions with uv"
echo " Versions: ${PYTHON_VERSIONS[*]}"
echo "========================================================"

for ver in "${PYTHON_VERSIONS[@]}"; do
  echo ""
  echo ">>> [Python $ver] Installing / syncing dependencies & running pytest..."
  uv run --python "$ver" pytest tests/
done

echo ""
echo "========================================================"
echo " All tests passed successfully across all Python versions!"
echo "========================================================"

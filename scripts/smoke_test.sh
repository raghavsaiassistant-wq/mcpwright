#!/usr/bin/env bash
# smoke_test.sh — bash version of the smoke test
# Usage: bash scripts/smoke_test.sh

set -e

echo "============================================================"
echo "mcpwright smoke test (bash)"
echo "============================================================"

# 1. Python
echo
echo "[1] Python"
PY_VERSION=$(python3 --version 2>&1 || python --version 2>&1)
echo "  ✓ $PY_VERSION"

# 2. npx
echo
echo "[2] npx"
if command -v npx &> /dev/null; then
    NPX_VERSION=$(npx --version 2>&1)
    echo "  ✓ npx found: $NPX_VERSION"
elif command -v npx.cmd &> /dev/null; then
    NPX_VERSION=$(npx.cmd --version 2>&1)
    echo "  ✓ npx.cmd found: $NPX_VERSION"
else
    echo "  ✗ npx not found. Install Node.js from https://nodejs.org/"
    exit 1
fi

# 3. Browser
echo
echo "[3] Browser"
if [[ "$OSTYPE" == "darwin"* ]]; then
    if [[ -d "/Applications/Google Chrome.app" ]]; then
        echo "  ✓ Chrome installed (macOS)"
    else
        echo "  ✗ Chrome not found at /Applications/Google Chrome.app"
        exit 1
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if command -v google-chrome &> /dev/null || command -v chromium &> /dev/null; then
        echo "  ✓ Chrome/Chromium installed (Linux)"
    else
        echo "  ✗ Chrome/Chromium not found. Install with:"
        echo "    sudo apt install -y google-chrome-stable"
        exit 1
    fi
fi

# 4. mcpwright import
echo
echo "[4] mcpwright import"
if python3 -c "import sys; sys.path.insert(0, '$(dirname $0)/..'); from core.session import browser_session; print('  ✓ mcpwright.session importable')" 2>&1; then
    :
else
    echo "  ✗ mcpwright.session not importable. Did you run 'pip install -e .'?"
    exit 1
fi

echo
echo "============================================================"
echo "✓ All checks passed."
echo "  Next: edit examples/01_basic_navigate.py and run it."
echo "============================================================"

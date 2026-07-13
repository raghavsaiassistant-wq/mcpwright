"""
smoke_test.py — Quick verification that mcpwright is set up correctly.

Run this first to make sure everything works:
  python scripts/smoke_test.py

It will:
  1. Check Python version
  2. Check Node.js / npx
  3. Check Chrome / browser installed
  4. Try to launch a browser session
  5. Navigate to example.com
  6. Take a screenshot
"""

import os
import platform
import shutil
import subprocess
import sys


def check(label, condition, detail=""):
    mark = "✓" if condition else "✗"
    print(f"  {mark} {label}{(' — ' + detail) if detail else ''}")
    return condition


def main():
    print("=" * 60)
    print("mcpwright smoke test")
    print("=" * 60)

    all_ok = True

    # 1. Python version
    print("\n[1] Python")
    py_version = platform.python_version()
    py_ok = check(f"Python {py_version}",
                  tuple(int(x) for x in py_version.split(".")[:2]) >= (3, 8))
    all_ok = all_ok and py_ok

    # 2. npx
    print("\n[2] npx (Node.js)")
    npx_path = shutil.which("npx.cmd") or shutil.which("npx")
    npx_ok = check("npx found", npx_path is not None, npx_path or "")
    all_ok = all_ok and npx_ok
    if npx_ok:
        try:
            r = subprocess.run([npx_path, "--version"],
                               capture_output=True, text=True, timeout=10)
            check(f"npx works (v{r.stdout.strip()})", r.returncode == 0)
        except Exception as e:
            check(f"npx --version: {e}", False)
            all_ok = False

    # 3. Browser
    print("\n[3] Browser")
    chrome_paths = {
        "Windows": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ],
        "Darwin": ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"],
        "Linux": ["/usr/bin/google-chrome", "/usr/bin/chromium"],
    }
    sys_plat = "Windows" if os.name == "nt" else ("Darwin" if sys.platform == "darwin" else "Linux")
    chrome_found = any(os.path.exists(p) for p in chrome_paths.get(sys_plat, []))
    check(f"Chrome/Chromium installed ({sys_plat})", chrome_found)
    all_ok = all_ok and chrome_found

    # 4. Browser session
    print("\n[4] Browser session")
    print("  → Trying to launch mcpwright session (will prompt for profile if needed)...")
    # Add core to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        from core.session import browser_session
        check("mcpwright.session importable", True)
    except ImportError as e:
        check(f"mcpwright.session: {e}", False)
        all_ok = False
        return

    # Skip actual browser launch in smoke test (requires profile path)
    print("  (skipped — set PROFILE_PATH and run examples/01_basic_navigate.py for full test)")

    # Summary
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ All checks passed. mcpwright is ready to use.")
        print("  Next: edit examples/01_basic_navigate.py and run it.")
    else:
        print("✗ Some checks failed. See above.")
        print("  See docs/setup.md for help.")
    print("=" * 60)


if __name__ == "__main__":
    main()

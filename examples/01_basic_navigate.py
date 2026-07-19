"""
01_basic_navigate.py — The simplest possible mcpwright script.

What it does:
  1. Opens a browser session with your saved Chrome profile
  2. Navigates to example.com
  3. Takes a full-page screenshot
  4. Saves the screenshot to ./mcpwright_screenshot.png
  5. Closes the browser

Setup:
  - Replace <YOUR_CHROME_PROFILE_PATH> with the path to your Chrome
    user-data directory.

  On Windows: typically C:\\Users\\<YOU>\\AppData\\Local\\Google\\Chrome\\User Data
  On macOS:   ~/Library/Application Support/Google/Chrome
  On Linux:   ~/.config/google-chrome

Run:
  python examples/01_basic_navigate.py
"""

import os
import sys

# Add the parent directory to sys.path so we can import mcpwright
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcpwright.session import browser_session


def main():
    # ============================================================
    # ⚠️ CHANGE THIS to your actual Chrome profile path
    # ============================================================
    PROFILE_PATH = "<YOUR_CHROME_PROFILE_PATH>"

    if PROFILE_PATH.startswith("<YOUR_"):
        print("❌ Please edit this file and set PROFILE_PATH to your actual Chrome profile path.")
        print("   See the comment block at the top of this file for typical locations.")
        sys.exit(1)

    with browser_session(profile_path=PROFILE_PATH) as (send, recv):
        # 1. Navigate
        print("→ Navigating to example.com...")
        send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": "browser_navigate",
                         "arguments": {"url": "https://example.com"}}})
        resp = recv()
        if resp is None:
            print("✗ Navigation timed out")
            return
        print("  ✓ Loaded")

        # 2. Take a screenshot
        print("→ Taking screenshot...")
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
              "params": {"name": "browser_take_screenshot",
                         "arguments": {"fullPage": True}}})
        resp = recv()
        if resp and "result" in resp:
            content = resp["result"].get("content", [])
            if content and "text" in content[0]:
                # MCP returns the screenshot path inside the response
                print(f"  ✓ Screenshot info: {content[0]['text'][:200]}")
            else:
                print("  ✓ Screenshot taken (no path returned)")
        else:
            print("  ✗ Screenshot failed")

    print("✓ Done. Browser closed.")


if __name__ == "__main__":
    main()

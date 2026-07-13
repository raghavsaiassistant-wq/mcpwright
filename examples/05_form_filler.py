"""
05_form_filler.py — Fill a generic form on any site.

What it does:
  1. Opens a form URL
  2. Reads field definitions from a JSON config
  3. For each field: focus, react_aware_type
  4. Submit

The `fields.json` schema:
  [
    {"selector": "input#name",     "value": "Your Name"},
    {"selector": "input#email",    "value": "you@example.com"},
    {"selector": "textarea#msg",   "value": "Hello!"}
  ]

Run:
  python examples/05_form_filler.py
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.session import browser_session
from core.resilience import smart_wait, react_aware_type


def main():
    PROFILE_PATH = "<YOUR_CHROME_PROFILE_PATH>"
    FORM_URL = "<URL_OF_FORM_PAGE>"
    FIELDS_FILE = "form_fields.json"
    SUBMIT_SELECTOR = "button[type='submit']"

    if any(s.startswith("<YOUR_") or s.startswith("<URL_")
           for s in [PROFILE_PATH, FORM_URL]):
        print("❌ Please edit PROFILE_PATH, FORM_URL, and create form_fields.json.")
        sys.exit(1)

    if not os.path.exists(FIELDS_FILE):
        print(f"❌ {FIELDS_FILE} not found.")
        print("   Create it with the field schema shown at the top of this file.")
        sys.exit(1)

    with open(FIELDS_FILE, "r", encoding="utf-8") as f:
        fields = json.load(f)

    with browser_session(profile_path=PROFILE_PATH) as (send, recv):
        print(f"→ Opening {FORM_URL}...")
        send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": "browser_navigate",
                         "arguments": {"url": FORM_URL}}})
        recv()

        # Fill each field
        for i, field in enumerate(fields, start=1):
            selector = field["selector"]
            value = field["value"]
            print(f"→ Filling field {i}: {selector} = {value[:30]}...")

            # Wait for the field to be present
            if not smart_wait(send, recv, "selector_present",
                              selector=selector, timeout=10):
                print(f"  ✗ Selector not found: {selector}")
                continue

            # Click to focus
            send({"jsonrpc": "2.0", "id": 10 + i, "method": "tools/call",
                  "params": {"name": "browser_click",
                             "arguments": {"element": f"Field {selector}",
                                           "ref": selector}}})
            recv(5)

            # Clear the field (select-all + delete)
            send({"jsonrpc": "2.0", "id": 20 + i, "method": "tools/call",
                  "params": {"name": "browser_evaluate",
                             "arguments": {
                                 "function": f"() => {{ const el = document.querySelector('{selector}'); if (el) {{ el.value = ''; el.dispatchEvent(new Event('input', {{bubbles: true}})); }} return true; }}"
                             }}})
            recv(3)

            # Type the value (React-aware)
            react_aware_type(send, recv, selector, value, char_delay_ms=20)
            print(f"  ✓ Filled")

        # Submit
        print("→ Submitting...")
        if smart_wait(send, recv, "selector_present",
                      selector=SUBMIT_SELECTOR, timeout=5):
            send({"jsonrpc": "2.0", "id": 99, "method": "tools/call",
                  "params": {"name": "browser_click",
                             "arguments": {"element": "Submit",
                                           "ref": SUBMIT_SELECTOR}}})
            recv(15)
            print("✓ Form submitted")
        else:
            print("  ✗ Submit button not found")


if __name__ == "__main__":
    main()

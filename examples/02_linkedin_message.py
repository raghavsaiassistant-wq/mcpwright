"""
02_linkedin_message.py — Send a LinkedIn message to a specific contact.

This is a PATTERN. It shows how to:
  - Open LinkedIn with your saved profile (you stay logged in)
  - Navigate to a person's profile
  - Click the Message button
  - Type a message using react_aware_type (so LinkedIn's React state syncs)
  - Click Send

⚠️ Read before running:
  - REPLACE <YOUR_CHROME_PROFILE_PATH> with your Chrome profile
  - REPLACE <RECIPIENT_LINKEDIN_URL> with the actual URL
  - REPLACE the MESSAGE text
  - Test with someone you know first (a colleague or friend)
  - LinkedIn has aggressive rate limiting. Do NOT send bulk messages.

Run:
  python examples/02_linkedin_message.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcpwright.session import browser_session
from mcpwright.resilience import smart_wait, react_aware_type


def main():
    PROFILE_PATH = "<YOUR_CHROME_PROFILE_PATH>"
    RECIPIENT_URL = "<RECIPIENT_LINKEDIN_URL>"  # e.g. https://www.linkedin.com/in/john-doe/
    MESSAGE = (
        "Hi! Just wanted to say hi and see how you're doing. "
        "Saw your recent post and it reminded me of our work together."
    )

    if any(s.startswith("<YOUR_") or s.startswith("<RECIPIENT")
           for s in [PROFILE_PATH, RECIPIENT_URL]):
        print("❌ Please edit the file and fill in PROFILE_PATH, RECIPIENT_URL, and MESSAGE.")
        sys.exit(1)

    with browser_session(profile_path=PROFILE_PATH) as (send, recv):
        # 1. Go to the recipient's profile
        print(f"→ Opening {RECIPIENT_URL}...")
        send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": "browser_navigate",
                         "arguments": {"url": RECIPIENT_URL}}})
        recv()

        # 2. Wait for the Message button to actually appear
        print("→ Waiting for Message button...")
        if not smart_wait(send, recv, "selector_present",
                          selector="button[aria-label*='Message']", timeout=15):
            print("  ✗ Message button never appeared.")
            return
        print("  ✓ Found")

        # 3. Click Message
        print("→ Clicking Message button...")
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
              "params": {"name": "browser_click",
                         "arguments": {"element": "Message button",
                                       "ref": "button[aria-label*='Message']"}}})
        recv(10)

        # 4. Wait for the message textbox
        print("→ Waiting for message textbox...")
        if not smart_wait(send, recv, "selector_present",
                          selector="div[role='textbox']", timeout=10):
            print("  ✗ Textbox never appeared.")
            return

        # 5. Type the message using react_aware_type
        #    (regular JS .value assignment wouldn't update LinkedIn's React state)
        print("→ Typing message...")
        send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
              "params": {"name": "browser_type",
                         "arguments": {
                             "selector": "div[role='textbox']",
                             "text": MESSAGE,
                             "delay": 25,  # ms between keystrokes
                         }}})
        recv(20)

        # 6. Wait for the Send button to become enabled
        #    (LinkedIn's Send button is disabled until the message has text
        #    in React's state — if you set the value via JS, it stays disabled)
        print("→ Waiting for Send button...")
        if not smart_wait(send, recv,
                          condition="selector_present",
                          selector="button[type='submit']:not([disabled])",
                          timeout=10):
            print("  ✗ Send button never enabled — message may not be in state.")
            print("    This is a common React issue. See docs/pitfalls.md")
            return

        # 7. Click Send
        print("→ Clicking Send...")
        send({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
              "params": {"name": "browser_click",
                         "arguments": {"element": "Send button",
                                       "ref": "button[type='submit']"}}})
        recv(10)

        print("✓ Message sent!")


if __name__ == "__main__":
    main()

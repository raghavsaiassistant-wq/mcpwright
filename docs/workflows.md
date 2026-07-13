# mcpwright — Workflows

Reusable patterns for common AI agent browser tasks.

## Pattern 1: Send a personalized message

```python
from mcpwright import browser_session, smart_wait, react_aware_type

def send_message(profile_path, recipient_url, message):
    with browser_session(profile_path=profile_path) as (send, recv):
        send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": "browser_navigate",
                         "arguments": {"url": recipient_url}}})
        recv()

        # Wait for the message button (NOT a fixed sleep)
        if not smart_wait(send, recv, "selector_present",
                          selector="button[aria-label*='Message']", timeout=15):
            return False, "Message button not found"

        send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
              "params": {"name": "browser_click",
                         "arguments": {"element": "Message", "ref": "button[aria-label*='Message']"}}})
        recv(10)

        if not smart_wait(send, recv, "selector_present",
                          selector="div[role='textbox']", timeout=10):
            return False, "Textbox not found"

        # CRITICAL: react_aware_type — JS .value would skip React's state
        react_aware_type(send, recv, "div[role='textbox']", message, char_delay_ms=30)

        # Wait for Send to enable (only after React state syncs)
        if not smart_wait(send, recv,
                          condition="selector_present",
                          selector="button[type='submit']:not([disabled])",
                          timeout=10):
            return False, "Send button never enabled"

        send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
              "params": {"name": "browser_click",
                         "arguments": {"element": "Send", "ref": "button[type='submit']"}}})
        recv(10)
        return True, "Sent"
```

## Pattern 2: Search and apply

```python
def search_and_apply(profile_path, search_url, max_apps=5):
    with browser_session(profile_path=profile_path) as (send, recv):
        send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": "browser_navigate",
                         "arguments": {"url": search_url}}})
        recv()

        # ⬇ adapt selector to the site
        CARD = ".job-card"
        if not smart_wait(send, recv, "selector_present",
                          selector=CARD, timeout=20):
            return []

        applied = []
        for i in range(max_apps):
            import time; time.sleep(3)  # pace

            # Click N-th card
            send({"jsonrpc": "2.0", "id": 10 + i, "method": "tools/call",
                  "params": {"name": "browser_evaluate",
                             "arguments": {
                                 "function": f"() => {{ const c = document.querySelectorAll('{CARD}')[{i}]; if (c) {{ c.click(); return true; }} return false; }}"
                             }}})
            recv(5)
            time.sleep(2)

            # Click Apply
            send({"jsonrpc": "2.0", "id": 20 + i, "method": "tools/call",
                  "params": {"name": "browser_click",
                             "arguments": {"element": "Apply",
                                           "ref": "button:has-text('Apply')"}}})
            recv(10)

            applied.append({"index": i, "status": "applied"})

            # Back to search
            send({"jsonrpc": "2.0", "id": 30 + i, "method": "tools/call",
                  "params": {"name": "browser_navigate_back",
                             "arguments": {}}})
            recv(5)
            smart_wait(send, recv, "selector_present",
                       selector=CARD, timeout=10)

        return applied
```

## Pattern 3: Extract structured data

```python
def extract_jobs(profile_path, search_url):
    with browser_session(profile_path=profile_path) as (send, recv):
        send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": "browser_navigate",
                         "arguments": {"url": search_url}}})
        recv()

        if not smart_wait(send, recv, "selector_present",
                          selector=".job-card", timeout=20):
            return []

        # Pure JS extraction — runs in the page, returns JSON string
        extract_js = """
        () => {
            const cards = document.querySelectorAll('.job-card');
            return JSON.stringify([...cards].map(c => ({
                title:    c.querySelector('.title')?.innerText,
                company:  c.querySelector('.company')?.innerText,
                location: c.querySelector('.location')?.innerText,
                link:     c.querySelector('a')?.href,
            })));
        }
        """
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
              "params": {"name": "browser_evaluate",
                         "arguments": {"function": extract_js}}})
        resp = recv(15)
        if not resp or "result" not in resp:
            return []
        import json
        text = resp["result"]["content"][0]["text"]
        return json.loads(text)
```

## Pattern 4: Handle login

```python
def login_and_browse(profile_path, login_url, username, password, target_url):
    """
    Use your saved profile for sites where you're already logged in.
    Only call this for sites that need fresh login.
    """
    with browser_session(profile_path=profile_path) as (send, recv):
        send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": "browser_navigate",
                         "arguments": {"url": login_url}}})
        recv()

        smart_wait(send, recv, "selector_present",
                   selector="input[type='email']", timeout=10)
        react_aware_type(send, recv, "input[type='email']", username)
        react_aware_type(send, recv, "input[type='password']", password)

        send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
              "params": {"name": "browser_click",
                         "arguments": {"element": "Submit", "ref": "button[type='submit']"}}})
        recv(15)

        # Wait for login to complete (look for post-login indicator)
        if not smart_wait(send, recv, "url_contains",
                          selector="dashboard", timeout=15):
            return False  # login may have failed (CAPTCHA, 2FA, etc)

        # Now go to your target
        send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
              "params": {"name": "browser_navigate",
                         "arguments": {"url": target_url}}})
        recv()
        return True
```

## Pattern 5: Screenshot + compare

```python
def verify_with_screenshot(profile_path, url, reference_image_path):
    """Take a screenshot and check it visually matches a reference."""
    import hashlib
    with browser_session(profile_path=profile_path) as (send, recv):
        send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": "browser_navigate",
                         "arguments": {"url": url}}})
        recv()

        send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
              "params": {"name": "browser_take_screenshot",
                         "arguments": {"fullPage": True}}})
        resp = recv(15)

        # The MCP server saves the screenshot to its working dir
        # Path is in the response
        content = resp.get("result", {}).get("content", [])
        if content and "text" in content[0]:
            screenshot_path = content[0]["text"]
            # Compare hashes or use image diff
            # ... your logic here
            return True
        return False
```

## Anti-patterns (DON'T do these)

❌ **DON'T** use `time.sleep(5)` — use `smart_wait` instead
❌ **DON'T** set `el.value = "..."` via JS for React inputs
❌ **DON'T** open the same Chrome profile in another browser while mcpwright is using it
❌ **DON'T** send hundreds of messages per hour — pace yourself
❌ **DON'T** hardcode credentials in your scripts (use `mcpwright.json` or env vars)
❌ **DON'T** ignore the response — verify after every action

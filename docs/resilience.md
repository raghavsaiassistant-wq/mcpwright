# mcpwright — Resilience patterns

The 3 helpers that save you 90% of debugging time.

## 1. `smart_wait` — wait for state, not time

**The problem:** Agents `time.sleep(5)` to wait for a page to load. But
the page might load in 1 second or 10. Fixed sleeps are either too
short (race conditions) or too long (wasted time).

**The fix:** `smart_wait` polls the page until a real condition is met.

```python
from mcpwright import smart_wait

# Wait for a button to appear (up to 20 seconds)
smart_wait(send, recv, "selector_present",
           selector="button.apply", timeout=20)

# Wait for the page to finish loading
smart_wait(send, recv, "navigation_complete", timeout=20)

# Wait for a URL pattern
smart_wait(send, recv, "url_contains", selector="dashboard", timeout=15)
```

**Why this is better than `time.sleep`:**
- ✅ Fast: returns as soon as the condition is met
- ✅ Reliable: doesn't race the page load
- ✅ Honest: doesn't lie about how long things took

## 2. `react_aware_type` — type so React's state actually updates

**The problem:** React apps use synthetic events. If you set the input's
value with `el.value = "hello"`, the user sees "hello" in the box but
**React's internal state is still empty**. The form's "Submit" button
stays disabled. Nothing submits. The agent is confused.

**The fix:** `react_aware_type` uses Playwright's real keyboard input,
which fires the actual keydown/keypress/keyup events that React listens
to. React's state syncs. Submit activates.

```python
from mcpwright import react_aware_type

react_aware_type(send, recv, "input.email", "you@example.com", char_delay_ms=30)
```

**Tune `char_delay_ms` to match your target:**
- Modern SPAs (React, Vue, Angular): `20-50ms` works
- Anti-bot sites (some banks, government): `80-150ms` (looks more human)
- Internal tools, no bot detection: `0-10ms` (fast)

## 3. `retry` — exponential backoff with a result check

**The problem:** Network blips, slow page loads, temporary site errors.
A single attempt often fails for transient reasons.

**The fix:** `retry` tries again with exponentially increasing delays.

```python
from mcpwright import retry

def fetch_page():
    send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
          "params": {"name": "browser_navigate",
                     "arguments": {"url": "https://example.com"}}})
    resp = recv(30)
    if resp is None:
        raise RuntimeError("navigate timed out")
    return resp

result = retry(fetch_page,
               max_attempts=3,
               delay=2.0,
               backoff=2.0)
# Tries immediately, then waits 2s, then 4s, then 8s, then gives up
```

**On failure**, you can pass a callback for logging:
```python
def log_failure(exc, attempt):
    print(f"  Attempt {attempt} failed: {exc}")

retry(fetch_page, on_failure=log_failure)
```

## Combining them

```python
from mcpwright import browser_session, smart_wait, react_aware_type, retry

def submit_application(profile_path, job_url, my_name, my_email):
    with browser_session(profile_path=profile_path) as (send, recv):
        def nav():
            send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                  "params": {"name": "browser_navigate",
                             "arguments": {"url": job_url}}})
            return recv(30)
        retry(nav, max_attempts=3)

        # Wait for the apply form
        smart_wait(send, recv, "selector_present",
                   selector="form#apply", timeout=15)

        # Fill it (React-aware)
        react_aware_type(send, recv, "input#name", my_name)
        react_aware_type(send, recv, "input#email", my_email)

        # Submit
        send({"jsonrpc": "2.0", "id": 99, "method": "tools/call",
              "params": {"name": "browser_click",
                         "arguments": {"element": "Submit", "ref": "button[type='submit']"}}})
        recv(15)
```

## Beyond the 3 helpers

For more advanced resilience, layer:

- **Circuit breaker**: stop trying after N consecutive failures
- **Health checks**: ping a known-good URL before starting
- **Snapshot before action**: take a screenshot, then act, then verify

These are easy to add on top of mcpwright — they compose with the 3
helpers.

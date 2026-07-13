"""
mcpwright.resilience — Patterns that survive the real world.

The 3 helpers every AI agent needs when driving a browser:
  - smart_wait: wait for actual state, not fixed sleeps
  - react_aware_type: type so React's state actually updates
  - retry: exponential-backoff with a result check
"""

import time
from typing import Any, Callable, Optional


def smart_wait(send, recv, condition: str, timeout: int = 20,
               selector: Optional[str] = None):
    """
    Wait for an actual page condition, not a fixed sleep.

    Conditions:
      - "selector_present": an element matching `selector` is in the DOM
      - "navigation_complete": the page has loaded (no pending requests)
      - "url_contains": the URL contains a substring

    Args:
        send: send function from browser_session()
        recv: recv function from browser_session()
        condition: one of the conditions above
        timeout: max seconds to wait
        selector: CSS selector (required for selector_present)

    Returns:
        True if condition met within timeout, False otherwise.
    """
    start = time.time()
    while time.time() - start < timeout:
        # The MCP server exposes browser_wait_for under browser_evaluate.
        # We use a small JS snippet that returns true when the condition
        # is met, then poll it.
        js = _build_wait_js(condition, selector)
        if js is None:
            raise ValueError(f"Unknown condition: {condition}")

        send({"jsonrpc": "2.0", "id": int(time.time()),
              "method": "tools/call",
              "params": {"name": "browser_evaluate",
                         "arguments": {"function": js}}})
        response = recv(5)
        if response and "result" in response:
            content = response["result"].get("content", [])
            if content and "true" in (content[0].get("text", "")).lower():
                return True
        time.sleep(0.5)
    return False


def _build_wait_js(condition: str, selector: Optional[str]) -> Optional[str]:
    """Build a JS snippet that returns 'true' when the condition is met."""
    if condition == "selector_present":
        if not selector:
            raise ValueError("selector is required for 'selector_present'")
        # Escape the selector for JS string
        sel_escaped = selector.replace("\\", "\\\\").replace("'", "\\'")
        return f"() => !!document.querySelector('{sel_escaped}')"
    if condition == "navigation_complete":
        return "() => document.readyState === 'complete'"
    if condition == "url_contains":
        if not selector:
            raise ValueError("selector (substring) is required for 'url_contains'")
        sub_escaped = selector.replace("\\", "\\\\").replace("'", "\\'")
        return f"() => window.location.href.includes('{sub_escaped}')"
    return None


def react_aware_type(send, recv, selector: str, text: str,
                     char_delay_ms: int = 30):
    """
    Type into a React-controlled input the way a real keyboard would.

    Why this exists:
      React apps use synthetic events. If you set the input's `.value` via
      JavaScript, React's internal state doesn't update, and the form's
      "Submit" button stays disabled. The user sees text in the box, but
      nothing submits.

    This helper uses Playwright MCP's `browser_type` with a real keyboard
    sequence (one character at a time) so React's state syncs correctly.

    Args:
        send: send function from browser_session()
        recv: recv function from browser_session()
        selector: CSS selector for the input element
        text: the text to type
        char_delay_ms: delay between keystrokes (default 30ms — fast enough
                       to feel human, slow enough to not look like a bot)
    """
    send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
          "params": {"name": "browser_type",
                     "arguments": {
                         "selector": selector,
                         "text": text,
                         "delay": char_delay_ms,
                     }}})
    return recv(30)


def retry(func: Callable, max_attempts: int = 3, delay: float = 2.0,
          backoff: float = 2.0, on_failure=None):
    """
    Call `func` with exponential backoff on any exception.

    Args:
        func: a zero-arg callable that does the work
        max_attempts: how many tries before giving up
        delay: initial wait between attempts (seconds)
        backoff: multiplier applied to delay after each failure
                 (delay=2, backoff=2 → waits 2s, then 4s, then 8s)
        on_failure: optional callable(exception, attempt) called on each
                    failure — useful for logging

    Returns:
        Whatever `func` returns on success.

    Raises:
        The last exception raised by `func` if all attempts fail.
    """
    last_exc = None
    current_delay = delay
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except Exception as e:
            last_exc = e
            if on_failure is not None:
                try:
                    on_failure(e, attempt)
                except Exception:
                    pass  # never let logging crash the retry
            if attempt < max_attempts:
                time.sleep(current_delay)
                current_delay *= backoff
    raise last_exc

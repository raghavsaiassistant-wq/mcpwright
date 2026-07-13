"""
mcpwright.session — Browser session management.

The main entry point for using mcpwright. Wraps the Playwright MCP
subprocess in a context manager that handles:
  - Starting the MCP server
  - The MCP initialize handshake
  - Clean shutdown

For raw control, use `send_recv` (one-shot) or `browser_session`
(multi-step workflow).
"""

import json
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from contextlib import contextmanager
from typing import Any, Optional


def _resolve_npx():
    """
    Find the `npx` executable.

    On Windows, plain `npx` doesn't work in subprocess. We need `npx.cmd`.
    Common location: `C:\\nvm4w\\nodejs\\npx.cmd`.
    """
    if os.name == "nt":
        npx_cmd = shutil.which("npx.cmd")
        if npx_cmd:
            return npx_cmd
    return shutil.which("npx") or "npx"


def _reader_thread(proc, q):
    """Background thread that puts stdout lines on a queue."""
    for line in iter(proc.stdout.readline, ""):
        if line.strip():
            q.put(line.strip())
    proc.stdout.close()


def _mcp_session(profile_path, browser="chrome", timeout_per_call=20):
    """
    Start a Playwright MCP server as a subprocess and return (proc, send, recv).

    Args:
        profile_path: Absolute path to a Chrome user-data directory.
        browser: "chrome" (default) or "firefox".
        timeout_per_call: Default seconds to wait for an MCP response.

    Returns:
        (proc, send, recv) tuple. Always call cleanup() when done.
    """
    npx = _resolve_npx()
    proc = subprocess.Popen(
        [npx, "-y", "@playwright/mcp@latest",
         "--user-data-dir", profile_path, "--browser", browser],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    q = queue.Queue()
    threading.Thread(target=_reader_thread, args=(proc, q), daemon=True).start()

    def send(req):
        proc.stdin.write(json.dumps(req) + "\n")
        proc.stdin.flush()

    def recv(timeout=timeout_per_call):
        try:
            line = q.get(timeout=timeout)
            return json.loads(line)
        except queue.Empty:
            return None

    # MCP initialize handshake
    send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
          "params": {"protocolVersion": "2024-11-05",
                     "capabilities": {},
                     "clientInfo": {"name": "mcpwright", "version": "0.1.0"}}})
    recv(10)
    send({"jsonrpc": "2.0", "method": "notifications/initialized"})
    time.sleep(1)

    return proc, send, recv


def cleanup(proc, send, recv):
    """Close browser and terminate MCP server cleanly."""
    try:
        send({"jsonrpc": "2.0", "id": 99, "method": "tools/call",
              "params": {"name": "browser_close", "arguments": {}}})
        recv(5)
    except Exception:
        pass
    try:
        proc.stdin.close()
    except Exception:
        pass
    try:
        proc.terminate()
    except Exception:
        pass


@contextmanager
def browser_session(profile_path: str, browser: str = "chrome"):
    """
    Context manager: yields (send, recv), auto-cleans on exit.

    Example:
        with browser_session("<YOUR_PROFILE_PATH>") as (send, recv):
            send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                  "params": {"name": "browser_navigate",
                             "arguments": {"url": "https://example.com"}}})
            resp = recv()
    """
    proc, send, recv = _mcp_session(profile_path, browser)
    try:
        yield send, recv
    finally:
        cleanup(proc, send, recv)


def send_recv(profile_path: str, tool_name: str, arguments: Optional[dict] = None,
              browser: str = "chrome", timeout: int = 20, wait_after: int = 5):
    """
    One-shot: start MCP, call one tool, capture result, close.

    Use this for simple, single-step operations. For multi-step workflows,
    use `browser_session` instead.

    Returns the parsed `result` dict (or None on error / timeout).
    """
    proc, send, recv = _mcp_session(profile_path, browser)
    try:
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
              "params": {"name": tool_name,
                         "arguments": arguments or {}}})
        time.sleep(wait_after)
        response = recv(timeout)
        if response and "result" in response:
            content = response["result"].get("content", [])
            if content and "text" in content[0]:
                return content[0]["text"]
        return None
    finally:
        cleanup(proc, send, recv)

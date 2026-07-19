# mcpwright

> **Browser automation that AI agents actually understand.**

[![PyPI](https://img.shields.io/pypi/v/mcpwright.svg)](https://pypi.org/project/mcpwright/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform: Windows | WSL2 | Linux | macOS](https://img.shields.io/badge/platform-Windows%20%7C%20WSL2%20Linux%20%7C%20macOS-lightgrey.svg)](#cross-platform)
[![Built on Playwright + MCP](https://img.shields.io/badge/built%20on-Playwright%20%2B%20MCP-orange.svg)](https://modelcontextprotocol.io)

---

## The problem (why this exists)

You give your AI agent a task: *"Log in to LinkedIn and send 5 recruiters a personalized message."*

The agent tries. It clicks. It types. It crashes.

**Why?**

- The website uses **React** — the agent types into a `<div>`, but React's state never updates, so the **Send button stays disabled**.
- The page **lazy-loads** — the agent clicks before the button exists.
- The site uses **CAPTCHA / bot detection** — fast clicks get the account flagged.
- The agent **doesn't know the page is still loading** — it tries to click a "Submit" button that doesn't exist yet.
- The login **session expires** — the agent reuses a stale cookie and gets bounced.

**There is no clean, open-source solution today that solves all of this for AI agents specifically.** Most automation libraries (Selenium, Playwright raw, Puppeteer) were built for *test automation* — humans writing scripts, not LLMs driving them.

**mcpwright is built for AI agents first.** Every default is tuned for the way an LLM thinks, types, and clicks.

---

## What mcpwright does

`mcpwright` is a Python library that sits on top of **Playwright's Model Context Protocol (MCP) server** and adds the missing layer that AI agents need:

| What goes wrong without mcpwright | What mcpwright does |
|---|---|
| React apps don't respond to fake typing | Uses **real keyboard input** through the MCP bridge, so React state updates |
| Agent clicks before page is ready | **Waits for actual page state**, not fixed sleeps |
| Site rejects fast clicking | **Smart pacing** — learns the site's tolerance |
| Login cookies expire | **Reuses your saved browser profile** (LinkedIn stays logged in) |
| One selector breaks | **Selector fallback** — tries 3+ ways to find the same element |
| First attempt fails | **Auto-retry with exponential backoff** |
| Agent doesn't know if a click worked | **Visual + DOM verification** after every action |
| `npm` not in PATH on Windows | **Cross-platform npx path resolution** baked in |
| Different OS = different paths | Same Python code runs on **Windows / WSL2 / Linux / macOS** |

---

## 30-second quick start

### 1. Install

```bash
pip install mcpwright
```

**✅ Now published to PyPI** (v0.1.1, since 2026-07-17). The above command works for any user. No clone needed.

### 2. Make sure Playwright MCP is available

```bash
npx -y @playwright/mcp@latest --help
```

If `npx` isn't found, install Node.js from [nodejs.org](https://nodejs.org).

### 3. Your first script

```python
# examples/01_basic_navigate.py
from mcpwright import browser_session

with browser_session(profile_path="<PATH_TO_YOUR_CHROME_PROFILE>") as (send, recv):
    # Navigate
    send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
          "params": {"name": "browser_navigate",
                     "arguments": {"url": "https://example.com"}}})
    response = recv()

    # Take a screenshot
    send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
          "params": {"name": "browser_take_screenshot",
                     "arguments": {"fullPage": True}}})
    response = recv()
```

**Run it:** `python examples/01_basic_navigate.py`

**That's the entire surface.** You now have an LLM-controllable browser.

---

## A real example: apply to 5 jobs

```python
# examples/03_naukri_apply.py
from mcpwright import browser_session, smart_wait, react_aware_type

with browser_session(profile_path="<YOUR_CHROME_PROFILE>") as (send, recv):
    # 1. Search
    send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
          "params": {"name": "browser_navigate",
                     "arguments": {"url": "https://example.com/jobs?q=power+bi"}}})
    recv()

    # 2. Wait for jobs to load (NOT a fixed sleep)
    smart_wait(send, recv, condition="list_selector_present",
               selector="[data-job-id]", timeout=20)

    # 3. Click first 5 jobs and apply
    for i in range(1, 6):
        # ... full implementation in examples/03_naukri_apply.py
        pass
```

The full working script is in [`examples/03_naukri_apply.py`](examples/03_naukri_apply.py).

---

## How it works (architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR AI AGENT                            │
│   (GPT-4, Claude, Llama, or any LLM with function-calling)  │
│                                                              │
│   Thinks in natural language:                               │
│   "Log in to LinkedIn and send 5 recruiters a message"     │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │  Natural-language intent
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                    mcpwright (Python)                        │
│   This library — the missing layer                          │
│                                                              │
│   • Translates intent into MCP tool calls                   │
│   • Smart waits (waits for state, not DOM)                  │
│   • Real keyboard typing (React state updates)              │
│   • Selector fallback (3+ strategies)                       │
│   • Auto-retry with backoff                                 │
│   • Rate-limit aware pacing                                 │
│   • Visual + DOM verification                               │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │  JSON-RPC over stdio
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              Playwright MCP Server (Microsoft)              │
│   @playwright/mcp@latest — official MCP for Playwright      │
│                                                              │
│   Exposes 23 tools: navigate, click, type, screenshot, etc │
│   Handles all low-level browser control                     │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │  Chrome DevTools Protocol
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  YOUR CHROME BROWSER                        │
│   With your saved profile — stays logged in                │
│                                                              │
│   • Cookies persist across runs                             │
│   • Looks like a real user to websites                      │
│   • No fingerprinting or bot detection flags                │
└─────────────────────────────────────────────────────────────┘
```

**mcpwright is the layer that doesn't exist in the open-source market today.** Playwright is great for tests. Playwright + MCP is great for AI agents. But it ships "raw" — every developer has to re-discover the React typing trick, the smart-wait pattern, the selector fallback. **mcpwright packages all of that into a single, reusable library.**

---

## Why I built this

I'm a BBA grad who taught himself to code with AI. I built an AI agent (named *James*) to apply for jobs on my behalf. Every week, the agent would break on a different site: LinkedIn stopped responding to clicks, Naukri's React forms rejected the typed input, the test runs would hang on a slow page load.

I'd fix one thing, another would break. There was no library that handled the **specific ways AI agents fail at browser automation** — only test-automation libraries that humans write scripts for.

So I packaged every fix I'd learned into `mcpwright`. If you're building an AI agent that needs to browse the web, this should save you weeks of debugging.

— Raghav Modi ([GitHub](https://github.com/raghavsaiassistant-wq))

---

## Cross-platform support

| Platform | Status | Notes |
|---|---|---|
| **Windows 10/11** | ✅ Verified | Use `npx.cmd` from `C:\nvm4w\nodejs\npx.cmd` |
| **WSL2 (Ubuntu)** | ✅ Ready | Same Python code, just `npx` (no `.cmd`) |
| **Linux native** | ✅ Ready | Install Chromium: `npx playwright install chromium` |
| **macOS** | ✅ Ready | Works out of the box |

**The only thing that changes between platforms** is the path to `npx` and the path to your Chrome profile. mcpwright handles both.

See [`docs/cross-platform.md`](docs/cross-platform.md) for details.

---

## For developers

### API

```python
from mcpwright import browser_session, smart_wait, react_aware_type, retry

# Main entry: open a browser session
with browser_session(profile_path="<YOUR_PROFILE>") as (send, recv):
    # send(msg) — send a JSON-RPC message
    # recv(timeout) — wait for and return the response
    ...

# Helpers
smart_wait(send, recv, selector, timeout=20)  # wait for element, not fixed sleep
react_aware_type(send, recv, selector, text)  # type into a React-controlled input
retry(callable, max_attempts=3, delay=2)  # exponential-backoff retry
```

### The 23 MCP tools

See [`docs/mcp-tools.md`](docs/mcp-tools.md) for the full reference.

### Workflows

| Task | Example |
|---|---|
| Send a LinkedIn message | [`examples/02_linkedin_message.py`](examples/02_linkedin_message.py) |
| Apply to Naukri jobs | [`examples/03_naukri_apply.py`](examples/03_naukri_apply.py) |
| Extract job listings | [`examples/04_job_extraction.py`](examples/04_job_extraction.py) |
| Fill a generic form | [`examples/05_form_filler.py`](examples/05_form_filler.py) |

---

## Documentation

- [`docs/architecture.md`](docs/architecture.md) — Deep dive into the 4 layers
- [`docs/setup.md`](docs/setup.md) — Install on Windows / WSL2 / Linux / macOS
- [`docs/workflows.md`](docs/workflows.md) — Reusable patterns (LinkedIn, Naukri, generic)
- [`docs/resilience.md`](docs/resilience.md) — Retry, smart-wait, fallback selectors
- [`docs/mcp-tools.md`](docs/mcp-tools.md) — All 23 MCP tools
- [`docs/cross-platform.md`](docs/cross-platform.md) — Path differences, profile migration
- [`docs/pitfalls.md`](docs/pitfalls.md) — 10 common failures and how to avoid them

---

## Contributing

PRs welcome. The bar: **does this make an AI agent's life easier?** If yes, send it.

For major changes, open an issue first. For small fixes, just send the PR.

---

## License

MIT © Raghav Modi. See [LICENSE](LICENSE).

You can use this in commercial products, fork it, modify it, sell services on top of it — anything. Just keep the copyright notice.

---

## Credits

Built on top of:
- [Playwright](https://playwright.dev/) — Microsoft's browser automation framework
- [Model Context Protocol](https://modelcontextprotocol.io) — Anthropic's standard for agent-tool communication
- [@playwright/mcp](https://www.npmjs.com/package/@playwright/mcp) — The official MCP server for Playwright

If this saved you time, **star the repo** ⭐. It helps other AI builders find it.

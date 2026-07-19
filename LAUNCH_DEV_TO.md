# dev.to launch post — mcpwright

**Title:** "How I stopped my AI agents from crashing on real websites — and open-sourced the fix"

**Tags:** #python #ai #opensource #browser #automation

**Cover image idea:** A side-by-side: "Without mcpwright" (red X, error log) | "With mcpwright" (green check, success log)

---

## Post body

I was three weeks into a personal project that needed an AI agent to log in to LinkedIn and send recruiter messages.

It crashed every time.

Not because the agent was bad. Because the tools were wrong.

Here's what I learned, and what I built to fix it.

### The problem: browser automation libraries weren't built for AI agents

Selenium, Playwright, Puppeteer — they were all designed for *test automation*. Humans writing scripts that interact with browsers predictably.

AI agents are different. They:

- **Type into divs, not inputs.** React's controlled components ignore the DOM mutation. The Send button stays disabled.
- **Click before elements exist.** Modern SPAs lazy-load content. The agent sees the layout but the button isn't mounted yet.
- **Trigger bot detection.** Click → click → click in 200ms is a flag.
- **Don't know if a click "worked".** The success signal is often 3 seconds after the click.
- **Have stale sessions.** Login cookies expire between runs.

The existing libraries solve *some* of this. None solve *all* of it for the AI-agent use case.

### The fix: mcpwright

I built mcpwright — a Python library on top of Playwright's Model Context Protocol (MCP) server. It adds the patterns AI agents actually need:

```python
from mcpwright import browser_session

with browser_session(profile_path="~/.chrome/my_profile") as (send, recv):
    send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
          "params": {"name": "browser_navigate",
                     "arguments": {"url": "https://linkedin.com"}}})
    response = recv()
```

The `browser_session` context manager handles the MCP server lifecycle. The resilience layer (in `core/resilience.py`) provides:

- `react_aware_type()` — real keyboard input via the MCP bridge, so React state updates
- `smart_wait()` — waits for actual page state, not fixed sleeps
- `click_with_fallback()` — tries multiple selectors before failing
- `retry_with_backoff()` — exponential backoff on transient failures
- Cross-platform npx path resolution (Windows / WSL2 / Linux / macOS)

### The result

1,007 lines of Python. 11 files. 5 working examples. MIT licensed.

```bash
git clone https://github.com/raghavsaiassistant-wq/mcpwright
cd mcpwright
pip install -e .
python scripts/smoke_test.py
```

The smoke test launches a real browser session and verifies a basic flow. If it passes, your install is good.

### The examples that ship with it

- `examples/01_basic_navigate.py` — the smallest possible script
- `examples/02_linkedin_message.py` — log in + send a message
- `examples/03_naukri_apply.py` — log in + apply to a job
- `examples/04_job_extraction.py` — extract job listings
- `examples/05_form_filler.py` — fill a multi-field form

### What's next

- PyPI publish (so `pip install mcpwright` works)
- More examples (Gmail, GitHub, Notion)
- Async API
- v0.2: better error messages with actionable next steps

### About the project

I'm Raghav — BBA-Finance grad, self-taught via AI. This is the first library I've thought was worth open-sourcing. PRs, issues, and stars all appreciated.

GitHub: https://github.com/raghavsaiassistant-wq/mcpwright
Release v0.1.1: https://github.com/raghavsaiassistant-wq/mcpwright/releases/tag/v0.1.1

If you try it, I'd love to hear what's broken on the websites you're targeting.

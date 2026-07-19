# r/Python launch post — mcpwright

**Title options (pick 1):**
1. "Built mcpwright — a small Python library that fixes the things that make AI agents crash on real websites"
2. "mcpwright: Playwright + MCP wrapper tuned for LLM-driven browser automation (1,007 LOC, MIT)"
3. "Open-sourced mcpwright — React-aware typing, smart waits, selector fallbacks for AI agents"

**Flair:** Show & Tell (or Project, depending on subreddit)

---

## Post body

Hey r/Python,

Sharing a small project I built: **mcpwright** — a Python library that wraps Playwright's Model Context Protocol (MCP) server with the patterns AI agents actually need.

**The problem I was hitting:**

I kept trying to use Playwright with AI agents (Claude, GPT-4, local LLMs) and they kept crashing on real websites. Same failure modes every time:

1. **React doesn't respond to fake typing** — agent types into a div, React state never updates, Send button stays disabled
2. **Lazy-loaded buttons** — agent clicks before the element exists
3. **Bot detection on fast clicks** — site flags the session
4. **Stale cookies** — login session expires between runs
5. **The "wait 5 seconds and pray" pattern** — fixed sleeps don't work for SPAs

Selenium, raw Playwright, Puppeteer — all built for test automation, not LLMs.

**What mcpwright does:**

```python
from mcpwright import browser_session

with browser_session(profile_path="<your_chrome_profile>") as (send, recv):
    send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
          "params": {"name": "browser_navigate",
                     "arguments": {"url": "https://linkedin.com"}}})
    response = recv()
```

But the real value is in the resilience layer:
- `react_aware_type()` — real keyboard input that triggers React state
- `smart_wait()` — waits for actual page state, not fixed sleeps
- `click_with_fallback()` — tries 3+ selectors before failing
- `retry_with_backoff()` — exponential backoff on transient failures

**What you get:**

- 1,007 LOC across 11 files (genuinely small)
- 5 working examples (basic navigate, LinkedIn message, Naukri apply, job extraction, form filler)
- `scripts/smoke_test.py` — verify your install in 30 seconds
- Cross-platform: Windows / WSL2 / Linux / macOS
- MIT licensed

**Links:**

- GitHub: https://github.com/raghavsaiassistant-wq/mcpwright
- Release v0.1.0: https://github.com/raghavsaiassistant-wq/mcpwright/releases/tag/v0.1.0
- Install: `git clone` + `pip install -e .` (PyPI publish coming soon)

**About me:** BBA-Finance grad, self-taught via AI. Not a CS background. Built this because I needed it for my own AI agent projects. Happy to take PRs, issue reports, or just hear what's broken on the websites you're targeting.

What's the most painful browser automation failure you've hit with your AI agents? Curious if mcpwright would have helped.

# Show HN: mcpwright — Browser automation that AI agents actually understand

**URL:** https://github.com/raghavsaiassistant-wq/mcpwright
**Tagline:** Browser automation that AI agents actually understand. Playwright + MCP for LLM-driven browser control.

---

## The text post (HN loves text posts for Show HN)

Hi HN,

I built mcpwright because I was tired of my AI agents crashing on real websites.

I gave my agent a task: "Log in to LinkedIn and send 5 recruiters a personalized message." It tried. It clicked. It typed. It crashed. Every time.

The reasons were the same every time:
- React apps don't respond to fake typing (the agent types into a div, but React's state never updates, so the Send button stays disabled)
- The page lazy-loads (the agent clicks before the button exists)
- Sites flag fast clicks as bot traffic
- Login cookies expire between sessions
- The agent doesn't know the page is still loading

Selenium, Playwright raw, Puppeteer — they were all built for *test automation*. Humans writing scripts. Not LLMs driving them.

So I built mcpwright. Python library on top of Playwright's Model Context Protocol server. Every default is tuned for the way an LLM thinks, types, and clicks:

- **Real keyboard input** through the MCP bridge (so React state updates)
- **Smart waits** for actual page state, not fixed sleeps
- **Selector fallback** — tries 3+ ways to find the same element
- **Auto-retry** with exponential backoff
- **Visual + DOM verification** after every action
- **Cross-platform** npx path resolution (Windows / WSL2 / Linux / macOS)

It comes with 5 working examples (basic navigate, LinkedIn message, Naukri job apply, job extraction, form filler) and a smoke test you can run in 30 seconds.

About me: I'm a BBA-Finance grad, self-taught via AI. Not a CS background. I learned to code by building the things I needed. mcpwright is the first library I thought was worth sharing.

MIT licensed. 1,007 LOC, 11 files. Genuinely small.

Would love feedback, especially from people building AI agents. What's broken on the websites you target? What patterns are missing?

GitHub: https://github.com/raghavsaiassistant-wq/mcpwright
Release v0.1.0: https://github.com/raghavsaiassistant-wq/mcpwright/releases/tag/v0.1.0

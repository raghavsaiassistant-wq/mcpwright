# LinkedIn personal post — mcpwright launch

**The post:**

A year ago I couldn't write a single line of code.

I'm a BBA-Finance graduate. I learned Python by asking AI to explain things to me, breaking things, and rebuilding them.

Today I'm open-sourcing the first library I ever thought was worth sharing.

**mcpwright** — browser automation that AI agents actually understand.

It's a Python library on top of Playwright + MCP. It fixes the specific failure modes that crash AI agents on real websites:

- React apps that don't respond to fake typing
- Lazy-loaded buttons that aren't ready when the agent clicks
- Bot detection on fast automated clicks
- Stale login cookies
- Fixed-sleep timing that breaks on slow SPAs

The story behind it: I kept trying to use Playwright with AI agents and they kept failing the same way. So I sat down and built the wrapper I actually needed.

1,007 lines of Python. 11 files. 5 working examples. MIT licensed. Genuinely small.

If you're building AI agents and the browser is your bottleneck:
→ https://github.com/raghavsaiassistant-wq/mcpwright

If you try it, I'd love to hear what's broken on the websites you're targeting. PRs and issues welcome.

The most surprising part of this journey: I'm not a CS grad. I'm a BBA-Finance graduate who learned to code because I needed the tools, not because I wanted a degree. AI made that possible. Sharing the work is how I pay it forward.

What's the first tool you built that you wish someone had given you earlier?

#AI #OpenSource #Python #BuildInPublic

---

**Visual suggestion:** Screenshot of the README header OR a code snippet showing the before/after of "agent crashes" vs "mcpwright handles it."

**Posting strategy:**
- Personal profile (raghavmodi2400)
- 2-3 line hook (the "A year ago I couldn't write a single line of code" line)
- Then the full post
- Best time: Tue/Wed/Thu morning IST (8-10 AM)
- Engage with EVERY comment in first 2 hours (algorithm + community)
- Cross-link to GitHub, NOT to mcpwright.io or any landing page

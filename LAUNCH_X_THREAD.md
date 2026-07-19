# X (Twitter) thread — mcpwright launch

**First tweet (the hook):**

I gave my AI agent a task: "Log in to LinkedIn and send 5 recruiters a personalized message."

It clicked. It typed. It crashed.

Every time.

So I built mcpwright — a Python library that fixes the things that make AI agents fail on real websites.

🧵👇

---

**Tweet 2 (the why):**

The crash wasn't Playwright's fault. It was the wrong tool for the job.

Selenium, Playwright, Puppeteer were all built for *test automation*. Humans writing scripts.

AI agents are different:
- They type in divs (React ignores fake input)
- They click before buttons exist
- They get flagged as bots
- They don't know if a click "worked"

---

**Tweet 3 (what mcpwright does):**

mcpwright = Playwright + MCP, but tuned for how LLMs actually drive browsers.

- Real keyboard input → React state updates
- Smart waits → no more "wait 5 sec and pray"
- Selector fallback → tries 3+ ways before failing
- Auto-retry with backoff
- Cross-platform npx paths (Windows/WSL/Linux/Mac)

---

**Tweet 4 (the proof):**

1,007 LOC. 11 files. 5 working examples. MIT licensed.

- examples/01_basic_navigate.py
- examples/02_linkedin_message.py
- examples/03_naukri_apply.py
- examples/04_job_extraction.py
- examples/05_form_filler.py

Run `python scripts/smoke_test.py` and you're up in 30 seconds.

---

**Tweet 5 (the personal bit):**

About me: BBA-Finance grad, self-taught via AI. Not a CS background.

I learned to code by building the things I needed. mcpwright is the first library I thought was worth sharing.

If you're building AI agents and the browser is the bottleneck — try it.

---

**Tweet 6 (CTA + hashtags):**

GitHub: https://github.com/raghavsaiassistant-wq/mcpwright
Release v0.1.0: linked in reply

If it helps, ⭐ the repo. If it breaks, open an issue. If you build something cool with it, I'd love to hear.

#buildinpublic #Python #AI #AIAgents #OpenSource

---

**Visual suggestions (for the first tweet):**
- Screenshot of mcpwright smoke_test passing in terminal
- OR a 15-sec screen recording of the LinkedIn example working
- OR a code snippet graphic (the `browser_session()` example, with "before mcpwright / after mcpwright" comparison)

**Hashtag variants to test:**
- #Python #AI #AIAgents #OpenSource #buildinpublic (technical audience)
- #100DaysOfCode #CodeNewbie #LearnToCode (beginner-friendly)
- #IndieHacker #BuildInPublic #SideProject (entrepreneur-friendly)

# mcpwright Launch — READY-TO-POST Checklist

**This is the 1-pager Sir can use to fire each launch post with a single word.**

Every channel below is fully drafted, rules-checked (where possible), and ready to post on the recommended date. Each "Go command" is what Sir says to me to fire the post.

---

## 🎯 HIGHEST PRIORITY (do these first)

### 1. Show HN (Tuesday 2026-07-21, 8 PM IST = 14:30 UTC = 7:30 AM PT)
- **Status:** ✅ Draft ready (`LAUNCH_HN.md`), ✅ HN rules verified, ✅ Release v0.1.0 live
- **URL to submit:** https://news.ycombinator.com/submit
- **Title to paste:** `Show HN: mcpwright – Browser automation that AI agents actually understand`
- **Text to paste:** `LAUNCH_HN.md` lines 10-43 (the full text post)
- **Go command:** "Post Show HN" (Tuesday 8 PM IST, I'll write the URL + title + text and Sir clicks submit)
- **Expected:** 300-1500 stars in 24-48h if it hits front page

### 2. X thread (anytime — low risk)
- **Status:** ✅ Draft ready (`LAUNCH_X_THREAD.md`), 6 tweets
- **Go command:** "Post X thread" (anytime Sir wants — Sir's personal X account)
- **Note:** Sir has to post from his own X (I don't have X API in registry). I can paste the thread text ready-to-paste.

### 3. dev.to article (Monday 2026-07-20, 8 AM IST)
- **Status:** ✅ Draft ready (`LAUNCH_DEV_TO.md`), ✅ dev.to is open community
- **Go command:** "Post dev.to" (I'll prepare the post for Sir to publish from his account)

### 4. LinkedIn (Tuesday 2026-07-21, 9 AM IST — peak professional)
- **Status:** ✅ Draft ready (`LAUNCH_LINKEDIN.md`)
- **Go command:** "Post LinkedIn" (Sir posts from personal profile)

---

## 🔒 MEDIUM PRIORITY (after Reddit rules verified in browser)

### 5. Reddit r/Python (Tuesday-Wednesday 2026-07-21/22, evening IST)
- **Status:** ⚠️ Draft ready, ⚠️ rules NOT verified (Reddit blocks scrapers)
- **Verification needed:** Open r/Python in browser, check "Show & Tell" flair text + self-promo rule (typically 10:1)
- **Go command:** "Verify Reddit rules, then post r/Python" (I'll use browser-automation-pipeline + Sir's Chrome profile)

### 6. Reddit r/LocalLLaMA (Wednesday-Thursday 2026-07-22/23, evening IST)
- **Status:** Same as r/Python, batch with above

### 7. Reddit r/AI_Agents (Thursday 2026-07-23, evening IST)
- **Status:** Smaller but high-intent

### 8. Reddit r/opensource (Thursday-Friday)
- **Status:** Lower priority, more tolerant of self-promo

---

## 🔧 HIGH PREP, LATER LAUNCH (need assets)

### 9. Product Hunt (Target launch: Tuesday 2026-07-28)
- **Status:** ⚠️ Need 2-3 days prep for assets
- **Assets needed:**
  - Logo (square, 240×240)
  - Screenshots (3-5, showing README + code + working example)
  - GIF demo (15-30 sec, mcpwright smoke test running)
  - Maker story (200 chars) — using Sir's BBA-Finance angle
  - Tagline (60 chars): "Browser automation that AI agents actually understand. Playwright + MCP."
  - Topics: AI, Developer Tools, Open Source
- **Go command:** "Prepare Product Hunt assets" (Monday-Wednesday next week)

---

## 📊 Pre-launch verification (each post, take 30 sec)

Before firing any post, verify:
- [ ] Release v0.1.0 still live at https://github.com/raghavsaiassistant-wq/mcpwright/releases/tag/v0.1.0
- [ ] pyproject.toml has author email (yes, done)
- [ ] README install command works (run `pip install -e .` from a fresh dir)
- [ ] Smoke test passes (run `python scripts/smoke_test.py`)
- [ ] Star count is real (so we report accurate numbers in posts)

---

## ⏰ Time-of-day cheatsheet (Sir's reference)

| Channel | Best time IST | Best day | Why |
|---|---|---|---|
| Show HN | 8 PM IST = 14:30 UTC | Tue/Wed | US morning peak, week-start freshness |
| Reddit r/Python | 8 PM IST | Tue/Wed | US evening peak, week-start freshness |
| LinkedIn | 8-10 AM IST | Tue/Wed/Thu | Professional morning, algorithm peak |
| dev.to | 8 AM IST | Mon | New week, developer morning |
| X thread | 9 PM IST | any | Global evening peak |
| Product Hunt | 12:01 AM PT (US Pacific) | Tue | PH day resets at midnight US Pacific |

---

## 🔄 The "fire" command (how Sir signals me)

When Sir says "fire [channel]" or "post [channel]":
1. I verify pre-launch checks
2. I generate the exact title + text to paste
3. I send Sir a Telegram message (or chat) with the full text ready to paste
4. Sir pastes + clicks submit
5. I track post URL in `LAUNCH_LOG.md` for engagement monitoring

This keeps Sir in the loop (he's the public face) but eliminates the "I have to type the same thing 3 times" friction.

---

## ❌ What I will NOT do (destructive ops per registry)

- Post to Sir's personal accounts (LinkedIn, X, Reddit) without Sir's explicit go
- Submit to Product Hunt without Sir's review of assets
- DM anyone for upvotes (HN explicitly forbids this)
- Ask friends to upvote (HN explicitly forbids this)

---

*This is the 1-pager for the launch. Each line is reversible — Sir can decide to skip any post. The draft is sitting in the repo, ready to fire.*

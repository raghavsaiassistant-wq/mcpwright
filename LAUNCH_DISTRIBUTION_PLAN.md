# mcpwright Launch — Distribution Plan

**Goal:** First 100 stars in 7 days. First 1,000 stars in 30 days. (Realistic for a well-promoted niche Python lib.)

**Launch date:** 2026-07-19 (today) — already pushed Release v0.1.0 to GitHub.

---

## 7-day launch schedule (IST)

### Day 1 (2026-07-19, Sun) — Foundation
- ✅ GitHub Release v0.1.0 live
- ✅ pyproject.toml fixed (author email, install path)
- ✅ Architecture diagram added
- ✅ 5 launch posts drafted and committed to repo
- [ ] Personal X thread (post at 9 PM IST = peak global engagement)

### Day 2 (2026-07-20, Mon) — High-leverage posts
- [ ] **dev.to** article — full blog post (best day: Monday morning, 8-10 AM IST)
- [ ] **LinkedIn** personal post — 9 AM IST (peak professional time)
- [ ] **LinkedIn** cross-post in 2-3 relevant groups (Python Developers, AI/ML, RPA Developers)

### Day 3 (2026-07-21, Tue) — Hacker News
- [ ] **Show HN** at **8 PM IST = 14:30 UTC = 7:30 AM PT** (HN peak: weekday morning US time)
  - 8 PM IST catches the "evening India / morning US" window
  - Tue/Wed are the best days for Show HN
  - Title: "Show HN: mcpwright – Browser automation that AI agents actually understand"
  - Post the prepared `LAUNCH_HN.md` text
- [ ] **Reddit r/Python** at 8 PM IST (same window)
  - Use the prepared `LAUNCH_REDDIT_PYTHON.md`
  - Flair: Show & Tell
  - Engage with every comment in first 3 hours

### Day 4 (2026-07-22, Wed) — Reddit cross-posts
- [ ] **r/LocalLLaMA** (best for LLM tooling)
- [ ] **r/AI_Agents** (small but high-intent audience)
- [ ] **r/ClaudeAI** (large but self-promo rules strict — use "I built this for my own use, sharing in case useful" framing)
- [ ] **r/opensource** (smaller but more tolerant of self-promo)

### Day 5-6 (Thu-Fri) — Engagement + Product Hunt prep
- [ ] Reply to every comment on all posts
- [ ] Make small follow-up commits if people report issues
- [ ] **Product Hunt** submission — schedule for Tuesday (best day)
  - Maker comment from Sir Raghav (personal account)
  - Tagline: "Browser automation that AI agents actually understand"
  - Topics: AI, Developer Tools, Open Source
  - Submit Friday for Tuesday launch (PH requires 24-48h review)

### Day 7 (2026-07-26, Sun) — Wave 2 content
- [ ] Second X thread with a code walkthrough (recorded demo)
- [ ] Second LinkedIn post with a "what I learned" angle
- [ ] First YouTube video: 5-min "Build with mcpwright" walkthrough
- [ ] Cross-link to dev.to post

---

## Channel mix (priority order, by expected ROI)

| Priority | Channel | Why | Expected stars (7d) | Risk |
|---|---|---|---|---|
| **#1** | **Hacker News (Show HN)** | Highest-quality audience for dev tools. 1 front-page post = 500-2000 stars. | 300-1500 | Self-promo tone = downvotes. Solution: technical, humble, problem-first text. |
| **#2** | **r/Python** | 1.5M+ subs, Show & Tell flair is the standard channel. Honest Python project posts do well. | 100-500 | Mods remove if no flair or pure link. Solution: use flair, paste full text. |
| **#3** | **X thread** | Build-in-public audience loves first-launch stories. Algorithm rewards threads with saves. | 50-300 | Algorithm volatility. Solution: post at peak, use visuals. |
| **#4** | **LinkedIn** | Sir's network (BBA, BI Analyst) will be early supporters. HR/recruiter network amplifies. | 30-150 | Too much self-promo = "LinkedIn cringe." Solution: story-driven, no hype. |
| **#5** | **dev.to** | Long-form audience. Article gets indexed by Google. | 20-100 | Lower virality but high-intent readers. |
| **#6** | **r/LocalLLaMA** | Highly relevant audience (LLM + browser). Niche but high-quality. | 50-200 | Strict on self-promo. Solution: contribute to other threads first. |
| **#7** | **Product Hunt** | Launch-day boost (single day), email digest. | 30-100 | Needs clean assets, maker story. |
| **#8** | **r/AI_Agents** | Tiny but high-intent. | 20-50 | Low ceiling. |
| **#9** | **Lobsters** | Tiny but high-quality. | 5-20 | Invite-only. Skip unless invited. |
| **#10** | **Indie Hackers** | Slight audience mismatch (not dev-tool focused), but good for "learned in public" story. | 5-15 | Low ROI. |

**Conservative estimate:** 600-2,500 stars in 7 days if HN hits front page + 2-3 Reddit posts land.
**Stretch estimate:** 5,000+ stars if HN hits #1 + viral X thread + Product Hunt top 5.

---

## Engagement playbook (first 3 hours after each post)

This is the most under-rated part of OSS promotion. **The first 3 hours decide everything.**

1. **Set a phone alarm** for 2 minutes after posting. Open the post on phone.
2. **Reply to EVERY comment in first 3 hours**, even "nice." Each reply is an engagement signal to the algorithm AND it shows the author cares.
3. **For technical questions**, link to specific code in the repo with line refs. Shows "I built this, I know it inside out."
4. **For "this is just Playwright" comments** (will happen on HN), reply with the specific failure modes mcpwright handles that raw Playwright doesn't. Have the comparison table memorized.
5. **For harsh criticism**, take it on the chin, ask what they'd build differently. Don't argue.
6. **For feature requests**, say "tracked in #<issue>" — even if you create the issue after the reply. Shows you're building, not just promoting.

---

## Visual assets to create (in priority order)

1. **Architecture diagram** (already in `docs/architecture-diagram.svg`)
2. **15-sec demo GIF** — `examples/01_basic_navigate.py` running in real time
3. **Before/After code comparison** — "AI agent crashes" vs "mcpwright handles it"
4. **5-min YouTube walkthrough** — "Build a LinkedIn DM bot in 5 min with mcpwright"
5. **Twitter header image** — "Browser automation for AI agents" with the library name

These should be created in batch on Day 5-6, then attached to the relevant posts.

---

## The "first-100-stars" emergency levers

If Day 3-4 shows weak traction (< 30 stars), trigger these in order:

1. **Ask 3 friends who are devs to star + share** with their network (1-2 per friend = 6-12 stars + 50-100 impressions)
2. **DM 5 people who star similar libraries** with "hey, I built something adjacent, would love your feedback" (don't ask for star, ask for feedback; stars follow)
3. **Post a "v0.1.0 release notes" announcement on X** with the visual demo GIF (separate from the launch thread)
4. **Submit to awesome-python** via PR: https://github.com/vinta/awesome-python — this list gets 100+ daily views
5. **Add a "Show HN"-style banner image to the GitHub repo** so the repo looks alive even if the post doesn't hit

---

## Metrics to track daily

- **Stars** (GitHub API: `gh api repos/raghavsaiassistant-wq/mcpwright | jq .stargazers_count`)
- **Issues opened** (any bug = engagement win)
- **Forks** (indicates actual usage)
- **PyPI download count** (after publish)
- **HN ranking** (if Show HN posted)
- **Reddit upvotes** + **comment count**

Save these daily in `daily_metrics.md` for the launch retrospective.

---

## What success looks like (Day 7)

- [ ] 100+ stars on GitHub
- [ ] 5+ unique issues opened
- [ ] 3+ people tagged the repo in their own projects
- [ ] At least 1 "I used it for X" public testimonial (HN comment, X reply, Reddit comment)
- [ ] PyPI published (or queued)
- [ ] 1+ piece of third-party content (someone wrote about it on their own blog)
- [ ] 5+ X followers gained (from non-bot accounts)

If 5+ of these are true by Day 7, the launch is on track. If < 3, the messaging isn't landing and we need to revisit.

---

*This plan is the default. The research subagent will validate channel rules + add recent examples when it returns. The schedule is loose enough to adjust based on real engagement.*

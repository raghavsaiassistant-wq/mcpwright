# mcpwright — Pitfalls

10 things that will break your agent, and how to fix them.

## 1. ❌ `time.sleep(5)` instead of `smart_wait`

**Symptom:** Race conditions. Sometimes works, sometimes doesn't.
Sometimes the page loads in 1s, sometimes 8s, and your agent is
forever either too early or too late.

**Fix:** Use `smart_wait(send, recv, "selector_present", selector=..., timeout=20)`.
It polls the page until the condition is met (or timeout).

## 2. ❌ Setting `el.value = "..."` for React inputs

**Symptom:** Text appears in the input, but the form's Submit button
stays disabled. Nothing happens. Agent is stuck.

**Why:** React listens to native keyboard events, not direct value
assignment. The DOM has "hello" but React's internal state is empty.

**Fix:** Use `react_aware_type(send, recv, selector, text)`. It uses
real keyboard input, so React's state syncs correctly.

## 3. ❌ Clicking before the page is ready

**Symptom:** "Element not found" or "Element not clickable" errors.

**Fix:** After every navigate, do `smart_wait` for the element you need.
Don't trust the immediate return of `browser_navigate`.

## 4. ❌ Same profile open in another browser

**Symptom:** "Profile is locked" or "Cannot create user data directory".

**Fix:** Close all Chrome windows before running mcpwright. Or use a
separate profile (copy your existing one to a new dir).

## 5. ❌ No retry on transient errors

**Symptom:** One network blip and your whole flow dies.

**Fix:** Wrap critical calls in `retry(...)`. Default: 3 attempts with
exponential backoff.

## 6. ❌ Typing too fast

**Symptom:** Site detects you as a bot, blocks you, or shows CAPTCHA.

**Fix:** Tune `char_delay_ms`:
- Most modern sites: 30-50ms
- Anti-bot sensitive sites: 80-150ms
- Internal tools: 0-20ms

When in doubt, err on the side of "looks human".

## 7. ❌ Hardcoded credentials in scripts

**Symptom:** Your email/password/token ends up in git history forever.

**Fix:** 
- Use `mcpwright.json` (add to `.gitignore`!) for non-secret config
- Use environment variables for secrets: `os.environ["MY_PASSWORD"]`
- Never commit `.env` files

## 8. ❌ Not verifying after actions

**Symptom:** Agent thinks it clicked Submit, but nothing actually
submitted. Loop runs 10 times silently doing nothing.

**Fix:** After every important action, verify:
- Did the URL change? (`smart_wait(..., "url_contains", ...)`)
- Is a new element now present?
- Take a screenshot and inspect it (when stuck)

## 9. ❌ Bulk actions without pacing

**Symptom:** Site rate-limits you, blocks your account, or bans your IP.

**Fix:**
- `time.sleep(3)` between bulk actions
- For LinkedIn-style sites: max 5-10 actions per hour from one account
- Rotate accounts / IPs only as a last resort (against ToS)

## 10. ❌ Trusting the first response

**Symptom:** MCP returns "OK" but the action didn't actually do what
you wanted.

**Fix:** Always check the response. mcpwright's `recv()` returns `None`
on timeout — treat that as a failure. Parse the response content and
look for error indicators.

## Bonus: The 5-minute debugging checklist

When your agent is broken, check in this order:

1. **Did the browser actually load?** Take a screenshot.
2. **Did smart_wait succeed?** Print the boolean it returned.
3. **Was the element found?** Use `browser_evaluate` to run
   `document.querySelectorAll('your-selector').length` and see.
4. **Did the click register?** After clicking, check if the expected
   post-click element is now present.
5. **Is the MCP server still alive?** Check the process. If it's gone,
   look at the stderr for the actual error.

If you get stuck, open an issue with:
- The OS / Python version
- The exact code (sanitize credentials first)
- The full error message
- A screenshot, if visual

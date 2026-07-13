# mcpwright — Architecture

This document explains the 4 layers of mcpwright and how they fit together.

## The 4 layers

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: YOUR AI AGENT                                      │
│   GPT-4, Claude, Llama, or any LLM with function-calling    │
│                                                              │
│   The agent thinks in natural language. It doesn't need to   │
│   know about Playwright, MCP, or browsers. It just sends     │
│   "intent" — what it wants to happen.                        │
│                                                              │
│   Example intent:                                            │
│     "Log in to LinkedIn and send 5 recruiters a message"    │
│     "Apply to the first 10 jobs on this page"                │
│     "Extract all job titles and companies"                   │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │  Natural-language intent
                           │  OR direct MCP tool calls
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: mcpwright (this library)                           │
│   Python — the missing layer between agents and browsers    │
│                                                              │
│   Responsibilities:                                          │
│   • Translate intent into specific MCP tool calls           │
│   • Smart waits (waits for state, not DOM)                  │
│   • Real keyboard typing (so React's state updates)         │
│   • Selector fallback (3+ strategies to find each element)  │
│   • Auto-retry with exponential backoff                     │
│   • Rate-limit aware pacing                                 │
│   • Visual + DOM verification after every action            │
│   • Cross-platform npx + profile path resolution            │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │  JSON-RPC 2.0 over stdio
                           │  (newline-delimited JSON messages)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: Playwright MCP Server                              │
│   @playwright/mcp@latest (Microsoft / Anthropic)           │
│                                                              │
│   A Node.js process that exposes 23 browser-control tools   │
│   over the Model Context Protocol (MCP). mcpwright launches │
│   it as a subprocess and talks to it via stdin/stdout.     │
│                                                              │
│   This layer handles the actual low-level browser control:  │
│   navigate, click, type, screenshot, etc.                   │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │  Chrome DevTools Protocol (CDP)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Your actual browser                                │
│   Chrome / Edge / Firefox with your saved profile          │
│                                                              │
│   Because the browser is real — with your cookies, your     │
│   saved logins, your usual fingerprints — the websites      │
│   treat you as a real user, not a bot.                      │
└─────────────────────────────────────────────────────────────┘
```

## Why this layering?

**Each layer does one thing well.** That's the design.

If you wanted to swap Playwright for a different browser framework, you'd
swap Layer 3 only. If you wanted to talk to a different LLM, you'd swap
Layer 1 only. **mcpwright is Layer 2 — the orchestration layer that makes
the rest play nicely together.**

## Why the missing layer exists

Playwright is great. Playwright + MCP is great. But out of the box, both
were built for **test automation** — humans writing scripts.

When an AI agent uses them, it hits a wall of problems that humans don't
hit:

1. **The agent types too fast.** Real humans have ~30-50ms between
   keystrokes. Agents type in 0ms. Sites detect this.
2. **The agent clicks before the page is ready.** Humans visually
   confirm before clicking. Agents don't.
3. **The agent types into `<div>`s for React inputs.** Setting
   `el.value = "..."` doesn't update React's internal state, so the form's
   "Submit" button stays disabled.
4. **The agent uses one selector.** If `button.submit` is wrong, it fails.
   Humans try `button[type='submit']`, `form#x button`, etc.

**mcpwright is the layer that fixes all of these.** The 3 helpers
(`smart_wait`, `react_aware_type`, `retry`) cover 90% of what AI agents
need.

## The MCP protocol in 30 seconds

MCP is a JSON-RPC 2.0 protocol. You send messages like:

```json
{"jsonrpc": "2.0", "id": 1, "method": "tools/call",
 "params": {"name": "browser_navigate",
            "arguments": {"url": "https://example.com"}}}
```

…and get responses like:

```json
{"jsonrpc": "2.0", "id": 1, "result": {
    "content": [{"type": "text", "text": "Loaded https://example.com"}]
}}
```

mcpwright wraps this in two helpers:

- `send(message)` — write a message to the MCP subprocess's stdin
- `recv(timeout)` — read one response from the subprocess's stdout

That's it. The rest is composing these into workflows.

See [`docs/mcp-tools.md`](mcp-tools.md) for the full list of tools you can
call.

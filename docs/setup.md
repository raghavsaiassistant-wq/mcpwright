# mcpwright — Setup

Get mcpwright running on your machine in ~5 minutes.

## Prerequisites

1. **Python 3.8+**
   ```bash
   python --version
   ```

2. **Node.js 18+** (so `npx` is available)
   ```bash
   npx --version
   ```
   If not installed, get it from [nodejs.org](https://nodejs.org/).

3. **Chrome, Edge, or Firefox** installed at the default location

## Step 1 — Install mcpwright

From PyPI (when published):
```bash
pip install mcpwright
```

For now, install from source:
```bash
git clone https://github.com/<owner>/mcpwright.git
cd mcpwright
pip install -e .
```

## Step 2 — Verify Playwright MCP works

```bash
npx -y @playwright/mcp@latest --help
```

You should see a help screen. If you get a "command not found" error,
your Node.js isn't installed correctly.

### Windows-specific: npx path

On Windows, plain `npx` doesn't work in subprocess. mcpwright handles
this automatically — it'll look for `npx.cmd` in your PATH. The most
common location is `C:\nvm4w\nodejs\npx.cmd`.

If you have multiple Node.js installations, set `NPX_PATH` env var:
```bash
# Windows (PowerShell)
$env:NPX_PATH = "C:\path\to\npx.cmd"

# macOS / Linux
export NPX_PATH=/usr/local/bin/npx
```

## Step 3 — Point mcpwright at your browser profile

mcpwright uses your real browser (with your saved logins). Find your
Chrome profile:

| OS | Typical location |
|---|---|
| Windows | `C:\Users\<YOU>\AppData\Local\Google\Chrome\User Data` |
| macOS | `~/Library/Application Support/Google/Chrome` |
| Linux | `~/.config/google-chrome` |

**Close Chrome first** (or mcpwright won't be able to use the profile).

Create `mcpwright.json` in your project root:
```json
{
  "profile_path": "/full/path/to/your/chrome/profile",
  "browser": "chrome"
}
```

Or pass it directly:
```python
from mcpwright import browser_session

with browser_session(profile_path="/full/path/to/profile") as (send, recv):
    ...
```

## Step 4 — Run an example

```bash
git clone https://github.com/<owner>/mcpwright.git
cd mcpwright/examples
# Edit 01_basic_navigate.py — set PROFILE_PATH
python 01_basic_navigate.py
```

You should see Chrome open, navigate to example.com, take a screenshot,
and close.

## Step 5 — Wire it into your agent

Pass mcpwright to your agent as a function-calling tool. Most modern
LLM SDKs make this easy. Example with OpenAI:

```python
import openai
from mcpwright import browser_session

def browse(url: str) -> str:
    """Visit a URL and return the visible text content."""
    with browser_session(profile_path="<YOUR_PROFILE>") as (send, recv):
        send({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
              "params": {"name": "browser_navigate",
                         "arguments": {"url": url}}})
        recv()
        send({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
              "params": {"name": "browser_snapshot",
                         "arguments": {}}})
        resp = recv()
        return resp.get("result", {}).get("content", [{}])[0].get("text", "")

client = openai.OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    tools=[{
        "type": "function",
        "function": {
            "name": "browse",
            "description": "Visit a URL in a real browser and return its text.",
            "parameters": {
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"]
            }
        }
    }],
    messages=[{"role": "user", "content": "What's on the mcpwright README?"}]
)
# ... handle tool calls
```

See [`docs/workflows.md`](workflows.md) for more patterns.

## Troubleshooting

### "npx is not recognized" (Windows)
Add Node.js to your PATH or set `NPX_PATH` env var.

### "Profile is locked"
Another Chrome instance is using the same profile. Close all Chrome
windows first.

### "Browser launches but commands time out"
The MCP server takes 5-15s to start. Increase `default_timeout` in your
config or wrap calls in `retry()`.

### "Sites detect me as a bot"
Slow down. Use `char_delay_ms: 80-120` for sensitive sites. See
[`docs/pitfalls.md`](pitfalls.md) for the full list of anti-detection
tips.

### Still stuck?
Open an issue on GitHub with the full error message and your OS / Python
version.

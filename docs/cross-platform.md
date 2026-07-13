# mcpwright — Cross-platform notes

mcpwright works on Windows, WSL2, Linux, and macOS. The Python code is
identical. Only two things change between platforms:

1. The path to `npx` (or `npx.cmd` on Windows)
2. The path to your browser profile directory

## Platform matrix

| Platform | npx path | Default Chrome profile |
|---|---|---|
| **Windows 10/11** | `C:\nvm4w\nodejs\npx.cmd` (or wherever you installed Node) | `C:\Users\<YOU>\AppData\Local\Google\Chrome\User Data` |
| **WSL2 (Ubuntu)** | `/usr/bin/npx` (auto-resolved) | `~/.config/google-chrome` (you must copy from Windows) |
| **Linux native** | `/usr/bin/npx` (auto-resolved) | `~/.config/google-chrome` |
| **macOS** | `/usr/local/bin/npx` (or Homebrew location) | `~/Library/Application Support/Google/Chrome` |

mcpwright's `_resolve_npx()` helper handles the npx path automatically:

```python
def _resolve_npx():
    if os.name == "nt":  # Windows
        npx_cmd = shutil.which("npx.cmd")
        if npx_cmd:
            return npx_cmd
    return shutil.which("npx") or "npx"
```

## WSL2 specifics

WSL2 has two quirks:

1. **Microsoft datacenter IP.** LinkedIn and some other sites may flag
   requests from WSL2's IP range. If you hit rate limits, run mcpwright
   on the Windows host (using the same Python code) or use a residential
   proxy.

2. **Profile path.** Your Chrome profile lives in Windows, not WSL2. To
   use it from WSL2, either:
   - **Copy it** (faster, but stale): `cp -r /mnt/c/Users/<you>/AppData/Local/Google/Chrome/User Data ~/.config/google-chrome`
   - **Symlink it** (live, but Windows-side changes propagate): `ln -s /mnt/c/Users/<you>/AppData/Local/Google/Chrome/User Data ~/.config/google-chrome`

For LinkedIn and similar, **running on Windows** is recommended.

## macOS specifics

- Chrome is typically at `/Applications/Google Chrome.app`
- The MCP server should find it automatically via the system path
- If you get "browser not found" errors, install Chrome from [google.com/chrome](https://google.com/chrome)

## Linux specifics

- You may need to install Chromium first: `npx playwright install chromium`
- For headless operation: add `--headless` to the MCP server command (mcpwright
  doesn't currently expose this, but you can patch `core/session.py` to add it)

## Verifying your setup

Run the smoke test:

```bash
python scripts/smoke_test.sh
```

It will:
1. Check Python version
2. Check Node.js / npx
3. Check Chrome is installed
4. Try to launch a session and navigate to example.com

If it works, you'll see:
```
✓ Python 3.11
✓ Node 20.x
✓ Chrome found
✓ MCP server started
✓ Navigated to example.com
✓ All checks passed
```

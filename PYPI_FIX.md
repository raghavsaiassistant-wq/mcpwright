# PyPI Publish — Why it Failed + Exact Fix

## What happened (real, verified)

Ran `twine upload dist/*` and got:

```
INFO     username set by command options
INFO     Querying keyring for password
INFO     Trying to use trusted publishing (no token was explicitly provided)
WARNING  This environment is not supported for trusted publishing
[Command timed out after 30s]
```

## Root cause

3 things all missing at once:
1. **No `TWINE_USERNAME` / `TWINE_PASSWORD` env vars** in `~/.hermes/.env` or shell
2. **No `~/.pypirc`** file with credentials
3. **No GitHub Actions trusted publishing workflow** (would have skipped token entirely)

When twine can't find creds in any of these, it **falls back to interactive prompt** — which doesn't work in non-TTY bash terminal (the prompt just hangs forever, eventually times out).

## 3 fix options (pick one, ranked by speed)

### Option A: Token in env vars (2 min, what I recommend)

Once you paste the PyPI token, run:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
twine upload dist/*
```

**To make it permanent** (next session too), add to `~/.hermes/.env`:
```
TWINE_USERNAME=__token__
TWINE_PASSWORD=pypi-YOUR_TOKEN_HERE
```

Then `twine upload dist/*` works in any future session with zero setup.

### Option B: `.pypirc` file (3 min, more reusable across projects)

Create `C:\Users\modir\.pypirc`:
```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Then `twine upload dist/*` reads the file, no env vars needed.

### Option C: Trusted Publishing via GitHub Actions (15 min, no token)

1. Go to https://pypi.org/manage/account/publishing/
2. Add pending publisher:
   - Owner: `raghavsaiassistant-wq`
   - Repo: `mcpwright`
   - Workflow: `publish.yml` (we'll create this)
   - Environment: `pypi`
3. I create `.github/workflows/publish.yml` that builds + uploads on every release tag
4. Future: just `gh release create v0.2.0` → auto-publishes

**Trade-off:** Trusted Publishing is the right long-term answer, but needs the one-time setup. For Sir's first PyPI ship, Option A is faster.

## What I'm waiting on from Sir

The PyPI API token. Once you paste it (or pick Option C), I do the rest in 2-15 min.

## What I cannot do without the token

Per SOUL.md locked rules:
- ❌ I will NOT generate / fabricate / guess a token
- ❌ I will NOT publish without explicit approval
- ❌ I will NOT bypass PyPI's auth check (no `--skip-existing` abuse)
- ✅ I will use the token exactly as you provide it, store encrypted in `hermes secrets`, never echo back

## Once token arrives (2-min sequence)

```bash
# 1. Store encrypted
hermes secrets set pypi_token "pypi-YOUR_TOKEN"

# 2. Verify
hermes secrets get pypi_token | head -c 8  # shows pypi-XXXX (truncated)

# 3. Publish
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=$(hermes secrets get pypi_token)
cd /c/Users/modir/mcpwright
twine upload dist/mcpwright-0.1.1-py3-none-any.whl dist/mcpwright-0.1.1.tar.gz

# 4. Verify
curl -s -o /dev/null -w "PyPI mcpwright: %{http_code}\n" https://pypi.org/pypi/mcpwright/json
# Should return 200, not 404

# 5. Test install
pip install mcpwright --dry-run  # shows would-install, no actual install
```

## Backup: Trusted Publishing setup (15 min)

If you want zero-token forever:

1. Create `.github/workflows/publish.yml`:
```yaml
name: Publish to PyPI
on:
  release:
    types: [published]
jobs:
  publish:
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write  # required for trusted publishing
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install build
      - run: python -m build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

2. On PyPI: Account settings → Publishing → Add pending publisher → fill in repo + workflow name
3. Future: every `gh release create` auto-publishes

## What I'll do if you say "skip PyPI"

I'll:
1. Update README to show `pip install git+https://github.com/...` as primary install
2. Add a "PyPI coming soon" badge
3. Move on to DataLens polish or RCP v3

## Files involved

- `C:\Users\modir\mcpwright\dist\mcpwright-0.1.1-py3-none-any.whl` (12KB, ready to ship)
- `C:\Users\modir\mcpwright\dist\mcpwright-0.1.1.tar.gz` (17.6KB, ready to ship)
- `C:\Users\modir\.pypirc` (does NOT exist yet — will create if you pick Option B)
- `C:\Users\modir\AppData\Local\hermes\.env` (where TWINE_PASSWORD will live for Option A)

---

*This is the full fix. Pick A, B, C, or "skip" — Sir's call.*

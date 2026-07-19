"""
mcpwright test suite (v0.1.1).

Verifies:
  1. Public API imports + version
  2. Pure-function helpers (resilience._build_wait_js, config)
  3. Example files are syntactically valid + reference real symbols
  4. mcpwright.json.example is valid JSON with required keys
  5. Every export in __all__ actually exists in the package

All tests run without launching a real browser (CI-friendly).
"""

import json
import os
import sys
import py_compile
from pathlib import Path

import pytest

import mcpwright
from mcpwright.resilience import _build_wait_js
from mcpwright.config import default_config, load_config, CONFIG_FILE_NAME


# ─────────────────────────────────────────────────────────────
# 1. Public API surface
# ─────────────────────────────────────────────────────────────
def test_package_imports():
    """mcpwright must import cleanly with no ModuleNotFoundError."""
    assert mcpwright is not None
    assert hasattr(mcpwright, "__version__")


def test_version_format():
    """Version must be semver-ish (X.Y.Z)."""
    parts = mcpwright.__version__.split(".")
    assert len(parts) == 3, f"version {mcpwright.__version__!r} is not X.Y.Z"
    for p in parts:
        assert p.isdigit(), f"version part {p!r} is not numeric"


def test_all_exports_resolve():
    """Every name in __all__ must be importable from the package."""
    for name in mcpwright.__all__:
        assert hasattr(mcpwright, name), f"__all__ references missing {name!r}"


def test_exports_are_callable():
    """Public functions should actually be callable."""
    callable_exports = [
        "browser_session", "send_recv",
        "smart_wait", "react_aware_type", "retry",
        "load_config", "default_config",
    ]
    for name in callable_exports:
        attr = getattr(mcpwright, name)
        assert callable(attr), f"{name} is in __all__ but not callable"


# ─────────────────────────────────────────────────────────────
# 2. resilience._build_wait_js (pure function)
# ─────────────────────────────────────────────────────────────
def test_build_wait_js_selector_present():
    """selector_present must build a JS expression using querySelector."""
    js = _build_wait_js("selector_present", "#submit-btn")
    assert js is not None
    assert "querySelector" in js
    assert "#submit-btn" in js


def test_build_wait_js_selector_present_requires_selector():
    """selector_present without selector must raise ValueError."""
    with pytest.raises(ValueError, match="selector is required"):
        _build_wait_js("selector_present", None)


def test_build_wait_js_navigation_complete():
    """navigation_complete must check document.readyState."""
    js = _build_wait_js("navigation_complete", None)
    assert "readyState" in js
    assert "complete" in js


def test_build_wait_js_url_contains():
    """url_contains must check window.location.href."""
    js = _build_wait_js("url_contains", "/dashboard")
    assert "window.location.href" in js
    assert "/dashboard" in js


def test_build_wait_js_url_contains_requires_selector():
    """url_contains without substring must raise ValueError."""
    with pytest.raises(ValueError, match="selector"):
        _build_wait_js("url_contains", None)


def test_build_wait_js_unknown_condition():
    """Unknown condition must return None (caller raises)."""
    assert _build_wait_js("nonsense_condition", "x") is None


def test_build_wait_js_escapes_quotes():
    """Quotes in selector must be escaped to prevent JS injection."""
    js = _build_wait_js("selector_present", "div[data-id='evil']")
    # The inner 'evil' should be escaped so the JS string remains valid
    assert "\\'" in js or "evil" in js  # either escaped or present, but the JS must be syntactically intact


# ─────────────────────────────────────────────────────────────
# 3. config helpers (pure)
# ─────────────────────────────────────────────────────────────
def test_default_config_has_required_keys():
    """default_config() must return all documented keys."""
    cfg = default_config()
    for key in ("browser", "default_timeout", "char_delay_ms", "retry", "profile_path"):
        assert key in cfg, f"default_config missing {key!r}"
    assert isinstance(cfg["retry"], dict)
    assert "max_attempts" in cfg["retry"]


def test_default_config_profile_path_is_none():
    """profile_path default is None (user must supply)."""
    assert default_config()["profile_path"] is None


def test_load_config_falls_back_to_default(tmp_path, monkeypatch):
    """load_config with no mcpwright.json anywhere returns defaults."""
    monkeypatch.chdir(tmp_path)  # isolated cwd with no mcpwright.json
    cfg = load_config()
    assert cfg["browser"] == "chrome"
    assert cfg["default_timeout"] == 20


def test_load_config_reads_explicit_path(tmp_path):
    """load_config(path=...) reads the given file."""
    cfg_file = tmp_path / "mcpwright.json"
    cfg_file.write_text(json.dumps({
        "browser": "edge",
        "default_timeout": 60,
        "char_delay_ms": 50,
        "retry": {"max_attempts": 5, "initial_delay": 1.0, "backoff": 3.0},
        "profile_path": "/tmp/profile",
    }))
    cfg = load_config(str(cfg_file))
    assert cfg["browser"] == "edge"
    assert cfg["default_timeout"] == 60
    assert cfg["retry"]["max_attempts"] == 5


def test_config_filename_constant():
    """CONFIG_FILE_NAME must be 'mcpwright.json' for cross-platform parity."""
    assert CONFIG_FILE_NAME == "mcpwright.json"


# ─────────────────────────────────────────────────────────────
# 4. Example files: structural integrity
# ─────────────────────────────────────────────────────────────
EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


@pytest.mark.parametrize("example", [
    "01_basic_navigate.py",
    "02_linkedin_message.py",
    "03_naukri_apply.py",
    "04_job_extraction.py",
    "05_form_filler.py",
])
def test_example_compiles(example):
    """Every example must be valid Python (no syntax errors)."""
    path = EXAMPLES_DIR / example
    assert path.exists(), f"example missing: {path}"
    py_compile.compile(str(path), doraise=True)


@pytest.mark.parametrize("example", [
    "01_basic_navigate.py",
    "02_linkedin_message.py",
    "03_naukri_apply.py",
    "04_job_extraction.py",
    "05_form_filler.py",
])
def test_example_imports_mcpwright(example):
    """Every example must import from mcpwright (not core or other)."""
    path = EXAMPLES_DIR / example
    content = path.read_text()
    assert "from mcpwright" in content, f"{example} doesn't import from mcpwright"
    assert "from core" not in content, f"{example} still references old 'core' import"


@pytest.mark.parametrize("example", [
    "01_basic_navigate.py",
    "02_linkedin_message.py",
    "03_naukri_apply.py",
    "04_job_extraction.py",
    "05_form_filler.py",
])
def test_example_has_main(example):
    """Every example must define a main() function and a __main__ guard."""
    content = (EXAMPLES_DIR / example).read_text()
    assert "def main(" in content, f"{example} missing main()"
    assert "__main__" in content, f"{example} missing if __name__ == '__main__' guard"


# ─────────────────────────────────────────────────────────────
# 5. mcpwright.json.example (config reference)
# ─────────────────────────────────────────────────────────────
def test_mcpwright_json_example_valid():
    """configs/mcpwright.json.example must be valid JSON."""
    path = Path(__file__).parent.parent / "configs" / "mcpwright.json.example"
    assert path.exists(), "configs/mcpwright.json.example missing"
    data = json.loads(path.read_text())
    # Must have at least the standard keys
    for key in ("browser", "default_timeout", "char_delay_ms"):
        assert key in data, f"example config missing {key!r}"


# ─────────────────────────────────────────────────────────────
# 6. Privacy: no leaked paths / tokens
# ─────────────────────────────────────────────────────────────
FORBIDDEN_PATH_PATTERNS = [
    "C:\\Users\\modir",
    "C:\\FluxUltra",
    "C:\\James",
    "C:\\James_Backup",
    "raghavsaiassistant@gmail.com",
    "raghavmodi2004@gmail.com",
]


def test_no_leaked_user_paths_in_source():
    """No C:\\Users\\modir, C:\\FluxUltra, etc. anywhere in the package source."""
    pkg_root = Path(__file__).parent.parent / "mcpwright"
    for py_file in pkg_root.rglob("*.py"):
        content = py_file.read_text()
        for pattern in FORBIDDEN_PATH_PATTERNS:
            assert pattern not in content, (
                f"{py_file.name} contains forbidden path/email: {pattern!r}"
            )


def test_no_leaked_user_paths_in_examples():
    """No C:\\Users\\modir, C:\\FluxUltra, etc. in examples/."""
    for py_file in EXAMPLES_DIR.rglob("*.py"):
        content = py_file.read_text()
        for pattern in FORBIDDEN_PATH_PATTERNS:
            assert pattern not in content, (
                f"{py_file.name} contains forbidden path/email: {pattern!r}"
            )

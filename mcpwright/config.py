"""
mcpwright.config — Config loading and defaults.

Reads from `mcpwright.json` (if present) or returns sensible defaults.
"""

import json
import os
from pathlib import Path


CONFIG_FILE_NAME = "mcpwright.json"


def default_config() -> dict:
    """
    Return a default config.

    Override any field by creating `mcpwright.json` in your project root
    or by passing values to `load_config()`.
    """
    return {
        "browser": "chrome",
        "default_timeout": 20,
        "char_delay_ms": 30,
        "retry": {
            "max_attempts": 3,
            "initial_delay": 2.0,
            "backoff": 2.0,
        },
        "profile_path": None,  # MUST be supplied by user, see docs/setup.md
    }


def load_config(path: str = None) -> dict:
    """
    Load config from `mcpwright.json`.

    Search order:
      1. Explicit `path` argument
      2. ./mcpwright.json (current directory)
      3. ~/.mcpwright.json (home directory)
      4. Built-in defaults
    """
    cfg = default_config()

    candidates = []
    if path:
        candidates.append(path)
    candidates.append(os.path.join(os.getcwd(), CONFIG_FILE_NAME))
    home = str(Path.home())
    candidates.append(os.path.join(home, f".{CONFIG_FILE_NAME}"))

    for candidate in candidates:
        if os.path.exists(candidate):
            with open(candidate, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
            # Shallow merge — user values win
            cfg.update(user_cfg)
            return cfg

    return cfg

"""
mcpwright — Browser automation that AI agents actually understand.

Playwright + MCP for LLM-driven browser control. Survives React,
lazy-loads, rate limits, and all the things that break naive agents.
"""

__version__ = "0.1.1"
__author__ = "Raghav Modi"

from mcpwright.session import browser_session, send_recv
from mcpwright.resilience import smart_wait, react_aware_type, retry
from mcpwright.config import load_config, default_config

__all__ = [
    "browser_session",
    "send_recv",
    "smart_wait",
    "react_aware_type",
    "retry",
    "load_config",
    "default_config",
    "__version__",
]

"""mcpwright — Browser automation that AI agents actually understand."""

__version__ = "0.1.0"
__author__ = "Raghav Modi"
__license__ = "MIT"

from core.session import browser_session, send_recv
from core.resilience import smart_wait, react_aware_type, retry
from core.config import load_config, default_config

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

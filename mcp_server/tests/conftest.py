"""Ensure mcp_server and the Python SDK package are importable from any CWD."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_MCP = Path(__file__).resolve().parent.parent
for path in (_MCP, _ROOT / "python"):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

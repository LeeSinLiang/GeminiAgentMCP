
"""This module contains utility functions for the MCP server."""

import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

def is_safe_path(path: str) -> bool:
    """Check if the path is within the project directory."""
    abs_path = os.path.abspath(path)
    return os.path.commonprefix([abs_path, PROJECT_ROOT]) == PROJECT_ROOT

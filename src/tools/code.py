"""This module contains the code-related tools for the MCP server."""

import logging
import subprocess
from mcp_instance import mcp
from .gemini import call_gemini
from .utils import is_safe_path

logger = logging.getLogger(__name__)

@mcp.tool
def lint_code(file_path: str, language: str) -> dict:
    """Lints a Python or JavaScript file and returns a report of issues."""
    logger.info("Executing lint_code for file: %s (%s)", file_path, language)
    if not is_safe_path(file_path):
        logger.warning("Attempted to access unsafe path: %s", file_path)
        raise ValueError(f"Access to path '{file_path}' is not allowed.")

    if language == "python":
        linter_command = ["pylint", file_path]
    elif language == "javascript":
        linter_command = ["eslint", file_path]
    else:
        logger.warning("Unsupported language for lint_code: %s", language)
        raise ValueError(
            f"Unsupported language: {language}. Supported languages are 'python' and 'javascript'."
        )

    try:
        result = subprocess.run(
            linter_command, capture_output=True, text=True, check=False, encoding='utf-8')
        logger.info("lint_code for %s executed successfully.", file_path)
        return {"linting_report": result.stdout}
    except FileNotFoundError as exc:
        logger.error("'%s' command not found.", linter_command[0])
        raise ValueError(
            f"'{linter_command[0]}' command not found. "
            f"Make sure the linter is installed and in your PATH."
        ) from exc
    except Exception as exc:
        logger.error("An unexpected error occurred in lint_code: %s", exc)
        raise RuntimeError(f"An unexpected error occurred: {exc}") from exc

@mcp.tool
def generate_unit_tests(file_path: str, item_name: str) -> dict:
    """Generates unit tests for a given function or class in a file."""
    logger.info(
        "Executing generate_unit_tests for item '%s' in file: %s", item_name, file_path)
    if not is_safe_path(file_path):
        logger.warning("Attempted to access unsafe path: %s", file_path)
        raise ValueError(f"Access to path '{file_path}' is not allowed.")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
    except FileNotFoundError as exc:
        logger.error("File not found: %s", file_path)
        raise FileNotFoundError(f"File not found: {file_path}") from exc
    except Exception as exc:
        logger.error("Error reading file %s: %s", file_path, exc)
        raise IOError(f"Error reading file {file_path}: {exc}") from exc

    prompt = (
        f"Generate unit tests for the function or class '{item_name}' in the following code:"
        f"\n\n```\n{file_content}\n```"
    )
    return call_gemini(prompt)

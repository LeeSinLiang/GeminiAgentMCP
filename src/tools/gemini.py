"""This module contains the Gemini-related tools for the MCP server."""

import logging
import subprocess
from src.mcp_instance import mcp

logger = logging.getLogger(__name__)

@mcp.tool
def call_gemini(prompt: str, context: str = '') -> dict:
    """Calls the Gemini CLI with a given prompt and context."""
    logger.info("Executing call_gemini with prompt: '%s...'")
    full_prompt = f"{context}\n\n{prompt}"
    try:
        result = subprocess.run(
            ['gemini', full_prompt], capture_output=True, text=True, check=True, encoding='utf-8')
        logger.info("call_gemini executed successfully.")
        return {"response": result.stdout}
    except FileNotFoundError as exc:
        logger.error("'gemini' command not found.")
        raise ValueError(
            "'gemini' command not found. Make sure the Gemini CLI is installed and in your PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        logger.error("Error calling Gemini CLI: %s", exc.stderr)
        raise RuntimeError(f"Error calling Gemini CLI: {exc.stderr}") from exc
    except Exception as exc:
        logger.error("An unexpected error occurred in call_gemini: %s", exc)
        raise RuntimeError(f"An unexpected error occurred: {exc}") from exc

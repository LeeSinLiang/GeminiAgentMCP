"""This module contains the documentation-related tools for the MCP server."""

import logging
from .gemini import call_gemini
from .utils import is_safe_path

logger = logging.getLogger(__name__)

def summarize_docs(files: list) -> dict:
    """Summarizes the content of a list of documentation files."""
    logger.info("Executing summarize_docs for files: %s", files)
    all_docs_content = ""
    for file_path in files:
        if not is_safe_path(file_path):
            logger.warning("Attempted to access unsafe path: %s", file_path)
            raise ValueError(f"Access to path '{file_path}' is not allowed.")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                all_docs_content += file.read() + "\n\n"
        except FileNotFoundError as exc:
            logger.error("File not found: %s", file_path)
            raise FileNotFoundError(f"File not found: {file_path}") from exc
        except Exception as exc:
            logger.error("Error reading file %s: %s", file_path, exc)
            raise IOError(f"Error reading file {file_path}: {exc}") from exc

    if not all_docs_content:
        logger.warning("No content found in the provided files for summarize_docs.")
        raise ValueError("No content found in the provided files.")

    prompt = f"Please summarize the following documentation:\n\n{all_docs_content}"
    return call_gemini(prompt)

def generate_docstrings(file_path: str) -> dict:
    """Generates docstrings for functions or classes in a given file."""
    logger.info("Executing generate_docstrings for file: %s", file_path)
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
        "Add docstrings to all functions and classes in the following code that are missing them. "
        "Return the full, updated code inside a single code block.:\n\n"
        f"```\n{file_content}\n```"
    )
    return call_gemini(prompt)
"""This module implements a Model Context Protocol (MCP) server for Gemini Agent."""

import os
import logging
import uvicorn
from mcp.server.fastmcp import FastMCP
from tools.gemini import call_gemini
from tools.docs import summarize_docs, generate_docstrings
from tools.code import lint_code, generate_unit_tests
from tools.dependencies import analyze_dependencies
from tools.github import create_github_issue, create_github_pr

# --- Logging Configuration ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- App Configuration ---
app = FastMCP(
    tools=[
        call_gemini,
        summarize_docs,
        generate_docstrings,
        lint_code,
        generate_unit_tests,
        analyze_dependencies,
        create_github_issue,
        create_github_pr,
    ]
)

if __name__ == '__main__':
    port = int(os.environ.get('MCP_PORT', 5001))
    logger.info("Starting MCP server on port %s", port)
    uvicorn.run(app, host="0.0.0.0", port=port)
"""This module implements a Model Context Protocol (MCP) server for Gemini Agent."""

import os
import logging
from flask import Flask, jsonify
from flask_jsonrpc import JSONRPC
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
app = Flask(__name__)
jsonrpc = JSONRPC(app, '/jsonrpc', enable_web_browsable_api=True)

# --- MCP Manifest ---
@app.route('/mcp', methods=['GET'])
def mcp_manifest():
    """
    Provides the MCP manifest, which describes the tools available on this server.
    """
    logger.info("MCP manifest requested.")
    manifest = {
        "mcp_version": "1.0",
        "tools": [
            {
                "name": "call_gemini",
                "description": (
                    "Calls the Gemini CLI with a given prompt and context "
                    "to get a response from the model."
                ),
                "inputs": {
                    "prompt": {
                        "type": "string",
                        "required": True,
                        "description": "The main input/question for the Gemini model."
                    },
                    "context": {
                        "type": "string",
                        "required": False,
                        "description": "Additional context for the model."
                    }
                },
                "outputs": {
                    "response": {
                        "type": "string",
                        "description": "The response from the Gemini model."
                    }
                }
            },
            {
                "name": "summarize_docs",
                "description": "Summarizes the content of a list of documentation files.",
                "inputs": {
                    "files": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "required": True,
                        "description": "A list of absolute paths to the documentation files."
                    }
                },
                "outputs": {
                    "summary": {
                        "type": "string",
                        "description": "The summary of the documentation."
                    }
                }
            },
            {
                "name": "lint_code",
                "description": "Lints a Python or JavaScript file and returns a report of issues.",
                "inputs": {
                    "file_path": {
                        "type": "string",
                        "required": True,
                        "description": "The absolute path to the file to lint."
                    },
                    "language": {
                        "type": "string",
                        "required": True,
                        "description": "The language of the file, either 'python' or 'javascript'."
                    }
                },
                "outputs": {
                    "linting_report": {
                        "type": "string",
                        "description": "The report from the linter."
                    }
                }
            },
            {
                "name": "analyze_dependencies",
                "description": (
                    "Analyzes a dependency file (e.g., requirements.txt, package.json) "
                    "and provides a summary of each dependency."
                ),
                "inputs": {
                    "file_path": {
                        "type": "string",
                        "required": True,
                        "description": "The absolute path to the dependency file."
                    }
                },
                "outputs": {
                    "dependency_report": {
                        "type": "object",
                        "description": "A JSON object with a summary of each dependency."
                    }
                }
            },
            {
                "name": "generate_unit_tests",
                "description": "Generates unit tests for a given function or class in a file.",
                "inputs": {
                    "file_path": {
                        "type": "string",
                        "required": True,
                        "description": "The absolute path to the file containing the code."
                    },
                    "item_name": {
                        "type": "string",
                        "required": True,
                        "description": "The name of the function or class to generate tests for."
                    }
                },
                "outputs": {
                    "test_code": {
                        "type": "string",
                        "description": "The generated unit test code."
                    }
                }
            },
            {
                "name": "generate_docstrings",
                "description": "Generates docstrings for functions or classes in a given file.",
                "inputs": {
                    "file_path": {
                        "type": "string",
                        "required": True,
                        "description": "The absolute path to the file."
                    }
                },
                "outputs": {
                    "updated_code": {
                        "type": "string",
                        "description": "The file content with the generated docstrings."
                    }
                }
            },
            {
                "name": "create_github_issue",
                "description": "Creates a new issue in a GitHub repository.",
                "inputs": {
                    "repo_owner": {
                        "type": "string",
                        "required": True,
                        "description": "The owner of the repository."
                    },
                    "repo_name": {
                        "type": "string",
                        "required": True,
                        "description": "The name of the repository."
                    },
                    "title": {
                        "type": "string",
                        "required": True,
                        "description": "The title of the issue."
                    },
                    "body": {
                        "type": "string",
                        "required": False,
                        "description": "The body of the issue."
                    }
                },
                "outputs": {
                    "issue_url": {
                        "type": "string",
                        "description": "The URL of the created issue."
                    }
                }
            },
            {
                "name": "create_github_pr",
                "description": "Creates a new pull request in a GitHub repository.",
                "inputs": {
                    "repo_owner": {
                        "type": "string",
                        "required": True,
                        "description": "The owner of the repository."
                    },
                    "repo_name": {
                        "type": "string",
                        "required": True,
                        "description": "The name of the repository."
                    },
                    "title": {
                        "type": "string",
                        "required": True,
                        "description": "The title of the pull request."
                    },
                    "body": {
                        "type": "string",
                        "required": False,
                        "description": "The body of the pull request."
                    },
                    "head": {
                        "type": "string",
                        "required": True,
                        "description": "The name of the branch where your changes are implemented."
                    },
                    "base": {
                        "type": "string",
                        "required": True,
                        "description": "The name of the branch you want the changes pulled into."
                    }
                },
                "outputs": {
                    "pr_url": {
                        "type": "string",
                        "description": "The URL of the created pull request."
                    }
                }
            }
        ]
    }
    return jsonify(manifest)

# --- JSON-RPC Methods ---
jsonrpc.register(call_gemini)
jsonrpc.register(summarize_docs)
jsonrpc.register(generate_docstrings)
jsonrpc.register(lint_code)
jsonrpc.register(generate_unit_tests)
jsonrpc.register(analyze_dependencies)
jsonrpc.register(create_github_issue)
jsonrpc.register(create_github_pr)

if __name__ == '__main__':
    port = int(os.environ.get('MCP_PORT', 5001))
    logger.info("Starting MCP server on port %s", port)
    app.run(port=port, debug=False)

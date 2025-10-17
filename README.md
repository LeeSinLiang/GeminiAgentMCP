# Gemini Agent MCP Server

This project is a Python-based FastMCP server that provides a Model Context Protocol (MCP) interface to the Gemini CLI and other development tools. It allows AI agents and other systems to programmatically call the Gemini model and perform various development tasks.

## Key Technologies

*   Python
*   FastMCP

## Features

The server exposes a set of tools to interact with the Gemini CLI and perform development tasks:

*   **`call_gemini`**: Calls the Gemini CLI with a given prompt. The Gemini CLI itself handles @-mentions of files and directories.
*   **`create_github_issue`**: Creates a new issue in a GitHub repository.
*   **`create_github_pr`**: Creates a new pull request in a GitHub repository.
*   **`summarize_docs`**: Summarizes the content of a list of documentation files.
*   **`generate_docstrings`**: Generates docstrings for functions or classes in a given file.
*   **`analyze_dependencies`**: Analyzes a dependency file (`requirements.txt` or `package.json`) and provides a summary of each dependency.
*   **`lint_code`**: Lints a Python or JavaScript file and returns a report of issues.
*   **`generate_unit_tests`**: Generates unit tests for a given function or class in a file.

## Getting Started

### Prerequisites

*   Python 3.x
*   pip

### Installation

1.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Server

```bash
python src/app.py
```

The server will start on `0.0.0.0:8000` by default.

## Development

### Conventions

*   **Code Style**: This project uses `pylint` for Python linting.
*   **Dependencies**: Project dependencies are managed in `requirements.txt`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

# Gemini Agent MCP Server

This server provides a Model Context Protocol (MCP) interface to the Gemini CLI. It allows AI agents and other systems to call the Gemini model and other tools by interacting with a standardized JSON-RPC endpoint.

## Setup

1.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Install Linters (for `lint_code` tool):**

    *   For Python linting, `pylint` is installed with the requirements.
    *   For JavaScript linting, you need to have `eslint` installed and available in your system's PATH. You can typically install it using npm:
        ```bash
        npm install -g eslint
        ```

3.  **Set Environment Variables:**

    *   **Ensure you are logged in to Gemini CLI:** Make sure you have the Gemini CLI installed and you are logged in. The server uses the Gemini CLI to call the Gemini model.

    *   **GitHub Token:** For the `create_github_issue` and `create_github_pr` tools, you need to set the `GITHUB_TOKEN` environment variable to your GitHub personal access token.

        ```bash
        export GITHUB_TOKEN="YOUR_GITHUB_TOKEN"
        ```

    *   **Server Port (Optional):** The server port can be configured using the `MCP_PORT` environment variable. It defaults to `5001`.

        ```bash
        export MCP_PORT=8080
        ```

4.  **Run the Server:**

    ```bash
    python src/main.py
    ```

    The server will start on the port specified by `MCP_PORT`, or 5001 by default.

## Usage

The server exposes two main endpoints:

*   `GET /mcp`: Returns the MCP manifest, which describes the available tools.
*   `POST /jsonrpc`: The JSON-RPC endpoint for calling the tools.

### Example: Calling a tool using JSON-RPC

You can use `curl` to send a JSON-RPC request to any of the available tools. Here is an example of calling the `call_gemini` tool:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "call_gemini",
    "params": {
      "prompt": "What is the capital of France?",
      "context": "This is a simple geography question."
    },
    "id": 1
  }' \
  http://127.0.0.1:5001/jsonrpc
```

This will return a JSON-RPC response with the answer from the Gemini model.

### Browsable API

For development and testing, you can access a web browsable API for the JSON-RPC endpoint by navigating to `http://127.0.0.1:5001/jsonrpc` in your web browser.

## Security

This server includes security measures to prevent unauthorized file access.

### File Path Validation

All tools that accept a file path (`summarize_docs`, `lint_code`, `analyze_dependencies`, `generate_unit_tests`, `generate_docstrings`) perform a validation to ensure that the requested path is within the project directory. This is to prevent directory traversal attacks where a user could potentially access sensitive files outside of the project's scope.

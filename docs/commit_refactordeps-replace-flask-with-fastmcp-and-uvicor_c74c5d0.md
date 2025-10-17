# Documentation for Commit c74c5d0

**Commit Hash:** c74c5d0d002d757450510087091503543dc4c7b8
**Commit Message:** refactor(deps): replace Flask with fastmcp and uvicorn
**Generated:** Thu Oct 16 12:20:41 EDT 2025
**Repository:** geminiAgentMCP

---

Here is the technical documentation for the provided git diff.

***

## Dependency Update: Migration from Flask to FastMCP Framework

### 1. Summary

This update marks a significant architectural migration of the application's web service layer. The project is moving from the synchronous Flask (WSGI) framework to **FastMCP**, a modern, high-performance ASGI framework. This change is intended to improve performance, scalability, and leverage modern Python asynchronous capabilities.

This involves replacing `Flask` and `flask-jsonrpc` with `fastmcp` and the `uvicorn` ASGI server.

### 2. Changes

#### Removed Dependencies

*   **`Flask`**: The previous micro-framework used for building the web service and its API endpoints.
*   **`flask-jsonrpc`**: The library that provided JSON-RPC protocol support on top of the Flask application.

#### Added Dependencies

*   **`fastmcp`**: The new core asynchronous web framework for building the API. All future web development will use this framework.
*   **`uvicorn`**: A lightning-fast ASGI (Asynchronous Server Gateway Interface) server, required to run the FastMCP application.

### 3. Impact

*   **Architectural Shift**: The application backend is now fully asynchronous, built to run on an ASGI server. This allows for higher concurrency and better performance, especially for I/O-bound tasks.
*   **Development Paradigm**: Developers must now write asynchronous code (using `async` and `await`) for request handlers and service logic to take full advantage of the new framework.
*   **Deployment**: The deployment process is fundamentally changed. The application must now be served by an ASGI-compatible server like `uvicorn` instead of a WSGI server (e.g., Gunicorn, Waitress).

### 4. Usage

To run the application locally after this change, you will use the `uvicorn` command.

Assuming your main application instance is named `app` in a file named `main.py`, run the following command from your project's root directory:

```bash
# Start the local development server with auto-reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Breaking Changes

**MAJOR BREAKING CHANGE:** This update completely replaces the web framework.

*   All code written for `Flask` and `flask-jsonrpc` is **not compatible** with FastMCP.
*   Flask-specific imports (e.g., `from flask import Flask, request`), decorators (`@app.route`), and context objects (`request`, `g`) are now obsolete and will raise errors.
*   The application's request/response lifecycle, dependency injection, and error handling mechanisms have changed entirely.

### 6. Migration Notes

All developers must take the following steps to adapt their local environments and ongoing work:

1.  **Update Environment**: Refresh your Python environment to install the new dependencies and remove the old ones.
    ```bash
    pip install -r requirements.txt
    ```

2.  **Refactor Endpoints**: All existing Flask routes and views must be rewritten using the FastMCP syntax. This includes updating route decorators, function signatures, and the methods for accessing request data and returning responses. Please consult the internal FastMCP documentation for API patterns and examples.

3.  **Update Run Scripts**: Any local development scripts (e.g., `.sh` or `.bat` files) or IDE run configurations must be updated to use the `uvicorn` command as shown in the **Usage** section above. CI/CD and deployment pipelines must also be updated accordingly.
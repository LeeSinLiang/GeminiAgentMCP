# Documentation for Commit e7828fc

**Commit Hash:** e7828fcb63b9fdbe6a3c1f52975e1311ef1096d4
**Commit Message:** feat(gemini): add base prompt and structured tags for sub-agent calls
**Generated:** Thu Oct 16 20:51:08 EDT 2025
**Repository:** geminiAgentMCP

---

Here is the technical documentation for the provided git diff.

***

### **Documentation: Enhanced Prompt Engineering for Gemini Sub-Agent**

This document outlines the recent changes to the `call_gemini_impl` function, which introduces a more robust and structured prompt engineering strategy.

#### **1. Summary**

The update refactors the prompt construction within the `call_gemini_impl` function to improve the reliability and safety of the underlying language model. A new `BASE_PROMPT` constant has been introduced to define a clear role and set of constraints for the model, framing it as a "sub-agent". The prompt format now uses XML-like tags to better distinguish between different instruction types, leading to more predictable behavior.

#### **2. Changes**

1.  **New `BASE_PROMPT` Constant:**
    *   A new module-level constant, `BASE_PROMPT`, has been added.
    *   This constant contains a foundational set of instructions that defines the model's role as a sub-agent within the Gemini CLI.
    *   It explicitly forbids the model from writing files or executing commands, limiting its capabilities to analysis and response generation.

2.  **Updated Prompt Structure:**
    *   The `full_prompt` sent to the Gemini model is now constructed using a more structured format.
    *   It prepends the `BASE_PROMPT` to every call.
    *   The `system_instruction` and `prompt` variables are now wrapped in `<system_instructions>` and `<prompt>` tags, respectively.

    **Before:**
    ```python
    full_prompt = f"{system_instruction}\n\n{prompt}"
    ```

    **After:**
    ```python
    BASE_PROMPT="..."
    full_prompt = f"{BASE_PROMPT}\n\n<system_instructions>{system_instruction}</system_instructions>\n\n<prompt>{prompt}</prompt>"
    ```

#### **3. Impact**

*   **Improved Reliability:** By providing a consistent role and strict constraints, the model's responses will be more focused and predictable. This reduces the likelihood of unexpected or undesirable behavior.
*   **Enhanced Safety:** The explicit prohibition on file writing and command execution acts as a critical safety layer, preventing the sub-agent from performing potentially harmful actions.
*   **Better Context Separation:** The use of XML-like tags helps the model clearly distinguish between the base rules, the specific system instructions for a task, and the user's prompt. This leads to more accurate and contextually appropriate responses.
*   **Improved Maintainability:** Centralizing the core instructions in the `BASE_PROMPT` constant makes it easier to manage and update the sub-agent's foundational behavior in a single location.

#### **4. Usage**

The function signature for `call_gemini_impl` remains unchanged. Developers will continue to call it as before. This change is internal to the function's implementation and does not require any modifications to existing function calls.

```python
# No change in how the function is called
response = call_gemini_impl(
    prompt="Analyze the following Python code for potential bugs.",
    system_instruction="You are a senior Python developer. Focus on logical errors and race conditions."
)
```

#### **5. Breaking Changes**

While there are no breaking changes to the API signature, this update introduces a **significant behavioral change**.

The Gemini sub-agent will now strictly adhere to the new constraints defined in `BASE_PROMPT`. It will refuse to generate responses that involve writing files or executing shell commands. Any existing prompts that relied on the model's ability to suggest such actions will now receive different, more constrained responses.

For example, a prompt asking "Write a 'hello world' script to /tmp/hello.py" will no longer produce the script content with an implicit instruction to write it. Instead, it will likely respond with the code and a statement that it cannot write files.

#### **6. Migration Notes**

*   **No Code Changes Required:** No modifications are needed for existing calls to `call_gemini_impl`.
*   **Review Existing Prompts:** Developers should review prompts that are passed to this function. If any prompts implicitly or explicitly ask the model to perform file I/O or command execution, they should be updated.
*   **Adapt Prompts to New Constraints:** Adjust prompts to request analysis, code generation, or information retrieval rather than direct actions. For instance, instead of "Run `pylint` on this file," a better prompt would be "Analyze this code and generate a Pylint-style report of potential issues."
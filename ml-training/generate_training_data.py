#!/usr/bin/env python3
"""
RLM Training Data Generator v2

Generates 150-200 training examples with real exec() outputs from real documents.
Each example is a multi-turn conversation where an assistant searches a document
using Python code, and the outputs come from actually executing that code.
"""

import json
import os
import sys
import io
import re
from pathlib import Path
from contextlib import redirect_stdout

# Add parent to path so we can import data_gen
sys.path.insert(0, str(Path(__file__).parent))

from data_gen.documents import get_all_documents
from data_gen.synthetic_docs import DOCUMENTS as SYNTHETIC_DOCS
from data_gen.traces import ALL_TRACES

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a SEARCH assistant with a Python REPL. You search documents - nothing else.

OUTPUT FORMAT: Your response must START with ```python - no preamble, no explanation, just code.

CONSTRAINT: Your training data is IRRELEVANT. You know NOTHING about this document.
- Answering without searching = WRONG
- Explaining instead of searching = WRONG
- Any text before your code block = WRONG

TOOLS:
- `context` - the document (already loaded, DO NOT redefine)
- `llm_query(question, context[start:end])` - ask sub-LLM about a chunk

WORKFLOW:
1. Write ```python with print() to search
2. STOP immediately after code block
3. Wait for output (appears in next message)
4. Search more OR give FINAL(answer)

SEARCH STRATEGY:
- If find() returns -1, try DIFFERENT keywords (not the same one)
- Try simpler terms, synonyms, related concepts
- Read surrounding text with context[idx:idx+500] to understand what you found

DO NOT:
- Explain what you're doing
- Answer from memory
- Write multiple code blocks
- Add text before ```python
- Redefine the context variable

When done searching, end with: FINAL(your evidence-based answer)"""

ERROR_REDEFINE_CONTEXT = (
    "ERROR: You cannot redefine 'context'. "
    "Use context.find() to search the existing text."
)

ERROR_NO_CODE = (
    "ERROR: You MUST write a ```python code block to search the document. "
    "You cannot answer from memory. Start with:\n"
    "```python\n"
    "idx = context.find('keyword')\n"
    "print(idx, context[idx:idx+500] if idx != -1 else 'not found')\n"
    "```"
)

ERROR_NO_CONTEXT_REF = (
    "ERROR: Your code must reference 'context' to search the document. "
    "Use context.find() or context[start:end] to access the text."
)

DOC_DIR = Path(__file__).parent / "data" / "documents"
GPO_PATH = Path(__file__).parent / "data" / "gpo_manual.txt"
OUTPUT_PATH = Path(__file__).parent / "data" / "rlm_training_v2.json"


# ---------------------------------------------------------------------------
# Execution engine
# ---------------------------------------------------------------------------

def execute_code(code: str, context: str) -> str:
    """Execute a code string with `context` available, capture stdout."""
    # Define a mock llm_query that returns a realistic response
    def llm_query(question, text_chunk):
        """Mock LLM query - returns a summary or FAILED based on content."""
        if not text_chunk or len(text_chunk.strip()) < 10:
            return "FAILED: Insufficient context provided."
        # Return a truncated version as a "summary"
        # In real usage, this calls an actual LLM
        lines = text_chunk.strip().split('\n')
        summary_lines = [l.strip() for l in lines if l.strip()][:3]
        return ' '.join(summary_lines)[:500]

    buf = io.StringIO()
    local_ns = {"context": context, "llm_query": llm_query}

    try:
        with redirect_stdout(buf):
            exec(code, {"__builtins__": __builtins__}, local_ns)
        output = buf.getvalue()
    except Exception as e:
        output = f"Traceback (most recent call last):\n  {type(e).__name__}: {e}"

    return output.rstrip('\n')


def check_redefines_context(code: str) -> bool:
    """Check if code tries to redefine the `context` variable."""
    # Match: context = ..., context=..., but not context[...] or context.find(...)
    patterns = [
        r'^\s*context\s*=',           # context = ...
        r'^\s*context\s*=',           # at line start
        r'\bopen\s*\(.*\).*read',     # open().read()
        r'requests\.get',              # requests.get
        r'load_document',              # load_document()
    ]
    for line in code.split('\n'):
        for pat in patterns:
            if re.search(pat, line):
                # Make sure it's not context[x] = or context.find
                if re.match(r'^\s*context\s*=', line):
                    return True
                if re.search(r'\bopen\s*\(', line) and 'context' in line:
                    return True
                if re.search(r'requests\.get', line):
                    return True
                if re.search(r'load_document', line):
                    return True
    return False


def check_references_context(code: str) -> bool:
    """Check if code references the `context` variable."""
    return 'context' in code


def build_messages(trace: dict, doc_content: str) -> list[dict]:
    """
    Build the messages array for one training example.

    A trace dict has:
      - doc: str (document name)
      - question: str
      - category: str
      - turns: list of dicts, each with:
          - role: "assistant"
          - content: str (the assistant's response - could be code or text)
          - error_type: optional str ("redefine_context", "no_code", "no_context_ref", "runtime")
            If set, the next user message uses the canned error instead of exec output.
          - is_final: optional bool - if True, this is a FINAL() message, no execution needed
          - llm_fail: optional bool - if True, llm_query should return FAILED
    """
    messages = []

    # First user message: system prompt + question
    messages.append({
        "role": "user",
        "content": SYSTEM_PROMPT + "\n\n---\n\n" + trace["question"]
    })

    for i, turn in enumerate(trace["turns"]):
        content = turn["content"]

        # Auto-wrap final messages that lack FINAL() format
        if turn.get("is_final") and "FINAL(" not in content:
            content = f"FINAL({content})"

        # Add assistant message
        messages.append({
            "role": "assistant",
            "content": content
        })

        # If this is a FINAL message, no user response needed
        if turn.get("is_final"):
            break

        # Determine user response
        error_type = turn.get("error_type")

        if error_type == "redefine_context":
            user_content = "Output:\n" + ERROR_REDEFINE_CONTEXT
        elif error_type == "no_code":
            user_content = "Output:\n" + ERROR_NO_CODE
        elif error_type == "no_context_ref":
            user_content = "Output:\n" + ERROR_NO_CONTEXT_REF
        else:
            # Extract code from the assistant's message
            code_match = re.search(r'```python\n(.*?)```', turn["content"], re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()

                # Check for context redefinition (for runtime error category)
                if error_type == "runtime":
                    # Execute and let it fail naturally
                    output = execute_code(code, doc_content)
                    user_content = "Output:\n" + output
                else:
                    output = execute_code(code, doc_content)
                    user_content = "Output:\n" + output
            else:
                # No code block found - shouldn't happen for valid traces
                user_content = "Output:\n" + ERROR_NO_CODE

        messages.append({
            "role": "user",
            "content": user_content
        })

    return messages


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_example(example: dict, idx: int) -> list[str]:
    """Validate a single training example. Returns list of issues."""
    issues = []
    msgs = example["messages"]

    # Check system prompt in first message
    first_msg = msgs[0]["content"]
    if not first_msg.startswith(SYSTEM_PROMPT):
        issues.append(f"Example {idx}: System prompt mismatch in first message")

    # Check alternating roles
    for i in range(1, len(msgs)):
        expected = "assistant" if i % 2 == 1 else "user"
        if msgs[i]["role"] != expected:
            issues.append(f"Example {idx}: Role mismatch at message {i}, "
                          f"expected {expected}, got {msgs[i]['role']}")

    # Check last message is assistant (FINAL or code)
    if msgs[-1]["role"] != "assistant":
        issues.append(f"Example {idx}: Last message should be assistant")

    # Check that FINAL examples actually have FINAL
    last_content = msgs[-1]["content"]
    if not last_content.startswith("```python") and "FINAL(" not in last_content:
        # Could be an error recovery that ends with code, that's ok
        pass

    return issues


def validate_all(examples: list[dict]) -> None:
    """Run validation on all examples and print results."""
    all_issues = []
    for i, ex in enumerate(examples):
        issues = validate_example(ex, i)
        all_issues.extend(issues)

    if all_issues:
        print(f"\n[!] {len(all_issues)} validation issues found:")
        for issue in all_issues[:20]:
            print(f"  - {issue}")
        if len(all_issues) > 20:
            print(f"  ... and {len(all_issues) - 20} more")
    else:
        print("\n[OK] All examples passed validation")


def print_stats(examples: list[dict], traces: list[dict]) -> None:
    """Print category distribution stats."""
    from collections import Counter
    cats = Counter(t["category"] for t in traces)
    print(f"\nTotal examples: {len(examples)}")
    print(f"\nCategory distribution:")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat:30s} {count:3d}")

    # Message count stats
    msg_counts = [len(ex["messages"]) for ex in examples]
    print(f"\nMessage count stats:")
    print(f"  Min: {min(msg_counts)}, Max: {max(msg_counts)}, "
          f"Avg: {sum(msg_counts)/len(msg_counts):.1f}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("RLM Training Data Generator v2")
    print("=" * 60)

    # Phase 1: Get all documents
    print("\n--- Phase 1: Loading documents ---")
    doc_dir = str(DOC_DIR)
    gpo_path = str(GPO_PATH) if GPO_PATH.exists() else None

    documents = get_all_documents(doc_dir, SYNTHETIC_DOCS, gpo_path)
    print(f"\nLoaded {len(documents)} documents:")
    for name, content in documents.items():
        print(f"  {name}: {len(content):,} chars")

    # Phase 2: Build training examples
    print("\n--- Phase 2: Building training examples ---")
    examples = []
    errors = []

    for i, trace in enumerate(ALL_TRACES):
        doc_name = trace["doc"]
        if doc_name not in documents:
            errors.append(f"Trace {i}: Document '{doc_name}' not found")
            continue

        doc_content = documents[doc_name]

        try:
            msgs = build_messages(trace, doc_content)
            examples.append({"messages": msgs})
        except Exception as e:
            errors.append(f"Trace {i} ({trace.get('category', '?')}): {e}")

    if errors:
        print(f"\n[!] {len(errors)} trace errors:")
        for err in errors:
            print(f"  - {err}")

    print(f"\nGenerated {len(examples)} examples from {len(ALL_TRACES)} traces")

    # Phase 3: Validate
    print("\n--- Phase 3: Validation ---")
    validate_all(examples)
    print_stats(examples, ALL_TRACES)

    # Phase 4: Save
    print("\n--- Phase 4: Saving ---")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(examples, f, indent=2, ensure_ascii=False)
    print(f"Saved to {OUTPUT_PATH}")
    print(f"File size: {OUTPUT_PATH.stat().st_size:,} bytes")

    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()

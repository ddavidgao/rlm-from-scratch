import re
from src.llm import chat_llm
# Instructions that tell the LLM how to use the REPL environment
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

class RLM:
    def __init__(self, root_model = "deepseek-r1:14b", sub_model="qwen3-coder:30b"):
        self.time_spent = 0
        self.root_model = root_model
        self.sub_model = sub_model
        self.sub_llm_calls = 0
        self.iterations = 0
        self.namespace = {}  # holds variables the LLM's code can access
        self.keywords = []
        self.counter = 0 # counter for chars read

    def run_code(self, codes):
        """Execute all code blocks and capture their print output"""
        import io
        import contextlib

        stdout = io.StringIO()  # single bucket collects all output
        for code in codes:
            try:
                with contextlib.redirect_stdout(stdout):
                    exec(code, self.namespace)
            except Exception as e:
                stdout.write(f"Error: {e}\n")  # append error, keep going
        return stdout.getvalue()
            
    def llm_query(self, question, subset):
        self.sub_llm_calls += 1
        result = chat_llm([{"role": "user", "content": f"Using ONLY the following context, answer the question. If the context doesn't contain enough information, respond with [FAILED] and briefly explain why.\n\nContext: {subset}\n\nQuestion: {question}"}], self.sub_model)
        self.time_spent += result["prompt_eval_duration"] + result["eval_duration"]
        return result["message"]["content"]

    def track_behavior(self, code_blocks):
        """Extract search keywords and chars read from code blocks."""
        for block in code_blocks:
            # TODO: use re.findall() to pull keywords from context.find('...')
            # pattern to match: context.find('some keyword') or context.find("some keyword")
            # append each found keyword to self.keywords

            keywords = re.findall(r"context\.find\(['\"](.+?)['\"]\)", block)
            self.keywords.extend(keywords)

            # Match literal slices: context[0:500] → 500 chars
            literal_slices = re.findall(r"context\[(\d+):(\d+)\]", block)
            for start, end in literal_slices:
                self.counter += int(end) - int(start)

            # Match variable slices: context[idx:idx+500] → 500 chars
            # Captures the offset number after the +
            var_slices = re.findall(r"context\[\w+:\w+\+(\d+)\]", block)
            for offset in var_slices:
                self.counter += int(offset)

    def extract_code(self, response):
        """Pull code out of ```python ... ``` blocks"""
        if "```python" in response:

            return [snippet.split("```")[0].strip() for i, snippet in enumerate(response.split("```python")) if i >= 1]
        return None

    def completion(self, question, context):
        """Main method - takes question + context, returns answer"""
        self.namespace["context"] = context  # make context available to exec'd code
        self.namespace["llm_query"] = self.llm_query
        messages = [
            {"role": "user", "content": SYSTEM_PROMPT + "\n\n---\n\n" + question}
        ]

        # REPL loop: LLM writes code → we run it → feed output back
        max_iterations = 30
        prev_response = None       # for repetition detection
        no_code_streak = 0         # consecutive turns without ```python

        for i in range(max_iterations):
            self.iterations += 1
            init = chat_llm(messages, self.root_model)

            response = init["message"]["content"]

            self.time_spent += init["prompt_eval_duration"] + init["eval_duration"]

            print(f"[DEBUG] LLM response:\n{response}\n---")  # see what LLM says

            # --- GUARDRAIL: repetition detection ---
            # If model gives the same response twice, it's stuck in a loop
            if prev_response and response.strip() == prev_response.strip():
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "user", "content": "You are REPEATING yourself. You must try a DIFFERENT search keyword. Use context.find() with a new term you haven't tried yet. If you've found enough evidence, say FINAL(your answer)."})
                prev_response = response
                continue
            prev_response = response

            # Check for code FIRST - run it before checking FINAL
            code = self.extract_code(response)

            # Only return FINAL if there's NO code to run
            if "FINAL" in response and not code:
                return response.split("FINAL")[1].strip("()")

            if code:
                no_code_streak = 0  # reset — model is following the workflow

                # Catch cheating - LLM trying to redefine context in any block
                if any("context =" in block or "context=" in block for block in code):
                    output = "ERROR: You cannot redefine 'context'. Use context.find() to search the existing text."
                # Catch fake code - must actually reference context to be a real search
                elif not any("context" in block for block in code):
                    output = "ERROR: Your code must search the `context` variable. Use context.find('keyword') to explore the document. You cannot answer from memory."
                else:
                    # --- GUARDRAIL: stale keyword detection ---
                    # Extract keywords from this code block before running
                    new_keywords = re.findall(r"context\.find\(['\"](.+?)['\"]\)", " ".join(code))
                    already_tried = [kw for kw in new_keywords if kw in self.keywords]

                    self.track_behavior(code)
                    output = self.run_code(code)

                    # If every keyword was already searched, nudge toward new terms
                    if new_keywords and len(already_tried) == len(new_keywords):
                        output += f"\n\nNOTE: You already searched for {already_tried}. Try DIFFERENT keywords — synonyms, related terms, or broader/narrower searches."
            else:
                no_code_streak += 1

                # --- GUARDRAIL: format drift ---
                # If model hasn't written code for 3 turns, it's lost the workflow
                if no_code_streak >= 3:
                    # Try to salvage an answer from whatever the model said
                    messages.append({"role": "assistant", "content": response})
                    messages.append({"role": "user", "content": "You have stopped writing code. Based on everything you've found so far, give your answer now. Respond with FINAL(your answer)."})
                    # Give it one last chance to produce a FINAL
                    last = chat_llm(messages, self.root_model)
                    last_response = last["message"]["content"]
                    self.time_spent += last["prompt_eval_duration"] + last["eval_duration"]
                    if "FINAL" in last_response:
                        return last_response.split("FINAL")[1].strip("()")
                    # If still no FINAL, return whatever it said
                    return last_response

                # No code = not following the workflow, push back
                output = "ERROR: You MUST write a ```python code block to search the document. You cannot answer from memory. Start with:\n```python\nidx = context.find('vessel')\nprint(idx, context[idx:idx+500] if idx != -1 else 'not found')\n```"

            # Add this exchange to history so LLM sees what happened
            messages.append({"role": "assistant", "content": response})
            messages.append({"role": "user", "content": f"Output:\n{output}"})

        # Hit max iterations without FINAL
        return "ERROR: Max iterations reached without conclusion"

    def get_behavior_stats(self, context_length):
        """Return a dict of behavioral metrics for eval."""
        unique_kw = set(self.keywords)
        return {
            "keywords_searched": self.keywords,           # every keyword in order
            "unique_keywords": len(unique_kw),            # how many distinct terms
            "repeated_keywords": len(self.keywords) - len(unique_kw),  # stuck-in-a-loop indicator
            "chars_read": self.counter,
            "doc_coverage_pct": round(self.counter / context_length * 100, 2) if context_length else 0,
        }

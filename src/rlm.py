import re
from src.llm import chat_llm

# Max chars of exec output to feed back to the model
MAX_OUTPUT_CHARS = 3000
# Max chars of non-code model response to keep in message history
MAX_RESPONSE_CHARS = 1500
# Max llm_query calls before we nudge model to use find() instead
MAX_LLM_QUERY_CALLS = 5
# Default preview window for doc.find()
DEFAULT_PREVIEW = 500
# Chunk size for document indexing
INDEX_CHUNK_SIZE = 2000


class SearchableDocument:
    """Wraps a raw text document with search-friendly methods.

    Provides auto-detected TOC, search with previews, and read tracking.
    Works with any document type — manuals, scripts, transcripts, etc.
    """

    def __init__(self, text):
        self._text = text
        self._reads = []
        self._total_chars_read = 0
        self._toc = self._detect_toc()

    def _detect_toc(self):
        """Auto-detect document structure. Tries multiple strategies:
        1. Explicit TOC/Contents section
        2. Structural headers (ALL CAPS, markdown ##, numbered sections)
        3. Scene headings (INT./EXT. for scripts)
        4. Fallback: first lines of evenly-spaced chunks

        Returns a compact list of (position, label) tuples.
        """
        lines = self._text.split('\n')
        headers = []

        # Strategy 1: Find an explicit TOC section and extract its entries
        toc_start = self._text.lower().find('contents')
        if toc_start != -1:
            # Read ~3000 chars from the TOC to grab entries
            toc_region = self._text[toc_start:toc_start + 3000]
            for line in toc_region.split('\n'):
                stripped = line.strip()
                # TOC entries are typically: "TOPIC_NAME    page_number" or just "TOPIC_NAME"
                if stripped and len(stripped) > 3 and not stripped.startswith('('):
                    # Remove trailing page numbers, dots, and leaders
                    label = re.sub(r'[\s.\-·]+\d+\s*$', '', stripped).strip()
                    # Also remove leading page numbers
                    label = re.sub(r'^\d+[\s.]+', '', label).strip()
                    if label and len(label) > 2 and len(label) < 80:
                        headers.append(label)
            if len(headers) > 5:
                # Deduplicate while preserving order
                seen = set()
                unique = []
                for h in headers:
                    key = h.lower()
                    if key not in seen:
                        seen.add(key)
                        unique.append(h)
                return unique[:40]  # cap at 40 entries

        # Strategy 2: Structural headers (ALL CAPS lines, markdown, numbered)
        pos = 0
        for line in lines:
            stripped = line.strip()
            is_header = False

            # ALL CAPS (common in manuals, legal docs)
            if (stripped == stripped.upper() and len(stripped) > 5
                    and len(stripped) < 80 and re.search(r'[A-Z]{3,}', stripped)):
                is_header = True

            # Markdown headers
            elif stripped.startswith('#'):
                is_header = True

            # Scene headings (screenplays)
            elif re.match(r'^(INT\.|EXT\.|INT/EXT\.)', stripped):
                is_header = True

            # Numbered sections like "1. Introduction" or "Chapter 1"
            elif re.match(r'^(Chapter|\d+\.)\s+\w', stripped, re.IGNORECASE):
                is_header = True

            if is_header:
                headers.append(stripped[:60])

            pos += len(line) + 1  # +1 for newline

        if len(headers) > 5:
            seen = set()
            unique = []
            for h in headers:
                key = h.lower()
                if key not in seen:
                    seen.add(key)
                    unique.append(h)
            return unique[:40]

        # Strategy 3: Fallback — sample first lines of evenly-spaced chunks
        chunk_size = max(len(self._text) // 20, 1000)
        for i in range(0, len(self._text), chunk_size):
            chunk = self._text[i:i + chunk_size]
            for cline in chunk.split('\n')[:5]:
                s = cline.strip()
                if s and len(s) > 5:
                    headers.append(s[:60])
                    break

        return headers[:20]

    def toc(self):
        """Return a compact table of contents (~200-500 chars).
        Shows what topics/sections the document contains.
        Use doc.find('TOPIC') to navigate to any topic."""
        if not self._toc:
            return f"Document: {len(self._text):,} chars (no clear structure detected). Use doc.find() to search."

        lines = [f"Document: {len(self._text):,} chars — Topics/sections found:"]
        for entry in self._toc:
            lines.append(f"  - {entry}")
        lines.append("Use doc.find('TOPIC NAME') to jump to any section.")
        return "\n".join(lines)

    def _log_read(self, start, end, method):
        """Track every read for accurate coverage stats."""
        chars = end - start
        self._reads.append({"start": start, "end": end, "chars": chars, "method": method})
        self._total_chars_read += chars

    def __len__(self):
        return len(self._text)

    def find(self, keyword, start=0, window=DEFAULT_PREVIEW):
        """Find keyword and return position + surrounding context."""
        idx = self._text.find(keyword, start)
        if idx == -1:
            return f"NOT FOUND: '{keyword}' (searched from position {start})"

        preview_start = max(0, idx - 50)
        preview_end = min(len(self._text), idx + window)
        preview = self._text[preview_start:preview_end]

        self._log_read(preview_start, preview_end, f"find('{keyword}')")

        return (
            f"FOUND '{keyword}' at position {idx}:\n"
            f"---\n"
            f"{preview}\n"
            f"---"
        )

    def find_all(self, keyword, max_results=10, window=200):
        """Find all occurrences of keyword with previews."""
        results = []
        start = 0
        while len(results) < max_results:
            idx = self._text.find(keyword, start)
            if idx == -1:
                break
            preview_start = max(0, idx - 30)
            preview_end = min(len(self._text), idx + window)
            preview = self._text[preview_start:preview_end]
            results.append(f"[pos {idx}]: ...{preview}...")
            self._log_read(preview_start, preview_end, f"find_all('{keyword}')")
            start = idx + 1

        if not results:
            return f"NOT FOUND: '{keyword}' — try different keywords"

        header = f"Found {len(results)} occurrence(s) of '{keyword}':\n"
        return header + "\n\n".join(results)

    def read(self, start, end=None, window=DEFAULT_PREVIEW):
        """Read a section of the document. Enforces minimum window size."""
        if end is None:
            end = start + window
        if end - start < 200:
            end = start + 200
        start = max(0, start)
        end = min(len(self._text), end)

        self._log_read(start, end, f"read({start}, {end})")

        return (
            f"[Positions {start}-{end} ({end - start} chars)]:\n"
            f"---\n"
            f"{self._text[start:end]}\n"
            f"---"
        )

    def get_read_stats(self):
        """Return reading statistics for eval."""
        if not self._reads:
            return {"total_chars_read": 0, "num_reads": 0, "coverage_pct": 0}

        # Merge overlapping read ranges for accurate unique coverage
        sorted_reads = sorted(self._reads, key=lambda r: r["start"])
        merged = []
        for r in sorted_reads:
            if merged and r["start"] <= merged[-1][1]:
                merged[-1] = (merged[-1][0], max(merged[-1][1], r["end"]))
            else:
                merged.append((r["start"], r["end"]))

        unique_chars = sum(end - start for start, end in merged)

        return {
            "total_chars_read": self._total_chars_read,
            "unique_chars_read": unique_chars,
            "num_reads": len(self._reads),
            "coverage_pct": round(unique_chars / len(self._text) * 100, 2) if self._text else 0,
            "read_log": self._reads,
        }

    def __repr__(self):
        return f"SearchableDocument({len(self._text):,} chars, {len(self._index)} sections)"


SYSTEM_PROMPT = """You are a SEARCH assistant with a Python REPL. You search documents to answer questions.

CONSTRAINT: Your training data is IRRELEVANT. You know NOTHING about this document.
You MUST find evidence in the document before answering.

TOOLS (available in your code):
- `doc.find('keyword')` — finds keyword, shows position + surrounding text
- `doc.find_all('keyword')` — shows ALL occurrences with previews
- `doc.read(start, end)` — reads a section (minimum 200 chars)
- `doc.toc()` — shows a compact table of contents / topic list for the document
- `llm_query(question, doc.read(start, end))` — ask sub-LLM about a chunk (use sparingly)

WORKFLOW:
1. Review the document map to understand what the document covers
2. Think about what topics/concepts from the question you need to look up
3. Write a ```python block to search for one topic
4. Read the output, then search for the next topic
5. After covering all relevant topics, say FINAL(your answer)

SEARCH STRATEGY:
- Think about what CATEGORIES of rules might apply, not just terms from the question
- If doc.find() returns NOT FOUND, try shorter or different terms
- Use doc.find_all() to see every place a term appears
- Cover ALL aspects of the question before answering

DO NOT:
- Answer from memory — you MUST search first
- Redefine doc or context

When done: FINAL(your evidence-based answer)"""


def strip_think_tokens(response):
    """Remove <think>...</think> blocks from R1-style model responses."""
    cleaned = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
    cleaned = re.sub(r'<think>.*$', '', cleaned, flags=re.DOTALL)
    return cleaned.strip()


def truncate_output(output, max_chars=MAX_OUTPUT_CHARS):
    """Truncate exec output to prevent context explosion."""
    if len(output) <= max_chars:
        return output
    half = max_chars // 2
    return (
        output[:half]
        + f"\n\n... [TRUNCATED — {len(output)} chars total] ...\n\n"
        + output[-half:]
    )


def truncate_response_for_history(response, code_blocks, max_chars=MAX_RESPONSE_CHARS):
    """Trim excessive non-code text from model response before adding to history."""
    if len(response) <= max_chars:
        return response
    if code_blocks:
        return "\n\n".join(f"```python\n{block}\n```" for block in code_blocks)
    return response[:max_chars] + "\n... [response truncated]"


class RLM:
    def __init__(self, root_model="rlm-r1-14b:latest", sub_model="rlm-r1-14b:latest"):
        self.time_spent = 0
        self.root_model = root_model
        self.sub_model = sub_model
        self.sub_llm_calls = 0
        self.iterations = 0
        self.namespace = {}
        self.keywords = []
        self.doc = None  # set in completion()

    def run_code(self, codes):
        """Execute code blocks and capture output.
        Auto-captures return values if no print() is used."""
        import io
        import contextlib

        stdout = io.StringIO()
        for code in codes:
            try:
                with contextlib.redirect_stdout(stdout):
                    exec(code, self.namespace)
            except Exception as e:
                stdout.write(f"Error: {e}\n")

        result = stdout.getvalue()

        # If no print output, eval the last expression for feedback
        if not result.strip() and codes:
            last_line = codes[-1].strip().split('\n')[-1].strip()
            try:
                val = eval(last_line, self.namespace)
                if val is not None:
                    result = str(val) + "\n"
            except:
                pass

        if not result.strip():
            result = "[NO OUTPUT] Your code produced no output. Call doc.find() directly — it returns results automatically.\n"

        return result

    def llm_query(self, question, subset):
        self.sub_llm_calls += 1

        if self.sub_llm_calls > MAX_LLM_QUERY_CALLS:
            return f"[QUERY LIMIT] You've used llm_query {self.sub_llm_calls} times. Use doc.find() to search instead."

        result = chat_llm([{"role": "user", "content": f"Using ONLY the following context, answer the question. If the context doesn't contain enough information, respond with [FAILED] and briefly explain why.\n\nContext: {subset}\n\nQuestion: {question}"}], self.sub_model)
        self.time_spent += result["prompt_eval_duration"] + result["eval_duration"]
        return result["message"]["content"]

    def track_behavior(self, code_blocks):
        """Extract search keywords from code blocks."""
        for block in code_blocks:
            keywords = re.findall(r"doc\.find(?:_all)?\(['\"](.+?)['\"]\)", block)
            keywords += re.findall(r"context\.find\(['\"](.+?)['\"]\)", block)
            self.keywords.extend(keywords)

    def extract_code(self, response):
        """Pull code out of ```python ... ``` blocks"""
        if "```python" in response:
            return [snippet.split("```")[0].strip() for i, snippet in enumerate(response.split("```python")) if i >= 1]
        return None

    def completion(self, question, context):
        """Main method - takes question + context, returns answer"""
        # Create SearchableDocument
        self.doc = SearchableDocument(context)
        self.namespace["doc"] = self.doc
        self.namespace["context"] = context
        self.namespace["llm_query"] = self.llm_query

        messages = [
            {"role": "user", "content": SYSTEM_PROMPT + "\n\n---\n\n" + question}
        ]

        max_iterations = 30
        prev_response = None
        no_code_streak = 0

        for i in range(max_iterations):
            self.iterations += 1
            init = chat_llm(messages, self.root_model)

            raw_response = init["message"]["content"]
            self.time_spent += init.get("prompt_eval_duration", 0) + init.get("eval_duration", 0)

            response = strip_think_tokens(raw_response)

            print(f"[DEBUG] LLM response:\n{response[:500]}{'... [truncated]' if len(response) > 500 else ''}\n---")

            # --- GUARDRAIL: repetition detection ---
            if prev_response and response.strip() == prev_response.strip():
                messages.append({"role": "assistant", "content": response})
                messages.append({"role": "user", "content": "You are REPEATING yourself. Try a DIFFERENT search term with doc.find(). If you have enough evidence, say FINAL(your answer)."})
                prev_response = response
                continue
            prev_response = response

            code = self.extract_code(response)

            if "FINAL" in response and not code:
                return response.split("FINAL")[1].strip("()")

            if code:
                no_code_streak = 0
                code = code[:1]

                if any(re.search(r'\b(doc|context)\s*=', block) for block in code):
                    output = "ERROR: You cannot redefine 'doc' or 'context'."
                elif not any("doc" in block or "context" in block for block in code):
                    output = "ERROR: Your code must use `doc` to search. Try: doc.find('keyword')"
                else:
                    new_keywords = re.findall(r"doc\.find(?:_all)?\(['\"](.+?)['\"]\)", " ".join(code))
                    new_keywords += re.findall(r"context\.find\(['\"](.+?)['\"]\)", " ".join(code))
                    already_tried = [kw for kw in new_keywords if kw in self.keywords]

                    self.track_behavior(code)
                    output = self.run_code(code)
                    output = truncate_output(output)

                    if new_keywords and len(already_tried) == len(new_keywords):
                        output += f"\n\nNOTE: You already searched for {already_tried}. Try DIFFERENT keywords."
            else:
                no_code_streak += 1

                if no_code_streak >= 3:
                    messages.append({"role": "assistant", "content": truncate_response_for_history(response, code)})
                    messages.append({"role": "user", "content": "You have stopped writing code. Based on everything you've found so far, give your answer now. Respond with FINAL(your answer)."})
                    last = chat_llm(messages, self.root_model)
                    last_raw = last["message"]["content"]
                    self.time_spent += last["prompt_eval_duration"] + last["eval_duration"]
                    last_response = strip_think_tokens(last_raw)
                    if "FINAL" in last_response:
                        return last_response.split("FINAL")[1].strip("()")
                    return last_response

                output = "ERROR: You MUST write a ```python code block. Try:\n```python\ndoc.find('keyword')\n```"

            messages.append({"role": "assistant", "content": truncate_response_for_history(response, code)})
            messages.append({"role": "user", "content": f"Output:\n{output}"})

        return "ERROR: Max iterations reached without conclusion"

    def get_behavior_stats(self, context_length):
        """Return behavioral metrics for eval, using accurate read tracking."""
        unique_kw = set(self.keywords)

        # Get accurate read stats from the document itself
        read_stats = self.doc.get_read_stats() if self.doc else {}

        return {
            "keywords_searched": self.keywords,
            "unique_keywords": len(unique_kw),
            "repeated_keywords": len(self.keywords) - len(unique_kw),
            "chars_read": read_stats.get("unique_chars_read", 0),
            "total_chars_read": read_stats.get("total_chars_read", 0),
            "num_reads": read_stats.get("num_reads", 0),
            "doc_coverage_pct": read_stats.get("coverage_pct", 0),
            "read_log": read_stats.get("read_log", []),
        }

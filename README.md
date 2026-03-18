# RLM — Recursive Language Model

An agentic document search system that forces LLMs to find evidence instead of hallucinating. Instead of letting a model answer from memory, you give it a Python REPL with search tools and make it actually look through the document. It writes code, sees the output, writes more code, and keeps going until it finds what it needs.

Built to understand how agentic LLM systems work from the ground up — the REPL loop, tool design, prompt engineering, fine-tuning, and the fundamental challenge of getting models to use tools reliably.

## Architecture: SearchableDocument

The core innovation is `SearchableDocument` — a wrapper that gives the model high-level search tools instead of a raw string:

```python
doc.find('keyword')      # → position + 500 chars of surrounding context
doc.find_all('keyword')  # → all occurrences with previews
doc.read(start, end)     # → section text (minimum 200 chars enforced)
doc.toc()                # → auto-detected table of contents (~124 tokens)
```

This is a deliberate departure from the MIT RLM paper (Zhang, Kraska, Khattab 2025), which gave models a raw `context` string and required them to write multi-line Python for every search. That worked with GPT-5/480B. SearchableDocument offloads the mechanical work to the tool layer so smaller models can focus on *what* to search rather than *how*.

**Auto-TOC detection** identifies document structure automatically — explicit table of contents, ALL CAPS headers, markdown headings, screenplay scene headings (`INT./EXT.`), numbered sections — and falls back to sampling chunk previews. Works on any document type without configuration.

### Guardrails

The REPL loop includes several protections discovered through 29 benchmark runs:

- **Hallucination stripping** — Only the first code block + brief preamble is kept in message history. Everything after is stripped, preventing models from seeing their own fabricated outputs.
- **Think token handling** — `<think>...</think>` blocks from R1-style models are stripped before processing.
- **Output truncation** — Exec output capped at 3000 chars to prevent context explosion.
- **Auto-eval fallback** — If code produces no print output, the last expression is evaluated and returned automatically.
- **First block only** — Only the first code block per response is executed, forcing one-search-per-iteration discipline.
- **Repetition detection** — Identical consecutive responses trigger a nudge to try different keywords.
- **Stale keyword detection** — Re-searching already-tried terms triggers a suggestion to vary the search.
- **Format drift recovery** — After 3 consecutive turns without code, the model is forced to give a FINAL answer.

## Benchmark Results

Tested across 6 models, 3 architecture versions, 29 total runs on a GPO Style Manual formatting task (7 rules to find):

### Architecture Progression

| Version | Key Change | Best Score | Best Model |
|---------|-----------|------------|------------|
| v1 (original) | Raw `context` string | 14% (1/7) | rlm-8b-sft |
| v2 (guardrails) | Think stripping, output truncation | 14% (1/7) | rlm-8b-sft |
| v3 (SearchableDocument) | `doc.find()`, auto-TOC, hallucination stripping | 0% formal / found correct evidence | qwen3-coder:30b |

### Model Comparison (v3 architecture)

| Model | Size | GPU Fit | Follows Workflow | Searches | Interprets |
|-------|------|---------|-----------------|----------|------------|
| lfm2.5-thinking 1.2B | 731MB | 100% | No | No | No |
| rlm-r1-14b (SFT) | 9GB | 100% | No | No | No |
| deepseek-r1:14b | 9GB | 100% | No | No | No |
| qwen2.5-coder:14b | 9GB | 100% | Mostly | Partially | No |
| qwen3-coder:30b | 18GB | 77% | Yes | Yes | Almost |
| Claude (via CLI) | Cloud | N/A | Yes | Yes | Yes |

### Key Findings

**The architecture works.** qwen3-coder:30b searched 61 unique keywords, navigated to the correct document sections using `doc.toc()`, and found real evidence (e.g., `U. S. gunboat _Katahdin_`). Claude with the same architecture answered 7/7 questions correctly on a fresh GAO report it had never seen, searching `deferred resignation`, `commissioners`, `paper returns`, `phone calls`, `December 2025`, and `Recommendations for Executive Action` — all from real document reads.

**The bottleneck is model reasoning, not architecture.** qwen3-coder:30b found the right sections but scored 0/7 on the formal grading because it couldn't make the final interpretive leap (e.g., connecting `_Katahdin_` underscore notation to "italics" to "the rule says no italics in tables"). The grading system is also too rigid — regex pattern matching misses correct-but-differently-worded answers.

**SFT teaches format, not discipline.** Fine-tuned models (1B, 8B, 14B) learned to write `context.find()` code blocks but not to stop, wait for output, and react to real results. They hallucinate outputs or give up after 2-3 iterations. This is a behavior discipline problem better suited to RL than SFT.

**R1-style models are problematic.** DeepSeek R1 generates thousands of hidden `<think>` tokens per turn (1537 seconds for 2 iterations). Even with think-token stripping, they ignore search instructions and answer from memory.

## Project Structure

- `src/rlm.py` — SearchableDocument + REPL loop with all guardrails
- `src/llm.py` — Ollama API wrapper
- `main.py` — GPO manual eval pipeline with deterministic rule checkers
- `eval_compare.py` — multi-model benchmark runner with chart generation
- `run_results.json` — all benchmark runs with behavioral metrics
- `ml-training/` — fine-tuning pipeline (QLoRA via Unsloth)
- `karpathy-gpt/` — transformer from scratch (Karpathy tutorial)

## ml-training

Fine-tuned three model sizes on 155 synthetic multi-turn RLM search conversations:

| Model | Base | LoRA Params | Training Time | Output |
|-------|------|-------------|---------------|--------|
| 1B | Llama 3.2 1B Instruct | 3.4M (0.28%) | <1 min | `outputs/1b/rlm_lora_v2/` |
| 8B | Llama 3.1 8B Instruct | ~13M | ~3 min | `outputs/8b/rlm_lora_v3/` |
| 14B | DeepSeek R1 Distill Qwen 14B | ~17M | ~5 min | `outputs/r1/rlm_lora_v4/` |

Training uses QLoRA (4-bit base, LoRA on attention layers) via Unsloth in Docker on WSL. Full deployment pipeline: LoRA adapter → merged HF model → GGUF F16 → GGUF Q4_K_M → Ollama registration.

### Deploying an SFT Model to Ollama

Five stages, each producing a different artifact:

**1. LoRA Adapter** → Small delta weights (~50MB). Just the changes from fine-tuning.

**2. Merged HF Model** → LoRA weights merged into base model, saved as HuggingFace safetensors.
```python
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="/workspace/outputs/8b/rlm_lora_v3",
    max_seq_length=1024, load_in_4bit=True
)
model.save_pretrained_merged("/workspace/outputs/8b/rlm-8b-sft-merged", tokenizer)
```

**3. GGUF F16** → Repackaged into llama.cpp's single-file format.
```bash
python3 ~/llama.cpp/convert_hf_to_gguf.py /path/to/merged --outtype f16
```

**4. GGUF Q4_K_M** → Compressed from fp16 to 4-bit. Build llama-quantize with `-DGGML_OPENMP=OFF` to avoid Docker libgomp issues.
```bash
llama-quantize input-F16.gguf output-Q4_K_M.gguf Q4_K_M
```

**5. Ollama Model** → Register with a Modelfile specifying the chat template.
```bash
ollama create rlm-8b-sft -f Modelfile
```

### Gotchas

- **`load_adapter()` vs `from_pretrained(adapter_dir)`**: `load_adapter` doesn't wrap as PeftModel, so Unsloth's merge silently skips.
- **Don't quantize across WSL mounts**: `/mnt/c/` I/O bridge can't handle 20GB of reads+writes. Copy to `~/`, quantize, copy back.
- **llama.cpp in Docker**: Missing `libgomp` (OpenMP). Build with `-DGGML_OPENMP=OFF` or install `libgomp-dev`.

## Next Phase: Tool-Use Discipline Training

The current bottleneck isn't model intelligence — it's tool-use discipline. Small models can write search code but can't reliably follow the REPL loop (write one block → stop → wait → react to real output). This is a behavior pattern, not a reasoning task.

### The Research Gap

- **Single-turn function calling** is solved — xLAM-1B beats GPT-3.5-Turbo (Berkeley BFCL benchmark)
- **Multi-turn agentic RL** is exploding — Agent-R1, AGENTRL, RLEF, ToolRM all dropped in 2025
- **REPL-style iterative tool use on small models (1-8B)** is the open area

Key evidence that small models can do this:
- ReAct fine-tuned 8B outperformed prompting-only 62B (Google, 2022)
- GRPO on Qwen-2-7B outperformed vanilla Qwen-2-72B on function calling
- Toolformer showed tool-use capability emerges at ~775M parameters

### Planned Approach

1. **Generate paired training data**: good (one code block → stop → react to real output) vs bad (hallucinate output, answer from memory, write multiple blocks)
2. **Train with DPO/GRPO** to prefer disciplined tool-use behavior
3. **SearchableDocument handles the search intelligence** — model just needs to use the tools reliably
4. **Eval on diverse documents** (manuals, scripts, reports, transcripts)

### Key Risk

The Reasoning Trap (Oct 2025): RL-enhanced reasoning proportionally increases tool hallucination. No known solution that doesn't sacrifice capability.

## karpathy-gpt

Built a transformer from scratch following Andrej Karpathy's "Let's build GPT from scratch" series. Starts from a bigram model and incrementally adds positional embeddings, self-attention, multi-head attention, and feed-forward networks. Character-level prediction on Tiny Shakespeare (~1.1M chars).

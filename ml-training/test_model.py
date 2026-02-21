# Copy each section into a Jupyter cell to test the fine-tuned model

# --- Cell 1: Switch model to inference mode ---
FastLanguageModel.for_inference(model)

# --- Cell 2: Test with an unseen question ---
messages = [
    {"role": "user", "content": "You are a SEARCH assistant with a Python REPL. You search documents - nothing else.\n\nOUTPUT FORMAT: Your response must START with ```python - no preamble, no explanation, just code.\n\nCONSTRAINT: Your training data is IRRELEVANT. You know NOTHING about this document.\n- Answering without searching = WRONG\n- Explaining instead of searching = WRONG\n- Any text before your code block = WRONG\n\nTOOLS:\n- `context` - the document (already loaded, DO NOT redefine)\n- `llm_query(question, context[start:end])` - ask sub-LLM about a chunk\n\nWORKFLOW:\n1. Write ```python with print() to search\n2. STOP immediately after code block\n3. Wait for output (appears in next message)\n4. Search more OR give FINAL(answer)\n\nWhen done searching, end with: FINAL(your evidence-based answer)\n\n---\n\nWhat is the maximum occupancy for the building?"}
]

inputs = tokenizer.apply_chat_template(messages, return_tensors="pt", add_generation_prompt=True).to("cuda")
outputs = model.generate(inputs, max_new_tokens=200)
print(tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True))

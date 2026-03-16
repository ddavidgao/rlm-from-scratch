"""
Comparative eval: run the same RLM question against multiple models sequentially.
Unloads each model after its run to keep VRAM safe.
"""
import json
import os
import sys
import time
import requests
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.rlm import RLM

RESULTS_FILE = "run_results.json"

# Models to compare — run sequentially, one at a time
MODELS_TO_EVAL = [
    "rlm-r1-14b:latest",    # new R1-based SFT (Q4_K_M)
    "rlm-8b-sft:latest",    # existing 8B Llama SFT
    "deepseek-r1:14b",      # base DeepSeek R1 (no SFT)
]

# Same question from main.py
QUESTION = """I need to format this table entry for a government report:

"The U.S.S. Katahdin, a 150 foot gunboat with a 500 horsepower engine, stationed at the League Island Navy Yard in Pennsylvania, commanded by Lieutenant Commander R. W. Meade of the United States Navy."

According to this manual, what are ALL the formatting rules that apply to this entry, considering it will appear in a TABLE? List each rule and the correction needed."""


def unload_model(model_name):
    """Tell Ollama to unload a model from VRAM."""
    try:
        requests.post("http://localhost:11434/api/generate", json={
            "model": model_name,
            "keep_alive": 0,
        })
        print(f"  Unloaded {model_name} from VRAM")
        time.sleep(3)  # give GPU a moment to free memory
    except Exception as e:
        print(f"  Warning: couldn't unload {model_name}: {e}")


def score_answer(answer):
    """Deterministic grading from main.py"""
    import re

    def check_italic(ans):
        mentions = re.search(r'italic', ans, re.IGNORECASE)
        if not mentions: return "MISSED"
        correct = re.search(r'(not?\s+italic|don.t\s+italic|no\s+italic|non.?italic)', ans, re.IGNORECASE)
        return "FOUND" if correct else "WRONG"

    def check_uss_spacing(ans):
        correct = re.search(r'U\.\s+S\.\s+S\.', ans)
        if correct: return "FOUND"
        wrong = re.search(r'U\.S\.S\.', ans)
        return "WRONG" if wrong else "MISSED"

    def check_hyphen_foot(ans):
        correct = re.search(r'150-foot', ans, re.IGNORECASE)
        if correct: return "FOUND"
        wrong = re.search(r'hyphen', ans, re.IGNORECASE)
        return "WRONG" if wrong else "MISSED"

    def check_navy_yard(ans):
        correct = re.search(r'navy-yard', ans, re.IGNORECASE)
        if correct: return "FOUND"
        wrong = re.search(r'navy\s+yard', ans, re.IGNORECASE)
        return "WRONG" if wrong else "MISSED"

    def check_pa_abbrev(ans):
        correct = re.search(r'\bPa\.', ans)
        return "FOUND" if correct else "MISSED"

    def check_lieut(ans):
        correct = re.search(r'Lieut\.', ans)
        if correct: return "FOUND"
        wrong = re.search(r'Lieutenant\s+Commander', ans)
        return "WRONG" if wrong else "MISSED"

    def check_usn_spelled(ans):
        mentions_usn = re.search(r'United States Navy', ans)
        if not mentions_usn: return "MISSED"
        keep = re.search(r'(spell|keep|do not abbreviat|don.t abbreviat|written out|full)', ans, re.IGNORECASE)
        if keep: return "FOUND"
        abbrev = re.search(r'U\.?\s*S\.?\s*N\.', ans)
        return "WRONG" if abbrev else "MISSED"

    RULE_CHECKERS = [
        ("Vessel names NOT italicized in tables", check_italic),
        ("U. S. S. with periods and spaces", check_uss_spacing),
        ("Hyphenate 150-foot compound adjective", check_hyphen_foot),
        ("Hyphenate navy-yard", check_navy_yard),
        ("Use Pa. abbreviation for Pennsylvania", check_pa_abbrev),
        ("Abbreviate Lieut. Commander with name", check_lieut),
        ("Keep United States Navy spelled out", check_usn_spelled),
    ]

    results = []
    found_count = 0
    for rule_name, checker in RULE_CHECKERS:
        verdict = checker(answer)
        if verdict == "FOUND":
            found_count += 1
        results.append((rule_name, verdict))
        print(f"    {verdict:6s}  {rule_name}")

    score = found_count / len(RULE_CHECKERS)
    print(f"    SCORE: {found_count}/{len(RULE_CHECKERS)} ({score:.0%})")
    return score, results


def run_eval(model_name, context):
    """Run one model through the eval, return results dict."""
    print(f"\n{'='*60}")
    print(f"  EVALUATING: {model_name}")
    print(f"{'='*60}")

    # Use same model for both root and sub to keep it simple
    rlm = RLM(root_model=model_name, sub_model=model_name)

    start = time.time()
    answer = rlm.completion(QUESTION, context)
    wall_time = time.time() - start

    print(f"\n  ANSWER: {answer[:300]}...")
    print(f"\n  --- GRADING ---")
    score, rule_results = score_answer(answer)

    behavior = rlm.get_behavior_stats(len(context))
    total_calls = rlm.iterations + rlm.sub_llm_calls
    llm_time = rlm.time_spent / 1_000_000_000

    # Determine run ID
    results = []
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            results = json.load(f)
    run_id = len(results) + 1

    run_data = {
        "run_id": run_id,
        "model": model_name,
        "timestamp": datetime.now().isoformat(),
        "total_llm_calls": total_calls,
        "root_iterations": rlm.iterations,
        "sub_llm_calls": rlm.sub_llm_calls,
        "time_seconds": round(llm_time, 2),
        "wall_time_seconds": round(wall_time, 2),
        "score": round(score, 2),
        "unique_keywords": behavior["unique_keywords"],
        "repeated_keywords": behavior["repeated_keywords"],
        "chars_read": behavior["chars_read"],
        "doc_coverage_pct": behavior["doc_coverage_pct"],
        "keywords_searched": behavior["keywords_searched"],
        "rule_verdicts": {name: verdict for name, verdict in rule_results},
        "answer_preview": answer[:300],
    }

    # Save incrementally
    results.append(run_data)
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n  Run #{run_id} saved: score={score:.0%}, calls={total_calls}, time={llm_time:.1f}s (wall: {wall_time:.1f}s)")

    # Unload model from VRAM before next run
    unload_model(model_name)

    return run_data


def main():
    # Load document
    with open("gpo_manual.txt", "r", encoding="utf-8") as f:
        context = f.read()
    print(f"Document loaded: {len(context)} characters")

    # Run each model
    all_results = []
    for model in MODELS_TO_EVAL:
        result = run_eval(model, context)
        all_results.append(result)

    # Print comparison table
    print(f"\n{'='*60}")
    print(f"  COMPARISON RESULTS")
    print(f"{'='*60}")
    print(f"  {'Model':<25} {'Score':>6} {'Calls':>6} {'Time':>8} {'Keywords':>9} {'Coverage':>9}")
    print(f"  {'-'*25} {'-'*6} {'-'*6} {'-'*8} {'-'*9} {'-'*9}")
    for r in all_results:
        print(f"  {r['model']:<25} {r['score']:>5.0%} {r['total_llm_calls']:>6} {r['time_seconds']:>7.1f}s {r['unique_keywords']:>9} {r['doc_coverage_pct']:>8.1f}%")

    print(f"\nAll results saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()

"""
Comparative eval v2: benchmarks models and generates comparison charts.
Runs each model sequentially, unloads between runs to protect VRAM.
Produces a grouped bar chart comparing all runs across key metrics.
"""
import json
import os
import sys
import time
import requests
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from src.rlm import RLM

RESULTS_FILE = "run_results.json"

# Models to compare
MODELS_TO_EVAL = [
    "qwen3-coder:30b",
]

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
        time.sleep(3)
    except Exception as e:
        print(f"  Warning: couldn't unload {model_name}: {e}")


# --- RULE CHECKERS (same as main.py) ---

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


def score_answer(answer):
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
    print(f"\n{'='*60}")
    print(f"  EVALUATING: {model_name}")
    print(f"{'='*60}")

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
        "rlm_version": "v3",  # v3 = planning step + guardrails
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

    results.append(run_data)
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n  Run #{run_id} saved: score={score:.0%}, calls={total_calls}, time={llm_time:.1f}s (wall: {wall_time:.1f}s)")

    unload_model(model_name)
    return run_data


def generate_comparison_chart():
    """Generate before/after comparison charts from run_results.json."""
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')  # non-interactive backend
    import numpy as np

    with open(RESULTS_FILE, "r") as f:
        all_results = json.load(f)

    # Group runs by version, take LATEST run per model per version
    version_runs = {}  # version -> {model -> run_data}

    for r in all_results:
        model = r["model"]
        version = r.get("rlm_version", "v1")
        if version not in version_runs:
            version_runs[version] = {}
        version_runs[version][model] = r  # last one wins

    versions = sorted(version_runs.keys())  # e.g. ['v1', 'v2', 'v3']
    models = sorted(set().union(*(v.keys() for v in version_runs.values())))

    if not models:
        print("No results to plot.")
        return

    # --- Figure 1: Grouped bar chart (score, keywords, coverage) ---
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(f"RLM Benchmark: {' vs '.join(versions)}", fontsize=16, fontweight='bold')

    x = np.arange(len(models))
    n_versions = len(versions)
    width = 0.8 / max(n_versions, 1)
    short_names = [m.replace(":latest", "").replace(":14b", " 14B") for m in models]
    colors = ['#e74c3c', '#f39c12', '#2ecc71', '#3498db', '#9b59b6'][:n_versions]

    def plot_grouped_bar(ax, metric, title, ylabel, fmt="{:.0f}", ylim=None):
        for vi, ver in enumerate(versions):
            offset = (vi - n_versions/2 + 0.5) * width
            vals = [version_runs.get(ver, {}).get(m, {}).get(metric, 0) for m in models]
            if metric == "score":
                vals = [v * 100 for v in vals]
            bars = ax.bar(x + offset, vals, width, label=ver, color=colors[vi], alpha=0.85)
            for bar in bars:
                label = fmt.format(bar.get_height())
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, label, ha='center', va='bottom', fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(short_names, fontsize=9)
        ax.legend(fontsize=8)
        if ylim:
            ax.set_ylim(ylim)

    plot_grouped_bar(axes[0, 0], "score", "Accuracy (rules found)", "Score (%)", fmt="{:.0f}%", ylim=(0, 105))
    plot_grouped_bar(axes[0, 1], "unique_keywords", "Search breadth", "Unique keywords")
    plot_grouped_bar(axes[1, 0], "doc_coverage_pct", "Document coverage", "Coverage (%)")
    plot_grouped_bar(axes[1, 1], "total_llm_calls", "Iterations used", "Total LLM calls")

    plt.tight_layout()
    plt.savefig("rlm_benchmark.png", dpi=150)
    print(f"\nBenchmark chart saved to rlm_benchmark.png")

    # --- Figure 2: Per-rule heatmap ---
    fig2, ax2 = plt.subplots(figsize=(14, 6))
    rule_names = [name for name, _ in RULE_CHECKERS]
    short_rules = [r[:35] + "..." if len(r) > 35 else r for r in rule_names]

    # Build heatmap data: rows = models+version, cols = rules
    # Values: FOUND=1, WRONG=-1, MISSED=0
    row_labels = []
    heatmap_data = []

    for version_label in versions:
        runs = version_runs.get(version_label, {})
        for m in models:
            r = runs.get(m)
            if not r:
                continue
            short = m.replace(":latest", "").replace(":14b", " 14B")
            row_labels.append(f"{short} ({version_label})")
            verdicts = r.get("rule_verdicts", {})
            row = []
            for rule_name in rule_names:
                v = verdicts.get(rule_name, "MISSED")
                row.append(1 if v == "FOUND" else (-1 if v == "WRONG" else 0))
            heatmap_data.append(row)

    if heatmap_data:
        heatmap_data = np.array(heatmap_data)
        from matplotlib.colors import ListedColormap
        cmap = ListedColormap(['#e74c3c', '#f0f0f0', '#2ecc71'])  # WRONG, MISSED, FOUND
        im = ax2.imshow(heatmap_data, cmap=cmap, vmin=-1, vmax=1, aspect='auto')

        ax2.set_xticks(range(len(short_rules)))
        ax2.set_xticklabels(short_rules, rotation=45, ha='right', fontsize=9)
        ax2.set_yticks(range(len(row_labels)))
        ax2.set_yticklabels(row_labels, fontsize=10)
        ax2.set_title("Per-Rule Results: Green=FOUND, Gray=MISSED, Red=WRONG", fontsize=13)

        # Add text annotations
        for i in range(len(row_labels)):
            for j in range(len(rule_names)):
                val = heatmap_data[i, j]
                text = "F" if val == 1 else ("W" if val == -1 else "M")
                color = "white" if val != 0 else "gray"
                ax2.text(j, i, text, ha='center', va='center', fontsize=10, fontweight='bold', color=color)

        plt.tight_layout()
        plt.savefig("rlm_rules_heatmap.png", dpi=150)
        print(f"Rules heatmap saved to rlm_rules_heatmap.png")


def main():
    with open("gpo_manual.txt", "r", encoding="utf-8") as f:
        context = f.read()
    print(f"Document loaded: {len(context)} characters")

    all_results = []
    for model in MODELS_TO_EVAL:
        result = run_eval(model, context)
        all_results.append(result)

    # Print comparison table
    print(f"\n{'='*60}")
    print(f"  COMPARISON RESULTS (v2 — with guardrails)")
    print(f"{'='*60}")
    print(f"  {'Model':<25} {'Score':>6} {'Calls':>6} {'Time':>8} {'Keywords':>9} {'Coverage':>9}")
    print(f"  {'-'*25} {'-'*6} {'-'*6} {'-'*8} {'-'*9} {'-'*9}")
    for r in all_results:
        print(f"  {r['model']:<25} {r['score']:>5.0%} {r['total_llm_calls']:>6} {r['time_seconds']:>7.1f}s {r['unique_keywords']:>9} {r['doc_coverage_pct']:>8.1f}%")

    # Generate charts
    print("\n--- Generating comparison charts ---")
    generate_comparison_chart()

    print(f"\nAll results saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()

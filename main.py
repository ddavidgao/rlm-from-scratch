import json
import os
import re
from datetime import datetime
from src.rlm import RLM

RESULTS_FILE = "run_results.json"

# --- DETERMINISTIC RULE CHECKERS ---
# Each checker is a tuple: (rule_name, check_function)
# check_function takes the answer string, returns "FOUND" / "MISSED" / "WRONG"
#   FOUND = correctly identified the rule
#   MISSED = didn't mention it
#   WRONG = mentioned the topic but got the correction backwards

def check_italic(ans):
    mentions = re.search(r'italic', ans, re.IGNORECASE)
    if not mentions:
        return "MISSED"
    # Must say NOT to italicize — check for negation near "italic"
    # Looks for "not italic", "don't italic", "no italic", "non-italic", "aren't italic"
    correct = re.search(r'(not?\s+italic|don.t\s+italic|no\s+italic|non.?italic)', ans, re.IGNORECASE)
    return "FOUND" if correct else "WRONG"

def check_uss_spacing(ans):
    # Correct: U. S. S. with spaces between
    correct = re.search(r'U\.\s+S\.\s+S\.', ans)
    if correct:
        return "FOUND"
    # Wrong: mentions U.S.S. without spaces (the incorrect format) as the recommendation
    wrong = re.search(r'U\.S\.S\.', ans)
    return "WRONG" if wrong else "MISSED"

def check_hyphen_foot(ans):
    # Must mention the hyphenated form "150-foot"
    correct = re.search(r'150-foot', ans, re.IGNORECASE)
    if correct:
        return "FOUND"
    # Wrong: mentions "150 foot" without hyphen as if it's fine
    wrong = re.search(r'hyphen', ans, re.IGNORECASE)
    # Mentioned hyphens but didn't get the specific correction
    return "WRONG" if wrong else "MISSED"

def check_navy_yard(ans):
    correct = re.search(r'navy-yard', ans, re.IGNORECASE)
    if correct:
        return "FOUND"
    # Mentioned "Navy Yard" without hyphen — noticed the topic but wrong
    wrong = re.search(r'navy\s+yard', ans, re.IGNORECASE)
    return "WRONG" if wrong else "MISSED"

def check_pa_abbrev(ans):
    correct = re.search(r'\bPa\.', ans)
    return "FOUND" if correct else "MISSED"

def check_lieut(ans):
    # Must mention the abbreviated form "Lieut." — not just "Lieutenant"
    correct = re.search(r'Lieut\.', ans)
    if correct:
        return "FOUND"
    # Just saying "Lieutenant Commander" isn't finding the abbreviation rule
    wrong = re.search(r'Lieutenant\s+Commander', ans)
    return "WRONG" if wrong else "MISSED"

def check_usn_spelled(ans):
    mentions_usn = re.search(r'United States Navy', ans)
    if not mentions_usn:
        return "MISSED"
    # FOUND if it says to keep spelled out / not abbreviate
    keep = re.search(r'(spell|keep|do not abbreviat|don.t abbreviat|written out|full)', ans, re.IGNORECASE)
    if keep:
        return "FOUND"
    # WRONG if it recommends abbreviating to U.S.N. or U. S. N.
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
    """Deterministic grading — no LLM needed. Returns (score_float, results_list)."""
    results = []
    found_count = 0
    for rule_name, checker in RULE_CHECKERS:
        verdict = checker(answer)
        if verdict == "FOUND":
            found_count += 1
        results.append((rule_name, verdict))
        print(f"  {verdict:6s}  {rule_name}")

    score = found_count / len(RULE_CHECKERS)
    print(f"\n  SCORE: {found_count}/{len(RULE_CHECKERS)} ({score:.0%})")
    return score, results


def save_result(run_data):
    """Append run data to results JSON file."""
    results = []
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r") as f:
            results = json.load(f)
    results.append(run_data)
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2)


def plot_results():
    """Generate scatter plot from all saved runs."""
    import matplotlib.pyplot as plt
    import pandas as pd

    if not os.path.exists(RESULTS_FILE):
        print("No results to plot yet.")
        return

    with open(RESULTS_FILE, "r") as f:
        results = json.load(f)

    if len(results) < 1:
        print("Need at least 1 run to plot.")
        return

    df = pd.DataFrame(results)

    # Color: oldest = red, newest = blue
    n = len(df)
    colors = [(1 - i/(max(n-1, 1)), 0, i/(max(n-1, 1))) for i in range(n)]

    fig, ax = plt.subplots(figsize=(10, 6))
    scatter = ax.scatter(
        df["total_llm_calls"],
        df["score"],
        c=colors,
        s=100,
        edgecolors="black",
        linewidth=0.5,
    )

    # Label each point with run number
    for i, row in df.iterrows():
        ax.annotate(f"#{row['run_id']}", (row["total_llm_calls"], row["score"]),
                    textcoords="offset points", xytext=(5, 5), fontsize=8)

    ax.set_xlabel("Total LLM Calls (root + sub)")
    ax.set_ylabel("Score (errors found / total)")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("RLM Performance: Effort vs Accuracy")
    ax.grid(True, alpha=0.3)

    # Legend for color
    ax.text(0.02, 0.98, "Red = older runs, Blue = newer runs",
            transform=ax.transAxes, fontsize=9, verticalalignment="top",
            style="italic", color="gray")

    plt.tight_layout()
    plt.savefig("rlm_performance.png", dpi=150)
    print("Plot saved to rlm_performance.png")
    plt.show()


# --- RUN ---
rlm = RLM()

with open("gpo_manual.txt", "r", encoding="utf-8") as f:
    context = f.read()

print(f"Context size: {len(context)} characters")

question = """I need to format this table entry for a government report:

"The U.S.S. Katahdin, a 150 foot gunboat with a 500 horsepower engine, stationed at the League Island Navy Yard in Pennsylvania, commanded by Lieutenant Commander R. W. Meade of the United States Navy."

According to this manual, what are ALL the formatting rules that apply to this entry, considering it will appear in a TABLE? List each rule and the correction needed."""

answer = rlm.completion(question, context)
print(f"\nFINAL ANSWER: {answer}")

# --- DETERMINISTIC GRADING ---
print("\n--- GRADING ---")
score, rule_results = score_answer(answer)

# --- BEHAVIORAL METRICS ---
behavior = rlm.get_behavior_stats(len(context))

# Calculate stats
total_calls = rlm.iterations + rlm.sub_llm_calls
time_seconds = rlm.time_spent / 1_000_000_000  # nanoseconds to seconds

# Determine run ID
run_id = 1
if os.path.exists(RESULTS_FILE):
    with open(RESULTS_FILE, "r") as f:
        existing = json.load(f)
        run_id = len(existing) + 1

run_data = {
    "run_id": run_id,
    "model": rlm.root_model,
    "timestamp": datetime.now().isoformat(),
    "total_llm_calls": total_calls,
    "root_iterations": rlm.iterations,
    "sub_llm_calls": rlm.sub_llm_calls,
    "time_seconds": round(time_seconds, 2),
    "score": round(score, 2),
    "unique_keywords": behavior["unique_keywords"],
    "repeated_keywords": behavior["repeated_keywords"],
    "chars_read": behavior["chars_read"],
    "doc_coverage_pct": behavior["doc_coverage_pct"],
    "keywords_searched": behavior["keywords_searched"],
    "rule_verdicts": {name: verdict for name, verdict in rule_results},
    "answer_preview": answer[:200],
}

save_result(run_data)

print(f"\n--- RUN #{run_id} ({rlm.root_model}) ---")
print(f"Root iterations:    {rlm.iterations}")
print(f"Sub-LLM calls:      {rlm.sub_llm_calls}")
print(f"Total LLM calls:    {total_calls}")
print(f"Time spent:          {time_seconds:.1f}s")
print(f"Score:               {score:.0%}")
print(f"Unique keywords:     {behavior['unique_keywords']}")
print(f"Repeated keywords:   {behavior['repeated_keywords']}")
print(f"Chars read:          {behavior['chars_read']}")
print(f"Doc coverage:        {behavior['doc_coverage_pct']}%")
print(f"Keywords:            {behavior['keywords_searched']}")
print(f"Results saved to {RESULTS_FILE}")

# Plot all results
plot_results()

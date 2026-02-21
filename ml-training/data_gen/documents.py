"""
Document registry and download management for training data generation.

Handles downloading Project Gutenberg texts, loading local documents,
and assembling the full document corpus used by the data generator.
"""

import os
import time
import urllib.request
import urllib.error
from pathlib import Path


GUTENBERG_TEXTS = [
    {
        "name": "cavalry_outpost",
        "url": "https://www.gutenberg.org/cache/epub/54515/pg54515.txt",
        "filename": "cavalry_outpost.txt",
    },
    {
        "name": "household_physician",
        "url": "https://www.gutenberg.org/cache/epub/31765/pg31765.txt",
        "filename": "household_physician.txt",
    },
    {
        "name": "boston_cooking_school",
        "url": "https://www.gutenberg.org/cache/epub/65063/pg65063.txt",
        "filename": "boston_cooking_school.txt",
    },
    {
        "name": "rules_of_road_sea",
        "url": "https://www.gutenberg.org/cache/epub/31357/pg31357.txt",
        "filename": "rules_of_road_sea.txt",
    },
    {
        "name": "cushings_manual",
        "url": "https://www.gutenberg.org/cache/epub/60757/pg60757.txt",
        "filename": "cushings_manual.txt",
    },
]

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2


def _strip_gutenberg_boilerplate(text: str) -> str:
    """Remove Project Gutenberg header and footer from a text.

    Strips everything before the '*** START OF' marker line and
    everything after the '*** END OF' marker line.
    """
    lines = text.splitlines(keepends=True)

    start_idx = 0
    end_idx = len(lines)

    for i, line in enumerate(lines):
        if "*** START OF" in line:
            start_idx = i + 1
            break

    for i, line in enumerate(lines):
        if "*** END OF" in line:
            end_idx = i
            break

    return "".join(lines[start_idx:end_idx]).strip()


def _download_with_retries(url: str, max_retries: int = MAX_RETRIES) -> str:
    """Download a URL's content as text, retrying on transient failures."""
    headers = {"User-Agent": "Mozilla/5.0 (training-data-gen)"}
    req = urllib.request.Request(url, headers=headers)

    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode("utf-8-sig")
        except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
            if attempt == max_retries:
                raise RuntimeError(
                    f"Failed to download {url} after {max_retries} attempts: {e}"
                ) from e
            print(f"  Attempt {attempt}/{max_retries} failed ({e}), retrying in {RETRY_DELAY_SECONDS}s...")
            time.sleep(RETRY_DELAY_SECONDS)

    # Unreachable, but satisfies type checkers
    raise RuntimeError(f"Failed to download {url}")


def download_gutenberg_texts(doc_dir: str) -> dict[str, str]:
    """Download all registered Gutenberg texts into doc_dir.

    Skips any text whose file already exists on disk.
    Returns a dict mapping document name -> absolute file path.
    """
    os.makedirs(doc_dir, exist_ok=True)
    paths: dict[str, str] = {}

    for entry in GUTENBERG_TEXTS:
        name = entry["name"]
        filepath = os.path.join(doc_dir, entry["filename"])
        paths[name] = filepath

        if os.path.exists(filepath):
            print(f"  [{name}] cached: {entry['filename']}")
            continue

        print(f"  [{name}] downloading from {entry['url']}...")
        raw_text = _download_with_retries(entry["url"])
        cleaned = _strip_gutenberg_boilerplate(raw_text)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(cleaned)

        print(f"  [{name}] saved ({len(cleaned):,} chars)")

    return paths


def load_document(path: str) -> str:
    """Read and return the full contents of a text file."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_all_documents(
    doc_dir: str,
    synthetic_docs: dict[str, str],
    gpo_path: str,
) -> dict[str, str]:
    """Assemble the complete document corpus for data generation.

    Combines three sources into a single name -> content mapping:
      1. Project Gutenberg texts (downloaded/cached into doc_dir)
      2. Synthetic documents (written to doc_dir as .txt files)
      3. The GPO style manual (loaded from gpo_path)

    Args:
        doc_dir: Directory for storing/caching document files.
        synthetic_docs: Dict mapping doc_name -> doc_content for
            programmatically generated documents.
        gpo_path: Path to gpo_manual.txt.

    Returns:
        Dict mapping document name -> full text content.
    """
    os.makedirs(doc_dir, exist_ok=True)
    all_docs: dict[str, str] = {}

    # 1. Gutenberg texts
    print("Loading Gutenberg texts...")
    gutenberg_paths = download_gutenberg_texts(doc_dir)
    for name, filepath in gutenberg_paths.items():
        all_docs[name] = load_document(filepath)

    # 2. Synthetic documents
    print(f"Loading {len(synthetic_docs)} synthetic document(s)...")
    for name, content in synthetic_docs.items():
        filepath = os.path.join(doc_dir, f"{name}.txt")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        all_docs[name] = content
        print(f"  [{name}] written ({len(content):,} chars)")

    # 3. GPO style manual
    print("Loading GPO style manual...")
    if os.path.exists(gpo_path):
        all_docs["gpo_manual"] = load_document(gpo_path)
        print(f"  [gpo_manual] loaded ({len(all_docs['gpo_manual']):,} chars)")
    else:
        print(f"  WARNING: GPO manual not found at {gpo_path}, skipping.")

    print(f"Total documents loaded: {len(all_docs)}")
    return all_docs

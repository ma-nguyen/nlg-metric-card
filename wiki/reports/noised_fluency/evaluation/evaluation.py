# Development of this software was supported in part by OpenAI ChatGPT.
import re
from pathlib import Path


def parse_changes(text: str):
    sections = {}
    current_section = None

    for line in text.splitlines():
        if line.startswith("Textual Description of"):
            current_section = line.replace("Textual Description of", "").strip()
            sections[current_section] = []

        match = re.search(r"change of (-?\d+\.?\d*)%", line)
        if match and current_section:
            change_val = float(match.group(1))
            sections[current_section].append(change_val)

    return sections


def compute_differences(sections):
    diffs = {}
    for sec, values in sections.items():
        diffs[sec] = []
        for i in range(len(values) - 1):
            diff = values[i + 1] - values[i]
            diffs[sec].append(diff)
    return diffs


def classify_change(max_abs_change: float) -> str:
    if max_abs_change < 25:
        return "low"
    elif max_abs_change < 60:
        return "moderate"
    else:
        return "high"

def main(file_path: str):
    print("=========== ANALYSIS REPORT ============")
    text = Path(file_path).read_text(encoding="utf-8")

    sections = parse_changes(text)
    diffs = compute_differences(sections)

    for sec in sections:
        max_abs_change = max(abs(v) for v in sections[sec])
        classification = classify_change(max_abs_change)

        print(f"\n=== {sec} ===")
        print("Change-Values:", [f"{v:.2f}" for v in sections[sec]])
        print("Differences (consecutive pairs):", [f"{d:.2f}" for d in diffs[sec]])
        print(f"Biggest absolute change: {max_abs_change:.2f}% → category: {classification}")


if __name__ == "__main__":
    main("input.txt")
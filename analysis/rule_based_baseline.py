"""Rule-based (non-LLM) metric-card baseline.

A deterministic template generator that derives card content purely from the score
tables by applying the documented threshold rules, with no LLM.
Its agreement with the lead author's v1 reference quantifies how much
of the LLM coverage in Table 2 is deterministic extraction.

Inputs
  * Score tables are parsed from the `gold_cards_v2/**/*.md` files
    (each card template embeds the exact numeric table the LLMs and
    both human annotators saw).
  * The v1 reference answers (lead author) are imported from
    `analysis/coverage_human_vs_human.py`, so the baseline is scored
    against the SAME primary reference as the LLM columns in Table 2.

Rules (identical to gold_cards_v2/README.md and the card templates)
  Noised fluency, per noise type:
    * monotonous decrease  = the score moves in the expected direction
      at every step as variation increases (expected direction is
      "increase" for perplexity metrics, "decrease" otherwise);
    * superlinear decrease = the per-step |Δ| grows at every step
      (the implicit gold→first-level step is included);
    * change rate          = by max |Δ%|: low iff ≤ NF_LOW_MAX,
      moderate iff ≤ NF_MOD_MAX, else high;
    * recommendation       = Yes iff more than NF_REC_MIN of the 10
      noise types have BOTH a high change rate AND a superlinear
      decrease.
  Noised fluency, compare card: a metric is recommended for a noise
    type iff it has both a high change rate and a superlinear decrease.
  Positioned error, single card (Q1-Q7 of the template):
    * Q1: Yes iff any perturbed variant scored above gold;
    * Q2: locations similar iff every variant has |Δ| < SIM;
    * Q3: shuffling vs. random similar iff every variant has |Δ| < SIM;
    * Q4 strengths   = variants with |Δ| ≥ HIGH;
    * Q5 weaknesses  = variants with |Δ| < HIGH;
    * Q6 recommendation = Yes iff more than POS_REC_MIN variants ≥ HIGH;
    * Q7 needs improvement = the weaknesses set.
  Positioned error, compare card:
    * recommendation  = metric with the most |Δ| ≥ HIGH variants;
    * anti-recommendation = metric with the fewest (ideally zero).

Outputs
  analysis/outputs/rule_based_per_card.csv
  analysis/outputs/rule_based_a_i.csv
  analysis/outputs/rule_based_a_sd.csv   <- Table 2 "RB" column
  plus a printed Table-2-comparable summary.

Usage
  python analysis/rule_based_baseline.py
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from coverage_human_vs_human import (  # noqa: E402
    GOLD, OUT, NOISE_ORDER,
    V1_NF_WIKI, V1_NF_SUM, V1_NF_WMT, V1_NF_TEDMT,
    V1_NF_WIKI_COMPARE, V1_NF_SUM_COMPARE, V1_NF_WMT_COMPARE,
    V1_NF_TEDMT_COMPARE,
    V1_POS_SINGLE, V1_POS_COMPARE,
    _set_agreement, _bin_agreement, _canon_metric,
)

ROOT = Path(__file__).resolve().parent.parent


# ------------------------------------------------------------------
#                            thresholds
# ------------------------------------------------------------------
@dataclass(frozen=True)
class Thresholds:
    """All numeric cutoffs used by the deterministic rules.

    The defaults reproduce the values used in the paper; the
    threshold-sensitivity check (analysis/threshold_sensitivity.py)
    varies them.
    """
    high: float = 70.0        # |Δ%| >= high  → high change rate (pos)
    sim: float = 10.0         # |Δ%| < sim    → "similar" (pos Q2/Q3)
    nf_low_max: float = 25.0  # NF change class: low iff max|Δ%| <= this
    nf_mod_max: float = 60.0  # NF change class: moderate iff <= this
    nf_rec_min: int = 7       # NF rec: Yes iff > this many high+super
    pos_rec_min: int = 5      # pos rec: Yes iff > this many >= high


DEFAULT = Thresholds()

# Metrics whose score is expected to INCREASE under noise.
_PPL_HINT = re.compile(r"ppl", re.IGNORECASE)


# ------------------------------------------------------------------
#                       score-table parsing
# ------------------------------------------------------------------
_NF_SECTION_RE = re.compile(r"^#### .*?\(`(?P<key>flu-[a-z]+)`\)", re.MULTILINE)
_NF_ROW_RE = re.compile(
    r"^\|\s*[^|]+\|\s*(?P<score>-?\d+(?:\.\d+)?)\s*"
    r"\|\s*(?P<edit>-?\d+(?:\.\d+)?)\s*"
    r"\|\s*(?P<delta>[+-]?\d+(?:\.\d+)?)%\s*\|",
    re.MULTILINE,
)
_POS_ROW_RE = re.compile(
    r"^\|\s*(?P<label>(?:Shuffling|Random)[^|]*?)\s*"
    r"\|\s*-?\d+(?:\.\d+)?\s*"
    r"\|\s*-?\d+(?:\.\d+)?\s*"
    r"\|\s*(?P<delta>[+-]?\d+(?:\.\d+)?)%\s*\|",
    re.MULTILINE,
)


def parse_nf_tables(path: Path) -> dict[str, list[float]]:
    """Per noise type, the Δ% sequence in increasing-variation order."""
    text = path.read_text(encoding="utf-8")
    # Only the score tables (before the annotation section) are input.
    text = text.split("## Your annotations")[0]
    out: dict[str, list[float]] = {}
    sections = _NF_SECTION_RE.split(text)
    # sections = [preamble, key1, body1, key2, body2, ...]
    for i in range(1, len(sections), 2):
        key, body = sections[i], sections[i + 1]
        deltas = [float(m["delta"]) for m in _NF_ROW_RE.finditer(body)]
        if not deltas:
            raise ValueError(f"no score rows for {key} in {path}")
        out[key] = deltas
    missing = set(NOISE_ORDER) - set(out)
    if missing:
        raise ValueError(f"missing noise sections in {path}: {missing}")
    return out


def parse_pos_table(path: Path) -> dict[str, float]:
    """Variant label ('shuffling-beg', ...) → Δ%."""
    text = path.read_text(encoding="utf-8").split("## Your annotations")[0]
    out: dict[str, float] = {}
    for m in _POS_ROW_RE.finditer(text):
        label = m["label"].lower().strip()
        label = re.sub(r"[\s,]+", "-", label)
        label = label.replace("beginning", "beg").replace("middle", "mid")
        out[label] = float(m["delta"])
    if len(out) != 6:
        raise ValueError(f"expected 6 pos variants in {path}, got {sorted(out)}")
    return out


# ------------------------------------------------------------------
#                     deterministic answer rules
# ------------------------------------------------------------------
def nf_classify(deltas: list[float], expect_increase: bool,
                th: Thresholds) -> tuple[str, str, str]:
    """(mono, super, change) for one noise type."""
    # Include the implicit gold step (Δ = 0) so that a wrong-direction
    # first level breaks monotonicity, exactly as a human reads it.
    seq = [0.0] + deltas
    if expect_increase:
        mono = all(b > a for a, b in zip(seq, seq[1:]))
    else:
        mono = all(b < a for a, b in zip(seq, seq[1:]))
    steps = [abs(b - a) for a, b in zip(seq, seq[1:])]
    super_ = len(steps) >= 2 and all(b > a for a, b in zip(steps, steps[1:]))
    peak = max(abs(d) for d in deltas)
    if peak <= th.nf_low_max:
        change = "l"
    elif peak <= th.nf_mod_max:
        change = "m"
    else:
        change = "h"
    return ("y" if mono else "n", "y" if super_ else "n", change)


def predict_nf_single(tables: dict[str, list[float]], metric_key: str,
                      th: Thresholds) -> tuple[list[tuple[str, str, str]], str]:
    expect_increase = bool(_PPL_HINT.search(metric_key))
    triples = [nf_classify(tables[n], expect_increase, th) for n in NOISE_ORDER]
    n_strong = sum(1 for (m, s, c) in triples if c == "h" and s == "y")
    rec = "y" if n_strong > th.nf_rec_min else "n"
    return triples, rec


def predict_nf_compare(single_preds: dict[str, list[tuple[str, str, str]]],
                       ) -> dict[str, set[str]]:
    """Per noise type, the set of metrics with high change + superlinear."""
    out: dict[str, set[str]] = {n: set() for n in NOISE_ORDER}
    for metric_key, triples in single_preds.items():
        for noise, (_m, s, c) in zip(NOISE_ORDER, triples):
            if c == "h" and s == "y":
                out[noise].add(metric_key)
    return out


def predict_pos_single(deltas: dict[str, float], th: Thresholds) -> dict[str, object]:
    strengths = {v for v, d in deltas.items() if abs(d) >= th.high}
    weaknesses = set(deltas) - strengths
    all_similar = all(abs(d) < th.sim for d in deltas.values())
    return {
        "1.1": "y" if any(d > 0 for d in deltas.values()) else "n",
        "1.2": "y" if all_similar else "n",
        "1.3": "y" if all_similar else "n",
        "2.1": strengths,
        "2.2": weaknesses,
        "2.3": "y" if len(strengths) > th.pos_rec_min else "n",
        "2.4": weaknesses,
    }


def predict_pos_compare(pos_deltas: dict[str, dict[str, float]],
                        th: Thresholds) -> dict[str, str]:
    counts = {m: sum(1 for d in deltas.values() if abs(d) >= th.high)
              for m, deltas in pos_deltas.items()}
    best = max(counts, key=lambda m: counts[m])
    worst = min(counts, key=lambda m: counts[m])
    return {"1": best, "2": worst}


# ------------------------------------------------------------------
#                      end-to-end prediction
# ------------------------------------------------------------------
NF_FAMILIES = [
    # (dataset label, directory, filename prefix, v1 single, v1 compare)
    ("wiki",  "noised_fluency_wiki",   "",      V1_NF_WIKI,  V1_NF_WIKI_COMPARE),
    ("sum",   "noised_fluency_sum_mt", "sum",   V1_NF_SUM,   V1_NF_SUM_COMPARE),
    ("wmt",   "noised_fluency_sum_mt", "wmt",   V1_NF_WMT,   V1_NF_WMT_COMPARE),
    ("tedmt", "noised_fluency_sum_mt", "tedmt", V1_NF_TEDMT, V1_NF_TEDMT_COMPARE),
]


def load_all_tables() -> dict:
    """Parse every score table once; predictions can then be recomputed
    for arbitrary thresholds without touching the filesystem again."""
    nf: dict[str, dict[str, dict[str, list[float]]]] = {}
    for ds, subdir, prefix, v1_single, _v1_cmp in NF_FAMILIES:
        nf[ds] = {}
        for metric_key in v1_single:
            fname = (f"{prefix}__{metric_key}_single.md" if prefix
                     else f"{metric_key}_single.md")
            path = GOLD / subdir / fname
            if not path.exists():
                print(f"  [warn] missing card template: {path}", file=sys.stderr)
                continue
            nf[ds][metric_key] = parse_nf_tables(path)
    pos = {metric_key: parse_pos_table(GOLD / "positioned_error" / f"{metric_key}_single.md")
           for metric_key in V1_POS_SINGLE}
    return {"nf": nf, "pos": pos}


def predict_all(tables: dict, th: Thresholds) -> dict:
    nf_single = {}   # (ds, metric) -> (triples, rec)
    nf_compare = {}  # ds -> {noise -> set(metric)}
    for ds, _subdir, _prefix, _v1_single, _v1_cmp in NF_FAMILIES:
        per_metric = {}
        for metric_key, tbl in tables["nf"][ds].items():
            per_metric[metric_key] = predict_nf_single(tbl, metric_key, th)
            nf_single[(ds, metric_key)] = per_metric[metric_key]
        nf_compare[ds] = predict_nf_compare(
            {m: triples for m, (triples, _r) in per_metric.items()})
    pos_single = {m: predict_pos_single(d, th) for m, d in tables["pos"].items()}
    pos_compare = predict_pos_compare(tables["pos"], th)
    return {"nf_single": nf_single, "nf_compare": nf_compare,
            "pos_single": pos_single, "pos_compare": pos_compare}


# ------------------------------------------------------------------
#                    scoring against the v1 reference
# ------------------------------------------------------------------
def score(preds: dict) -> dict:
    per_card_rows = []
    for ds, _subdir, _prefix, v1_single, v1_cmp in NF_FAMILIES:
        for metric_key, (v1_triples, v1_rec) in v1_single.items():
            if (ds, metric_key) not in preds["nf_single"]:
                continue
            p_triples, p_rec = preds["nf_single"][(ds, metric_key)]
            per_card_rows.append({
                "test": "noised_fluency", "size": "single",
                "dataset": ds, "metric": metric_key,
                "mono_n": 10,
                "mono_match": sum(a[0] == b[0] for a, b in zip(v1_triples, p_triples)),
                "super_n": 10,
                "super_match": sum(a[1] == b[1] for a, b in zip(v1_triples, p_triples)),
                "change_n": 10,
                "change_match": sum(a[2] == b[2] for a, b in zip(v1_triples, p_triples)),
                "rec_n": 1, "rec_match": int(v1_rec == p_rec),
            })

    compare_rows = []
    for ds, _subdir, _prefix, v1_single, v1_cmp in NF_FAMILIES:
        valid = set(v1_single.keys())
        p_cmp = preds["nf_compare"][ds]
        cell_match = sum(
            (m in v1_cmp[noise]) == (m in p_cmp[noise])
            for noise in NOISE_ORDER for m in valid)
        compare_rows.append({
            "test": "noised_fluency", "size": "compare", "dataset": ds,
            "metric": "(all)",
            "rec_cells_n": 10 * len(valid), "rec_cells_match": cell_match,
        })

    pos_single_rows = []
    for metric_key, v1_ans in V1_POS_SINGLE.items():
        p_ans = preds["pos_single"][metric_key]
        scores = {}
        for k, v1v in v1_ans.items():
            if isinstance(v1v, set):
                scores[k] = _set_agreement(v1v, p_ans[k])
            else:
                scores[k] = _bin_agreement(v1v, p_ans[k])
        pos_single_rows.append({
            "test": "positioned_error", "size": "single", "dataset": "wiki",
            "metric": metric_key,
            **{f"a_{k.replace('.', '_')}": scores[k] for k in v1_ans},
        })

    p_cmp = preds["pos_compare"]
    pos_compare_row = {
        "test": "positioned_error", "size": "compare", "dataset": "wiki",
        "metric": "(all)",
        "a_1": _bin_agreement(_canon_metric(V1_POS_COMPARE["1"]), _canon_metric(p_cmp["1"])),
        "a_2": _bin_agreement(_canon_metric(V1_POS_COMPARE["2"]), _canon_metric(p_cmp["2"])),
    }
    return {"nf_single": per_card_rows, "nf_compare": compare_rows,
            "pos_single": pos_single_rows, "pos_compare": pos_compare_row}


def aggregate(rows: dict) -> tuple[list[dict], list[tuple[str, float]]]:
    """Mirror the a_i / a_{s,d} aggregation of coverage_human_vs_human."""
    def avg(xs):
        xs = list(xs)
        return sum(xs) / len(xs) if xs else 0.0

    nf_single_a_i = {}
    for ds in ("wiki", "sum", "wmt", "tedmt"):
        cards = [r for r in rows["nf_single"] if r["dataset"] == ds]
        if not cards:
            continue
        n = len(cards)
        nf_single_a_i[ds] = {
            "mono":   sum(r["mono_match"] for r in cards) / (10 * n),
            "super":  sum(r["super_match"] for r in cards) / (10 * n),
            "change": sum(r["change_match"] for r in cards) / (10 * n),
            "rec":    sum(r["rec_match"] for r in cards) / n,
        }
    nf_compare_a_i = {r["dataset"]: r["rec_cells_match"] / r["rec_cells_n"]
                      for r in rows["nf_compare"]}

    pos_keys = ("1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "2.4")
    pos_a_i_mean = {
        k: avg(r[f"a_{k.replace('.', '_')}"] for r in rows["pos_single"])
        for k in pos_keys
    }
    pos_compare_a_i = {"1": rows["pos_compare"]["a_1"],
                       "2": rows["pos_compare"]["a_2"]}

    a_i_rows = []
    for ds, sub in nf_single_a_i.items():
        for instr, val in sub.items():
            a_i_rows.append({"family": "noised_fluency_single", "dataset": ds,
                             "instruction": instr, "a_i": val})
    for ds, val in nf_compare_a_i.items():
        a_i_rows.append({"family": "noised_fluency_compare", "dataset": ds,
                         "instruction": "rec_grid", "a_i": val})
    for instr, val in pos_a_i_mean.items():
        a_i_rows.append({"family": "positioned_error_single", "dataset": "wiki",
                         "instruction": instr, "a_i": val})
    for instr, val in pos_compare_a_i.items():
        a_i_rows.append({"family": "positioned_error_compare", "dataset": "wiki",
                         "instruction": instr, "a_i": val})

    nf_single_avg = {instr: avg(nf_single_a_i[ds][instr] for ds in nf_single_a_i)
                     for instr in ("mono", "super", "change", "rec")}
    sd_rows = [
        ("Retrieval (pos*)",
         avg([pos_a_i_mean["1.1"], pos_a_i_mean["1.2"], pos_a_i_mean["1.3"]])),
        ("Conclusion (pos* single)",
         avg([pos_a_i_mean["2.1"], pos_a_i_mean["2.2"],
              pos_a_i_mean["2.3"], pos_a_i_mean["2.4"]])),
        ("Conclusion (pos* compare)", avg(pos_compare_a_i.values())),
        ("Conclusion (single, fluency)", avg(nf_single_avg.values())),
        ("Conclusion (compare, fluency)", avg(nf_compare_a_i.values())),
        ("Human Likeness (pos*)",
         avg([pos_a_i_mean["1.2"], pos_a_i_mean["1.3"]])),
        ("Reduced Guidance (pos*)", pos_a_i_mean["2.4"]),
        ("Consistency (pos*)",
         abs(pos_a_i_mean["2.1"] - pos_a_i_mean["2.2"])),
    ]
    return a_i_rows, sd_rows


# ------------------------------------------------------------------
def main():
    OUT.mkdir(exist_ok=True)
    tables = load_all_tables()
    preds = predict_all(tables, DEFAULT)
    rows = score(preds)
    a_i_rows, sd_rows = aggregate(rows)

    per_card = (rows["nf_single"] + rows["nf_compare"]
                + rows["pos_single"] + [rows["pos_compare"]])
    fieldnames = sorted({k for r in per_card for k in r})
    with (OUT / "rule_based_per_card.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(per_card)

    with (OUT / "rule_based_a_i.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["family", "dataset", "instruction", "a_i"])
        w.writeheader()
        for r in a_i_rows:
            w.writerow({**r, "a_i": round(r["a_i"], 4)})

    with (OUT / "rule_based_a_sd.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dimension", "a_RB"])
        for dim, val in sd_rows:
            w.writerow([dim, round(val, 4)])

    print("Rule-based baseline vs. lead-author (v1) reference")
    print(f"(thresholds: {DEFAULT})\n")
    for dim, val in sd_rows:
        print(f"  {dim:<32} {100*val:5.1f}%")
    print("\nNote: 'pos*' rows cover the positioned-error family only —")
    print("the injection family has no v1 reference set (same coverage")
    print("as the a^HH column in Table 2, dagger footnote).")
    print(f"\nWrote: {OUT.relative_to(ROOT)}/rule_based_per_card.csv")
    print(f"Wrote: {OUT.relative_to(ROOT)}/rule_based_a_i.csv")
    print(f"Wrote: {OUT.relative_to(ROOT)}/rule_based_a_sd.csv")


if __name__ == "__main__":
    main()

"""Threshold sensitivity check for the metric-card content rules.

Recomputes the
deterministic card content (analysis/rule_based_baseline.py) under a
grid of alternative cutoffs and reports

  1. the fraction of subanswer labels that flip relative to the
     default thresholds (how much does the card content depend on the
     exact cutoff?), and
  2. the agreement with the lead-author v1 reference at each setting
     (would a different cutoff have changed the paper's conclusions?).

Counted subanswer labels (only independent decisions are counted;
answers that are deterministic complements of another answer, such as
weaknesses = ~strengths, are not double-counted):
  * positioned error, per card: 6 strength-membership labels,
    2 similarity verdicts (Q2, Q3), 1 higher-than-gold verdict,
    1 recommendation                        -> 10 per card, 3 cards
  * positioned error, compare: 2 labels (recommendation, anti-rec.)
  * noised fluency, per card: 10 mono + 10 superlinear + 10 change
    classes + 1 recommendation              -> 31 per card, 22 cards
  (the compare-card recommendation grid is derived from change+super
   and is therefore not counted a second time)

Outputs
  analysis/outputs/threshold_sensitivity.csv
  plus a printed summary table.

Usage
  python analysis/threshold_sensitivity.py
"""
from __future__ import annotations

from pathlib import Path
import csv
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from coverage_human_vs_human import NOISE_ORDER, OUT  # noqa: E402
from rule_based_baseline import (  # noqa: E402
    Thresholds, DEFAULT, load_all_tables, predict_all, score, aggregate,
)

ROOT = Path(__file__).resolve().parent.parent

# The grid: vary one family of cutoffs at a time around the defaults.
HIGH_GRID = [60.0, 65.0, 70.0, 75.0, 80.0]
SIM_GRID = [5.0, 10.0, 15.0]
NF_CLASS_GRID = [(15.0, 50.0), (20.0, 55.0), (25.0, 60.0),
                 (30.0, 65.0), (35.0, 70.0)]


def _labels(preds: dict) -> list[tuple]:
    """Flatten a prediction set into (id, label) pairs for flip counting."""
    out: list[tuple] = []
    for (ds, metric), (triples, rec) in sorted(preds["nf_single"].items()):
        for noise, (m, s, c) in zip(NOISE_ORDER, triples):
            out.append((("nf", ds, metric, noise, "mono"), m))
            out.append((("nf", ds, metric, noise, "super"), s))
            out.append((("nf", ds, metric, noise, "change"), c))
        out.append((("nf", ds, metric, "rec"), rec))
    for metric, ans in sorted(preds["pos_single"].items()):
        for variant in sorted(ans["2.1"] | ans["2.2"]):
            out.append((("pos", metric, variant, "strength"),
                        "y" if variant in ans["2.1"] else "n"))
        out.append((("pos", metric, "1.1"), ans["1.1"]))
        out.append((("pos", metric, "1.2"), ans["1.2"]))
        out.append((("pos", metric, "1.3"), ans["1.3"]))
        out.append((("pos", metric, "2.3"), ans["2.3"]))
    out.append((("pos", "compare", "rec"), preds["pos_compare"]["1"]))
    out.append((("pos", "compare", "antirec"), preds["pos_compare"]["2"]))
    return out


def _flip_fraction(base: list[tuple], other: list[tuple]) -> tuple[int, int]:
    base_map = dict(base)
    other_map = dict(other)
    assert base_map.keys() == other_map.keys(), "label universes diverge"
    flips = sum(1 for k in base_map if base_map[k] != other_map[k])
    return flips, len(base_map)


def main():
    OUT.mkdir(exist_ok=True)
    tables = load_all_tables()

    base_preds = predict_all(tables, DEFAULT)
    base_labels = _labels(base_preds)

    settings: list[Thresholds] = []
    for high in HIGH_GRID:
        settings.append(Thresholds(high=high))
    for sim in SIM_GRID:
        settings.append(Thresholds(sim=sim))
    for low, mod in NF_CLASS_GRID:
        settings.append(Thresholds(nf_low_max=low, nf_mod_max=mod))

    rows = []
    for th in settings:
        preds = predict_all(tables, th)
        flips, total = _flip_fraction(base_labels, _labels(preds))
        _a_i, sd = aggregate(score(preds))
        sd_map = dict(sd)
        rows.append({
            "high": th.high, "sim": th.sim,
            "nf_low_max": th.nf_low_max, "nf_mod_max": th.nf_mod_max,
            "is_default": th == DEFAULT,
            "labels_total": total, "labels_flipped": flips,
            "flip_pct": round(100 * flips / total, 2),
            "a_RB_retrieval_pos": round(100 * sd_map["Retrieval (pos*)"], 1),
            "a_RB_conclusion_pos_single":
                round(100 * sd_map["Conclusion (pos* single)"], 1),
            "a_RB_conclusion_nf_single":
                round(100 * sd_map["Conclusion (single, fluency)"], 1),
            "a_RB_conclusion_nf_compare":
                round(100 * sd_map["Conclusion (compare, fluency)"], 1),
        })

    out_path = OUT / "threshold_sensitivity.csv"
    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("Threshold sensitivity (label flips vs. default thresholds)\n")
    print(f"{'high':>5} {'sim':>4} {'nf_low':>6} {'nf_mod':>6} "
          f"{'flipped':>8} {'flip%':>6}   note")
    for r in rows:
        note = "<- default" if r["is_default"] else ""
        print(f"{r['high']:>5.0f} {r['sim']:>4.0f} {r['nf_low_max']:>6.0f} "
              f"{r['nf_mod_max']:>6.0f} "
              f"{r['labels_flipped']:>4}/{r['labels_total']:<4} "
              f"{r['flip_pct']:>5.1f}%   {note}")
    max_flip = max(r["flip_pct"] for r in rows if not r["is_default"])
    print(f"\nMax flip rate across the grid: {max_flip:.1f}% "
          f"(use this for the sentence in Sec. 4 / Appendix)")
    print(f"Wrote: {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

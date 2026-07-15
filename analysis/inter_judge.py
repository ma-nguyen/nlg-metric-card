"""Pairwise Spearman correlations between LLM judges, plus comparison to
judge-vs-human correlation. Tests whether the three judges agree with each
other more than they agree with human raters — direct evidence of shared
LLM bias if they do.

Reads from analysis/outputs/merged_ratings_per_card.csv (produced by
correlate.py with --judges for all three providers).
"""
import argparse
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr

DIMENSIONS = [
    "Structure", "Precision", "Understandability", "Objectivity",
    "Usefulness", "Language", "Factual Accuracy",
]


def _spearman(x, y):
    r = spearmanr(x, y)
    return float(getattr(r, "statistic", r[0])), float(getattr(r, "pvalue", r[1]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--merged", default="analysis/outputs/merged_ratings_per_card.csv")
    ap.add_argument("--out-dir", default="analysis/outputs")
    args = ap.parse_args()

    merged = pd.read_csv(args.merged)
    providers = sorted(merged.provider.unique())

    pivot = (merged
             .pivot_table(index=["card_id", "condition", "dimension"],
                          columns="provider", values="judge_mean")
             .reset_index())

    inter_rows = []
    for p1, p2 in combinations(providers, 2):
        for dim in DIMENSIONS:
            sub = pivot[pivot.dimension == dim].dropna(subset=[p1, p2])
            if len(sub) < 3:
                continue
            sp, pval = _spearman(sub[p1].values, sub[p2].values)
            inter_rows.append({
                "pair": f"{p1}--{p2}",
                "dimension": dim,
                "spearman": sp,
                "p": pval,
                "n": int(len(sub)),
            })
    inter = pd.DataFrame(inter_rows)

    human_pivot = (merged.drop_duplicates(subset=["card_id", "dimension"])
                          [["card_id", "dimension", "human_mean"]])
    judge_human_rows = []
    for prov in providers:
        for dim in DIMENSIONS:
            sub = (pivot[pivot.dimension == dim]
                   [["card_id", prov]]
                   .merge(human_pivot[human_pivot.dimension == dim],
                          on="card_id"))
            if len(sub) < 3:
                continue
            sp, pval = _spearman(sub[prov].values, sub.human_mean.values)
            judge_human_rows.append({
                "pair": f"{prov}--human",
                "dimension": dim,
                "spearman": sp,
                "p": pval,
                "n": int(len(sub)),
            })
    jh = pd.DataFrame(judge_human_rows)

    out = Path(args.out_dir)
    inter.to_csv(out / "inter_judge_correlations.csv", index=False)
    jh.to_csv(out / "judge_human_correlations.csv", index=False)

    print("--- Inter-judge Spearman per dimension ---")
    print(inter.pivot(index="dimension", columns="pair", values="spearman")
              .reindex(DIMENSIONS).round(2).to_string())

    print("\n--- Judge-vs-human Spearman per dimension ---")
    print(jh.pivot(index="dimension", columns="pair", values="spearman")
            .reindex(DIMENSIONS).round(2).to_string())

    print("\n--- Mean Spearman across 7 dims ---")
    means = pd.concat([
        inter.groupby("pair")["spearman"].mean(),
        jh.groupby("pair")["spearman"].mean(),
    ]).round(3)
    print(means.to_string())
    print(f"\n  Mean inter-judge   : {inter['spearman'].mean():.3f} (n={len(inter)} cells)")
    print(f"  Mean judge--human  : {jh['spearman'].mean():.3f} (n={len(jh)} cells)")


if __name__ == "__main__":
    main()

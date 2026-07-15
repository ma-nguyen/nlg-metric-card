"""Correlate human-mean ratings with one or more LLM-judge ratings.

Per (provider, dimension): Spearman + Pearson with bootstrapped 95% CIs (n=2000).
Also: FS-vs-ABLMC mean differences per provider, and per-dimension scatter
plots (one per provider).

Pass one or more judge CSVs via --judges. Each must have a `provider` column
(set automatically by judge_*.py); legacy single-provider CSVs without that
column are tagged "deepseek" by default for backward compatibility.
"""
import argparse
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
    return float(getattr(r, "statistic", r[0]))


def _pearson(x, y):
    return float(pearsonr(x, y)[0])


def bootstrap_ci(x, y, fn, n=2000, seed=0, alpha=0.05):
    rng = np.random.default_rng(seed)
    out = np.empty(n)
    for i in range(n):
        idx = rng.integers(0, len(x), size=len(x))
        try:
            out[i] = fn(x[idx], y[idx])
        except Exception:
            out[i] = np.nan
    lo = float(np.nanpercentile(out, 100 * alpha / 2))
    hi = float(np.nanpercentile(out, 100 * (1 - alpha / 2)))
    return lo, hi


def load_judges(paths):
    frames = []
    for p in paths:
        df = pd.read_csv(p)
        if "provider" not in df.columns:
            df["provider"] = Path(p).stem.replace("_ratings", "")
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--human", default="analysis/outputs/human_ratings_long.csv")
    ap.add_argument("--judges", nargs="+",
                    default=["analysis/outputs/deepseek_ratings.csv"],
                    help="One or more judge CSVs")
    ap.add_argument("--out", default="analysis/outputs")
    ap.add_argument("--bootstrap", type=int, default=2000)
    ap.add_argument("--no-plots", action="store_true")
    args = ap.parse_args()

    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)

    h = pd.read_csv(args.human)
    j = load_judges(args.judges)

    h_mean = (h.groupby(["card_id", "condition", "dimension"])["score"]
                .mean().rename("human_mean").reset_index())
    j_mean = (j.groupby(["provider", "card_id", "condition", "dimension"])["score"]
                .mean().rename("judge_mean").reset_index())
    j_std  = (j.groupby(["provider", "card_id", "condition", "dimension"])["score"]
                .std().rename("judge_std").reset_index())

    merged = (j_mean
              .merge(j_std,  on=["provider", "card_id", "condition", "dimension"])
              .merge(h_mean, on=["card_id", "condition", "dimension"]))
    merged.to_csv(out / "merged_ratings_per_card.csv", index=False)

    rows = []
    for provider in sorted(merged["provider"].unique()):
        for dim in DIMENSIONS:
            sub = merged[(merged.provider == provider) & (merged.dimension == dim)]
            if len(sub) < 3:
                continue
            x = sub.human_mean.values; y = sub.judge_mean.values
            sp = _spearman(x, y); pe = _pearson(x, y)
            sp_res = spearmanr(x, y)
            sp_p = float(getattr(sp_res, "pvalue", sp_res[1]))
            pe_p = float(pearsonr(x, y)[1])
            sp_lo, sp_hi = bootstrap_ci(x, y, _spearman, n=args.bootstrap)
            pe_lo, pe_hi = bootstrap_ci(x, y, _pearson,  n=args.bootstrap, seed=1)
            rows.append({
                "provider": provider, "dimension": dim, "n": int(len(sub)),
                "spearman": sp, "spearman_p": sp_p,
                "spearman_lo": sp_lo, "spearman_hi": sp_hi,
                "pearson":  pe, "pearson_p":  pe_p,
                "pearson_lo":  pe_lo, "pearson_hi":  pe_hi,
            })
    corr = pd.DataFrame(rows)
    corr.to_csv(out / "correlations_per_dimension.csv", index=False)

    fs_v = (merged.groupby(["provider", "condition", "dimension"])
                  .agg(human_mean=("human_mean", "mean"),
                       judge_mean=("judge_mean", "mean"))
                  .reset_index())
    fs_v.to_csv(out / "fs_vs_ablmc_means.csv", index=False)

    if not args.no_plots:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            for provider in sorted(merged["provider"].unique()):
                for dim in DIMENSIONS:
                    sub = merged[(merged.provider == provider)
                                 & (merged.dimension == dim)]
                    if sub.empty:
                        continue
                    fig, ax = plt.subplots(figsize=(4, 4))
                    for cond, mk in [("FS", "o"), ("ABLMC", "s")]:
                        s = sub[sub.condition == cond]
                        ax.scatter(s.human_mean, s.judge_mean, marker=mk, label=cond)
                        for _, r in s.iterrows():
                            ax.annotate(int(r.card_id),
                                        (r.human_mean, r.judge_mean),
                                        textcoords="offset points",
                                        xytext=(4, 4), fontsize=8)
                    ax.plot([1, 5], [1, 5], "--", alpha=0.3, color="grey")
                    ax.set_xlim(0.5, 5.5); ax.set_ylim(0.5, 5.5)
                    ax.set_xlabel("Human mean")
                    ax.set_ylabel(f"{provider} mean")
                    ax.set_title(f"{provider} · {dim}")
                    ax.legend(); fig.tight_layout()
                    fname = f"scatter_{provider}_{dim.replace(' ', '_')}.png"
                    fig.savefig(out / fname, dpi=140)
                    plt.close(fig)
        except ImportError:
            print("matplotlib not installed; skipping plots")

    print("\n--- Correlations (n=8 cards per dimension) ---")
    print(corr.round(3).to_string(index=False))
    print(f"\nSaved -> {out/'correlations_per_dimension.csv'}")


if __name__ == "__main__":
    main()

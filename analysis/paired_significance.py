"""Paired significance tests on per-author FS vs ABLMC quality ratings,
plus a paired test on the per-author time ratio tr_i = t_ABLMC / t_FS.

Quality test (the original): loads `analysis/outputs/human_summary_by_card.csv`
(per-card means already averaged across the two external raters) and
computes within-author (FS - ABLMC) deltas, then runs Wilcoxon
signed-rank, sign test, paired t, and Cohen's dz, both overall (mean
over 7 Likert dimensions) and per-dimension.

Time test: tr_i values are taken from Table 1a of main.tex (n=4
participants). H0: median(tr_i) = 1 (no time saving). Same suite of
tests; we report the same `smallest attainable two-sided p = 0.125`
caveat — the point is honest non-significance, not significance.

With n=4 paired observations every test is severely underpowered
(Wilcoxon two-sided p cannot drop below 0.125, sign test below 0.125).
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

DIMS = ["Structure", "Precision", "Understandability",
        "Objectivity", "Usefulness", "Language", "Factual Accuracy"]
PAIRS = [(3, 1, "P1"), (6, 2, "P2"), (7, 4, "P3"), (8, 5, "P4")]

# Per-participant ABLMC/FS time ratio from Table 1a of main.tex.
# (P1, P2, P3, P4 in order.)
TIME_RATIOS = np.array([1.26, 1.12, 1.35, 0.92])


def main():
    here = Path(__file__).resolve().parent
    out = here / "outputs"
    df = pd.read_csv(out / "human_summary_by_card.csv")

    df["overall"] = df[DIMS].mean(axis=1)
    overall = dict(zip(df.card_id, df.overall))

    rows = []
    deltas = np.array([overall[fs] - overall[ab] for fs, ab, _ in PAIRS])
    rows.append(_test_row("Overall (mean of 7 dims)", deltas))

    for dim in DIMS:
        s = df.set_index("card_id")[dim]
        d = np.array([s[fs] - s[ab] for fs, ab, _ in PAIRS])
        rows.append(_test_row(dim, d))

    # Time-ratio test. Sign convention: positive delta = ABLMC slower (so a
    # positive mean argues *against* time-saving). We test H0: median tr = 1.
    rows.append(_test_row("Time ratio tr - 1 (ABLMC slower if >0)",
                          TIME_RATIOS - 1.0))

    res = pd.DataFrame(rows)
    res.to_csv(out / "fs_vs_ablmc_paired_tests.csv", index=False)
    print(res.to_string(index=False))


def _test_row(name, d):
    n = len(d); npos = int(np.sum(d > 0)); nneg = int(np.sum(d < 0))
    try:
        w, wp = stats.wilcoxon(d, alternative="two-sided", zero_method="wilcox")
    except ValueError:
        w, wp = float("nan"), float("nan")
    sp = stats.binomtest(min(npos, nneg), npos + nneg, 0.5).pvalue \
        if (npos + nneg) > 0 else float("nan")
    t, tp = stats.ttest_rel(d + 0, np.zeros_like(d)) \
        if d.std(ddof=1) > 0 else (float("nan"), float("nan"))
    dz = d.mean() / d.std(ddof=1) if d.std(ddof=1) > 0 else float("nan")
    return {
        "metric": name,
        "n": n,
        "mean_delta_fs_minus_ablmc": round(float(d.mean()), 3),
        "sd_delta": round(float(d.std(ddof=1)), 3),
        "n_pos": npos, "n_neg": nneg,
        "wilcoxon_W": round(float(w), 3) if not np.isnan(w) else None,
        "wilcoxon_p_two_sided": round(float(wp), 4) if not np.isnan(wp) else None,
        "sign_test_p_two_sided": round(float(sp), 4),
        "paired_t": round(float(t), 3) if not np.isnan(t) else None,
        "paired_t_p_two_sided": round(float(tp), 4) if not np.isnan(tp) else None,
        "cohens_dz": round(float(dz), 3) if not np.isnan(dz) else None,
    }


if __name__ == "__main__":
    main()

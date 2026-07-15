"""Parse the Google-Form CSV with subjective Metric Card ratings.

Outputs to --out-dir:
- human_ratings_long.csv         : tidy long-form
- human_summary_by_condition.csv : mean/std/n by (condition, dimension)
- human_summary_by_card.csv      : per-card means across annotators
- human_iaa_per_dimension.csv    : Cohen's linearly-weighted kappa per dim
- human_iaa_overall.csv          : Krippendorff's alpha (ordinal) overall
"""
import argparse
import csv
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

DIMENSIONS = [
    "Structure", "Precision", "Understandability", "Objectivity",
    "Usefulness", "Language", "Factual Accuracy",
]
DIM_PREFIXES = {d.lower(): d for d in DIMENSIONS}
LIKERT_RE = re.compile(r"^\((\d)\)")

DEFAULT_MAPPING = {
    1: ("ABLMC", "BARTScore-avg-f", "InjTest_ABLMC_1.docx"),
    2: ("ABLMC", "BARTScore-avg-f", "InjTest_ABLMC_2.docx"),
    3: ("FS",    "ROUGE-L",         "InjTest_FS_1.docx"),
    4: ("ABLMC", "BARTScore-avg-f", "InjTest_ABLMC_3.docx"),
    5: ("ABLMC", "BARTScore-avg-f", "InjTest_ABLMC_4.docx"),
    6: ("FS",    "ROUGE-L",         "InjTest_FS_2.docx"),
    7: ("FS",    "ROUGE-L",         "InjTest_FS_3.docx"),
    8: ("FS",    "ROUGE-L",         "InjTest_FS_4.docx"),
}


def parse_likert(s):
    m = LIKERT_RE.match((s or "").strip())
    return int(m.group(1)) if m else None


def header_to_dimension(h):
    h = (h or "").strip().lower()
    for prefix, name in DIM_PREFIXES.items():
        if h.startswith(prefix + ":"):
            return name
    return None


def parse_card_id(s):
    m = re.match(r"\s*(\d+)", s or "")
    return int(m.group(1)) if m else None


def parse_csv(csv_path):
    with open(csv_path, encoding="utf-8") as f:
        header = next(csv.reader(f))

    blocks = []
    for i, col in enumerate(header):
        if "Enter Number" in col:
            blocks.append({"id_col": i, "dim_cols": []})
        elif blocks and len(blocks[-1]["dim_cols"]) < 7:
            dim = header_to_dimension(col)
            if dim:
                blocks[-1]["dim_cols"].append((i, dim))

    if len(blocks) != 8 or any(len(b["dim_cols"]) != 7 for b in blocks):
        raise ValueError(
            f"Header parse failed: got {len(blocks)} blocks, sizes "
            f"{[len(b['dim_cols']) for b in blocks]}"
        )

    block_order_card_id = [None] * len(blocks)

    rows = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for ann_idx, row in enumerate(reader):
            if not any(c.strip() for c in row):
                continue
            for bi, b in enumerate(blocks):
                cid = parse_card_id(row[b["id_col"]])
                if cid is None:
                    cid = block_order_card_id[bi]
                else:
                    if block_order_card_id[bi] is None:
                        block_order_card_id[bi] = cid
                if cid is None:
                    continue
                for col_i, dim in b["dim_cols"]:
                    score = parse_likert(row[col_i])
                    if score is None:
                        continue
                    rows.append({
                        "annotator": f"A{ann_idx + 1}",
                        "timestamp": row[0],
                        "card_id": cid,
                        "dimension": dim,
                        "score": score,
                    })
    return pd.DataFrame(rows)


def add_condition(df, mapping):
    df = df.copy()
    df["condition"]   = df["card_id"].map(lambda c: mapping[c][0])
    df["metric"]      = df["card_id"].map(lambda c: mapping[c][1])
    df["source_file"] = df["card_id"].map(lambda c: mapping[c][2])
    return df


def cohen_weighted_kappa(a, b, n_categories=5):
    a = np.asarray(a); b = np.asarray(b)
    mask = ~(np.isnan(a) | np.isnan(b))
    a = a[mask].astype(int); b = b[mask].astype(int)
    cats = np.arange(1, n_categories + 1)
    O = np.zeros((n_categories, n_categories))
    for x, y in zip(a, b):
        O[x - 1, y - 1] += 1
    n = O.sum()
    if n == 0:
        return float("nan")
    O = O / n
    pa = O.sum(axis=1); pb = O.sum(axis=0)
    E = np.outer(pa, pb)
    W = 1 - np.abs(np.subtract.outer(cats, cats)) / (n_categories - 1)
    denom = 1 - np.sum(W * E)
    if denom == 0:
        return float("nan")
    return float((np.sum(W * O) - np.sum(W * E)) / denom)


def per_dimension_iaa(df):
    rows = []
    for dim in DIMENSIONS:
        wide = (df[df.dimension == dim]
                .pivot_table(index="card_id", columns="annotator", values="score"))
        if wide.shape[1] < 2:
            continue
        a = wide.iloc[:, 0].values; b = wide.iloc[:, 1].values
        valid = ~(np.isnan(a) | np.isnan(b))
        a_v = a[valid]; b_v = b[valid]
        pearson = (float(np.corrcoef(a_v, b_v)[0, 1])
                   if len(a_v) > 1 and np.std(a_v) > 0 and np.std(b_v) > 0
                   else float("nan"))
        rows.append({
            "dimension": dim,
            "weighted_kappa": cohen_weighted_kappa(a, b),
            "pearson": pearson,
            "n_pairs": int(valid.sum()),
        })
    return pd.DataFrame(rows)


def krippendorff_alpha_overall(df):
    import krippendorff
    pivot = df.pivot_table(
        index="annotator", columns=["card_id", "dimension"], values="score"
    )
    return float(krippendorff.alpha(
        reliability_data=pivot.values, level_of_measurement="ordinal"
    ))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="MetricCardEvaluation - Formularantworten 1.csv")
    ap.add_argument("--out-dir", default="analysis/outputs")
    ap.add_argument("--mapping", default=None,
                    help="Optional JSON file overriding card_id -> "
                         "[condition, metric, file]")
    args = ap.parse_args()

    mapping = DEFAULT_MAPPING
    if args.mapping:
        with open(args.mapping) as f:
            mapping = {int(k): tuple(v) for k, v in json.load(f).items()}

    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)

    df = add_condition(parse_csv(args.csv), mapping)
    df.to_csv(out / "human_ratings_long.csv", index=False)

    s_cond = (df.groupby(["condition", "dimension"])["score"]
                .agg(["mean", "std", "count"]))
    s_cond.to_csv(out / "human_summary_by_condition.csv")

    s_card = (df.groupby(["card_id", "condition", "dimension"])["score"]
                .mean().unstack("dimension"))
    s_card.to_csv(out / "human_summary_by_card.csv")

    iaa = per_dimension_iaa(df)
    iaa.to_csv(out / "human_iaa_per_dimension.csv", index=False)
    pd.DataFrame([{
        "krippendorff_alpha_ordinal": krippendorff_alpha_overall(df),
        "n_annotators": df.annotator.nunique(),
        "n_items": df.groupby(["card_id", "dimension"]).ngroups,
    }]).to_csv(out / "human_iaa_overall.csv", index=False)

    print(f"Wrote {len(df)} rows to {out/'human_ratings_long.csv'}")
    print("\n--- Mean ratings by condition ---")
    print(s_cond.round(2))
    print("\n--- IAA per dimension (Cohen weighted kappa, Pearson) ---")
    print(iaa.round(3).to_string(index=False))


if __name__ == "__main__":
    main()

"""Generate fillable Markdown templates for the second-annotator gold cards.

Reads the existing prompt templates and per-metric values used by the
LLM-card pipeline, renders them with score-change percentages computed
the same way as the production scripts, and writes a Markdown stub
under `gold_cards_v2/<test>/...md` with empty answer slots.

The user (second annotator) opens each stub, fills in answers in place,
and saves. They must NOT consult `*/evaluation/*.pdf` (lead author's
cards) while annotating — that would contaminate the human-human
ceiling. See `gold_cards_v2/README.md`.

Currently implemented:
- positioned_error single (WikiText-103, 3 metrics)
- positioned_error compare (WikiText-103, 1 card)
- noised_fluency_wiki single (WikiText-103, 4 metrics)
- noised_fluency_wiki compare (WikiText-103, 1 card)

Easy to extend to noised_fluency_sum_mt by adding a similar block; the
templates and JSON score files live under
  sum_mt/reports/noised_fluency/prompt_templates/{sum,wmt,tedmt}_{pt,cpt}.txt
  sum_mt/score_saves/{sum,wmt-de-en,ted-zh-en}/<metric>/flu-*.json
"""
from pathlib import Path
import argparse
import json
import re

ROOT = Path(__file__).resolve().parent.parent
OUT  = ROOT / "gold_cards_v2"

# CLI-controlled flag: when False (default), existing files are kept as-is so
# that filled-in annotations are never silently overwritten. Pass --force to
# regenerate everything.
FORCE = False

def _safe_write(path: Path, content: str) -> None:
    """Write `content` to `path` only if it would not destroy human edits.

    Behaviour:
      * If the file does not exist → write it.
      * If the file exists and matches `content` exactly → no-op (silent).
      * If the file exists and differs from `content` in any way → skip with
        a warning. The differing bytes are assumed to be human annotations
        and must not be clobbered. Use --force to override.

    Exact-match is deliberately strict: any difference at all (filled
    answer, manually-tweaked wording, even a stray newline) blocks the
    write. This is the right default for an annotation-collection workflow
    where the cost of losing answers vastly outweighs the cost of telling
    the user to pass --force when they actually want a regeneration.
    """
    try:
        rel = path.relative_to(ROOT)
    except ValueError:
        rel = path
    if path.exists() and not FORCE:
        existing = path.read_text(encoding="utf-8")
        if existing == content:
            return  # already up to date, no-op
        print(f"  skip {rel} (exists and differs — pass --force to overwrite)")
        return
    path.write_text(content, encoding="utf-8")
    print(f"  wrote {rel}")

# ---------- Helpers shared with the production scripts -------------------

def calc_change(result: float, ref: float) -> float:
    return (result - ref) / abs(ref) * 100.0


def load_kv(path: Path) -> dict:
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


# ---------- Positioned-error single (per-metric) -------------------------

POS_KEYS = [
    ("shuffling_beginning", "Shuffling, Beginning"),
    ("shuffling_middle",    "Shuffling, Middle"),
    ("shuffling_end",       "Shuffling, End"),
    ("random_beginning",    "Random,    Beginning"),
    ("random_middle",       "Random,    Middle"),
    ("random_end",          "Random,    End"),
]

POS_SINGLE_INSTRUCTIONS = [
    ("Did a perturbed output score higher than the gold output? "
     "If yes, which one?", "list"),
    ("Were the scores similar for every location (beginning, middle, end)? "
     "Yes iff every individual location-score has |change| < 10%. "
     "Answer with `Yes` or `No` only -- no list.", "binary"),
    ("Were the scores similar between the shuffling-test and the random-test? "
     "Yes iff every individual variant has |change| < 10%. "
     "Answer with `Yes` or `No` only -- no list.", "binary"),
    ("**Strengths.** List every variation with high change rate or higher (≥70%).",
     "list"),
    ("**Weaknesses.** List every variation without high change rate or higher (<70%).",
     "list"),
    ("**Recommendation.** Yes if the metric has more than 5 variants with ≥70% change, "
     "else No.", "binary"),
    ("What needs improvement? (List positional variants where the metric did "
     "not reach a near-minimal score.)", "list"),
]


def render_positioned_error_single():
    out_dir = OUT / "positioned_error"
    out_dir.mkdir(parents=True, exist_ok=True)
    values_dir = ROOT / "wiki" / "reports" / "positioned_error" / "results_single_values"

    for vfile in sorted(values_dir.glob("*.txt")):
        v = load_kv(vfile)
        ref = float(v["ref"])
        metric = v["metric"]
        info = v.get("Additional Information", "")

        # Build score table
        table_rows = ["| Variant                | Gold     | Perturbed | Δ (%)      |",
                      "|------------------------|----------|-----------|------------|"]
        for key, label in POS_KEYS:
            res = float(v[f"result_{key}"])
            chg = calc_change(res, ref)
            table_rows.append(
                f"| {label:<22} | {ref:>8.4f} | {res:>9.4f} | {chg:>+9.2f}% |"
            )
        table = "\n".join(table_rows)

        # Build instruction sections with empty answer slots
        instr_blocks = []
        for i, (instr, kind) in enumerate(POS_SINGLE_INSTRUCTIONS, 1):
            slot = "_Your answer (Yes/No):_" if kind == "binary" else "_Your answer:_"
            instr_blocks.append(f"### {i}. {instr}\n\n{slot}\n\n\n")

        md = f"""# Gold Card v2 — Positioned Error Test, WikiText-103
## Metric: {metric} (single-metric card)

> **Annotator instructions.** Do not open `wiki/reports/positioned_error/evaluation/Positional_Error_Evaluation.pdf` while filling this in. Use only the score table below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** {info}

**Task:** open-ended text generation
**Dataset:** WikiText-103, 1000 paragraphs (~256 tokens each)
**Perturbation:** 10 consecutive tokens at the beginning, middle, or end of each gold paragraph are either shuffled (shuffling-test) or replaced with random vocabulary tokens (random-test).

**Test results:**

{table}

---

## Your annotations

{''.join(instr_blocks)}
"""
        outfile = out_dir / f"{vfile.stem}_single.md"
        _safe_write(outfile, md)


# ---------- Positioned-error compare (across metrics) --------------------

POS_COMPARE_INSTRUCTIONS = [
    ("**Recommendation.** Name the metric with the most high-change-rate variants (≥70%) "
     "overall.", "list"),
    ("**Anti-recommendation.** Explicitly state which metric you would NOT recommend, "
     "and why. A human would not recommend a metric whose variations have no high "
     "change rates.", "list"),
]


def render_positioned_error_compare():
    out_dir = OUT / "positioned_error"
    out_dir.mkdir(parents=True, exist_ok=True)
    cval_path = ROOT / "wiki" / "reports" / "positioned_error" / "results_compare_values" / "positioned_error_cval.txt"
    v = load_kv(cval_path)
    metrics = re.split(r"\s+", v["metrics"].strip())
    refs = list(map(float, v["ref"].split()))
    info = v.get("Additional Information", "")

    # Build per-metric rows for each variant key
    header = (
        "| Variant                | "
        + " | ".join(f"{m} (Gold/Pert/Δ%)" for m in metrics)
        + " |"
    )
    sep = "|" + "|".join(["---"] * (len(metrics) + 1)) + "|"
    rows = [header, sep]

    for key, label in POS_KEYS:
        cells = [f" {label:<22} "]
        results = list(map(float, v[f"result_{key}"].split()))
        for i, m in enumerate(metrics):
            chg = calc_change(results[i], refs[i])
            cells.append(f" {refs[i]:.3f} / {results[i]:.3f} / {chg:+.2f}% ")
        rows.append("|" + "|".join(cells) + "|")

    table = "\n".join(rows)
    instr_blocks = []
    for i, (instr, _kind) in enumerate(POS_COMPARE_INSTRUCTIONS, 1):
        instr_blocks.append(f"### {i}. {instr}\n\n_Your answer:_\n\n\n")

    md = f"""# Gold Card v2 — Positioned Error Test, WikiText-103
## Compare card across metrics

> **Annotator instructions.** Do not open `wiki/reports/positioned_error/evaluation/Positional_Error_Evaluation.pdf` while filling this in. Use only the score table below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Metrics compared:** {", ".join(metrics)}
**Additional information:** {info}

**Task:** open-ended text generation
**Dataset:** WikiText-103
**Perturbation:** 10 consecutive tokens at beginning/middle/end shuffled or replaced with random vocab tokens.

**Test results:**

{table}

---

## Your annotations

{''.join(instr_blocks)}
"""
    outfile = out_dir / "compare.md"
    _safe_write(outfile, md)


# ---------- Noised fluency, wiki -----------------------------------------

# Order matches the prompt template's example table; the lead author used
# this order in the gold PDF as well.
NF_NOISE_ORDER = [
    ("flu-lemmatizeverb",     "Verb lemmatization"),
    ("flu-randomworddrop",    "Random word drop"),
    ("flu-noisepunct",        "Punctuation noise"),
    ("flu-sentencemiddleswap","Sentence-middle swap"),
    ("flu-removepreposition", "Preposition removal"),
    ("flu-removestopwords",   "Stop-word removal"),
    ("flu-randomlocalswap",   "Local word swap"),
    ("flu-truncate",          "Truncate (remove suffix)"),
    ("flu-removearticle",     "Article removal"),
    ("flu-randomtokenrep",    "Random token repetition"),
]

# Display labels for the four wiki metrics
NF_WIKI_METRICS = [
    ("mauve-gpt2",          "MAUVE-GPT2-base"),
    ("mauve-roberta",       "MAUVE-RoBERTa-base"),
    ("mauve-roberta-large", "MAUVE-RoBERTa-large"),
    ("gpt-ppl",             "GPT2-base-PPL"),
]

NF_INSTRUCTIONS_HEADER = """\
### 1. Sensitivity to the Perturbation

For each noise type, fill in three cells. Categorise the **change rate** by the *largest* `|Δ%|` observed across all variation levels for that noise type:

- `low`      iff `max(|Δ%|) ≤ 25`
- `moderate` iff `max(|Δ%|) ≤ 60`
- `high`     otherwise (especially when `≈ 100`)

`monotonous decrease` = score moves in the expected direction at every step as variation increases. `superlinear decrease` = the per-step `|Δ|` *grows* as variation grows. (Note: for `GPT2-base-PPL` higher = worse, so the expected direction is `score increases`. Apply the same definitions accordingly: monotonous = monotonous in the *correct* direction; the change-rate categories use `|Δ%|` and so don't need a sign flip.)
"""

NF_RECOMMENDATION_BLOCK = """\

### 2. Recommendation

Yes iff *more than 7* of the 10 noise types have **both** a high change rate **and** a superlinear decrease, else No.

_Your answer (Yes/No):_
"""


def _load_noise_json(score_dir: Path, noise_key: str):
    """Return list of (variation_str, mean, edit_ratio) for a single noise file,
    sorted by parsed variation. Handles both wiki-style keys (`flu-X-0.5`) and
    sum_mt-style keys (`ref_flu-X-0.5_seedreduce`)."""
    p = score_dir / f"{noise_key}.json"
    if not p.exists():
        return []
    raw = json.loads(p.read_text())
    rows = []
    for k, v in raw.items():
        # Try sum_mt-style first: ref_<noise>-<var>_<suffix>
        m = re.match(rf"^(?:ref_)?{re.escape(noise_key)}-(.+?)(?:_[a-zA-Z]+)?$", k)
        var = m.group(1) if m else k
        rows.append((var, float(v["mean"]), float(v.get("edit_ratio", 0.0))))
    def _key(r):
        try: return float(r[0])
        except ValueError: return 0.0
    rows.sort(key=_key)
    return rows


def _format_variation(noise_key: str, var: str) -> str:
    if noise_key == "flu-sentencemiddleswap":
        try: return f"{int(float(var))} sentence(s) swapped"
        except ValueError: return var
    try: return f"{int(float(var) * 100)}%"
    except ValueError: return var


def _max_abs_change(rows, ref) -> float:
    if ref == 0 or not rows:
        return 0.0
    return max(abs((m - ref) / abs(ref) * 100.0) for _, m, _ in rows)


def render_noised_fluency_wiki_single():
    out_dir = OUT / "noised_fluency_wiki"
    out_dir.mkdir(parents=True, exist_ok=True)
    base = ROOT / "wiki" / "score_saves" / "wiki"

    for metric_key, metric_label in NF_WIKI_METRICS:
        score_dir = base / metric_key
        if not score_dir.exists():
            print(f"  skip {metric_label}: no score_saves at {score_dir}")
            continue
        ref = json.loads((score_dir / "ref.json").read_text())["ref"]["mean"]

        # Per-noise-type results table
        sections = [f"**Reference (gold) score:** {ref:.4f}\n"]
        for noise_key, noise_label in NF_NOISE_ORDER:
            rows = _load_noise_json(score_dir, noise_key)
            sections.append(f"\n#### {noise_label} (`{noise_key}`)\n")
            sections.append("| Variation | Score | edit_ratio | Δ vs gold |")
            sections.append("|---|---|---|---|")
            for var, mean, edit in rows:
                chg = (mean - ref) / abs(ref) * 100.0 if ref else 0.0
                sections.append(
                    f"| {_format_variation(noise_key, var)} "
                    f"| {mean:.4f} | {edit:.3f} | {chg:+.2f}% |"
                )
        results_block = "\n".join(sections)

        # Annotation table (10 rows × 3 fillable cells)
        ann_rows = ["| Noise type | Monotonous decrease | Superlinear decrease | Change rate |",
                    "|---|---|---|---|"]
        for noise_key, noise_label in NF_NOISE_ORDER:
            ann_rows.append(f"| {noise_label} (`{noise_key}`) | _Yes/No_ | _Yes/No_ | _low/moderate/high_ |")
        annotation_table = "\n".join(ann_rows)

        md = f"""# Gold Card v2 — Noised Fluency Test, WikiText-103
## Metric: {metric_label} (single-metric card)

> **Annotator instructions.** Do not open `wiki/reports/noised_fluency/evaluation/Noised_Fluency_WIKI.pdf` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** {"Higher GPT-PPL = lower quality." if metric_key == "gpt-ppl" else "Score range 0 (worst) to 1 (best)."}

**Task:** open-ended text generation
**Dataset:** WikiText-103, 1000 paragraphs (~256 tokens each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

{results_block}

---

## Your annotations

{NF_INSTRUCTIONS_HEADER}
{annotation_table}
{NF_RECOMMENDATION_BLOCK}"""

        outfile = out_dir / f"{metric_key.replace('-', '_')}_single.md"
        _safe_write(outfile, md)


def render_noised_fluency_wiki_compare():
    out_dir = OUT / "noised_fluency_wiki"
    out_dir.mkdir(parents=True, exist_ok=True)
    base = ROOT / "wiki" / "score_saves" / "wiki"

    # Build a per-noise-type summary table: rows = noise types,
    # columns = each metric's max |Δ%| (the value that drives change-rate categorisation).
    refs = {}
    max_changes = {}
    for metric_key, _ in NF_WIKI_METRICS:
        score_dir = base / metric_key
        refs[metric_key] = json.loads((score_dir / "ref.json").read_text())["ref"]["mean"]
        max_changes[metric_key] = {}
        for noise_key, _ in NF_NOISE_ORDER:
            rows = _load_noise_json(score_dir, noise_key)
            max_changes[metric_key][noise_key] = _max_abs_change(rows, refs[metric_key])

    header = "| Noise type | " + " | ".join(label + " max abs(Δ%)" for _, label in NF_WIKI_METRICS) + " |"
    sep    = "|" + "|".join(["---"] * (len(NF_WIKI_METRICS) + 1)) + "|"
    table_rows = [header, sep]
    for noise_key, noise_label in NF_NOISE_ORDER:
        cells = [f" {noise_label} (`{noise_key}`) "]
        for metric_key, _ in NF_WIKI_METRICS:
            cells.append(f" {max_changes[metric_key][noise_key]:.2f}% ")
        table_rows.append("|" + "|".join(cells) + "|")
    summary_table = "\n".join(table_rows)

    # Annotation: per-noise-type, name the recommended metric(s) (or "none").
    rec_rows = ["| Noise type | Recommended metric(s) |", "|---|---|"]
    for _, noise_label in NF_NOISE_ORDER:
        rec_rows.append(f"| {noise_label} | _name(s) or `none`_ |")
    rec_table = "\n".join(rec_rows)

    md = f"""# Gold Card v2 — Noised Fluency Test, WikiText-103
## Compare card across metrics

> **Annotator instructions.** Do not open `wiki/reports/noised_fluency/evaluation/Noised_Fluency_WIKI.pdf` while filling this in. The single-metric tables you produced for `mauve_gpt2_single.md`, `mauve_roberta_single.md`, `mauve_roberta_large_single.md`, `gpt_ppl_single.md` are the per-metric ground truth — this card aggregates them. Save in place.

**Metrics compared:** {", ".join(label for _, label in NF_WIKI_METRICS)}
**Task:** open-ended text generation
**Dataset:** WikiText-103
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Maximum absolute Δ% per (metric, noise type)** — drives the change-rate category. (Refer to the per-metric single cards for full per-variation tables.)

{summary_table}

---

## Your annotations

For each noise type, name the metric(s) that should be **recommended** for that noise type. A metric is recommended for a noise type iff it has *both* a `high` change rate *and* a `superlinear decrease` for that noise type, as you classified them in the corresponding single card. Multiple metrics may qualify for one noise type; if none qualify, write `none`.

{rec_table}
"""
    outfile = out_dir / "compare.md"
    _safe_write(outfile, md)


# ---------- Noised fluency, sum_mt (sum / wmt / tedmt) -------------------

# Each entry: (score_saves dirname, display label, per-metric "Additional info" text).
NF_SUM_METRICS = [
    ("bart_score_avg_f",    "BARTScore-avg-f",     "Log-likelihood; higher (closer to 0) = better. Reference values are negative."),
    ("bert_score_f",        "BERTScore-f",         "Score range 0 (worst) to 1 (best)."),
    ("rouge2-f",            "ROUGE-2",             "Score range 0 (worst) to 1 (best)."),
    ("rougeL-f",            "ROUGE-L",             "Score range 0 (worst) to 1 (best)."),
    ("unieval_coherence",   "UniEval-Coherence",   "Score range 0 (worst) to 1 (best)."),
    ("unieval_consistency", "UniEval-Consistency", "Score range 0 (worst) to 1 (best)."),
    ("unieval_fluency",     "UniEval-Fluency",     "Score range 0 (worst) to 1 (best)."),
    ("unieval_overall",     "UniEval-Overall",     "Score range 0 (worst) to 1 (best)."),
    ("unieval_relevance",   "UniEval-Relevance",   "Score range 0 (worst) to 1 (best)."),
]

NF_WMT_METRICS = [
    ("bart_score_wmt",      "BARTScore",   "Log-likelihood; higher (closer to 0) = better. Reference values are negative."),
    ("bert_score_f_wmt",    "BERTScore-f", "Score range 0 (worst) to 1 (best)."),
    ("bleu_wmt",            "BLEU",        "Reported on a 0–100 scale; higher = better."),
    ("bleurt_wmt",          "BLEURT",      "Higher = better. Reference is on a small scale (~0–1) and may dip slightly negative; relative changes can therefore look large in % terms — judge change rate by absolute |Δ%| as defined in the rules."),
]

NF_TEDMT_METRICS = [
    ("bart_score_ted",      "BARTScore",   "Log-likelihood; higher (closer to 0) = better. Reference values are negative."),
    ("bert_score_f_ted",    "BERTScore-f", "Score range 0 (worst) to 1 (best)."),
    ("bleu_ted",            "BLEU",        "Reported on a 0–100 scale; higher = better."),
    ("bleurt_ted",          "BLEURT",      "Higher = better. Reference value is small in magnitude (close to zero, may be slightly negative); relative changes can therefore look very large in % terms — judge change rate by absolute |Δ%| as defined in the rules."),
]

# (score_saves subdir, output dir name, dataset label, dataset description sentence,
#  task description, evaluation-pdf-path-hint, metrics list)
NF_SUMMT_BUCKETS = [
    ("sum", "noised_fluency_sum_mt", "CNN-DailyMail",
     "CNN-DailyMail, 100 reference summaries (~3 sentences each)",
     "summarization",
     "sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_SUM.pdf",
     NF_SUM_METRICS,
     "sum"),
    ("wmt-de-en", "noised_fluency_sum_mt", "WMT21 De-En",
     "WMT21 De-En, 1000 reference translations (~1 sentence each)",
     "machine translation",
     "sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_WMT.pdf",
     NF_WMT_METRICS,
     "wmt"),
    ("ted-zh-en", "noised_fluency_sum_mt", "TED Zh-En",
     "TED Zh-En, 1000 reference translations (~1 sentence each)",
     "machine translation",
     "sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_TEDMT.pdf",
     NF_TEDMT_METRICS,
     "tedmt"),
]


def render_noised_fluency_summt_single():
    base_root = ROOT / "sum_mt" / "score_saves"
    for score_subdir, out_subdir, dataset_label, dataset_descr, task, pdf_hint, metrics, file_prefix in NF_SUMMT_BUCKETS:
        out_dir = OUT / out_subdir
        out_dir.mkdir(parents=True, exist_ok=True)
        base = base_root / score_subdir

        for metric_key, metric_label, info in metrics:
            score_dir = base / metric_key
            if not score_dir.exists():
                print(f"  skip {dataset_label} / {metric_label}: no score_saves at {score_dir}")
                continue
            ref = json.loads((score_dir / "ref.json").read_text())["ref"]["mean"]

            # Per-noise-type results table
            sections = [f"**Reference (gold) score:** {ref:.4f}\n"]
            for noise_key, noise_label in NF_NOISE_ORDER:
                rows = _load_noise_json(score_dir, noise_key)
                sections.append(f"\n#### {noise_label} (`{noise_key}`)\n")
                sections.append("| Variation | Score | edit_ratio | Δ vs gold |")
                sections.append("|---|---|---|---|")
                for var, mean, edit in rows:
                    chg = (mean - ref) / abs(ref) * 100.0 if ref else 0.0
                    sections.append(
                        f"| {_format_variation(noise_key, var)} "
                        f"| {mean:.4f} | {edit:.3f} | {chg:+.2f}% |"
                    )
            results_block = "\n".join(sections)

            # Annotation table (10 rows × 3 fillable cells)
            ann_rows = ["| Noise type | Monotonous decrease | Superlinear decrease | Change rate |",
                        "|---|---|---|---|"]
            for noise_key, noise_label in NF_NOISE_ORDER:
                ann_rows.append(f"| {noise_label} (`{noise_key}`) | _Yes/No_ | _Yes/No_ | _low/moderate/high_ |")
            annotation_table = "\n".join(ann_rows)

            md = f"""# Gold Card v2 — Noised Fluency Test, {dataset_label}
## Metric: {metric_label} (single-metric card)

> **Annotator instructions.** Do not open `{pdf_hint}` while filling this in. Use only the score tables below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Additional information about the metric:** {info}

**Task:** {task}
**Dataset:** {dataset_descr}
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Test results:**

{results_block}

---

## Your annotations

{NF_INSTRUCTIONS_HEADER}
{annotation_table}
{NF_RECOMMENDATION_BLOCK}"""

            outfile = out_dir / f"{file_prefix}__{metric_key.replace('-', '_')}_single.md"
            _safe_write(outfile, md)


def render_noised_fluency_summt_compare():
    base_root = ROOT / "sum_mt" / "score_saves"
    for score_subdir, out_subdir, dataset_label, dataset_descr, task, pdf_hint, metrics, file_prefix in NF_SUMMT_BUCKETS:
        out_dir = OUT / out_subdir
        out_dir.mkdir(parents=True, exist_ok=True)
        base = base_root / score_subdir

        # Build per-noise-type max-|Δ%| summary across this bucket's metrics
        refs = {}
        max_changes = {}
        per_metric_card_links = []
        for metric_key, metric_label, _ in metrics:
            score_dir = base / metric_key
            if not score_dir.exists():
                continue
            refs[metric_key] = json.loads((score_dir / "ref.json").read_text())["ref"]["mean"]
            max_changes[metric_key] = {}
            for noise_key, _ in NF_NOISE_ORDER:
                rows = _load_noise_json(score_dir, noise_key)
                max_changes[metric_key][noise_key] = _max_abs_change(rows, refs[metric_key])
            per_metric_card_links.append(f"`{file_prefix}__{metric_key.replace('-', '_')}_single.md`")

        header = "| Noise type | " + " | ".join(label + " max abs(Δ%)" for _, label, _ in metrics) + " |"
        sep    = "|" + "|".join(["---"] * (len(metrics) + 1)) + "|"
        table_rows = [header, sep]
        for noise_key, noise_label in NF_NOISE_ORDER:
            cells = [f" {noise_label} (`{noise_key}`) "]
            for metric_key, _, _ in metrics:
                cells.append(f" {max_changes[metric_key][noise_key]:.2f}% " if metric_key in max_changes else " — ")
            table_rows.append("|" + "|".join(cells) + "|")
        summary_table = "\n".join(table_rows)

        rec_rows = ["| Noise type | Recommended metric(s) |", "|---|---|"]
        for _, noise_label in NF_NOISE_ORDER:
            rec_rows.append(f"| {noise_label} | _name(s) or `none`_ |")
        rec_table = "\n".join(rec_rows)

        md = f"""# Gold Card v2 — Noised Fluency Test, {dataset_label}
## Compare card across metrics

> **Annotator instructions.** Do not open `{pdf_hint}` while filling this in. The single-metric tables you produce for {", ".join(per_metric_card_links)} are the per-metric ground truth — this card aggregates them. Save in place.

**Metrics compared:** {", ".join(label for _, label, _ in metrics)}
**Task:** {task}
**Dataset:** {dataset_descr}
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Maximum absolute Δ% per (metric, noise type)** — drives the change-rate category. (Refer to the per-metric single cards for full per-variation tables.)

{summary_table}

---

## Your annotations

For each noise type, name the metric(s) that should be **recommended** for that noise type. A metric is recommended for a noise type iff it has *both* a `high` change rate *and* a `superlinear decrease` for that noise type, as you classified them in the corresponding single card. Multiple metrics may qualify for one noise type; if none qualify, write `none`.

{rec_table}
"""
        outfile = out_dir / f"{file_prefix}__compare.md"
        _safe_write(outfile, md)


# ---------- main ---------------------------------------------------------

def main():
    global FORCE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force", action="store_true",
        help="Overwrite existing files even if they contain answers. "
             "Default is to skip any non-pristine file.",
    )
    args = parser.parse_args()
    FORCE = args.force
    OUT.mkdir(exist_ok=True)
    if FORCE:
        print("(--force) existing files WILL be overwritten")
    print("Generating positioned-error templates ...")
    render_positioned_error_single()
    render_positioned_error_compare()
    print()
    print("Generating noised-fluency-wiki templates ...")
    render_noised_fluency_wiki_single()
    render_noised_fluency_wiki_compare()
    print()
    print("Generating noised-fluency-sum_mt templates ...")
    render_noised_fluency_summt_single()
    render_noised_fluency_summt_compare()
    print()
    print("Done. Open the .md files under gold_cards_v2/<bucket>/ and fill in answers.")


if __name__ == "__main__":
    main()

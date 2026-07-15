"""Compute the human-human ceiling a^{HH}_{s,d} from gold_cards_v2.

Compares the second-annotator gold cards in `gold_cards_v2/` against the
lead author's reference answers (extracted manually from the v1 evaluation
PDFs in `wiki/reports/*/evaluation/` and `sum_mt/reports/*/evaluation/`
and encoded inline below).

The aggregation mirrors `tab:coverage` (Table 2) and Appendix D in
main.tex:
  * per-instruction agreement a_i is averaged within (test, dataset),
  * a_i across datasets is the mean over the 4 datasets that share the
    instruction (only for noised-fluency, where wiki/sum/wmt/tedmt all
    use the same 4 sub-instructions),
  * a_{s,d} is the mean over instructions that share that
    (size-class, dimension) cell.

v1 references for the injection card family are absent (the lead
author's `sum_mt/reports/injection/evaluation/` folder is empty), so
Table 2 rows that combine pos+inj are reported here as "pos only" with
an explicit asterisk; combining is left to the writeup.

Outputs:
  analysis/outputs/human_vs_human_overlap_per_card.csv
  analysis/outputs/human_vs_human_a_i.csv
  analysis/outputs/human_vs_human_a_sd.csv

Usage:
  python analysis/coverage_human_vs_human.py
"""
from __future__ import annotations

from pathlib import Path
import csv
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
GOLD = ROOT / "gold_cards_v2"
OUT = ROOT / "analysis" / "outputs"

# Canonical noise-type order used in every noised-fluency card.
NOISE_ORDER = [
    "flu-lemmatizeverb",
    "flu-randomworddrop",
    "flu-noisepunct",
    "flu-sentencemiddleswap",
    "flu-removepreposition",
    "flu-removestopwords",
    "flu-randomlocalswap",
    "flu-truncate",
    "flu-removearticle",
    "flu-randomtokenrep",
]

# ------------------------------------------------------------------
#                           v1 reference data
# ------------------------------------------------------------------
# Each noised-fluency card: ten 3-tuples (mono, super, change) in
# NOISE_ORDER, plus a single recommendation. All three fields are
# normalised to lowercase: y/n for mono and super, l/m/h for change,
# y/n for the recommendation (lead author writes "Suitable" /
# "Not suitable", supervisor writes "Yes" / "No"; we map both to y/n).

# wiki: 4 metrics, each a list of length 10 of "<m><s><c>" triples.
# Letters: y=yes, n=no, l=low, m=moderate, h=high.
def _parse_compact(triples: str) -> list[tuple[str, str, str]]:
    """Each triple is exactly 3 chars: mono | super | change."""
    triples = triples.split()
    assert len(triples) == 10, triples
    out = []
    for t in triples:
        assert len(t) == 3, t
        m, s, c = t
        assert m in "yn" and s in "yn" and c in "lmh", t
        out.append((m, s, c))
    return out


V1_NF_WIKI = {
    # GPT2-base-PPL: monotonous = Yes when score *increases* (rule says so).
    "gpt_ppl":            (_parse_compact("ynm yyh ynm yym yyh yyh yyh ynm yyh ynh"), "n"),
    "mauve_gpt2":         (_parse_compact("yym yyh yyh ynh yyh yyh yyh nnh yym yyh"), "n"),
    "mauve_roberta":      (_parse_compact("yym yyh yyh yym yym yyh yyh ynh yyl yyh"), "n"),
    "mauve_roberta_large":(_parse_compact("yyh yyh yyh yyh yyh yyh yyh ynh yym yyh"), "y"),
}

V1_NF_SUM = {
    "bart_score_avg_f":   (_parse_compact("ynl ynl yyl ynl ynl yyl ynl nnl yyl ynl"), "n"),
    "bert_score_f":       (_parse_compact("ynl ynh yyl ynm ynl ynm ynh nnl yyl ynh"), "n"),
    "rouge2_f":            (_parse_compact("ynl ynm nnl ynl ynl ynl ynm nnl ynl ynl"), "n"),
    "rougeL_f":            (_parse_compact("ynl ynl nnl ynl yyl ynl ynl nnl yyl ynl"), "n"),
    "unieval_coherence":  (_parse_compact("ynl ynh ynl ynh ynl ynm ynh nnm ynl nnh"), "n"),
    "unieval_consistency":(_parse_compact("yyl ynh ynl ynm ynl ynl ynm nnl yyl ynm"), "n"),
    "unieval_fluency":    (_parse_compact("ynl ynh ynm ynh ynm ynm ynh nnm yyl ynh"), "n"),
    "unieval_relevance":  (_parse_compact("ynl ynh ynm ynh ynm ynm ynh nnm ynl ynh"), "n"),
    "unieval_overall":    (_parse_compact("ynl ynh ynl ynh ynm ynm ynh nnm ynl ynh"), "n"),
}

V1_NF_WMT = {
    # WMT/TEDMT: only 1 sentence per reference, so sentencemiddleswap has
    # exactly 1 variation level → superlinearity is undefined; lead author
    # generally said No, except where the absolute drop is huge (BLEURT).
    "bart_score_wmt":   (_parse_compact("ynl ynh ynl ynl ynl yym ynm ynm yyl ynm"), "n"),
    "bert_score_f_wmt": (_parse_compact("ynl ynh ynl ynm ynl ynm ynm ynm ynl ynl"), "n"),
    "bleu_wmt":         (_parse_compact("yyl ynh ynl ynl ynm ynm ynm yym yyl ynm"), "n"),
    "bleurt_wmt":       (_parse_compact("ynm ynh ynl yyh ynh ynh ynh ynh yym ynh"), "n"),
}

V1_NF_TEDMT = {
    "bart_score_ted":   (_parse_compact("ynl ynh ynl ynl ynl yym ynm yym yyl ynm"), "n"),
    "bert_score_f_ted": (_parse_compact("ynl ynh ynl ynl ynl ynm ynm ynm ynl ynm"), "n"),
    "bleu_ted":         (_parse_compact("ynl ynh yym ynl ynl ynm ynm yym yyl ynm"), "n"),
    "bleurt_ted":       (_parse_compact("ynh ynh ynh yym ynh ynh ynh ynh yyh ynh"), "n"),
}

# Compare-card recommendations: per noise type, the *set* of metrics
# the lead author flagged with an X in the recommendation matrix.
V1_NF_WIKI_COMPARE = {
    "flu-lemmatizeverb":      {"mauve_roberta_large"},
    "flu-randomworddrop":     {"gpt_ppl", "mauve_gpt2", "mauve_roberta", "mauve_roberta_large"},
    "flu-noisepunct":         {"mauve_gpt2", "mauve_roberta", "mauve_roberta_large"},
    "flu-sentencemiddleswap": {"mauve_roberta", "mauve_roberta_large"},
    "flu-removepreposition":  {"gpt_ppl", "mauve_gpt2", "mauve_roberta_large"},
    "flu-removestopwords":    {"gpt_ppl", "mauve_gpt2", "mauve_roberta", "mauve_roberta_large"},
    "flu-randomlocalswap":    {"gpt_ppl", "mauve_gpt2", "mauve_roberta", "mauve_roberta_large"},
    "flu-truncate":           set(),
    "flu-removearticle":      {"gpt_ppl"},
    "flu-randomtokenrep":     {"mauve_gpt2", "mauve_roberta", "mauve_roberta_large"},
}
# SUM compare: lead recommended nothing (no X marks in matrix).
V1_NF_SUM_COMPARE = {n: set() for n in NOISE_ORDER}
V1_NF_WMT_COMPARE = {n: set() for n in NOISE_ORDER}
V1_NF_WMT_COMPARE["flu-sentencemiddleswap"] = {"bleurt_wmt"}
V1_NF_TEDMT_COMPARE = {n: set() for n in NOISE_ORDER}
V1_NF_TEDMT_COMPARE["flu-removearticle"] = {"bleurt_ted"}


# Positioned-error answers (instruction-level, not cell-level).
# Q1.1, Q1.2, Q1.3 are scalar yes/no; Q2.1/Q2.2/Q2.4 are sets;
# Q2.3 is yes/no.
V1_POS_SINGLE = {
    "mauve_gpt2_base": {
        "1.1": "n", "1.2": "n", "1.3": "n",
        "2.1": {"shuffling-end", "random-end"},
        "2.2": {"shuffling-beg", "shuffling-mid", "random-beg", "random-mid"},
        "2.3": "n",
        "2.4": {"shuffling-beg", "shuffling-mid", "random-beg", "random-mid"},
    },
    "mauve_roberta_base": {
        "1.1": "n", "1.2": "n", "1.3": "n",
        "2.1": set(),
        "2.2": {"shuffling-beg", "shuffling-mid", "shuffling-end",
                "random-beg", "random-mid", "random-end"},
        "2.3": "n",
        "2.4": {"shuffling-beg", "shuffling-mid", "shuffling-end",
                "random-beg", "random-mid", "random-end"},
    },
    "mauve_roberta_large": {
        "1.1": "n", "1.2": "n", "1.3": "n",
        "2.1": {"shuffling-end", "random-beg", "random-mid", "random-end"},
        "2.2": {"shuffling-beg", "shuffling-mid"},
        "2.3": "n",
        "2.4": {"shuffling-beg", "shuffling-mid"},
    },
}
V1_POS_COMPARE = {
    "1": "MAUVE-RoBERTa-Large",
    "2": "MAUVE-RoBERTa-Base",
}


# ------------------------------------------------------------------
#                           v2 markdown parsing
# ------------------------------------------------------------------
_NOISE_RE = re.compile(
    r"^\| (?P<label>[^|]+?)\s*\(`(?P<key>flu-[a-z]+)`\)\s*\|"
    r"\s*(?P<mono>[A-Za-z]+)\s*\|"
    r"\s*(?P<super>[A-Za-z]+)\s*\|"
    r"\s*(?P<change>[a-z]+)\s*\|",
    re.MULTILINE,
)


def _norm_yn(s: str) -> str:
    s = s.strip().lower()
    if s.startswith("y"): return "y"
    if s.startswith("n"): return "n"
    raise ValueError(f"unparsable yes/no: {s!r}")


def _norm_change(s: str) -> str:
    s = s.strip().lower()
    if s == "low": return "l"
    if s == "moderate": return "m"
    if s == "high": return "h"
    raise ValueError(f"unparsable change rate: {s!r}")


def parse_nf_single(path: Path) -> tuple[list[tuple[str, str, str]], str]:
    """Return ((mono, super, change) for each of 10 noises, recommendation)."""
    text = path.read_text(encoding="utf-8")
    rows: dict[str, tuple[str, str, str]] = {}
    for m in _NOISE_RE.finditer(text):
        rows[m["key"]] = (_norm_yn(m["mono"]), _norm_yn(m["super"]),
                          _norm_change(m["change"]))
    triples = [rows[n] for n in NOISE_ORDER]

    # Recommendation: line "_Your answer (Yes/No):_ Yes" or "No".
    rec_match = re.search(r"_Your answer \(Yes/No\):_\s*([A-Za-z]+)", text)
    if rec_match is None:
        raise ValueError(f"no recommendation answer in {path}")
    rec = _norm_yn(rec_match.group(1))
    return triples, rec


def parse_nf_compare(path: Path, valid_metrics: set[str]) -> dict[str, set[str]]:
    """Return per-noise-type set of recommended metric_keys.

    Uses the table at the bottom of the compare card; entries are
    metric labels separated by commas. We map labels back to the
    metric_keys used in V1_*_COMPARE by case-insensitive substring
    match against the supplied valid_metrics set.
    """
    text = path.read_text(encoding="utf-8")
    # The recommendation table is the last "| ... | ... |" block.
    # Each row is "| <Noise label> | <metrics or 'none'> |".
    # Map noise display label → noise key by exact match in NOISE_LABELS.
    label_to_key = {
        "Verb lemmatization": "flu-lemmatizeverb",
        "Random word drop": "flu-randomworddrop",
        "Punctuation noise": "flu-noisepunct",
        "Sentence-middle swap": "flu-sentencemiddleswap",
        "Preposition removal": "flu-removepreposition",
        "Stop-word removal": "flu-removestopwords",
        "Local word swap": "flu-randomlocalswap",
        "Truncate (remove suffix)": "flu-truncate",
        "Article removal": "flu-removearticle",
        "Random token repetition": "flu-randomtokenrep",
    }
    out: dict[str, set[str]] = {n: set() for n in NOISE_ORDER}
    # Take only the section after "## Your annotations" to avoid
    # accidentally matching the score-summary table.
    annot_marker = "## Your annotations"
    if annot_marker in text:
        text = text.split(annot_marker, 1)[1]
    for line in text.splitlines():
        if not line.startswith("| "):
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 2:
            continue
        label, metrics_cell = parts[0], parts[1]
        if label not in label_to_key:
            continue
        key = label_to_key[label]
        if metrics_cell.lower().strip().strip("`") in ("none", "_name(s) or `none`_"):
            out[key] = set()
            continue
        # Match each comma-separated metric label against valid_metrics.
        recommended = set()
        for tok in metrics_cell.split(","):
            tok = tok.strip().lower()
            if not tok or tok in ("none",):
                continue
            for vm in valid_metrics:
                if _label_matches_key(tok, vm):
                    recommended.add(vm)
                    break
        out[key] = recommended
    return out


def _label_matches_key(label: str, key: str) -> bool:
    """True iff free-text metric label refers to metric key.

    Both sides are normalised to lowercase alphanumeric only, then
    matched canonical-form-equal. The canonical form drops:
      * dataset suffixes (`_wmt`, `_ted`) on the key,
      * `f` suffixes on rouge metrics (`rouge2f` → `rouge2`),
      * `base`/`avg`/`-f` decorations on labels.
    """
    def canon(s: str) -> str:
        s = re.sub(r"[^a-z0-9]", "", s.lower())
        # strip dataset suffix on the key side
        s = re.sub(r"(wmt|ted)$", "", s)
        # canonicalise common variants
        s = s.replace("gpt2basepll", "gptppl")
        s = s.replace("gpt2baseppl", "gptppl")
        s = s.replace("gpt2basepl", "gptppl")
        s = s.replace("bartscoreavgf", "bartscore")
        s = s.replace("bertscoref", "bertscore")
        s = s.replace("bert_score_f", "bertscore")
        s = s.replace("rouge2f", "rouge2")
        s = s.replace("rougelf", "rougel")
        s = s.replace("base", "")  # 'mauvegpt2base' -> 'mauvegpt2'
        s = s.replace("avgf", "")
        return s
    return canon(label) == canon(key)


# ------------------------------------------------------------------
#                  positioned-error v2 markdown parsing
# ------------------------------------------------------------------
def parse_pos_single(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    # Find each "_Your answer:_" line; the answer follows on the same
    # line (for binary/short) or as a bulleted list on subsequent lines
    # before the next "###".
    out: dict[str, object] = {}
    sections = re.split(r"^### \d+\.\s", text, flags=re.MULTILINE)
    # sections[0] is the preamble; sections[1..7] are answers.
    if len(sections) < 8:
        raise ValueError(f"expected 7 answer sections in {path}, got {len(sections)-1}")
    keys = ["1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "2.4"]
    for k, sec in zip(keys, sections[1:]):
        m = re.search(r"_Your answer(?: \(Yes/No\))?:_\s*(.*?)(?:\n\n|\Z)",
                      sec, re.DOTALL)
        if m is None:
            raise ValueError(f"no answer for Q{k} in {path}")
        body = m.group(1).strip()
        if k in ("1.1", "1.2", "1.3", "2.3"):
            out[k] = _parse_pos_binary(body)
        else:  # 2.1, 2.2, 2.4 — set of variants
            out[k] = _parse_pos_variants(body)
    return out


def _parse_pos_binary(body: str) -> str:
    # Body might be "No", "Yes", or "No\n" etc.
    first = body.strip().split("\n", 1)[0].strip()
    if first.lower().startswith("no"): return "n"
    if first.lower().startswith("yes"): return "y"
    raise ValueError(f"unparsable pos binary answer: {body!r}")


def _parse_pos_variants(body: str) -> set[str]:
    body = body.strip()
    if body.lower() in ("none", ""):
        return set()
    out = set()
    for line in body.splitlines():
        line = line.strip().lstrip("-* ").strip()
        if not line or line.lower() == "none":
            continue
        out.add(_normalise_pos_label(line))
    return out


def _normalise_pos_label(s: str) -> str:
    """'Shuffling, Beginning' → 'shuffling-beg', etc."""
    s = s.lower().strip()
    s = re.sub(r"[\s,]+", "-", s)
    # 'shuffling-beginning' → 'shuffling-beg', 'random-end' stays
    s = s.replace("beginning", "beg").replace("middle", "mid")
    return s


def parse_pos_compare(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    sections = re.split(r"^### (\d+)\.\s", text, flags=re.MULTILINE)
    # Pattern: [preamble, "1", body1, "2", body2, ...]
    for i in range(1, len(sections), 2):
        n, body = sections[i], sections[i + 1]
        m = re.search(r"_Your answer:_\s*([^\n]+)", body)
        if m:
            out[n] = m.group(1).strip()
    return out


# ------------------------------------------------------------------
#                            agreement helpers
# ------------------------------------------------------------------
def _set_agreement(v1: set, v2: set) -> float:
    """Coverage as in §3.4: fraction of v2's items that match v1."""
    if not v2:
        # Both empty → trivially perfect; v2 empty but v1 not → 0.
        return 1.0 if not v1 else 0.0
    return len(v1 & v2) / len(v2)


def _bin_agreement(v1: str, v2: str) -> float:
    return 1.0 if v1 == v2 else 0.0


# ------------------------------------------------------------------
#                            main computation
# ------------------------------------------------------------------
def compute_nf_single_overlap(
    bucket_dir: Path, file_prefix: str, v1_data: dict, dataset_label: str,
) -> list[dict]:
    """Per-card overlap for noised-fluency single cards in one dataset."""
    rows = []
    for metric_key, (v1_triples, v1_rec) in v1_data.items():
        if file_prefix:
            fname = f"{file_prefix}__{metric_key}_single.md"
        else:
            fname = f"{metric_key}_single.md"
        v2_path = bucket_dir / fname
        if not v2_path.exists():
            print(f"  [warn] missing v2 card: {v2_path}", file=sys.stderr)
            continue
        v2_triples, v2_rec = parse_nf_single(v2_path)
        mono_match = sum(a[0] == b[0] for a, b in zip(v1_triples, v2_triples))
        super_match = sum(a[1] == b[1] for a, b in zip(v1_triples, v2_triples))
        change_match = sum(a[2] == b[2] for a, b in zip(v1_triples, v2_triples))
        rec_match = int(v1_rec == v2_rec)
        rows.append({
            "test": "noised_fluency",
            "size": "single",
            "dataset": dataset_label,
            "metric": metric_key,
            "mono_n": 10, "mono_match": mono_match,
            "super_n": 10, "super_match": super_match,
            "change_n": 10, "change_match": change_match,
            "rec_n": 1,    "rec_match": rec_match,
        })
    return rows


def compute_nf_compare_overlap(
    bucket_dir: Path, fname: str, v1_recs: dict[str, set[str]], dataset_label: str,
    valid_metrics: set[str],
) -> dict:
    v2_path = bucket_dir / fname
    v2_recs = parse_nf_compare(v2_path, valid_metrics)
    n_metrics = len(valid_metrics)
    cell_match = 0
    for noise in NOISE_ORDER:
        v1set = v1_recs[noise]
        v2set = v2_recs[noise]
        for m in valid_metrics:
            if (m in v1set) == (m in v2set):
                cell_match += 1
    return {
        "test": "noised_fluency",
        "size": "compare",
        "dataset": dataset_label,
        "metric": "(all)",
        "rec_cells_n": 10 * n_metrics,
        "rec_cells_match": cell_match,
    }


def compute_pos_single_overlap(bucket_dir: Path) -> list[dict]:
    rows = []
    for metric_key, v1_ans in V1_POS_SINGLE.items():
        v2_path = bucket_dir / f"{metric_key}_single.md"
        v2_ans = parse_pos_single(v2_path)
        scores = {}
        for k, v1v in v1_ans.items():
            v2v = v2_ans[k]
            if isinstance(v1v, set):
                scores[k] = _set_agreement(v1v, v2v)
            else:
                scores[k] = _bin_agreement(v1v, v2v)
        rows.append({
            "test": "positioned_error",
            "size": "single",
            "dataset": "wiki",
            "metric": metric_key,
            **{f"a_{k.replace('.', '_')}": scores[k] for k in v1_ans},
        })
    return rows


def compute_pos_compare_overlap(bucket_dir: Path) -> dict:
    v2_path = bucket_dir / "compare.md"
    v2 = parse_pos_compare(v2_path)
    a1 = _bin_agreement(_canon_metric(V1_POS_COMPARE["1"]), _canon_metric(v2["1"]))
    a2 = _bin_agreement(_canon_metric(V1_POS_COMPARE["2"]), _canon_metric(v2["2"]))
    return {
        "test": "positioned_error",
        "size": "compare",
        "dataset": "wiki",
        "metric": "(all)",
        "a_1": a1,
        "a_2": a2,
    }


def _canon_metric(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower().split(".")[0])


# ------------------------------------------------------------------
#                            aggregation
# ------------------------------------------------------------------
def main():
    OUT.mkdir(exist_ok=True)
    per_card_rows: list[dict] = []

    # --- Noised fluency single ---
    per_card_rows += compute_nf_single_overlap(
        GOLD / "noised_fluency_wiki", "", V1_NF_WIKI, "wiki")
    per_card_rows += compute_nf_single_overlap(
        GOLD / "noised_fluency_sum_mt", "sum", V1_NF_SUM, "sum")
    per_card_rows += compute_nf_single_overlap(
        GOLD / "noised_fluency_sum_mt", "wmt", V1_NF_WMT, "wmt")
    per_card_rows += compute_nf_single_overlap(
        GOLD / "noised_fluency_sum_mt", "tedmt", V1_NF_TEDMT, "tedmt")

    # --- Noised fluency compare (per-noise × metric cells) ---
    compare_rows = [
        compute_nf_compare_overlap(GOLD / "noised_fluency_wiki", "compare.md",
                                   V1_NF_WIKI_COMPARE, "wiki",
                                   set(V1_NF_WIKI.keys())),
        compute_nf_compare_overlap(GOLD / "noised_fluency_sum_mt", "sum__compare.md",
                                   V1_NF_SUM_COMPARE, "sum",
                                   set(V1_NF_SUM.keys())),
        compute_nf_compare_overlap(GOLD / "noised_fluency_sum_mt", "wmt__compare.md",
                                   V1_NF_WMT_COMPARE, "wmt",
                                   set(V1_NF_WMT.keys())),
        compute_nf_compare_overlap(GOLD / "noised_fluency_sum_mt", "tedmt__compare.md",
                                   V1_NF_TEDMT_COMPARE, "tedmt",
                                   set(V1_NF_TEDMT.keys())),
    ]

    # --- Positioned error single + compare ---
    pos_single_rows = compute_pos_single_overlap(GOLD / "positioned_error")
    pos_compare_row = compute_pos_compare_overlap(GOLD / "positioned_error")

    # ----- Per-card CSV -----
    fieldnames = sorted({k for r in per_card_rows + compare_rows + pos_single_rows + [pos_compare_row] for k in r})
    with (OUT / "human_vs_human_overlap_per_card.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in per_card_rows + compare_rows + pos_single_rows + [pos_compare_row]:
            w.writerow(r)

    # ----- a_i: per-instruction agreements averaged within (test, dataset) -----
    # Noised-fluency single → 4 sub-instructions (mono, super, change, rec).
    nf_single_a_i = {}
    for ds in ("wiki", "sum", "wmt", "tedmt"):
        cards = [r for r in per_card_rows if r["size"] == "single" and r["dataset"] == ds]
        if not cards:
            continue
        n = len(cards)
        nf_single_a_i[ds] = {
            "mono":   sum(r["mono_match"]   for r in cards) / (10 * n),
            "super":  sum(r["super_match"]  for r in cards) / (10 * n),
            "change": sum(r["change_match"] for r in cards) / (10 * n),
            "rec":    sum(r["rec_match"]    for r in cards) / n,
        }

    # Compare card: only the per-noise × metric recommendation grid.
    nf_compare_a_i = {r["dataset"]: r["rec_cells_match"] / r["rec_cells_n"] for r in compare_rows}

    # Positioned-error single → 7 instructions.
    pos_a_i = {f"Q{r['metric']}": [] for r in pos_single_rows}  # placeholder
    pos_a_i = {f"{k}": [] for k in ("1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "2.4")}
    for r in pos_single_rows:
        for k in pos_a_i:
            pos_a_i[k].append(r[f"a_{k.replace('.', '_')}"])
    pos_a_i_mean = {k: sum(v) / len(v) for k, v in pos_a_i.items()}

    # Positioned-error compare → 2 instructions.
    pos_compare_a_i = {"1": pos_compare_row["a_1"], "2": pos_compare_row["a_2"]}

    # ----- Output a_i CSV -----
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
    with (OUT / "human_vs_human_a_i.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["family", "dataset", "instruction", "a_i"])
        w.writeheader()
        for r in a_i_rows:
            w.writerow({**r, "a_i": round(r["a_i"], 4)})

    # ----- a_{s,d} aggregations -----
    # noised-fluency: a_i averaged across the 4 datasets, then per-(s,d).
    def avg(xs): return sum(xs) / len(xs) if xs else 0.0

    nf_single_a_i_avg = {
        instr: avg([nf_single_a_i[ds][instr] for ds in nf_single_a_i])
        for instr in ("mono", "super", "change", "rec")
    }
    a_concl_single_fluency = avg(nf_single_a_i_avg.values())

    nf_compare_a_i_avg = avg(nf_compare_a_i.values())  # only 1 instruction
    a_concl_compare_fluency = nf_compare_a_i_avg

    # Positioned-error (pos only — no inj v2 reference exists):
    a_retrieval_pos = avg([pos_a_i_mean["1.1"], pos_a_i_mean["1.2"], pos_a_i_mean["1.3"]])
    a_concl_pos_single = avg([pos_a_i_mean["2.1"], pos_a_i_mean["2.2"],
                              pos_a_i_mean["2.3"], pos_a_i_mean["2.4"]])
    a_concl_pos_compare = avg(list(pos_compare_a_i.values()))
    a_concl_pos_combined = avg([a_concl_pos_single, a_concl_pos_compare])
    a_humanlike_pos = avg([pos_a_i_mean["1.2"], pos_a_i_mean["1.3"]])
    a_reduced_pos = pos_a_i_mean["2.4"]
    a_consistency_pos = abs(pos_a_i_mean["2.1"] - pos_a_i_mean["2.2"])

    sd_rows = [
        ("Retrieval (pos*)",            a_retrieval_pos),
        ("Conclusion (pos* single)",    a_concl_pos_single),
        ("Conclusion (pos* compare)",   a_concl_pos_compare),
        ("Conclusion (pos*)",           a_concl_pos_combined),
        ("Conclusion (single, fluency)", a_concl_single_fluency),
        ("Conclusion (compare, fluency)", a_concl_compare_fluency),
        ("Human Likeness (pos*)",       a_humanlike_pos),
        ("Reduced Guidance (pos*)",     a_reduced_pos),
        ("Consistency (pos*)",          a_consistency_pos),
    ]
    with (OUT / "human_vs_human_a_sd.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["dimension", "a_HH"])
        for name, val in sd_rows:
            w.writerow([name, round(val, 4)])

    # ----- Print summary -----
    print()
    print("=" * 60)
    print("Human-human ceiling a^{HH}_{s,d} (* = pos-only; v1 inj cards do not exist)")
    print("=" * 60)
    for name, val in sd_rows:
        print(f"  {name:<35} {val * 100:5.1f}%")
    print()
    # Also print per-card raw cell counts for sanity-checking.
    total_single_cells = total_single_match = 0
    for r in per_card_rows:
        total_single_cells += r["mono_n"] + r["super_n"] + r["change_n"] + r["rec_n"]
        total_single_match += r["mono_match"] + r["super_match"] + r["change_match"] + r["rec_match"]
    total_compare_cells = sum(r["rec_cells_n"] for r in compare_rows)
    total_compare_match = sum(r["rec_cells_match"] for r in compare_rows)
    pos_single_cell_n, pos_single_cell_m = 0, 0
    for r in pos_single_rows:
        # 7 instructions per pos card; binary scored 0/1, set scored fractional → still average.
        for k in ("1.1", "1.2", "1.3", "2.1", "2.2", "2.3", "2.4"):
            pos_single_cell_n += 1
            pos_single_cell_m += r[f"a_{k.replace('.', '_')}"]
    pos_compare_cells = 2
    pos_compare_match = pos_compare_row["a_1"] + pos_compare_row["a_2"]
    print(f"Raw totals (information):")
    print(f"  Noised-fluency single   : {total_single_match}/{total_single_cells} cells "
          f"({100*total_single_match/total_single_cells:.1f}%)")
    print(f"  Noised-fluency compare  : {total_compare_match}/{total_compare_cells} cells "
          f"({100*total_compare_match/total_compare_cells:.1f}%)")
    print(f"  Positioned-error single : {pos_single_cell_m:.2f}/{pos_single_cell_n} instr-units "
          f"({100*pos_single_cell_m/pos_single_cell_n:.1f}%)")
    print(f"  Positioned-error compare: {pos_compare_match:.0f}/{pos_compare_cells} instructions "
          f"({100*pos_compare_match/pos_compare_cells:.0f}%)")
    print()
    print(f"Wrote: {OUT.relative_to(ROOT)}/human_vs_human_overlap_per_card.csv")
    print(f"Wrote: {OUT.relative_to(ROOT)}/human_vs_human_a_i.csv")
    print(f"Wrote: {OUT.relative_to(ROOT)}/human_vs_human_a_sd.csv")


if __name__ == "__main__":
    main()

"""Comparability of ROUGE-L (FS) vs. BARTScore-avg-f (ABLMC) as authoring tasks.

Responds to EMNLP reviewer TVpE (W2): the creation study confounds the
FS/ABLMC condition with the metric (FS cards were always written for
ROUGE-L, ABLMC cards for BARTScore-avg-f). This script quantifies, post
hoc, how comparable the two authoring tasks were:

  1. Deterministic card content derived from the two score tables
     (change rates, threshold labels, similarity verdicts,
     recommendation) — identical structure, near-identical labels.
  2. The lead author's human reference cards for the two metrics
     (transcribed from sum_mt/reports/injection/evaluation/
     "Injection Test.pdf") — instruction-by-instruction agreement.
  3. Length of the LLM drafts for the two metrics (all three models;
     the ABLMC participants saw the highest-coverage model's draft).
  4. Length of the cards the participants actually produced
     (FS vs. ABLMC; note this one is condition-confounded — ABLMC
     lengths inherit the draft's verbosity — and is reported only for
     completeness).

Usage
  python analysis/comparability_fs_ablmc.py
"""
from __future__ import annotations

from pathlib import Path
import re
import statistics

ROOT = Path(__file__).resolve().parent.parent
CARDS = ROOT / "analysis" / "cards_text"
LLM_REPORTS = ROOT / "sum_mt" / "reports" / "injection" / "results_single_reports"

# ------------------------------------------------------------------
# 1. Score tables (from sum_mt/reports/injection/results_single_values/)
# ------------------------------------------------------------------
SCORES = {
    "ROUGE-L":         {"ref": 0.286197, "inj1": 0.126527, "inj2": 0.098507},
    "BARTScore-avg-f": {"ref": -6.063610, "inj1": -8.247265, "inj2": -9.390858},
}
HIGH = 70.0   # >=70% -> high change rate
SIM = 10.0    # similarity rule of the injection template:
              # "similar if change rate difference < 10%" (pair reading)

# Change-rate vocabulary of the card templates (gold_cards_v2/README.md).
VOCAB = [(10, "very low"), (30, "low"), (50, "low to moderate"),
         (70, "moderate to high"), (90, "high"), (101, "very high")]


def change_pct(score: float, ref: float) -> float:
    return (score - ref) / abs(ref) * 100.0


def vocab_label(delta_abs: float) -> str:
    for bound, label in VOCAB:
        if delta_abs < bound:
            return label
    return "very high"


def derive_content(vals: dict) -> dict:
    d1 = change_pct(vals["inj1"], vals["ref"])
    d2 = change_pct(vals["inj2"], vals["ref"])
    strengths = [k for k, d in (("Inj1", d1), ("Inj2", d2)) if abs(d) >= HIGH]
    weaknesses = [k for k, d in (("Inj1", d1), ("Inj2", d2)) if abs(d) < HIGH]
    return {
        "delta_inj1": d1,
        "delta_inj2": d2,
        "class_inj1": vocab_label(abs(d1)),
        "class_inj2": vocab_label(abs(d2)),
        "higher_than_gold": "Yes" if (d1 > 0 or d2 > 0) else "No",
        "similar": "Yes" if abs(abs(d1) - abs(d2)) < SIM else "No",
        "strengths": strengths or ["None"],
        "weaknesses": weaknesses or ["None"],
        "recommendation": "Yes" if len(strengths) == 2 else "No",
    }


# ------------------------------------------------------------------
# 2. Lead author's reference answers (Injection Test.pdf, single cards)
#    Instruction keys follow the template: 1.1 higher-than-gold,
#    1.2 similarity, 2.1 strengths, 2.2 weaknesses,
#    2.3 recommendation, 2.4 needs improvement.
# ------------------------------------------------------------------
V1_INJ = {
    "ROUGE-L": {
        "1.1": "No", "1.2": "Yes", "2.1": ["None"],
        "2.2": ["Inj1", "Inj2"], "2.3": "No", "2.4": ["Inj1", "Inj2"],
    },
    "BARTScore-avg-f": {
        "1.1": "No", "1.2": "No", "2.1": ["None"],
        "2.2": ["Inj1", "Inj2"], "2.3": "No", "2.4": ["Inj1", "Inj2"],
    },
}


# ------------------------------------------------------------------
# word-count helpers
# ------------------------------------------------------------------
def words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def participant_card_words(path: Path) -> int:
    text = path.read_text(encoding="utf-8")
    marker = "## Participant metric card"
    if marker in text:
        text = text.split(marker, 1)[1]
    return words(text)


def main():
    # --- 1. deterministic content ---
    print("1. Deterministic card content from the two score tables")
    derived = {}
    for metric, vals in SCORES.items():
        c = derive_content(vals)
        derived[metric] = c
        print(f"\n  {metric}:")
        print(f"    change rates      Inj1 {c['delta_inj1']:+.1f}% ({c['class_inj1']}), "
              f"Inj2 {c['delta_inj2']:+.1f}% ({c['class_inj2']})")
        print(f"    higher than gold  {c['higher_than_gold']}")
        print(f"    similar (<{SIM:.0f}%)    {c['similar']}")
        print(f"    strengths         {', '.join(c['strengths'])}")
        print(f"    weaknesses        {', '.join(c['weaknesses'])}")
        print(f"    recommendation    {c['recommendation']}")

    keys = ["higher_than_gold", "similar", "strengths", "weaknesses",
            "recommendation"]
    same = [k for k in keys
            if derived["ROUGE-L"][k] == derived["BARTScore-avg-f"][k]]
    print(f"\n  -> identical on {len(same)}/{len(keys)} derived fields "
          f"({', '.join(same)});")
    diff = [k for k in keys if k not in same]
    print(f"     differing: {', '.join(diff) if diff else 'none'}")

    # --- 2. reference-card agreement ---
    print("\n2. Lead author's reference cards (Injection Test.pdf)")
    instr = ["1.1", "1.2", "2.1", "2.2", "2.3", "2.4"]
    agree = [k for k in instr if V1_INJ["ROUGE-L"][k] == V1_INJ["BARTScore-avg-f"][k]]
    n_sub = {m: sum(len(v) if isinstance(v, list) else 1
                    for v in V1_INJ[m].values()) for m in V1_INJ}
    print(f"  instructions per card : {len(instr)} vs {len(instr)}")
    print(f"  subanswers per card   : {n_sub['ROUGE-L']} vs {n_sub['BARTScore-avg-f']}")
    print(f"  identical labels      : {len(agree)}/{len(instr)} instructions "
          f"(differs only on: {', '.join(k for k in instr if k not in agree)})")

    # --- 3. LLM draft lengths ---
    print("\n3. LLM draft lengths (words)")
    draft_words = {"ROUGE-L": [], "BARTScore-avg-f": []}
    for model_dir in sorted(LLM_REPORTS.iterdir()):
        if not model_dir.is_dir():
            continue
        r = model_dir / "rougel.txt"
        b = model_dir / "bartscoreavgf.txt"
        if r.exists() and b.exists():
            wr, wb = words(r.read_text()), words(b.read_text())
            draft_words["ROUGE-L"].append(wr)
            draft_words["BARTScore-avg-f"].append(wb)
            print(f"  {model_dir.name:<24} rouge-l {wr:>4}  bartscore {wb:>4}")
    for m, ws in draft_words.items():
        if ws:
            print(f"  mean {m:<20} {statistics.mean(ws):.0f} words")

    # --- 4. participant card lengths (condition-confounded; FYI only) ---
    print("\n4. Participant card lengths (condition-confounded, FYI)")
    for cond in ("FS", "ABLMC"):
        ws = [participant_card_words(p)
              for p in sorted(CARDS.glob(f"InjTest_{cond}_*.txt"))]
        print(f"  {cond:<6} per card {ws}  mean {statistics.mean(ws):.0f} words")


if __name__ == "__main__":
    main()

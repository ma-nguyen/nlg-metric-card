# Gold Card v2 — Positioned Error Test, WikiText-103
## Compare card across metrics

> **Annotator instructions.** Do not open `wiki/reports/positioned_error/evaluation/Positional_Error_Evaluation.pdf` while filling this in. Use only the score table below and the answer rules in `gold_cards_v2/README.md`. Save in place.

**Metrics compared:** MAUVE-GPT2-base, MAUVE-RoBERTa-Base, MAUVE-RoBERTa-Large
**Additional information:** The Metric scores from 0 (Minimum) to 1 (Maximum)

**Task:** open-ended text generation
**Dataset:** WikiText-103
**Perturbation:** 10 consecutive tokens at beginning/middle/end shuffled or replaced with random vocab tokens.

**Test results:**

| Variant                | MAUVE-GPT2-base (Gold/Pert/Δ%) | MAUVE-RoBERTa-Base (Gold/Pert/Δ%) | MAUVE-RoBERTa-Large (Gold/Pert/Δ%) |
|---|---|---|---|
| Shuffling, Beginning   | 0.948 / 0.546 / -42.42% | 0.962 / 0.958 / -0.39% | 0.979 / 0.354 / -63.84% |
| Shuffling, Middle      | 0.948 / 0.821 / -13.40% | 0.962 / 0.948 / -1.43% | 0.979 / 0.619 / -36.73% |
| Shuffling, End         | 0.948 / 0.018 / -98.06% | 0.962 / 0.511 / -46.87% | 0.979 / 0.255 / -73.91% |
| Random,    Beginning   | 0.948 / 0.638 / -32.69% | 0.962 / 0.894 / -7.09% | 0.979 / 0.032 / -96.76% |
| Random,    Middle      | 0.948 / 0.345 / -63.64% | 0.962 / 0.911 / -5.28% | 0.979 / 0.121 / -87.64% |
| Random,    End         | 0.948 / 0.007 / -99.22% | 0.962 / 0.510 / -47.02% | 0.979 / 0.039 / -95.97% |

---

## Your annotations

### 1. **Recommendation.** Name the metric with the most high-change-rate variants (≥70%) overall.

_Your answer:_ MAUVE-RoBERTa-Large


### 2. **Anti-recommendation.** Explicitly state which metric you would NOT recommend, and why. A human would not recommend a metric whose variations have no high change rates.

_Your answer:_ MAUVE-RoBERTa-Base. Under the positioned-error perturbation test, it scores similar in two thirds of all cases and only reaches low-to-moderate change in the other third.




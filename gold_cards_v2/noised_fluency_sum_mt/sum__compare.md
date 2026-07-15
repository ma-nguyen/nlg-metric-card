# Gold Card v2 — Noised Fluency Test, CNN-DailyMail
## Compare card across metrics

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_SUM.pdf` while filling this in. The single-metric tables you produce for `sum__bart_score_avg_f_single.md`, `sum__bert_score_f_single.md`, `sum__rouge2_f_single.md`, `sum__rougeL_f_single.md`, `sum__unieval_coherence_single.md`, `sum__unieval_consistency_single.md`, `sum__unieval_fluency_single.md`, `sum__unieval_overall_single.md`, `sum__unieval_relevance_single.md` are the per-metric ground truth — this card aggregates them. Save in place.

**Metrics compared:** BARTScore-avg-f, BERTScore-f, ROUGE-2, ROUGE-L, UniEval-Coherence, UniEval-Consistency, UniEval-Fluency, UniEval-Overall, UniEval-Relevance
**Task:** summarization
**Dataset:** CNN-DailyMail, 100 reference summaries (~3 sentences each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Maximum absolute Δ% per (metric, noise type)** — drives the change-rate category. (Refer to the per-metric single cards for full per-variation tables.)

| Noise type | BARTScore-avg-f max abs(Δ%) | BERTScore-f max abs(Δ%) | ROUGE-2 max abs(Δ%) | ROUGE-L max abs(Δ%) | UniEval-Coherence max abs(Δ%) | UniEval-Consistency max abs(Δ%) | UniEval-Fluency max abs(Δ%) | UniEval-Overall max abs(Δ%) | UniEval-Relevance max abs(Δ%) |
|---|---|---|---|---|---|---|---|---|---|
| Verb lemmatization (`flu-lemmatizeverb`) | 2.53% | 12.08% | 1.83% | 0.80% | 5.50% | 4.26% | 15.62% | 9.13% | 11.02% |
| Random word drop (`flu-randomworddrop`) | 23.81% | 75.84% | 49.63% | 17.26% | 89.29% | 62.54% | 92.47% | 85.46% | 98.02% |
| Punctuation noise (`flu-noisepunct`) | 3.29% | 16.30% | 0.00% | 0.00% | 13.22% | 13.22% | 42.45% | 24.02% | 26.60% |
| Sentence-middle swap (`flu-sentencemiddleswap`) | 7.16% | 32.04% | 7.08% | 9.53% | 64.90% | 31.16% | 70.46% | 62.52% | 84.95% |
| Preposition removal (`flu-removepreposition`) | 5.44% | 20.11% | 12.39% | 4.18% | 24.20% | 15.33% | 53.45% | 34.26% | 44.06% |
| Stop-word removal (`flu-removestopwords`) | 8.09% | 28.69% | 21.62% | 6.27% | 29.67% | 17.53% | 55.56% | 38.67% | 52.39% |
| Local word swap (`flu-randomlocalswap`) | 15.61% | 67.33% | 49.08% | 10.29% | 79.63% | 47.67% | 94.10% | 79.61% | 97.68% |
| Truncate (remove suffix) (`flu-truncate`) | 7.21% | 3.34% | 1.16% | 5.44% | 36.32% | 8.19% | 28.23% | 29.85% | 52.08% |
| Article removal (`flu-removearticle`) | 2.21% | 8.04% | 11.88% | 5.36% | 1.49% | 0.72% | 2.30% | 1.69% | 2.25% |
| Random token repetition (`flu-randomtokenrep`) | 14.34% | 69.11% | 21.06% | 19.95% | 62.28% | 28.16% | 91.81% | 67.19% | 86.78% |

---

## Your annotations

For each noise type, name the metric(s) that should be **recommended** for that noise type. A metric is recommended for a noise type iff it has *both* a `high` change rate *and* a `superlinear decrease` for that noise type, as you classified them in the corresponding single card. Multiple metrics may qualify for one noise type; if none qualify, write `none`.

| Noise type | Recommended metric(s)                |
|---|--------------------------------------|
| Verb lemmatization | none                                 |
| Random word drop | UniEval-Coherence, UniEval-Relevance |
| Punctuation noise | none                                 |
| Sentence-middle swap | none                                 |
| Preposition removal | none                                 |
| Stop-word removal | none                                 |
| Local word swap | UniEval-Fluency, UniEval-Relevance   |
| Truncate (remove suffix) | none                                 |
| Article removal | none                                 |
| Random token repetition | BERTScore-f, UniEval-Fluency         |

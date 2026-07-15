# Gold Card v2 — Noised Fluency Test, TED Zh-En
## Compare card across metrics

> **Annotator instructions.** Do not open `sum_mt/reports/noised_fluency/evaluation/Noised_Fluency_TEDMT.pdf` while filling this in. The single-metric tables you produce for `tedmt__bart_score_ted_single.md`, `tedmt__bert_score_f_ted_single.md`, `tedmt__bleu_ted_single.md`, `tedmt__bleurt_ted_single.md` are the per-metric ground truth — this card aggregates them. Save in place.

**Metrics compared:** BARTScore, BERTScore-f, BLEU, BLEURT
**Task:** machine translation
**Dataset:** TED Zh-En, 1000 reference translations (~1 sentence each)
**Perturbation:** ten fluency-noise types each applied at multiple intensity levels.

**Maximum absolute Δ% per (metric, noise type)** — drives the change-rate category. (Refer to the per-metric single cards for full per-variation tables.)

| Noise type | BARTScore max abs(Δ%) | BERTScore-f max abs(Δ%) | BLEU max abs(Δ%) | BLEURT max abs(Δ%) |
|---|---|---|---|---|
| Verb lemmatization (`flu-lemmatizeverb`) | 4.82% | 6.26% | 7.18% | 96.22% |
| Random word drop (`flu-randomworddrop`) | 89.71% | 85.61% | 81.15% | 924.99% |
| Punctuation noise (`flu-noisepunct`) | 15.13% | 19.17% | 29.86% | 67.05% |
| Sentence-middle swap (`flu-sentencemiddleswap`) | 3.28% | 6.83% | 4.90% | 49.19% |
| Preposition removal (`flu-removepreposition`) | 12.56% | 12.43% | 14.20% | 163.50% |
| Stop-word removal (`flu-removestopwords`) | 46.02% | 39.69% | 54.50% | 470.27% |
| Local word swap (`flu-randomlocalswap`) | 50.61% | 59.10% | 54.88% | 698.42% |
| Truncate (remove suffix) (`flu-truncate`) | 54.75% | 26.75% | 55.76% | 242.18% |
| Article removal (`flu-removearticle`) | 8.08% | 5.84% | 13.43% | 60.34% |
| Random token repetition (`flu-randomtokenrep`) | 51.57% | 58.03% | 44.87% | 548.89% |

---

## Your annotations

For each noise type, name the metric(s) that should be **recommended** for that noise type. A metric is recommended for a noise type iff it has *both* a `high` change rate *and* a `superlinear decrease` for that noise type, as you classified them in the corresponding single card. Multiple metrics may qualify for one noise type; if none qualify, write `none`.

| Noise type | Recommended metric(s) |
|---|-----------------------|
| Verb lemmatization | none                  |
| Random word drop | none                  |
| Punctuation noise | none                  |
| Sentence-middle swap | none                  |
| Preposition removal | none                  |
| Stop-word removal | none                  |
| Local word swap | none                  |
| Truncate (remove suffix) | none                  |
| Article removal | none                  |
| Random token repetition | none                  |

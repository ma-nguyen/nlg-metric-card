# [TODO PAPER TITLE]

This repository contains the code base and results of the paper **"[...]"**, 
extending the paper  [On the Blind Spots of Model-Based Evaluation Metrics for Text Generation](https://aclanthology.org/2023.acl-long.674.pdf) with three contributions: **interpreting the findings within LLM evaluation and development**, **automatically generating LLM-based metric cards** and **evaluating the usability of LLM-based metric cards**. 

---

## Project Structure

```
.
├── MetricCard_CreationAndEval/ # Metric Card Creation + Evaluation Setup and Results   
├── sum_mt/                     # Machine Translation (MT/) and Summarization (SUM/)
└── wiki/                       # Open-Ended Generation tests
```

This project runs blind spot tests across three NLP tasks and automatically generates **metric cards** — LLM-written reports that analyse test results and provide in-depth insight into each metric's validity. To evaluate the usability of the automatically generated **metric cards** as pre-written metric cards, participants are tasked to create metric cards and evaluate those.  

---

## Table of Contents
1. [Setup](#1-setup)
2. [Activate Environments](#2-activate-environments)
3. [Run Tests](#3-run-tests)
4. [Saved Results](#4-saved-results)
5. [Generate Metric Card Reports](#5-generate-metric-card-reports)

---

## 1. Setup

### 1.1 Machine Translation & Summarization *(run once)*

```bash
conda create -n ss python=3.10
conda activate ss
pip cache purge
pip install notebook==6.5.6 jupyter_contrib_nbextensions matplotlib --prefer-binary
pip install evaluate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_trf
```

```python
import nltk
nltk.download('punkt_tab')
```

Prepare datasets:
```bash
cd MT && bash prepare_data.sh
cd SUM && bash prepare_data.sh
```

### 1.2 Open-Ended Generation *(run once)*

```bash
conda create -n blindspots_wiki python=3.10
conda activate blindspots_wiki
pip cache purge
conda install pytorch torchvision torchaudio cpuonly -c pytorch
pip install notebook==6.5.6 jupyter_contrib_nbextensions matplotlib --prefer-binary
pip install -r requirements.txt
pip install "numpy<2.0" pyinflect
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_trf
```

Prepare dataset:
```bash
python get_wiki_data.py
```

---

## 2. Activate Environments

```bash
# MT or SUM
conda activate ss

# wiki
conda activate blindspots_wiki
```

---

## 3. Run Tests

This project uses the same test interface as the [original repository](https://github.com/cloudygoose/blindspot_nlg) — refer there for full documentation on all available tests (fluency, consistency, injection, frequent n-gram, positioned error, etc.).

**Quick example (Summarization):**
```bash
cd SUM
python score.py --rouge --hypo_transform flu-truncate-0.1,flu-truncate-0.2,flu-truncate-0.3,
```
The respective output should look like this:
```bash
=== BEGIN OF REPORT for rougeL-f ===
ref: 0.286197 ref-percentage: 0.000000 noise-ratio: 0.000000 std: 0.000000
ref_flu-truncate-0.1: 0.289952 ref-percentage: 1.311899 noise-ratio: 0.113948 std: 0.000000
ref_flu-truncate-0.2: 0.295400 ref-percentage: 3.215607 noise-ratio: 0.215171 std: 0.000000
ref_flu-truncate-0.3: 0.298050 ref-percentage: 4.141645 noise-ratio: 0.312281 std: 0.000000
=== END OF REPORT for rougeL-f ===
```

**Quick example (Open-Ended Generation):**
```bash
# Run all fluency & consistency tests across all metrics
for metric in gpt-ppl mlm-ppl mauve-gpt2 mauve-roberta mauve-electra; do
    ./pipeline.sh $metric ref con-all flu-all
done
```
The respective output is saved in `score_saves/wiki/${metric_name}/${test_name}.json` by default.

---

## 4. Saved Results

Pre-computed test results are saved in:
```bash
# in sum_mt/ or wiki/
results/[perturbation_test]_results/
```

---

## 5. Generate Metric Card Reports

This is the core contribution of this thesis. LLMs are used to automatically generate **metric cards** — analytical reports that interpret blind spot test results.

### Run in `sum_mt/`

```bash
python injection_report.py s           # single reports
python injection_report.py c           # compare reports
python noised_fluency_report.py s sum  # dataset sum 
python noised_fluency_report.py c sum
python noised_fluency_report.py s wmt
python noised_fluency_report.py c wmt
python noised_fluency_report.py s tedmt
python noised_fluency_report.py c tedmt
```

### Run in `wiki/`

```bash
python positioned_error_report.py s
python positioned_error_report.py c
python noised_fluency_report.py s
python noised_fluency_report.py c
```

`s` = single report per result file | `c` = compare report across results

### Report Directory Structure

```
# in sum_mt/ or wiki/
reports/[perturbation_test]/
├── evaluation/              # Alignment of LLM-generated vs. human-written reports
├── prompt_templates/        # Editable prompt templates
├── prompt_value_template/   # Input template for single/compare prompts
├── results_single_reports/  # Generated single metric cards
├── results_single_values/   # Input values for single prompts
├── results_compare_reports/ # Generated compare metric cards
└── results_compare_values/  # Input values for compare prompts
```

### Configure LLM & API Key

In `injection_report.py`, `positioned_error_report.py`, or `noised_fluency_report.py`:

```python
API_KEY = "[Your API-key]"
MODEL = "[Your desired Model]"
```
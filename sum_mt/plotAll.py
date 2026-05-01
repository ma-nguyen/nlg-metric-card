# Development of this software was supported in part by OpenAI ChatGPT.
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import argparse
import math

def extract_from_dict(score_dict, negate=False):
    data = []
    for v in score_dict.values():
        score = -v['mean'] if negate else v['mean']
        data.append((v['edit_ratio'], score, v['std']))
    return sorted(data, key=lambda x: x[0])

def load_result(metric_subdir, negate=False):
    results = []
    ref_path = os.path.join(metric_subdir, 'ref.json')
    if not os.path.exists(ref_path):
        raise FileNotFoundError(f"ref.json nicht gefunden in {metric_subdir}")
    with open(ref_path) as f:
        ref_data = extract_from_dict(json.load(f), negate)
    ref_score = ref_data[0]

    for file in os.listdir(metric_subdir):
        if file.endswith('.json') and file != 'ref.json':
            name = file.replace('.json','')
            with open(os.path.join(metric_subdir, file)) as f:
                data = extract_from_dict(json.load(f), negate)
            data.insert(0, ref_score)
            results.append((name, data))
    return results

def check_rank(score):
    for i in range(len(score)-1):
        if score[i] <= score[i+1] + 1e-5:
            return False
    return True

def transform_name(name, disabled=False):
    name_transforms = {
        'bleu': 'BLEU',
        'bert_score_f': 'BERTScore',
        'bleurt': 'BLEURT-base512',
        'bart_score': 'BARTScore',
        'bart_score_avg_f': 'BARTScore',
        'rouge2-f': 'ROUGE-2',
        'rougeL-f': 'ROUGE-L',
        'unieval_coherence': 'UniEval-coherence(sum)',
        'unieval_consistency': 'UniEval-consistency(sum)',
        'unieval_fluency': 'UniEval-fluency(sum)',
        'unieval_relevance': 'UniEval-relevance(sum)',
        'unieval_overall': 'UniEval-overall(sum)',
    }
    if disabled: return name
    return name_transforms.get(name, name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--metric_results_dir', type=str, required=True)
    parser.add_argument('-o', '--output_path', type=str, default='plot.png')
    parser.add_argument('-m', '--max_edr', type=float, default=0.52)
    parser.add_argument('-e', '--error_bar', action='store_true')
    parser.add_argument('--size', type=float, default=14)
    parser.add_argument('--dpi', type=int, default=300)
    parser.add_argument('--disable_transform', action='store_true')
    parser.add_argument('--legend_fontsize', type=int, default=10)
    args = parser.parse_args()

    plot_order = None
    nrows = 0
    ncols = 0
    if args.metric_results_dir == "score_saves/sum":
        plot_order = [
            'rouge2-f',
            'rougeL-f',
            'bert_score_f',
            'bart_score_avg_f',
            'unieval_coherence',
            'unieval_consistency',
            'unieval_fluency',
            'unieval_relevance',
            'unieval_overall',
        ]

        nrows = 3
        ncols = 4
    elif args.metric_results_dir == "score_saves/ted-zh-en":
        plot_order = [
            'bleu',
            'bert_score_f',
            'bleurt',
            'bart_score'
        ]

        nrows = 1
        ncols = 4
    elif args.metric_results_dir == "score_saves/wmt-de-en":
        plot_order = [
            'bleu',
            'bert_score_f',
            'bleurt',
            'bart_score'
        ]

        nrows = 1
        ncols = 4

    subfolders_all = [f for f in os.listdir(args.metric_results_dir)
                      if os.path.isdir(os.path.join(args.metric_results_dir, f))]
    subfolders = [f for f in plot_order if f in subfolders_all]

    n_plots = len(subfolders)

    fig, axs = plt.subplots(nrows, ncols, figsize=(args.size, args.size*nrows/ncols+1))
    if args.metric_results_dir == "score_saves/sum":
        fig, axs = plt.subplots(nrows, ncols, figsize=(args.size, args.size*nrows/ncols))

    fig.subplots_adjust(top=0.75, bottom=0.15, left=0.05, right=0.95, wspace=0.3, hspace=0.3)
    fig.set_dpi(args.dpi)
    axs = np.array(axs).reshape(-1)

    legend_order = [
        'ref',
        'flu-truncate',
        'flu-lemmatizeverb',
        'flu-randomworddrop',
        'flu-randomtokenrep',
        'flu-noisepunct',
        'flu-removearticle',
        'flu-sentencemiddleswap',
        'flu-removepreposition',
        'flu-randomlocalswap',
        'flu-removestopwords'
    ]

    legend_names = {
        'ref': 'Reference',
        'flu-truncate': 'Truncation',
        'flu-lemmatizeverb': 'Verb lemmatization',
        'flu-randomworddrop': 'Token Drop',
        'flu-randomtokenrep': 'Repeated Token',
        'flu-noisepunct': 'Noised Punctuation',
        'flu-removearticle': 'Article Removel',
        'flu-sentencemiddleswap': 'Middle Swap',
        'flu-removepreposition': 'Preposition Removal',
        'flu-randomlocalswap': 'Local Swap',
        'flu-removestopwords': 'Stop-word Removal'
    }

    handles_all = {}
    labels_all = {}

    for ax, subfolder in zip(axs, subfolders):
        subdir_path = os.path.join(args.metric_results_dir, subfolder)
        negate = 'ppl' in subfolder.lower()
        results = load_result(subdir_path, negate)

        for name, data in results:
            edr, score, score_std = zip(*data)
            edr, score, score_std = list(edr), list(score), list(score_std)
            num = sum([e < args.max_edr for e in edr])
            edr, score, score_std = edr[:num], score[:num], score_std[:num]

            line_type = '.--' if check_rank(score) else '.-'
            line = ax.plot(
                edr, score, line_type,
                label=name,
                linewidth=1.0,
                markersize=3
            )[0]

            if args.error_bar:
                ax.fill_between(edr, np.array(score) - np.array(score_std),
                                np.array(score) + np.array(score_std), alpha=0.2)

            handles_all[name] = line
            labels_all[name] = legend_names.get(name, name)

        ax.set_title(transform_name(subfolder, args.disable_transform))
        ax.set_xlabel('noise-ratio', fontsize = 8)
        ax.set_ylabel('score', fontsize = 8)
        ax.grid(linestyle='--', linewidth=0.5)
        ax.tick_params(axis='x', labelsize=8)
        ax.tick_params(axis='y', labelsize=8)
        ax.set_xticks(np.arange(0, args.max_edr + 0.1, 0.1))
        ax.set_xlim(0, args.max_edr)

    for i in range(n_plots, nrows * ncols):
        axs[i].axis('off')

    handles_sorted = [handles_all[k] for k in legend_order if k in handles_all]
    labels_sorted = [labels_all[k] for k in legend_order if k in labels_all]

    labels_per_row = 5

    if args.metric_results_dir == "score_saves/sum":
        fig.tight_layout(rect=[0, 0, 1, 0.88])
        fig.legend(handles_sorted, labels_sorted, loc='upper center', ncol=labels_per_row,
                   bbox_to_anchor=(0.5, 0.938), fontsize=args.legend_fontsize)
        fig.text(0.5, 0.95, "Fluency Test for SummEval", ha='center', va='bottom', fontsize=14)
    elif args.metric_results_dir == "score_saves/ted-zh-en":
        fig.tight_layout(rect=[0, 0, 1, 0.7])
        fig.legend(handles_sorted, labels_sorted, loc='upper center', ncol=labels_per_row,
                   bbox_to_anchor=(0.5, 0.85), fontsize=args.legend_fontsize)
        fig.text(0.5, 0.88, "Fluency Test for WMT", ha='center', va='bottom', fontsize=14)
    elif args.metric_results_dir == "score_saves/wmt-de-en":
        fig.tight_layout(rect=[0, 0, 1, 0.7])
        fig.legend(handles_sorted, labels_sorted, loc='upper center', ncol=labels_per_row,
                   bbox_to_anchor=(0.5, 0.85), fontsize=args.legend_fontsize)
        fig.text(0.5, 0.88, "Fluency Test for TEDMT", ha='center', va='bottom', fontsize=14)

    fig.savefig(args.output_path, dpi=args.dpi)
    print("Saved to", args.output_path)
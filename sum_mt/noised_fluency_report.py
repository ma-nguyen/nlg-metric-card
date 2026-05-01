# Development of this software was supported in part by OpenAI ChatGPT.
import os
import re
import sys
import json
import requests
import argparse
from collections import defaultdict

def set_template_fluency_dir(task_dataset, prompt_type):
    if prompt_type == "single":
        if task_dataset == "sum":
            print("------ Report for the task: Summary, using the CNN-Dailymail data set ------")
            template_file = os.path.join(TEMPLATE_DIR, "sum_pt.txt")
            fluency_dir = "score_saves/sum"
        elif task_dataset == "wmt":
            print("------ Report for the task: Machine Translation, using the WMT data set ------")
            template_file = os.path.join(TEMPLATE_DIR, "wmt_pt.txt")
            fluency_dir = "score_saves/wmt-de-en"
        elif task_dataset == "tedmt":
            print("------ Report for the task: Machine Translation, using the TED-MT data set ------")
            template_file = os.path.join(TEMPLATE_DIR, "tedmt_pt.txt")
            fluency_dir = "score_saves/ted-zh-en"
    elif prompt_type == "compare":
        if task_dataset == "sum":
            print("------ Report for the task: Summary, using the CNN-Dailymail data set ------")
            template_file = os.path.join(TEMPLATE_DIR, "sum_cpt.txt")
            fluency_dir = "score_saves/sum"
        elif task_dataset == "wmt":
            print("------ Report for the task: Machine Translation, using the WMT data set ------")
            template_file = os.path.join(TEMPLATE_DIR, "wmt_cpt.txt")
            fluency_dir = "score_saves/wmt-de-en"
        elif task_dataset == "tedmt":
            print("------ Report for the task: Machine Translation, using the TED-MT data set ------")
            template_file = os.path.join(TEMPLATE_DIR, "tedmt_cpt.txt")
            fluency_dir = "score_saves/ted-zh-en"

    return template_file, fluency_dir

def set_output_dir(task_dataset, prompt_type):
    if prompt_type == "single":
        if task_dataset == "sum":
            output_dir = os.path.join(ROOT_OUTPUT_DIR, "results_single_reports", "sum")
        elif task_dataset == "wmt":
            output_dir = os.path.join(ROOT_OUTPUT_DIR, "results_single_reports", "wmt")
        elif task_dataset == "tedmt":
            output_dir = os.path.join(ROOT_OUTPUT_DIR, "results_single_reports", "tedmt")
    elif prompt_type == "compare":
        if task_dataset == "sum":
            output_dir = os.path.join(ROOT_OUTPUT_DIR, "results_compare_reports", "sum")
        elif task_dataset == "wmt":
            output_dir = os.path.join(ROOT_OUTPUT_DIR, "results_compare_reports", "wmt")
        elif task_dataset == "tedmt":
            output_dir = os.path.join(ROOT_OUTPUT_DIR, "results_compare_reports", "tedmt")

    return output_dir

def pipeline_single_prompts(task_dataset):
    print("Running single prompt pipeline...")

    template_file, fluency_dir = set_template_fluency_dir(task_dataset, "single")
    template = load_template(template_file)
    output_dir = set_output_dir(task_dataset, "single")

    for metric in os.listdir(fluency_dir):
        if metric == "cache":
            continue
        if metric == ".DS_Store":
            continue

        metric_dir = os.path.join(fluency_dir, metric)

        result = parse_tables_to_text_s(metric_dir, task_dataset)

        template_filled = template.replace(f"[result]", result)
        prompt = template_filled.replace(f"[metric]", metric)

        file_path, filename = generate_filename(metric, output_dir)

        llm_reply = call_llm_api(prompt, API_URL, API_KEY, MODEL)
        llm_reply = clean_text(llm_reply)

        save_report(file_path, llm_reply)

def pipeline_compare_prompt(task_dataset):
    print("Running compare prompt pipeline...")

    template_file, fluency_dir = set_template_fluency_dir(task_dataset, "compare")
    template = load_template(template_file)
    output_dir = set_output_dir(task_dataset, "compare")

    metrics = []
    for metric in os.listdir(fluency_dir):
        if metric == "cache":
            continue
        if metric == ".DS_Store":
            continue

        metrics.append(metric)

    result = parse_tables_to_text_c(fluency_dir)
    template = template.replace(f"[result]", result)
    prompt = template.replace(f"[metric]", " ".join(metrics))

    file_path, filename = generate_filename(metrics, output_dir)

    llm_reply = call_llm_api(prompt, API_URL, API_KEY, MODEL)
    llm_reply = clean_text(llm_reply)

    save_report(file_path, llm_reply)

def load_template(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Prompt Template-File '{filepath}' not found.")
        sys.exit(1)

def load_values(filepath):
    values = {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, val = line.split("=", 1)
                    values[key.strip()] = val.strip()
        return values
    except FileNotFoundError:
        print(f"Error: Prompt Values-File '{filepath}' not found.")
        sys.exit(1)


def read_json_files(metric_dir):
    data = defaultdict(dict)
    global_ref = None

    for filename in os.listdir(metric_dir):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(metric_dir, filename)

        with open(filepath, "r", encoding="utf-8") as f:
            content = json.load(f)

        for key, metrics in content.items():
            if "-" in key:
                test_name, variation = key.rsplit("-", 1)
            else:
                test_name, variation = key, "unknown"

            if test_name.lower() == "ref":
                global_ref = metrics
            else:
                data[test_name][variation] = metrics

    return data, global_ref

def variation_to_display(var, test_name):
    map_var = var.replace("_seedreduce", "").lower()
    if test_name.lower() == "sentencemiddleswap":
        try:
            return str(int(float(map_var)))
        except ValueError:
            return map_var
    else:
        try:
            if map_var.lower() in ("gold", "unknown"):
                return map_var
        except AttributeError:
            pass
        try:
            return f"{int(float(map_var) * 100)}"
        except ValueError:
            return map_var

def calc_change(result, ref):
    return (result - ref) / abs(ref) * 100.0

def generate_table(test_name, variations, global_ref):
    lines = ["Variation\tScore\tEdit_Ratio"]
    map_key = test_name.replace("ref_flu-", "").lower()

    if global_ref:
        lines.append(f"gold\t{global_ref['mean']:.3f}\t{global_ref['edit_ratio']:.3f}")

    for var, metrics in variations.items():
        var_display = variation_to_display(var, map_key)
        lines.append(f"{var_display}\t{metrics['mean']:.3f}\t{metrics['edit_ratio']:.3f}")

    return f"Table for {test_name}:\n" + "\n".join(lines) + "\n"

def generate_text_from_table(metric, test_name, variations, global_ref):
    TEST_DESCRIPTIONS = {
        "gold": "unperturbed gold outputs",
        "truncate": "{var}% of words at the end of the gold outputs are removed",
        "removearticle": "{var}% of articles (the/a/an) of the gold outputs are removed",
        "removepreposition": "{var}% of prepositions of the gold outputs are removed",
        "removestopwords": "{var}% of stop-words of the gold outputs are removed",
        "lemmatizeverb": "{var}% of verbs of the gold outputs are randomized",
        "randomworddrop": "{var}% of words of the gold outputs are removed",
        "randomtokenrep": "{var}% of words of the gold outputs are repeated once",
        "randomlocalswap": "{var}% of words of the gold outputs are swapped",
        "sentencemiddleswap": "the left and right part of the sentence is swapped (cut-off point is in the middle) to synthesize wrong SVO order. Done for {var} sentences",
        "noisepunct": "{var}% punctuation of the gold outputs are noised"
    }

    text_lines = []
    text_lines.append(metric)
    idx = 1
    map_key = test_name.replace("ref_flu-", "").lower()

    if global_ref:
        desc_template = TEST_DESCRIPTIONS.get("gold", "gold text")
        description = desc_template
        text_lines.append(f"{idx}. when {description}, the metric scores a {global_ref['mean']:.3f}, edit_ratio: {global_ref['edit_ratio']:.3f}, leading to a change of {calc_change(global_ref['mean'], global_ref['mean']):.1f}%")
        idx += 1

    for var, values in variations.items():
        var_display = variation_to_display(var, map_key)
        desc_template = TEST_DESCRIPTIONS.get(map_key, f"{var_display} variation of {map_key}")
        description = desc_template.format(var=var_display)
        text_lines.append(f"{idx}. when {description}, the metric scores a {values['mean']:.3f}, edit_ratio: {values['edit_ratio']:.3f}, leading to a change of {calc_change(values['mean'], global_ref['mean']):.1f}%")
        idx += 1

    return f"Textual Description of {test_name}:\n" + "\n".join(text_lines) + "\n", text_lines




def save_tables(tables, output_file):
    with open(output_file, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(tables))

def save_texts(texts, output_file):
    with open(output_file, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(texts))

def save_concatenated(text_lines_all, output_file):
    concatenated = " ".join(text_lines_all)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(concatenated)



def parse_json_files(metric_dir, output_file_tables, output_file_text, output_file_concat):
    data, global_ref = read_json_files(metric_dir)
    metric = os.path.basename(metric_dir)

    all_tables = []
    all_texts = []
    all_lines_concat = []

    for test_name, variations in data.items():
        table_str = generate_table(test_name, variations, global_ref)
        all_tables.append(table_str)

        table_text, lines = generate_text_from_table(metric, test_name, variations, global_ref)
        all_texts.append(table_text)
        all_lines_concat.extend(lines)


    save_tables(all_tables, output_file_tables)
    save_texts(all_texts, output_file_text)
    save_concatenated(all_lines_concat, output_file_concat)
    print("Debugging-Info has been saved in sum_mt/reports/noised_fluency/debug")

def parse_tables_to_text_s(metric_dir, task_dataset):
    if task_dataset == "sum":
        debug_directory = os.path.join(BASE_DIR, "reports", "noised_fluency", "debug", "sum")
    elif task_dataset == "wmt":
        debug_directory = os.path.join(BASE_DIR, "reports", "noised_fluency", "debug", "wmt")
    elif task_dataset == "tedmt":
        debug_directory = os.path.join(BASE_DIR, "reports", "noised_fluency", "debug", "tedmt")

    output_file_tables = os.path.join(debug_directory, "all_tables.txt")
    output_file_text = os.path.join(debug_directory, "all_descriptions.txt")
    output_file_concat = os.path.join(debug_directory, "all_descriptions_concatenated.txt")

    parse_json_files(metric_dir, output_file_tables, output_file_text, output_file_concat)

    with open(output_file_concat, "r", encoding="utf-8") as f:
        return f.read()

def parse_tables_to_text_c(fluency_dir):
    debug_directory = os.path.join(BASE_DIR, "reports", "noised_fluency", "debug", "all")

    all_concat_texts = []

    for metric_name in os.listdir(fluency_dir):
        metric_dir = os.path.join(fluency_dir, metric_name)
        if not os.path.isdir(metric_dir):
            continue

        output_file_tables = os.path.join(debug_directory, f"{metric_name}_all_tables.txt")
        output_file_text = os.path.join(debug_directory, f"{metric_name}_all_descriptions.txt")
        output_file_concat = os.path.join(debug_directory, f"{metric_name}_all_descriptions_concatenated.txt")

        parse_json_files(metric_dir, output_file_tables, output_file_text, output_file_concat)

        with open(output_file_concat, "r", encoding="utf-8") as f:
            metric_text = f"{metric_name}:\n{f.read()}\n"
            all_concat_texts.append(metric_text)

    return "\n".join(all_concat_texts)

def fill_template(template, values):
    for key, val in values.items():
        template = template.replace(f"[{key}]", val)
    return template

def generate_filename(metric_s, output_dir):
    if isinstance (metric_s, str):
        filename = re.sub(r"[^a-zA-Z0-9]", "", metric_s).lower()
        base_filename = filename + ".txt"
    elif isinstance (metric_s, list):
        filename_parts = [re.sub(r"[^a-zA-Z0-9]", "", m).lower() for m in metric_s]
        base_filename = "_".join(filename_parts) + ".txt"

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, base_filename)

    while os.path.exists(file_path):
        print(f"File-Name '{base_filename}' is already taken.")
        choice = input("Overwrite (o), New Name (n) or Abort (a)? [o/n/a]: ").strip().lower()
        if choice == "o":
            break
        elif choice == "n":
            new_name = input("Please enter new File-Name (without Path, .txt will be appended): ").strip()
            if not new_name.endswith(".txt"):
                new_name += ".txt"
            file_path = os.path.join(output_dir, new_name)
            base_filename = new_name
        elif choice == "a":
            sys.exit(1)

    return file_path, base_filename

def call_llm_api(prompt, api_url, api_key, model):
    headers = {
        "Accept": "application/api_urljson",
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are an assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 20000,
        "temperature": 0.0,
        "top_p": 0.5
    }
    print("Request to Model has been sent. Waiting for Response ...")
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"API-Error: Status {response.status_code} - {response.text}")
        sys.exit(1)

    return response.json()["choices"][0]["message"]["content"]

def clean_text(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = text.replace("\u202F", " ").replace("\u00A0", " ").replace("[NNBSP]", " ").strip()

    return text

def save_report(file_path, content):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Report saved as: '{os.path.basename(file_path)}'")
        return True
    except Exception as e:
        print(f"Error: Saving failed: {e}")
        return False


if __name__ == "__main__":
    API_URL = "https://chat-ai.academiccloud.de/v1/chat/completions"
    API_KEY = "99a0aa3518ee41d994be433c896f736c"
    MODEL = "llama-3.3-70b-instruct"

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, "reports", "noised_fluency", "prompt_templates")
    ROOT_VALUES_DIR = os.path.join(BASE_DIR, "reports", "noised_fluency")
    ROOT_OUTPUT_DIR = os.path.join(BASE_DIR, "reports", "noised_fluency")

    parser = argparse.ArgumentParser(description="Run prompt pipeline")
    parser.add_argument(
        "prompt_type",
        choices=["s", "c"],
        help="Choose prompt type: 's' for single_prompt, 'c' for compare_prompt"
    )
    parser.add_argument(
        "fluency_task_dataset",
        choices=["sum", "wmt", "tedmt"],
        help="Choose prompt type: 'sum' for summarization, 'wmt' for machine translation on WMT, 'tedmt' for machine translation for TED-MT"
    )
    args = parser.parse_args()

    if args.prompt_type == "s":
        pipeline_single_prompts(args.fluency_task_dataset)
    elif args.prompt_type == "c":
        pipeline_compare_prompt(args.fluency_task_dataset)
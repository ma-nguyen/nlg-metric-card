# Development of this software was supported in part by OpenAI ChatGPT.
import os
import re
import sys
import requests
import argparse

def pipeline_single_prompts():
    print("Running single prompt pipeline...")

    template_file = os.path.join(TEMPLATE_DIR, "positioned_error_pt.txt")
    template = load_template(template_file)

    output_dir = os.path.join(ROOT_OUTPUT_DIR, "results_single_reports")

    values_dir = os.path.join(ROOT_VALUES_DIR, "results_single_values")
    for val_file in os.listdir(values_dir):
        if not val_file.endswith(".txt"):
            continue

        values_path = os.path.join(values_dir, val_file)

        values = load_values(values_path)
        metric = [values.get("metric", "llm_response")]

        format_changes(values) # given the values calculate changes and format them for the prompt

        prompt = fill_template(template, values)

        file_path, filename = generate_filename(metric, output_dir)

        llm_reply = call_llm_api(prompt, API_URL, API_KEY, MODEL)
        llm_reply = clean_text(llm_reply)

        save_report(file_path, llm_reply)

def pipeline_compare_prompt():
    print("Running compare prompt pipeline...")

    template_file = os.path.join(TEMPLATE_DIR, "positioned_error_cpt.txt")
    template = load_template(template_file)

    output_dir = os.path.join(ROOT_OUTPUT_DIR, "results_compare_reports")

    values_path = os.path.join(ROOT_VALUES_DIR, "results_compare_values", "positioned_error_cval.txt")
    values = load_values(values_path)

    metrics = values["metrics"].split()
    format_table(values, metrics)  # given the values calculate changes and format the table for the prompt

    prompt = fill_template(template, values)

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

def calc_change(result, ref):
    return (result - ref) / abs(ref) * 100.0

def format_changes(values):
    ref = float(values.get("ref", 1))
    keys = [
        "shuffling_beginning", "shuffling_middle", "shuffling_end",
        "random_beginning", "random_middle", "random_end"
    ]
    for key in keys:
        result = float(values.get(f"result_{key}", 0))
        change = calc_change(result, ref)
        values[f"change_{key}"] = f"{change:+.1f}%"

def format_table(values, metrics):
    ref_list = list(map(float, values["ref"].split()))
    keys_map = {
        "rsb": "result_shuffling_beginning",
        "rsm": "result_shuffling_middle",
        "rse": "result_shuffling_end",
        "rrb": "result_random_beginning",
        "rrm": "result_random_middle",
        "rre": "result_random_end",
    }
    data_lists = {short: list(map(float, values[long].split())) for short, long in keys_map.items()}

    header = (
        "Metric\tRef\t"
        "Shuff_Beg\tΔShuff_Beg(%)\t"
        "Shuff_Mid\tΔShuff_Mid(%)\t"
        "Shuff_End\tΔShuff_End(%)\t"
        "Rand_Beg\tΔRand_Beg(%)\t"
        "Rand_Mid\tΔRand_Mid(%)\t"
        "Rand_End\tΔRand_End(%)"
    )
    lines = [header]
    for i, metric in enumerate(metrics):
        row = [
            metric,
            f"{ref_list[i]:.3f}",
            f"{data_lists['rsb'][i]:.3f}", f"{calc_change(data_lists['rsb'][i], ref_list[i]):+.1f}",
            f"{data_lists['rsm'][i]:.3f}", f"{calc_change(data_lists['rsm'][i], ref_list[i]):+.1f}",
            f"{data_lists['rse'][i]:.3f}", f"{calc_change(data_lists['rse'][i], ref_list[i]):+.1f}",
            f"{data_lists['rrb'][i]:.3f}", f"{calc_change(data_lists['rrb'][i], ref_list[i]):+.1f}",
            f"{data_lists['rrm'][i]:.3f}", f"{calc_change(data_lists['rrm'][i], ref_list[i]):+.1f}",
            f"{data_lists['rre'][i]:.3f}", f"{calc_change(data_lists['rre'][i], ref_list[i]):+.1f}",
        ]
        lines.append("\t".join(row))

    table = "\n".join(lines)
    values["table"] = table.strip()


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
        "max_tokens": 7000,
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
    text = text.replace("\u202F", " ").replace("\u00A0", " ").replace("[NNBSP]", " ").replace(" ", " ").strip()

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


# === MAIN ===
if __name__ == "__main__":
    # API configuration comes from the environment; see README.
    API_URL = os.environ.get(
        "METRICX_API_URL",
        "https://chat-ai.academiccloud.de/v1/chat/completions")
    API_KEY = os.environ.get("METRICX_API_KEY")
    if not API_KEY:
        sys.exit("Error: set the METRICX_API_KEY environment variable "
                 "(API key for the LLM endpoint).")
    MODEL = os.environ.get("METRICX_MODEL", "qwen3-32b")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMPLATE_DIR = os.path.join(BASE_DIR, "reports", "positioned_error", "prompt_templates")
    ROOT_VALUES_DIR = os.path.join(BASE_DIR, "reports", "positioned_error")
    ROOT_OUTPUT_DIR = os.path.join(BASE_DIR, "reports", "positioned_error")

    parser = argparse.ArgumentParser(description="Run prompt pipeline")
    parser.add_argument(
        "prompt_type",
        choices=["s", "c"],
        help="Choose prompt type: 's' for single_prompt, 'c' for compare_prompt"
    )
    args = parser.parse_args()

    print("------ Report for the task: Open-ended Text, using the WikiText-103 data set ------")
    if args.prompt_type == "s":
        pipeline_single_prompts()
    elif args.prompt_type == "c":
        pipeline_compare_prompt()


"""DeepSeek as LLM-as-a-judge over the participant Metric Cards.

Uses the OpenAI-compatible DeepSeek endpoint. Caches each call's raw JSON
response so re-runs are free; safe to interrupt and resume.

Requires: openai>=1.0, env var DEEPSEEK_API_KEY.

Usage:
    DEEPSEEK_API_KEY=sk-... python analysis/judge_deepseek.py \\
        [--cards-dir analysis/cards_text] \\
        [--out analysis/outputs/deepseek_ratings.csv] \\
        [--model deepseek-chat] \\
        [--seeds 0 1 2]
"""
import argparse
import json
import os
import sys
import time

from openai import OpenAI

from judge_common import (
    JSON_SCHEMA, SYSTEM_PROMPT, USER_TEMPLATE,
    run_judge_loop, validate_data,
)


def make_call_fn(client, model, max_retries=3):
    def call(card_text, seed):
        last_err = None
        for attempt in range(max_retries):
            try:
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user",
                         "content": USER_TEMPLATE.format(card_text=card_text)},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.0,
                    seed=seed,
                    max_tokens=1500,
                )
                raw = resp.choices[0].message.content
                data = validate_data(json.loads(raw))
                return data, raw
            except Exception as e:
                last_err = e
                time.sleep(2 ** attempt)
        raise RuntimeError(
            f"DeepSeek call failed after {max_retries} retries: {last_err}"
        )
    _ = JSON_SCHEMA  # imported for parity with structured-output providers
    return call


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cards-dir", default="analysis/cards_text")
    ap.add_argument("--out", default="analysis/outputs/deepseek_ratings.csv")
    ap.add_argument("--cache-dir", default="analysis/outputs/deepseek_cache")
    ap.add_argument("--model", default="deepseek-chat")
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    ap.add_argument("--base-url", default="https://api.deepseek.com")
    args = ap.parse_args()

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        sys.exit("ERROR: set DEEPSEEK_API_KEY environment variable")

    client = OpenAI(api_key=api_key, base_url=args.base_url)
    run_judge_loop(
        cards_dir=args.cards_dir, cache_dir=args.cache_dir, out_path=args.out,
        seeds=args.seeds, model_name=args.model, provider="deepseek",
        call_fn=make_call_fn(client, args.model),
    )


if __name__ == "__main__":
    main()

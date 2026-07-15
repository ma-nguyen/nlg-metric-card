"""Google Gemini as LLM-as-a-judge over the participant Metric Cards.

Same rubric as judge_deepseek.py / judge_anthropic.py; outputs the same CSV
schema. Uses the google-genai SDK with structured outputs
(response_mime_type="application/json" + response_schema) so the response
is guaranteed to validate against the rubric.

Defaults to gemini-2.5-pro. For tier-comparable comparison against
deepseek-chat / claude-sonnet-4-6, pass --model gemini-2.5-flash.

Requires: google-genai>=0.3, env var GEMINI_API_KEY (or GOOGLE_API_KEY).

Usage:
    GEMINI_API_KEY=... python analysis/judge_gemini.py \\
        [--cards-dir analysis/cards_text] \\
        [--out analysis/outputs/gemini_ratings.csv] \\
        [--model gemini-2.5-pro] \\
        [--seeds 0 1 2]
"""
import argparse
import json
import os
import sys
import time

from google import genai
from google.genai import types as gtypes

from judge_common import (
    DIMENSIONS, KEY_FOR, SYSTEM_PROMPT, USER_TEMPLATE,
    run_judge_loop, validate_data,
)

GEMINI_SCHEMA = {
    "type": "object",
    "properties": {
        **{KEY_FOR[d]: {"type": "integer", "minimum": 1, "maximum": 5}
           for d in DIMENSIONS},
        "rationale": {
            "type": "object",
            "properties": {KEY_FOR[d]: {"type": "string"} for d in DIMENSIONS},
            "required": [KEY_FOR[d] for d in DIMENSIONS],
        },
    },
    "required": [KEY_FOR[d] for d in DIMENSIONS] + ["rationale"],
}


def make_call_fn(client, model, max_retries=3):
    def call(card_text, seed):
        last_err = None
        for attempt in range(max_retries):
            try:
                resp = client.models.generate_content(
                    model=model,
                    contents=USER_TEMPLATE.format(card_text=card_text),
                    config=gtypes.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT,
                        temperature=0.0,
                        seed=seed,
                        response_mime_type="application/json",
                        response_schema=GEMINI_SCHEMA,
                        max_output_tokens=2048,
                    ),
                )
                raw = resp.text
                data = validate_data(json.loads(raw))
                return data, raw
            except Exception as e:
                last_err = e
                time.sleep(2 ** attempt)
        raise RuntimeError(
            f"Gemini call failed after {max_retries} retries: {last_err}"
        )
    return call


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cards-dir", default="analysis/cards_text")
    ap.add_argument("--out", default="analysis/outputs/gemini_ratings.csv")
    ap.add_argument("--cache-dir", default="analysis/outputs/gemini_cache")
    ap.add_argument("--model", default="gemini-3.1-pro-preview")
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    args = ap.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        sys.exit("ERROR: set GEMINI_API_KEY (or GOOGLE_API_KEY) environment variable")

    client = genai.Client(api_key=api_key)
    run_judge_loop(
        cards_dir=args.cards_dir, cache_dir=args.cache_dir, out_path=args.out,
        seeds=args.seeds, model_name=args.model, provider="gemini",
        call_fn=make_call_fn(client, args.model),
    )


if __name__ == "__main__":
    main()

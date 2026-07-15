"""Anthropic Claude as LLM-as-a-judge over the participant Metric Cards.

Same rubric as judge_deepseek.py / judge_gemini.py; outputs the same CSV
schema. Uses the official anthropic SDK with structured outputs (json_schema)
so the response is guaranteed to validate against the rubric.

Defaults to claude-opus-4-7. For tier-comparable comparison against
deepseek-chat and gemini-2.5-flash, pass --model claude-sonnet-4-6.

Note: Anthropic Messages API does not expose a `seed` parameter. The three
"seeds" produce three independent calls; any variance reflects the model's
natural decoding nondeterminism rather than seeded randomness.

Requires: anthropic>=0.50, env var ANTHROPIC_API_KEY.

Usage:
    ANTHROPIC_API_KEY=sk-ant-... python analysis/judge_anthropic.py \\
        [--cards-dir analysis/cards_text] \\
        [--out analysis/outputs/anthropic_ratings.csv] \\
        [--model claude-opus-4-7] \\
        [--seeds 0 1 2]
"""
import argparse
import json
import os
import sys
import time

import anthropic

from judge_common import (
    JSON_SCHEMA, SYSTEM_PROMPT, USER_TEMPLATE,
    run_judge_loop, validate_data,
)


def make_call_fn(client, model, max_retries=3):
    def call(card_text, seed):
        last_err = None
        for attempt in range(max_retries):
            try:
                resp = client.messages.create(
                    model=model,
                    max_tokens=2048,
                    system=SYSTEM_PROMPT,
                    messages=[{
                        "role": "user",
                        "content": USER_TEMPLATE.format(card_text=card_text),
                    }],
                    output_config={
                        "format": {"type": "json_schema", "schema": JSON_SCHEMA},
                    },
                )
                text_blocks = [b for b in resp.content if b.type == "text"]
                if not text_blocks:
                    raise ValueError(f"no text block in response: {resp}")
                raw = text_blocks[0].text
                data = validate_data(json.loads(raw))
                return data, raw
            except Exception as e:
                last_err = e
                time.sleep(2 ** attempt)
        raise RuntimeError(
            f"Anthropic call failed after {max_retries} retries: {last_err}"
        )
    return call


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cards-dir", default="analysis/cards_text")
    ap.add_argument("--out", default="analysis/outputs/anthropic_ratings.csv")
    ap.add_argument("--cache-dir", default="analysis/outputs/anthropic_cache")
    ap.add_argument("--model", default="claude-opus-4-7")
    ap.add_argument("--seeds", nargs="+", type=int, default=[0, 1, 2])
    args = ap.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ERROR: set ANTHROPIC_API_KEY environment variable")

    client = anthropic.Anthropic()
    run_judge_loop(
        cards_dir=args.cards_dir, cache_dir=args.cache_dir, out_path=args.out,
        seeds=args.seeds, model_name=args.model, provider="anthropic",
        call_fn=make_call_fn(client, args.model),
    )


if __name__ == "__main__":
    main()

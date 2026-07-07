"""
session3_2_disclosure_evaluator.py
Session 3.2 — Research Judgement in an Institutional Context

Evaluates a draft AI disclosure statement against the five-element minimum
disclosure standard and generates a revised compliant statement.

Usage:
    python session3_2_disclosure_evaluator.py \
        --text "AI tools were used to assist with the preparation of this manuscript." \
        --provider gemini \
        --output report_session3_2.txt

    python session3_2_disclosure_evaluator.py \
        --file disclosure_draft.txt \
        --provider gemini

Environment variables:
    GEMINI_API_KEY, GROQ_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY
"""

import argparse
import datetime
from llm_client import call_llm, get_client_info

DISCLOSURE_SYSTEM = (
    "You are a research integrity advisor specializing in AI disclosure standards. "
    "Evaluate the following disclosure statement or methods section against the "
    "five-element minimum AI disclosure standard:\n\n"
    "1. Task specification: Does it state exactly which tasks AI was used for?\n"
    "2. Tool identification: Does it name the model, version, and date of use?\n"
    "3. Prompt documentation: Does it provide or reference the exact prompts used?\n"
    "4. Verification statement: Does it describe what verification steps were applied?\n"
    "5. Failure-mode report: Does it report the failure-discovery rate and corrections made?\n\n"
    "For each element: "
    "(a) State whether it is present, absent, or partially present. "
    "(b) Quote the relevant text if present. "
    "(c) Provide specific guidance on what to add if absent or insufficient. "
    "Conclude with a revised disclosure statement that meets all five elements, "
    "based on what can be inferred from the text provided. "
    "Mark any inferred details with [RESEARCHER TO COMPLETE] where actual information is needed."
)

POLICY_CHECK_SYSTEM = (
    "You are a research compliance advisor. Given the following AI disclosure statement, "
    "assess whether it would satisfy the disclosure requirements of: "
    "(1) Nature Portfolio journals "
    "(2) Elsevier journals "
    "(3) NIH grant applications "
    "For each, state: compliant / partially compliant / non-compliant, and explain why. "
    "Note: Base your assessment on general knowledge of these policies as of 2025–2026. "
    "Always recommend the researcher verify against the current policy at the source."
)


def run(text: str, provider: str, model: str = None) -> dict:
    info = get_client_info(provider, model)
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")

    print(f"\n{'='*70}")
    print("SESSION 3.2 — AI DISCLOSURE STATEMENT EVALUATOR")
    print(f"{'='*70}")
    print(f"Provider : {info}")
    print(f"Timestamp: {timestamp}")
    print(f"{'='*70}\n")
    print(f"Draft disclosure ({len(text)} chars):\n{text}\n")

    print("── STEP 1: FIVE-ELEMENT EVALUATION ──────────────────────────────────")
    evaluation = call_llm(DISCLOSURE_SYSTEM, f"Disclosure statement:\n\n{text}", provider=provider, model=model)
    print(evaluation)

    print("\n── STEP 2: PUBLISHER/FUNDER POLICY CHECK ────────────────────────────")
    policy_check = call_llm(POLICY_CHECK_SYSTEM, f"Disclosure statement:\n\n{text}", provider=provider, model=model)
    print(policy_check)

    print("\n── REMINDER ──────────────────────────────────────────────────────────")
    print(
        "The revised statement is a starting point only. You must complete all\n"
        "[RESEARCHER TO COMPLETE] sections with the actual details of your AI use.\n"
        "Always verify compliance against the current policy of your specific journal or funder.\n"
        "(Zyphur 2026, Competency 2: Model and Parameter Specification)"
    )

    return {
        "text": text,
        "provider": info,
        "timestamp": timestamp,
        "evaluation": evaluation,
        "policy_check": policy_check,
    }


def main():
    parser = argparse.ArgumentParser(description="Session 3.2 — AI Disclosure Statement Evaluator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Draft disclosure statement as a string")
    group.add_argument("--file", help="Path to a .txt file containing the draft disclosure statement")
    parser.add_argument("--provider", default="gemini", choices=["gemini", "groq", "openai", "claude"])
    parser.add_argument("--model", default=None)
    parser.add_argument("--output", default=None, help="Optional output file path (.txt)")
    args = parser.parse_args()

    if args.file:
        with open(args.file, "r") as f:
            text = f.read()
    else:
        text = args.text

    results = run(text, args.provider, args.model)

    if args.output:
        with open(args.output, "w") as f:
            f.write(f"SESSION 3.2 — AI DISCLOSURE STATEMENT EVALUATOR\n")
            f.write(f"Provider : {results['provider']}\nTimestamp: {results['timestamp']}\n\n")
            f.write("── FIVE-ELEMENT EVALUATION ──\n" + results["evaluation"] + "\n\n")
            f.write("── PUBLISHER/FUNDER POLICY CHECK ──\n" + results["policy_check"] + "\n")
        print(f"\nReport saved to: {args.output}")


if __name__ == "__main__":
    main()

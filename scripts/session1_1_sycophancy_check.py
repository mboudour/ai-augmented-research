"""
session1_1_sycophancy_check.py
Session 1.1 — Research Judgement in an AI Environment

Runs a sycophancy check and adversarial critique on a research question or hypothesis.
Outputs a structured report to stdout and optionally to a text file.

Usage:
    python session1_1_sycophancy_check.py \
        --question "Does social media use increase political polarization?" \
        --provider gemini \
        --output report_session1_1.txt

Environment variables:
    GEMINI_API_KEY, GROQ_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY
"""

import argparse
import datetime
from llm_client import call_llm, get_client_info

SYCOPHANCY_SYSTEM = (
    "You are a critical research methods advisor. Your task is to identify any "
    "assumptions, biases, or leading framings embedded in the research question or "
    "hypothesis provided. Do not answer the question itself. Instead: "
    "(1) List the assumptions the question takes for granted. "
    "(2) Explain how each assumption could bias the research design or interpretation. "
    "(3) Suggest a more neutral reformulation of the question. "
    "Be specific and direct."
)

ADVERSARIAL_SYSTEM = (
    "You are a rigorous academic peer reviewer. Your task is to construct the "
    "strongest possible counterargument against the research question or hypothesis "
    "provided. Draw on methodological, theoretical, and empirical objections. "
    "Be specific and cite the types of evidence or arguments that would challenge "
    "the premise. Do not be diplomatic — your goal is to stress-test the research."
)


def run(question: str, provider: str, model: str = None) -> dict:
    info = get_client_info(provider, model)
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")

    print(f"\n{'='*70}")
    print("SESSION 1.1 — SYCOPHANCY CHECK & ADVERSARIAL CRITIQUE")
    print(f"{'='*70}")
    print(f"Provider : {info}")
    print(f"Timestamp: {timestamp}")
    print(f"Question : {question}")
    print(f"{'='*70}\n")

    print("── STEP 1: SYCOPHANCY CHECK ──────────────────────────────────────────")
    print(f"System prompt: {SYCOPHANCY_SYSTEM[:120]}...\n")
    syco_result = call_llm(SYCOPHANCY_SYSTEM, f"Research question: {question}", provider=provider, model=model)
    print(syco_result)

    print("\n── STEP 2: ADVERSARIAL CRITIQUE ──────────────────────────────────────")
    print(f"System prompt: {ADVERSARIAL_SYSTEM[:120]}...\n")
    adv_result = call_llm(ADVERSARIAL_SYSTEM, f"Research question or hypothesis: {question}", provider=provider, model=model)
    print(adv_result)

    print("\n── VERIFICATION REMINDER ─────────────────────────────────────────────")
    print(
        "Review each identified assumption and objection independently against the literature.\n"
        "An AI critique is a brainstorm prompt, not a peer review. Your domain expertise\n"
        "must assess which objections are substantive and which reflect model limitations.\n"
        "(Zyphur 2026, Competency 5: Sycophancy Detection and Human-as-Verifier Discipline)"
    )

    return {
        "question": question,
        "provider": info,
        "timestamp": timestamp,
        "sycophancy_check": syco_result,
        "adversarial_critique": adv_result,
    }


def main():
    parser = argparse.ArgumentParser(description="Session 1.1 — Sycophancy Check & Adversarial Critique")
    parser.add_argument("--question", required=True, help="Research question or hypothesis to analyse")
    parser.add_argument("--provider", default="gemini", choices=["gemini", "groq", "openai", "claude"])
    parser.add_argument("--model", default=None, help="Override the default model for the provider")
    parser.add_argument("--output", default=None, help="Optional output file path (.txt)")
    args = parser.parse_args()

    results = run(args.question, args.provider, args.model)

    if args.output:
        with open(args.output, "w") as f:
            f.write(f"SESSION 1.1 — SYCOPHANCY CHECK & ADVERSARIAL CRITIQUE\n")
            f.write(f"Provider : {results['provider']}\n")
            f.write(f"Timestamp: {results['timestamp']}\n")
            f.write(f"Question : {results['question']}\n\n")
            f.write("── SYCOPHANCY CHECK ──\n")
            f.write(results["sycophancy_check"] + "\n\n")
            f.write("── ADVERSARIAL CRITIQUE ──\n")
            f.write(results["adversarial_critique"] + "\n")
        print(f"\nReport saved to: {args.output}")


if __name__ == "__main__":
    main()

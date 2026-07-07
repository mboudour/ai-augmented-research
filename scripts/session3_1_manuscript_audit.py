"""
session3_1_manuscript_audit.py
Session 3.1 — Authorship, Integrity, and the Limits of AI Assistance

Runs a citation audit and adversarial critique on a manuscript passage or abstract.
Accepts text input directly or from a .txt file.

Usage:
    python session3_1_manuscript_audit.py \
        --text "Remote work has become a defining feature..." \
        --provider gemini \
        --output report_session3_1.txt

    python session3_1_manuscript_audit.py \
        --file abstract.txt \
        --provider gemini

Environment variables:
    GEMINI_API_KEY, GROQ_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY
"""

import argparse
import datetime
from llm_client import call_llm, get_client_info

CITATION_AUDIT_SYSTEM = (
    "You are a rigorous citation auditor for academic manuscripts. "
    "Review the passage provided and: "
    "(1) List every citation mentioned (author, year). "
    "(2) For each citation, identify the specific empirical claim it is used to support. "
    "(3) Flag any claims that appear to go beyond what a typical paper of that type would support. "
    "(4) Identify any factual claims made without citation that require one. "
    "Be specific. Do not verify the citations yourself — identify what needs verification."
)

ADVERSARIAL_SYSTEM = (
    "You are a rigorous academic peer reviewer conducting an adversarial critique. "
    "Review the passage provided and identify: "
    "(1) Any overstatements or claims stronger than the evidence supports. "
    "(2) Any important contradictory evidence or alternative interpretations that are omitted. "
    "(3) Any unsupported inferences — conclusions that do not follow from the cited evidence. "
    "(4) Any methodological concerns implied by the claims. "
    "Be specific and direct. Your goal is to identify every weakness in the passage."
)

AUTHORSHIP_SYSTEM = (
    "You are a research integrity advisor. Review the following manuscript passage and: "
    "(1) Identify any arguments, interpretations, or conclusions that appear to be "
    "    generated rather than summarized — i.e., that go beyond what the cited sources "
    "    would directly support and represent novel intellectual contributions. "
    "(2) For each such element, state whether it is the kind of contribution that must "
    "    originate with the human researcher (a judgement task) or could be appropriately "
    "    AI-assisted (a labour task). "
    "(3) Identify any elements where the authorship boundary is unclear. "
    "(Zyphur 2026: The authorship boundary — the researcher must be able to independently "
    "produce and defend every claim in the manuscript.)"
)


def run(text: str, provider: str, model: str = None) -> dict:
    info = get_client_info(provider, model)
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")

    print(f"\n{'='*70}")
    print("SESSION 3.1 — MANUSCRIPT AUDIT")
    print(f"{'='*70}")
    print(f"Provider : {info}")
    print(f"Timestamp: {timestamp}")
    print(f"{'='*70}\n")
    print(f"Passage ({len(text)} chars):\n{text[:300]}{'...' if len(text) > 300 else ''}\n")

    print("── STEP 1: CITATION AUDIT ────────────────────────────────────────────")
    citation_audit = call_llm(CITATION_AUDIT_SYSTEM, f"Manuscript passage:\n\n{text}", provider=provider, model=model)
    print(citation_audit)

    print("\n── STEP 2: ADVERSARIAL CRITIQUE ──────────────────────────────────────")
    adversarial = call_llm(ADVERSARIAL_SYSTEM, f"Manuscript passage:\n\n{text}", provider=provider, model=model)
    print(adversarial)

    print("\n── STEP 3: AUTHORSHIP BOUNDARY CHECK ────────────────────────────────")
    authorship = call_llm(AUTHORSHIP_SYSTEM, f"Manuscript passage:\n\n{text}", provider=provider, model=model)
    print(authorship)

    print("\n── VERIFICATION PROTOCOL REMINDER ───────────────────────────────────")
    print(
        "Three-step citation verification for each flagged citation:\n"
        "  Step 1: Confirm the paper exists (search DOI or title)\n"
        "  Step 2: Confirm the abstract matches the summary\n"
        "  Step 3: Confirm the specific claim is present in the paper body\n"
        "Record the failure-discovery rate: how many citations required correction?\n"
        "(Zyphur 2026, Competency 1: Citation Verification)"
    )

    return {
        "text": text,
        "provider": info,
        "timestamp": timestamp,
        "citation_audit": citation_audit,
        "adversarial_critique": adversarial,
        "authorship_check": authorship,
    }


def main():
    parser = argparse.ArgumentParser(description="Session 3.1 — Manuscript Audit")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text", help="Manuscript passage as a string")
    group.add_argument("--file", help="Path to a .txt file containing the manuscript passage")
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
            f.write(f"SESSION 3.1 — MANUSCRIPT AUDIT\n")
            f.write(f"Provider : {results['provider']}\nTimestamp: {results['timestamp']}\n\n")
            f.write("── CITATION AUDIT ──\n" + results["citation_audit"] + "\n\n")
            f.write("── ADVERSARIAL CRITIQUE ──\n" + results["adversarial_critique"] + "\n\n")
            f.write("── AUTHORSHIP BOUNDARY CHECK ──\n" + results["authorship_check"] + "\n")
        print(f"\nReport saved to: {args.output}")


if __name__ == "__main__":
    main()

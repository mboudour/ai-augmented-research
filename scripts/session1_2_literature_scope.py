"""
session1_2_literature_scope.py
Session 1.2 — Literature Discovery, Synthesis, and Research Design

Queries the Semantic Scholar API for papers related to a research question,
then uses an LLM to synthesize the results and flag citations for verification.

Usage:
    python session1_2_literature_scope.py \
        --question "How does remote work affect organizational commitment?" \
        --limit 10 \
        --provider gemini \
        --output report_session1_2.txt

Environment variables:
    GEMINI_API_KEY, GROQ_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY
    S2_API_KEY (optional — Semantic Scholar API key for higher rate limits)
"""

import argparse
import datetime
import json
import requests
from llm_client import call_llm, get_client_info

SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

SYNTHESIS_SYSTEM = (
    "You are a rigorous academic research assistant performing a literature scoping exercise. "
    "You will be given a list of paper titles and abstracts retrieved from Semantic Scholar. "
    "Your tasks: "
    "(1) Identify the 3–5 most relevant papers for the research question. "
    "(2) Summarize the main findings of those papers in 2–3 sentences each. "
    "(3) Identify any major gaps or contradictions in the literature. "
    "(4) Suggest 2–3 follow-up search terms that would extend the scope. "
    "Be specific. Do not fabricate citations — work only from the papers provided."
)

VERIFICATION_SYSTEM = (
    "You are a citation auditor. You will be given a synthesis of academic papers. "
    "For each claim in the synthesis, identify: "
    "(1) Which paper it is attributed to. "
    "(2) Whether the claim is a direct summary of the abstract provided, an inference, or unsupported. "
    "Flag any claims that go beyond what the provided abstracts support."
)


def search_semantic_scholar(query: str, limit: int = 10, api_key: str = None) -> list:
    headers = {}
    if api_key:
        headers["x-api-key"] = api_key
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,abstract,externalIds",
    }
    resp = requests.get(SEMANTIC_SCHOLAR_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return data.get("data", [])


def format_papers(papers: list) -> str:
    lines = []
    for i, p in enumerate(papers, 1):
        authors = ", ".join(a["name"] for a in p.get("authors", [])[:3])
        if len(p.get("authors", [])) > 3:
            authors += " et al."
        year = p.get("year", "n.d.")
        title = p.get("title", "Untitled")
        abstract = p.get("abstract") or "No abstract available."
        lines.append(f"[{i}] {authors} ({year}). {title}\nAbstract: {abstract[:400]}...")
    return "\n\n".join(lines)


def run(question: str, limit: int, provider: str, model: str = None, s2_key: str = None) -> dict:
    info = get_client_info(provider, model)
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")

    print(f"\n{'='*70}")
    print("SESSION 1.2 — LITERATURE SCOPING & SYNTHESIS")
    print(f"{'='*70}")
    print(f"Provider : {info}")
    print(f"Timestamp: {timestamp}")
    print(f"Question : {question}")
    print(f"{'='*70}\n")

    print("── STEP 1: SEMANTIC SCHOLAR SEARCH ──────────────────────────────────")
    papers = search_semantic_scholar(question, limit=limit, api_key=s2_key)
    print(f"Retrieved {len(papers)} papers.\n")
    papers_text = format_papers(papers)
    print(papers_text[:1000] + "...\n[truncated for display — full list passed to LLM]\n")

    print("── STEP 2: AI SYNTHESIS ──────────────────────────────────────────────")
    user_prompt = f"Research question: {question}\n\nPapers retrieved:\n\n{papers_text}"
    synthesis = call_llm(SYNTHESIS_SYSTEM, user_prompt, provider=provider, model=model)
    print(synthesis)

    print("\n── STEP 3: CITATION VERIFICATION AUDIT ──────────────────────────────")
    audit = call_llm(VERIFICATION_SYSTEM, f"Synthesis:\n\n{synthesis}\n\nSource papers:\n\n{papers_text}", provider=provider, model=model)
    print(audit)

    print("\n── VERIFICATION REMINDER ─────────────────────────────────────────────")
    print(
        "Every citation in the synthesis must be verified against the primary source:\n"
        "  Step 1: Confirm the paper exists (DOI or title search)\n"
        "  Step 2: Confirm the abstract matches the summary\n"
        "  Step 3: Confirm the specific claim is present in the paper\n"
        "(Zyphur 2026, Competency 1: Citation Verification)"
    )

    return {
        "question": question,
        "provider": info,
        "timestamp": timestamp,
        "papers": papers,
        "synthesis": synthesis,
        "citation_audit": audit,
    }


def main():
    parser = argparse.ArgumentParser(description="Session 1.2 — Literature Scoping & Synthesis")
    parser.add_argument("--question", required=True, help="Research question for literature scoping")
    parser.add_argument("--limit", type=int, default=10, help="Number of papers to retrieve (default: 10)")
    parser.add_argument("--provider", default="gemini", choices=["gemini", "groq", "openai", "claude"])
    parser.add_argument("--model", default=None)
    parser.add_argument("--s2-key", default=None, help="Optional Semantic Scholar API key")
    parser.add_argument("--output", default=None, help="Optional output file path (.txt)")
    args = parser.parse_args()

    results = run(args.question, args.limit, args.provider, args.model, args.s2_key)

    if args.output:
        with open(args.output, "w") as f:
            f.write(f"SESSION 1.2 — LITERATURE SCOPING & SYNTHESIS\n")
            f.write(f"Provider : {results['provider']}\n")
            f.write(f"Timestamp: {results['timestamp']}\n")
            f.write(f"Question : {results['question']}\n\n")
            f.write("── SYNTHESIS ──\n")
            f.write(results["synthesis"] + "\n\n")
            f.write("── CITATION AUDIT ──\n")
            f.write(results["citation_audit"] + "\n\n")
            f.write("── RAW PAPER DATA (JSON) ──\n")
            f.write(json.dumps(results["papers"], indent=2))
        print(f"\nReport saved to: {args.output}")


if __name__ == "__main__":
    main()

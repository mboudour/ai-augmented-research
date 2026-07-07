"""
session2_1_data_quality_audit.py
Session 2.1 — Validity Reasoning in AI-Mediated Data Work

Loads a CSV or Excel file, computes a data quality profile, and uses an LLM
to audit the cleaning assumptions and flag methodological risks.

Usage:
    python session2_1_data_quality_audit.py \
        --file data.csv \
        --provider gemini \
        --output report_session2_1.txt

Environment variables:
    GEMINI_API_KEY, GROQ_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY
"""

import argparse
import datetime
import io
import pandas as pd
from llm_client import call_llm, get_client_info

AUDIT_SYSTEM = (
    "You are a rigorous data quality auditor for academic research. "
    "You will be given a summary profile of a dataset. Your tasks: "
    "(1) Identify the top 5 data quality issues (missing values, outliers, type mismatches, "
    "    encoding problems, implausible values). "
    "(2) For each issue, state the methodological assumption that would be made if the issue "
    "    is ignored (e.g., 'missing at random', 'outlier is measurement error'). "
    "(3) Recommend a specific remediation step for each issue. "
    "(4) Flag any columns where the data type or value range suggests a potential "
    "    measurement validity problem. "
    "Be specific. Reference column names from the profile."
)

REPRODUCIBILITY_SYSTEM = (
    "You are a computational reproducibility advisor for academic research. "
    "You will be given a data quality audit. Your tasks: "
    "(1) List the decisions made during data cleaning that must be documented for reproducibility. "
    "(2) For each decision, write a one-sentence entry for the methods section of a paper "
    "    that describes the decision and its justification. "
    "(3) Identify any decisions that require a sensitivity analysis "
    "    (i.e., the results may change depending on the choice made). "
    "(Zyphur 2026, Competency 2: Model and Parameter Specification)"
)


def profile_dataframe(df: pd.DataFrame) -> str:
    buf = io.StringIO()
    buf.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n\n")
    buf.write("Column summary:\n")
    for col in df.columns:
        dtype = str(df[col].dtype)
        n_missing = int(df[col].isna().sum())
        pct_missing = round(100 * n_missing / len(df), 1)
        n_unique = int(df[col].nunique())
        if pd.api.types.is_numeric_dtype(df[col]):
            desc = df[col].describe()
            buf.write(
                f"  {col} [{dtype}]: missing={n_missing} ({pct_missing}%), "
                f"unique={n_unique}, min={desc['min']:.3g}, max={desc['max']:.3g}, "
                f"mean={desc['mean']:.3g}, std={desc['std']:.3g}\n"
            )
        else:
            top_vals = df[col].value_counts().head(3).to_dict()
            buf.write(
                f"  {col} [{dtype}]: missing={n_missing} ({pct_missing}%), "
                f"unique={n_unique}, top_values={top_vals}\n"
            )
    return buf.getvalue()


def run(filepath: str, provider: str, model: str = None) -> dict:
    info = get_client_info(provider, model)
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")

    print(f"\n{'='*70}")
    print("SESSION 2.1 — DATA QUALITY AUDIT")
    print(f"{'='*70}")
    print(f"Provider : {info}")
    print(f"Timestamp: {timestamp}")
    print(f"File     : {filepath}")
    print(f"{'='*70}\n")

    # Load data
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)
    print(f"Loaded: {df.shape[0]} rows × {df.shape[1]} columns\n")

    print("── STEP 1: DATA PROFILE ──────────────────────────────────────────────")
    profile = profile_dataframe(df)
    print(profile)

    print("── STEP 2: AI DATA QUALITY AUDIT ────────────────────────────────────")
    audit = call_llm(AUDIT_SYSTEM, f"Dataset profile:\n\n{profile}", provider=provider, model=model)
    print(audit)

    print("\n── STEP 3: REPRODUCIBILITY DOCUMENTATION ────────────────────────────")
    repro = call_llm(REPRODUCIBILITY_SYSTEM, f"Data quality audit:\n\n{audit}", provider=provider, model=model)
    print(repro)

    print("\n── VERIFICATION REMINDER ─────────────────────────────────────────────")
    print(
        "Review each flagged issue against the original data collection protocol.\n"
        "AI-identified issues are hypotheses, not diagnoses. Each must be confirmed\n"
        "by inspecting the raw data and the data collection documentation.\n"
        "(Zyphur 2026, Competency 5: Sycophancy Detection and Human-as-Verifier Discipline)"
    )

    return {
        "file": filepath,
        "provider": info,
        "timestamp": timestamp,
        "profile": profile,
        "audit": audit,
        "reproducibility": repro,
    }


def main():
    parser = argparse.ArgumentParser(description="Session 2.1 — Data Quality Audit")
    parser.add_argument("--file", required=True, help="Path to CSV or Excel file")
    parser.add_argument("--provider", default="gemini", choices=["gemini", "groq", "openai", "claude"])
    parser.add_argument("--model", default=None)
    parser.add_argument("--output", default=None, help="Optional output file path (.txt)")
    args = parser.parse_args()

    results = run(args.file, args.provider, args.model)

    if args.output:
        with open(args.output, "w") as f:
            f.write(f"SESSION 2.1 — DATA QUALITY AUDIT\n")
            f.write(f"Provider : {results['provider']}\n")
            f.write(f"Timestamp: {results['timestamp']}\n")
            f.write(f"File     : {results['file']}\n\n")
            f.write("── DATA PROFILE ──\n")
            f.write(results["profile"] + "\n\n")
            f.write("── AI AUDIT ──\n")
            f.write(results["audit"] + "\n\n")
            f.write("── REPRODUCIBILITY DOCUMENTATION ──\n")
            f.write(results["reproducibility"] + "\n")
        print(f"\nReport saved to: {args.output}")


if __name__ == "__main__":
    main()

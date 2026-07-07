"""
session2_2_end_to_end_pipeline.py
Session 2.2 — From Research Question to Verified Finding (End-to-End Case Study)

Runs the full pipeline on a CSV/Excel dataset:
  1. Summary statistics
  2. AI cleaning audit
  3. Exploratory visualization (saved as PNG)
  4. AI-generated interpretation
  5. Adversarial verification of the interpretation

Usage:
    python session2_2_end_to_end_pipeline.py \
        --file data.csv \
        --question "What is the relationship between X and Y?" \
        --provider gemini \
        --output-dir ./pipeline_output

Environment variables:
    GEMINI_API_KEY, GROQ_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY
"""

import argparse
import datetime
import os
import io
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from llm_client import call_llm, get_client_info

INTERPRETATION_SYSTEM = (
    "You are a rigorous academic data analyst. You will be given summary statistics "
    "and a description of a dataset. Your tasks: "
    "(1) Identify the 3 most substantively interesting patterns in the data. "
    "(2) For each pattern, state what it suggests about the research question. "
    "(3) For each pattern, state what alternative explanations exist that the data alone "
    "    cannot rule out. "
    "(4) Recommend the next analytical step for each pattern. "
    "Be specific. Do not overstate what descriptive statistics can establish."
)

VERIFICATION_SYSTEM = (
    "You are a rigorous peer reviewer. You will be given an AI-generated interpretation "
    "of a dataset. Your tasks: "
    "(1) Identify every causal claim or overstatement in the interpretation. "
    "(2) For each claim, state whether it is supported by descriptive statistics alone "
    "    or requires additional analysis. "
    "(3) Identify any alternative explanations that were not considered. "
    "(4) Rate the overall interpretive validity on a scale of 1–5 and justify the rating."
)


def profile_dataframe(df: pd.DataFrame) -> str:
    buf = io.StringIO()
    buf.write(f"Shape: {df.shape[0]} rows × {df.shape[1]} columns\n\n")
    for col in df.columns:
        dtype = str(df[col].dtype)
        n_missing = int(df[col].isna().sum())
        n_unique = int(df[col].nunique())
        if pd.api.types.is_numeric_dtype(df[col]):
            desc = df[col].describe()
            buf.write(
                f"  {col} [{dtype}]: missing={n_missing}, unique={n_unique}, "
                f"min={desc['min']:.3g}, max={desc['max']:.3g}, "
                f"mean={desc['mean']:.3g}, std={desc['std']:.3g}\n"
            )
        else:
            top_vals = df[col].value_counts().head(3).to_dict()
            buf.write(f"  {col} [{dtype}]: missing={n_missing}, unique={n_unique}, top={top_vals}\n")
    return buf.getvalue()


def make_visualizations(df: pd.DataFrame, output_dir: str) -> list:
    saved = []
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) >= 1:
        fig, axes = plt.subplots(1, min(len(numeric_cols), 4), figsize=(4 * min(len(numeric_cols), 4), 4))
        if len(numeric_cols) == 1:
            axes = [axes]
        for ax, col in zip(axes, numeric_cols[:4]):
            df[col].dropna().hist(ax=ax, bins=20, color="#4E2A84", edgecolor="white")
            ax.set_title(col, fontsize=10)
            ax.set_xlabel("")
        plt.suptitle("Variable Distributions", fontsize=12, fontweight="bold")
        plt.tight_layout()
        path = os.path.join(output_dir, "distributions.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        saved.append(path)
        print(f"  Saved: {path}")

    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        fig, ax = plt.subplots(figsize=(max(6, len(numeric_cols)), max(5, len(numeric_cols) - 1)))
        im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.columns)))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=9)
        ax.set_yticklabels(corr.columns, fontsize=9)
        for i in range(len(corr)):
            for j in range(len(corr.columns)):
                ax.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center", fontsize=8)
        plt.colorbar(im, ax=ax)
        ax.set_title("Correlation Matrix", fontsize=12, fontweight="bold")
        plt.tight_layout()
        path = os.path.join(output_dir, "correlation_matrix.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        plt.close()
        saved.append(path)
        print(f"  Saved: {path}")

    return saved


def run(filepath: str, question: str, provider: str, model: str, output_dir: str) -> dict:
    os.makedirs(output_dir, exist_ok=True)
    info = get_client_info(provider, model)
    timestamp = datetime.datetime.now().isoformat(timespec="seconds")

    print(f"\n{'='*70}")
    print("SESSION 2.2 — END-TO-END RESEARCH PIPELINE")
    print(f"{'='*70}")
    print(f"Provider : {info}")
    print(f"Timestamp: {timestamp}")
    print(f"File     : {filepath}")
    print(f"Question : {question}")
    print(f"{'='*70}\n")

    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)
    print(f"Loaded: {df.shape[0]} rows × {df.shape[1]} columns\n")

    print("── STEP 1: SUMMARY STATISTICS ────────────────────────────────────────")
    profile = profile_dataframe(df)
    print(profile)

    print("── STEP 2: AI CLEANING AUDIT ─────────────────────────────────────────")
    cleaning_audit = call_llm(
        "You are a data quality auditor. Identify the top 3 data quality issues in this "
        "dataset profile and recommend a specific remediation for each.",
        f"Dataset profile:\n\n{profile}",
        provider=provider, model=model
    )
    print(cleaning_audit)

    print("\n── STEP 3: EXPLORATORY VISUALIZATIONS ───────────────────────────────")
    viz_paths = make_visualizations(df, output_dir)

    print("\n── STEP 4: AI INTERPRETATION ─────────────────────────────────────────")
    interp_prompt = (
        f"Research question: {question}\n\n"
        f"Dataset profile:\n{profile}\n\n"
        f"Cleaning issues identified:\n{cleaning_audit}"
    )
    interpretation = call_llm(INTERPRETATION_SYSTEM, interp_prompt, provider=provider, model=model)
    print(interpretation)

    print("\n── STEP 5: ADVERSARIAL VERIFICATION ─────────────────────────────────")
    verification = call_llm(VERIFICATION_SYSTEM, f"Interpretation:\n\n{interpretation}", provider=provider, model=model)
    print(verification)

    print("\n── VERIFICATION REMINDER ─────────────────────────────────────────────")
    print(
        "The interpretation is AI-generated from descriptive statistics only.\n"
        "No causal claims are warranted without appropriate inferential analysis.\n"
        "Record the failure-discovery rate: how many claims required revision?\n"
        "(Zyphur 2026, Competency 6: Structured Failure-Mode Reporting)"
    )

    report_path = os.path.join(output_dir, "pipeline_report.txt")
    with open(report_path, "w") as f:
        f.write(f"SESSION 2.2 — END-TO-END PIPELINE REPORT\n")
        f.write(f"Provider : {info}\nTimestamp: {timestamp}\n")
        f.write(f"File: {filepath}\nQuestion: {question}\n\n")
        f.write("── DATA PROFILE ──\n" + profile + "\n\n")
        f.write("── CLEANING AUDIT ──\n" + cleaning_audit + "\n\n")
        f.write("── INTERPRETATION ──\n" + interpretation + "\n\n")
        f.write("── ADVERSARIAL VERIFICATION ──\n" + verification + "\n")
    print(f"\nFull report saved to: {report_path}")

    return {
        "profile": profile, "cleaning_audit": cleaning_audit,
        "interpretation": interpretation, "verification": verification,
        "visualizations": viz_paths, "report": report_path,
    }


def main():
    parser = argparse.ArgumentParser(description="Session 2.2 — End-to-End Research Pipeline")
    parser.add_argument("--file", required=True, help="Path to CSV or Excel file")
    parser.add_argument("--question", required=True, help="Research question")
    parser.add_argument("--provider", default="gemini", choices=["gemini", "groq", "openai", "claude"])
    parser.add_argument("--model", default=None)
    parser.add_argument("--output-dir", default="./pipeline_output", help="Directory for output files")
    args = parser.parse_args()
    run(args.file, args.question, args.provider, args.model, args.output_dir)


if __name__ == "__main__":
    main()

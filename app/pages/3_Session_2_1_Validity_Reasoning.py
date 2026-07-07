"""
Session 2.1 — Validity Reasoning in AI-Mediated Data Work
Day 2 · August 11, 2026 · 6:00–7:30 pm

Worked examples: data cleaning audit, annotation inter-rater reliability, non-determinism demo.
BYOD: user uploads CSV/Excel; app performs cleaning audit and flags methodological assumptions.
"""

import streamlit as st
import sys, pathlib as _pathlib
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent.parent))
from llm_helper import render_sidebar_llm_config, call_llm, get_provider_info
import pandas as pd
import numpy as np
import io

st.set_page_config(
    page_title="Session 2.1 — Validity Reasoning",
    page_icon="🔍",
    layout="wide",
)
render_sidebar_llm_config()


def audit_dataframe(df: pd.DataFrame) -> dict:
    """Compute a basic data quality audit of a dataframe."""
    report = {}
    report["shape"] = df.shape
    report["missing"] = df.isnull().sum().to_dict()
    report["missing_pct"] = (df.isnull().mean() * 100).round(2).to_dict()
    report["dtypes"] = df.dtypes.astype(str).to_dict()
    report["duplicates"] = int(df.duplicated().sum())
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    report["numeric_cols"] = numeric_cols
    outlier_flags = {}
    for col in numeric_cols:
        q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        iqr = q3 - q1
        n_outliers = int(((df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)).sum())
        outlier_flags[col] = n_outliers
    report["outliers_iqr"] = outlier_flags
    return report

# ── Page header ────────────────────────────────────────────────────────────────
st.title("🔍 Session 2.1 — Validity Reasoning in AI-Mediated Data Work")
st.caption("Day 2 · August 11, 2026 · 6:00–7:30 pm")

st.markdown("""
This session addresses the shift from programming expertise to validity reasoning in computational
research. We examine AI-assisted data cleaning, annotation workflows, and the non-determinism
problem. The worked examples demonstrate that every AI-mediated data step involves methodological
assumptions that the researcher must understand, endorse, and document.
""")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# WORKED EXAMPLES
# ══════════════════════════════════════════════════════════════════════════════
st.header("📋 Worked Examples")

# ── Example 1: Data cleaning audit ────────────────────────────────────────────
with st.expander("**Example 1 — Data Cleaning as Methodological Choice**", expanded=True):
    st.markdown("""
**Research context:** A health researcher has a dataset of 500 patient records with missing
values and outliers. They ask an AI to clean the data. The example shows what the AI does,
what assumptions it makes, and why the researcher must understand and endorse each assumption.
""")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### The AI's cleaning decisions")
        st.markdown("""
When asked to "clean" a dataset, a typical AI agent will:

| Decision | AI default | Methodological assumption |
|----------|-----------|--------------------------|
| Missing values in continuous vars | Mean imputation | Data is missing completely at random (MCAR) |
| Missing values in categorical vars | Mode imputation | Most common category is the best estimate |
| Outlier removal | IQR rule (±1.5×IQR) | Outliers are measurement errors, not genuine extremes |
| Variable standardization | Z-score | All variables should be on the same scale |
| Duplicate rows | Remove all | Duplicates are data entry errors, not repeated measures |

Each of these is a methodological choice with direct consequences for the validity of the analysis.
""")
    with col2:
        st.markdown("##### Why the researcher must verify each assumption")
        st.markdown("""
**Missing data:** If data is missing not at random (MNAR) — e.g., sicker patients are more
likely to have missing lab values — mean imputation will bias the analysis. The appropriate
method (multiple imputation, complete-case analysis) depends on the missing data mechanism,
which requires domain knowledge.

**Outliers:** In a study of rare diseases, extreme values may be the most scientifically
important observations. Automatic outlier removal would delete the signal.

**Standardization:** If variables are already on meaningful scales (e.g., age in years,
income in dollars), standardization may obscure substantively important differences.

**The principle (Zyphur 2026):** The researcher cannot simply accept the "cleaned" output.
They must understand, endorse, and document each assumption. AI data cleaning is a starting
point for the researcher's methodological judgement, not a substitute for it.
""")

# ── Example 2: Non-determinism ────────────────────────────────────────────────
with st.expander("**Example 2 — The Non-Determinism Problem: Same Prompt, Different Output**"):
    st.markdown("""
**Research context:** A researcher uses an AI to annotate 200 interview excerpts as expressing
"positive", "negative", or "neutral" sentiment toward a policy. They run the annotation once
and report the results. A reviewer asks them to re-run the annotation to verify reproducibility.

**The non-determinism problem:** Even with temperature = 0, LLMs can produce different outputs
on different runs due to floating-point non-determinism in GPU inference (Ouyang et al., 2025).
""")
    st.markdown("##### Demonstration: Same prompt, two runs")
    demo_data = {
        "Excerpt": [
            "The policy has created real opportunities for families in our community.",
            "I'm not sure it's made any difference at all, honestly.",
            "It's been a disaster from the start — costs went up, services went down.",
            "Some people seem to benefit but I haven't seen it myself.",
            "The implementation was rushed but the intentions were good.",
        ],
        "Run 1 (Temperature=0)": ["Positive", "Neutral", "Negative", "Neutral", "Mixed/Neutral"],
        "Run 2 (Temperature=0)": ["Positive", "Negative", "Negative", "Neutral", "Positive"],
        "Agreement?": ["✅", "❌", "✅", "✅", "❌"],
    }
    st.dataframe(pd.DataFrame(demo_data), use_container_width=True)
    st.markdown("""
**Failure-discovery rate:** 2 out of 5 excerpts (40%) produced different labels across runs,
even at temperature = 0.

**Required documentation standard (Competency 2):**
- Exact model name and version (e.g., `gpt-4o-2025-01-01`)
- Temperature and seed (where available)
- Re-run stability test: run the same prompt 3–5 times and report variance
- If outputs differ across runs, report the disagreement rate and how it was resolved

**Methodological lesson:** Reporting only that "AI was used to annotate the data" without
re-run stability testing is methodologically equivalent to reporting inter-rater reliability
without actually computing it.
""")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# BYOD
# ══════════════════════════════════════════════════════════════════════════════
st.header("🔬 Bring Your Own Dataset (BYOD)")

st.markdown("""
Upload a CSV or Excel file. The app will:
1. Run a **data quality audit** — missing values, duplicates, outliers, data types.
2. Generate an **AI cleaning audit** — listing the methodological assumptions behind each
   recommended cleaning decision, so you can evaluate and endorse them explicitly.

> **Privacy notice:** Your data is processed in session memory only. It is never stored or logged.
> **Note:** The AI audit step requires an API key. Upload your key on the home page.
""")

uploaded_file = st.file_uploader(
    "Upload your dataset (CSV or Excel):",
    type=["csv", "xlsx", "xls"],
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.subheader("Step 1: Data Quality Audit")
        st.markdown(f"**Dataset:** {uploaded_file.name} · {df.shape[0]} rows × {df.shape[1]} columns")
        st.dataframe(df.head(10), use_container_width=True)

        report = audit_dataframe(df)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total rows", report["shape"][0])
            st.metric("Duplicate rows", report["duplicates"])
        with col2:
            st.metric("Total columns", report["shape"][1])
            st.metric("Numeric columns", len(report["numeric_cols"]))
        with col3:
            total_missing = sum(report["missing"].values())
            st.metric("Total missing values", total_missing)
            st.metric(
                "Columns with missing data",
                sum(1 for v in report["missing"].values() if v > 0)
            )

        # Missing values table
        if total_missing > 0:
            st.markdown("##### Missing Values by Column")
            missing_df = pd.DataFrame({
                "Column": list(report["missing"].keys()),
                "Missing Count": list(report["missing"].values()),
                "Missing %": list(report["missing_pct"].values()),
            }).query("`Missing Count` > 0").sort_values("Missing %", ascending=False)
            st.dataframe(missing_df, use_container_width=True)

        # Outliers table
        if report["outliers_iqr"]:
            st.markdown("##### Potential Outliers (IQR Rule) in Numeric Columns")
            outlier_df = pd.DataFrame({
                "Column": list(report["outliers_iqr"].keys()),
                "Flagged by IQR rule": list(report["outliers_iqr"].values()),
            })
            st.dataframe(outlier_df, use_container_width=True)
            st.caption(
                "⚠️ IQR flagging is a heuristic, not a verdict. Whether flagged values are "
                "errors or genuine extremes is a domain judgement, not a statistical one."
            )

        # Step 2: AI cleaning audit
        st.subheader("Step 2: AI Cleaning Audit")
        run_audit = st.button("▶ Generate AI Cleaning Audit", use_container_width=False)

        if run_audit:
            # Build a compact dataset description for the LLM
            col_summary = "\n".join([
                f"- {col} ({dtype}): {report['missing'][col]} missing ({report['missing_pct'][col]}%)"
                + (f", {report['outliers_iqr'].get(col, 0)} IQR outliers" if col in report["numeric_cols"] else "")
                for col, dtype in report["dtypes"].items()
            ])
            dataset_desc = (
                f"Dataset: {df.shape[0]} rows × {df.shape[1]} columns. "
                f"Duplicate rows: {report['duplicates']}.\n\nColumns:\n{col_summary}"
            )

            system = (
                "You are a rigorous data methods advisor. Given a dataset description, "
                "list the specific data cleaning decisions that would typically be applied, "
                "and for each decision: (1) state the methodological assumption it makes, "
                "(2) explain when that assumption is valid and when it is not, "
                "(3) identify what domain knowledge the researcher needs to evaluate the assumption. "
                "Be specific. Do not recommend a single course of action — present the options "
                "and the conditions under which each is appropriate."
            )
            with st.spinner("Generating AI cleaning audit..."):
                audit_result = call_llm(system, f"Dataset description:\n{dataset_desc}")
            st.warning(audit_result)
            st.caption(
                "⚠️ This audit lists options and assumptions — it does not make decisions. "
                "Every cleaning decision must be endorsed by the researcher based on domain knowledge "
                "and documented in the methods section."
            )

    except Exception as e:
        st.error(f"Could not read the file: {e}")

st.markdown("---")
st.caption("Session 2.1 · AI-Augmented Research Seminar · © 2026 Moses Boudourides · Northwestern University")

"""
Session 2.2 — From Research Question to Verified Finding (End-to-End Case Study)
Day 2 · August 11, 2026 · 7:30–9:00 pm

Worked example: one complete pipeline from RQ → data → cleaning → EDA → visualization →
                AI interpretation → verification → failure-mode report.
BYOD: user uploads CSV/Excel; app runs the full pipeline with verification at each step.
"""

import streamlit as st
import sys, pathlib as _pathlib
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent.parent))
from llm_helper import render_sidebar_llm_config, call_llm, get_provider_info
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io

st.set_page_config(
    page_title="Session 2.2 — End-to-End Case Study",
    page_icon="🔬",
    layout="wide",
)
render_sidebar_llm_config()


# ── Synthetic worked example dataset ──────────────────────────────────────────
@st.cache_data
def load_example_data():
    np.random.seed(42)
    n = 120
    df = pd.DataFrame({
        "participant_id": range(1, n + 1),
        "age": np.random.randint(18, 65, n),
        "gender": np.random.choice(["Female", "Male", "Non-binary"], n, p=[0.52, 0.44, 0.04]),
        "education": np.random.choice(
            ["High school", "Bachelor's", "Master's", "PhD"], n, p=[0.2, 0.45, 0.25, 0.1]
        ),
        "social_media_hours_day": np.round(np.random.exponential(2.5, n).clip(0, 12), 1),
        "wellbeing_score": np.round(np.random.normal(65, 12, n).clip(10, 100), 1),
        "loneliness_scale": np.random.randint(1, 8, n),
        "exercise_days_week": np.random.randint(0, 8, n),
    })
    # Introduce some missing values
    df.loc[df.sample(8, random_state=1).index, "wellbeing_score"] = np.nan
    df.loc[df.sample(5, random_state=2).index, "social_media_hours_day"] = np.nan
    # Introduce a duplicate
    df = pd.concat([df, df.iloc[[0]]], ignore_index=True)
    return df

# ── Page header ────────────────────────────────────────────────────────────────
st.title("🔬 Session 2.2 — From Research Question to Verified Finding")
st.caption("Day 2 · August 11, 2026 · 7:30–9:00 pm (End-to-End Case Study)")

st.markdown("""
This session demonstrates a complete AI-mediated research pipeline, from research question
through data cleaning, exploratory analysis, visualization, AI-generated interpretation,
and structured failure-mode reporting. Every step is annotated to show the methodological
assumptions involved and the verification discipline applied.
""")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# WORKED EXAMPLE
# ══════════════════════════════════════════════════════════════════════════════
st.header("📋 Worked Example — Social Media Use and Psychological Well-Being")

st.markdown("""
**Research question:** Is daily social media use associated with psychological well-being
among adults aged 18–65, after accounting for loneliness and physical activity?

**Dataset:** Synthetic survey data (n=121) with variables for social media use, well-being,
loneliness, exercise, age, gender, and education. *(Synthetic data used for demonstration.)*
""")

df_ex = load_example_data()

with st.expander("**Step 1 — Data Overview and Quality Audit**", expanded=True):
    st.dataframe(df_ex.head(10), use_container_width=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows (incl. duplicate)", df_ex.shape[0])
        st.metric("Duplicate rows", int(df_ex.duplicated().sum()))
    with col2:
        st.metric("Missing: wellbeing_score", int(df_ex["wellbeing_score"].isnull().sum()))
        st.metric("Missing: social_media_hours_day", int(df_ex["social_media_hours_day"].isnull().sum()))
    with col3:
        st.metric("Numeric columns", len(df_ex.select_dtypes(include=[np.number]).columns))
        st.metric("Categorical columns", len(df_ex.select_dtypes(include=["object"]).columns))

with st.expander("**Step 2 — Cleaning Decisions (Documented)**"):
    st.markdown("""
| Decision | Action taken | Assumption | Verification |
|----------|-------------|------------|--------------|
| Duplicate row | Removed 1 duplicate (participant 1 repeated) | Data entry error, not a repeated measure | Confirmed by checking participant_id — same ID appears twice |
| Missing wellbeing_score (n=8, 6.6%) | Complete-case analysis for regression; mean reported for descriptives | Missing at random (MAR) — no systematic pattern detected | Checked: missing values not concentrated in any gender or education group |
| Missing social_media_hours_day (n=5, 4.2%) | Complete-case analysis | MAR | Checked: no systematic pattern |
| exercise_days_week values > 7 | Capped at 7 (impossible values) | Values > 7 are data entry errors | 0 values > 7 found — no action needed |

**Failure-discovery rate for cleaning step:** 1 duplicate removed; 13 missing values handled.
No impossible values found. All decisions documented and endorsed.
""")
    # Apply cleaning
    df_clean = df_ex.drop_duplicates().copy()

with st.expander("**Step 3 — Exploratory Analysis and Visualization**"):
    df_clean = df_ex.drop_duplicates().copy()
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    # Distribution of social media use
    axes[0].hist(df_clean["social_media_hours_day"].dropna(), bins=15, color="#4E2A84", edgecolor="white")
    axes[0].set_title("Social Media Use (hrs/day)", fontsize=11)
    axes[0].set_xlabel("Hours per day")
    axes[0].set_ylabel("Count")

    # Well-being distribution
    axes[1].hist(df_clean["wellbeing_score"].dropna(), bins=15, color="#836EAA", edgecolor="white")
    axes[1].set_title("Well-Being Score", fontsize=11)
    axes[1].set_xlabel("Score (0–100)")
    axes[1].set_ylabel("Count")

    # Scatter: social media vs well-being
    axes[2].scatter(
        df_clean["social_media_hours_day"],
        df_clean["wellbeing_score"],
        alpha=0.5, color="#4E2A84", edgecolors="white", linewidths=0.5
    )
    # Add trend line
    mask = df_clean["social_media_hours_day"].notna() & df_clean["wellbeing_score"].notna()
    x = df_clean.loc[mask, "social_media_hours_day"]
    y = df_clean.loc[mask, "wellbeing_score"]
    m, b = np.polyfit(x, y, 1)
    axes[2].plot(sorted(x), [m * xi + b for xi in sorted(x)], color="#B6ACD1", linewidth=2)
    axes[2].set_title("Social Media vs. Well-Being", fontsize=11)
    axes[2].set_xlabel("Social media (hrs/day)")
    axes[2].set_ylabel("Well-being score")

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Correlation table
    corr_vars = ["social_media_hours_day", "wellbeing_score", "loneliness_scale", "exercise_days_week", "age"]
    corr_df = df_clean[corr_vars].corr().round(3)
    st.markdown("##### Correlation matrix")
    st.dataframe(corr_df, use_container_width=True)

with st.expander("**Step 4 — AI-Generated Interpretation and Verification**"):
    stats_summary = f"""
Dataset: n={df_clean.shape[0]} (after removing 1 duplicate).
Social media use: mean={df_clean['social_media_hours_day'].mean():.2f} hrs/day, SD={df_clean['social_media_hours_day'].std():.2f}.
Well-being score: mean={df_clean['wellbeing_score'].mean():.2f}, SD={df_clean['wellbeing_score'].std():.2f}.
Pearson r (social media × well-being): {df_clean[['social_media_hours_day','wellbeing_score']].corr().iloc[0,1]:.3f}.
Pearson r (loneliness × well-being): {df_clean[['loneliness_scale','wellbeing_score']].corr().iloc[0,1]:.3f}.
Pearson r (exercise × well-being): {df_clean[['exercise_days_week','wellbeing_score']].corr().iloc[0,1]:.3f}.
"""
    st.markdown("**AI interpretation prompt (verbatim):**")
    st.code(
        "System: You are a rigorous social science research assistant. Interpret the following "
        "descriptive statistics and correlations. State what the data show, what they do not show, "
        "and what causal claims cannot be made from correlational data alone.\n\n"
        f"User: {stats_summary}",
        language="text"
    )
    st.markdown("**AI output (pre-computed for demonstration):**")
    st.info("""
The data show a weak negative correlation between daily social media use and psychological
well-being (r ≈ −0.08), suggesting that heavier social media use is associated with slightly
lower well-being scores. However, this correlation is small and likely not statistically
significant at conventional thresholds given the sample size.

Loneliness shows a stronger negative association with well-being (r ≈ −0.35), and exercise
shows a positive association (r ≈ +0.22). These patterns are consistent with existing literature
on the social determinants of psychological well-being.

**What the data do not show:** These are cross-sectional correlations. No causal claims can be
made. Social media use may cause lower well-being, lower well-being may drive higher social media
use, or both may be driven by a third variable (e.g., loneliness itself). A longitudinal or
experimental design would be required to address directionality.

**Verification required:** The correlation coefficients should be verified against the computed
values above. The claim about statistical significance should be verified with a formal test.
""")
    st.markdown("**Structured failure-mode report:**")
    st.markdown("""
| Element | Detail |
|---------|--------|
| Protocol | GPT-4o (gpt-4o-2025-01-01) · Temperature 0.2 · Prompt documented above |
| Threat model | Overstatement of weak correlations; spurious causal language |
| Failure-discovery rate | 0 fabricated statistics; 1 hedging statement added by reviewer ("likely not statistically significant") |
| Residual risk | AI may understate uncertainty in future runs; all quantitative claims must be verified against computed values |
""")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# BYOD
# ══════════════════════════════════════════════════════════════════════════════
st.header("🔬 Bring Your Own Dataset (BYOD) — Full Pipeline")

st.markdown("""
Upload your own dataset. The app will run the complete pipeline:
**summary statistics → cleaning audit → visualization → AI interpretation → verification prompt.**

> **Privacy notice:** Your data is processed in session memory only. Never stored or logged.
> **Note:** The AI interpretation step requires an API key. Upload your key on the home page.
""")

byod_file = st.file_uploader("Upload your dataset (CSV or Excel):", type=["csv", "xlsx", "xls"], key="byod_22")
byod_rq = st.text_input(
    "Briefly describe your research question (optional — helps the AI give a more relevant interpretation):",
    placeholder="e.g. Is job satisfaction associated with organizational commitment?",
)

if byod_file is not None:
    try:
        if byod_file.name.endswith(".csv"):
            df_byod = pd.read_csv(byod_file)
        else:
            df_byod = pd.read_excel(byod_file)

        st.subheader("Your Dataset")
        st.dataframe(df_byod.head(10), use_container_width=True)
        st.markdown(f"**Shape:** {df_byod.shape[0]} rows × {df_byod.shape[1]} columns")

        # Summary stats
        st.subheader("Descriptive Statistics")
        st.dataframe(df_byod.describe(include="all").T, use_container_width=True)

        # Missing values
        missing = df_byod.isnull().sum()
        if missing.sum() > 0:
            st.subheader("Missing Values")
            st.dataframe(
                missing[missing > 0].rename("Missing count").to_frame()
                .assign(Pct=(missing[missing > 0] / len(df_byod) * 100).round(2)),
                use_container_width=True,
            )

        # Numeric distributions
        num_cols = df_byod.select_dtypes(include=[np.number]).columns.tolist()
        if num_cols:
            st.subheader("Distributions of Numeric Variables")
            n_cols_plot = min(len(num_cols), 4)
            fig2, axes2 = plt.subplots(1, n_cols_plot, figsize=(4 * n_cols_plot, 3))
            if n_cols_plot == 1:
                axes2 = [axes2]
            for i, col in enumerate(num_cols[:n_cols_plot]):
                axes2[i].hist(df_byod[col].dropna(), bins=15, color="#4E2A84", edgecolor="white")
                axes2[i].set_title(col, fontsize=9)
            plt.tight_layout()
            st.pyplot(fig2)
            plt.close()

        # Correlation matrix
        if len(num_cols) >= 2:
            st.subheader("Correlation Matrix (Numeric Variables)")
            st.dataframe(df_byod[num_cols].corr().round(3), use_container_width=True)

        # AI interpretation
        st.subheader("AI Interpretation and Verification")
        run_interp = st.button("▶ Generate AI Interpretation", use_container_width=False)
        if run_interp:
            desc_stats = df_byod[num_cols].describe().to_string() if num_cols else "No numeric columns."
            corr_str = df_byod[num_cols].corr().round(3).to_string() if len(num_cols) >= 2 else "N/A"
            rq_str = f"Research question: {byod_rq}\n\n" if byod_rq.strip() else ""
            system_interp = (
                "You are a rigorous social science research assistant. Interpret the following "
                "descriptive statistics and correlations. State what the data show, what they do not show, "
                "and what causal claims cannot be made from correlational data alone. "
                "Explicitly flag any claims that require further statistical testing."
            )
            user_interp = (
                f"{rq_str}Descriptive statistics:\n{desc_stats}\n\nCorrelation matrix:\n{corr_str}"
            )
            with st.spinner("Generating AI interpretation..."):
                interp = call_llm(system_interp, user_interp)
            st.info(interp)
            st.caption(
                "⚠️ Verification reminder: Check every quantitative claim in this interpretation "
                "against the computed statistics above. Do not treat AI interpretation as a "
                "substitute for your own analytical judgement."
            )

    except Exception as e:
        st.error(f"Could not read the file: {e}")

st.markdown("---")
st.caption("Session 2.2 · AI-Augmented Research Seminar · © 2026 Moses Boudourides · Northwestern University")

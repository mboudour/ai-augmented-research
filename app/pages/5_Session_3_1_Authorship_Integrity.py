"""
Session 3.1 — Authorship, Integrity, and the Limits of AI Assistance
Day 3 · August 12, 2026 · 6:00–7:30 pm

Worked examples: citation audit on AI-assisted abstract, authorship boundary test,
                 adversarial manuscript critique.
BYOD: user pastes abstract or manuscript passage; app runs citation audit + adversarial critique.
"""

import streamlit as st
import sys, pathlib as _pathlib
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent.parent))
from llm_helper import render_sidebar_llm_config, call_llm, get_provider_info

st.set_page_config(
    page_title="Session 3.1 — Authorship & Integrity",
    page_icon="✍️",
    layout="wide",
)
render_sidebar_llm_config()


# ── Page header ────────────────────────────────────────────────────────────────
st.title("✍️ Session 3.1 — Authorship, Integrity, and the Limits of AI Assistance")
st.caption("Day 3 · August 12, 2026 · 6:00–7:30 pm")

st.markdown("""
This session examines the authorship boundary, the citation hallucination problem in scholarly
writing, and the five-step verification protocol for AI-assisted manuscripts. The worked examples
demonstrate the citation audit and the adversarial critique in practice.
""")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# WORKED EXAMPLES
# ══════════════════════════════════════════════════════════════════════════════
st.header("📋 Worked Examples")

with st.expander("**Example 1 — The Authorship Boundary: What AI Can and Cannot Do**", expanded=True):
    st.markdown("""
**The core principle:** The researcher must be able to independently produce and defend every
claim in the manuscript. Using AI to generate novel arguments, fabricate evidence, or substitute
for the researcher's interpretation crosses the authorship boundary.

**The plagiarism frame is a category error (Zyphur 2026):** Most institutional policies frame
AI writing assistance as a plagiarism issue — presenting AI text as one's own. But this misses
the deeper problem. A researcher who uses AI to generate claims they cannot defend has published
*invalid research*, regardless of who "owns" the text.
""")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### ✅ Acceptable AI writing assistance (labour tasks)")
        st.markdown("""
- **Language polishing:** Improving clarity, grammar, and register without changing the meaning
- **Length compression:** Condensing a paragraph to meet a word limit
- **Register conversion:** Making technical prose more accessible (or vice versa)
- **Structural reorganization:** Reordering sentences or paragraphs for flow
- **Format conversion:** Converting a bullet list to prose, or vice versa

In all of these cases, the intellectual content — the argument, the evidence, the interpretation
— originates with the researcher. The AI is improving the presentation, not generating the substance.
""")
    with col2:
        st.markdown("##### ⚠️ Unacceptable AI writing assistance (judgement tasks)")
        st.markdown("""
- **Generating novel arguments** the researcher has not independently reasoned through
- **Fabricating or selecting evidence** to support a conclusion
- **Interpreting findings** in the context of the theoretical literature
- **Writing the discussion section** without the researcher's independent analysis
- **Generating the conclusion** without the researcher's own synthesis

The test: *Can the researcher explain, in their own words, where this claim comes from and
why it is valid?* If not, the AI has substituted for the researcher's intellectual authority.
""")

with st.expander("**Example 2 — Five-Step Manuscript Verification Protocol**"):
    st.markdown("""
**Research context:** A researcher has used AI to assist with drafting the introduction of a
paper on remote work and organizational commitment. The following demonstrates the five-step
verification protocol applied to a representative passage.

**Draft passage (AI-assisted):**
> "Remote work has become a defining feature of contemporary organizational life. Research
> consistently shows that remote workers report higher job satisfaction (Allen et al., 2021)
> and lower organizational commitment (Golden & Veiga, 2005). A meta-analysis by Gajendran
> and Harrison (2007) found that remote work had a small but significant positive effect on
> job performance (d = 0.18) and a negative effect on coworker relationships."
""")
    verification_data = {
        "Step": [
            "1. Citation audit",
            "1. Citation audit",
            "1. Citation audit",
            "2. Factual claim audit",
            "3. Inference audit",
            "4. Consistency check",
            "5. Sycophancy check",
        ],
        "Element checked": [
            "Allen et al. (2021)",
            "Golden & Veiga (2005)",
            "Gajendran & Harrison (2007)",
            "d = 0.18 for job performance",
            "'Research consistently shows...'",
            "Positive satisfaction + negative commitment",
            "Overall framing",
        ],
        "Finding": [
            "✅ Exists; content matches",
            "✅ Exists; content matches",
            "✅ Exists; d = 0.18 confirmed",
            "✅ Matches Gajendran & Harrison Table 3",
            "⚠️ 'Consistently' overstates — literature is mixed",
            "⚠️ Tension not acknowledged in draft",
            "⚠️ AI framing omits null/negative findings on satisfaction",
        ],
        "Action": [
            "No change needed",
            "No change needed",
            "No change needed",
            "No change needed",
            "Replace 'consistently' with 'generally, though not uniformly'",
            "Add sentence acknowledging the tension",
            "Add reference to studies finding no satisfaction effect",
        ],
    }
    import pandas as pd
    st.dataframe(pd.DataFrame(verification_data), use_container_width=True)
    st.markdown("""
**Failure-discovery rate:** 3 out of 7 checked elements (43%) required revision.
None involved fabricated citations, but all three involved overstatement or omission.

**Methodological lesson:** Citation hallucination is not the only risk in AI-assisted writing.
Selective framing, overstatement, and omission of contradictory evidence are equally serious
problems that require the researcher's independent critical assessment.
""")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# BYOD
# ══════════════════════════════════════════════════════════════════════════════
st.header("🔬 Bring Your Own Manuscript Passage (BYOD)")

st.markdown("""
Paste an abstract or manuscript passage below. The app will:
1. Run a **citation audit prompt** — asking the AI to identify all citations and flag any
   that cannot be verified from the passage alone.
2. Run an **adversarial critique** — asking the AI to identify overstatements, omissions,
   and unsupported inferences.

> **Privacy notice:** Your text is processed in session memory only. Never stored or logged.
> **Note:** Requires an API key. Upload your key on the home page.
""")

manuscript_text = st.text_area(
    "Paste your abstract or manuscript passage:",
    height=200,
    placeholder="Paste your text here...",
)

col1, col2 = st.columns(2)
with col1:
    run_citation = st.button("▶ Run Citation Audit", use_container_width=True)
with col2:
    run_critique = st.button("▶ Run Adversarial Critique", use_container_width=True)

if run_citation and manuscript_text.strip():
    with st.spinner("Running citation audit..."):
        system = (
            "You are a rigorous citation auditor for academic manuscripts. "
            "Review the passage provided and: "
            "(1) List every citation mentioned (author, year). "
            "(2) For each citation, identify the specific empirical claim it is used to support. "
            "(3) Flag any claims that appear to go beyond what a typical paper of that type would support. "
            "(4) Identify any factual claims that are made without citation and that require one. "
            "Be specific. Do not verify the citations yourself — your role is to identify what needs verification."
        )
        result = call_llm(system, f"Manuscript passage:\n\n{manuscript_text}")
    st.subheader("Citation Audit Result")
    st.info(result)
    st.caption(
        "⚠️ This audit identifies what to check — it does not verify citations. "
        "You must look up each flagged citation against the primary source yourself. "
        "The three-step protocol: (1) paper exists, (2) abstract matches, (3) specific claim is present."
    )

if run_critique and manuscript_text.strip():
    with st.spinner("Running adversarial critique..."):
        system = (
            "You are a rigorous academic peer reviewer conducting an adversarial critique. "
            "Review the passage provided and identify: "
            "(1) Any overstatements or claims that are stronger than the evidence supports. "
            "(2) Any important contradictory evidence or alternative interpretations that are omitted. "
            "(3) Any unsupported inferences — conclusions that do not follow from the cited evidence. "
            "(4) Any methodological concerns implied by the claims. "
            "Be specific and direct. Your goal is to identify every weakness in the passage."
        )
        result = call_llm(system, f"Manuscript passage:\n\n{manuscript_text}")
    st.subheader("Adversarial Critique Result")
    st.warning(result)
    st.caption(
        "⚠️ Evaluate each critique independently. An AI adversarial critique is a brainstorm "
        "prompt, not a peer review. The researcher's domain expertise must assess which "
        "objections are substantive and which reflect model limitations."
    )

if (run_citation or run_critique) and not manuscript_text.strip():
    st.error("Please paste a manuscript passage before running the analysis.")

st.markdown("---")
st.caption("Session 3.1 · AI-Augmented Research Seminar · © 2026 Moses Boudourides · Northwestern University")

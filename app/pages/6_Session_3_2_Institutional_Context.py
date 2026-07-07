"""
Session 3.2 — Research Judgement in an Institutional Context
Day 3 · August 12, 2026 · 7:30–9:00 pm

Worked examples: AI disclosure statement evaluation, policy comparison table,
                 future directions synthesis.
BYOD: user pastes a draft methods section describing AI use; app evaluates against
      the minimum AI disclosure standard.
"""

import streamlit as st
import sys, pathlib as _pathlib
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent.parent))
from llm_helper import render_sidebar_llm_config, call_llm, get_provider_info
import pandas as pd

st.set_page_config(
    page_title="Session 3.2 — Institutional Context",
    page_icon="🏛️",
    layout="wide",
)
render_sidebar_llm_config()


# ── Page header ────────────────────────────────────────────────────────────────
st.title("🏛️ Session 3.2 — Research Judgement in an Institutional Context")
st.caption("Day 3 · August 12, 2026 · 7:30–9:00 pm")

st.markdown("""
This session examines how universities, journals, and funders are setting the rules for AI use
in research — and how researchers should navigate those rules. We cover the minimum AI disclosure
standard, the current state of publisher policies, and the long-term trajectory of human-AI
collaboration in scientific discovery.
""")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# WORKED EXAMPLES
# ══════════════════════════════════════════════════════════════════════════════
st.header("📋 Worked Examples")

with st.expander("**Example 1 — The Minimum AI Disclosure Standard**", expanded=True):
    st.markdown("""
**The principle:** Transparency about AI use is a condition of research integrity, not a
stylistic choice. The minimum disclosure standard requires that any reader be able to
understand exactly how AI was used, verify that the use was appropriate, and reproduce
the workflow if needed.

**The five elements of an adequate AI disclosure statement:**
""")
    disclosure_data = {
        "Element": [
            "1. Task specification",
            "2. Tool identification",
            "3. Prompt documentation",
            "4. Verification statement",
            "5. Failure-mode report",
        ],
        "What it requires": [
            "State exactly which tasks AI was used for (e.g., 'literature scoping', 'data annotation', 'language editing')",
            "Name the model and version (e.g., 'GPT-4o, gpt-4o-2025-01-01') and the date of use",
            "Provide the exact prompt(s) used, or a link to a supplementary file containing them",
            "State what verification steps were applied to each AI-generated output",
            "Report the failure-discovery rate: how many AI outputs required correction and what corrections were made",
        ],
        "Common omission": [
            "'AI was used to assist with writing' (no task specification)",
            "'ChatGPT was used' (no version, no date)",
            "No prompts provided",
            "No verification described",
            "No failure-mode information",
        ],
    }
    st.dataframe(pd.DataFrame(disclosure_data), use_container_width=True)

    st.markdown("##### Adequate vs. inadequate disclosure: two examples")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**❌ Inadequate disclosure**")
        st.code(
            "AI tools were used to assist with the preparation of this manuscript.",
            language="text"
        )
        st.markdown("""
This statement fails all five elements. It does not specify which tasks, which tools,
which prompts, what verification was applied, or what errors were found and corrected.
It provides no information that would allow a reader to evaluate the integrity of the research.
""")
    with col2:
        st.markdown("**✅ Adequate disclosure**")
        st.code(
            "GPT-4o (gpt-4o-2025-01-01, accessed July 2026) was used for two tasks: "
            "(1) initial literature scoping (prompts provided in Supplementary File S1) "
            "and (2) language editing of the Discussion section. All AI-suggested citations "
            "were verified against primary sources using the three-step protocol described "
            "in Section 2.3. The citation audit identified 2 inaccurate references (out of 18) "
            "that were corrected before submission. No AI assistance was used in data "
            "collection, analysis, or interpretation.",
            language="text"
        )
        st.markdown("""
This statement specifies the task, the tool and version, the date, the prompts (by reference),
the verification method, and the failure-discovery rate. A reader can evaluate the integrity
of the research and reproduce the workflow.
""")

with st.expander("**Example 2 — Publisher and Funder Policy Landscape**"):
    st.markdown("""
The policy landscape is evolving rapidly. The following table summarizes the current positions
of major publishers and funders as of mid-2026. Researchers should always check the current
policy of the specific journal or funder before submission.
""")
    policy_data = {
        "Organization": [
            "Nature Portfolio", "Elsevier", "Springer Nature", "PLOS",
            "NIH (US)", "UKRI (UK)", "ERC (EU)", "NSF (US)",
        ],
        "AI authorship": [
            "Prohibited", "Prohibited", "Prohibited", "Prohibited",
            "N/A (funder)", "N/A (funder)", "N/A (funder)", "N/A (funder)",
        ],
        "Disclosure required?": [
            "Yes — in Methods", "Yes — in Methods", "Yes — in Methods", "Yes — in Methods",
            "Yes — in application", "Yes — in application", "Yes — in application", "Yes — in application",
        ],
        "Peer review confidentiality": [
            "AI prohibited in review", "AI prohibited in review", "AI prohibited in review",
            "AI prohibited in review", "N/A", "N/A", "N/A", "N/A",
        ],
        "Policy URL": [
            "nature.com/nature-portfolio/editorial-policies",
            "elsevier.com/about/policies/publishing-ethics",
            "springernature.com/gp/policies/editorial-policies",
            "plos.org/publication-ethics",
            "grants.nih.gov/grants/guide/notice-files",
            "ukri.org/about-us/policies-standards-and-data",
            "erc.europa.eu/apply-grant/open-science",
            "nsf.gov/policies",
        ],
    }
    st.dataframe(pd.DataFrame(policy_data), use_container_width=True)
    st.caption(
        "⚠️ This table reflects policies as of July 2026. Policies are changing rapidly. "
        "Always verify the current policy at the source URL before submission."
    )

with st.expander("**Example 3 — Future Directions: Human-AI Collaboration in Scientific Discovery**"):
    st.markdown("""
**The complementary-strengths model:** The most productive long-term relationship between
human researchers and AI systems is one of complementary strengths, not substitution.

| Human strengths | AI strengths |
|----------------|-------------|
| Theoretical framing and conceptual innovation | Pattern recognition across large corpora |
| Domain expertise and contextual judgement | Rapid synthesis of structured information |
| Ethical reasoning and value judgements | Consistent application of defined rules |
| Accountability and scholarly responsibility | Tireless execution of routine tasks |
| Creative hypothesis generation | Systematic exploration of parameter spaces |
| Peer community and disciplinary norms | Cross-domain analogical transfer |

**The agentic turn:** AI systems are increasingly capable of executing multi-step research
workflows autonomously — querying databases, running analyses, generating reports. This raises
the stakes for the human-in-the-loop discipline. As AI systems become more capable, the
researcher's role shifts from execution to direction, verification, and accountability.

**The open question:** As AI systems begin to generate novel hypotheses that humans would not
have formulated independently, the authorship boundary becomes genuinely contested. The field
has not yet resolved this question. What is clear is that the researcher who publishes an
AI-generated hypothesis bears full scholarly responsibility for its validity — regardless of
how it was generated.
""")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# BYOD
# ══════════════════════════════════════════════════════════════════════════════
st.header("🔬 Bring Your Own AI Disclosure Statement (BYOD)")

st.markdown("""
Paste a draft methods section or AI disclosure statement below. The app will evaluate it
against the five-element minimum disclosure standard and identify what is missing or insufficient.

> **Privacy notice:** Your text is processed in session memory only. Never stored or logged.
> **Note:** Requires an API key. Upload your key on the home page.
""")

disclosure_text = st.text_area(
    "Paste your draft AI disclosure statement or methods section:",
    height=200,
    placeholder="e.g. 'AI tools were used to assist with the preparation of this manuscript...'",
)

run_eval = st.button("▶ Evaluate Against Disclosure Standard", use_container_width=False)

if run_eval and disclosure_text.strip():
    with st.spinner("Evaluating disclosure statement..."):
        system = (
            "You are a research integrity advisor specializing in AI disclosure standards. "
            "Evaluate the following disclosure statement or methods section against the five-element "
            "minimum AI disclosure standard:\n"
            "1. Task specification: Does it state exactly which tasks AI was used for?\n"
            "2. Tool identification: Does it name the model, version, and date of use?\n"
            "3. Prompt documentation: Does it provide or reference the exact prompts used?\n"
            "4. Verification statement: Does it describe what verification steps were applied?\n"
            "5. Failure-mode report: Does it report the failure-discovery rate and corrections made?\n\n"
            "For each element: (a) state whether it is present, absent, or partially present; "
            "(b) quote the relevant text if present; (c) provide specific guidance on what to add "
            "if absent or insufficient. Conclude with a revised disclosure statement that meets "
            "all five elements, based on what can be inferred from the text provided."
        )
        result = call_llm(system, f"Disclosure statement:\n\n{disclosure_text}")
    st.subheader("Disclosure Evaluation Result")
    st.info(result)
    st.caption(
        "⚠️ This evaluation is AI-generated. Review each element independently against the "
        "five-element standard described in the worked example above. The revised statement "
        "provided is a starting point — you must complete it with the actual details of your AI use."
    )

if run_eval and not disclosure_text.strip():
    st.error("Please paste a disclosure statement before running the evaluation.")

st.markdown("---")

# ── Closing synthesis ──────────────────────────────────────────────────────────
st.header("🎓 Seminar Synthesis: The Researcher's Compact with AI")
st.markdown("""
Across three days and six sessions, this seminar has argued for a single, consistent position:

> **AI augments research by taking on labour tasks and expanding the researcher's discovery
> capacity. It does not replace the researcher's judgement, accountability, or scholarly
> responsibility. Every AI-mediated output requires human verification before it enters
> the scholarly record.**

The six competencies — citation verification, model specification, prompt discipline,
adversarial review, sycophancy detection, and failure-mode reporting — are not bureaucratic
requirements. They are the practical expression of this compact. A researcher who applies
them consistently is not limiting their use of AI; they are using AI in a way that is
methodologically defensible, reproducible, and worthy of the scholarly community's trust.

The most important skill in AI-augmented research is not knowing which tool to use.
It is knowing when to stop and think.
""")

st.markdown("---")
st.caption("Session 3.2 · AI-Augmented Research Seminar · © 2026 Moses Boudourides · Northwestern University")

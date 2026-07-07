"""
AI-Augmented Research — Seminar Companion App
Landing page: seminar overview, 6-session architecture, BYOD description, resources.
"""

import streamlit as st
from llm_helper import render_sidebar_llm_config, PROVIDERS

st.set_page_config(
    page_title="AI-Augmented Research",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar: LLM provider + API key ───────────────────────────────────────────
render_sidebar_llm_config()

# ── Page header ────────────────────────────────────────────────────────────────
st.title("🧠 AI-Augmented Research")
st.subheader("A Three-Day Academic Seminar — August 10, 11 & 12, 2026")

st.markdown("""
**Instructor:** Moses Boudourides, Data Science Graduate Program,
School of Professional Studies, Northwestern University

> **📋 Registration**
> **[Register now at instats.org](https://instats.org)**
""")

st.markdown("---")

# ── Core Identity ──────────────────────────────────────────────────────────────
st.markdown("""
### A No-Code Seminar for Academic Researchers

This seminar is conceived as a **fully no-code** research methods workshop: participants are not
expected to write or modify a single line of code. It is designed for doctoral students, postdoctoral
researchers, and faculty across all disciplines who want to engage seriously with AI as a research tool
— not as a novelty, but as a methodologically rigorous component of the scholarly workflow.

The central argument of the seminar is that AI literacy for academic researchers is fundamentally a
**judgement problem**, not a tooling-skills problem. The barrier to sophisticated computational research
has shifted from programming expertise to **validity reasoning** — the ability to direct, verify, and
critically assess what AI-mediated tools produce.

Participants work through this Streamlit companion app, which provides annotated worked examples and
BYOD (Bring Your Own Data/Document) interfaces for each of the six sessions. The app demonstrates the
verification disciplines discussed in the seminar: citation auditing, prompt documentation, sycophancy
detection, and structured failure-mode reporting.
""")

st.markdown("---")

# ── AI Provider Info ───────────────────────────────────────────────────────────
st.markdown("### Supported AI Providers")
st.markdown("""
The app supports four AI providers. Select your provider in the sidebar and upload your API key
as a plain-text `.txt` file. Keys are held in session memory only and are never stored or logged.
""")

provider_data = {
    "Provider": ["Google Gemini (Free)", "Groq (Free)", "OpenAI", "Anthropic Claude"],
    "Default model": ["Gemini 1.5 Flash", "Llama 3.1 70B", "GPT-4o", "Claude 3.5 Sonnet"],
    "Cost": ["Free tier (1,500 req/day)", "Free tier (14,400 req/day)", "Paid (per token)", "Paid (per token)"],
    "Get key": [
        "aistudio.google.com",
        "console.groq.com",
        "platform.openai.com",
        "console.anthropic.com",
    ],
}
import pandas as pd
st.dataframe(pd.DataFrame(provider_data), use_container_width=True)
st.caption(
    "For seminar participants with no existing API account, **Gemini 1.5 Flash** (free, "
    "no credit card required) is the recommended starting point."
)

st.markdown("---")

# ── Navigation ─────────────────────────────────────────────────────────────────
st.markdown("### How to Navigate")
st.markdown("""
Use the **sidebar** to select a session. Each session page contains:
1. **Worked examples** — annotated demonstrations showing the prompt, the raw AI output, the verification step, and the final verified result.
2. **BYOD extension** — upload your own data, question, or manuscript to run the same workflow on your own research.

| Day | Date | Session | Theme |
|-----|------|---------|-------|
| **Day 1** | Aug 10 · 6:00–7:30 pm | Session 1.1 | Research Judgement in an AI Environment |
| **Day 1** | Aug 10 · 7:30–9:00 pm | Session 1.2 | Literature Discovery, Synthesis, and Research Design |
| **Day 2** | Aug 11 · 6:00–7:30 pm | Session 2.1 | Validity Reasoning in AI-Mediated Data Work |
| **Day 2** | Aug 11 · 7:30–9:00 pm | Session 2.2 | From Research Question to Verified Finding (Case Study) |
| **Day 3** | Aug 12 · 6:00–7:30 pm | Session 3.1 | Authorship, Integrity, and the Limits of AI Assistance |
| **Day 3** | Aug 12 · 7:30–9:00 pm | Session 3.2 | Research Judgement in an Institutional Context |
""")

st.info("👈 Select a session from the sidebar to begin.")

st.markdown("---")

# ── Two Foundational Distinctions ──────────────────────────────────────────────
st.markdown("### Two Foundational Distinctions")
st.markdown("""
Every session in this seminar is organized around two foundational distinctions:

**1. Labour tasks versus judgement tasks.**
Labour tasks are rule-based, routine, and highly verifiable — formatting citations, transcribing
recordings, generating boilerplate code. These can be safely delegated to AI. Judgement tasks require
domain expertise and scholarly accountability — framing the research question, interpreting a null result,
evaluating the significance of a finding. These must remain with the human researcher.

**2. Discovery activities versus verification activities.**
Discovery involves generating possibilities, exploring literature, and surfacing analogies — AI adds
immense value here. Verification involves checking references, validating claims, and reproducing
computations — here, human judgement is paramount and AI assistance requires careful management.

The most common and consequential error in AI-augmented research is conflating the two: treating
AI-generated outputs from the discovery phase as verified findings without applying rigorous checks.
""")

st.markdown("---")

# ── The Six Core Competencies ──────────────────────────────────────────────────
st.markdown("### The Six Core Competencies (Zyphur 2026)")
st.markdown("""
| # | Competency | What it addresses |
|---|-----------|-------------------|
| 1 | **Citation Verification** | Detecting and eliminating citation hallucination |
| 2 | **Model and Parameter Specification** | Documenting versions, temperatures, and seeds for reproducibility |
| 3 | **Prompt Discipline** | Treating prompts as methodological choices and documenting them verbatim |
| 4 | **Model Heterogeneity in Adversarial Review** | Using multiple AI families to challenge assumptions |
| 5 | **Sycophancy Detection and Human-as-Verifier Discipline** | Counteracting LLM agreement bias |
| 6 | **Structured Failure-Mode Reporting** | Documenting AI failure modes, rates, and residual risks |
""")

st.markdown("---")

# ── BYOD ───────────────────────────────────────────────────────────────────────
st.markdown("### Bring Your Own Data/Document (BYOD)")
st.markdown("""
| Session | BYOD Input | What the app does |
|---------|-----------|-------------------|
| **1.1** | Research question or hypothesis (text) | Runs sycophancy check + adversarial critique |
| **1.2** | Research question (text) | Scopes literature via Semantic Scholar API + citation verification |
| **2.1** | Dataset (CSV/Excel) | Performs cleaning audit and flags methodological assumptions |
| **2.2** | Dataset (CSV/Excel) | Full pipeline: summary stats → cleaning → visualization → AI interpretation → verification |
| **3.1** | Abstract or manuscript passage (text) | Citation audit + sycophancy check + adversarial critique |
| **3.2** | Draft AI disclosure statement (text) | Evaluates against the minimum AI disclosure standard |

> **Privacy notice:** All user-uploaded files and text are processed in session memory only.
> No data is written to disk, stored, or transmitted to any service other than the AI provider you select.
> Your API key is never displayed, stored, or logged.
""")

st.markdown("---")

# ── Resources ──────────────────────────────────────────────────────────────────
st.markdown("### Resources")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
**📋 InStats Seminar Page**
[Register and view full details](https://instats.org)
    """)
with col2:
    st.markdown("""
**💻 GitHub Repository**
[View the code, slides, and paper](https://github.com/mboudour/ai-augmented-research)
    """)
with col3:
    st.markdown("""
**📄 Position Paper**
[AI-Augmented Research (PDF)](https://github.com/mboudour/ai-augmented-research/raw/main/paper/ai_augmented_research.pdf)
    """)

st.markdown("---")
st.caption("© 2026 Moses Boudourides · Northwestern University · Built with Streamlit")

"""
Session 1.2 — Literature Discovery, Synthesis, and Research Design
Day 1 · August 10, 2026 · 7:30–9:00 pm

Worked examples: citation hallucination detection, RAG vs. general LLM comparison,
                 research design AI assistance.
BYOD: user enters a research question; app queries Semantic Scholar API + runs citation verification.
"""

import streamlit as st
import sys, pathlib as _pathlib
sys.path.insert(0, str(_pathlib.Path(__file__).resolve().parent.parent))
from llm_helper import render_sidebar_llm_config, call_llm, get_provider_info
import requests
import pandas as pd

st.set_page_config(
    page_title="Session 1.2 — Literature Discovery",
    page_icon="📚",
    layout="wide",
)
render_sidebar_llm_config()


def search_semantic_scholar(query: str, limit: int = 8) -> list:
    """Query the Semantic Scholar public API and return a list of paper dicts."""
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,year,abstract,externalIds,citationCount",
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("data", [])
    except Exception as e:
        return []

# ── Page header ────────────────────────────────────────────────────────────────
st.title("📚 Session 1.2 — Literature Discovery, Synthesis, and Research Design")
st.caption("Day 1 · August 10, 2026 · 7:30–9:00 pm")

st.markdown("""
This session covers the discovery-versus-verification distinction in literature work, the citation
hallucination problem, and the use of AI in research design. The worked examples demonstrate the
three-step citation verification protocol and the difference between RAG-based and general LLM
literature retrieval.
""")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# WORKED EXAMPLES
# ══════════════════════════════════════════════════════════════════════════════
st.header("📋 Worked Examples")

# ── Example 1: Citation hallucination ─────────────────────────────────────────
with st.expander("**Example 1 — Citation Hallucination: The Three-Step Verification Protocol**", expanded=True):
    st.markdown("""
**Research context:** A researcher asks a general-purpose LLM (no RAG, no retrieval grounding)
to provide five key references on the effect of social media on adolescent mental health.

**The hallucination risk:** General LLMs generate plausible-sounding citations from memory.
Studies report hallucination rates of 18–55% depending on the model (Walters & Wilder, 2023).
""")
    st.markdown("##### Prompt used")
    st.code(
        "Model: GPT-4o | Temperature: 0.3 | Date: July 2026\n\n"
        "System: You are a helpful research assistant.\n\n"
        "User: Please provide five key academic references on the effect of social media "
        "use on adolescent mental health, with full citations in APA format.",
        language="text"
    )
    st.markdown("##### Raw AI output (representative)")
    st.code("""
1. Twenge, J. M., & Campbell, W. K. (2019). Media use is linked to lower psychological
   well-being: Evidence from three datasets. Psychiatric Quarterly, 90(2), 311–331.

2. Orben, A., & Przybylski, A. K. (2019). The association between adolescent well-being
   and digital technology use. Nature Human Behaviour, 3(2), 173–182.

3. Coyne, S. M., Rogers, A. A., Zurcher, J. D., Stockdale, L., & Booth, M. (2020).
   Does time spent using social media impact mental health? An eight year longitudinal study.
   Computers in Human Behavior, 104, 106160.

4. Vannucci, A., Flannery, K. M., & Ohannessian, C. M. (2017). Social media use and
   anxiety in emerging adults. Journal of Affective Disorders, 207, 163–166.

5. Kelly, Y., Zilanawala, A., Booker, C., & Sacker, A. (2019). Social media use and
   adolescent mental health: Findings from the UK Millennium Cohort Study.
   EClinicalMedicine, 6, 59–68.
""", language="text")

    st.markdown("##### Three-step verification results")
    data = {
        "Citation": [
            "Twenge & Campbell (2019) Psychiatric Quarterly",
            "Orben & Przybylski (2019) Nature Human Behaviour",
            "Coyne et al. (2020) Computers in Human Behavior",
            "Vannucci et al. (2017) Journal of Affective Disorders",
            "Kelly et al. (2019) EClinicalMedicine",
        ],
        "Step 1: Paper exists?": ["✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes"],
        "Step 2: Abstract matches?": ["⚠️ Partial", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes"],
        "Step 3: Specific claim present?": ["⚠️ Volume/issue incorrect", "✅ Yes", "✅ Yes", "✅ Yes", "✅ Yes"],
        "Verdict": ["Needs correction", "✅ Valid", "✅ Valid", "✅ Valid", "✅ Valid"],
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True)
    st.markdown("""
**Failure-discovery rate:** 1 out of 5 citations (20%) required correction (incorrect volume/issue).
The paper exists but the bibliographic details were inaccurate.

**Methodological lesson (Competency 1):** Even when a paper exists, the specific details may be
wrong. The three-step protocol — existence, abstract match, claim present — is the minimum standard.
A citation audit is a non-negotiable step before submission.
""")

# ── Example 2: Research design AI assistance ──────────────────────────────────
with st.expander("**Example 2 — AI in Research Design: Tutor Mode and Its Limits**"):
    st.markdown("""
**Research context:** A political scientist unfamiliar with network analysis wants to study
information diffusion on social media. They use AI in Tutor mode to understand the method.
""")
    st.code(
        "Model: GPT-4o | Temperature: 0.3\n\n"
        "System: You are a rigorous methods tutor. Explain the method clearly, including "
        "its assumptions, requirements, and limitations. Do not recommend it — describe it.\n\n"
        "User: I want to study how political misinformation spreads on Twitter. A colleague "
        "suggested network analysis. Can you explain what network analysis involves, what "
        "assumptions it makes, and what its limitations are for this type of research?",
        language="text"
    )
    st.markdown("""
**What the AI does well here:** Explains the method (nodes, edges, centrality measures,
community detection), its assumptions (stationarity of the network, completeness of the data),
and its limitations (API data restrictions, sampling bias, inability to infer causation).

**What the AI cannot do:** Determine whether network analysis is the *right* method for this
specific research question, given the researcher's theoretical framework, data access, and
disciplinary context. That is a judgement task.

**Verification step:** The researcher should verify the AI's description of the method against
a primary methods text (e.g., Wasserman & Faust 1994; Borgatti et al. 2018) before adopting it.

**Methodological lesson:** AI in Tutor mode democratizes methodological access. A researcher
can develop sufficient literacy to make an informed design decision without becoming a network
analysis expert. But the decision itself — and the ability to defend it — must remain with the researcher.
""")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# BYOD
# ══════════════════════════════════════════════════════════════════════════════
st.header("🔬 Bring Your Own Research Question (BYOD)")

st.markdown("""
Enter a research question below. The app will:
1. **Query Semantic Scholar** (no API key required for this step) to retrieve real papers on your topic.
2. **Generate an AI literature summary** of the retrieved papers.
3. **Run a citation verification prompt** — asking the AI to flag any claims in the summary that
   require primary-source verification.

> **Note:** The AI summary step requires an API key. Upload your key on the home page.
""")

byod_query = st.text_input(
    "Your research question or topic:",
    placeholder="e.g. effect of mindfulness interventions on workplace stress",
)

n_papers = st.slider("Number of papers to retrieve:", min_value=3, max_value=10, value=5)

run_byod = st.button("▶ Search and Summarise", use_container_width=False)

if run_byod and byod_query.strip():
    # Step 1: Semantic Scholar search
    with st.spinner("Querying Semantic Scholar..."):
        papers = search_semantic_scholar(byod_query, limit=n_papers)

    if not papers:
        st.error("No results returned from Semantic Scholar. Try a different query.")
    else:
        st.subheader("Step 1: Retrieved Papers")
        rows = []
        for p in papers:
            authors = ", ".join([a.get("name", "") for a in p.get("authors", [])[:3]])
            if len(p.get("authors", [])) > 3:
                authors += " et al."
            doi = p.get("externalIds", {}).get("DOI", "N/A")
            rows.append({
                "Title": p.get("title", "N/A"),
                "Authors": authors,
                "Year": p.get("year", "N/A"),
                "Citations": p.get("citationCount", "N/A"),
                "DOI": doi,
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)
        st.caption("✅ These papers are real — retrieved live from Semantic Scholar. Verify each DOI before citing.")

        # Step 2: AI summary
        st.subheader("Step 2: AI Literature Summary")
        paper_list = "\n".join([
            f"- {r['Authors']} ({r['Year']}). {r['Title']}."
            for r in rows
        ])
        system_sum = (
            "You are a rigorous academic research assistant. Based only on the list of papers "
            "provided, write a concise literature summary (3–4 paragraphs) that identifies "
            "the main themes, key findings, and gaps in this body of work. "
            "Do not invent citations or add papers not in the list."
        )
        user_sum = f"Research topic: {byod_query}\n\nPapers:\n{paper_list}"
        with st.spinner("Generating AI summary..."):
            summary = call_llm(system_sum, user_sum)
        st.info(summary)
        st.code(
            f"Model: gpt-4o | Temperature: 0.2\nSystem: {system_sum[:120]}...\nUser: [paper list above]",
            language="text"
        )

        # Step 3: Verification prompt
        st.subheader("Step 3: Citation Verification Prompt")
        system_ver = (
            "You are a citation auditor. Review the literature summary provided and identify: "
            "(1) any specific empirical claims that require primary-source verification, "
            "(2) any claims that go beyond what the listed papers can support, "
            "(3) any gaps or limitations in the summary. "
            "Be specific about which sentences require verification."
        )
        with st.spinner("Running verification audit..."):
            verification = call_llm(system_ver, f"Summary:\n{summary}\n\nPapers used:\n{paper_list}")
        st.warning(verification)
        st.caption(
            "⚠️ Verification reminder: This audit is itself AI-generated. "
            "Use it as a checklist to guide your own reading of the primary sources — "
            "do not treat it as a substitute for reading the papers."
        )

if run_byod and not byod_query.strip():
    st.error("Please enter a research question before running the search.")

st.markdown("---")
st.caption("Session 1.2 · AI-Augmented Research Seminar · © 2026 Moses Boudourides · Northwestern University")

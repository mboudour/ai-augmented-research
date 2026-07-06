"""
Session 1.1 — Research Judgement in an AI Environment
Day 1 · August 10, 2026 · 6:00–7:30 pm

Worked examples: sycophancy check, adversarial critique, labour-vs-judgement classification.
BYOD: user submits a research question or hypothesis; app runs sycophancy check + adversarial critique.
"""

import streamlit as st
import os

st.set_page_config(
    page_title="Session 1.1 — Research Judgement",
    page_icon="🧠",
    layout="wide",
)

# ── Shared API key helper ──────────────────────────────────────────────────────
def get_api_key():
    return st.session_state.get("api_key", None)

def call_llm(system_prompt: str, user_prompt: str, model: str = "gpt-4o") -> str:
    """Call OpenAI-compatible API and return the response text."""
    api_key = get_api_key()
    if not api_key:
        return "⚠️ No API key found. Please upload your API key file on the home page."
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_tokens=1200,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ API error: {e}"

# ── Page header ────────────────────────────────────────────────────────────────
st.title("🧠 Session 1.1 — Research Judgement in an AI Environment")
st.caption("Day 1 · August 10, 2026 · 6:00–7:30 pm")

st.markdown("""
This session establishes the foundational framework for the seminar. We examine the AI ecosystem,
the labour-versus-judgement demarcation, and the cognitive partner model — including the risk of
algorithmic sycophancy. The worked examples below demonstrate each concept with full annotation.
""")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# WORKED EXAMPLES
# ══════════════════════════════════════════════════════════════════════════════
st.header("📋 Worked Examples")

# ── Example 1: Sycophancy check ───────────────────────────────────────────────
with st.expander("**Example 1 — Detecting Sycophancy: The Leading-Question Trap**", expanded=True):
    st.markdown("""
**Research context:** A doctoral student in education policy believes that charter schools improve
student outcomes. They ask an AI the following question.

**The sycophancy risk:** The question embeds a premise that the AI is likely to validate.
""")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### 🔴 Leading prompt (sycophancy-prone)")
        st.code(
            "Model: GPT-4o | Temperature: 0.3 | Date: July 2026\n\n"
            "System: You are a helpful research assistant.\n\n"
            "User: Is it true that charter schools improve student outcomes "
            "compared to traditional public schools?",
            language="text"
        )
        st.markdown("""
**Raw AI output (representative):**
> "Yes, there is evidence suggesting that charter schools can improve student outcomes in certain
> contexts. Studies such as CREDO (2015) and Angrist et al. (2010) have found positive effects
> on reading and mathematics achievement, particularly in urban areas..."

**Verification step:** CREDO (2015) exists and does report positive effects for some charter
schools — but the full report also documents that 31% of charter schools perform significantly
*worse* than comparable public schools. The AI's framing is selectively confirmatory.

**Verdict:** ⚠️ Sycophantic. The AI confirmed the premise without presenting the full picture.
""")
    with col2:
        st.markdown("##### 🟢 Neutral prompt (sycophancy-resistant)")
        st.code(
            "Model: GPT-4o | Temperature: 0.3 | Date: July 2026\n\n"
            "System: You are a critical research assistant. Present evidence on both sides.\n\n"
            "User: What does the empirical literature say about the relationship between "
            "charter school attendance and student academic outcomes?",
            language="text"
        )
        st.markdown("""
**Raw AI output (representative):**
> "The empirical literature on charter schools and student outcomes is mixed. Some studies
> find positive effects (CREDO 2015 for urban charter schools; Angrist et al. 2010 for Boston
> charter schools), while others find null or negative effects (Bifulco & Ladd 2006; Zimmer
> et al. 2009). Effect sizes vary substantially by location, school type, and student population..."

**Verification step:** All four citations verified against primary sources. The framing accurately
reflects the contested nature of the evidence.

**Verdict:** ✅ Balanced. The neutral framing produced a more accurate representation of the literature.

**Methodological lesson (Competency 5):** AI agreement is not evidence. Researchers must actively
design prompts that challenge their assumptions rather than confirm them.
""")

# ── Example 2: Labour vs. Judgement classification ────────────────────────────
with st.expander("**Example 2 — The Labour-versus-Judgement Demarcation**"):
    st.markdown("""
**Research context:** A sociologist is beginning a mixed-methods study of organizational resilience.
They ask an AI to help plan the research. The example below shows the same request framed two ways —
one that correctly uses AI for a labour task, and one that incorrectly delegates a judgement task.
""")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### ✅ Appropriate delegation (labour task)")
        st.code(
            "Model: GPT-4o | Temperature: 0.3\n\n"
            "User: I am conducting a mixed-methods study of organizational resilience. "
            "Please format the following five references in APA 7th edition:\n"
            "[references listed]",
            language="text"
        )
        st.markdown("""
**Why this is appropriate:** Citation formatting is a rule-based, verifiable task with an
objective standard. The AI applies the APA rules; the researcher verifies the output against
the APA manual. No scholarly judgement is required or delegated.

**Verification step:** Each formatted citation checked against APA 7th edition rules. ✅
""")
    with col2:
        st.markdown("##### ⚠️ Inappropriate delegation (judgement task)")
        st.code(
            "Model: GPT-4o | Temperature: 0.3\n\n"
            "User: I am conducting a mixed-methods study of organizational resilience. "
            "What theoretical framework should I use and which variables should I include "
            "in my regression model?",
            language="text"
        )
        st.markdown("""
**Why this is problematic:** Selecting a theoretical framework and specifying a regression
model are judgement tasks. They require domain expertise, knowledge of the specific research
context, and scholarly accountability. The AI can surface options, but the researcher must
independently evaluate and defend every choice.

**The substitution error (Zyphur 2026):** Using AI to substitute for the researcher's
intellectual authority rather than to augment it. A researcher who publishes an AI-selected
theoretical framework they cannot independently defend has published invalid research.

**Correct use:** Ask the AI to *list and describe* candidate frameworks, then make the
selection yourself based on your own theoretical judgement.
""")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# BYOD
# ══════════════════════════════════════════════════════════════════════════════
st.header("🔬 Bring Your Own Research Question (BYOD)")

st.markdown("""
Enter a research question or hypothesis below. The app will:
1. Run a **sycophancy check** — asking the AI to identify any assumptions embedded in your framing.
2. Run an **adversarial critique** — asking the AI to construct the strongest possible counterargument.
3. Show you both outputs side by side so you can evaluate them independently.

> **Note:** This requires an API key. Upload your key on the home page before proceeding.
""")

user_question = st.text_area(
    "Your research question or hypothesis:",
    placeholder="e.g. Does social media use increase political polarization among young adults?",
    height=100,
)

col_run1, col_run2 = st.columns(2)

with col_run1:
    run_syco = st.button("▶ Run Sycophancy Check", use_container_width=True)
with col_run2:
    run_adv = st.button("▶ Run Adversarial Critique", use_container_width=True)

if run_syco and user_question.strip():
    with st.spinner("Running sycophancy check..."):
        system = (
            "You are a critical research methods advisor. Your task is to identify any "
            "assumptions, biases, or leading framings embedded in the research question or "
            "hypothesis provided. Do not answer the question itself. Instead, list the "
            "assumptions the question takes for granted, explain how each assumption could "
            "bias the research, and suggest a more neutral reformulation."
        )
        result = call_llm(system, f"Research question: {user_question}")
    st.subheader("Sycophancy Check Result")
    st.markdown(f"""
**Prompt used (verbatim):**
```
System: {system[:200]}...
User: Research question: {user_question}
Model: gpt-4o | Temperature: 0.3
```
**AI output:**
""")
    st.info(result)
    st.caption(
        "⚠️ Verification reminder: Review each identified assumption independently. "
        "AI identification of assumptions is itself subject to model bias — use this output "
        "as a starting point for your own critical reflection, not as a definitive audit."
    )

if run_adv and user_question.strip():
    with st.spinner("Running adversarial critique..."):
        system = (
            "You are a rigorous academic peer reviewer. Your task is to construct the "
            "strongest possible counterargument against the research question or hypothesis "
            "provided. Draw on methodological, theoretical, and empirical objections. "
            "Be specific and cite the types of evidence or arguments that would challenge "
            "the premise. Do not be diplomatic — your goal is to stress-test the research."
        )
        result = call_llm(system, f"Research question or hypothesis: {user_question}")
    st.subheader("Adversarial Critique Result")
    st.markdown(f"""
**Prompt used (verbatim):**
```
System: {system[:200]}...
User: Research question or hypothesis: {user_question}
Model: gpt-4o | Temperature: 0.3
```
**AI output:**
""")
    st.warning(result)
    st.caption(
        "⚠️ Verification reminder: Evaluate each objection independently against the literature. "
        "An AI critique is a brainstorm prompt, not a peer review. The researcher's domain "
        "expertise must assess which objections are substantive."
    )

if (run_syco or run_adv) and not user_question.strip():
    st.error("Please enter a research question before running the analysis.")

st.markdown("---")
st.caption("Session 1.1 · AI-Augmented Research Seminar · © 2026 Moses Boudourides · Northwestern University")

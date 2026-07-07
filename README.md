# AI-Augmented Research
**instats Seminar — August 10, 11, and 12, 2026**
**Instructor:** Moses Boudourides, Data Science Graduate Program, School of Professional Studies, Northwestern University

> ### 📋 Registration
> **[Register now at instats.org](https://instats.org/seminar/ai-assisted-systematic-reviews-and-meta)**

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://ai-augmented-research.streamlit.app) [Streamlit App](https://ai-augmented-research.streamlit.app)

---

## Overview

This repository contains all materials for the *AI-Augmented Research* seminar: slide decks,
a position paper, and the source code for the interactive Streamlit companion app.

The seminar argues that AI literacy for academic researchers is fundamentally a **judgement
problem**, not a tooling-skills problem. The barrier to sophisticated computational research
has shifted from programming expertise to validity reasoning — the ability to direct, verify,
and critically assess what AI-mediated tools produce.

The seminar is aligned with Michael Zyphur's (2026) *Responsible AI in Academic Research:
A Competency Framework for Research Training*.

---

## Seminar Schedule

| Day | Date | Session | Title | Time |
|-----|------|---------|-------|------|
| 1 | Aug 10 | 1.1 | Research Judgement in an AI Environment | 6:00–7:30 pm |
| 1 | Aug 10 | 1.2 | Literature Discovery, Synthesis, and Research Design | 7:30–9:00 pm |
| 2 | Aug 11 | 2.1 | Validity Reasoning in AI-Mediated Data Work | 6:00–7:30 pm |
| 2 | Aug 11 | 2.2 | From Research Question to Verified Finding (Case Study) | 7:30–9:00 pm |
| 3 | Aug 12 | 3.1 | Authorship, Integrity, and the Limits of AI Assistance | 6:00–7:30 pm |
| 3 | Aug 12 | 3.2 | Research Judgement in an Institutional Context | 7:30–9:00 pm |

---

## Interactive Companion App

The Streamlit app provides:
1. **Worked examples** — annotated demonstrations for each session
2. **BYOD (Bring Your Own Data/Document)** — interactive interfaces for participants to
   apply the verification workflows to their own research

**Running locally:**
```bash
cd app
pip install -r requirements.txt
streamlit run app.py
```

**API key:** BYOD features support four providers: Gemini (free), Groq (free), OpenAI, and Claude. Upload a plain-text `.txt` file containing your key via the sidebar. Keys are held in session memory only and are never stored or logged.

---

## The Six Core Competencies (Zyphur 2026)

1. **Citation Verification** — Three-step protocol to detect citation hallucination
2. **Model and Parameter Specification** — Documenting versions, temperatures, and seeds
3. **Prompt Discipline** — Treating prompts as methodological choices
4. **Model Heterogeneity in Adversarial Review** — Using multiple AI families
5. **Sycophancy Detection and Human-as-Verifier Discipline** — Counteracting agreement bias
6. **Structured Failure-Mode Reporting** — Documenting failure modes and residual risks

---

## Position Paper

A manuscript describing the workshope is available here:

[AI-Augmented Research: A Framework for Scholarly Judgement and Responsible Practice](./paper/ai_augmented_research.pdf)
---

## License

© 2026 Moses Boudourides · Northwestern University

Materials in this repository are made available for educational use.
Please cite appropriately if you use or adapt them.

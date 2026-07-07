# Scripts — AI-Augmented Research Seminar

This folder contains standalone Python scripts and a prompt library for the
*AI-Augmented Research* seminar. The scripts mirror the BYOD workflows in the
Streamlit app and can be run locally from the command line.

---

## Requirements

```bash
pip install openai anthropic pandas matplotlib requests openpyxl
```

---

## API Keys

Set the relevant environment variable before running any script:

| Provider | Environment variable | Free tier? | Get key |
|---|---|---|---|
| Google Gemini | `GEMINI_API_KEY` | Yes | [aistudio.google.com](https://aistudio.google.com) |
| Groq | `GROQ_API_KEY` | Yes | [console.groq.com](https://console.groq.com) |
| OpenAI | `OPENAI_API_KEY` | No | [platform.openai.com](https://platform.openai.com) |
| Anthropic Claude | `ANTHROPIC_API_KEY` | No | [console.anthropic.com](https://console.anthropic.com) |

```bash
export GEMINI_API_KEY="your-key-here"
```

---

## Scripts

### `llm_client.py` — Shared LLM client (not run directly)
Provides `call_llm()` and `get_client_info()` used by all scripts.

---

### Session 1.1 — `session1_1_sycophancy_check.py`
Runs a sycophancy check and adversarial critique on a research question.

```bash
python session1_1_sycophancy_check.py \
    --question "Does social media use increase political polarization?" \
    --provider gemini \
    --output report_1_1.txt
```

---

### Session 1.2 — `session1_2_literature_scope.py`
Queries Semantic Scholar and synthesizes the results with citation verification.

```bash
python session1_2_literature_scope.py \
    --question "How does remote work affect organizational commitment?" \
    --limit 10 \
    --provider gemini \
    --output report_1_2.txt
```

---

### Session 2.1 — `session2_1_data_quality_audit.py`
Profiles a CSV/Excel dataset and runs an AI data quality audit.

```bash
python session2_1_data_quality_audit.py \
    --file data.csv \
    --provider gemini \
    --output report_2_1.txt
```

---

### Session 2.2 — `session2_2_end_to_end_pipeline.py`
Full pipeline: summary stats → cleaning audit → visualizations → interpretation → verification.

```bash
python session2_2_end_to_end_pipeline.py \
    --file data.csv \
    --question "What is the relationship between X and Y?" \
    --provider gemini \
    --output-dir ./pipeline_output
```

---

### Session 3.1 — `session3_1_manuscript_audit.py`
Citation audit, adversarial critique, and authorship boundary check on a manuscript passage.

```bash
python session3_1_manuscript_audit.py \
    --file abstract.txt \
    --provider gemini \
    --output report_3_1.txt

# Or pass text directly:
python session3_1_manuscript_audit.py \
    --text "Remote work has become a defining feature..." \
    --provider gemini
```

---

### Session 3.2 — `session3_2_disclosure_evaluator.py`
Evaluates a draft AI disclosure statement against the five-element minimum standard.

```bash
python session3_2_disclosure_evaluator.py \
    --text "AI tools were used to assist with the preparation of this manuscript." \
    --provider gemini \
    --output report_3_2.txt
```

---

## Prompt Library

The `prompts/` subfolder contains all system prompts used in the scripts and the
Streamlit app, saved verbatim with design rationale and known failure modes.

This implements **Competency 3 (Prompt Discipline)** from the Zyphur (2026) framework:
prompts are methodological choices and must be documented with the same rigour as
any other methodological decision.

See `prompts/README.md` for the full inventory.

---

## The Six Core Competencies (Zyphur 2026)

Each script implements one or more of the six core competencies:

| Script | Competencies |
|---|---|
| `session1_1_sycophancy_check.py` | C4 (Adversarial Review), C5 (Sycophancy Detection) |
| `session1_2_literature_scope.py` | C1 (Citation Verification), C3 (Prompt Discipline) |
| `session2_1_data_quality_audit.py` | C2 (Parameter Specification), C5 (Human-as-Verifier) |
| `session2_2_end_to_end_pipeline.py` | C1, C5, C6 (Failure-Mode Reporting) |
| `session3_1_manuscript_audit.py` | C1, C4, C5 |
| `session3_2_disclosure_evaluator.py` | C2, C3, C6 |

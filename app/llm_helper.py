"""
llm_helper.py — Shared LLM call helper for the AI-Augmented Research seminar app.

Supports four providers:
  1. Google Gemini (free tier)  — via OpenAI-compatible endpoint
  2. Groq (free tier)           — via OpenAI-compatible endpoint
  3. OpenAI                     — via standard OpenAI API
  4. Anthropic Claude           — via Anthropic SDK

Provider and key are read from st.session_state, set by the sidebar in app.py.
"""

import streamlit as st

# ── Provider configuration ─────────────────────────────────────────────────────
PROVIDERS = {
    "Gemini (Free)": {
        "label": "Google Gemini 1.5 Flash — Free tier",
        "models": ["gemini-1.5-flash", "gemini-1.5-pro"],
        "default_model": "gemini-1.5-flash",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "key_name": "GEMINI_API_KEY",
        "key_help": "Get a free key at https://aistudio.google.com — no credit card required.",
        "free": True,
    },
    "Groq (Free)": {
        "label": "Groq — Llama 3.1 70B — Free tier",
        "models": ["llama-3.1-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"],
        "default_model": "llama-3.1-70b-versatile",
        "base_url": "https://api.groq.com/openai/v1",
        "key_name": "GROQ_API_KEY",
        "key_help": "Get a free key at https://console.groq.com — no credit card required.",
        "free": True,
    },
    "OpenAI": {
        "label": "OpenAI GPT-4o",
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
        "default_model": "gpt-4o",
        "base_url": "https://api.openai.com/v1",
        "key_name": "OPENAI_API_KEY",
        "key_help": "Requires a paid OpenAI API key from https://platform.openai.com",
        "free": False,
    },
    "Claude": {
        "label": "Anthropic Claude 3.5 Sonnet",
        "models": ["claude-3-5-sonnet-20241022", "claude-3-haiku-20240307"],
        "default_model": "claude-3-5-sonnet-20241022",
        "base_url": None,  # Uses Anthropic SDK directly
        "key_name": "ANTHROPIC_API_KEY",
        "key_help": "Requires a paid Anthropic API key from https://console.anthropic.com",
        "free": False,
    },
}


def render_sidebar_llm_config():
    """Render the LLM provider selector and API key upload in the sidebar."""
    with st.sidebar:
        st.header("🤖 AI Provider")

        provider_name = st.selectbox(
            "Select provider:",
            options=list(PROVIDERS.keys()),
            index=0,
            key="llm_provider",
        )
        provider = PROVIDERS[provider_name]

        st.caption(f"**{provider['label']}**")

        if provider["free"]:
            st.success("✅ Free tier available — no credit card required.")
        else:
            st.info("💳 Paid API key required.")

        st.caption(provider["key_help"])

        # Model selector
        model_choice = st.selectbox(
            "Model:",
            options=provider["models"],
            index=0,
            key="llm_model",
        )
        st.session_state["llm_model_choice"] = model_choice

        # API key upload
        st.markdown("**API Key**")
        key_file = st.file_uploader(
            f"Upload {provider_name} key (.txt file):",
            type=["txt"],
            key=f"key_upload_{provider_name}",
            label_visibility="collapsed",
        )
        if key_file is not None:
            api_key = key_file.read().decode("utf-8").strip()
            st.session_state[provider["key_name"]] = api_key
            st.success("Key loaded (not displayed).")

        if st.button("Clear key", key="clear_key_btn"):
            for k in [p["key_name"] for p in PROVIDERS.values()]:
                st.session_state.pop(k, None)
            st.info("All keys cleared.")

        # Status
        active_key = st.session_state.get(provider["key_name"])
        if active_key:
            st.caption(f"✅ {provider_name} key active.")
        else:
            st.caption(f"⚠️ No {provider_name} key loaded.")

        st.markdown("---")


def call_llm(system_prompt: str, user_prompt: str) -> str:
    """
    Call the selected LLM provider with the given prompts.
    Returns the response text, or an error message string.
    """
    provider_name = st.session_state.get("llm_provider", "Gemini (Free)")
    provider = PROVIDERS[provider_name]
    model = st.session_state.get("llm_model_choice", provider["default_model"])
    api_key = st.session_state.get(provider["key_name"])

    if not api_key:
        return (
            f"⚠️ No API key for **{provider_name}**. "
            f"Please upload your key using the sidebar. {provider['key_help']}"
        )

    # ── Claude: use Anthropic SDK ──────────────────────────────────────────────
    if provider_name == "Claude":
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model=model,
                max_tokens=1500,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            return message.content[0].text
        except Exception as e:
            return f"❌ Claude API error: {e}"

    # ── All others: use OpenAI-compatible endpoint ─────────────────────────────
    try:
        import openai
        client = openai.OpenAI(
            api_key=api_key,
            base_url=provider["base_url"],
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ {provider_name} API error: {e}"


def get_provider_info() -> str:
    """Return a short string describing the active provider and model for prompt documentation."""
    provider_name = st.session_state.get("llm_provider", "Gemini (Free)")
    model = st.session_state.get("llm_model_choice", PROVIDERS[provider_name]["default_model"])
    return f"{provider_name} · {model} · Temperature 0.2"

"""
llm_client.py — Shared LLM client for all standalone scripts.

Supports four providers via environment variables or command-line arguments:
  - Gemini (free):  GEMINI_API_KEY
  - Groq (free):    GROQ_API_KEY
  - OpenAI:         OPENAI_API_KEY
  - Claude:         ANTHROPIC_API_KEY

Usage:
    from llm_client import call_llm, get_client_info

    response = call_llm(
        system_prompt="You are a critical research assistant.",
        user_prompt="Is it true that charter schools improve outcomes?",
        provider="gemini",   # gemini | groq | openai | claude
        model=None,          # None = use provider default
    )
"""

import os

PROVIDER_CONFIG = {
    "gemini": {
        "env_key": "GEMINI_API_KEY",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "default_model": "gemini-1.5-flash",
        "sdk": "openai",
    },
    "groq": {
        "env_key": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "default_model": "llama-3.1-70b-versatile",
        "sdk": "openai",
    },
    "openai": {
        "env_key": "OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o",
        "sdk": "openai",
    },
    "claude": {
        "env_key": "ANTHROPIC_API_KEY",
        "base_url": None,
        "default_model": "claude-3-5-sonnet-20241022",
        "sdk": "anthropic",
    },
}


def call_llm(
    system_prompt: str,
    user_prompt: str,
    provider: str = "gemini",
    model: str = None,
    temperature: float = 0.2,
    max_tokens: int = 1500,
    api_key: str = None,
) -> str:
    """
    Call the specified LLM provider and return the response text.

    Parameters
    ----------
    system_prompt : str
        The system-level instruction.
    user_prompt : str
        The user message.
    provider : str
        One of: gemini, groq, openai, claude.
    model : str or None
        Model name. If None, uses the provider default.
    temperature : float
        Sampling temperature (0.0–1.0).
    max_tokens : int
        Maximum tokens in the response.
    api_key : str or None
        API key. If None, reads from the relevant environment variable.

    Returns
    -------
    str
        The model's response text.
    """
    provider = provider.lower()
    if provider not in PROVIDER_CONFIG:
        raise ValueError(f"Unknown provider '{provider}'. Choose from: {list(PROVIDER_CONFIG)}")

    cfg = PROVIDER_CONFIG[provider]
    key = api_key or os.environ.get(cfg["env_key"])
    if not key:
        raise EnvironmentError(
            f"No API key found for provider '{provider}'. "
            f"Set the environment variable {cfg['env_key']} or pass api_key= explicitly."
        )
    model = model or cfg["default_model"]

    if cfg["sdk"] == "anthropic":
        import anthropic
        client = anthropic.Anthropic(api_key=key)
        message = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return message.content[0].text

    else:  # openai-compatible
        import openai
        client = openai.OpenAI(api_key=key, base_url=cfg["base_url"])
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content


def get_client_info(provider: str, model: str = None) -> str:
    """Return a documentation string for the prompt log."""
    cfg = PROVIDER_CONFIG.get(provider.lower(), {})
    model = model or cfg.get("default_model", "unknown")
    return f"Provider: {provider} | Model: {model} | Temperature: 0.2"

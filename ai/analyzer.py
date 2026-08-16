"""Dispatches crop-analysis requests to whichever AI provider is configured.

KisanLens is built provider-agnostic on purpose: app.py and every UI
component call analyze_crop() without knowing or caring which AI backend is
behind it. Today that's Gemini (free). Later, flipping KISANLENS_PROVIDER to
"openai" in .env is the only change needed to upgrade - no code edits, no UI
changes.
"""

import os

from .schemas import CropAnalysis

PROVIDER_LABELS = {"gemini": "Google Gemini", "openai": "OpenAI"}
DEFAULT_PROVIDER = "gemini"


def get_active_provider() -> str:
    """Return the configured provider key ('gemini' or 'openai')."""
    raw = os.getenv("KISANLENS_PROVIDER", DEFAULT_PROVIDER).strip().lower()
    if not raw:
        return DEFAULT_PROVIDER
    if raw not in PROVIDER_LABELS:
        raise RuntimeError(
            f"Unknown KISANLENS_PROVIDER '{raw}' in .env. Use 'gemini' or 'openai'."
        )
    return raw


def get_active_provider_label() -> str:
    """Human-readable provider name for display in the UI."""
    return PROVIDER_LABELS[get_active_provider()]


def analyze_crop(image_bytes: bytes, mime_type: str = "image/jpeg", language: str = "English") -> CropAnalysis:
    """Run one crop-image analysis through the active AI provider.

    Raises RuntimeError with a farmer/judge-readable message on any failure
    (missing key, rate limit, network issue). app.py already catches this and
    offers Demo Mode as a fallback, so callers don't need to handle it twice.
    """
    provider = get_active_provider()

    if provider == "openai":
        from .providers.openai_provider import analyze
    else:
        from .providers.gemini_provider import analyze

    return analyze(image_bytes, mime_type, language)

"""Google Gemini vision provider - the default, free AI backend for KisanLens.

Gemini is the default because Google AI Studio issues a free API key in a
couple of minutes with no credit card and no billing setup, and the free
tier comfortably covers a hackathon demo (image input + structured JSON
output). Get a key at https://aistudio.google.com/apikey and put it in your
.env file as GEMINI_API_KEY.

Docs: https://ai.google.dev/gemini-api/docs
"""

import os

from google import genai
from google.genai import types

from ..prompts import SYSTEM_PROMPT, USER_PROMPT
from ..schemas import CropAnalysis

# gemini-2.5-flash is a well-established model that has stayed on Google's
# free tier for a long time, so it's the safest default for a demo. Newer
# models (check https://ai.google.dev/gemini-api/docs/models) can be tried
# without touching code by setting KISANLENS_GEMINI_MODEL in .env.
DEFAULT_MODEL = "gemini-2.5-flash"


def analyze(image_bytes: bytes, mime_type: str, language: str) -> CropAnalysis:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Get a free key (no credit card needed) "
            "at https://aistudio.google.com/apikey and add it to your .env file."
        )

    model = os.getenv("KISANLENS_GEMINI_MODEL", DEFAULT_MODEL)
    client = genai.Client(api_key=api_key)

    user_text = USER_PROMPT + (
        "\nThe user selected Hindi as the report language, so make the Hindi fields especially clear."
        if language == "Hindi"
        else ""
    )
    image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)

    try:
        response = client.models.generate_content(
            model=model,
            contents=[user_text, image_part],
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                response_mime_type="application/json",
                response_schema=CropAnalysis,
            ),
        )
    except Exception as exc:
        raise RuntimeError(_friendly_gemini_error(exc)) from exc

    if getattr(response, "parsed", None) is not None:
        return response.parsed

    # Fallback: validate the raw JSON text ourselves in case a future
    # SDK/model combination doesn't auto-populate `.parsed`.
    if getattr(response, "text", None):
        return CropAnalysis.model_validate_json(response.text)

    raise RuntimeError(
        "Gemini did not return a usable result. Try a clearer, well-lit photo, "
        "or switch to Demo Mode."
    )


def _friendly_gemini_error(exc: Exception) -> str:
    message = str(exc)
    if "RESOURCE_EXHAUSTED" in message or "429" in message:
        return (
            "Gemini's free tier briefly rate-limits requests (a handful per "
            "minute). Wait ~30 seconds and try again, or switch to Demo Mode "
            "for the rest of the presentation."
        )
    if "API_KEY_INVALID" in message or "API key not valid" in message:
        return (
            "That GEMINI_API_KEY looks invalid. Double-check it at "
            "https://aistudio.google.com/apikey (keys usually start with 'AIza')."
        )
    if "PERMISSION_DENIED" in message:
        return (
            "Gemini rejected this request (permission denied). Confirm the API "
            "key is active at https://aistudio.google.com/apikey."
        )
    return f"Gemini request failed: {message}"

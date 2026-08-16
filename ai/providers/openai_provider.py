"""OpenAI vision provider - optional upgrade path for KisanLens.

Not used by default (see ai/analyzer.py) because it needs a paid API key.
When the project is ready for it, switch by setting in .env:

    KISANLENS_PROVIDER=openai
    OPENAI_API_KEY=your_key_here

No other code changes needed - app.py and the UI call the same analyze_crop()
function regardless of which provider is active.
"""

import base64
import json
import os

from openai import OpenAI

from ..prompts import SYSTEM_PROMPT, USER_PROMPT
from ..schemas import CropAnalysis

# OpenAI's model lineup moves fast; if this default ever 404s, check
# https://platform.openai.com/docs/models and set KISANLENS_OPENAI_MODEL.
DEFAULT_MODEL = "gpt-5.5"


def _parse_fallback(text: str) -> CropAnalysis:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
    data = json.loads(cleaned)
    return CropAnalysis.model_validate(data)


def analyze(image_bytes: bytes, mime_type: str, language: str) -> CropAnalysis:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is missing. Add it to your .env file, or set "
            "KISANLENS_PROVIDER=gemini to use the free backend instead."
        )

    client = OpenAI(api_key=api_key)
    model = os.getenv("KISANLENS_OPENAI_MODEL", DEFAULT_MODEL)

    encoded = base64.b64encode(image_bytes).decode("utf-8")
    image_data_url = f"data:{mime_type};base64,{encoded}"

    user_text = USER_PROMPT + (
        "\nThe user selected Hindi as the report language, so make the Hindi fields especially clear."
        if language == "Hindi"
        else ""
    )

    content = [
        {"type": "input_text", "text": user_text},
        {"type": "input_image", "image_url": image_data_url},
    ]
    input_payload = [{"role": "user", "content": content}]

    # Preferred path: SDK structured parsing into the Pydantic model.
    try:
        response = client.responses.parse(
            model=model,
            instructions=SYSTEM_PROMPT,
            input=input_payload,
            text_format=CropAnalysis,
        )
        if getattr(response, "output_parsed", None) is not None:
            return response.output_parsed
        if getattr(response, "output_text", None):
            return _parse_fallback(response.output_text)
    except Exception as parse_error:
        # Fallback keeps the project usable across SDK/model combinations.
        fallback_error = parse_error
    else:
        fallback_error = None

    # Compatibility fallback using JSON schema directly.
    schema = CropAnalysis.model_json_schema()

    def make_openai_strict(schema_part):
        if isinstance(schema_part, dict):
            if schema_part.get("type") == "object":
                # OpenAI Structured Outputs requires this.
                schema_part["additionalProperties"] = False
                properties = schema_part.get("properties", {})
                if properties:
                    schema_part["required"] = list(properties.keys())
            for value in schema_part.values():
                make_openai_strict(value)
        elif isinstance(schema_part, list):
            for item in schema_part:
                make_openai_strict(item)

    make_openai_strict(schema)

    response = client.responses.create(
        model=model,
        instructions=SYSTEM_PROMPT,
        input=input_payload,
        text={
            "format": {
                "type": "json_schema",
                "name": "crop_analysis",
                "strict": True,
                "schema": schema,
            }
        },
    )

    if not getattr(response, "output_text", None):
        raise RuntimeError(f"No structured result returned by OpenAI. {fallback_error or ''}")

    return _parse_fallback(response.output_text)

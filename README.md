# 🌱 KisanLens

**See the problem. Understand the crop. Take action.**

KisanLens is a Python + Streamlit hackathon MVP for AI-assisted crop-health visual assessment. A user uploads a crop/leaf photo, the app sends the image to a vision-capable AI model, and the UI presents a structured, farmer-friendly report.

## What is included

- Modern responsive Streamlit UI
- Drag-and-drop image upload, with automatic resizing of large phone photos
- Live AI vision analysis — **free by default**, via Google Gemini
- Provider-agnostic AI layer: switch to OpenAI later by changing one setting, no code changes
- Structured Pydantic result model
- Crop identification, possible issue / health status, AI confidence estimate, severity
- Observed visual symptoms, immediate actions, prevention guidance
- Expert-help escalation
- English + Hindi report fields
- Low-quality / non-plant / healthy-looking handling
- Demo Mode for reliable hackathon presentations if wifi or an API ever fails mid-pitch
- No database, login, payment, IoT, custom ML training, or unnecessary infrastructure

## Run locally

### 1. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get a free API key and configure it

Copy `.env.example` to `.env`:

```bash
cp .env.example .env      # macOS/Linux
copy .env.example .env    # Windows
```

Then get a **free** Gemini API key — no credit card, ready in about two minutes:

1. Go to <https://aistudio.google.com/apikey>
2. Sign in with a Google account
3. Click **Create API key**
4. Paste it into `.env` as `GEMINI_API_KEY=...`

That's it — `KISANLENS_PROVIDER=gemini` is already the default in `.env.example`, so no other setting needs to change.

Do **not** put the API key in source code or commit `.env` to GitHub (it's already in `.gitignore`).

### 4. Start KisanLens

```bash
streamlit run app.py
```

The browser should open the local Streamlit app. The sidebar shows "🔌 Powered by Google Gemini" when Live AI Analysis is selected, confirming the key is picked up.

## Upgrading to OpenAI later

The AI layer was built provider-agnostic on purpose, so this project isn't locked into one vendor. When you're ready to pay for OpenAI (e.g. after advancing to a later round), just edit `.env`:

```text
KISANLENS_PROVIDER=openai
OPENAI_API_KEY=your_key_here
```

No code changes needed — `app.py` and every UI component call the same `analyze_crop()` function regardless of which provider is behind it.

## Hackathon demo plan

1. Open KisanLens.
2. Show the upload area and explain the user problem.
3. Upload a crop image and click **Analyze My Crop** on **Live AI Analysis** — this is now a real, working AI call.
4. Walk through the assessment, symptoms, actions, prevention, and responsible-AI notice.
5. Switch the sidebar language to **Hindi** and show the farmer-friendly explanation.
6. Keep **Demo Mode** in your back pocket only if venue wifi or the free-tier rate limit becomes an issue mid-pitch — mention out loud that it's a fallback, not the main event, so judges know Live AI Analysis is the real thing.

## Architecture

```text
Crop image
    ↓
Streamlit UI (app.py)
    ↓
utils/image.py  →  resized, compressed JPEG bytes
    ↓
ai/analyzer.py  →  reads KISANLENS_PROVIDER, picks a backend
    ↓                                   ↓
ai/providers/gemini_provider.py   ai/providers/openai_provider.py
   (default, free)                     (optional, paid)
    ↓                                   ↓
        Vision + structured JSON output
                    ↓
            Pydantic CropAnalysis
                    ↓
       Result cards + Hindi explanation
```

## Responsible AI choices

KisanLens intentionally does not claim that a single photograph can establish a definitive disease diagnosis.

The model is instructed to:

- avoid certainty from limited visual evidence
- recognize insufficient images
- recognize non-plant images
- distinguish healthy-looking from symptomatic
- explain visible evidence
- avoid hazardous pesticide dosing
- recommend professional help for serious or uncertain cases

The displayed "confidence" is explicitly an **AI confidence estimate**, not a scientifically validated accuracy measurement.

**Free-tier data note:** Google's free Gemini API tier may use submitted prompts/images to improve their models (this is standard for free tiers, not specific to KisanLens). Fine for a hackathon demo with sample crop photos; worth knowing if you ever handle sensitive images.

## What this MVP intentionally does not include

- Authentication
- User accounts
- Database
- Payments
- Marketplace
- IoT sensors
- Custom CNN/model training
- TensorFlow/PyTorch training pipeline
- Weather API
- Expert chat
- Social network
- Farm management suite

These are future roadmap ideas, not 4-hour MVP requirements.

## Troubleshooting

### "GEMINI_API_KEY is missing"

Create `.env` from `.env.example` (see step 3 above) and add your free key from <https://aistudio.google.com/apikey>.

### Live AI request fails with a rate-limit message

Gemini's free tier allows roughly 10-15 requests per minute. Wait ~30 seconds and try again, or switch to Demo Mode for the rest of a live presentation. This is expected behavior on a free tier, not a bug.

### Live AI request fails for another reason

Switch to **Demo Mode** to keep the presentation moving. Then check:

- the API key is valid (regenerate at <https://aistudio.google.com/apikey> if unsure)
- internet connection works
- `KISANLENS_PROVIDER` in `.env` matches which key you actually set

### The model gives a cautious answer

That is intentional. KisanLens is designed to say "insufficient evidence" instead of confidently inventing a disease.

## Presentation one-liner

> KisanLens uses AI vision to analyze a photo of a crop, identify possible visible health issues, explain the evidence in simple language, and provide actionable first-step guidance to farmers — built on a free AI backend so the team can prove the concept before spending anything.

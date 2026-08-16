import streamlit as st
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

from ai.analyzer import analyze_crop, get_active_provider_label
from components.landing import render_landing
from components.results import render_results
from demo.sample_results import DEMO_ANALYSIS
from utils.image import image_to_jpeg_bytes, validate_image
from utils.translations import render_hindi_section

try:
    PROVIDER_LABEL = get_active_provider_label()
except RuntimeError:
    # A bad KISANLENS_PROVIDER value should never take down the whole app -
    # Demo Mode must keep working no matter what. Live AI Analysis will
    # still surface the real error when someone tries to use it.
    PROVIDER_LABEL = "Unknown"

st.set_page_config(
    page_title="KisanLens — AI Crop Health Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
  --green-950:#0d2f1b;
  --green-900:#123d23;
  --green-800:#166534;
  --green-700:#198754;
  --green-500:#22c55e;
  --mint:#eaf8ee;
  --cream:#f8fbf7;
  --ink:#17201a;
  --muted:#66736a;
  --line:#dfe9e2;
  --amber:#f59e0b;
  --red:#ef4444;
}

html, body, [class*="css"] {
  font-family: 'DM Sans', sans-serif;
}

.stApp {
  background:
    radial-gradient(circle at 10% 0%, rgba(34,197,94,.10), transparent 28%),
    radial-gradient(circle at 90% 10%, rgba(22,101,52,.08), transparent 30%),
    var(--cream);
}

.block-container {
  max-width: 1180px;
  padding-top: 2rem;
  padding-bottom: 4rem;
}

.hero {
  padding: 3.4rem 2.8rem;
  border: 1px solid rgba(255,255,255,.65);
  border-radius: 30px;
  background: linear-gradient(135deg, #123d23 0%, #166534 55%, #1f8a4c 100%);
  color: white;
  box-shadow: 0 24px 70px rgba(13,47,27,.20);
  position: relative;
  overflow: hidden;
}
.hero:after {
  content:"";
  position:absolute;
  width:280px;height:280px;
  border-radius:50%;
  right:-70px;top:-100px;
  background:rgba(255,255,255,.08);
}
.eyebrow {
  text-transform:uppercase;
  letter-spacing:.14em;
  font-size:.78rem;
  font-weight:800;
  opacity:.82;
}
.hero h1 {
  font-family:'Manrope',sans-serif;
  font-size:clamp(2.4rem,6vw,4.8rem);
  line-height:.98;
  margin:.55rem 0 1rem;
  letter-spacing:-.05em;
}
.hero p {
  max-width:720px;
  font-size:1.1rem;
  line-height:1.65;
  opacity:.92;
}

.card {
  background:rgba(255,255,255,.82);
  border:1px solid var(--line);
  border-radius:22px;
  padding:1.25rem 1.35rem;
  box-shadow:0 12px 35px rgba(13,47,27,.06);
  backdrop-filter:blur(10px);
}
.section-title {
  font-family:'Manrope',sans-serif;
  font-size:1.35rem;
  font-weight:800;
  color:var(--green-950);
  margin:.2rem 0 .8rem;
}
.muted { color:var(--muted); }
.badge {
  display:inline-flex;
  align-items:center;
  gap:.4rem;
  border-radius:999px;
  padding:.38rem .72rem;
  font-size:.78rem;
  font-weight:800;
  background:var(--mint);
  color:var(--green-800);
}
.metric {
  border:1px solid var(--line);
  border-radius:18px;
  padding:1rem;
  background:white;
}
.metric-label { color:var(--muted); font-size:.78rem; font-weight:700; text-transform:uppercase; letter-spacing:.08em; }
.metric-value { color:var(--green-950); font-family:'Manrope',sans-serif; font-size:1.55rem; font-weight:800; margin-top:.25rem; }
.action-item {
  padding:.75rem 0;
  border-bottom:1px solid #edf2ee;
}
.action-item:last-child { border-bottom:0; }
.disclaimer {
  border:1px solid #f5dfac;
  background:#fff9e9;
  color:#664d0b;
  border-radius:18px;
  padding:1rem 1.1rem;
  font-size:.9rem;
  line-height:1.55;
}
.footer {
  text-align:center;
  color:#7b887f;
  font-size:.82rem;
  margin-top:3rem;
}
div[data-testid="stFileUploader"] {
  border:1.5px dashed #9dc5a8;
  border-radius:20px;
  background:rgba(234,248,238,.55);
  padding:.4rem;
}
.stButton > button {
  border-radius:13px;
  border:1px solid #cfe1d3;
  font-weight:800;
  min-height:2.75rem;
}
.stButton > button[kind="primary"] {
  background:linear-gradient(135deg,#166534,#22a35b);
  border:0;
  box-shadow:0 10px 22px rgba(22,101,52,.18);
}
[data-testid="stSidebar"] {
  background:#f1f8f2;
  border-right:1px solid #dfe9e2;
}
.smallcaps {
  text-transform:uppercase;
  letter-spacing:.1em;
  font-size:.72rem;
  font-weight:800;
  color:#738078;
}
</style>
""", unsafe_allow_html=True)

if "analysis" not in st.session_state:
    st.session_state.analysis = None
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.markdown("## 🌱 KisanLens")
    st.caption("AI Crop Health Intelligence")
    st.divider()
    mode = st.radio(
        "Experience",
        ["Live AI Analysis", "Demo Mode"],
        help="Use Demo Mode if you are offline or want a guaranteed hackathon-stage walkthrough.",
    )
    if mode == "Live AI Analysis":
        st.caption(f"🔌 Powered by {PROVIDER_LABEL}")
    language = st.selectbox("Report language", ["English", "Hindi"])
    st.divider()
    st.markdown("**Responsible AI**")
    st.caption(
        "KisanLens provides a preliminary visual assessment. "
        "It does not replace a qualified agricultural professional."
    )
    if st.session_state.history:
        st.markdown("**Recent analyses**")
        for item in st.session_state.history[-4:][::-1]:
            st.caption(f"{item['crop']} · {item['issue']}")

if st.session_state.analysis is None:
    render_landing()

    uploaded = st.file_uploader(
        "Drop a crop/leaf image here, or click to browse",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed",
    )

    if uploaded:
        try:
            image = Image.open(uploaded).convert("RGB")
            st.session_state.uploaded_image = image
            st.image(image, caption="Image ready for analysis", use_container_width=True)

            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                analyze_clicked = st.button("🔬 Analyze My Crop", type="primary", use_container_width=True)
            with c2:
                if st.button("↻ Change Image", use_container_width=True):
                    st.session_state.uploaded_image = None
                    st.rerun()

            if analyze_clicked:
                ok, message = validate_image(image)
                if not ok:
                    st.error(message)
                elif mode == "Demo Mode":
                    st.session_state.analysis = DEMO_ANALYSIS.model_copy()
                    st.session_state.analysis.demo_mode = True
                    st.rerun()
                else:
                    with st.status("🌱 KisanLens is analyzing your crop…", expanded=True) as status:
                        st.write("✓ Examining visible symptoms")
                        st.write("✓ Checking image quality and plant context")
                        st.write("✓ Assessing possible health issues")
                        st.write("✓ Preparing farmer-friendly guidance")
                        try:
                            image_bytes = image_to_jpeg_bytes(image)
                            result = analyze_crop(image_bytes, language=language)
                            st.session_state.analysis = result
                            st.session_state.history.append({
                                "crop": result.crop_name,
                                "issue": result.possible_issue,
                            })
                            status.update(label="Analysis complete ✓", state="complete", expanded=False)
                            st.rerun()
                        except Exception as exc:
                            status.update(label="Analysis could not be completed", state="error", expanded=True)
                            st.error(
                                "The live AI request failed. You can switch to Demo Mode and "
                                "continue your presentation. Technical detail: " + str(exc)
                            )
        except Exception:
            st.error("That file could not be opened as an image. Please try JPG, PNG, or WEBP.")
    else:
        st.markdown(
            '<div class="card"><div class="section-title">How it works</div>'
            '<div class="muted">① Upload &nbsp; → &nbsp; ② Analyze &nbsp; → &nbsp; '
            '③ Understand &nbsp; → &nbsp; ④ Take action</div></div>',
            unsafe_allow_html=True,
        )

else:
    if st.button("← Analyze another crop"):
        st.session_state.analysis = None
        st.session_state.uploaded_image = None
        st.rerun()

    render_results(st.session_state.analysis, st.session_state.uploaded_image)

    if language == "Hindi":
        render_hindi_section(st.session_state.analysis)

st.markdown(
    '<div class="footer">KisanLens · Built for responsible AI-assisted agricultural guidance · '
    'Not a professional diagnosis</div>',
    unsafe_allow_html=True,
)

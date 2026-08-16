import streamlit as st


def _severity_label(severity: str) -> str:
    return {
        "low": "🟢 LOW",
        "moderate": "🟠 MODERATE",
        "high": "🔴 HIGH",
        "not_assessable": "⚪ NOT ASSESSABLE",
    }.get(severity, severity.upper())


def render_results(result, image=None):
    if getattr(result, "demo_mode", False):
        st.info("🎬 Demo Mode — this result is preloaded for a reliable presentation fallback.")

    if image is not None:
        left, right = st.columns([1, 1.6], gap="large")
        with left:
            st.image(image, caption="Analyzed image", use_container_width=True)
        with right:
            _hero(result)
    else:
        _hero(result)

    st.write("")
    a, b = st.columns(2, gap="large")
    with a:
        _list_card("🔍 What KisanLens observed", result.observed_symptoms, empty="No clear visual symptoms.")
    with b:
        _list_card("🌱 What you can do now", result.immediate_actions, numbered=True)

    st.write("")
    _list_card("🛡️ Prevention", result.prevention_steps)

    if result.expert_help_recommended:
        st.markdown(
            f'<div class="card" style="border-color:#f3d58b;background:#fffaf0">'
            f'<div class="section-title">📋 When to seek expert help</div>'
            f'<div class="muted">{result.expert_help_reason or "Consider speaking with a qualified agricultural professional."}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    if result.image_quality != "good" or result.assessment_status == "insufficient_evidence":
        st.write("")
        st.warning(
            "Try a closer, well-lit photo with the affected leaf in focus. "
            "Include both healthy and affected parts when possible."
        )

    st.write("")
    st.markdown(
        '<div class="disclaimer"><strong>⚠️ Responsible AI notice</strong><br>'
        'KisanLens provides an AI-generated preliminary assessment based on the uploaded image. '
        'It is not a definitive diagnosis. For serious, rapidly spreading, or uncertain crop problems, '
        'consult a qualified agricultural professional.</div>',
        unsafe_allow_html=True,
    )


def _hero(result):
    st.markdown(
        f"""
        <div class="card">
          <div class="badge">🌱 CROP HEALTH ASSESSMENT</div>
          <h2 style="font-family:Manrope;font-size:2rem;margin:.75rem 0 .2rem;color:#0d2f1b">
            {result.crop_name}
          </h2>
          <div class="muted" style="font-size:1.05rem;margin-bottom:1.2rem">
            {result.possible_issue}
          </div>
          <div style="font-size:1rem;line-height:1.55;margin-bottom:1rem">
            {result.farmer_summary}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            f'<div class="metric"><div class="metric-label">AI confidence estimate</div>'
            f'<div class="metric-value">{result.confidence}%</div>'
            f'<div class="muted" style="font-size:.75rem">Not a validated accuracy score</div></div>',
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f'<div class="metric"><div class="metric-label">Severity</div>'
            f'<div class="metric-value">{_severity_label(result.severity)}</div></div>',
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f'<div class="metric"><div class="metric-label">Image quality</div>'
            f'<div class="metric-value">{result.image_quality.title()}</div></div>',
            unsafe_allow_html=True,
        )


def _list_card(title, items, numbered=False, empty="Nothing specific to report."):
    if not items:
        items = [empty]
    rows = []
    for i, item in enumerate(items, start=1):
        prefix = f"<strong>{i}.</strong>" if numbered else "•"
        rows.append(f'<div class="action-item">{prefix}&nbsp; {item}</div>')
    st.markdown(
        f'<div class="card"><div class="section-title">{title}</div>{"".join(rows)}</div>',
        unsafe_allow_html=True,
    )

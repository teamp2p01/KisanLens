import streamlit as st


def render_hindi_section(result):
    st.write("")
    st.markdown(
        '<div class="card">'
        '<div class="badge">🇮🇳 हिंदी में समझाएं</div>'
        f'<h3 style="font-family:Manrope;color:#0d2f1b;margin:.75rem 0 .4rem">'
        f'{result.farmer_summary_hindi or "इस तस्वीर के आधार पर प्रारंभिक जानकारी नीचे दी गई है।"}</h3>'
        '</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2, gap="large")
    with c1:
        _hindi_list("🌱 अभी क्या करें", result.immediate_actions_hindi)
    with c2:
        _hindi_list("🛡️ बचाव के तरीके", result.prevention_steps_hindi)


def _hindi_list(title, items):
    rows = "".join(
        f'<div class="action-item">•&nbsp; {item}</div>'
        for item in (items or ["कोई विशेष सुझाव उपलब्ध नहीं है।"])
    )
    st.markdown(
        f'<div class="card"><div class="section-title">{title}</div>{rows}</div>',
        unsafe_allow_html=True,
    )

import streamlit as st


def render_landing():
    st.markdown(
        """
        <section class="hero">
          <div class="eyebrow">AI + Agriculture · Responsible Crop Intelligence</div>
          <h1>See the problem.<br>Understand the crop.<br>Take action.</h1>
          <p>
            KisanLens turns a simple crop photo into a cautious, farmer-friendly health assessment:
            what the AI can see, what might be happening, how serious it appears, and what to do next.
          </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    cols = st.columns(4)
    items = [
        ("📷", "Upload", "Use a clear photo of the affected crop or leaf."),
        ("🔬", "Analyze", "AI vision checks visible symptoms and image quality."),
        ("🌱", "Understand", "Get simple explanations and practical next steps."),
        ("🛡️", "Act responsibly", "Low-confidence cases are surfaced instead of guessed."),
    ]
    for col, (icon, title, text) in zip(cols, items):
        with col:
            st.markdown(
                f'<div class="card"><div style="font-size:1.7rem">{icon}</div>'
                f'<div class="section-title" style="font-size:1rem">{title}</div>'
                f'<div class="muted" style="font-size:.88rem">{text}</div></div>',
                unsafe_allow_html=True,
            )

    st.write("")
    st.markdown(
        '<div class="smallcaps">Designed for a farmer-first experience</div>'
        '<h2 style="font-family:Manrope;margin:.3rem 0 .4rem;color:#0d2f1b">'
        'From photograph to practical guidance.</h2>',
        unsafe_allow_html=True,
    )
    st.caption(
        "KisanLens is intentionally designed as a first layer of assistance, not as a replacement "
        "for agricultural experts."
    )

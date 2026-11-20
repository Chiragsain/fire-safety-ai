import random

import streamlit as st

st.set_page_config(page_title="Fire Safety AI", page_icon="🧯", layout="centered")

st.markdown(
    """
    <style>
    .result {padding: 1rem; border-radius: 12px; text-align: center;
             font-size: 1.2rem; font-weight: 600; margin-top: 0.5rem;}
    .safe {background: #e8f5e9; color: #1b5e20;}
    .danger {background: #ffebee; color: #b71c1c;}
    </style>
    """,
    unsafe_allow_html=True,
)

EXTINGUISHER_SVG = """
<svg viewBox="0 0 300 300" xmlns="http://www.w3.org/2000/svg" width="200">
  <ellipse cx="150" cy="285" rx="80" ry="10" fill="#00000030"/>
  <rect x="115" y="30" width="70" height="40" rx="8" fill="#333"/>
  <path d="M185 45 Q230 40 235 110" stroke="#333" stroke-width="10" fill="none"/>
  <rect x="100" y="70" width="100" height="210" rx="38" fill="#d32f2f"/>
  <rect x="100" y="150" width="100" height="60" fill="#ffffff"/>
  <text x="150" y="176" text-anchor="middle" font-size="20" font-weight="bold" fill="#d32f2f">FIRE</text>
  <text x="150" y="196" text-anchor="middle" font-size="11" fill="#333">EXTINGUISHER</text>
</svg>
"""

FIRE_CATEGORIES = {
    "Electrical": "Cut the power first, then use a CO2 or dry powder extinguisher. Never use water.",
    "Cooking oil": "Turn off the heat and cover the pan with a lid. Never pour water on it.",
    "Paper / wood": "Water or a dry powder extinguisher works well on ordinary combustibles.",
    "Gas": "Shut off the gas supply if it is safe. Move away and call emergency services.",
}

st.title("🧯 Fire Safety AI")
st.caption("An illustrative web app. It is a concept demo and is not connected to any hardware.")

tab_home, tab_ai, tab_about = st.tabs(["Home", "AI Assistant", "About"])

with tab_home:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(EXTINGUISHER_SVG, unsafe_allow_html=True)
    with col2:
        st.subheader("Smart protection against fire")
        st.write(
            "This concept shows how an AI system could help people spot fires early "
            "and choose the right way to put them out."
        )
        st.markdown(
            "- Detects fire risk from signs such as heat and smoke\n"
            "- Suggests the right extinguishing method\n"
            "- Gives simple safety advice in the moment"
        )

    st.subheader("Choose the right method")
    fire_type = st.selectbox("What is burning?", list(FIRE_CATEGORIES.keys()))
    st.info(FIRE_CATEGORIES[fire_type])

with tab_ai:
    st.subheader("Fire risk scan (simulated)")
    st.write("Press the button to run a simulated AI scan of a room.")

    if st.button("Run AI scan", type="primary"):
        with st.spinner("Analysing heat, smoke and light patterns..."):
            import time
            time.sleep(1.2)
        risk = random.randint(5, 95)
        st.progress(risk / 100, text=f"Fire risk: {risk}%")
        if risk >= 60:
            st.markdown('<div class="result danger">🔥 High risk: leave the area and call for help</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown('<div class="result safe">✅ Low risk: no fire detected</div>',
                        unsafe_allow_html=True)

    st.divider()
    st.subheader("Ask the safety assistant")
    question = st.text_input("Your question", placeholder="e.g. What do I do if a pan catches fire?")
    if question:
        q = question.lower()
        if "pan" in q or "oil" in q or "kitchen" in q:
            answer = FIRE_CATEGORIES["Cooking oil"]
        elif "electric" in q or "wire" in q or "socket" in q:
            answer = FIRE_CATEGORIES["Electrical"]
        elif "gas" in q or "cylinder" in q:
            answer = FIRE_CATEGORIES["Gas"]
        elif "water" in q:
            answer = "Water is only safe on paper and wood fires. Avoid it on electrical, oil and gas fires."
        else:
            answer = "Try asking about a pan fire, an electrical fire, a gas fire, or whether to use water."
        st.write(answer)

with tab_about:
    st.subheader("About this concept")
    st.write(
        "Fire Safety AI is an illustrative web app. It shows how an AI-based fire "
        "safety tool could look and work for users. The scan and assistant are simulated, "
        "and the app is not connected to any physical device."
    )
    st.write("Built with Python and Streamlit.")

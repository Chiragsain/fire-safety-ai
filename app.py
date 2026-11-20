from datetime import datetime

import streamlit as st

st.set_page_config(page_title="Society Fire Alert", page_icon="🚨", layout="wide",
                   initial_sidebar_state="expanded")

BLOCKS = {
    "Block A": [f"A-{n}" for n in range(101, 111)],
    "Block B": [f"B-{n}" for n in range(101, 111)],
    "Independent Houses": [f"House {n}" for n in range(1, 6)],
}
ALL_UNITS = [u for units in BLOCKS.values() for u in units]

FIRE_TYPES = {
    "Kitchen / cooking": ("🍳", [
        "Turn off the gas and the stove if it is safe to reach them.",
        "Cover a pan fire with a lid. Never pour water on an oil fire.",
        "Do not go back inside for belongings.",
    ]),
    "Electrical": ("⚡", [
        "Switch off the main power supply (MCB) only if it is safe.",
        "Use a CO2 or dry powder extinguisher. Never use water on electrical fires.",
        "Do not use the lift.",
    ]),
    "Gas cylinder": ("🧪", [
        "Close the regulator valve only if you can reach it safely.",
        "Move everyone away from the area immediately.",
        "Do not switch lights or electrical items on or off.",
    ]),
    "General / unknown": ("🔥", [
        "Alert others and leave by the staircase.",
        "Close doors behind you to slow the spread of fire.",
        "If there is smoke, stay low and cover your nose and mouth.",
    ]),
}

COMMON_STEPS = [
    "Leave the building by the stairs, never the lift.",
    "Gather at the society assembly point.",
    "Call 101 (Fire) or 112 (Emergency) from a safe place.",
    "Help children, elderly and people with disabilities to exit.",
]

# Edit these to your society's real numbers
CONTACTS = [
    ("🚒", "Fire helpline", "101"),
    ("🆘", "Emergency", "112"),
    ("🚑", "Ambulance", "108"),
    ("🛡️", "Society security desk", "+91 98214 37652"),
    ("📋", "Society secretary", "+91 77031 58946"),
]

HERO_ART = (
    '<div class="hero-art"><svg viewBox="0 0 120 120">'
    '<circle cx="60" cy="60" r="56" fill="rgba(255,255,255,0.15)"/>'
    '<path d="M60 20 L94 33 V62 C94 84 79 98 60 105 C41 98 26 84 26 62 V33 Z" '
    'fill="#ffffff" opacity="0.95"/>'
    '<path class="flame" d="M60 44 C70 56 76 66 74 78 C72 90 48 90 46 78 C44 66 50 56 60 44 Z" '
    'fill="#f97316"/>'
    '</svg></div>'
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp {
  background:
    radial-gradient(at 0% 0%, #fde68a 0px, transparent 50%),
    radial-gradient(at 100% 0%, #f9a8d4 0px, transparent 50%),
    radial-gradient(at 100% 100%, #a5b4fc 0px, transparent 55%),
    radial-gradient(at 0% 100%, #6ee7b7 0px, transparent 45%),
    #fdf4ff;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; max-width: 1250px; }

section[data-testid="stSidebar"] { background: linear-gradient(180deg, #312e81 0%, #701a75 100%); }
section[data-testid="stSidebar"] * { color: #fdf2f8 !important; }

.hero { background: linear-gradient(135deg, #4c1d95 0%, #be185d 50%, #ea580c 100%); color: #fff;
        padding: 2rem 2.4rem; border-radius: 24px; margin-bottom: 1.5rem;
        box-shadow: 0 25px 50px -20px rgba(190, 24, 93, 0.6);
        display: flex; justify-content: space-between; align-items: center; gap: 1rem;
        animation: fadeDown 0.8s ease both; }
.hero h1 { margin: 0; font-size: 2.1rem; font-weight: 700; letter-spacing: -0.5px; }
.hero p { margin: 0.35rem 0 0; opacity: 0.92; font-size: 1rem; }
.hero-art svg { width: 120px; height: 120px; display: block; }
@keyframes fadeDown { from { opacity: 0; transform: translateY(-16px); } to { opacity: 1; transform: none; } }

.flame { transform-origin: 50% 90%; animation: flicker 1.3s ease-in-out infinite; }
@keyframes flicker {
  0%, 100% { transform: scale(1) rotate(-2deg); }
  50% { transform: scale(1.08, 1.12) rotate(2deg); }
}
.float { display: inline-block; animation: float 3s ease-in-out infinite; }
@keyframes float { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-6px); } }

.card { background: rgba(255, 255, 255, 0.94); border-radius: 20px; padding: 1.4rem 1.6rem;
        border: 1px solid #e9d5ff; border-top: 4px solid #a855f7; margin-bottom: 1rem;
        box-shadow: 0 12px 30px -15px rgba(124, 58, 237, 0.35); }
.card h3 { margin: 0 0 0.8rem; font-size: 1.15rem; font-weight: 600;
           background: linear-gradient(90deg, #7c3aed, #db2777); -webkit-background-clip: text;
           background-clip: text; color: transparent; }
.muted { color: #6b7280; font-size: 0.9rem; }

.banner { border-radius: 20px; padding: 1.2rem 1.5rem; color: #fff; margin-bottom: 1rem;
          display: flex; align-items: center; gap: 1rem; box-shadow: 0 15px 30px -15px rgba(0,0,0,.35); }
.banner .icon { font-size: 2.2rem; }
.banner .title { font-weight: 700; font-size: 1.1rem; }
.banner .sub { opacity: 0.95; font-size: 0.92rem; }
.banner-danger { background: linear-gradient(120deg, #be123c 0%, #e11d48 45%, #f97316 100%);
                 animation: pulse 1.8s infinite; }
.banner-warn { background: linear-gradient(120deg, #f59e0b 0%, #facc15 100%); color: #422006; }
.banner-ok { background: linear-gradient(120deg, #0d9488 0%, #059669 50%, #22d3ee 100%); }

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0.55); }
  70% { box-shadow: 0 0 0 16px rgba(225, 29, 72, 0); }
  100% { box-shadow: 0 0 0 0 rgba(225, 29, 72, 0); }
}

.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(118px, 1fr)); gap: 0.7rem; }
.unit { border-radius: 16px; padding: 0.9rem 0.4rem; text-align: center; font-weight: 600;
        font-size: 0.95rem; color: #fff;
        background: linear-gradient(135deg, #34d399 0%, #14b8a6 60%, #06b6d4 100%);
        border: 1px solid rgba(255,255,255,0.4); transition: transform 0.2s;
        box-shadow: 0 6px 14px -8px rgba(20, 184, 166, 0.8); }
.unit:hover { transform: translateY(-4px) scale(1.03); }
.unit small { display: block; font-weight: 400; font-size: 0.72rem; opacity: 0.92; margin-top: 2px; }
.unit.fire { background: linear-gradient(135deg, #be123c 0%, #e11d48 50%, #f97316 100%);
             border-color: transparent; animation: pulse 1.6s infinite;
             box-shadow: 0 8px 18px -8px rgba(225, 29, 72, 0.9); }
.unit.fire small { opacity: 1; }
.block-title { font-weight: 700; color: #7c3aed; margin: 1rem 0 0.5rem; font-size: 0.9rem;
               text-transform: uppercase; letter-spacing: 1.2px; }

.step { display: flex; gap: 0.8rem; align-items: flex-start; padding: 0.6rem 0; color: #3b0764;
        border-bottom: 1px dashed #e9d5ff; font-size: 0.95rem; }
.step:last-child { border-bottom: none; }
.step:hover .num { transform: scale(1.15); }
.num { min-width: 28px; height: 28px; border-radius: 50%; color: #fff; font-size: 0.8rem; font-weight: 700;
       background: linear-gradient(135deg, #7c3aed, #db2777); display: flex; align-items: center;
       justify-content: center; transition: transform 0.2s; box-shadow: 0 4px 10px -4px #db2777; }

.contact { display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0;
           border-bottom: 1px dashed #e9d5ff; color: #3b0764; font-size: 0.95rem; }
.contact:last-child { border-bottom: none; }
.contact a { background: linear-gradient(135deg, #7c3aed, #db2777); color: #fff !important;
             padding: 0.3rem 0.9rem; border-radius: 999px; text-decoration: none; font-weight: 600;
             font-size: 0.85rem; transition: transform 0.2s, box-shadow 0.2s; }
.contact a:hover { transform: scale(1.06); box-shadow: 0 6px 14px -6px rgba(219, 39, 119, 0.7); }

.chip { display: inline-block; padding: 0.2rem 0.75rem; border-radius: 999px; font-size: 0.78rem;
        font-weight: 700; background: #ede9fe; color: #5b21b6; margin-right: 0.35rem; }
.chip.large { background: #fecdd3; color: #9f1239; }
.chip.medium { background: #fde68a; color: #78350f; }
.chip.small { background: #a7f3d0; color: #065f46; }
.chip.resolved { background: #bbf7d0; color: #14532d; }

.alert-row { display: flex; justify-content: space-between; align-items: center; gap: 1rem;
             padding: 0.9rem 1rem; border-radius: 14px; background: #fff1f2; border: 1px solid #fda4af;
             margin-bottom: 0.6rem; }
.alert-row.past { background: #f5f3ff; border-color: #ddd6fe; }
.alert-row .where { font-weight: 700; color: #9f1239; font-size: 1rem; }
.alert-row.past .where { color: #4c1d95; }
.alert-row .meta { color: #6b7280; font-size: 0.85rem; }

.stButton > button { transition: transform 0.15s, box-shadow 0.15s; border-radius: 12px; }
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 18px -8px rgba(124, 58, 237, 0.7); }

.stat { background: linear-gradient(135deg, rgba(249,168,212,0.25), rgba(165,180,252,0.25));
        border: 1px solid rgba(255,255,255,0.2); border-radius: 14px; padding: 0.8rem 1rem; margin-bottom: 0.6rem; }
.stat .n { font-size: 1.6rem; font-weight: 700; color: #fff !important; }
.stat .l { font-size: 0.8rem; opacity: 0.85; }

@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; transition: none !important; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


@st.cache_resource
def _cached_store():
    return {"next_id": 1, "alerts": []}


def shared_store():
    """Alerts shared by everyone running this app (demo only)."""
    store = _cached_store()
    for a in store["alerts"]:
        a.setdefault("safe", [])
    return store


def block_of(unit):
    for block, units in BLOCKS.items():
        if unit in units:
            return block
    return "Society"


def hero(title, subtitle):
    st.markdown(
        f'<div class="hero"><div><h1>{title}</h1><p>{subtitle}</p></div>{HERO_ART}</div>',
        unsafe_allow_html=True)


def unit_grid(units, burning):
    tiles = []
    for u in units:
        if u in burning:
            tiles.append(f'<div class="unit fire">🔥 {u}<small>Fire reported</small></div>')
        else:
            tiles.append(f'<div class="unit">{u}<small>Safe</small></div>')
    return f'<div class="grid">{"".join(tiles)}</div>'


def steps_html(steps):
    return "".join(f'<div class="step"><div class="num">{i + 1}</div><div>{s}</div></div>'
                   for i, s in enumerate(steps))


def contacts_html():
    rows = []
    for icon, label, number in CONTACTS:
        clean = number.replace(" ", "")
        rows.append(f'<div class="contact"><span>{icon} {label}<br>'
                    f'<span class="muted">{number}</span></span>'
                    f'<a href="tel:{clean}">Call</a></div>')
    return "".join(rows)


@st.fragment(run_every=3)
def resident_view():
    store = shared_store()
    active = [a for a in store["alerts"] if a["active"]]

    # Pop-up notification for each new alert, once per session
    seen = st.session_state.setdefault("seen", set())
    for a in store["alerts"]:
        if a["id"] not in seen:
            seen.add(a["id"])
            if a["active"]:
                st.toast(f"🔥 Fire alert: {a['unit']} at {a['time']}", icon="🚨")

    left, right = st.columns([1.25, 1], gap="large")

    with left:
        your_unit = st.selectbox("Your flat / house", ALL_UNITS)

        if active:
            latest = active[-1]
            if latest["unit"] == your_unit:
                st.markdown(
                    f'<div class="banner banner-danger"><div class="icon flame">🔥</div><div>'
                    f'<div class="title">Your home is affected ({latest["unit"]})</div>'
                    f'<div class="sub">Evacuate now using the stairs and call 101.</div></div></div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="banner banner-warn"><div class="icon">🚨</div><div>'
                    f'<div class="title">Fire reported at {latest["unit"]}</div>'
                    f'<div class="sub">{block_of(latest["unit"])} · {latest["time"]} · '
                    f'Severity: {latest["severity"]}</div></div></div>',
                    unsafe_allow_html=True)

            # "I am safe" check-in
            if your_unit in latest["safe"]:
                st.success("✅ You have checked in as safe. Thank you.")
            else:
                if st.button("✅ I am safe", type="primary", use_container_width=True,
                             key=f"safe_{latest['id']}_{your_unit}"):
                    latest["safe"].append(your_unit)
                    st.rerun(scope="fragment")
        else:
            st.markdown(
                '<div class="banner banner-ok"><div class="icon float">✅</div><div>'
                '<div class="title">All clear</div>'
                '<div class="sub">No active fire alerts in the society.</div></div></div>',
                unsafe_allow_html=True)

        burning = {a["unit"] for a in active}
        st.markdown('<div class="card"><h3>Society map</h3>', unsafe_allow_html=True)
        for block, units in BLOCKS.items():
            st.markdown(f'<div class="block-title">{block}</div>{unit_grid(units, burning)}',
                        unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right:
        if active:
            fire_icon, fire_steps = FIRE_TYPES[active[-1]["type"]]
            st.markdown(
                f'<div class="card"><h3>{fire_icon} Steps for {active[-1]["type"]}</h3>'
                f'{steps_html(fire_steps)}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="card"><h3>🛡️ Safety steps for everyone</h3>'
            f'{steps_html(COMMON_STEPS)}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="card"><h3>📞 Emergency contacts</h3>{contacts_html()}</div>',
            unsafe_allow_html=True)


def report_view():
    store = shared_store()
    active = [a for a in store["alerts"] if a["active"]]
    past = [a for a in store["alerts"] if not a["active"]]

    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown('<div class="card"><h3>🚨 Report a fire</h3>', unsafe_allow_html=True)
        with st.form("report_form", border=False):
            unit = st.selectbox("Flat / house where the fire started", ALL_UNITS)
            fire_type = st.selectbox("Type of fire", list(FIRE_TYPES.keys()))
            severity = st.radio("Severity", ["Small", "Medium", "Large"], horizontal=True)
            send = st.form_submit_button("Send alert to all members", type="primary",
                                         use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if send:
            store["alerts"].append({
                "id": store["next_id"],
                "unit": unit,
                "type": fire_type,
                "severity": severity,
                "time": datetime.now().strftime("%H:%M:%S"),
                "active": True,
                "safe": [],
            })
            store["next_id"] += 1
            st.toast(f"Alert sent about {unit}", icon="✅")
            st.rerun()

    with right:
        st.markdown('<div class="card"><h3>Active alerts</h3>', unsafe_allow_html=True)
        if not active:
            st.markdown('<p class="muted">No active alerts. Everything is calm. 🌤️</p>',
                        unsafe_allow_html=True)
        for a in reversed(active):
            sev = a["severity"].lower()
            safe_list = ", ".join(a["safe"]) if a["safe"] else "None yet"
            st.markdown(
                f'<div class="alert-row"><div><div class="where">🔥 {a["unit"]}</div>'
                f'<div class="meta">{a["type"]} · {a["time"]}</div>'
                f'<div class="meta">✅ Checked in ({len(a["safe"])}): {safe_list}</div></div>'
                f'<span class="chip {sev}">{a["severity"]}</span></div>',
                unsafe_allow_html=True)
            if st.button("Mark resolved", key=f"resolve_{a['id']}"):
                a["active"] = False
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card"><h3>📜 Past incidents</h3>', unsafe_allow_html=True)
    if not past:
        st.markdown('<p class="muted">No resolved incidents yet.</p>', unsafe_allow_html=True)
    for a in reversed(past):
        st.markdown(
            f'<div class="alert-row past"><div><div class="where">{a["unit"]}</div>'
            f'<div class="meta">{a["type"]} · {a["severity"]} · {a["time"]}</div>'
            f'<div class="meta">Residents checked in: {len(a["safe"])}</div></div>'
            f'<span class="chip resolved">Resolved</span></div>',
            unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ---------- Layout ----------
store = shared_store()
active_count = sum(1 for a in store["alerts"] if a["active"])

with st.sidebar:
    st.markdown("### 🏘️ Society Fire Alert")
    role = st.radio("I am a", ["Resident", "Report a fire (demo)"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f'<div class="stat"><div class="n">{len(ALL_UNITS)}</div>'
                f'<div class="l">Flats & houses</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="stat"><div class="n">{active_count}</div>'
                f'<div class="l">Active fire alerts</div></div>', unsafe_allow_html=True)
    st.caption("Demo only. Alerts are simulated and shared by everyone running this app.")

if role == "Resident":
    hero("Society Fire Alert", "Stay informed. Stay safe. Know exactly what to do.")
    resident_view()
else:
    hero("Fire Reporting Desk", "Notify every member in seconds with the exact location.")
    report_view()

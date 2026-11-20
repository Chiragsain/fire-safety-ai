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

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }
.stApp { background: radial-gradient(circle at top left, #fff7ed 0%, #f1f5f9 40%, #e0e7ff 100%); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; max-width: 1250px; }

section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0f172a, #1e3a8a); }
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

.hero { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 60%, #ea580c 130%); color: #fff;
        padding: 2rem 2.4rem; border-radius: 24px; margin-bottom: 1.5rem;
        box-shadow: 0 25px 50px -20px rgba(15, 23, 42, 0.55); }
.hero h1 { margin: 0; font-size: 2.1rem; font-weight: 700; letter-spacing: -0.5px; }
.hero p { margin: 0.35rem 0 0; opacity: 0.85; font-size: 1rem; }

.card { background: rgba(255, 255, 255, 0.92); border-radius: 20px; padding: 1.4rem 1.6rem;
        border: 1px solid #e2e8f0; margin-bottom: 1rem;
        box-shadow: 0 10px 30px -15px rgba(15, 23, 42, 0.25); }
.card h3 { margin: 0 0 0.8rem; font-size: 1.15rem; color: #0f172a; font-weight: 600; }
.muted { color: #64748b; font-size: 0.9rem; }

.banner { border-radius: 20px; padding: 1.2rem 1.5rem; color: #fff; margin-bottom: 1rem;
          display: flex; align-items: center; gap: 1rem; box-shadow: 0 15px 30px -15px rgba(0,0,0,.35); }
.banner .icon { font-size: 2.2rem; }
.banner .title { font-weight: 700; font-size: 1.1rem; }
.banner .sub { opacity: 0.92; font-size: 0.92rem; }
.banner-danger { background: linear-gradient(120deg, #dc2626, #f97316); animation: pulse 1.8s infinite; }
.banner-warn { background: linear-gradient(120deg, #f59e0b, #fbbf24); color: #1f2937; }
.banner-ok { background: linear-gradient(120deg, #059669, #34d399); }

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0.55); }
  70% { box-shadow: 0 0 0 16px rgba(220, 38, 38, 0); }
  100% { box-shadow: 0 0 0 0 rgba(220, 38, 38, 0); }
}

.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(118px, 1fr)); gap: 0.7rem; }
.unit { border-radius: 16px; padding: 0.9rem 0.4rem; text-align: center; font-weight: 600;
        font-size: 0.95rem; background: linear-gradient(180deg, #ecfdf5, #d1fae5); color: #065f46;
        border: 1px solid #a7f3d0; transition: transform 0.2s; }
.unit:hover { transform: translateY(-3px); }
.unit small { display: block; font-weight: 400; font-size: 0.72rem; opacity: 0.8; margin-top: 2px; }
.unit.fire { background: linear-gradient(135deg, #dc2626, #f97316); color: #fff; border-color: transparent;
             animation: pulse 1.6s infinite; }
.unit.fire small { opacity: 1; }
.block-title { font-weight: 600; color: #334155; margin: 1rem 0 0.5rem; font-size: 0.95rem;
               text-transform: uppercase; letter-spacing: 1px; }

.step { display: flex; gap: 0.8rem; align-items: flex-start; padding: 0.6rem 0; color: #334155;
        border-bottom: 1px dashed #e2e8f0; font-size: 0.95rem; }
.step:last-child { border-bottom: none; }
.num { min-width: 28px; height: 28px; border-radius: 50%; color: #fff; font-size: 0.8rem; font-weight: 600;
       background: linear-gradient(135deg, #1e3a8a, #6366f1); display: flex; align-items: center;
       justify-content: center; }

.contact { display: flex; justify-content: space-between; align-items: center; padding: 0.65rem 0;
           border-bottom: 1px dashed #e2e8f0; color: #334155; font-size: 0.95rem; }
.contact:last-child { border-bottom: none; }
.contact a { background: #1e3a8a; color: #fff !important; padding: 0.3rem 0.85rem; border-radius: 999px;
             text-decoration: none; font-weight: 600; font-size: 0.85rem; }

.chip { display: inline-block; padding: 0.2rem 0.75rem; border-radius: 999px; font-size: 0.78rem;
        font-weight: 600; background: #e0e7ff; color: #3730a3; margin-right: 0.35rem; }
.chip.large { background: #fee2e2; color: #991b1b; }
.chip.medium { background: #fef3c7; color: #92400e; }
.chip.small { background: #dcfce7; color: #166534; }
.chip.resolved { background: #dcfce7; color: #166534; }

.alert-row { display: flex; justify-content: space-between; align-items: center; gap: 1rem;
             padding: 0.9rem 1rem; border-radius: 14px; background: #fff7ed; border: 1px solid #fed7aa;
             margin-bottom: 0.6rem; }
.alert-row.past { background: #f8fafc; border-color: #e2e8f0; }
.alert-row .where { font-weight: 600; color: #7c2d12; font-size: 1rem; }
.alert-row.past .where { color: #334155; }
.alert-row .meta { color: #64748b; font-size: 0.85rem; }

.stat { background: rgba(255,255,255,0.1); border-radius: 14px; padding: 0.8rem 1rem; margin-bottom: 0.6rem; }
.stat .n { font-size: 1.6rem; font-weight: 700; color: #fff !important; }
.stat .l { font-size: 0.8rem; opacity: 0.8; }
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
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


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
                    f'<div class="banner banner-danger"><div class="icon">🔥</div><div>'
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
                '<div class="banner banner-ok"><div class="icon">✅</div><div>'
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

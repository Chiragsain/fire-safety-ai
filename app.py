from datetime import datetime

import streamlit as st

st.set_page_config(page_title="Society Fire Alert", page_icon="🚨", layout="wide")

BLOCKS = {
    "Block A": [f"A-{n}" for n in range(101, 111)],
    "Block B": [f"B-{n}" for n in range(101, 111)],
    "Independent Houses": [f"House {n}" for n in range(1, 6)],
}
ALL_UNITS = [u for units in BLOCKS.values() for u in units]

FIRE_TYPES = {
    "Kitchen / cooking": [
        "Turn off the gas and the stove if it is safe to reach them.",
        "Cover a pan fire with a lid. Never pour water on an oil fire.",
        "Do not go back inside for belongings.",
    ],
    "Electrical": [
        "Switch off the main power supply (MCB) only if it is safe.",
        "Use a CO2 or dry powder extinguisher. Never use water on electrical fires.",
        "Do not use the lift.",
    ],
    "Gas cylinder": [
        "Close the regulator valve only if you can reach it safely.",
        "Move everyone away from the area immediately.",
        "Do not switch lights or electrical items on or off.",
    ],
    "General / unknown": [
        "Alert others and leave by the staircase.",
        "Close doors behind you to slow the spread of fire.",
        "If there is smoke, stay low and cover your nose and mouth.",
    ],
}

COMMON_STEPS = [
    "Leave the building by the stairs, never the lift.",
    "Gather at the society assembly point.",
    "Call 101 (Fire) or 112 (Emergency) from a safe place.",
    "Help children, elderly and people with disabilities to exit.",
]


@st.cache_resource
def shared_store():
    """Alerts shared by everyone running this app (demo only)."""
    return {"next_id": 1, "alerts": []}


def block_of(unit):
    for block, units in BLOCKS.items():
        if unit in units:
            return block
    return ""


@st.fragment(run_every=3)
def resident_view():
    store = shared_store()
    active = [a for a in store["alerts"] if a["active"]]

    your_unit = st.selectbox("Select your flat / house", ALL_UNITS)

    # Notify about new alerts once per session
    seen = st.session_state.setdefault("seen", set())
    for a in store["alerts"]:
        if a["id"] not in seen:
            seen.add(a["id"])
            if a["active"]:
                st.toast(f"🔥 Fire alert: {a['unit']} ({a['time']})", icon="🚨")

    if active:
        latest = active[-1]
        if latest["unit"] == your_unit:
            st.error(f"🔥 YOUR HOME IS AFFECTED ({latest['unit']}). Evacuate now and call 101.")
        else:
            st.warning(f"🔥 Fire reported at {latest['unit']} ({block_of(latest['unit']) or 'society'}) "
                       f"at {latest['time']}. Severity: {latest['severity']}.")
    else:
        st.success("No active fire alerts in the society.")

    st.subheader("Society map")
    burning = {a["unit"] for a in active}
    for block, units in BLOCKS.items():
        st.markdown(f"**{block}**")
        cols = st.columns(5)
        for i, unit in enumerate(units):
            with cols[i % 5]:
                if unit in burning:
                    st.error(f"{unit} 🔥")
                else:
                    st.success(unit)

    st.subheader("What to do now")
    if active:
        fire_type = active[-1]["type"]
        st.markdown(f"**For this type of fire ({fire_type}):**")
        for step in FIRE_TYPES[fire_type]:
            st.markdown(f"- {step}")
    st.markdown("**For everyone:**")
    for step in COMMON_STEPS:
        st.markdown(f"- {step}")


def report_view():
    st.header("Report a fire (demo)")
    store = shared_store()

    with st.form("report_form"):
        unit = st.selectbox("Flat / house where the fire started", ALL_UNITS)
        fire_type = st.selectbox("Type of fire", list(FIRE_TYPES.keys()))
        severity = st.radio("Severity", ["Small", "Medium", "Large"], horizontal=True)
        send = st.form_submit_button("🚨 Send alert to all members", type="primary")

    if send:
        store["alerts"].append({
            "id": store["next_id"],
            "unit": unit,
            "type": fire_type,
            "severity": severity,
            "time": datetime.now().strftime("%H:%M:%S"),
            "active": True,
        })
        store["next_id"] += 1
        st.success(f"Alert sent to all members about {unit}.")

    st.subheader("Active alerts")
    active = [a for a in store["alerts"] if a["active"]]
    if not active:
        st.write("None.")
    for a in active:
        c1, c2 = st.columns([4, 1])
        c1.write(f"🔥 **{a['unit']}** | {a['type']} | {a['severity']} | {a['time']}")
        if c2.button("Mark resolved", key=f"resolve_{a['id']}"):
            a["active"] = False
            st.rerun()


st.title("🏘️ Society Fire Alert System")
st.sidebar.title("Menu")
role = st.sidebar.radio("I am a", ["Resident", "Report a fire (demo)"])
st.sidebar.caption("Demo only. Alerts are simulated and shared by everyone running this app.")

if role == "Resident":
    resident_view()
else:
    report_view()

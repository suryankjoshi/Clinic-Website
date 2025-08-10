# Home.py
import streamlit as st
from utils.auth import require_auth, logout_button

st.set_page_config(page_title="Clinic Website", page_icon="🏥", layout="wide", initial_sidebar_state="collapsed")
require_auth()
logout_button()

st.markdown("<h1 style='text-align:center;'>Clinic Portal</h1>", unsafe_allow_html=True)
st.caption(f"Logged in as: {st.session_state.user} ({st.session_state.role})")

_, mid, _ = st.columns([1,2,1])
with mid:
    c1, c2 = st.columns(2)
    with c1:
        st.page_link("pages/1_New Patient.py", label="➕ New Patient", help="Add patient demographics", use_container_width=True)
    with c2:
        st.page_link("pages/2_Symptoms (Doctor).py", label="🩺 Symptoms (Doctor)", help="Doctor-only", use_container_width=True)

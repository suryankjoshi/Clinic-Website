# utils/auth.py
import streamlit as st

DEMO_USERS = {
    "doctor@example.com": {"password": "doc123", "role": "doctor"},
    "reception@example.com": {"password": "rec123", "role": "receptionist"},
}

def require_auth():
    if "auth" not in st.session_state:
        st.session_state.auth = False
        st.session_state.role = None
        st.session_state.user = None

    if not st.session_state.auth:
        st.title("Login")
        email = st.text_input("Email")
        pwd = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            user = DEMO_USERS.get(email)
            if user and user["password"] == pwd:
                st.session_state.auth = True
                st.session_state.role = user["role"]
                st.session_state.user = email
                st.rerun()
            else:
                st.error("Invalid email or password.")
        st.stop()  # block the page content when unauthenticated

def logout_button():
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

def guard_doctor():
    if st.session_state.role != "doctor":
        st.warning("Not authorized (Doctor only).")
        st.stop()

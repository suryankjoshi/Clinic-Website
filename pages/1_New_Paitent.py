# pages/1_New Patient.py
import streamlit as st
from utils.auth import require_auth, logout_button
from services.db_dummy import DummyDB

st.set_page_config(page_title="New Patient", page_icon="➕", layout="centered")
require_auth()
logout_button()
db = DummyDB()

st.title("New Patient (Demographics)")
with st.form("new_patient"):
    name = st.text_input("Child's Full Name *")
    dob = st.date_input("Date of Birth *")
    sex = st.selectbox("Sex *", ["Male", "Female", "Other"])
    weight = st.number_input("Weight (kg) *", min_value=0.5, max_value=80.0, step=0.1)
    guardian_name = st.text_input("Parent/Guardian Name *")
    guardian_phone = st.text_input("Parent/Guardian Phone *")  # keep simple; you can add regex later
    height = st.number_input("Height (cm)", min_value=0.0, max_value=200.0, step=0.5)
    allergies = st.text_input("Allergies (comma-separated)")
    address = st.text_area("Address")
    notes = st.text_area("Notes")

    submitted = st.form_submit_button("Save Patient")

if submitted:
    required = [name, dob, sex, weight, guardian_name, guardian_phone]
    if not all(required):
        st.error("Please fill all required fields (*)")
    else:
        pid = db.create_patient({
            "name": name,
            "dob": str(dob),
            "sex": sex,
            "weight_kg": float(weight),
            "height_cm": float(height) if height else None,
            "guardian_name": guardian_name,
            "guardian_phone": guardian_phone,
            "allergies": [a.strip() for a in allergies.split(",")] if allergies else [],
            "address": address,
            "notes": notes,
        })
        st.success(f"Saved! Patient ID: {pid}")
        st.session_state["selected_patient_id"] = pid
        if st.session_state.role == "doctor":
            st.info("You can now open the Symptoms page to continue.")
        else:
            st.info("Reception done. Doctor will proceed with symptoms.")

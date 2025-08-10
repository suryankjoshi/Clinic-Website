# pages/2_Symptoms (Doctor).py
import streamlit as st
from utils.auth import require_auth, logout_button, guard_doctor
from services.db_dummy import DummyDB

st.set_page_config(page_title="Symptoms", page_icon="🩺", layout="wide")
require_auth()
guard_doctor()
logout_button()
db = DummyDB()

SYMPTOMS = [
    "Fever","Cough (dry)","Cough (wet)","Runny nose","Nasal blockage","Sore throat",
    "Ear pain","Ear discharge","Vomiting","Loose stools","Abdominal pain","Rash",
    "Wheeze","Breathlessness","Poor feeding","Lethargy","Decreased urine","Itching"
]
FREQUENCY = ["None","Once/day","2–3/day","Hourly","Every 2–4 hours","Night-only","With feeds"]
SEVERITY  = ["None","1–3 (mild)","4–6 (moderate)","7–10 (severe)"]

st.title("Symptoms (Doctor)")

pid = st.session_state.get("selected_patient_id", "")
pid = st.text_input("Patient ID", value=pid, help="Enter or paste a Patient ID")
patient = db.get_patient(pid) if pid else None

if not patient:
    st.info("Enter a valid Patient ID (from New Patient page) to proceed.")
    st.stop()

st.write(f"**Patient:** {patient['name']} • Sex: {patient['sex']} • Weight: {patient['weight_kg']} kg")

st.markdown("### Record Symptoms")
rows = []
for s in SYMPTOMS:
    with st.expander(s, expanded=False):
        present = st.checkbox(f"Present: {s}", key=f"present_{s}")
        freq = st.selectbox("Frequency", FREQUENCY, index=0, key=f"freq_{s}", disabled=not present)
        sev  = st.selectbox("Severity", SEVERITY, index=0, key=f"sev_{s}", disabled=not present)
        note = st.text_input("Notes", key=f"note_{s}", disabled=not present, placeholder="Optional")
        if present:
            rows.append({"symptom": s, "frequency": freq, "severity": sev, "notes": note})

if st.button("Save Symptoms", type="primary"):
    # In a real app you'd attach to a visit record. For demo, store a simple field on patient.
    db.update_patient(pid, {"_last_symptoms": rows})
    st.success(f"Saved {len(rows)} symptom(s) for patient {pid}.")

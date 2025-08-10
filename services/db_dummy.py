# services/db_dummy.py
import uuid
from typing import Dict, List, Optional
from .db_port import DBPort

_STORE = {"patients": {}}

class DummyDB(DBPort):
    def create_patient(self, data: Dict) -> str:
        pid = str(uuid.uuid4())[:8]
        _STORE["patients"][pid] = {"id": pid, **data}
        return pid

    def update_patient(self, patient_id: str, data: Dict) -> None:
        if patient_id in _STORE["patients"]:
            _STORE["patients"][patient_id].update(data)

    def get_patient(self, patient_id: str) -> Optional[Dict]:
        return _STORE["patients"].get(patient_id)

    def find_patients(self, query: str) -> List[Dict]:
        q = (query or "").strip().lower()
        vals = _STORE["patients"].values()
        return [
            p for p in vals
            if q in p.get("id","").lower()
            or q in p.get("name","").lower()
            or q in p.get("guardian_phone","")
        ]

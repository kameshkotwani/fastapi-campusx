from pydantic import BaseModel
from typing import Optional


# Define a Pydantic model for a patient
class Patient(BaseModel):
    patient_id: str
    name: str
    city: Optional[str] = None
    age: int
    gender: str
    height: float
    weight: float
    bmi: float
    verdict: str

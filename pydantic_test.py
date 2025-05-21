from patient import Patient
from pprint import pprint

# internally python converts the data types if it can.
patient_info: dict = {
    "name": "kamesh kotwani",
    "age": 61,
    "weight": 75.2,
    "height": 1.75,
    "married": True,
    "allergies": ["pollen", "dust"],
    "email": "abc@hdfc.com",
    "contact_details": {"phone": "1234567890", "emergency_contact": "9876543210"},
    "address": {"city": "Indore", "state": "Madhya Pradesh", "pincode": 452001},
}

patient1: Patient = Patient(**patient_info)


def insert_patient(patient: Patient) -> None:
    pprint(patient.model_dump(), sort_dicts=False)

    print("patient inserted successfully")


def update_patient(patient: Patient) -> None:
    print(f"Patient Name: {patient.name}")
    print(f"Patient Age: {patient.age}")
    print("patient updated successfully")


insert_patient(patient1)

pprint(patient1)

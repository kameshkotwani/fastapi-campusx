import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000"

st.title("CRUD Application with FastAPI Backend")

# Read
st.header("View Patients Items")
if st.button("Get All Items"):
    response = requests.get(API_URL + "/view")
    if response.status_code == 200:
        items = response.json()
        # Convert the received dict into a list of records
        data = [details["data"] for _, details in items.items()]
        # Adjust these column names according to your data schema
        df = pd.DataFrame(
            data,
            columns=[
                "Patient ID",
                "Name",
                "City",
                "Age",
                "Gender",
                "Height",
                "Weight",
                "BMI",
                "Verdict",
            ],
        )
        st.table(df)
    else:
        st.error("Failed to fetch items.")
# Create
st.header("Create Patient")

create_name = st.text_input("Name", key="create_name")
create_id = st.text_input("id", key="create_id")
create_age = st.number_input("Age", key="create_age", value=0, min_value=0)
create_weight = st.number_input("Weight (kg)", key="create_weight", value=0.0, step=0.1)
create_height = st.number_input("Height (m)", key="create_height", value=0.0, step=0.1)
create_married = st.checkbox("Married", key="create_married")
create_allergies = st.text_area("Allergies (comma separated)", key="create_allergies")
create_email = st.text_input("Email", key="create_email")

st.subheader("Contact Details")
contact_phone = st.text_input("Phone", key="contact_phone")
contact_emergency = st.text_input("Emergency Contact", key="contact_emergency")

st.subheader("Address")
address_city = st.text_input("City", key="address_city")
address_state = st.text_input("State", key="address_state")
address_pincode = st.text_input("Pincode", key="address_pincode")

if st.button("Create Patient"):
    patient_data = {
        "id": create_id,
        "name": create_name,
        "age": create_age,
        "weight": create_weight,
        "height": create_height,
        "married": create_married,
        "allergies": [a.strip() for a in create_allergies.split(",") if a.strip()],
        "email": create_email,
        "contact_details": {
            "phone": contact_phone,
            "emergency_contact": contact_emergency,
        },
        "address": {
            "city": address_city,
            "state": address_state,
            "pincode": address_pincode,
        },
    }
    response = requests.post(API_URL + "/create", json=patient_data)
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.write(response.json())


# Update
st.header("Update Item")
update_id = st.text_input("Item ID to Update", key="update_id")
update_name = st.text_input("New Name", key="update_name")
update_desc = st.text_input("New Description", key="update_desc")
if st.button("Update"):
    response = requests.put(
        f"{API_URL}/{update_id}", json={"name": update_name, "description": update_desc}
    )
    st.write(response.json())

# Delete
st.header("Delete Item")
delete_id = st.text_input("Item ID to Delete", key="delete_id")
if st.button("Delete"):
    response = requests.delete(f"{API_URL}/{delete_id}")
    if response.ok:
        st.success("Item deleted.")
    else:
        st.error("Failed to delete item.")

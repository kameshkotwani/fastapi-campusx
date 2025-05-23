from fastapi import FastAPI, HTTPException, Depends, Query
from typing import Optional
import sqlite3
from api import Patient


def get_db():
    conn = sqlite3.connect("patients.db")
    try:
        yield conn
    finally:
        print("closing connection")
        conn.close()


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Welcome!"}


@app.get("/view")
def get_items(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients;")
    rows = cursor.fetchall()
    result = {}
    for row in rows:
        result[row[0]] = {"patient_id": row[0], "data": row}
    return result


@app.get("/items/{item_id}")
def read_item(item_id: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (item_id,))
    row = cursor.fetchone()
    if row:
        return {"patient_id": row[0], "data": row}
    else:
        raise HTTPException(status_code=404, detail={"error": "Patient not found"})


@app.get("/sort")
def sort_patients(
    column: str = Query(..., description="sort on the basis of height weight or bmi"),
    order: Optional[str] = Query(
        "asc", description="default is asc mention desc otherwise"
    ),
    db: sqlite3.Connection = Depends(get_db),
):
    valid_fields = ["height", "weight", "bmi"]
    if column not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail={"invalid": f"invalid field request,select from {valid_fields}"},
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400, detail={"invalid": "invalid order,select from [asc,desc]"}
        )

    cursor = db.cursor()

    cursor.execute(f"SELECT * FROM patients ORDER BY {column} {order}")
    column_names = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    result = {}
    for row in rows:
        result[row[0]] = dict(zip(column_names, row))
    return result


@app.post("/create")
def create_item(patient: Patient, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT 1 FROM patients WHERE patient_id = ?", (patient.id,))
    if cursor.fetchone():
        raise HTTPException(
            status_code=400, detail={"error": "Patient with this ID already exists"}
        )
    cursor.execute(
        "INSERT INTO patients (patient_id, name, age, height, weight, bmi,verdict) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            patient.id,
            patient.name,
            patient.age,
            patient.height,
            patient.weight,
            patient.bmi,
            patient.verdict,
        ),
    )
    db.commit()
    return {"message": "Patient created successfully", "patient_id": patient.id}

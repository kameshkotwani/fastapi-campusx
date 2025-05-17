import sqlite3
import json

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('patients.db')
cursor = conn.cursor()

# Create patients table
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    patient_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    age INTEGER,
    gender TEXT,
    height REAL,
    weight REAL,
    bmi REAL,
    verdict TEXT
)
''')

# Sample data
patient_data = {
    "P001": {"name": "Ananya Sharma", "city": "Guwahati", "age": 28, "gender": "female", "height": 1.65, "weight": 90.0, "bmi": 33.06, "verdict": "Obese"},
    "P002": {"name": "Ravi Mehta", "city": "Mumbai", "age": 35, "gender": "male", "height": 1.75, "weight": 85, "bmi": 27.76, "verdict": "Overweight"},
    "P003": {"name": "Sneha Kulkarni", "city": "Pune", "age": 22, "gender": "female", "height": 1.6, "weight": 45, "bmi": 17.58, "verdict": "Underweight"},
    "P004": {"name": "Arjun Verma", "city": "Bangalore", "age": 40, "gender": "male", "height": 1.8, "weight": 95, "bmi": 29.32, "verdict": "Overweight"},
    "P005": {"name": "Neha Sinha", "city": "Kolkata", "age": 30, "gender": "female", "height": 1.55, "weight": 75, "bmi": 31.22, "verdict": "Obese"}
}

# Insert data into the table
for patient_id, details in patient_data.items():
    cursor.execute('''
    INSERT OR REPLACE INTO patients 
    (patient_id, name, city, age, gender, height, weight, bmi, verdict)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        patient_id,
        details['name'],
        details['city'],
        details['age'],
        details['gender'],
        details['height'],
        details['weight'],
        details['bmi'],
        details['verdict']
    ))

# Commit changes and close connection
conn.commit()
print("Database created successfully with sample data.")

# Verify data was inserted by querying the table
cursor.execute("SELECT * FROM patients")
rows = cursor.fetchall()
print(f"\nPatient records in database ({len(rows)}):")
for row in rows:
    print(row)

conn.close()
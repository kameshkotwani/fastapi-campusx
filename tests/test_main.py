import sqlite3
import json
import unittest
from fastapi.testclient import TestClient
from api.main import app, get_db


def override_get_db():
    # Create an in-memory SQLite database connection for testing
    db = sqlite3.connect(":memory:")
    cursor = db.cursor()
    # Create the patients table, storing address as TEXT
    cursor.execute("""
        CREATE TABLE patients (
            patient_id TEXT PRIMARY KEY,
            name TEXT,
            city TEXT,
            age INTEGER,
            gender TEXT,
            height REAL,
            weight REAL,
            bmi REAL,
            verdict TEXT,
            address TEXT
        )
    """)
    # Insert some sample data with the address column converted to JSON
    sample_data = [
        (
            "P001",
            "Ananya Sharma",
            "Guwahati",
            28,
            "female",
            1.65,
            90.0,
            33.06,
            "Obese",
            {"city": "Guwahati", "state": "Assam", "pincode": 781001},
        ),
        (
            "P002",
            "Ravi Mehta",
            "Mumbai",
            35,
            "male",
            1.75,
            85.0,
            27.76,
            "Overweight",
            {"city": "Mumbai", "state": "Maharashtra", "pincode": 400001},
        ),
        (
            "P003",
            "Sneha Kulkarni",
            "Pune",
            22,
            "female",
            1.6,
            45.0,
            17.58,
            "Underweight",
            {"city": "Pune", "state": "Maharashtra", "pincode": 411001},
        ),
    ]
    # Convert the address dict to a JSON string before inserting
    processed_data = []
    for row in sample_data:
        row = list(row)
        row[-1] = json.dumps(row[-1])
        processed_data.append(tuple(row))
    cursor.executemany(
        "INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", processed_data
    )
    db.commit()
    try:
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestAPI(unittest.TestCase):
    def test_root_endpoint(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Welcome!"})

    def test_view_items(self):
        response = client.get("/view")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("P001", data)
        self.assertIn("P002", data)
        self.assertIn("P003", data)

    def test_read_item_found(self):
        response = client.get("/items/P001")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["patient_id"], "P001")
        self.assertIsInstance(data["data"], list)

    def test_read_item_not_found(self):
        response = client.get("/items/P999")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIn("error", data["detail"])

    def test_sort_patients_valid(self):
        response = client.get("/sort", params={"column": "height", "order": "asc"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Verify sorting by checking that heights are in ascending order
        heights = [record["height"] for record in data.values()]
        self.assertEqual(heights, sorted(heights))

    def test_sort_patients_invalid_column(self):
        response = client.get(
            "/sort", params={"column": "invalid_field", "order": "asc"}
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("invalid", data["detail"])

    def test_sort_patients_invalid_order(self):
        response = client.get(
            "/sort", params={"column": "weight", "order": "invalid_order"}
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn("invalid", data["detail"])


if __name__ == "__main__":
    unittest.main()
